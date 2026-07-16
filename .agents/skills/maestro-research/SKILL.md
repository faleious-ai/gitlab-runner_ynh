---
name: maestro-research
description: Resolve external technical unknowns using primary sources, explicit freshness and durable findings. Use when a task depends on current YunoHost, GitLab, GitLab Runner, API, security or packaging facts not proven by the repository.
---

# MAESTRO Research

Research is an evidence-producing task, not background prose.

## Scope

Turn the unknown into one to three falsifiable questions. State what decision or invariant each answer will affect. Do not research broadly when a narrow fact is sufficient.

## Source order

1. repository code, tests and current artifacts;
2. official specification or protocol;
3. official product documentation;
4. first-party source repository, release metadata or API;
5. primary research paper;
6. secondary source only when no primary source exists, marked accordingly.

For changing facts, record observation date, version/tag/commit and relevant edition. Local code remains authority for what this package currently does; web sources establish external contracts, not local behavior.

## Gather

- Use parallel subagents for independent questions when useful; each returns only distilled findings and sources.
- Follow a claim to the source that owns it.
- Use two independent authoritative sources when a high-risk claim has ambiguity.
- Capture exact identifiers, versions, URLs, deprecation status and limitations.
- Do not dump raw pages into project memory.

## Classify findings

- `VERIFIED_PRIMARY`: directly supported by current primary source;
- `CORROBORATED`: supported by multiple authoritative sources;
- `CONFLICTING`: authoritative sources disagree;
- `UNVERIFIED`: source unavailable or insufficient;
- `STALE_RISK`: source may no longer describe current behavior.

No source means no factual claim. Preserve an explicit unknown instead of filling it with a plausible answer.

## Distill

Each durable finding contains:

- question/ID;
- concise finding;
- source URL or repository path;
- version/date/commit;
- confidence class;
- affected requirement, invariant or task;
- limitation or unresolved conflict.

Store findings where the repository already keeps research or ADR rationale. Link from the task contract; do not duplicate full content into status or handoff.

## Decision handling

- If research resolves a reversible technical choice, the orchestrator or executor may decide and document it.
- If sources conflict on a material consequence, present alternatives to the Maestro Director through `maestro-grill`.
- If a finding invalidates the charter, use `maestro-spec` before implementation.

## Completion

Research is complete when every scoped question has a sourced answer or an honest unknown, and no build decision rests on an unchecked external assumption. Report sources consulted, rejected sources and why the result is sufficient for the task.