from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLI = ROOT / "scripts" / "autoupdate.py"
FIXTURE = ROOT / "scripts" / "autoupdate" / "fixtures" / "release-v19.0.1.json"
MANIFEST = ROOT / "manifest.toml"


class LiveCandidateTests(unittest.TestCase):
    def test_fixed_runner_and_helper_candidate_is_non_promoting(self) -> None:
        before = hashlib.sha256(MANIFEST.read_bytes()).hexdigest()
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "candidate.toml"
            report = Path(directory) / "candidate.json"
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CLI),
                    "generate",
                    "--fixture",
                    str(FIXTURE),
                    "--manifest",
                    str(MANIFEST),
                    "--output",
                    str(output),
                    "--report",
                    str(report),
                    "--write",
                ],
                cwd=ROOT,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
            payload = json.loads(report.read_text(encoding="utf-8"))
            self.assertEqual(payload["mode"], "write")
            self.assertTrue(payload["changed"])
            self.assertFalse(payload["promoted"])
            self.assertEqual(payload["candidate_upstream_version"], "19.0.1")
            self.assertEqual(len(payload["release"]["runner"]), 3)
            self.assertEqual(payload["release"]["helper_images"]["architectures"], ["amd64", "arm64", "armhf"])
            self.assertEqual(
                {len(asset["sha256"]) for asset in payload["release"]["runner"]}
                | {len(payload["release"]["helper_images"]["sha256"])},
                {64},
            )
            self.assertEqual(hashlib.sha256(MANIFEST.read_bytes()).hexdigest(), before)
            self.assertIn('version = "19.0.1~ynh1"', output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

