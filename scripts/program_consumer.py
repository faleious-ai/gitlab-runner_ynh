#!/usr/bin/env python3
"""Read-only Runner adapter for the coordinator MAESTRO program engine."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def run_engine(engine: Path, coordinator: Path, runner: Path, command: str) -> dict[str, Any]:
    completed = subprocess.run(
        [
            sys.executable,
            str(engine),
            command,
            "--root",
            str(coordinator),
            "--repo",
            f"coordinator={coordinator}",
            "--repo",
            f"runner={runner}",
        ],
        text=True,
        capture_output=True,
        check=False,
    )
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as error:
        raise RuntimeError(f"coordinator engine did not emit JSON: {completed.stdout!r}") from error
    if completed.returncode not in {0, 2}:
        raise RuntimeError(completed.stderr or completed.stdout)
    return payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coordinator-root", required=True)
    parser.add_argument("--runner-root", default=".")
    args = parser.parse_args(argv)
    coordinator = Path(args.coordinator_root).resolve()
    runner = Path(args.runner_root).resolve()
    engine = coordinator / "scripts" / "maestro_program.py"
    backlog_path = coordinator / "continuity" / "PROGRAM_BACKLOG.json"
    if not engine.is_file() or not backlog_path.is_file():
        print(json.dumps({"valid": False, "reasons": ["COORDINATOR_PROGRAM_NOT_AVAILABLE"]}, sort_keys=True))
        return 2
    refresh = run_engine(engine, coordinator, runner, "refresh-queue")
    doctor = run_engine(engine, coordinator, runner, "doctor")
    plan = run_engine(engine, coordinator, runner, "plan")
    backlog = json.loads(backlog_path.read_text(encoding="utf-8"))
    by_id = {task["id"]: task for task in backlog["tasks"]}
    runner_tasks = [task_id for task_id in plan.get("eligible_tasks", []) if "runner" in by_id[task_id]["repositories"]]
    runner_lanes = [
        lane for lane in plan.get("lanes", []) if any(task_id in runner_tasks for task_id in lane.get("task_ids", []))
    ]
    result = {
        "valid": bool(refresh.get("derived")) and doctor.get("valid") is True and plan.get("valid") is True,
        "eligible_runner_tasks": runner_tasks,
        "runner_lanes": runner_lanes,
        "program_stop_allowed": plan.get("stop_allowed", False),
        "checkpoint_allowed": plan.get("checkpoint_allowed", False),
        "stop_reason": plan.get("stop_reason"),
        "parallelism_required": plan.get("parallelism_required", False),
        "coordinator_plan": plan,
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["valid"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
