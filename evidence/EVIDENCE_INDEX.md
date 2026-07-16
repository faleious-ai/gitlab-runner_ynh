# Índice de evidências

## Estados

- `OBSERVED`: fato inspecionado, sem demonstração completa.
- `VERIFIED`: demonstrado de forma reproduzível.
- `FAILED`: critério executado/revisado e não atendido.
- `UNVERIFIED`: não demonstrado.
- `SUPERSEDED`: substituído.

## Evidências históricas

| ID | Estado | Round | Assunto | Localização | Resultado |
|---|---|---|---|---|---|
| EVD-20260716-001-RUNNER | VERIFIED | RND-20260716-001 | bootstrap MAESTRO | `AGENTS.md`, `CONTEXT.md`, `continuity/`, `docs/`, `evidence/` | estrutura criada sem mudança funcional |
| EVD-20260716-002-RUNNER | VERIFIED | RND-20260716-002 | contrato orquestrador/Codex | protocolos, ADR-0005 e especificações | rodada completa, revisão, sincronização e paralelismo persistidos |
| EVD-WP01B-INVENTORY | VERIFIED | RND-20260716-003 | inventário Runner | `docs/audit/RUNNER_PACKAGE_BASELINE.md` | manifest, assets, scripts, action, Docker e lifecycle documentados |
| EVD-WP01B-TOKEN-SECURITY | VERIFIED | RND-20260716-003 | risco credential-like | `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md` | risco localizado sem uso/reprodução do valor |
| EVD-WP01B-UPSTREAM-DIVERGENCE | VERIFIED | RND-20260716-003 | comparação upstream | `docs/audit/UPSTREAM_DIVERGENCE.md` | fork funcionalmente igual ao snapshot auditado |
| EVD-WP01B-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-004 | revisão WP-01B | `continuity/reviews/REV-RND-20260716-003.md` | verdict `ACCEPTED` |
| EVD-WP02-ORCHESTRATOR-REVIEW-005 | VERIFIED | RND-20260716-006 | revisão da fundação inicial | `continuity/reviews/REV-RND-20260716-005.md` | verdict `CORRECTION_REQUIRED` |

## Revisão de RND-20260716-007

| ID | Estado | Assunto | Resultado da revisão |
|---|---|---|---|
| EVD-WP02C-LIVE-DISCOVERY | OBSERVED | descoberta online | API paginada, stable-only, origem e `observed_at` implementados; self-link/page não confrontado |
| EVD-WP02C-CHECKSUM-TRUST | FAILED | checksum e assinatura | quatro hashes confrontados, porém falha criptográfica pode ser classificada como indisponibilidade |
| EVD-WP02C-SOURCE-BOUNDARY | OBSERVED | origem e redirects | allowlists exatas presentes; self-link e limite efetivo de redirects não demonstrados |
| EVD-WP02C-MANIFEST-CANDIDATE | VERIFIED | manifest candidato | cópia completa, nove campos allowlisted, diff determinístico e sem promoção |
| EVD-WP02C-TOKEN-NOT-IN-ARGV | OBSERVED | transporte de registro | subprocesso principal usa ambiente, mas script legado ainda aceita credencial por argumentos |
| EVD-WP02C-YUNOHOST-ACTION-CONTRACT | FAILED | config panel | botão existe, mas `scripts/config` não define `run__register()` nem entradas efêmeras |
| EVD-WP02C-LIFECYCLE-IDENTITY | FAILED | backup/restore | restore depende de senha não persistida e backup não declara preservação do config |
| EVD-WP02C-TESTS-AND-REMOTE-CI | UNVERIFIED | testes e CI | testes locais declarados; nenhum run/status remoto recuperado para o SHA |
| EVD-WP02C-CROSS-REPO-SYNTHESIS | VERIFIED | síntese | commits e estado cross-repo reconciliados |
| EVD-WP02C-ORCHESTRATOR-REVIEW | VERIFIED | revisão independente | `continuity/reviews/REV-RND-20260716-007.md`; verdict `CORRECTION_REQUIRED` |

## Evidências requeridas para CHR-WP02-003

- `EVD-WP02D-YUNOHOST-RUN-CONTROLLER`;
- `EVD-WP02D-EPHEMERAL-REGISTRATION-INPUTS`;
- `EVD-WP02D-LIFECYCLE-IDENTITY`;
- `EVD-WP02D-SIGNATURE-FAIL-CLOSED`;
- `EVD-WP02D-SELF-LINK-REDIRECTS`;
- `EVD-WP02D-CANONICAL-EVIDENCE`;
- `EVD-WP02D-LOCAL-TESTS`;
- `EVD-WP02D-REMOTE-CI`;
- `EVD-WP02D-CROSS-REPO-SYNTHESIS`;
- `EVD-WP02D-ORCHESTRATOR-REVIEW`.

## Regras

Claims devem apontar para método, entrada/commit, resultado e limitação. Fixture não é autoridade de freshness ou checksum por si só. O índice funcional canônico é este arquivo. Nunca reproduzir a credencial histórica. Aceite permanece exclusivo do orquestrador.