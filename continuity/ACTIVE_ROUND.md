# Rodada ativa

Charter-ID: `CHR-GOV-AUTONOMY-001`  
Estado: `EXECUTED_AWAITING_REVIEW`
Preparado em: 2026-07-17  
Executor principal: Codex  
Unidade: `adoção Runner da fila técnica contínua`

## Contrato canônico

O charter detalhado está no coordenador `faleious-ai/gitlab_ynh/continuity/ACTIVE_ROUND.md`, commit `e6e0a4c201cdfc1106fa0c060b502c7bc0a5135a`.

Baseline deste Runner: `17be5e890010c2eb96d857713f2bc0164092b943`. Resolver novamente `origin/master` no START.

## Tarefas Runner

### `T-RUN-01-supported-docker-default`

- Executar `tests.acceptance.test_supported_docker_default`.
- Preservar o oracle do Orquestrador.
- Selecionar tag patch Alpine ainda suportada e observada no registry oficial.
- Manter `manifest.toml` e `config_panel.toml` coerentes.
- Não usar `latest` ou `edge`.
- RED atual: `alpine:3.20` não é patch exata e a série encerrou suporte antes da observação.

### `T-RUN-02-observability`

- Diagnosticar a falha de fetch de `release.sha256` por estágio e rota oficial.
- Reexecutar observação live somente com código funcional já publicado.
- Tentar mecanismo read-only adequado para observar CI por SHA.
- Preservar `UNVERIFIED` quando o resultado não for observado.

### `T-RUN-03-process-adoption`

Depende de `T-GOV-01-program-engine` no coordenador.

- Integrar mandato, fila, lanes e gate estrito em `AGENTS.md`, protocolos e arquitetura Runner.
- Manter commits por tarefa e `master` linear.
- Fazer bloqueio parcial liberar tarefas independentes.
- Proteger o acceptance test do Orquestrador contra alteração silenciosa.

## Paralelismo

T-RUN-01 e T-RUN-02 são independentes e devem ser preparados em lanes sobrepostas, com paths exclusivos. O Executor principal integra, testa, publica e verifica uma tarefa por vez.

Registrar `Lane-ID`, baseline, ownership, `started_at`, `ready_at`, RED/GREEN, output e confirmação de ausência de commit pelo subagente.

## Limites

- nenhuma promoção de versão Runner;
- nenhum registro real ou alteração de ambiente real;
- nenhuma alteração retrospectiva da matriz upstream;
- sem branch, PR, worktree, squash ou force push;
- o Executor não declara `ACCEPTED`.

## Fechamento

Todos os trabalhos Runner não bloqueados de `RND-20260717-015` foram executados e publicados. Entregar ao Orquestrador os acceptance results, a matriz task→commit→claim→evidência e os HEADs remotos coincidentes. Estado: `EXECUTED_AWAITING_REVIEW`; o Executor não escreve `ACCEPTED`.

Após a adoção do motor, continuar pelas tarefas elegíveis da fila canônica do programa. Entregar commits por tarefa, acceptance results, lanes demonstradas, claims limitados e estado remoto retomável.
