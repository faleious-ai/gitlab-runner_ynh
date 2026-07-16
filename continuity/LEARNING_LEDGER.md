# Learning ledger

Append-only registry for failures, dead ends and process lessons that must survive context resets. This file complements, but does not duplicate, `STATUS`, `HANDOFF_CURRENT`, round records or the evidence index.

## Entry schema

| Field | Required content |
|---|---|
| Backprop-ID | `BP-YYYYMMDD-NNN` |
| Round/Task | source `Round-ID` and `Task-ID` |
| classification | implementation bug, criterion gap, requirement gap, environment, dependency or process gap |
| pattern | stable category used to detect recurrence |
| symptom | exact observed failure, without secrets |
| root cause | technical cause, not merely failed command |
| contract change | criterion/invariant/interface/process amendment, or `none` with reason |
| RED | command/oracle and observed failing result |
| GREEN | command/oracle and observed passing result |
| commit | final task SHA when available |
| systemic action | none, candidate task or required human decision |

## Entries

No backprop entries recorded under the new protocol yet.

## Rules

- Never delete entries. Corrections append a superseding note.
- Never reproduce credentials, tokens or sensitive payloads.
- One unexpected failure produces one entry; do not bulk unrelated failures.
- Expected RED in a planned TDD slice is not logged unless it exposes an unmodeled gap.
- Three entries in the same pattern category require a dedicated systemic task proposal.
- Link large logs/evidence rather than copying them here.
- `STATUS` records current state; this ledger records why a failed approach must not be repeated.
