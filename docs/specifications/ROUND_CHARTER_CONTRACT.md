# Contrato de rodada completa

`continuity/ACTIVE_ROUND.md` é a autorização executável. A rodada define baseline, escopo, DAG, gates e intervalo de revisão. Cada tarefa define a unidade atômica de implementação, commit, sincronização e reversão.

## Estados

- `DRAFT`: perguntas ou decisões pendentes.
- `READY`: autorizado para execução integral.
- `IN_PROGRESS`: execução iniciada.
- `TASK_LOCAL_COMPLETE_AWAITING_SYNC`: tarefa concluída e commit apenas local.
- `TASK_REMOTE_SYNC_BLOCKED`: commit de tarefa não publicado por acesso, divergência ou indisponibilidade.
- `BLOCKED_HUMAN`: todo trabalho independente e persistência possível terminaram; resta gate humano real.
- `EXECUTED_AWAITING_REVIEW`: todos os commits de tarefa publicados e verificáveis.
- `ACCEPTED`, `CORRECTION_REQUIRED`, `SUPERSEDED`.

## Conteúdo obrigatório da rodada

- Charter-ID, objetivo, estado e `baseline_head` esperado;
- decisões humanas e técnicas vigentes;
- escopo, fora de escopo e repositórios autorizados;
- DAG de tarefas e ondas paralelas;
- gates humanos, riscos e rollback;
- Definition of Done integrada;
- plano de persistência remota e pacote de revisão.

## Conteúdo obrigatório de cada tarefa

| Campo | Exigência |
|---|---|
| `Task-ID` | único na rodada, estável e citado no commit |
| objetivo | um resultado reversível e verificável |
| dependências | Task-IDs e estado exigido |
| seam | interface pública observada pelo teste/validação |
| claims/invariantes | comportamento, segurança ou contrato que deve valer |
| paths/ownership | arquivos autorizados e conflitos proibidos |
| TDD | teste RED e GREEN para mudança comportamental, ou justificativa |
| gates | comandos exatos e nível de evidência esperado |
| review | eixos Spec/Charter e Engineering |
| commit | mensagem, condição de atomicidade e rollback |
| cross-repo | commits com mesmo Round-ID/Task-ID quando aplicável |

Tarefa grande demais para um commit coerente deve ser dividida antes do primeiro edit. Não use commits parciais apenas para registrar progresso.

## TDD

Toda mudança comportamental usa seam público predefinido. O charter não precisa prescrever a implementação, mas precisa tornar o comportamento observável. O executor registra:

1. teste/comando capaz de falhar pelo defeito ou ausência da capacidade;
2. RED observado antes do fix;
3. implementação mínima;
4. GREEN observado;
5. suíte/regressão proporcional.

Teste acoplado a detalhe interno, busca textual, constante tautológica ou mock que não atravessa o caminho real não satisfaz o contrato.

## Backprop

Falhas inesperadas produzem classificação, causa raiz, alteração de invariante/critério quando necessária, teste de regressão e memória durável. O executor pode corrigir autonomamente lacunas técnicas reversíveis. Alteração material de comportamento externo ou consequência prática vira gate humano.

## Revisão pré-commit

Toda tarefa recebe duas passagens independentes antes do commit:

- conformidade com spec/charter;
- engenharia, segurança e lifecycle.

P0/P1 bloqueiam. Findings sem correção recebem rationale explícito e não podem ser omitidos do pacote remoto.

## Persistência

- um commit por tarefa concluída e por repositório afetado;
- push e verificação remota antes da próxima tarefa que escreva no mesmo repositório;
- sem squash, branch, PR, worktree, force push ou reescrita de histórico publicado;
- a última tarefa da rodada reconcilia continuidade e evidências;
- `EXECUTED_AWAITING_REVIEW` exige lista completa dos commits entre `baseline_head` e `round_head`.

## Preparação

O ChatGPT pergunta ao Maestro Diretor apenas o que possa alterar comportamento, compatibilidade, ambiente, custo, segurança, privilégio, publicação ou irreversibilidade. Questões técnicas reversíveis são decididas e justificadas pelo orquestrador.

## Saída

O Codex encerra conforme o estado real. Somente o orquestrador registra `ACCEPTED` após revisar cada commit e o intervalo integrado.
