import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "evidence" / "wp02e-remote-ci-observation.json"


class RemoteCiObservationTests(unittest.TestCase):
    def test_remote_ci_observation_is_portable_and_unverified(self):
        self.assertTrue(ARTIFACT.is_file())
        report = json.loads(ARTIFACT.read_text(encoding="utf-8"))
        self.assertEqual(report["artifact_id"], "EVD-WP02E-REMOTE-CI")
        self.assertEqual(report["artifact_kind"], "remote-ci-observation")
        self.assertEqual(report["task_id"], "T-WP02E-05-remote-ci-observation")
        self.assertEqual(report["producer_commit"], "2563fc31e1b71db89315fd8c707235ed98659962")
        self.assertEqual(report["target_commit"], report["producer_commit"])
        self.assertEqual(report["result"], "unverified")
        self.assertEqual(report["evidence_state"], "UNVERIFIED")
        observations = {item["mechanism"]: item for item in report["observations"]}
        self.assertEqual(observations["github_fetch_commit_workflow_runs"]["result"], "workflow_runs=[]")
        self.assertEqual(observations["github_get_commit_combined_status"]["result"], "statuses=[]")
        self.assertEqual(observations["gh"]["result"], "unavailable")
        self.assertTrue(report["local_equivalent_gates"]["not_remote_ci_evidence"])
        serialized = ARTIFACT.read_text(encoding="utf-8")
        self.assertNotIn("/workspace/", serialized)
        self.assertNotIn("/root/", serialized)


if __name__ == "__main__":
    unittest.main()
