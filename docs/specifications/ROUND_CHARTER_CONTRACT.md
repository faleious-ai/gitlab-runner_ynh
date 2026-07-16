# Contrato de rodada completa

`continuity/ACTIVE_ROUND.md` é a autorização executável.

## Estados

`DRAFT`, `READY`, `IN_PROGRESS`, `BLOCKED_HUMAN`, `EXECUTED_AWAITING_REVIEW`, `ACCEPTED`, `CORRECTION_REQUIRED`, `SUPERSEDED`.

## Conteúdo obrigatório

- Charter-ID, objetivo e estado;
- perguntas humanas e decisões, ou declaração de que não foram necessárias;
- escopo, fora de escopo, paths/repositórios autorizados;
- tarefas, dependências e DAG paralelo;
- outputs, critérios de aceite e Definition of Done;
- validações/evidências;
- riscos, rollback, gates e bloqueios válidos;
- política de commits e pacote de revisão.

## Preparação

O ChatGPT pergunta ao usuário apenas o que possa alterar comportamento, compatibilidade, ambiente, custo, segurança, privilégio, publicação ou irreversibilidade. Questões técnicas reversíveis são decididas e justificadas pelo orquestrador.

## Execução

O Codex executa todo o charter `READY`. Orientação adicional do prompt é registrada, mas não autoriza expansão silenciosa da missão ou operação irreversível.

## Saída

O Codex encerra em `EXECUTED_AWAITING_REVIEW` ou `BLOCKED_HUMAN`. Somente o orquestrador registra `ACCEPTED`.
