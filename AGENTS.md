# Runner program contract

This repository consumes the canonical MAESTRO program maintained in `faleious-ai/gitlab_ynh`.

The startup sequence is a fast-forward synchronization of coordinator and Runner, followed by the Runner consumer:

`python scripts/program_consumer.py --coordinator-root ../gitlab_ynh --runner-root .`

The consumer combines static backlog tasks with dynamic correction tasks from `PROGRAM_FINDINGS.json`. The planner defines ordering, lane requirements, checkpoints and completion.

Behavioral work follows public-seam RED/GREEN validation. Parallel preparation uses distinct workers and isolated workspaces with recorded artifacts and logs. Integration and publication remain serial per task and repository. A SELF-bound receipt accompanies the implementation and evidence in the same commit.

Protected contracts remain owned by the Orchestrator. External actions with material consequences remain governed by their declared gates. Queue emptiness alone is not a completion signal.
