# AGENTS.md

## Missão

Manter o pacote YunoHost do GitLab Runner com atualização segura, reproduzível e coordenada entre o binário Runner e suas helper images. O repositório é a fonte de verdade; contexto de chat não é autoridade.

## Entrada mínima obrigatória

1. Leia `continuity/HANDOFF_CURRENT.md`.
2. Leia `continuity/STATUS.md`.
3. Resolva o HEAD atual de `master` antes de qualquer escrita.
4. Carregue somente as rotas necessárias à unidade ativa.

## Roteamento sob demanda

| Necessidade | Leia |
|---|---|
| propósito, limites e integração com o programa | `CONTEXT.md` |
| próxima unidade e ordem local | `continuity/EXECUTION_PLAN.md` |
| protocolo de rodada/commit | `continuity/ROUND_PROTOCOL.md` |
| decisões e rationale | `continuity/DECISIONS.md` e ADRs indicados |
| arquitetura MAESTRO local | `docs/architecture/MAESTRO_WORK_ARCHITECTURE.md` |
| limites entre repositórios | `docs/architecture/CROSS_REPOSITORY_BOUNDARIES.md` |
| contrato do autoupdate | `docs/specifications/RUNNER_AUTOUPDATE_SPEC.md` |
| divisão detalhada | `docs/specifications/WORK_BREAKDOWN.md` |
| evidências | `evidence/EVIDENCE_INDEX.md` |

Não leia tudo por padrão. Expanda o contexto somente quando dependência, risco ou decisão exigir.

## Invariantes operacionais

- Trabalhe exclusivamente em `master`; não crie branches, PRs ou worktrees secundárias.
- Cada rodada de IA termina com exatamente um commit atômico neste repositório.
- Trabalho coordenado com `gitlab_ynh` usa o mesmo `Round-ID` nos dois commits.
- Reconcilie o HEAD antes do commit; nunca use force push.
- Atualize no mesmo commit: implementação/documentação, `STATUS`, `HANDOFF_CURRENT`, `EVIDENCE_INDEX` e registro em `continuity/rounds/`.
- Runner e helper images formam um conjunto de versão atômico; não atualizar apenas um lado sem compatibilidade demonstrada.
- Releases publicadas permanecem fixadas por versão, URL e SHA256; runtime nunca resolve `latest`.
- Nunca registre runner token, registration/authentication token, PAT, segredo Docker ou credencial de instância.
- Operações de registro/desregistro e executor devem usar ambiente controlado e redaction.
- O agente decide questões técnicas reversíveis; gates humanos seguem `ADR-0004`.
- Pare apenas em bloqueio real e registre causa, evidência e recurso/decisão necessários.

## Validação mínima

Aplicar conforme o escopo: schema/lint, integridade de sources, install, upgrade, service health, registration, executor Docker, helper image, backup/restore, remove, idempotência, erros e redaction.

A rodada só termina quando o commit está em `master` e o próximo agente consegue retomar pelo handoff.