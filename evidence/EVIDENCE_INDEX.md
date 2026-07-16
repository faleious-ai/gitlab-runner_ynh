# Índice de evidências

## Estados

- `OBSERVED`: inspecionado, ainda sem teste completo.
- `VERIFIED`: demonstrado de forma reproduzível.
- `FAILED`: check executado e falhou.
- `UNVERIFIED`: não demonstrado.
- `SUPERSEDED`: substituído.

## Entradas

| ID | Estado | Round | Assunto | Localização | Resultado |
|---|---|---|---|---|---|
| EVD-20260716-001-RUNNER | VERIFIED | RND-20260716-001 | bootstrap MAESTRO | `AGENTS.md`, `CONTEXT.md`, `continuity/`, `docs/`, `evidence/` | estrutura criada sem mudança funcional |
| EVD-RUNNER-BASELINE-001 | OBSERVED | pre-bootstrap | versão e sources | `manifest.toml` | `18.6.2~ynh1`, auditoria detalhada pendente |
| EVD-RUNNER-BASELINE-002 | OBSERVED | pre-bootstrap | autoupdate | `manifest.toml` | bloco principal comentado; helper sem estratégia automática observada |

## Próximas evidências

- `EVD-WP01B-INVENTORY`;
- `EVD-WP01B-LIFECYCLE`;
- `EVD-WP01B-TOKEN-SECURITY`;
- `EVD-WP01B-EXECUTOR-HELPERS`;
- `EVD-WP01B-UPSTREAM-DIVERGENCE`;
- `EVD-WP01B-ASSURANCE-GAPS`.

## Regras

Registrar método/comando, ambiente, commit de entrada, resultado, limitações e risco residual. Redigir qualquer segredo antes de persistir.