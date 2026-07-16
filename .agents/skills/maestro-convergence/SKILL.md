---
name: maestro-convergence
description: Measure whether iterative engineering work is converging, oscillating, regressing or blocked by a ceiling. Prioritize claims, gates and findings over diff size, and trigger upstream correction instead of adding blind iterations.
---

# MAESTRO Convergence

Iteration count is a budget, not proof. Stop or continue according to measurable state.

## Metrics per cycle

Record:

- claims/invariants demonstrated versus total;
- focal, integration, security, lifecycle and CI gates passing/failing;
- findings P0/P1/P2/P3 opened and closed;
- tasks done, active, blocked and unstarted;
- test count and pass/fail/skip state;
- repeated failure categories from the learning ledger;
- files/lines changed as a secondary stability signal;
- remote synchronization state.

Do not use coverage percentage or diff size alone as quality.

## Classify

### CONVERGING

- demonstrated claims increase;
- failures/findings decrease without new regressions;
- task frontier advances;
- repeated failures do not recur;
- later diffs narrow toward integration and evidence.

### CONVERGED

- every required claim is proven at its required evidence level or explicitly gated;
- all mandatory gates pass;
- no P0/P1 finding remains;
- no unauthorized behavior or stale task exists;
- all task commits are remote and integrated;
- remaining P2/P3 items are accepted, deferred with rationale or out of scope.

### CEILING

- progress is blocked by a missing environment, permission, external service, unavailable source or material human decision;
- the same environmental error persists despite reasonable alternatives;
- independent work is complete.

A ceiling is not convergence. Record the exact unblock condition.

### OSCILLATING

- fixes alternate between two incompatible states;
- pass/fail results move back and forth;
- agents repeatedly overwrite the same design choice;
- interfaces or specs conflict.

Stop forward implementation and repair specification, precedence or ownership.

### REGRESSING

- previously passing gate fails;
- demonstrated claim loses evidence;
- tests are deleted/weakened to obtain green;
- new P0/P1 findings exceed closed ones;
- task commits introduce unrelated scope.

Treat regression as blocking. Identify the first offending task commit and correct or revert it.

### STALLED

- claims, tasks and findings do not change across repeated cycles;
- the same strategy is retried;
- small diffs occur while mandatory tests still fail.

Invoke `maestro-backprop` and diagnose the process gap before another iteration.

## Thresholds

- two repeats of the same unexplained failure: mandatory root-cause review;
- three entries in the same backprop pattern category: create a systemic task;
- any P0 or regression: stop forward progress in dependent tasks;
- remote sync blocked: no additional commits in that repository.

Thresholds do not authorize abandoning independent work.

## Recovery

1. freeze dependent forward work;
2. classify convergence state with evidence;
3. inspect spec clarity, oracle quality, ownership, external dependencies and task size;
4. amend the narrowest upstream contract or validation;
5. resume from current remote history; do not restart completed tasks;
6. record before/after metrics.

## Report

Use a compact matrix when safe:

`cycle|claims|gates|P0/P1|tasks|backprop|sync|state|next`

Explain any `CEILING`, `OSCILLATING`, `REGRESSING` or `STALLED` state in complete prose. A completion sentinel or agent statement never overrides the metrics and gates.