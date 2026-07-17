#!/usr/bin/env python3
"""Resolve GitLab Runner releases and create a reviewed manifest candidate.

The offline path consumes a checked-in snapshot and confronts every catalog
hash with the snapshot's recorded official checksum document.  The refresh
path queries only the GitLab Runner Releases API and the version-pinned S3
release metadata.  Neither path mutates the tracked manifest by default.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.11 is the supported runtime
    tomllib = None  # type: ignore[assignment]


REQUIRED_ARCHITECTURES = ("amd64", "arm64", "armhf")
OFFICIAL_PROJECT = "gitlab-org/gitlab-runner"
OFFICIAL_API = "https://gitlab.com/api/v4/projects/gitlab-org%2Fgitlab-runner/releases"
OFFICIAL_RELEASE_PREFIX = "https://gitlab.com/gitlab-org/gitlab-runner/-/releases/"
OFFICIAL_DOWNLOAD_HOSTS = {
    "gitlab-runner-downloads.s3.amazonaws.com",
    "gitlab-runner-downloads.s3.dualstack.us-east-1.amazonaws.com",
}
OFFICIAL_KEY_URL = "https://packages.gitlab.com/runner/gitlab-runner/gpgkey/runner-gitlab-runner-49F16C5CC3A0F81F.pub.gpg"
OFFICIAL_KEY_FINGERPRINT = "931DA69CFA3AFEBBC97DAA8C6C57C29C6BA75A4E"
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
FINGERPRINT_RE = re.compile(r"^[0-9A-F]{40}$")
SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$")
MANIFEST_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)
# The Releases API page includes the complete asset-link matrix for up to 100
# releases. Keep a bounded cap while allowing that official response shape.
MAX_METADATA_BYTES = 8 * 1024 * 1024
MAX_REDIRECTS = 3
GPG_FAILURE_CODES = {
    "BADSIG",
    "ERRSIG",
    "EXPSIG",
    "EXPKEYSIG",
    "KEYEXPIRED",
    "REVKEYSIG",
    "KEYREVOKED",
    "SIGEXPIRED",
    "NO_PUBKEY",
    "NODATA",
    "BADARMOR",
    "FAILURE",
}
REQUIRED_FILENAMES = tuple(
    [f"gitlab-runner_{arch}.deb" for arch in REQUIRED_ARCHITECTURES]
    + ["gitlab-runner-helper-images.deb"]
)
MANIFEST_FIELDS = {
    "version",
    "amd64.url",
    "amd64.sha256",
    "arm64.url",
    "arm64.sha256",
    "armhf.url",
    "armhf.sha256",
    "url",
    "sha256",
}


class ResolutionError(ValueError):
    """Raised when a release cannot be used as an atomic candidate."""


def _normalize_fingerprint(value: Any, field: str) -> str:
    fingerprint = _require_string(value, field).replace(" ", "").upper()
    if not FINGERPRINT_RE.fullmatch(fingerprint):
        raise ResolutionError(f"{field} must be an exact 40-character fingerprint")
    return fingerprint


def _version_key(version: str) -> tuple[int, int, int]:
    match = SEMVER_RE.fullmatch(version)
    if not match:
        raise ResolutionError(f"unsupported release version: {version}")
    return tuple(int(part) for part in match.groups())


def _is_prerelease(release: dict[str, Any]) -> bool:
    tag = str(release.get("tag_name", ""))
    return bool(release.get("stable") is False or release.get("upcoming_release") or "-" in tag.lstrip("v"))


def _require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ResolutionError(f"{field} must be a non-empty string")
    return value


def _validate_url(value: Any, tag: str, field: str) -> str:
    url = _require_string(value, field)
    parsed = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed.path)
    if parsed.scheme != "https" or parsed.hostname not in OFFICIAL_DOWNLOAD_HOSTS:
        raise ResolutionError(f"{field} is not an official HTTPS download URL")
    if parsed.query or parsed.fragment or "latest" in path.lower() or f"/{tag}/" not in f"{path}/":
        raise ResolutionError(f"{field} must be version-pinned to {tag}")
    return url


def _validate_checksum_url(value: Any, tag: str, field: str = "checksum_url") -> str:
    url = _validate_url(value, tag, field)
    if urllib.parse.unquote(urllib.parse.urlparse(url).path) != f"/{tag}/release.sha256":
        raise ResolutionError(f"{field} must point to release.sha256 for {tag}")
    return url


def _validate_signature_url(value: Any, tag: str, field: str = "signature_url") -> str:
    url = _validate_url(value, tag, field)
    if urllib.parse.unquote(urllib.parse.urlparse(url).path) != f"/{tag}/release.sha256.asc":
        raise ResolutionError(f"{field} must point to release.sha256.asc for {tag}")
    return url


def _validate_release_url(value: Any, tag: str) -> str:
    url = _require_string(value, "release_url")
    expected = f"{OFFICIAL_RELEASE_PREFIX}{tag}"
    if url != expected:
        raise ResolutionError("release_url must exactly identify the official GitLab Runner release")
    return url


def _validate_release_self_link(release: dict[str, Any], tag: str) -> str:
    links = release.get("_links")
    self_link = links.get("self") if isinstance(links, dict) else None
    if not isinstance(self_link, str):
        raise ResolutionError("release self-link is required")
    try:
        return _validate_release_url(self_link, tag)
    except ResolutionError as error:
        raise ResolutionError("release self-link is not canonical for the selected project and tag") from error


def _validate_hash(value: Any, field: str) -> str:
    value = _require_string(value, field).lower()
    if not SHA256_RE.fullmatch(value):
        raise ResolutionError(f"{field} must be a SHA256 hex digest")
    return value


def _validate_size(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ResolutionError(f"{field} must be a positive integer")
    return value


def _validate_source(payload: dict[str, Any]) -> dict[str, Any]:
    source = payload.get("source")
    if not isinstance(source, dict):
        raise ResolutionError("source metadata must be an object")
    if source.get("project") != OFFICIAL_PROJECT:
        raise ResolutionError("source project is not the official GitLab Runner project")
    if source.get("api") != OFFICIAL_API:
        raise ResolutionError("source API is not the official GitLab Runner Releases API")
    kind = source.get("kind", source.get("fixture_kind"))
    if kind not in {"offline-fixture", "offline-release-snapshot", "current-online"}:
        raise ResolutionError("source kind must distinguish offline fixture/snapshot/current-online")
    _require_string(source.get("observed_at"), "source observed_at")
    return source


def _validate_runner_assets(
    release: dict[str, Any], required_architectures: Iterable[str]
) -> list[dict[str, Any]]:
    tag = _require_string(release.get("tag_name"), "tag_name")
    required = tuple(required_architectures)
    assets = release.get("runner_assets")
    if not isinstance(assets, list):
        raise ResolutionError("runner_assets must be a list")

    by_arch: dict[str, dict[str, Any]] = {}
    seen_urls: set[str] = set()
    for asset in assets:
        if not isinstance(asset, dict):
            raise ResolutionError("runner asset must be an object")
        arch = _require_string(asset.get("architecture"), "runner asset architecture")
        if arch not in required:
            raise ResolutionError(f"unexpected runner architecture: {arch}")
        if arch in by_arch:
            raise ResolutionError(f"duplicate runner asset for architecture: {arch}")
        filename = _require_string(asset.get("filename"), "runner asset filename")
        expected_filename = f"gitlab-runner_{arch}.deb"
        if filename != expected_filename:
            raise ResolutionError(f"unexpected filename for {arch}: {filename}")
        url = _validate_url(asset.get("url"), tag, f"runner {arch} url")
        if url in seen_urls:
            raise ResolutionError(f"duplicate runner asset URL: {url}")
        seen_urls.add(url)
        if urllib.parse.unquote(urllib.parse.urlparse(url).path) != f"/{tag}/deb/{filename}":
            raise ResolutionError(f"runner {arch} URL does not point to the expected DEB")
        normalized = {
            "architecture": arch,
            "filename": filename,
            "url": url,
            "sha256": _validate_hash(asset.get("sha256"), f"runner {arch} sha256"),
            "size": _validate_size(asset.get("size"), f"runner {arch} size"),
        }
        if asset.get("local_path") is not None:
            normalized["local_path"] = _require_string(asset["local_path"], f"runner {arch} local_path")
        by_arch[arch] = normalized

    if set(by_arch) != set(required):
        missing = sorted(set(required) - set(by_arch))
        raise ResolutionError(f"runner asset matrix incomplete; missing: {', '.join(missing)}")
    return [by_arch[arch] for arch in required]


def _validate_helper_images(
    release: dict[str, Any], required_architectures: Iterable[str]
) -> dict[str, Any]:
    tag = _require_string(release.get("tag_name"), "tag_name")
    helper = release.get("helper_images")
    if not isinstance(helper, dict):
        raise ResolutionError("helper_images must be an object")
    if _require_string(helper.get("version"), "helper_images version") != tag:
        raise ResolutionError("helper image version does not match Runner release")
    architectures = helper.get("architectures")
    if not isinstance(architectures, list) or not all(isinstance(item, str) for item in architectures):
        raise ResolutionError("helper_images architectures must be a list of strings")
    missing = sorted(set(required_architectures) - set(architectures))
    if missing:
        raise ResolutionError(f"helper image matrix incomplete; missing: {', '.join(missing)}")
    filename = _require_string(helper.get("filename"), "helper_images filename")
    if filename != "gitlab-runner-helper-images.deb":
        raise ResolutionError("unexpected helper image package filename")
    url = _validate_url(helper.get("url"), tag, "helper_images url")
    if urllib.parse.unquote(urllib.parse.urlparse(url).path) != f"/{tag}/deb/{filename}":
        raise ResolutionError("helper image URL does not point to the expected DEB")
    normalized = {
        "version": tag,
        "filename": filename,
        "url": url,
        "sha256": _validate_hash(helper.get("sha256"), "helper_images sha256"),
        "size": _validate_size(helper.get("size"), "helper_images size"),
        "architectures": sorted(set(architectures)),
    }
    if helper.get("local_path") is not None:
        normalized["local_path"] = _require_string(helper["local_path"], "helper_images local_path")
    return normalized


def _validate_official_checksums(
    release: dict[str, Any], runner: list[dict[str, Any]], helper: dict[str, Any]
) -> dict[str, Any]:
    tag = _require_string(release.get("tag_name"), "tag_name")
    official = release.get("official_checksums")
    if not isinstance(official, dict):
        raise ResolutionError("official checksum provenance is required")
    if official.get("tag_name") != tag:
        raise ResolutionError("official checksum tag does not match release")
    checksum_url = _validate_checksum_url(official.get("url"), tag, "official checksum_url")
    assets = official.get("assets")
    if not isinstance(assets, dict) or set(assets) != set(REQUIRED_FILENAMES):
        raise ResolutionError("official checksum catalog must contain exactly the required assets")
    for filename, digest in assets.items():
        assets[filename] = _validate_hash(digest, f"official checksum {filename}")
    catalog = {asset["filename"]: asset["sha256"] for asset in [*runner, helper]}
    for filename in REQUIRED_FILENAMES:
        if catalog[filename] != assets[filename]:
            raise ResolutionError(f"catalog checksum does not match official checksum for {filename}")
    _validate_hash(official.get("document_sha256"), "official checksum document_sha256")
    signature = official.get("signature")
    if not isinstance(signature, dict):
        raise ResolutionError("official checksum signature provenance is required")
    _validate_signature_url(signature.get("url"), tag)
    status = signature.get("status")
    if status not in {"verified", "equivalent-recomputation", "unverified-environment"}:
        raise ResolutionError("official checksum signature trust status is invalid")
    _require_string(signature.get("method"), "official checksum signature method")
    key_fingerprint = signature.get("key_fingerprint")
    if key_fingerprint is not None:
        key_fingerprint = _normalize_fingerprint(key_fingerprint, "official checksum key fingerprint")
        if key_fingerprint != OFFICIAL_KEY_FINGERPRINT:
            raise ResolutionError("official checksum key fingerprint does not match the pinned key")
    key_validity = signature.get("key_validity", "not-observed")
    if key_validity not in {"valid", "unavailable", "not-observed"}:
        raise ResolutionError("official checksum key validity is invalid")
    if status == "verified":
        if key_fingerprint != OFFICIAL_KEY_FINGERPRINT:
            raise ResolutionError("verified checksum key fingerprint is required")
        if key_validity != "valid":
            raise ResolutionError("verified checksum key validity must be valid")
    normalized_signature = {
        "url": signature["url"],
        "status": status,
        "method": signature["method"],
        "key_validity": key_validity,
    }
    if key_fingerprint is not None:
        normalized_signature["key_fingerprint"] = key_fingerprint
    return {
        "url": checksum_url,
        "document_sha256": official["document_sha256"],
        "assets": dict(sorted(assets.items())),
        "signature": normalized_signature,
    }


def resolve_release(
    payload: dict[str, Any],
    required_architectures: Iterable[str] = REQUIRED_ARCHITECTURES,
) -> dict[str, Any]:
    """Select the newest stable release and validate it atomically."""

    source = _validate_source(payload)
    releases = payload.get("releases")
    if not isinstance(releases, list) or not releases:
        raise ResolutionError("source payload must contain a non-empty releases list")
    stable = [release for release in releases if isinstance(release, dict) and not _is_prerelease(release)]
    if not stable:
        raise ResolutionError("source contains no stable release")
    stable.sort(key=lambda release: _version_key(_require_string(release.get("tag_name"), "tag_name")), reverse=True)
    release = stable[0]
    tag = _require_string(release.get("tag_name"), "tag_name")
    version = ".".join(str(part) for part in _version_key(tag))
    runner = _validate_runner_assets(release, required_architectures)
    helper = _validate_helper_images(release, required_architectures)
    checksums = _validate_official_checksums(release, runner, helper)
    checksum_url = _validate_checksum_url(release.get("checksum_url"), tag)
    if checksum_url != checksums["url"]:
        raise ResolutionError("release checksum_url does not match official checksum provenance")
    release_url = _validate_release_url(release.get("release_url"), tag)
    return {
        "release_tag": tag,
        "version": version,
        "released_at": _require_string(release.get("released_at"), "released_at"),
        "release_url": release_url,
        "checksum_url": checksum_url,
        "runner": runner,
        "helper_images": helper,
        "checksum_trust": checksums,
        "source": source,
    }


def verify_local_asset(asset: dict[str, Any], root: Path | None = None) -> None:
    """Verify optional fixture-local files without downloading release assets."""

    local_path = asset.get("local_path")
    if not local_path:
        return
    path = Path(local_path)
    if root and not path.is_absolute():
        path = root / path
    if not path.is_file():
        raise ResolutionError(f"local asset does not exist: {path}")
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            total += len(chunk)
            digest.update(chunk)
    if total != asset["size"]:
        raise ResolutionError(f"local asset size mismatch: {asset['filename']}")
    if digest.hexdigest() != asset["sha256"]:
        raise ResolutionError(f"local asset checksum mismatch: {asset['filename']}")


def verify_resolved_local_assets(resolved: dict[str, Any], root: Path | None = None) -> None:
    for asset in resolved["runner"]:
        verify_local_asset(asset, root)
    verify_local_asset(resolved["helper_images"], root)


def _read_limited(response: Any, limit: int = MAX_METADATA_BYTES) -> bytes:
    body = response.read(limit + 1)
    if len(body) > limit:
        raise ResolutionError("source metadata exceeds the configured size limit")
    return body


class _BoundedRedirectHandler(urllib.request.HTTPRedirectHandler):
    def __init__(self, validator: Callable[[str], bool]):
        super().__init__()
        self._validator = validator
        self._redirects = 0

    def redirect_request(self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str) -> Any:
        self._redirects += 1
        if self._redirects > MAX_REDIRECTS:
            raise ResolutionError("redirect limit exceeded")
        if not self._validator(newurl):
            raise ResolutionError("unexpected redirect origin")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _fetch_raw(
    url: str,
    timeout: float = 10,
    retries: int = 2,
    opener: Callable[..., Any] | None = None,
    response_validator: Callable[[str], bool] | None = None,
) -> tuple[bytes, Any]:
    last_error: Exception | None = None
    default_opener = opener is None or opener is urllib.request.urlopen
    bounded_opener = (
        urllib.request.build_opener(_BoundedRedirectHandler(response_validator or (lambda _url: True))) if default_opener else None
    )
    for attempt in range(retries + 1):
        try:
            if default_opener:
                response_context = bounded_opener.open(url, timeout=timeout)
            else:
                response_context = opener(url, timeout=timeout)  # type: ignore[misc]
            with response_context as response:
                final_url = response.geturl() if callable(getattr(response, "geturl", None)) else url
                if response_validator and not response_validator(final_url):
                    raise ResolutionError("unexpected redirect origin")
                return _read_limited(response), getattr(response, "headers", {})
        except (OSError, urllib.error.URLError, TimeoutError, ResolutionError) as error:
            last_error = error
            if attempt == retries:
                break
    if isinstance(last_error, ResolutionError):
        raise last_error
    raise ResolutionError(f"source fetch failed after {retries + 1} attempts: {url}") from last_error


def fetch_bytes(
    url: str,
    timeout: float = 10,
    retries: int = 2,
    opener: Callable[..., Any] | None = None,
    response_validator: Callable[[str], bool] | None = None,
) -> bytes:
    """Fetch bounded metadata with deterministic retries and redirect checks."""

    return _fetch_raw(url, timeout, retries, opener, response_validator)[0]


def fetch_json(
    url: str,
    timeout: float = 10,
    retries: int = 2,
    opener: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    try:
        payload = json.loads(fetch_bytes(url, timeout=timeout, retries=retries, opener=opener))
    except json.JSONDecodeError as error:
        raise ResolutionError("source metadata is not valid JSON") from error
    if not isinstance(payload, dict):
        raise ResolutionError("source metadata must be a JSON object")
    return payload


def _official_endpoint(url: str, kind: str) -> bool:
    parsed = urllib.parse.urlparse(url)
    path = urllib.parse.unquote(parsed.path)
    if parsed.scheme != "https" or parsed.query and kind != "api" or parsed.fragment:
        return False
    if kind == "api":
        return parsed.hostname == "gitlab.com" and path == "/api/v4/projects/gitlab-org/gitlab-runner/releases"
    if kind == "key":
        return url == OFFICIAL_KEY_URL
    if kind == "release":
        return parsed.hostname == "gitlab.com" and bool(re.fullmatch(r"/gitlab-org/gitlab-runner/-/releases/v\d+\.\d+\.\d+(?:[-+][^/]*)?", path))
    if kind == "download":
        return parsed.hostname in OFFICIAL_DOWNLOAD_HOSTS and bool(
            re.fullmatch(r"/v\d+\.\d+\.\d+(?:[-+][^/]*)?/(?:deb/[^/]+|release\.sha256(?:\.asc)?)", path)
        )
    return False


def _official_fetch(
    url: str,
    kind: str,
    timeout: float,
    retries: int,
    opener: Callable[..., Any] | None = None,
) -> tuple[bytes, Any]:
    if not _official_endpoint(url, kind):
        raise ResolutionError(f"unexpected {kind} origin")
    validator = lambda final_url: _official_endpoint(final_url, kind)
    return _fetch_raw(url, timeout, retries, opener, validator)


def fetch_json_pages(
    url: str,
    timeout: float = 10,
    retries: int = 2,
    opener: Callable[..., Any] | None = None,
) -> list[dict[str, Any]]:
    """Fetch all GitLab Releases API pages and reject changed response shape."""

    if url != OFFICIAL_API:
        raise ResolutionError("release API URL must be canonical")
    pages: list[dict[str, Any]] = []
    page = 1
    while page <= 100:
        query = urllib.parse.urlencode({"per_page": 100, "page": page})
        page_url = f"{url}?{query}"
        body, headers = _official_fetch(page_url, "api", timeout, retries, opener)
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as error:
            raise ResolutionError("release API response is not valid JSON") from error
        if not isinstance(payload, list) or not all(isinstance(item, dict) for item in payload):
            raise ResolutionError("release API response schema changed: expected release list")
        pages.extend(payload)
        next_page = headers.get("X-Next-Page") if hasattr(headers, "get") else None
        if next_page:
            try:
                page = int(next_page)
            except (TypeError, ValueError) as error:
                raise ResolutionError("release API pagination header is invalid") from error
        elif len(payload) == 100:
            page += 1
        else:
            break
    if page > 100:
        raise ResolutionError("release API pagination exceeded safety bound")
    return pages


def parse_checksum_document(document: bytes | str, required: Iterable[str] = REQUIRED_FILENAMES) -> dict[str, str]:
    """Parse an official release.sha256 document and reject duplicate records."""

    text = document.decode("utf-8") if isinstance(document, bytes) else document
    selected = set(required)
    result: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        match = re.fullmatch(r"([0-9a-fA-F]{64})\s+[*]?(.+)", line)
        if not match:
            raise ResolutionError("official checksum document contains an invalid line")
        digest, filename = match.groups()
        basename = Path(filename.strip()).name
        if basename not in selected:
            continue
        if basename in result:
            raise ResolutionError(f"duplicate official checksum for {basename}")
        result[basename] = digest.lower()
    missing = sorted(selected - set(result))
    if missing:
        raise ResolutionError(f"official checksum document missing: {', '.join(missing)}")
    return dict(sorted(result.items()))


def _signature_status(
    checksum: bytes,
    signature: bytes,
    timeout: float,
    retries: int,
    opener: Callable[..., Any] | None,
) -> dict[str, Any]:
    """Verify the release signature and fail closed once GPG is available."""

    method = (
        "official checksum document over pinned HTTPS; exact required asset records parsed and confronted; "
        "GPG verification requires the documented GitLab Runner signing key"
    )

    def failure(reason: str) -> ResolutionError:
        return ResolutionError(f"checksum signature verification failed: {reason}")

    gpg = shutil.which("gpg") or shutil.which("gpg.exe")
    if not gpg and os.name == "nt":
        for candidate in (Path(os.environ.get("ProgramFiles", "")) / "Git" / "usr" / "bin" / "gpg.exe", Path("C:/Program Files/Git/usr/bin/gpg.exe")):
            if candidate.is_file():
                gpg = str(candidate)
                break
    if not gpg:
        return {
            "status": "unverified-environment",
            "method": method + "; gpg unavailable",
            "key_validity": "unavailable",
        }

    try:
        key, _ = _official_fetch(OFFICIAL_KEY_URL, "key", timeout, retries, opener)
        with tempfile.TemporaryDirectory(prefix="runner-gpg-") as directory:
            home = Path(directory)
            key_path = home / "runner.pub.asc"
            keyring_path = home / "runner.keyring.gpg"
            checksum_path = home / "release.sha256"
            signature_path = home / "release.sha256.asc"
            key_path.write_bytes(key)
            checksum_path.write_bytes(checksum)
            signature_path.write_bytes(signature)
            env = {**os.environ, "GNUPGHOME": str(home)}
            gpg_path = lambda path: path.as_posix() if os.name == "nt" else str(path)
            try:
                dearmored = subprocess.run(
                    [gpg, "--batch", "--yes", "--no-autostart", "--dearmor", "--output", gpg_path(keyring_path), gpg_path(key_path)],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except OSError as error:
                raise failure("GPG key conversion could not be executed") from error
            if dearmored.returncode != 0:
                raise failure("GPG key conversion returned nonzero")

            gpgv = shutil.which("gpgv") or shutil.which("gpgv.exe")
            if not gpgv and os.name == "nt":
                sibling = Path(gpg).with_name("gpgv.exe")
                if sibling.is_file():
                    gpgv = str(sibling)
            if not gpgv:
                raise failure("gpgv unavailable")
            try:
                verified = subprocess.run(
                    [gpgv, "--status-fd", "1", "--keyring", gpg_path(keyring_path), gpg_path(signature_path), gpg_path(checksum_path)],
                    env=env,
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except OSError as error:
                raise failure("gpgv could not be executed") from error

            status_lines = (verified.stdout or "").splitlines()
            status_codes = [parts[1] for parts in (line.split() for line in status_lines) if len(parts) > 1 and parts[0] == "[GNUPG:]"]
            for code in status_codes:
                if code in {"EXPSIG", "EXPKEYSIG", "KEYEXPIRED", "SIGEXPIRED"}:
                    raise failure("signature or key is expired")
                if code in {"REVKEYSIG", "KEYREVOKED"}:
                    raise failure("signature or key is revoked")
                if code in GPG_FAILURE_CODES:
                    raise failure(f"verifier status {code}")
            if verified.returncode != 0:
                raise failure("verifier returned nonzero")

            validsig_records = [
                parts for parts in (line.split() for line in status_lines) if len(parts) > 1 and parts[0] == "[GNUPG:]" and parts[1] == "VALIDSIG"
            ]
            if len(validsig_records) != 1 or len(validsig_records[0]) < 6:
                raise failure("verifier output did not contain exactly one complete VALIDSIG record")
            try:
                fingerprint = _normalize_fingerprint(validsig_records[0][2], "verifier fingerprint")
            except ResolutionError as error:
                raise failure("verifier fingerprint is invalid") from error
            if fingerprint != OFFICIAL_KEY_FINGERPRINT:
                raise failure("verifier fingerprint does not match the pinned key")
            expiration = validsig_records[0][5]
            if expiration.isdigit() and expiration != "0" and int(expiration) <= int(datetime.now(timezone.utc).timestamp()):
                raise failure("signature or key is expired")
            return {
                "status": "verified",
                "method": method + "; trusted fingerprint matched",
                "key_fingerprint": fingerprint,
                "key_validity": "valid",
            }
    except OSError as error:
        raise failure("verification environment could not be prepared") from error


def _probe_size(url: str, timeout: float, retries: int, opener: Callable[..., Any] | None) -> int:
    if not _official_endpoint(url, "download"):
        raise ResolutionError("asset size probe origin is not official")
    last_error: Exception | None = None
    default_opener = opener is None or opener is urllib.request.urlopen
    bounded_opener = (
        urllib.request.build_opener(_BoundedRedirectHandler(lambda final_url: _official_endpoint(final_url, "download")))
        if default_opener
        else None
    )
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(url, method="HEAD")
            if default_opener:
                response_context = bounded_opener.open(request, timeout=timeout)
            else:
                response_context = opener(request, timeout=timeout)  # type: ignore[misc]
            with response_context as response:
                final_url = response.geturl() if callable(getattr(response, "geturl", None)) else url
                if not _official_endpoint(final_url, "download"):
                    raise ResolutionError("unexpected redirect origin")
                value = response.headers.get("Content-Length") if hasattr(response, "headers") else None
                if value and value.isdigit() and int(value) > 0:
                    return int(value)
                raise ResolutionError("official asset did not provide a positive Content-Length")
        except (OSError, urllib.error.URLError, TimeoutError, ResolutionError) as error:
            last_error = error
            if attempt == retries:
                break
    raise ResolutionError(f"official asset size probe failed: {url}") from last_error


def _release_link(release: dict[str, Any], name: str) -> str:
    assets = release.get("assets")
    links = assets.get("links") if isinstance(assets, dict) else None
    if not isinstance(links, list):
        raise ResolutionError("release API schema changed: assets.links is required")
    matches = [item for item in links if isinstance(item, dict) and item.get("name") == name]
    if len(matches) != 1:
        raise ResolutionError(f"release API must contain exactly one asset link named {name}")
    return _require_string(matches[0].get("url"), f"release asset {name} url")


def discover_current(
    api_url: str = OFFICIAL_API,
    timeout: float = 10,
    retries: int = 2,
    opener: Callable[..., Any] | None = None,
) -> dict[str, Any]:
    """Discover, checksum-validate and size-probe the newest stable release."""

    releases = fetch_json_pages(api_url, timeout, retries, opener)
    stable = [item for item in releases if not _is_prerelease(item)]
    if not stable:
        raise ResolutionError("release API contains no eligible stable release")
    stable.sort(key=lambda item: _version_key(_require_string(item.get("tag_name"), "tag_name")), reverse=True)
    api_release = stable[0]
    tag = _require_string(api_release.get("tag_name"), "tag_name")
    _version_key(tag)
    release_url = _validate_release_self_link(api_release, tag)
    checksum_url = _release_link(api_release, "checksums")
    signature_url = _release_link(api_release, "checksums GPG signature")
    _validate_checksum_url(checksum_url, tag)
    _validate_signature_url(signature_url, tag)
    checksum_document, _ = _official_fetch(checksum_url, "download", timeout, retries, opener)
    checksum_map = parse_checksum_document(checksum_document)
    runner_assets: list[dict[str, Any]] = []
    for arch in REQUIRED_ARCHITECTURES:
        filename = f"gitlab-runner_{arch}.deb"
        url = _release_link(api_release, f"package: DEB {arch}")
        _validate_url(url, tag, f"runner {arch} url")
        runner_assets.append(
            {
                "architecture": arch,
                "filename": filename,
                "url": url,
                "sha256": checksum_map[filename],
                "size": _probe_size(url, timeout, retries, opener),
            }
        )
    helper_url = f"https://gitlab-runner-downloads.s3.amazonaws.com/{tag}/deb/gitlab-runner-helper-images.deb"
    _validate_url(helper_url, tag, "helper_images url")
    helper = {
        "version": tag,
        "filename": "gitlab-runner-helper-images.deb",
        "url": helper_url,
        "sha256": checksum_map["gitlab-runner-helper-images.deb"],
        "size": _probe_size(helper_url, timeout, retries, opener),
        "architectures": list(REQUIRED_ARCHITECTURES),
    }
    signature_document, _ = _official_fetch(signature_url, "download", timeout, retries, opener)
    signature = _signature_status(checksum_document, signature_document, timeout, retries, opener)
    source = {
        "api": OFFICIAL_API,
        "project": OFFICIAL_PROJECT,
        "download_base": "https://gitlab-runner-downloads.s3.amazonaws.com",
        "kind": "current-online",
        "observed_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "pagination": "GitLab X-Next-Page with per_page=100",
    }
    payload = {
        "source": source,
        "releases": [
            {
                "tag_name": tag,
                "stable": True,
                "released_at": _require_string(api_release.get("released_at"), "released_at"),
                "release_url": release_url,
                "checksum_url": checksum_url,
                "runner_assets": runner_assets,
                "helper_images": helper,
                "official_checksums": {
                    "tag_name": tag,
                    "url": checksum_url,
                    "document_sha256": hashlib.sha256(checksum_document).hexdigest(),
                    "assets": checksum_map,
                    "signature": {"url": signature_url, **signature},
                },
            }
        ],
    }
    resolved = resolve_release(payload)
    return {"payload": payload, "resolved": resolved}


def manifest_upstream_version(manifest_path: Path) -> str:
    match = MANIFEST_VERSION_RE.search(manifest_path.read_text(encoding="utf-8"))
    if not match:
        raise ResolutionError(f"manifest version not found: {manifest_path}")
    version = match.group(1).split("~", 1)[0]
    _version_key(version)
    return version


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _replace_manifest_field(text: str, field: str, value: str) -> str:
    pattern = re.compile(rf'(?m)^(\s*{re.escape(field)}\s*=\s*)"[^"]*"(\s*)$')
    replacement = rf'\1{_toml_string(value)}\2'
    text, count = pattern.subn(replacement, text)
    if count != 1:
        raise ResolutionError(f"manifest candidate expected exactly one field: {field}")
    return text


def render_manifest_candidate(manifest_path: Path, resolved: dict[str, Any], package_revision: str = "ynh1") -> tuple[str, list[str], list[str]]:
    """Return a complete manifest copy and its deterministic allowlisted diff."""

    original = manifest_path.read_text(encoding="utf-8")
    if tomllib is None:
        raise ResolutionError("Python tomllib is required to parse manifest.toml")
    try:
        tomllib.loads(original)
    except tomllib.TOMLDecodeError as error:
        raise ResolutionError("tracked manifest is not valid TOML") from error
    replacements = {
        "version": f"{resolved['version']}~{package_revision}",
        "amd64.url": resolved["runner"][0]["url"],
        "amd64.sha256": resolved["runner"][0]["sha256"],
        "arm64.url": resolved["runner"][1]["url"],
        "arm64.sha256": resolved["runner"][1]["sha256"],
        "armhf.url": resolved["runner"][2]["url"],
        "armhf.sha256": resolved["runner"][2]["sha256"],
        "url": resolved["helper_images"]["url"],
        "sha256": resolved["helper_images"]["sha256"],
    }
    candidate = original
    for field, value in replacements.items():
        candidate = _replace_manifest_field(candidate, field, value)
    try:
        tomllib.loads(candidate)
    except tomllib.TOMLDecodeError as error:
        raise ResolutionError("generated manifest candidate is not valid TOML") from error
    diff = list(
        difflib.unified_diff(
            original.splitlines(),
            candidate.splitlines(),
            fromfile=str(manifest_path),
            tofile=f"{manifest_path}.candidate",
            lineterm="",
        )
    )
    changed_fields: set[str] = set()
    for line in diff:
        if not line.startswith(("+", "-")) or line.startswith(("+++", "---")):
            continue
        match = re.match(r"^[+-]\s*([A-Za-z0-9_.]+)\s*=", line)
        if not match or match.group(1) not in MANIFEST_FIELDS:
            raise ResolutionError("manifest candidate diff contains a field outside the allowlist")
        changed_fields.add(match.group(1))
    if changed_fields != set(replacements):
        raise ResolutionError("manifest candidate diff does not contain exactly the authorized fields")
    return candidate, sorted(changed_fields), diff


def render_candidate(resolved: dict[str, Any], package_revision: str = "ynh1") -> str:
    """Backward-compatible deterministic summary for callers of the old helper."""

    lines = [
        "# Candidate summary; tracked manifest is never promoted by this tool.",
        "",
        "[candidate]",
        f"release = {_toml_string(resolved['release_tag'])}",
        f"upstream_version = {_toml_string(resolved['version'])}",
        f"package_version = {_toml_string(resolved['version'] + '~' + package_revision)}",
        f"release_url = {_toml_string(resolved['release_url'])}",
        f"checksum_url = {_toml_string(resolved['checksum_url'])}",
        "",
    ]
    for asset in resolved["runner"]:
        lines.extend([f"{asset['architecture']}.url = {_toml_string(asset['url'])}", f"{asset['architecture']}.sha256 = {_toml_string(asset['sha256'])}"])
    lines.extend([f"helper.url = {_toml_string(resolved['helper_images']['url'])}", f"helper.sha256 = {_toml_string(resolved['helper_images']['sha256'])}", ""])
    return "\n".join(lines)


def atomic_write(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    previous = path.read_text(encoding="utf-8") if path.exists() else None
    if previous == content:
        return False
    fd, temp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.unlink(temp_name)
    return True


def _assert_candidate_destination(output: Path, manifest: Path) -> None:
    if output.resolve() == manifest.resolve():
        raise ResolutionError("candidate output must not overwrite the tracked manifest")
    try:
        root = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=manifest.parent,
            capture_output=True,
            text=True,
            check=False,
        )
        if root.returncode == 0:
            repo = Path(root.stdout.strip())
            relative = output.resolve().relative_to(repo.resolve())
            tracked = subprocess.run(
                ["git", "ls-files", "--error-unmatch", "--", relative.as_posix()],
                cwd=repo,
                capture_output=True,
                text=True,
                check=False,
            )
            if tracked.returncode == 0:
                raise ResolutionError("candidate output must be outside tracked files")
    except ValueError:
        pass


def build_report(resolved: dict[str, Any], manifest_path: Path) -> dict[str, Any]:
    baseline = manifest_upstream_version(manifest_path)
    candidate = resolved["version"]
    return {
        "schema_version": 2,
        "mode": "dry-run",
        "promoted": False,
        "baseline_manifest_version": baseline,
        "candidate_upstream_version": candidate,
        "candidate_is_newer": _version_key(candidate) > _version_key(baseline),
        "source_kind": resolved["source"]["kind"],
        "observed_at": resolved["source"]["observed_at"],
        "release": resolved,
    }


def build_manifest_report(
    resolved: dict[str, Any], manifest_path: Path, changed_fields: list[str], diff: list[str], output: Path
) -> dict[str, Any]:
    report = build_report(resolved, manifest_path)
    report.update(
        {
            "manifest_candidate": str(output),
            "changed_fields": changed_fields,
            "diff": diff,
            "diff_guard": "allowlist-only",
        }
    )
    return report


def _load_fixture(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ResolutionError(f"cannot load fixture: {path}") from error
    if not isinstance(payload, dict):
        raise ResolutionError("fixture must be a JSON object")
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> bool:
    content = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    return atomic_write(path, content)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check")
    check.add_argument("--fixture", type=Path, required=True)
    check.add_argument("--manifest", type=Path, default=Path("manifest.toml"))
    check.add_argument("--verify-files", action="store_true")
    check.add_argument("--report", type=Path)

    generate = subparsers.add_parser("generate")
    source = generate.add_mutually_exclusive_group(required=True)
    source.add_argument("--fixture", type=Path)
    source.add_argument("--refresh", action="store_true")
    generate.add_argument("--manifest", type=Path, default=Path("manifest.toml"))
    generate.add_argument("--output", type=Path, required=True)
    generate.add_argument("--report", type=Path)
    generate.add_argument("--verify-files", action="store_true")
    generate.add_argument("--write", action="store_true", help="write only to the explicit staging output")

    discover = subparsers.add_parser("discover")
    discover.add_argument("--manifest", type=Path, default=Path("manifest.toml"))
    discover.add_argument("--report", type=Path, required=True)
    discover.add_argument("--timeout", type=float, default=10)
    discover.add_argument("--retries", type=int, default=2)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "discover":
            discovered = discover_current(timeout=args.timeout, retries=args.retries)
            report = build_report(discovered["resolved"], args.manifest)
            report["discovery"] = {
                "api": OFFICIAL_API,
                "pagination": discovered["payload"]["source"]["pagination"],
                "selected_tag": discovered["resolved"]["release_tag"],
                "signature": discovered["resolved"]["checksum_trust"]["signature"],
            }
            _write_json(args.report, report)
            print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
            return 0

        if args.command == "check":
            payload = _load_fixture(args.fixture)
            resolved = resolve_release(payload)
            if args.verify_files:
                verify_resolved_local_assets(resolved, args.fixture.parent)
            report = build_report(resolved, args.manifest)
            if args.report:
                _write_json(args.report, report)
            print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
            return 0

        if args.refresh:
            resolved = discover_current()["resolved"]
            signature = resolved["checksum_trust"]["signature"]
            if signature.get("status") != "verified" or signature.get("key_validity") != "valid":
                raise ResolutionError("generate --refresh requires verified checksum signature")
        else:
            payload = _load_fixture(args.fixture)
            resolved = resolve_release(payload)
            if args.verify_files:
                verify_resolved_local_assets(resolved, args.fixture.parent)
        candidate, changed_fields, diff = render_manifest_candidate(args.manifest, resolved)
        _assert_candidate_destination(args.output, args.manifest)
        report = build_manifest_report(resolved, args.manifest, changed_fields, diff, args.output)
        changed = atomic_write(args.output, candidate) if args.write else False
        report["mode"] = "write" if args.write else "dry-run"
        report["changed"] = changed
        if args.report:
            _write_json(args.report, report)
        print(json.dumps({"mode": report["mode"], "changed": changed, "output": str(args.output), "changed_fields": changed_fields}, sort_keys=True))
        if not args.write:
            print(candidate, end="")
        return 0
    except ResolutionError as error:
        print(f"autoupdate: {error}", file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
