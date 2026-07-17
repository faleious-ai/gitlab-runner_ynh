# Runner handoff v2

State: `IN_PROGRESS`
Charter: `CHR-PROGRAM-V2-CONTINUE-001`
Expected initial round: `RND-20260717-017`

Current task: `T-GOV-ARCHITECTURE-V2-READONLY-CONSUMER` is locally GREEN and paired with the coordinator correction. The next planner-selected Runner task is `T-RUN-CI-REPAIR-001`.

Coordinator and Runner synchronization precedes the Runner consumer. Lane records include isolated workspaces, artifacts and logs. Canonical integration is one task at a time with a SELF-bound receipt, followed by publication and replanning. Program completion is a semantic planner result rather than simple queue emptiness.
