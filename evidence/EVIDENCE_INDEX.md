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

## Revisão de RND-20260716-005

| ID | Estado | Assunto | Resultado da revisão |
|---|---|---|---|
| EVD-WP02-SECRET-REMEDIATION | VERIFIED | fixture, scanner e redaction | literal removido; scanner e redaction presentes/testados |
| EVD-WP02-REGISTER-ACTION | OBSERVED | action e registro compartilhado | target/helper/cardinalidade confirmados; contrato YunoHost e token fora de argv não demonstrados |
| EVD-WP02-RELEASE-PROVENANCE | FAILED | fonte/checksum/freshness | fixture confia em hashes fornecidos; checksum oficial e descoberta corrente não integrados |
| EVD-WP02-ATOMIC-RESOLVER | OBSERVED | matriz Runner/helper | matriz e falhas estruturais confirmadas, mas sem hash com cadeia de confiança |
| EVD-WP02-GENERATOR-TESTS | FAILED | generator/diff | produz TOML auxiliar, não cópia/diff do manifest real |
| EVD-WP02-CI-AND-REDACTION | UNVERIFIED | CI remoto | testes locais declarados; nenhum check/status remoto recuperado; actions por tags mutáveis |
| EVD-WP02-ORCHESTRATOR-REVIEW | VERIFIED | revisão independente | `continuity/reviews/REV-RND-20260716-005.md`; verdict `CORRECTION_REQUIRED` |

## Evidências requeridas para CHR-WP02-002

- `EVD-WP02C-LIVE-DISCOVERY`;
- `EVD-WP02C-CHECKSUM-TRUST`;
- `EVD-WP02C-SOURCE-BOUNDARY`;
- `EVD-WP02C-MANIFEST-CANDIDATE`;
- `EVD-WP02C-TOKEN-NOT-IN-ARGV`;
- `EVD-WP02C-YUNOHOST-ACTION-CONTRACT`;
- `EVD-WP02C-TESTS-AND-REMOTE-CI`;
- `EVD-WP02C-CROSS-REPO-SYNTHESIS`;
- `EVD-WP02C-ORCHESTRATOR-REVIEW`.

## Regras

Claims devem apontar para método, entrada/commit, resultado e limitação. Fixture não é autoridade de checksum ou freshness por si só. Nunca reproduzir a credencial histórica. Aceite permanece exclusivo do orquestrador.
