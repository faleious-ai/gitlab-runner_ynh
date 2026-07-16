import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class LegacyRegistrationTests(unittest.TestCase):
    def test_legacy_action_and_token_flag_are_absent_from_active_entry_points(self):
        self.assertFalse((ROOT / "scripts" / "actions" / "register").exists())
        active_paths = [
            ROOT / "scripts" / "config",
            ROOT / "scripts" / "_register.sh",
            ROOT / "scripts" / "install",
            ROOT / "scripts" / "restore",
        ]
        for path in active_paths:
            self.assertNotIn("--token", path.read_text(encoding="utf-8"), str(path))


if __name__ == "__main__":
    unittest.main()
