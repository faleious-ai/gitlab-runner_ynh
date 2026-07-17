import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "evidence" / "wp02e-integration-gates.json"


class IntegrationEvidenceTests(unittest.TestCase):
    def test_integration_report_preserves_claim_boundaries(self):
        self.assertTrue(ARTIFACT.is_file())
        report = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(report["artifact_id"], "EVD-WP02E-INTEGRATION")
        self.assertEqual(report["task_id"], "T-WP02E-06-integration-gates")
        self.assertEqual(report["producer_commit"], "978ec18218e38920a169aa15490ec0cab4399133")
        self.assertEqual(report["evidence_state"], "LOCAL_VERIFIED")
        self.assertEqual(report["result"], "passed")
        self.assertEqual(report["manifest"]["version"], "18.6.2~ynh1")
        self.assertTrue(report["manifest"]["unchanged"])
        self.assertFalse(report["safety"]["credential_used"])
        self.assertFalse(report["safety"]["real_registration"])
        self.assertFalse(report["safety"]["manifest_promoted"])
        gates = {gate["name"]: gate for gate in report["gates"]}
        self.assertEqual(gates["unit_tests"]["count"], 37)
        self.assertEqual(gates["lifecycle_harness"]["result"], "passed")
        self.assertFalse(gates["autoupdate_check"]["promoted"])
        self.assertEqual(gates["t02_live_result_oracle"]["trust_status"], "not-observed")
        self.assertEqual(gates["t05_remote_ci_oracle"]["observed_state"], "UNVERIFIED")
        self.assertEqual(len(report["task_commits"]), 5)
        serialized = ARTIFACT.read_text(encoding="utf-8")
        self.assertNotIn("/workspace/", serialized)
        self.assertNotIn("/root/", serialized)


if __name__ == "__main__":
    unittest.main()
