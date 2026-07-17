# Índice de evidências

## Estados

- `STRUCTURALLY_OBSERVED`: forma/presença inspecionada, sem execução comportamental.
- `LOCAL_VERIFIED`: demonstrado localmente em seam adequado.
- `REMOTE_CI_VERIFIED`: run remoto associado ao SHA confirmado.
- `LIFECYCLE_VERIFIED`: lifecycle proporcional executado.
- `FAILED`: critério executado/revisado e não atendido.
- `UNVERIFIED`: não demonstrado.
- `SUPERSEDED`: substituído.

## Evidências históricas

| ID | Estado | Round | Assunto | Localização | Resultado |
|---|---|---|---|---|---|
| EVD-20260716-001-RUNNER | LOCAL_VERIFIED | RND-20260716-001 | bootstrap MAESTRO | `AGENTS.md`, `CONTEXT.md`, `continuity/`, `docs/`, `evidence/` | estrutura criada sem mudança funcional |
| EVD-20260716-002-RUNNER | LOCAL_VERIFIED | RND-20260716-002 | contrato orquestrador/Codex | protocolos, ADR-0005 e especificações | rodada, revisão e sincronização persistidas |
| EVD-WP01B-INVENTORY | LOCAL_VERIFIED | RND-20260716-003 | inventário Runner | `docs/audit/RUNNER_PACKAGE_BASELINE.md` | manifest, assets, scripts, action, Docker e lifecycle documentados |
| EVD-WP01B-TOKEN-SECURITY | LOCAL_VERIFIED | RND-20260716-003 | risco credential-like | `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md` | risco localizado sem uso/reprodução do valor |
| EVD-WP01B-UPSTREAM-DIVERGENCE | LOCAL_VERIFIED | RND-20260716-003 | comparação upstream | `docs/audit/UPSTREAM_DIVERGENCE.md` | fork igual ao snapshot auditado |
| EVD-WP01B-ORCHESTRATOR-REVIEW | LOCAL_VERIFIED | RND-20260716-004 | revisão WP-01B | `continuity/reviews/REV-RND-20260716-003.md` | verdict `ACCEPTED` |
| EVD-WP02-ORCHESTRATOR-REVIEW-005 | LOCAL_VERIFIED | RND-20260716-006 | revisão fundação WP-02 | `continuity/reviews/REV-RND-20260716-005.md` | verdict `CORRECTION_REQUIRED` |

## Revisão de RND-20260716-007

| ID | Estado | Assunto | Resultado da revisão |
|---|---|---|---|
| EVD-WP02C-LIVE-DISCOVERY | STRUCTURALLY_OBSERVED | descoberta online | API paginada, stable-only e origem implementados; self-link/page incompletos |
| EVD-WP02C-CHECKSUM-TRUST | FAILED | checksum e assinatura | hashes confrontados, porém falha criptográfica pode ser classificada como indisponibilidade |
| EVD-WP02C-SOURCE-BOUNDARY | STRUCTURALLY_OBSERVED | origem e redirects | allowlists presentes; self-link e limite efetivo não demonstrados |
| EVD-WP02C-MANIFEST-CANDIDATE | LOCAL_VERIFIED | manifest candidato | cópia completa, nove campos allowlisted, diff determinístico e sem promoção |
| EVD-WP02C-TOKEN-NOT-IN-ARGV | STRUCTURALLY_OBSERVED | transporte de registro | subprocesso principal usa ambiente, mas interface legada permanece |
| EVD-WP02C-YUNOHOST-ACTION-CONTRACT | FAILED | config panel | botão sem controlador real/inputs efêmeros |
| EVD-WP02C-LIFECYCLE-IDENTITY | FAILED | backup/restore | identidade não preservada; restore depende de senha não persistida |
| EVD-WP02C-TESTS-AND-REMOTE-CI | UNVERIFIED | testes e CI | testes locais declarados; nenhum run/status remoto recuperado |
| EVD-WP02C-CROSS-REPO-SYNTHESIS | LOCAL_VERIFIED | síntese | commits e estado reconciliados |
| EVD-WP02C-ORCHESTRATOR-REVIEW | LOCAL_VERIFIED | revisão independente | `continuity/reviews/REV-RND-20260716-007.md`; `CORRECTION_REQUIRED` |

