---
name: maestro-review
description: Perform evidence-grounded adversarial review before high-impact implementation and before every task commit. Keep Spec/Charter and Engineering/Security/Lifecycle findings independent and never self-accept.
---

# MAESTRO Review

A review attempts to refute the work. “Looks good” is not evidence.

## Modes

### PRE_BUILD_SPEC_CHALLENGE

Use before the first edit of high-impact work.

1. Read the task contract, relevant charter, ADRs, code callers and primary-source research.
2. Try to disprove:
   - goal solves the actual problem;
   - public seam is real and testable;
   - invariants cover failure, ordering, secrets and rollback;
   - interface matches callers and platform contracts;
   - task boundaries and dependencies are complete;
   - lifecycle and negative cases are owned;
   - proposed validation can detect the claimed defect.
3. Classify findings:
   - `BLOCK`: building now would create a material defect;
   - `HARDEN`: add or sharpen claim/invariant/test;
   - `NOTE`: non-blocking information.
4. End with `GO` or `NO_GO` and evidence.

Technical reversible hardening is applied through `maestro-spec`. A material human choice routes to `maestro-grill`.

### PRE_COMMIT_TASK_REVIEW

Run two independent contexts or subagents against the exact task diff and baseline.

#### Axis A — Spec/Charter

Find:

- missing or partially implemented requirements;
- unauthorized behavior or scope creep;
- interface drift;
- claim without adequate evidence;
- task marked complete while dependency or output is absent;
- technical amendment not backpropagated to the proper contract.

#### Axis B — Engineering/Security/Lifecycle

Find:

- logic and error-path defects;
- secret exposure, trust downgrade or unsafe defaults;
- lifecycle gaps across install/upgrade/backup/restore/remove;
- compatibility and rollback failures;
- dead paths and implementation-only tests;
- unnecessary complexity, duplication with consequence or speculative abstraction;
- non-atomic state transitions and partial output.

Do not let either axis see or anchor on the other’s conclusions before producing its report.

## Evidence rule

Every finding cites file/line, command/output or authoritative source. A hunch is tagged `UNVERIFIED` and cannot be P0/P1 without supporting evidence.

## Severity

- P0: active unsafe state, secret, destructive action, trust failure or data loss.
- P1: material spec, behavior, lifecycle or compatibility defect; blocks commit.
- P2: substantial quality, operability or evidence gap.
- P3: low-risk improvement.

## Finding lifecycle

For every finding, the executor must:

- fix it and cite the verification;
- reject it with evidence and rationale; or
- escalate the exact material decision.

No finding may disappear silently. After fixes, rerun affected tests and both-axis review where the change is material.

## Round review preparation

Before declaring the round reviewable, inspect the ordered task commits and integrated baseline→head diff. Look for cross-task regression, incompatible interfaces, stale continuity and evidence overclaim.

## Boundaries

- Do not write implementation during review.
- Do not mark `ACCEPTED`; external ChatGPT owns final review.
- Do not inflate style preferences into blockers.
- Do not review trivial changes with ceremony disproportionate to risk, but every task still receives the two-axis pre-commit check.