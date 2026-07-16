---
name: maestro-build
description: Execute an authorized MAESTRO task end-to-end against its charter, using subagents where safe, TDD for behavior, backpropagation on failure, internal review, one remote commit per task and no self-acceptance.
---

# MAESTRO Build

Execute one authorized task to a remotely verifiable state. The round authorizes; the task implements, commits, synchronizes and reverts.

## Load

1. Read `AGENTS.md`, current status, handoff and active charter.
2. Confirm charter `READY`, branch `master`, clean tree and current `origin/master`.
3. Select the next unblocked `Task-ID` from the DAG.
4. Load only the specification, ADRs, sources and skills needed by that task.
5. Confirm seam, claims, paths, dependencies, gates, rollback and commit message.

If the task contract is incomplete, use `maestro-spec` before editing.

## Pre-build

For high-impact work—security, credentials, public interfaces, lifecycle, supply chain, destructive paths or shared modules—run `maestro-review` in pre-build mode. Do not edit while verdict is `NO_GO`.

## Execute

1. Mark the task in progress in the appropriate working record when needed.
2. Dispatch subagents only for independent outputs with explicit path ownership. They do not commit or push.
3. For behavioral change, invoke `maestro-tdd` and observe RED before implementation.
4. Implement the minimum code needed for the current vertical slice.
5. Run the cheapest relevant gate, then progressively deeper gates.
6. On unexpected failure, invoke `maestro-backprop`; do not retry blindly.
7. Integrate subagent outputs centrally and re-run behavior at the real seam.
8. Keep the claim matrix current: claim, mechanism, command, result, evidence level, limitation.

Do not stop for progress reports, task length, research, first failed approach or ordinary test failure. Continue every independent DAG node.

## Gate cascade

Apply proportionally:

1. syntax, schema, parse, lint or build;
2. focal RED/GREEN tests;
3. integration and negative cases;
4. security, secret and provenance checks;
5. lifecycle/smoke: install, upgrade, service, backup, restore, remove as applicable;
6. remote CI and external probes when the claim is remote.

A later gate never substitutes for a missing earlier one. A passing unit test never proves lifecycle.

## Pre-commit

Run, in order:

1. `maestro-check` read-only drift audit;
2. `maestro-review` with independent Spec/Charter and Engineering axes;
3. `maestro-guardrails` against the final diff;
4. secret scan and exact gate reruns affected by review fixes.

P0/P1 findings block the commit. P2/P3 are fixed or explicitly reasoned in the review packet.

## Commit and sync

1. Fetch and reconcile `origin/master` without rewriting published history.
2. Ensure the diff contains only this task and its tests/evidence.
3. Create exactly one commit: `RND-<id> T-<id>: <result>`.
4. Push fast-forward to `origin/master` without force.
5. Fetch again; confirm local HEAD equals remote HEAD and SHA is retrievable.
6. Only then mark the task remotely complete and start the next writing task.

Do not create a separate commit for RED. Preserve RED output in a versioned report, fixture or round record; the task commit includes the regression test and coherent fix.

## Exit

A task exits as:

- `TASK_REMOTE_VERIFIED`;
- `TASK_LOCAL_COMPLETE_AWAITING_SYNC`;
- `TASK_REMOTE_SYNC_BLOCKED`;
- a documented dependency or human gate after all independent work is done.

The final task of the round reconciles continuity and the complete remote review packet. Never output or persist `ACCEPTED`; that belongs to the external orchestrator/reviewer.