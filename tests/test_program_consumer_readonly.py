from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONSUMER = ROOT / "scripts" / "program_consumer.py"


class ProgramConsumerReadOnlyTests(unittest.TestCase):
    def test_consumer_uses_temporary_queue_and_preserves_tracked_projection(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            coordinator = root / "coordinator"
            runner = root / "runner"
            scripts = coordinator / "scripts"
            continuity = coordinator / "continuity"
            scripts.mkdir(parents=True)
            continuity.mkdir()
            runner.mkdir()
            tracked_queue = continuity / "PROGRAM_QUEUE.json"
            tracked_queue.write_text('{"sentinel":"unchanged"}\n', encoding="utf-8")
            (continuity / "PROGRAM_BACKLOG.json").write_text('{"tasks":[]}\n', encoding="utf-8")
            (continuity / "PROGRAM_FINDINGS.json").write_text('{"findings":[]}\n', encoding="utf-8")
            engine = scripts / "maestro_program.py"
            engine.write_text(
                """#!/usr/bin/env python3
import json, pathlib, sys
command = sys.argv[1]
queue = pathlib.Path(sys.argv[sys.argv.index('--queue') + 1])
if command == 'refresh-queue':
    queue.write_text(json.dumps({'derived': True}), encoding='utf-8')
    payload = {'derived': True}
elif command == 'doctor':
    payload = {'valid': queue.is_file()}
else:
    payload = {'valid': queue.is_file(), 'eligible_tasks': [], 'lanes': [], 'stop_allowed': False, 'checkpoint_allowed': True, 'stop_reason': 'CHECKPOINT', 'parallelism_required': False}
print(json.dumps(payload))
""",
                encoding="utf-8",
            )
            completed = subprocess.run(
                [sys.executable, str(CONSUMER), "--coordinator-root", str(coordinator), "--runner-root", str(runner)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
            self.assertEqual(tracked_queue.read_text(encoding="utf-8"), '{"sentinel":"unchanged"}\n')
            self.assertTrue(json.loads(completed.stdout)["checkpoint_allowed"])


if __name__ == "__main__":
    unittest.main()
