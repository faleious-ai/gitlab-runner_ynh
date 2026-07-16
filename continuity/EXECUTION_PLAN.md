# Plano de execução local

A sequência de longo prazo está aqui; a autorização concreta pertence a `continuity/ACTIVE_ROUND.md`.

## Política

- ChatGPT prepara/revisa rodadas completas após perguntas humanas necessárias.
- Codex executa todo charter `READY` e não para enquanto houver trabalho não bloqueado.
- Usar DAG e subagentes em frentes independentes; Codex integra.
- `master` exclusiva, sem branches/PRs/worktrees.
- Um commit normativo por rodada futura; mesmo `Round-ID` cross-repo.
- Implementação somente após baseline aceito pelo orquestrador.

## WP-00 — Bootstrap MAESTRO

Status: `DONE`.

## WP-00B — Contrato orquestrador-executor

Status: `DONE`.

## WP-01B — Auditoria baseline Runner

Status: `ACTIVE_CHARTER_READY`.

Charter: `CHR-WP01-001`.

Saídas:

1. inventário estrutural/lifecycle;
2. matriz versão × arquitetura × assets;
3. Runner/helper images;
4. tokens/redaction;
5. Docker/executor;
6. testes/workflows;
7. upstream/divergência;
8. lacunas e backlog.

Critério de saída: fatos por path/commit, desconhecidos explícitos, nenhuma implementação misturada, commits/evidências persistidos e revisão do orquestrador.

## WP-02A — Fonte de verdade de release

Status: `PLANNED`; depende de WP-01B `ACCEPTED`.

## WP-02B — Resolver atômico Runner/helper images

Status: `PLANNED`.

## WP-02C — Gerador determinístico

Status: `PLANNED`.

## WP-02D — Testes unitários e negativos

Status: `PLANNED`.

## WP-02E — Lifecycle

Status: `PLANNED`.

## WP-02F — Automação recorrente

Status: `PLANNED`.

## WP-09 — Manutenção contínua

Status: `PLANNED`.

Monitorar drift, compatibilidade, YunoHost/Debian, tokens/executor e releases.
