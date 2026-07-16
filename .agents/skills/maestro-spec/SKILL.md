---
name: maestro-spec
description: Create or amend executable task contracts, technical specifications, invariants and interfaces under MAESTRO authority. Use before implementation when scope, seam, claims, validation or ownership are incomplete, and during technical backpropagation.
---

# MAESTRO Spec

Turn intent into an executable contract without collapsing the repository's layered memory into one file.

## Authority order

1. explicit Maestro Director decision;
2. accepted ADRs and program specifications;
3. active charter;
4. technical task contract;
5. implementation.

A lower layer never silently overrides a higher one.

## Canonical destinations

- mission/program behavior: `docs/specifications/`;
- durable rationale: `docs/decisions/` and `continuity/DECISIONS.md`;
- current authorization and DAG: `continuity/ACTIVE_ROUND.md`;
- current state: `continuity/STATUS.md`;
- resume point: `continuity/HANDOFF_CURRENT.md`;
- failures/lessons: `continuity/LEARNING_LEDGER.md`;
- proof registry: `evidence/EVIDENCE_INDEX.md`;
- append-only history: `continuity/rounds/`.

Do not duplicate the same authority in multiple files. Link to the canonical source.

## Task contract

Before the first edit, every task must have:

- `Task-ID` and one observable result;
- dependencies and integration order;
- public seam;
- interfaces and invariants touched;
- claims that can be proven or explicitly marked unverified;
- paths and ownership;
- exact RED/GREEN contract for behavioral work;
- gate cascade and expected evidence level;
- review axes;
- commit message and rollback boundary.

A task that cannot fit one coherent commit is too large. Split it before coding.

## Modes

### NEW

Create the smallest contract that makes the work unambiguous. Preserve implementation freedom. Specify WHAT, observable constraints and proof; avoid prescribing HOW unless architecture or safety requires it.

### AMEND

Change only named sections or requirements. State reason, affected Task-IDs, compatibility effect and required revalidation. Technical reversible amendments are autonomous.

### BACKPROP

When a failure exposes a gap, classify it and update the narrowest authoritative layer:

- implementation bug: test and code, no spec change unless a class of recurrence exists;
- missing/incomplete/wrong criterion: amend criterion and add regression test;
- missing requirement: add requirement only if within authorized mission;
- external behavior/product consequence: stop for Maestro Director decision.

## Quality rules

- Every behavioral claim names a seam and oracle.
- Every interface states inputs, outputs, errors and relevant lifecycle ordering.
- Every security invariant has a negative case.
- Every remote claim distinguishes local, CI and lifecycle proof.
- Unknowns remain explicit; research them or mark them `UNVERIFIED`.
- Do not use Caveman compression where loss of nuance can affect security, compatibility, recovery or human choice.

## Output

Produce a focused diff, affected Task-IDs, rationale, new/changed validation, compatibility impact and whether human authority is required. Do not implement code in this skill.