---
name: maestro-caveman
description: Compress machine-oriented matrices, ledgers and handoffs without losing facts. Never use compression where ambiguity can affect security, human choice, recovery, compatibility or destructive operations.
---

# MAESTRO Caveman

Compression reduces context cost; it never outranks precision.

## Allowed

Use compact fragments, tables and symbols in:

- task/claim matrices;
- convergence snapshots;
- backprop ledgers;
- file ownership maps;
- repetitive validation summaries;
- machine-oriented handoff sections whose vocabulary is already defined.

## Forbidden

Use complete language for:

- human gates and recommendations;
- security findings and threat models;
- ADRs and architectural rationale;
- recovery, rollback and destructive procedures;
- compatibility and migration consequences;
- legal/licensing notices;
- public user documentation;
- error messages, commands and evidence excerpts.

## Grammar

Fragments are allowed when the relation remains unambiguous. Remove filler and repeated prose, not conditions or qualifiers.

Permitted symbols:

- `→` transition/result;
- `∀` every;
- `∃` exists;
- `!` required;
- `?` unknown/optional only when context defines which;
- `⊥` forbidden/impossible;
- `≠`, `≤`, `≥` mathematical relation;
- `&`, `|` logical conjunction/disjunction;
- `§` section reference.

Do not substitute symbols when a human reader could reasonably interpret them differently.

## Preserve verbatim

Never compress or alter:

- code, shell commands and paths;
- identifiers, env vars and function names;
- URLs, versions, hashes, Task-IDs and SHAs;
- error strings and log excerpts;
- JSON, TOML, YAML, SQL and regex;
- quoted requirements or source text;
- dates, counts and thresholds.

## Shapes

Claim row:

`C3|LOCAL_VERIFIED|config button → run__register|pytest ...|pass|lifecycle ?`

Backprop row:

`B4|MISSING_CRITERION|restore re-registers|∴ V12 + regression test`

Task row:

`T-07|DONE|self-link validation|deps:T-05|commit:<sha>`

## Quality gate

Before saving compressed text, ask:

1. Did any condition, exception, evidence level or consequence disappear?
2. Can a new agent act correctly without reconstructing prose from chat?
3. Could a human misunderstand risk or authorization?

If yes, expand. Compression is rejected whenever cutting a word cuts a fact.