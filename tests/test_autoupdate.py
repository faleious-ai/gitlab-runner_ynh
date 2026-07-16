from __future__ import annotations

import copy
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.error import URLError


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import autoupdate  # noqa: E402
import secret_scan  # noqa: E402


FIXTURE = ROOT / "scripts" / "autoupdate" / "fixtures" / "release-v19.0.1.json"


def usable_bash() -> str | None:
    candidates = [shutil.which("bash"), r"C:\Program Files\Git\bin\bash.exe", r"C:\Program Files\Git\usr\bin\bash.exe"]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            probe = subprocess.run([candidate, "-c", "exit 0"], capture_output=True, check=False)
        except OSError:
            continue
        if probe.returncode == 0:
            return candidate
    return None


BASH = usable_bash()


class AutoupdateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_resolves_stable_runner_and_helper_set(self) -> None:
        resolved = autoupdate.resolve_release(self.payload)
        self.assertEqual(resolved["release_tag"], "v19.0.1")
        self.assertEqual([item["architecture"] for item in resolved["runner"]], ["amd64", "arm64", "armhf"])
        self.assertEqual(resolved["helper_images"]["version"], "v19.0.1")
        self.assertTrue(set(resolved["helper_images"]["architectures"]) >= {"amd64", "arm64", "armhf"})

    def test_prerelease_is_not_selected(self) -> None:
        payload = {"source": self.payload["source"], "releases": [self.payload["releases"][1]]}
        with self.assertRaises(autoupdate.ResolutionError):
            autoupdate.resolve_release(payload)

    def test_missing_architecture_fails_closed(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["releases"][0]["runner_assets"] = payload["releases"][0]["runner_assets"][:-1]
        with self.assertRaisesRegex(autoupdate.ResolutionError, "matrix incomplete"):
            autoupdate.resolve_release(payload)

    def test_duplicate_architecture_fails_closed(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["releases"][0]["runner_assets"].append(copy.deepcopy(payload["releases"][0]["runner_assets"][0]))
        with self.assertRaisesRegex(autoupdate.ResolutionError, "duplicate"):
            autoupdate.resolve_release(payload)

    def test_helper_version_mismatch_fails_closed(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["releases"][0]["helper_images"]["version"] = "v19.0.0"
        with self.assertRaisesRegex(autoupdate.ResolutionError, "does not match"):
            autoupdate.resolve_release(payload)

    def test_bad_checksum_and_unpinned_url_fail_closed(self) -> None:
        payload = copy.deepcopy(self.payload)
        payload["releases"][0]["runner_assets"][0]["sha256"] = "not-a-hash"
        with self.assertRaisesRegex(autoupdate.ResolutionError, "sha256"):
            autoupdate.resolve_release(payload)

        payload = copy.deepcopy(self.payload)
        payload["releases"][0]["helper_images"]["url"] = "https://gitlab-runner-downloads.s3.amazonaws.com/latest/deb/gitlab-runner-helper-images.deb"
        with self.assertRaisesRegex(autoupdate.ResolutionError, "version-pinned"):
            autoupdate.resolve_release(payload)

        payload = copy.deepcopy(self.payload)
        payload["releases"][0]["official_checksums"]["assets"]["gitlab-runner_amd64.deb"] = "0" * 64
        with self.assertRaisesRegex(autoupdate.ResolutionError, "does not match official"):
            autoupdate.resolve_release(payload)

        payload = copy.deepcopy(self.payload)
        payload["source"]["project"] = "attacker/project"
        with self.assertRaisesRegex(autoupdate.ResolutionError, "official GitLab Runner project"):
            autoupdate.resolve_release(payload)

        payload = copy.deepcopy(self.payload)
        payload["releases"][0]["official_checksums"]["signature"]["status"] = "bad"
        with self.assertRaisesRegex(autoupdate.ResolutionError, "signature trust status"):
            autoupdate.resolve_release(payload)

    def test_local_checksum_is_verified(self) -> None:
        resolved = autoupdate.resolve_release(self.payload)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "asset.deb"
            content = b"offline fixture asset"
            path.write_bytes(content)
            asset = resolved["runner"][0]
            asset["local_path"] = path.name
            asset["size"] = len(content)
            asset["sha256"] = hashlib.sha256(content).hexdigest()
            autoupdate.verify_resolved_local_assets(resolved, Path(directory))
            asset["sha256"] = "0" * 64
            with self.assertRaisesRegex(autoupdate.ResolutionError, "checksum mismatch"):
                autoupdate.verify_resolved_local_assets(resolved, Path(directory))

    def test_fetch_retries_without_leaking_response_body(self) -> None:
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def read(self, _limit):
                return b'{"ok": true}'

        calls = {"count": 0}

        def flaky_opener(_url, timeout):
            self.assertEqual(timeout, 0.25)
            calls["count"] += 1
            if calls["count"] < 3:
                raise URLError("synthetic network failure")
            return Response()

        self.assertEqual(autoupdate.fetch_json("https://example.invalid", timeout=0.25, retries=2, opener=flaky_opener), {"ok": True})
        self.assertEqual(calls["count"], 3)

        class PageResponse(Response):
            def __init__(self, body, next_page=None, final_url=autoupdate.OFFICIAL_API):
                self.body = body
                self.headers = {"X-Next-Page": next_page} if next_page else {}
                self.final_url = final_url

            def read(self, _limit):
                return self.body

            def geturl(self):
                return self.final_url

        pages = [
            PageResponse(json.dumps([{"tag_name": "v19.2.0"}]).encode(), "2"),
            PageResponse(json.dumps([{"tag_name": "v19.1.1"}]).encode()),
        ]

        def page_opener(_url, timeout):
            self.assertEqual(timeout, 0.25)
            return pages.pop(0)

        discovered_pages = autoupdate.fetch_json_pages(autoupdate.OFFICIAL_API, timeout=0.25, retries=0, opener=page_opener)
        self.assertEqual([item["tag_name"] for item in discovered_pages], ["v19.2.0", "v19.1.1"])

        with self.assertRaisesRegex(autoupdate.ResolutionError, "unexpected redirect origin"):
            autoupdate._official_fetch(
                autoupdate.OFFICIAL_API,
                "api",
                timeout=0.25,
                retries=0,
                opener=lambda _url, timeout: PageResponse(b"[]", final_url="https://evil.example/releases"),
            )

        with self.assertRaisesRegex(autoupdate.ResolutionError, "missing"):
            autoupdate.parse_checksum_document("0" * 64 + "  deb/gitlab-runner_amd64.deb\n")

        duplicate = "\n".join(["0" * 64 + "  deb/gitlab-runner_amd64.deb"] * 2)
        with self.assertRaisesRegex(autoupdate.ResolutionError, "duplicate"):
            autoupdate.parse_checksum_document(duplicate)

    def test_candidate_is_deterministic_and_atomic(self) -> None:
        resolved = autoupdate.resolve_release(self.payload)
        rendered_a = autoupdate.render_candidate(resolved)
        rendered_b = autoupdate.render_candidate(resolved)
        self.assertEqual(rendered_a, rendered_b)
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "candidate.toml"
            self.assertTrue(autoupdate.atomic_write(output, rendered_a))
            self.assertFalse(autoupdate.atomic_write(output, rendered_b))
            self.assertEqual(output.read_text(encoding="utf-8"), rendered_a)
            original = "safe baseline\n"
            output.write_text(original, encoding="utf-8")
            invalid = copy.deepcopy(self.payload)
            invalid["releases"][0]["helper_images"]["version"] = "v18.0.0"
            with self.assertRaises(autoupdate.ResolutionError):
                autoupdate.resolve_release(invalid)
            self.assertEqual(output.read_text(encoding="utf-8"), original)

        candidate, fields, diff = autoupdate.render_manifest_candidate(ROOT / "manifest.toml", resolved)
        self.assertEqual(fields, sorted(autoupdate.MANIFEST_FIELDS))
        self.assertIn('version = "19.0.1~ynh1"', candidate)
        self.assertTrue(any("amd64.sha256" in line for line in diff))
        self.assertIn('version = "18.6.2~ynh1"', (ROOT / "manifest.toml").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(autoupdate.ResolutionError, "must not overwrite"):
                autoupdate._assert_candidate_destination(ROOT / "manifest.toml", ROOT / "manifest.toml")
            output = Path(directory) / "candidate.toml"
            autoupdate._assert_candidate_destination(output, ROOT / "manifest.toml")

    def test_action_target_and_manifest_baseline(self) -> None:
        config_panel = (ROOT / "config_panel.toml").read_text(encoding="utf-8")
        self.assertIn("type = \"button\"", config_panel)
        self.assertIn("[main.registration.register]", config_panel)
        self.assertTrue((ROOT / "scripts" / "config").is_file())
        config_script = (ROOT / "scripts" / "config").read_text(encoding="utf-8")
        self.assertIn('register_runner_set "${gitlab_url:-}" "${token:-}" "${docker_image:-}"', config_script)
        report = autoupdate.build_report(autoupdate.resolve_release(self.payload), ROOT / "manifest.toml")
        self.assertEqual(report["baseline_manifest_version"], "18.6.2")
        self.assertFalse(report["promoted"])

    def test_secret_scan_current_tree(self) -> None:
        self.assertEqual(secret_scan.scan(ROOT), [])

    @unittest.skipUnless(BASH, "bash is required for shell action tests")
    def test_registration_rejects_mismatched_cardinality_before_execution(self) -> None:
        action = ROOT / "scripts" / "actions" / "register"
        result = subprocess.run(
            [BASH, str(action), "--gitlab_url", "https://gitlab.example", "--token", "TEST_ONLY_TOKEN_PLACEHOLDER,SECOND", "--docker_image", "alpine:3.20"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("equal cardinality", result.stderr)
        self.assertNotIn("TEST_ONLY_TOKEN_PLACEHOLDER", result.stdout + result.stderr)

    @unittest.skipUnless(BASH, "bash is required for shell action tests")
    def test_registration_validates_all_urls_before_first_execution(self) -> None:
        action = ROOT / "scripts" / "actions" / "register"
        result = subprocess.run(
            [BASH, str(action), "--gitlab_url", "https://gitlab.example,not-a-url", "--token", "TEST_ONLY_TOKEN_PLACEHOLDER,SECOND", "--docker_image", "alpine:3.20,alpine:3.20"],
            cwd=ROOT,
            env={**dict(os.environ), "RUNNER_BIN": "true"},
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("URL is invalid", result.stderr)
        self.assertNotIn("registration succeeded", result.stdout)

    @unittest.skipUnless(BASH, "bash is required for shell redaction tests")
    def test_registration_redaction_never_returns_token(self) -> None:
        token = "TEST_ONLY_TOKEN_PLACEHOLDER"
        result = subprocess.run(
            [BASH, "-c", f"source scripts/_register.sh; _register_redact 'runner failed token={token}' '{token}'"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0)
        self.assertNotIn(token, result.stdout + result.stderr)
        self.assertIn("[REDACTED]", result.stdout)

        fake = ROOT / "tests" / "fixtures" / "fake_runner.sh"
        try:
            os.chmod(fake, 0o755)
        except OSError:
            self.skipTest("cannot make fake runner executable")
        with tempfile.TemporaryDirectory() as directory:
            argv_log = Path(directory) / "argv.log"
            env_log = Path(directory) / "env.log"
            env = {
                **dict(os.environ),
                "RUNNER_BIN": "tests/fixtures/fake_runner.sh",
                "ARGV_LOG": str(argv_log),
                "ENV_LOG": str(env_log),
                "gitlab_url": "https://gitlab.example",
                "token": token,
                "docker_image": "alpine:3.20",
            }
            result = subprocess.run(
                [
                    BASH,
                    "-c",
                    "source scripts/config; run__register",
                    "register",
                ],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertNotIn(token, result.stdout + result.stderr)
            self.assertNotIn(token, argv_log.read_text(encoding="utf-8"))
            self.assertNotIn("https://gitlab.example", argv_log.read_text(encoding="utf-8"))
            self.assertIn(f"CI_SERVER_TOKEN={token}", env_log.read_text(encoding="utf-8"))
            self.assertIn("REGISTER_NON_INTERACTIVE=true", env_log.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
