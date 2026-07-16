---
name: maestro-deepen
description: Improve one shallow module in a dedicated task while preserving behavior, reducing interface burden and keeping tests green before and after. Never run as incidental cleanup inside a feature task.
---

# MAESTRO Deepen

Refactor structure only. Behavior is frozen.

## Preconditions

- dedicated authorized Task-ID;
- current focal and integration suites green;
- no active feature work in the same paths;
- public behavior and compatibility baseline recorded;
- rollback is the single task commit.

If behavior must change, stop and route through `maestro-spec`, `maestro-tdd` and `maestro-build` as a behavioral task.

## Select one module

Choose the most consequential shallow module touched by recent work. Evidence of shallowness includes:

- callers must know hidden ordering, policy or platform details;
- pass-through layers add interface without hiding complexity;
- the same decision is repeated across callers;
- a logical change causes edits across many files;
- multiple flags or primitive strings encode one domain concept;
- tests must reach through the public interface to inspect internals.

Do not sweep the codebase. One module per task.

## Diagnose

State:

- current interface and callers;
- hidden fact leaked to callers;
- change amplification or recurring defect caused by the design;
- why the module is shallow;
- behavior that must remain invariant.

Cite files and tests. “Could be cleaner” is not sufficient.

## Design

Prefer:

- a smaller public interface with stronger invariants;
- complexity pulled behind the interface;
- dependencies accepted at a deliberate seam;
- results returned instead of uncontrolled side effects;
- errors designed out where practical;
- one authoritative implementation of a decision.

Do not add an abstraction for a single hypothetical variation. A real seam normally has at least two adapters or a demonstrated test/replacement need.

## Verify

1. Run the full applicable suite before changes and record the baseline.
2. Add characterization tests only where existing behavior is not protected.
3. Refactor incrementally; keep tests green.
4. Verify old callers or provide an authorized migration with compatibility tests.
5. Run focal, integration and lifecycle gates after.
6. Compare public interfaces before/after and demonstrate reduced surface or hidden knowledge.

## Review and commit

Run `maestro-check`, both-axis `maestro-review` and `maestro-guardrails`. The commit must contain only the selected structural task and tests that preserve behavior.

Completion requires:

- interface demonstrably smaller or safer;
- leaked decision localized;
- no behavior or compatibility drift;
- green gates before and after;
- no speculative extension;
- one remotely verified task commit.