## Evidências de RND-20260716-009 — processo

| ID | Estado | Task | Assunto | Resultado |
|---|---|---|---|---|
| EVD-PROC-ADR006 | LOCAL_VERIFIED | T-01 | política de commits por tarefa e decisões D1–D5 | ADR, AGENTS e protocolos publicados nos dois repositórios |
| EVD-PROC-CAVEKIT-RESEARCH | LOCAL_VERIFIED | T-02 | leitura/adaptação Cavekit | relatório no coordenador; índice e licença no Runner |
| EVD-PROC-SKILL-SUITE | STRUCTURALLY_OBSERVED | T-03..T-14 | 12 skills MAESTRO | arquivos publicados individualmente; eficácia testada em RND-20260716-010 e retropropagada em RND-20260717-011 |
| EVD-PROC-LEARNING-LEDGER | LOCAL_VERIFIED | T-15 | memória de backprop/dead ends | schema append-only publicado |
| EVD-PROC-ARCHITECTURE | LOCAL_VERIFIED | T-16 | máquina de estados e papéis | tarefa/commit/TDD/review/backprop integrados à arquitetura |
| EVD-PROC-CHR003-MIGRATION | LOCAL_VERIFIED | T-17 | charter executável | oito Task-IDs com seams, RED/GREEN, gates e dependências |

## Evidências de CHR-WP02-003 — RND-20260716-010

| ID | Estado | Task/round | Seam e localização | Commit remoto ou limitação |
|---|---|---|---|---|
| EVD-WP02D-YUNOHOST-RUN-CONTROLLER | LOCAL_VERIFIED | T-WP02D-01 / RND-20260716-010 | `config_panel.toml`, `scripts/config`, `tests/test_config_controller.py`; RED/GREEN no round record | `ada6b78ca4db00c1dcacda4eb01736f123f6040b`; sem host YunoHost real |
| EVD-WP02D-EPHEMERAL-REGISTRATION-INPUTS | LOCAL_VERIFIED | T-WP02D-01 / RND-20260716-010 | inputs `password`/`url` com `bind = "null"`; harness sem segredo persistido | `ada6b78ca4db00c1dcacda4eb01736f123f6040b`; token real não usado |
| EVD-WP02D-NO-LEGACY-ARGV | LOCAL_VERIFIED | T-WP02D-02 / RND-20260716-010 | `tests/test_legacy_register_removed.py`, controlador seguro e suíte | `79fb763c6c2d20f9bb1b76e42a266da1b41e8ad9`; referências históricas permanecem documentais |
| EVD-WP02D-LIFECYCLE-IDENTITY | LOCAL_VERIFIED | T-WP02D-03 / RND-20260716-010 | harness temporário backup→restore | `2f0185cbf8b630f94d9618c9d7afe56cabc434b3`; sem host YunoHost/Docker |
| EVD-WP02D-SIGNATURE-FAIL-CLOSED | LOCAL_VERIFIED | T-WP02D-04 / RND-20260716-010 | adaptador GPG/GPGV falso; refresh bloqueado sem confiança | `35e8e44dd9fb39b47ad71e6dfb06e854c0029618`; lógica local preservada, transport live falha na revisão integrada |
| EVD-WP02D-SELF-LINK-REDIRECTS | LOCAL_VERIFIED | T-WP02D-05 / RND-20260716-010 | API/HTTP falsos; self-link e paths de release/download | `51dbb98a7e6de477c4f3234b1c7d40b4ac1a54ac`; redirect da chave oficial não coberto |
| EVD-WP02D-CANONICAL-EVIDENCE | FAILED | T-WP02D-06 / RND-20260716-010 | scanner de portabilidade e artefatos JSON | `2acc1a3ec1a6c42a81eacea02f7ae093131070de`; campo factual live foi acrescentado sem nova observação |
| EVD-WP02D-LOCAL-TESTS | LOCAL_VERIFIED | T-WP02D-01..07 / RND-20260716-010 | 32 testes, scanner, parsers, Bash e dry-run | nível local somente |
| EVD-WP02D-REMOTE-CI | UNVERIFIED | T-WP02D-07 / RND-20260716-010 | workflow read-only e actions fixadas | nenhum run/status remoto recuperado; não promover |
| EVD-WP02D-CROSS-REPO-SYNTHESIS | FAILED | T-WP02D-08 / RND-20260716-010 | continuidade cross-repo | commits existem, porém handoff/index mantiveram referências pré-T08 |
| EVD-WP02D-ORCHESTRATOR-REVIEW | LOCAL_VERIFIED | RND-20260717-011 | `continuity/reviews/REV-RND-20260716-010.md` | verdict `CORRECTION_REQUIRED`; Runner review commit `dd24f407e8bfcfe84b8b8ed95cfcabc7004a4463` |

