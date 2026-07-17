from __future__ import annotations

import hashlib
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
ABSOLUTE_LOCAL_PATH = re.compile(r"(?:^|[\s\"'(])(?:/workspace/|/root/|/tmp/|[A-Za-z]:[\\/])")


def _strings(value: object, path: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from _strings(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _strings(child, f"{path}[{index}]")
    elif isinstance(value, str):
        yield path, value


class EvidencePortabilityTests(unittest.TestCase):
    def test_json_reports_have_no_machine_local_paths(self) -> None:
        for report_path in sorted(EVIDENCE.glob("*.json")):
            payload = json.loads(report_path.read_text(encoding="utf-8"))
            for path, value in _strings(payload):
                if "://" not in value:
                    self.assertIsNone(ABSOLUTE_LOCAL_PATH.search(value), f"{report_path}:{path}: {value}")

    def test_historical_reports_preserve_pre_t06_semantics_and_are_superseded(self) -> None:
        expected_sha256 = {
            "wp02-checksum-trust.json": "3c0b97751115896db04adaeef42e39d4008b29c94117665002edd695e750c4ed",
            "wp02-online-discovery.json": "285ca22df3d45d6185e5b95a5e5a2bfcef9a4c6993c0aca689f47881b8d4c421",
        }
        index = (EVIDENCE / "EVIDENCE_INDEX.md").read_text(encoding="utf-8")
        self.assertIn("| EVD-ARCH-V2-RUNNER | LOCAL_VERIFIED |", index)
        self.assertIn("SUPERSEDED", index)
        for name, expected in expected_sha256.items():
            payload = (EVIDENCE / name).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), expected, name)

        live = json.loads((EVIDENCE / "wp02e-live-trust-observation.json").read_text(encoding="utf-8"))
        self.assertEqual(live["result"], "failed")
        self.assertEqual(live["trust"]["status"], "not-observed")

    def test_current_round_evidence_is_task_and_sha_traceable(self) -> None:
        index = (EVIDENCE / "EVIDENCE_INDEX.md").read_text(encoding="utf-8")
        required = {
            "EVD-ARCH-V2-RUNNER": "7dc24ccb8b539c052966eee4d22820e51e418433",
            "EVD-ARCH-V2-HARDEN-RUNNER": "dafcac9a26e56d8c3731fae66e9e4cc5f5a0d015",
            "EVD-RUNNER-DOCKER-DEFAULT": "40e3a0854da387ed51320afa15416abb1747009f",
            "EVD-RUNNER-FULL-SUITE-LINUX": "7dc24ccb8b539c052966eee4d22820e51e418433",
        }
        for evidence_id, trace in required.items():
            self.assertIn(f"| {evidence_id} |", index)
            self.assertIn(trace, index)

    def test_round_records_explain_red_green_or_not_applicable(self) -> None:
        round_record = (ROOT / "continuity" / "rounds" / "RND-20260716-010.md").read_text(encoding="utf-8")
        for task in ("T-WP02D-01", "T-WP02D-02", "T-WP02D-03", "T-WP02D-04", "T-WP02D-05"):
            section = round_record.split(f"## {task}", 1)[1].split("## ", 1)[0]
            self.assertIn("RED observado", section, task)
            self.assertIn("GREEN observado", section, task)
        section = round_record.split("## T-WP02D-06", 1)[1].split("## T-WP02D-07", 1)[0]
        self.assertIn("NOT_APPLICABLE", section)


if __name__ == "__main__":
    unittest.main()
