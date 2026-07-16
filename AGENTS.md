# AGENTS.md

## Missão

Manter o pacote YunoHost do GitLab Runner com atualização segura, reproduzível e coordenada entre o binário Runner e suas helper images. O repositório remoto é a fonte de verdade; estado exclusivamente local não é entrega persistida.

## Contrato de invocação

`Leia AGENTS.md e continue` significa executar integralmente o charter `READY` em `continuity/ACTIVE_ROUND.md`, concluir todas as tarefas não bloqueadas e publicar o commit final em `origin/master` de cada repositório afetado.

Orientação adicional deve ser registrada no round record e não expande silenciosamente missão ou autorização.

## Papéis

- **Maestro Diretor humano:** missão, prioridade, consequências, gates e irreversibilidade.
- **ChatGPT:** orquestrador e revisor; pergunta o necessário, define a rodada completa e revisa somente resultados remotos verificáveis.
- **Codex:** executor principal; executa, integra subagentes, valida, cria o commit, publica em `origin/master` e entrega o pacote remoto de revisão. Não aceita o próprio trabalho.
- **Subagentes:** frentes independentes, sem commit, push, integração final ou expansão de escopo.

## Entrada mínima

1. Leia `continuity/HANDOFF_CURRENT.md`.
2. Leia `continuity/STATUS.md`.
3. Leia `continuity/ACTIVE_ROUND.md`.
4. Execute `git fetch origin` e resolva HEAD local e `origin/master`.
5. Confirme charter `READY`; caso contrário, não implemente.
6. Carregue somente contexto roteado.

## Roteamento

| Necessidade | Leia |
|---|---|
| propósito e integração | `CONTEXT.md` |
| charter autorizado e DAG | `continuity/ACTIVE_ROUND.md` |
| plano de longo prazo | `continuity/EXECUTION_PLAN.md` |
| protocolo de execução, commit e push | `continuity/ROUND_PROTOCOL.md` |
| revisão | `continuity/REVIEW_PROTOCOL.md` |
| decisões/rationale | `continuity/DECISIONS.md` e ADRs |
| papéis | `docs/architecture/ORCHESTRATOR_EXECUTOR_MODEL.md` |
| arquitetura MAESTRO | `docs/architecture/MAESTRO_WORK_ARCHITECTURE.md` |
| limites cross-repo | `docs/architecture/CROSS_REPOSITORY_BOUNDARIES.md` |
| contrato de rodada | `docs/specifications/ROUND_CHARTER_CONTRACT.md` |
| subagentes/paralelismo | `docs/specifications/PARALLEL_EXECUTION_POLICY.md` |
| autoupdate Runner | `docs/specifications/RUNNER_AUTOUPDATE_SPEC.md` |
| divisão detalhada | `docs/specifications/WORK_BREAKDOWN.md` |
| evidências | `evidence/EVIDENCE_INDEX.md` |

## Execução completa

- Execute todo o charter e dependências inevitáveis.
- Não pare por progresso, tarefa longa, pesquisa, teste falho ou primeira estratégia malsucedida.
- Ao bloquear uma frente, continue todas as independentes.
- Só pare por conclusão integral, bloqueio humano válido ou interrupção ambiental real com estado seguro persistido.
- Commit apenas local recebe `LOCAL_COMPLETE_AWAITING_SYNC`.
- Falha de publicação recebe `REMOTE_SYNC_BLOCKED`.
- `EXECUTED_AWAITING_REVIEW` exige SHA completo publicado e recuperável em `origin/master` de todos os repositórios afetados.

## Paralelismo

Use subagentes para manifest/sources, lifecycle, tokens, Docker/helpers, testes/workflows e upstream quando independentes. O Codex mantém ownership de integração, documentos canônicos, validação final, commit e push.

## Invariantes

- Exclusivamente `master`; sem branches, PRs ou worktrees.
- Um commit final publicado por rodada e repositório; trabalho cross-repo usa o mesmo `Round-ID`.
- Reconcilie `origin/master` antes do commit e do push; nunca force push.
- Commit ainda não publicado pode ser rebaseado ou recriado sobre o remoto mais recente, com repetição dos checks impactados, para preservar um único commit final fast-forward.
- No fechamento, atualize implementação/docs, `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, `EVIDENCE_INDEX` e round record.
- A conclusão exige `HEAD == origin/master`, árvore limpa e SHA completo recuperável no GitHub.
- Pacote de revisão usa paths/URLs remotos; links locais `C:/...` não são evidência disponível ao revisor.
- Runner e helper images são conjunto atômico.
- Releases permanecem fixadas por versão, URL e SHA256; nunca resolver `latest` em runtime.
- Nunca persistir runner token, authentication token, PAT, segredo Docker ou credencial.
- Registro/executor usam ambiente controlado e redaction.
- Questões técnicas reversíveis são decididas no mandato; gates seguem ADR-0004/ADR-0005.

## Validação

Conforme escopo: schema/lint, sources/hashes, determinismo, install, upgrade, service, registration redigido, Docker/helper image, backup/restore, remove, idempotência, erros e ausência de segredo.

## Fechamento

A execução só termina com todo trabalho não bloqueado concluído, evidência indexada, commits publicados em `origin/master`, HEADs local/remoto coincidentes, handoff atualizado e pacote remoto pronto para revisão do ChatGPT.