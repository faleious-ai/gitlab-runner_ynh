from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONSUMER = ROOT / "scripts" / "program_consumer.py"


class ProgramQueueConsumerAcceptanceTests(unittest.TestCase):
    def test_consumer_uses_coordinator_engine_and_filters_runner_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            coordinator = root / "coordinator"
            runner = root / "runner"
            (coordinator / "scripts").mkdir(parents=True)
            (coordinator / "continuity").mkdir()
            runner.mkdir()
            engine = coordinator / "scripts" / "maestro_program.py"
            engine.write_text(
                """#!/usr/bin/env python3
import json, sys
command=sys.argv[1]
if command == 'refresh-queue': payload={'derived': True}
elif command == 'doctor': payload={'valid': True}
else: payload={'valid': True, 'eligible_tasks':['T-RUN','T-COORD'], 'lanes':[{'lane_id':'L1','task_ids':['T-RUN']}], 'stop_allowed':False, 'checkpoint_allowed':False, 'stop_reason':'ELIGIBLE_WORK_REMAINS', 'parallelism_required':True}
print(json.dumps(payload))
""",
                encoding="utf-8",
            )
            backlog = {
                "tasks": [
                    {"id": "T-RUN", "repositories": ["runner"]},
                    {"id": "T-COORD", "repositories": ["coordinator"]},
                ]
            }
            (coordinator / "continuity" / "PROGRAM_BACKLOG.json").write_text(
                json.dumps(backlog), encoding="utf-8"
            )
            completed = subprocess.run(
                [
                    sys.executable,
                    str(CONSUMER),
                    "--coordinator-root",
                    str(coordinator),
                    "--runner-root",
                    str(runner),
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr or completed.stdout)
            result = json.loads(completed.stdout)
            self.assertEqual(result["eligible_runner_tasks"], ["T-RUN"])
            self.assertFalse(result["program_stop_allowed"])
            self.assertTrue(result["parallelism_required"])

    def test_consumer_fails_closed_without_coordinator_program(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            completed = subprocess.run(
                [sys.executable, str(CONSUMER), "--coordinator-root", str(root), "--runner-root", str(root)],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertIn("COORDINATOR_PROGRAM_NOT_AVAILABLE", completed.stdout)


if __name__ == "__main__":
    unittest.main()
