from __future__ import annotations

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

    def test_verified_reports_record_observed_key_validity(self) -> None:
        expected_fingerprint = "931DA69CFA3AFEBBC97DAA8C6C57C29C6BA75A4E"
        for name in ("wp02-checksum-trust.json", "wp02-online-discovery.json"):
            payload = json.loads((EVIDENCE / name).read_text(encoding="utf-8"))
            signatures = []
            if "signature" in payload:
                signatures.append(payload["signature"])
            if "discovery" in payload:
                signatures.append(payload["discovery"]["signature"])
            if "release" in payload:
                signatures.append(payload["release"]["checksum_trust"]["signature"])
            for signature in signatures:
                if signature.get("status") == "verified":
                    self.assertEqual(signature.get("key_fingerprint"), expected_fingerprint, name)
                    self.assertEqual(signature.get("key_validity"), "valid", name)

    def test_current_round_evidence_is_task_and_sha_traceable(self) -> None:
        index = (EVIDENCE / "EVIDENCE_INDEX.md").read_text(encoding="utf-8")
        required = {
            "EVD-WP02D-YUNOHOST-RUN-CONTROLLER": "ada6b78ca4db00c1dcacda4eb01736f123f6040b",
            "EVD-WP02D-EPHEMERAL-REGISTRATION-INPUTS": "ada6b78ca4db00c1dcacda4eb01736f123f6040b",
            "EVD-WP02D-NO-LEGACY-ARGV": "79fb763c6c2d20f9bb1b76e42a266da1b41e8ad9",
            "EVD-WP02D-LIFECYCLE-IDENTITY": "2f0185cbf8b630f94d9618c9d7afe56cabc434b3",
            "EVD-WP02D-SIGNATURE-FAIL-CLOSED": "35e8e44dd9fb39b47ad71e6dfb06e854c0029618",
            "EVD-WP02D-SELF-LINK-REDIRECTS": "51dbb98a7e6de477c4f3234b1c7d40b4ac1a54ac",
            "EVD-WP02D-CANONICAL-EVIDENCE": "T-WP02D-06",
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
