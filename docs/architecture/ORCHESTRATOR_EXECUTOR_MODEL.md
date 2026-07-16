# Modelo de orquestração e execução

## Papéis

- **Maestro Diretor humano:** decide missão, prioridade, consequências práticas, gates éticos, custos relevantes, acesso privilegiado e operações irreversíveis.
- **ChatGPT — orquestrador e revisor externo:** reconcilia o remoto, resolve perguntas materiais, especifica a rodada e suas tarefas, revisa cada commit e o intervalo integrado e define aceite, correção ou gate humano.
- **Codex — executor principal:** executa integralmente o charter `READY`, coordena subagentes, integra, valida, cria um commit por tarefa, publica e prepara evidência. Não aprova o próprio resultado.
- **Subagentes:** trabalham em frentes independentes, sem autoridade de commit, push, integração final, edição concorrente de paths ou expansão de escopo.
- **Revisores internos:** contextos/subagentes separados para os eixos Spec/Charter e Engineering/Security/Lifecycle antes de cada commit.

## Unidades

- **Rodada:** autorização, baseline, escopo, DAG, gates e veredito.
- **Tarefa:** resultado atômico, seam, claims, TDD, commit, sincronização e rollback.
- **Commit:** versão remota e reversível da tarefa.
- **Evidence item:** prova de claim em nível estrutural, local, CI ou lifecycle.

## Invocação

`Leia AGENTS.md e continue` significa executar todo o charter ativo, tarefa por tarefa, e só parar após concluir tudo que não estiver bloqueado por decisão humana real ou interrupção ambiental persistida.

## Fluxo

```text
Maestro Diretor
  → ChatGPT/orquestrador
  → charter READY + Task-IDs
  → Codex/subagentes
  → RED/GREEN + gates + revisão interna
  → commit remoto por tarefa
  → pacote baseline...round_head
  → ChatGPT/revisor externo
  → ACCEPTED | CORRECTION_REQUIRED | HUMAN_GATE | REJECTED_UNSAFE
```

## Autonomia

O Codex e o orquestrador decidem autonomamente escolhas técnicas reversíveis e backprop técnico. O humano é acionado somente quando uma escolha altera missão, produto, compatibilidade prometida, custo relevante, risco aceito, privilégio, publicação ou irreversibilidade.

## Revisão

A autoria não valida a própria conclusão. O executor realiza checks e revisão interna, mas termina em `EXECUTED_AWAITING_REVIEW`. O ChatGPT revisa material remoto, cada Task-ID e o resultado integrado. Claims sem prova permanecem unverified.

## Bloqueio

Ao encontrar gate humano, o executor conclui primeiro tarefas independentes, publica tudo que for seguro e registra condição, tentativas, alternativas, decisão exata e grafo restante. Falha de push é `TASK_REMOTE_SYNC_BLOCKED`, não gate de produto.

## Autoridade local

Este repositório mantém autoridade sobre Runner, helper images, tokens, executor Docker, updater, skills de execução e lifecycle. A coordenação transversal permanece em `faleious-ai/gitlab_ynh` até existir o repositório `gitlab-mcp`.
