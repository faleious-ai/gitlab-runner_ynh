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
| EVD-RUNNER-BASELINE-001 | OBSERVED | pre-bootstrap | versão/sources | `manifest.toml` | `18.6.2~ynh1`; auditoria pendente |
| EVD-RUNNER-BASELINE-002 | OBSERVED | pre-bootstrap | autoupdate | `manifest.toml` | bloco comentado/helper sem estratégia observada |
| EVD-WP01B-INVENTORY | VERIFIED | RND-20260716-003 | inventário Runner | `docs/audit/RUNNER_PACKAGE_BASELINE.md` | manifest, assets, scripts, ação, Docker e lifecycle documentados |
| EVD-WP01B-TOKEN-SECURITY | VERIFIED | RND-20260716-003 | tokens e redaction | `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md` | fixture credential-like localizado sem reproduzir o valor; fluxo de registro e riscos documentados |
| EVD-WP01B-UPSTREAM-DIVERGENCE | VERIFIED | RND-20260716-003 | comparação upstream | `docs/audit/UPSTREAM_DIVERGENCE.md` | fork funcionalmente igual ao snapshot YunoHost-Apps |
| EVD-WP01B-ASSURANCE-GAPS | VERIFIED | RND-20260716-003 | autoupdate, Docker e lifecycle | `docs/audit/AUTOUPDATE_GAPS.md`, `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md` | gaps e critérios de aceite derivados |

## Verificação de EVD-20260716-002-RUNNER

- invocação mínima e papéis no `AGENTS.md`;
- charter completo/DAG em `ACTIVE_ROUND.md`;
- execução até conclusão/bloqueio no `ROUND_PROTOCOL.md`;
- revisão independente no `REVIEW_PROTOCOL.md`;
- ownership de subagentes em `PARALLEL_EXECUTION_POLICY.md`;
- nenhum arquivo funcional do pacote alterado.

## Evidências ainda requeridas

- `EVD-WP01B-ORCHESTRATOR-REVIEW`.

## Regras

Registrar método/comando, ambiente, commit, resultado, limitações e risco residual. Redigir segredos. O trabalho do Codex só recebe aceite após revisão do orquestrador.
