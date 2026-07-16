# Arquitetura MAESTRO local

## Finalidade

Tornar o repositório uma superfície de trabalho continuável para humanos e agentes, na qual cada mudança atravessa intenção, contrato, execução, validação, revisão, persistência e aprendizagem sem depender do contexto do chat.

## Princípio

O modelo descreve e executa; contratos, testes, gates e revisor decidem o que pode ser promovido. Plausibilidade nunca substitui prova. A autonomia técnica é ampla dentro do mandato e limitada por consequência humana, privilégio, risco e irreversibilidade.

## Camadas

1. **Intenção** — usuário, issue ou incidente define resultado e consequência.
2. **Especificação** — documentos em `docs/specifications/` definem o comportamento durável.
3. **Contexto** — `AGENTS.md` e índices roteiam progressive disclosure.
4. **Tarefa** — `ACTIVE_ROUND` define Task-ID, seam, claims, ownership, gates e rollback.
5. **Execução** — TDD, implementação mínima, subagentes com ownership e backprop.
6. **Validação** — gate cascade proporcional e estados explícitos de evidência.
7. **Revisão** — challenge pré-build, dois eixos pré-commit e revisor externo remoto.
8. **Persistência** — um commit remoto por tarefa, sem squash ou reescrita publicada.
9. **Governança** — ADRs e gates humanos proporcionais.
10. **Memória** — status, handoff, rounds, evidence index, learning ledger e Git.

## Máquina de estados

```text
ROUND_READY
  → TASK_SCOPED
  → PRE_BUILD_REVIEW?
  → RED
  → GREEN
  → VALIDATING
  → INTERNAL_REVIEW
  → TASK_COMMITTED_LOCAL
  → TASK_REMOTE_VERIFIED
  → next TASK | ROUND_INTEGRATION
  → EXECUTED_AWAITING_REVIEW
  → ACCEPTED | CORRECTION_REQUIRED | HUMAN_GATE | REJECTED_UNSAFE
```

Desvios:

```text
failure → BACKPROP → contract/test amendment → RED
sync failure → TASK_REMOTE_SYNC_BLOCKED
material decision → BLOCKED_HUMAN
unsafe remote state → selective revert/compensation
```

Nenhum estado é promovido por declaração. A tarefa só fica persistida quando o SHA está em `origin/master`. A rodada só fica revisável quando todos os commits e evidências estão remotos.

## Memória em camadas

| Camada | Autoridade |
|---|---|
| orientação | `AGENTS.md` |
| skills | `.agents/skills/README.md` e `SKILL.md` aplicáveis |
| propósito | `CONTEXT.md` |
| contrato durável | `docs/specifications/` |
| rationale | `docs/decisions/` e `continuity/DECISIONS.md` |
| autorização/tarefas | `continuity/ACTIVE_ROUND.md` |
| estado | `continuity/STATUS.md` |
| retomada | `continuity/HANDOFF_CURRENT.md` |
| aprendizagem | `continuity/LEARNING_LEDGER.md` |
| prova | `evidence/EVIDENCE_INDEX.md` |
| histórico | `continuity/rounds/` e commits Git |

Arquivos de estado não duplicam especificações; apontam para a autoridade.

## Unidade de rastreabilidade

A rodada possui `Round-ID` e baseline. Cada tarefa possui `Task-ID` e exatamente um commit por repositório afetado. O commit liga:

`Task-ID → claims/invariantes → seam → RED/GREEN → gates → evidência → rollback`.

Subagentes produzem outputs; somente o executor integra, valida, commita e publica.

## Evidência

- `STRUCTURALLY_OBSERVED`: forma/presença;
- `LOCAL_VERIFIED`: comportamento executado localmente;
- `REMOTE_CI_VERIFIED`: run remoto associado ao SHA;
- `LIFECYCLE_VERIFIED`: install/upgrade/service/backup/restore/remove proporcional;
- `UNVERIFIED` e `FAILED`.

Um nível não implica o seguinte. Busca textual nunca prova runtime.

## Aprendizagem

Falha inesperada é classificada e retropropagada para o menor contrato que a teria prevenido. O ledger preserva causa, RED, GREEN e padrão. Recorrência transforma caso local em tarefa sistêmica; não em expansão silenciosa do fix atual.

## Reversibilidade

O commit por tarefa é a unidade preferencial de reversão. Dependências entre commits são explícitas. Commits publicados não são squashados, reordenados ou reescritos. Operação irreversível continua atrás de gate humano.

## Fechamento

Cada tarefa deixa código e prova coerentes. Cada rodada deixa o programa mais fácil de continuar. Se um agente novo precisar reconstruir intenção, falhas ou prova pelo chat, a rodada não fechou corretamente.
