#!/usr/bin/env python3
"""Resolve and generate a coordinated GitLab Runner update candidate.

The command is deliberately offline-first: a checked-in release fixture is the
input used by CI and by the default dry-run. The network adapter is available
for a future scheduled invocation, but it only accepts the official release
API and versioned S3 assets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, Iterable


REQUIRED_ARCHITECTURES = ("amd64", "arm64", "armhf")
OFFICIAL_DOWNLOAD_HOSTS = {
    "gitlab-runner-downloads.s3.amazonaws.com",
    "gitlab-runner-downloads.s3.dualstack.us-east-1.amazonaws.com",
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:[-+].*)?$")
MANIFEST_VERSION_RE = re.compile(r'^version\s*=\s*"([^"]+)"', re.MULTILINE)
MAX_METADATA_BYTES = 1024 * 1024


class ResolutionError(ValueError):
    """Raised when a release cannot be used as an atomic candidate."""


def _version_key(version: str) -> tuple[int, int, int]:
    match = SEMVER_RE.fullmatch(version)
    if not match:
        raise ResolutionError(f"unsupported release version: {version}")
    return tuple(int(part) for part in match.groups())


def _is_prerelease(release: dict[str, Any]) -> bool:
    tag = str(release.get("tag_name", ""))
    return release.get("stable") is False or "-" in tag.lstrip("v")


def _require_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ResolutionError(f"{field} must be a non-empty string")
    return value


def _validate_url(url: Any, tag: str, field: str) -> str:
    url = _require_string(url, field)
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in OFFICIAL_DOWNLOAD_HOSTS:
        raise ResolutionError(f"{field} is not an official HTTPS download URL")
    if "latest" in parsed.path.lower() or f"/{tag}/" not in f"{parsed.path}/":
        raise ResolutionError(f"{field} must be version-pinned to {tag}")
    return url


def _validate_hash(value: Any, field: str) -> str:
    value = _require_string(value, field).lower()
    if not SHA256_RE.fullmatch(value):
        raise ResolutionError(f"{field} must be a SHA256 hex digest")
    return value


def _validate_size(value: Any, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ResolutionError(f"{field} must be a positive integer")
    return value


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
        if not url.endswith(f"/deb/{filename}"):
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
    if not url.endswith(f"/deb/{filename}"):
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


def resolve_release(
    payload: dict[str, Any],
    required_architectures: Iterable[str] = REQUIRED_ARCHITECTURES,
) -> dict[str, Any]:
    """Select the newest stable release and validate Runner/helpers atomically."""

    releases = payload.get("releases")
    if not isinstance(releases, list) or not releases:
        raise ResolutionError("source payload must contain a non-empty releases list")
    stable = [release for release in releases if isinstance(release, dict) and not _is_prerelease(release)]
    if not stable:
        raise ResolutionError("source contains no stable release")
    stable.sort(key=lambda release: _version_key(_require_string(release.get("tag_name"), "tag_name")), reverse=True)
    release = stable[0]
    tag = _require_string(release.get("tag_name"), "tag_name")
    version = f"{_version_key(tag)[0]}.{_version_key(tag)[1]}.{_version_key(tag)[2]}"
    runner = _validate_runner_assets(release, required_architectures)
    helper = _validate_helper_images(release, required_architectures)

    checksum_url = _validate_url(release.get("checksum_url"), tag, "checksum_url")
    release_url = _require_string(release.get("release_url"), "release_url")
    if not release_url.startswith("https://gitlab.com/"):
        raise ResolutionError("release_url must point to the official GitLab project")
    return {
        "release_tag": tag,
        "version": version,
        "released_at": _require_string(release.get("released_at"), "released_at"),
        "release_url": release_url,
        "checksum_url": checksum_url,
        "runner": runner,
        "helper_images": helper,
        "source": payload.get("source", {}),
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


def fetch_bytes(
    url: str,
    timeout: float = 10,
    retries: int = 2,
    opener: Callable[..., Any] = urllib.request.urlopen,
) -> bytes:
    """Fetch bounded metadata with deterministic retry count and safe errors."""

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            with opener(url, timeout=timeout) as response:
                return _read_limited(response)
        except (OSError, urllib.error.URLError, TimeoutError, ResolutionError) as error:
            last_error = error
            if attempt == retries:
                break
    raise ResolutionError(f"source fetch failed after {retries + 1} attempts: {url}") from last_error


def fetch_json(
    url: str,
    timeout: float = 10,
    retries: int = 2,
    opener: Callable[..., Any] = urllib.request.urlopen,
) -> dict[str, Any]:
    try:
        payload = json.loads(fetch_bytes(url, timeout=timeout, retries=retries, opener=opener))
    except json.JSONDecodeError as error:
        raise ResolutionError("source metadata is not valid JSON") from error
    if not isinstance(payload, dict):
        raise ResolutionError("source metadata must be a JSON object")
    return payload


def manifest_upstream_version(manifest_path: Path) -> str:
    match = MANIFEST_VERSION_RE.search(manifest_path.read_text(encoding="utf-8"))
    if not match:
        raise ResolutionError(f"manifest version not found: {manifest_path}")
    version = match.group(1).split("~", 1)[0]
    _version_key(version)
    return version


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def render_candidate(resolved: dict[str, Any], package_revision: str = "ynh1") -> str:
    """Render only candidate version/source/hash fields in stable order."""

    lines = [
        "# Generated candidate; do not promote without a reviewed package round.",
        "# This file is not consumed by install/upgrade at runtime.",
        "",
        "[candidate]",
        f"release = {_toml_string(resolved['release_tag'])}",
        f"upstream_version = {_toml_string(resolved['version'])}",
        f"package_version = {_toml_string(resolved['version'] + '~' + package_revision)}",
        f"release_url = {_toml_string(resolved['release_url'])}",
        f"checksum_url = {_toml_string(resolved['checksum_url'])}",
        "",
        "[runner]",
    ]
    for asset in resolved["runner"]:
        arch = asset["architecture"]
        lines.extend(
            [
                f"{arch}.url = {_toml_string(asset['url'])}",
                f"{arch}.sha256 = {_toml_string(asset['sha256'])}",
            ]
        )
    helper = resolved["helper_images"]
    lines.extend(
        [
            "",
            "[helper_images]",
            f"url = {_toml_string(helper['url'])}",
            f"sha256 = {_toml_string(helper['sha256'])}",
            f"architectures = {json.dumps(helper['architectures'])}",
            "",
        ]
    )
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


def build_report(resolved: dict[str, Any], manifest_path: Path) -> dict[str, Any]:
    baseline = manifest_upstream_version(manifest_path)
    candidate = resolved["version"]
    return {
        "schema_version": 1,
        "mode": "dry-run",
        "promoted": False,
        "baseline_manifest_version": baseline,
        "candidate_upstream_version": candidate,
        "candidate_is_newer": _version_key(candidate) > _version_key(baseline),
        "release": resolved,
    }


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
    for command in ("check", "generate"):
        sub = subparsers.add_parser(command)
        sub.add_argument("--fixture", type=Path, required=True)
        sub.add_argument("--manifest", type=Path, default=Path("manifest.toml"))
        sub.add_argument("--verify-files", action="store_true")
        if command == "check":
            sub.add_argument("--report", type=Path)
        else:
            sub.add_argument("--output", type=Path, required=True)
            sub.add_argument("--write", action="store_true", help="write candidate only when explicitly requested")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        payload = _load_fixture(args.fixture)
        resolved = resolve_release(payload)
        if args.verify_files:
            verify_resolved_local_assets(resolved, args.fixture.parent)
        if args.command == "check":
            report = build_report(resolved, args.manifest)
            output = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            if args.report:
                _write_json(args.report, report)
            print(output, end="")
        else:
            content = render_candidate(resolved)
            changed = atomic_write(args.output, content) if args.write else False
            print(json.dumps({"mode": "write" if args.write else "dry-run", "changed": changed, "output": str(args.output)}, sort_keys=True))
            if not args.write:
                print(content, end="")
        return 0
    except ResolutionError as error:
        print(f"autoupdate: {error}", file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
