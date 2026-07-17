---
name: maestro-check
description: Run a read-only drift and evidence audit between charter claims, interfaces, tasks, code, tests, CI, lifecycle and canonical records. Use before every task commit and before round review.
---

# MAESTRO Check

Pure diagnostic. Write nothing. Detect drift before it becomes a remote claim.

## Inputs

- active charter and Task-ID;
- task baseline and current diff;
- applicable specifications/ADRs;
- claim matrix;
- tests and command outputs;
- evidence index and continuity state.

## Check claims and invariants

For each claim, classify:

- `HOLD`: demonstrated at the required seam and evidence level;
- `VIOLATE`: observed behavior contradicts the claim;
- `UNVERIFIABLE`: no adequate oracle or environment;
- `OVERCLAIMED`: evidence exists but at a weaker level than stated;
- `MISSING`: required claim or invariant absent from implementation/tests;
- `EXTRA`: behavior or surface was introduced without authorization.

Cite file/line, command and output. Presence of a string, file or function is structural observation only.

## Check interfaces

For every external seam—CLI, config panel, manifest, file, env, process, service or lifecycle entry point—classify:

- `MATCH`;
- `DRIFT`;
- `MISSING`;
- `EXTRA`;
- `DEAD_PATH` when declared but not executable through the real caller.

Verify inputs, outputs, error modes, secret transport and ordering constraints, not only shape.

## Check task and commit boundaries

- Every changed path maps to the current Task-ID.
- No independent task is mixed into the diff.
- Dependencies are already remote or explicitly included cross-repo.
- The task can be reverted selectively, or dependency constraints are documented.
- RED/GREEN evidence exists for behavioral change.
- Subagent outputs are integrated or explicitly discarded.

## Check evidence levels

Use only:

- `STRUCTURALLY_OBSERVED`;
- `LOCAL_VERIFIED`;
- `REMOTE_CI_VERIFIED`;
- `LIFECYCLE_VERIFIED`;
- `UNVERIFIED`;
- `FAILED`.

Examples:

- grep finds `run__register`: structural only;
- test invokes `run__register` and captures helper call: local verified;
- workflow run tied to commit succeeds: remote CI verified;
- package install/backup/restore scenario succeeds: lifecycle verified.

Do not infer a stronger level.

## Evidence provenance and immutability

An artifact that records an observation is semantically immutable. Formatting or schema migration must not add a factual result that the original command did not emit.

For every observed report:

- preserve the original payload or archive it under a versioned path;
- create a new artifact for a new observation;
- record `producer_commit`, exact command, `observed_at`, source/final URL where applicable, result and limitation;
- mark the prior artifact `SUPERSEDED` in the index instead of completing it retrospectively;
- treat a field added by hand as metadata only, never as proof of the field's value;
- reject `verified`, `valid`, `passed` or equivalent when provenance points only to a schema edit, fixture rewrite or documentation task.

For external transports, inspect the real redirect/final-origin chain used by the current official endpoint. A mock that replaces the fetch layer can prove parser behavior but cannot prove transport compatibility.

## Check canonical memory

- one authoritative state file per concern;
- no duplicate evidence index;
- status, handoff and active round agree;
- paths are remote and portable;
- claims cite current SHAs/Task-IDs;
- final continuity uses already-published SHAs, not future tense or pre-task placeholders;
- historical failures are not silently deleted.

## Report

Group findings by severity:

- P0: unsafe state, secret, destructive or trust failure;
- P1: charter/behavior/lifecycle defect that blocks commit;
- P2: material quality or evidence gap;
- P3: low-risk improvement.

For each finding provide evidence, violated contract and remedy hint. Do not apply fixes. An empty report must list the surfaces, commands and evidence checked; “looks good” is not a valid report.
