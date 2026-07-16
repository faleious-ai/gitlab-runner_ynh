# Protocolo de rodada de IA

Identificadores: `RND-YYYYMMDD-NNN` e `T-<NN>-<slug>`.

A rodada é a unidade de autorização, baseline, escopo e revisão. A tarefa é a unidade de implementação, commit, sincronização e reversão. Estado exclusivamente local não é persistência MAESTRO.

## ORCHESTRATE

O ChatGPT reconcilia estado, decisões, evidências e HEADs remotos; resolve questões técnicas reversíveis; pergunta ao Maestro Diretor apenas o que altera produto, consequência, custo, privilégio, risco ou irreversibilidade; e só marca o charter `READY` quando tarefas, DAG, seams, critérios, gates e persistência estão definidos.

Cada tarefa deve declarar:

- `Task-ID`, objetivo e dependências;
- seam público observado;
- claims/invariantes e interfaces tocadas;
- paths autorizados e ownership;
- contrato de verificação com comandos e estados de evidência esperados;
- estratégia RED→GREEN quando houver mudança comportamental;
- condição de commit e rollback.

## START — Codex

1. confirmar repositório e `master`;
2. executar `git fetch origin`;
3. registrar `baseline_head = origin/master` da rodada;
4. verificar árvore limpa e HEAD reconciliado;
5. ler `AGENTS.md`, `HANDOFF_CURRENT.md`, `STATUS.md`, `ACTIVE_ROUND.md` e o índice de skills;
6. confirmar charter `READY`, atribuir `Round-ID` e registrar orientação adicional;
7. decompor DAG, tarefas e paralelismo seguro.

## PRE-BUILD CHALLENGE

Para tarefa de alto impacto, antes do primeiro edit:

1. executar revisão adversarial da tarefa contra charter, código, ADRs e fontes externas aplicáveis;
2. tentar refutar goal, seams, invariantes, lifecycle, segurança e rollback;
3. corrigir especificação técnica reversível autonomamente;
4. escalar apenas decisão humana material;
5. registrar `GO` ou `NO_GO` com evidência.

## EXECUTE — POR TAREFA

1. marcar tarefa `IN_PROGRESS` no registro de trabalho quando necessário;
2. carregar somente contexto e skills aplicáveis;
3. para mudança comportamental, executar ciclo `RED → GREEN` no seam público;
4. implementar somente o mínimo exigido pelos claims;
5. executar gate cascade proporcional: parse/build → teste focal → integração → lifecycle/smoke → segurança/CI;
6. em falha inesperada, executar backprop antes de nova tentativa cega;
7. manter matriz claim → mecanismo → comando → resultado → estado de evidência;
8. concluir todos os nós independentes quando uma frente bloquear.

## BACKPROP

Toda falha inesperada é classificada como:

- `IMPLEMENTATION_BUG`;
- `MISSING_CRITERION`;
- `INCOMPLETE_CRITERION`;
- `WRONG_CRITERION`;
- `MISSING_REQUIREMENT`;
- `ENVIRONMENTAL_LIMIT`;
- `EXTERNAL_DEPENDENCY`.

Backprop técnico pode atualizar invariante, critério, teste e memória sem gate. Mudança de comportamento externo, produto, custo, acesso, risco ou irreversibilidade exige decisão do Maestro Diretor.

## INTERNAL REVIEW — ANTES DE CADA COMMIT

Executar duas revisões independentes, preferencialmente em contextos/subagentes separados:

1. **Spec/Charter:** requisitos ausentes/parciais, scope creep, interface drift, claims sem prova.
2. **Engineering:** bugs, segurança, lifecycle, compatibilidade, falhas negativas, simplicidade e reversibilidade.

P0/P1 bloqueiam o commit. P2/P3 são corrigidos ou recebem rationale explícito. Depois executar `maestro-check` e `maestro-guardrails`.

## TASK COMMIT

Para cada tarefa concluída:

1. executar `git fetch origin`;
2. confirmar que o remoto é ancestral direto do trabalho local ou reconciliar apenas mudanças ainda não publicadas;
3. revisar diff, segredos, ruído, paths e claims;
4. repetir checks impactados;
5. criar exatamente um commit atômico com mensagem `RND-<id> T-<id>: <resultado>`;
6. não incluir trabalho de outra tarefa independente;
7. não criar commits intermediários de teste RED; a evidência RED fica em output/fixture/log versionado ou round record, e o commit final contém teste + fix coerentes;
8. registrar rollback seletivo pela reversão desse commit.

Após o commit local, o estado da tarefa é `TASK_LOCAL_COMPLETE_AWAITING_SYNC`.

## TASK REMOTE SYNC

1. executar `git fetch origin`;
2. verificar `git rev-list --left-right --count origin/master...HEAD`;
3. com fast-forward seguro, executar `git push origin master`;
4. nunca usar force push;
5. após push, fazer novo fetch e confirmar `HEAD == origin/master`;
6. confirmar SHA completo recuperável pelo GitHub e outputs remotos presentes;
7. só então marcar tarefa `TASK_REMOTE_VERIFIED` e iniciar a próxima tarefa que escreva neste repositório.

Falha de push produz `TASK_REMOTE_SYNC_BLOCKED`. Não empilhar novos commits neste repositório até resolver; continue apenas trabalho independente sem escrita ou em outro repositório.

Trabalho cross-repo usa o mesmo `Round-ID` e `Task-ID`, com um commit atômico em cada repositório afetado e confirmação remota em todos antes de fechar a tarefa.

## CONVERGENCE

A cada ciclo relevante, registre:

- claims/invariantes demonstrados versus totais;
- gates passando/falhando;
- findings P0–P3 abertos;
- tarefas concluídas/bloqueadas;
- falhas repetidas e categorias de backprop;
- estabilidade do diff como sinal secundário.

Oscilação, pass rate estacionado, repetição de estratégia ou findings persistentes indicam não convergência. Corrija especificação, validação ou ownership; não apenas aumente iterações.

## ROUND CLOSE

A última tarefa da rodada é de integração/continuidade e atualiza `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, decisões, evidence index e round record.

Estados de saída:

- `TASK_LOCAL_COMPLETE_AWAITING_SYNC`;
- `TASK_REMOTE_SYNC_BLOCKED`;
- `BLOCKED_HUMAN`;
- `EXECUTED_AWAITING_REVIEW`.

`EXECUTED_AWAITING_REVIEW` exige:

- todos os Task-IDs concluídos ou bloqueados validamente;
- todos os commits de tarefa publicados em ordem em `origin/master`;
- HEADs coincidentes e árvores limpas;
- matriz task→commit→claim→evidência remota;
- pacote sem links locais;
- CI/lifecycle classificados segundo a prova real.

O Codex nunca marca `ACCEPTED`.

## REVIEW

O ChatGPT revisa o intervalo `baseline_head...round_head`, cada commit de tarefa e o comportamento integrado. Persiste `ACCEPTED`, `CORRECTION_REQUIRED`, `HUMAN_GATE` ou `REJECTED_UNSAFE` em tarefa/commit próprio de orquestração.
