---
name: maestro-backprop
description: Trace every unexpected failure or review finding to the narrowest cause, classify the contract gap, add a regression oracle and persist the lesson. Technical reversible backpropagation is autonomous; material behavior changes require human authority.
---

# MAESTRO Backprop

Fixing code without fixing the contract or memory allows the same class of defect to return.

## Trigger

- focal, integration, security, lifecycle or CI failure;
- user-reported defect;
- reviewer finding with root cause;
- repeated dead end or oscillation;
- `maestro-check` violation or overclaim.

Ordinary expected RED from a planned TDD slice is not a defect. Backprop only when the failure teaches something not already represented by the task contract.

## Six-step protocol

### 1. TRACE

Capture the exact symptom, command, output and real seam. Locate the narrowest relevant claim, criterion, interface or missing dimension. Identify the failing path, not merely the file where the exception surfaced.

### 2. CLASSIFY

Choose one:

- `IMPLEMENTATION_BUG`: contract already correct; code violates it;
- `MISSING_CRITERION`: requirement exists but this case was not asserted;
- `INCOMPLETE_CRITERION`: criterion is too vague or partial;
- `WRONG_CRITERION`: contract asserts incorrect behavior;
- `MISSING_REQUIREMENT`: authorized mission omitted a needed behavior;
- `ENVIRONMENTAL_LIMIT`: required environment/tool unavailable;
- `EXTERNAL_DEPENDENCY`: first-party contract or service blocks progress;
- `PROCESS_GAP`: review, evidence, ownership or synchronization protocol allowed the failure.

### 3. ANALYZE ROOT CAUSE

State:

- what was wrong;
- why existing test/review did not catch it;
- class of recurrence;
- narrowest authoritative layer to change;
- whether external behavior or consequence changes.

Do not record “test failed” as root cause.

### 4. AMEND CONTRACT

For technical reversible changes, update the applicable criterion, invariant, interface, task or process autonomously through `maestro-spec`.

Escalate through `maestro-grill` only when the amendment changes product behavior, compatibility promise, privilege, cost, risk acceptance, publication or irreversibility.

### 5. RED → GREEN

Create a regression oracle at the real seam. Observe it fail before the fix. Apply the minimum fix. Observe it pass. Run the original unminimized scenario and full proportional gate cascade.

A new invariant without an executable oracle is not a completed backprop.

### 6. LOG

Append one entry to `continuity/LEARNING_LEDGER.md` containing:

- Backprop-ID, date, Round-ID and Task-ID;
- classification and pattern category;
- symptom and root cause;
- contract amendment;
- RED command/result;
- GREEN command/result;
- affected files and final task commit;
- whether broader systemic amendment is indicated.

Link the evidence index where material. Do not duplicate full logs.

## Pattern escalation

If the same pattern category recurs three times, open a dedicated process/spec task. Examples:

- input validation;
- concurrency/order;
- error handling/rollback;
- integration/interface drift;
- observability/evidence;
- secret/trust boundary;
- lifecycle preservation;
- remote synchronization.

Do not silently broaden the current fix to every module.

## Boundaries

- No bulk backprop: each failure gets an independent entry.
- No patch-first/spec-never behavior.
- No claim that a test would have caught the bug unless RED was observed.
- No use or reproduction of secrets while tracing.
- Backprop does not authorize expansion beyond the charter.

Completion means contract, regression test, implementation, evidence and durable lesson agree.