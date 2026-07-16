# Contrato de rodada completa

`continuity/ACTIVE_ROUND.md` é a autorização executável. A rodada deve definir não apenas implementação e validação, mas também como o resultado será publicado e revisado no GitHub.

## Estados

- `DRAFT`: perguntas ou decisões pendentes.
- `READY`: autorizado para execução integral.
- `IN_PROGRESS`: execução iniciada.
- `LOCAL_COMPLETE_AWAITING_SYNC`: tarefas/checks concluídos e commit apenas local.
- `REMOTE_SYNC_BLOCKED`: publicação remota falhou por acesso, divergência ou indisponibilidade.
- `BLOCKED_HUMAN`: todo trabalho independente e persistência possível terminaram; resta gate humano real.
- `EXECUTED_AWAITING_REVIEW`: commits publicados e verificáveis em `origin/master`.
- `ACCEPTED`: revisor confirmou critérios e evidências.
- `CORRECTION_REQUIRED`: revisão encontrou lacunas.
- `SUPERSEDED`: substituído.

## Transição obrigatória

`EXECUTED_AWAITING_REVIEW` só pode ser declarado após:

1. commit local final;
2. push fast-forward sem force;
3. `HEAD == origin/master`;
4. SHA completo recuperável no GitHub;
5. evidências, round record, status e handoff publicados;
6. mesma verificação em todos os repositórios cross-repo.

Commit exclusivamente local usa `LOCAL_COMPLETE_AWAITING_SYNC`. Falha de push usa `REMOTE_SYNC_BLOCKED`.

## Conteúdo obrigatório

- Charter-ID, objetivo e estado;
- perguntas humanas e decisões, ou declaração de que não foram necessárias;
- escopo, fora de escopo, paths/repositórios autorizados;
- entradas canônicas e baseline `origin/master`;
- tarefas, dependências e DAG paralelo;
- outputs, critérios de aceite e Definition of Done;
- validações/evidências;
- riscos, rollback, gates e bloqueios válidos;
- política de commit, reconciliação, push e handoff;
- pacote remoto de revisão com SHAs completos e paths/URLs do GitHub.

## Preparação

O ChatGPT pergunta ao usuário apenas o que possa alterar comportamento, compatibilidade, ambiente, custo, segurança, privilégio, publicação ou irreversibilidade. Questões técnicas reversíveis são decididas e justificadas pelo orquestrador.

## Execução

O Codex executa todo o charter `READY`. Orientação adicional do prompt é registrada, mas não autoriza expansão silenciosa da missão ou operação irreversível.

## Saída

O Codex encerra conforme o estado real: `LOCAL_COMPLETE_AWAITING_SYNC`, `REMOTE_SYNC_BLOCKED`, `BLOCKED_HUMAN` ou `EXECUTED_AWAITING_REVIEW`. Somente o orquestrador registra `ACCEPTED`.

Todo charter deve declarar que commit local não basta, que um único commit final por repositório deve ser publicado em `origin/master`, que os HEADs local/remoto precisam coincidir e que links locais `C:/...` não substituem evidência versionada.