## Findings da revisão RND-20260717-011

| ID | Estado | Finding | Evidência | Próxima tarefa |
|---|---|---|---|---|
| EVD-WP02E-KEY-TRANSPORT | LOCAL_VERIFIED | cadeia capturada aceita somente o par CloudFront host/path observado; adversários continuam fail-closed | T01 `6fb500ec3474c07137fcb8962512ed0adc59a9bb`; sem claim live | `T-WP02E-01` |
| EVD-WP02E-LIVE-TRUST | UNVERIFIED | nova execução live falhou no fetch de `release.sha256` antes da chave/GPG | `evidence/wp02e-live-trust-observation.json`; sem promoção de confiança | `T-WP02E-02` |
| EVD-WP02E-HISTORICAL-PROVENANCE | LOCAL_VERIFIED | payloads históricos restaurados byte a byte ao estado pré-T06; observação antiga marcada `SUPERSEDED`; T02 é a única fonte live atual | SHA-256 fixado no teste de provenance; `evidence/wp02e-live-trust-observation.json`; este task commit | `T-WP02E-03` |
| EVD-WP02E-DOCKER-DEFAULT | FAILED | panel `alpine:latest` diverge do install `alpine:3.20` sem rationale | config/manifest | `T-WP02E-04` |
| EVD-WP02E-FINAL-CONTINUITY | FAILED | future/pending e pre-T08 heads no estado final | handoff/index RND-20260716-010 | `T-WP02E-07` |
| EVD-WP02E-PROCESS-BACKPROP | LOCAL_VERIFIED | imutabilidade de evidência e transport seam incorporados | `.agents/skills/`, `REVIEW_PROTOCOL`, `LEARNING_LEDGER` | commit `4cefe926732c95344c3d7d129aa9dbe110dcae72` |

## Evidências requeridas para CHR-WP02-004

- `EVD-WP02E-KEY-TRANSPORT`;
- `EVD-WP02E-LIVE-TRUST`;
- `EVD-WP02E-HISTORICAL-PROVENANCE`;
- `EVD-WP02E-DOCKER-DEFAULT`;
- `EVD-WP02E-REMOTE-CI`;
- `EVD-WP02E-INTEGRATION`;
- `EVD-WP02E-FINAL-CONTINUITY`;
- `EVD-WP02E-ORCHESTRATOR-REVIEW`.

## Regras

Claims apontam para Task-ID, seam, método, comando, resultado, SHA e limitação. Fixture não é autoridade de freshness ou checksum por si só. Busca textual é somente estrutural. Artefato observado é semanticamente imutável; nova factualidade exige nova observação e novo artefato. O índice funcional canônico é este arquivo. Nunca reproduzir a credencial histórica. Aceite permanece exclusivo do orquestrador.
