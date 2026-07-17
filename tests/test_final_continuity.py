import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class FinalContinuityV2Tests(unittest.TestCase):
    def test_runner_continuity_points_to_program_v2_and_current_round(self) -> None:
        active = (ROOT / "continuity" / "ACTIVE_ROUND.md").read_text(encoding="utf-8")
        status = (ROOT / "continuity" / "STATUS.md").read_text(encoding="utf-8")
        handoff = (ROOT / "continuity" / "HANDOFF_CURRENT.md").read_text(encoding="utf-8")
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        consumer = ROOT / "scripts" / "program_consumer.py"

        self.assertIn("CHR-PROGRAM-V2-CONTINUE-001", active)
        self.assertIn("State: `IN_PROGRESS`", active)
        self.assertIn("PROGRAM_V2_IN_PROGRESS", status)
        self.assertIn("IN_PROGRESS", handoff)
        self.assertIn("program_consumer.py", agents)
        self.assertTrue(consumer.is_file())
        self.assertNotIn("WP02E_EXECUTED_AWAITING_REVIEW", status)
        self.assertNotIn("eligible_tasks=[]", handoff)

    def test_historical_evidence_remains_history_not_current_authority(self) -> None:
        index = (ROOT / "evidence" / "EVIDENCE_INDEX.md").read_text(encoding="utf-8")
        self.assertIn("EVD-RUNNER-LIVE-TRUST | LOCAL_VERIFIED", index)
        self.assertIn("EVD-RUNNER-REMOTE-CI | FAILED", index)


if __name__ == "__main__":
    unittest.main()
