---
name: maestro-grill
description: Resolve only material human decisions before a charter or task is authorized. Ask one question at a time, provide a recommendation and consequences, and never outsource reversible technical choices to the Maestro Director.
---

# MAESTRO Grill

Use the user's attention only where human authority changes the result.

## Trigger

Run when an unresolved choice affects one or more of:

- mission or product behavior;
- compatibility promise;
- security posture or accepted risk;
- privilege, credentials or production access;
- cost, licensing or recurring resource use;
- publication, deletion, migration or irreversibility;
- ethical or practical consequence.

Do not run for reversible implementation choices, naming, library mechanics or ordinary debugging. The orchestrator decides those and records rationale.

## Calibration

Infer domain familiarity, how fixed the decision is and desired pressure from context. Do not start with a questionnaire.

## Question protocol

Ask one question at a time. Each question contains:

1. the exact decision;
2. why it changes the outcome;
3. a recommended option;
4. concise alternatives;
5. consequences, reversibility and required access;
6. a direct choice format.

Example shape:

> Decisão: manter compatibilidade com configuração antiga ou migrar estritamente?  
> Recomendação: compatibilidade por uma versão, porque reduz risco de restore.  
> A: compatibilidade temporária — mais código, rollback simples.  
> B: migração estrita — menos código, quebra instalações antigas.  
> Escolha A/B.

## Ladder

Climb only until the charter is materially unambiguous:

1. desired practical outcome;
2. observable definition of done;
3. explicit out-of-scope boundary;
4. compatibility and migration consequence;
5. security/privilege/cost boundary;
6. irreversible action and rollback;
7. unknown that only the human can resolve.

Stop as soon as remaining unknowns are technical and reversible.

## Unknown routing

- external factual unknown → `maestro-research`;
- technical design trade-off → orchestrator decides and records;
- missing testability → `maestro-spec`;
- material human consequence → continue one-question protocol.

## Output

Produce a decision record containing question, recommendation, selected option, rejected alternatives, consequences and affected charter/tasks. Do not implement or silently infer an answer. Do not ask multiple unrelated questions in one turn.