# Índice de evidências

## Estados

- `OBSERVED`: inspecionado, sem teste completo.
- `VERIFIED`: demonstrado de forma reproduzível.
- `FAILED`: check falhou.
- `UNVERIFIED`: não demonstrado.
- `SUPERSEDED`: substituído.

## Entradas

| ID | Estado | Round | Assunto | Localização | Resultado |
|---|---|---|---|---|---|
| EVD-20260716-001-RUNNER | VERIFIED | RND-20260716-001 | bootstrap MAESTRO | `AGENTS.md`, `CONTEXT.md`, `continuity/`, `docs/`, `evidence/` | estrutura criada sem mudança funcional |
| EVD-20260716-002-RUNNER | VERIFIED | RND-20260716-002 | contrato orquestrador/Codex | `AGENTS.md`, `ACTIVE_ROUND.md`, protocolos, ADR-0005 e especificações | rodada completa, revisão e paralelismo persistidos; sem mudança funcional |
| EVD-RUNNER-BASELINE-001 | OBSERVED | pre-bootstrap | versão/sources | `manifest.toml` | `18.6.2~ynh1` |
| EVD-RUNNER-BASELINE-002 | OBSERVED | pre-bootstrap | autoupdate | `manifest.toml` | bloco comentado/helper sem estratégia observada |
| EVD-WP01B-INVENTORY | VERIFIED | RND-20260716-003 | inventário Runner | `docs/audit/RUNNER_PACKAGE_BASELINE.md` | manifest, assets, scripts, action, Docker e lifecycle documentados |
| EVD-WP01B-TOKEN-SECURITY | VERIFIED | RND-20260716-003 | tokens e redaction | `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md` | credential-like literal localizado sem reproduzir o valor; fluxo e riscos documentados |
| EVD-WP01B-UPSTREAM-DIVERGENCE | VERIFIED | RND-20260716-003 | comparação upstream | `docs/audit/UPSTREAM_DIVERGENCE.md` | fork funcionalmente igual ao snapshot YunoHost-Apps |
| EVD-WP01B-ASSURANCE-GAPS | VERIFIED | RND-20260716-003 | autoupdate, Docker e lifecycle | `docs/audit/AUTOUPDATE_GAPS.md`, `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md` | gaps e critérios de aceite derivados |
| EVD-WP01B-ORCHESTRATOR-REVIEW | VERIFIED | RND-20260716-004 | revisão independente WP-01B | `continuity/reviews/REV-RND-20260716-003.md` | outputs e commit conferidos; achados críticos reproduzidos; verdict `ACCEPTED` |

## Evidências requeridas para CHR-WP02-001

- `EVD-WP02-SECRET-REMEDIATION`;
- `EVD-WP02-REGISTER-ACTION`;
- `EVD-WP02-RELEASE-PROVENANCE`;
- `EVD-WP02-ATOMIC-RESOLVER`;
- `EVD-WP02-GENERATOR-TESTS`;
- `EVD-WP02-CI-AND-REDACTION`;
- `EVD-WP02-ORCHESTRATOR-REVIEW`.

## Evidências produzidas por RND-20260716-005

| ID | Estado | Round | Assunto | Localização | Resultado |
|---|---|---|---|---|---|
| EVD-WP02-SECRET-REMEDIATION | VERIFIED | RND-20260716-005 | fixture, secret scan e redaction | `tests.toml`, `scripts/secret_scan.py`, `scripts/_register.sh`, `tests/test_autoupdate.py` | literal removido; scan e redaction testados sem token real |
| EVD-WP02-REGISTER-ACTION | VERIFIED | RND-20260716-005 | action e registro compartilhado | `actions.json`, `scripts/actions/register`, `scripts/_register.sh`, `scripts/install`, `scripts/restore` | target existente; cardinalidade fail-closed e fluxo compartilhado testados |
| EVD-WP02-RELEASE-PROVENANCE | VERIFIED | RND-20260716-005 | fonte e fixture offline | `docs/decisions/ADR-0006-runner-release-provenance.md`, `scripts/autoupdate/fixtures/release-v19.0.1.json` | API/S3 oficiais, stable-only e conjunto versionado documentados |
| EVD-WP02-ATOMIC-RESOLVER | VERIFIED | RND-20260716-005 | Runner/helper resolver | `scripts/autoupdate.py`, `tests/test_autoupdate.py` | amd64/arm64/armhf + helper same-version; falhas fechadas cobertas |
| EVD-WP02-GENERATOR-TESTS | VERIFIED | RND-20260716-005 | dry-run, determinismo e atomicidade | `scripts/autoupdate.py`, `evidence/wp02-candidate-report.json` | candidata `v19.0.1` observada sem promoção; escrita explícita e idempotente |
| EVD-WP02-CI-AND-REDACTION | VERIFIED | RND-20260716-005 | CI read-only e assurance | `.github/workflows/validation.yml`, `tests/test_autoupdate.py` | suíte local passou; CI não cria branch/PR/commit |

## Regras

Registrar método/comando, ambiente, commit, resultado, limitações e risco residual. Redigir segredos e nunca reproduzir o valor histórico. O trabalho do Codex só recebe aceite após revisão independente.
