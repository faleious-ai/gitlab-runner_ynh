from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "evidence" / "wp02e-live-trust-observation.json"
PRODUCER_COMMIT = "6fb500ec3474c07137fcb8962512ed0adc59a9bb"


class LiveObservationProvenanceTests(unittest.TestCase):
    def test_live_failure_artifact_is_provenance_bound_and_portable(self) -> None:
        self.assertTrue(ARTIFACT.is_file())
        report = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(report["artifact_kind"], "live-observation-failure")
        self.assertEqual(report["producer_commit"], PRODUCER_COMMIT)
        self.assertEqual(report["result"], "failed")
        self.assertEqual(report["command"], "PYTHONDONTWRITEBYTECODE=1 python3 scripts/autoupdate.py discover --manifest manifest.toml --report evidence/wp02e-live-trust-observation.json --timeout 5 --retries 0")
        self.assertEqual(report["failure"]["stage"], "official-checksum-fetch")
        self.assertEqual(report["failure"]["return_code"], 2)
        self.assertEqual(report["trust"]["status"], "not-observed")
        self.assertEqual(report["trust"]["key_validity"], "not-observed")
        serialized = ARTIFACT.read_text(encoding="utf-8")
        self.assertNotRegex(serialized, re.compile(r"(?:/workspace/|/root/|/tmp/|[A-Za-z]:\\)"))
        self.assertNotIn("temporary=", serialized)
        self.assertNotIn("key_fingerprint", report["trust"])


if __name__ == "__main__":
    unittest.main()
