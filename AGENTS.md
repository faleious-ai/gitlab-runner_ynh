# AGENTS.md

## Missão

Manter o pacote YunoHost do GitLab Runner com atualização segura, reproduzível e coordenada entre o binário Runner e suas helper images. O repositório remoto é a fonte de verdade; estado exclusivamente local não é entrega persistida.

## Contrato de invocação

`Leia AGENTS.md e continue` significa executar integralmente o charter `READY` em `continuity/ACTIVE_ROUND.md`, concluir todas as tarefas não bloqueadas e publicar cada commit de tarefa em `origin/master` antes de avançar para a próxima tarefa que escreva neste repositório.

Orientação adicional deve ser registrada no round record e não expande silenciosamente missão, autorização ou irreversibilidade.

## Papéis

- **Maestro Diretor humano:** missão, prioridade, consequências, gates e irreversibilidade.
- **ChatGPT:** orquestrador e revisor; pergunta o necessário, define a rodada completa e revisa somente resultados remotos verificáveis.
- **Codex:** executor principal; executa, integra subagentes, valida, cria e publica commits de tarefa e entrega o pacote remoto de revisão. Não aceita o próprio trabalho.
- **Subagentes:** frentes independentes, sem commit, push, integração final ou expansão de escopo.

## Entrada mínima

1. Leia `continuity/HANDOFF_CURRENT.md`.
2. Leia `continuity/STATUS.md`.
3. Leia `continuity/ACTIVE_ROUND.md`.
4. Execute `git fetch origin` e resolva HEAD local e `origin/master`.
5. Confirme charter `READY`; caso contrário, não implemente.
6. Carregue somente contexto roteado.
7. Leia `.agents/skills/README.md` e carregue apenas as skills aplicáveis à tarefa atual.

## Roteamento

| Necessidade | Leia |
|---|---|
| propósito e integração | `CONTEXT.md` |
| charter autorizado e DAG | `continuity/ACTIVE_ROUND.md` |
| plano de longo prazo | `continuity/EXECUTION_PLAN.md` |
| execução, commits e push | `continuity/ROUND_PROTOCOL.md` |
| revisão | `continuity/REVIEW_PROTOCOL.md` |
| decisões/rationale | `continuity/DECISIONS.md` e ADRs |
| papéis | `docs/architecture/ORCHESTRATOR_EXECUTOR_MODEL.md` |
| arquitetura MAESTRO | `docs/architecture/MAESTRO_WORK_ARCHITECTURE.md` |
| limites cross-repo | `docs/architecture/CROSS_REPOSITORY_BOUNDARIES.md` |
| contrato de rodada | `docs/specifications/ROUND_CHARTER_CONTRACT.md` |
| subagentes/paralelismo | `docs/specifications/PARALLEL_EXECUTION_POLICY.md` |
| autoupdate Runner | `docs/specifications/RUNNER_AUTOUPDATE_SPEC.md` |
| skills locais | `.agents/skills/README.md` |
| evidências | `evidence/EVIDENCE_INDEX.md` |

## Skills obrigatórias por condição

- mudança comportamental: `maestro-tdd`;
- falha inesperada ou finding recorrente: `maestro-backprop`;
- fato externo incerto: `maestro-research`;
- mudança de alto impacto antes do primeiro edit: `maestro-review` em modo spec challenge;
- antes de todo commit: `maestro-check`, `maestro-review` em dois eixos e `maestro-guardrails`;
- loop com múltiplas tentativas: `maestro-convergence`;
- melhoria estrutural sem mudança de comportamento: `maestro-deepen`, somente em tarefa própria.

## Execução completa

- Execute todo o charter e dependências inevitáveis.
- Não pare por progresso, tarefa longa, pesquisa, teste falho ou primeira estratégia malsucedida.
- Ao bloquear uma frente, continue todas as independentes.
- Cada tarefa declara seam, claims/invariantes, verificação, ownership e dependências antes do primeiro edit.
- Cada tarefa concluída produz um commit atômico remoto próprio; não acumule tarefas independentes em um commit.
- Só pare por conclusão integral, bloqueio humano válido ou interrupção ambiental real com estado seguro persistido.
- Commit apenas local recebe `TASK_LOCAL_COMPLETE_AWAITING_SYNC`.
- Falha de publicação recebe `TASK_REMOTE_SYNC_BLOCKED`.
- `EXECUTED_AWAITING_REVIEW` exige todos os commits de tarefa publicados e recuperáveis em todos os repositórios afetados.

## TDD e evidência

- Teste comportamento em seam público; busca textual ou presença de arquivo não prova execução.
- Mudança comportamental exige evidência RED anterior ao fix e GREEN posterior.
- Cada claim aponta para método, comando, resultado e limitação.
- Diferencie `STRUCTURALLY_OBSERVED`, `LOCAL_VERIFIED`, `REMOTE_CI_VERIFIED` e `LIFECYCLE_VERIFIED`.
- Nunca promova claim além da evidência disponível.

## Paralelismo

Use subagentes para manifest/sources, lifecycle, tokens, Docker/helpers, testes/workflows e upstream quando independentes. O Codex mantém ownership de integração, documentos canônicos, validação final, commits de tarefa e push. Subagentes nunca escrevem simultaneamente nos mesmos paths.

## Invariantes

- Exclusivamente `master`; sem branches, PRs ou worktrees.
- Uma tarefa concluída gera exatamente um commit publicado por repositório afetado; trabalho cross-repo usa o mesmo `Round-ID` e `Task-ID`.
- Não squashar, não reordenar e não reescrever commits publicados.
- Reconcilie `origin/master` antes de cada commit e de cada push; nunca force push.
- Commit ainda não publicado pode ser rebaseado ou recriado sobre o remoto mais recente, com repetição dos checks impactados.
- Após cada commit de tarefa, publique, faça novo fetch e confirme `HEAD == origin/master` antes da próxima escrita neste repositório.
- No fechamento da rodada, atualize `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, `EVIDENCE_INDEX` e round record em tarefa explícita de continuidade.
- Pacote de revisão usa paths/URLs remotos; links locais não são evidência.
- Runner e helper images são conjunto atômico.
- Releases permanecem fixadas por versão, URL e SHA256; nunca resolver `latest` em runtime.
- Nunca persistir runner token, authentication token, PAT, segredo Docker ou credencial.
- Registro/executor usam ambiente controlado e redaction.
- Questões técnicas reversíveis são decididas no mandato; gates seguem ADR-0004/ADR-0005.

## Validação

Conforme escopo: schema/lint, sources/hashes, determinismo, testes focais, integração, install, upgrade, service, registration redigido, Docker/helper image, backup/restore, remove, idempotência, erros e ausência de segredo. Gates baratos precedem gates caros.

## Fechamento

A execução só termina com todo trabalho não bloqueado concluído, matriz claim→prova reconciliada, commits de tarefa publicados, HEADs local/remoto coincidentes, árvores limpas, handoff atualizado e pacote remoto pronto para revisão do ChatGPT.
