import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL = {
    name: (ROOT / "continuity" / name).read_text(encoding="utf-8")
    for name in ("ACTIVE_ROUND.md", "HANDOFF_CURRENT.md", "STATUS.md")
}
CANONICAL["EVIDENCE_INDEX.md"] = (ROOT / "evidence" / "EVIDENCE_INDEX.md").read_text(encoding="utf-8")
ROUND = (ROOT / "continuity" / "rounds" / "RND-20260717-012.md").read_text(encoding="utf-8")


TASK_SHAS = {
    "T-WP02E-01-official-key-transport": "6fb500ec3474c07137fcb8962512ed0adc59a9bb",
    "T-WP02E-02-live-trust-observation": "8c0c52592d2ccd3f9ebd706d56e63f9b12410f69",
    "T-WP02E-03-historical-evidence-repair": "ea9774001fbf181b5fc210a17fad6a1208a83d4c",
    "T-WP02E-04-docker-default-consistency": "2563fc31e1b71db89315fd8c707235ed98659962",
    "T-WP02E-05-remote-ci-observation": "978ec18218e38920a169aa15490ec0cab4399133",
    "T-WP02E-06-integration-gates": "08563cbd2c957e6cca16ae6535a56ef9b2d52b9e",
}


class FinalContinuityTests(unittest.TestCase):
    def test_canonical_state_uses_published_task_shas_and_final_status(self):
        self.assertIn("Estado: `EXECUTED_AWAITING_REVIEW`", CANONICAL["ACTIVE_ROUND.md"])
        self.assertIn("Estado: `EXECUTED_AWAITING_REVIEW`", CANONICAL["HANDOFF_CURRENT.md"])
        self.assertIn("WP02E_EXECUTED_AWAITING_REVIEW", CANONICAL["STATUS.md"])
        self.assertNotIn("READY_FOR_CODEX_FULL_ROUND", CANONICAL["HANDOFF_CURRENT.md"])
        self.assertNotIn("Última rodada executada pelo Codex: `RND-20260716-010`", CANONICAL["STATUS.md"])
        self.assertNotIn("Próxima ação", CANONICAL["STATUS.md"])
        self.assertIn("EVD-WP02E-LIVE-TRUST | UNVERIFIED", CANONICAL["EVIDENCE_INDEX.md"])
        self.assertIn("EVD-WP02E-REMOTE-CI | UNVERIFIED", CANONICAL["EVIDENCE_INDEX.md"])
        self.assertIn("EVD-WP02E-FINAL-CONTINUITY | LOCAL_VERIFIED", CANONICAL["EVIDENCE_INDEX.md"])
        for task_id, sha in TASK_SHAS.items():
            self.assertIn(task_id, CANONICAL["STATUS.md"] + CANONICAL["EVIDENCE_INDEX.md"] + ROUND)
            self.assertIn(sha, CANONICAL["STATUS.md"] + CANONICAL["EVIDENCE_INDEX.md"] + ROUND)
        self.assertIn("this task commit", ROUND)
        self.assertIn("EXECUTED_AWAITING_REVIEW", ROUND)
        self.assertIn("Estado: `EXECUTED_AWAITING_REVIEW`", ROUND)
        self.assertNotIn("Estado: `ACCEPTED`", "".join(CANONICAL.values()) + ROUND)


if __name__ == "__main__":
    unittest.main()
