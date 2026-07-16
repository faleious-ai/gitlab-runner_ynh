# Modelo de orquestração e execução

## Papéis

- **Maestro Diretor humano:** decide missão, prioridade, consequências práticas, gates éticos, custos relevantes e operações irreversíveis.
- **ChatGPT — orquestrador e revisor:** reconcilia o repositório, pergunta ao usuário o necessário, especifica a rodada completa em `continuity/ACTIVE_ROUND.md`, revisa commits/evidências e define aceite, correção ou gate humano.
- **Codex — executor principal:** executa integralmente o charter `READY`, coordena subagentes, integra, valida e persiste. Não aprova o próprio resultado.
- **Subagentes:** trabalham em frentes independentes sem autoridade de commit, integração final ou expansão de escopo.

## Invocação

`Leia AGENTS.md e continue` significa executar todo o charter ativo e só parar após concluir tudo que não estiver bloqueado por decisão humana real.

## Fluxo

`Usuário -> ChatGPT/orquestrador -> ACTIVE_ROUND -> Codex/subagentes -> commits/evidências -> ChatGPT/revisor -> aceite, correção ou gate humano`.

## Bloqueio

Ao encontrar gate humano, o Codex conclui primeiro todas as tarefas independentes, deixa estado seguro e registra o grafo restante. Usuário e orquestrador resolvem o gate; a retomada usa charter revisado e novo `Round-ID` vinculado ao mesmo objetivo quando aplicável.

## Autoridade local

Este repositório mantém autoridade sobre Runner, helper images, tokens, executor Docker e lifecycle. A coordenação transversal permanece em `faleious-ai/gitlab_ynh` até existir o repositório `gitlab-mcp`.
