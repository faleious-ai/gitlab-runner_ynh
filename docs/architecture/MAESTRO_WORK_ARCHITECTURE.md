# Arquitetura MAESTRO local

## Finalidade

Tornar o repositório uma superfície de trabalho continuável para humanos e agentes, na qual uma mudança no pacote Runner atravessa intenção, especificação, contexto, contratos, execução, validação, governança e memória.

## Princípio

O agente pode executar tecnicamente com ampla autonomia, mas não pode transformar plausibilidade em prova nem atravessar gates de risco, segredo ou irreversibilidade.

## Camadas

1. **Intenção** — issue, usuário ou incidente define o resultado desejado.
2. **Especificação** — `RUNNER_AUTOUPDATE_SPEC.md` e work package definem escopo e aceite.
3. **Contexto** — `AGENTS.md` roteia leitura mínima e arquivos sob demanda.
4. **Contratos** — manifest, scripts, testes, versão Runner/helper images e lifecycle.
5. **Execução** — unidade delimitada diretamente em `master`.
6. **Validação** — checks proporcionais, inclusive executor/helper image quando aplicável.
7. **Governança** — ADRs e gates humanos.
8. **Memória** — status, handoff, rounds, evidence index e Git.

## Máquina de estados

```text
READY -> SCOPED -> EXECUTING -> VALIDATING -> PERSISTING -> COMMITTED -> READY
                         \-> BLOCKED
                         \-> REVERTING -> PERSISTING
```

Nenhum estado é promovido por declaração. `COMMITTED` exige commit real em `master`.

## Memória em camadas

| Camada | Autoridade |
|---|---|
| orientação | `AGENTS.md` |
| propósito | `CONTEXT.md` |
| contrato | `docs/specifications/` |
| rationale | `docs/decisions/` |
| estado | `continuity/STATUS.md` |
| retomada | `continuity/HANDOFF_CURRENT.md` |
| ordem | `continuity/EXECUTION_PLAN.md` |
| prova | `evidence/EVIDENCE_INDEX.md` |
| histórico | `continuity/rounds/` e Git |

## Papéis

- **Maestro humano:** missão, risco, segredo, produção e irreversibilidade.
- **Agente executor:** análise, decisão técnica, implementação, testes e persistência.
- **Verificador:** testes, revisão separada, pipeline ou agente em fase de crítica.
- **Repositório:** memória e contratos executáveis.

## Evidência proporcional

- mudança documental: coerência e rastreabilidade;
- manifest/source: schema, URLs, hashes e matriz;
- updater: determinismo, idempotência e falhas negativas;
- Runner: service, registration e executor;
- segurança: redaction e ausência de segredo;
- produção: gate humano e rollback.

## Fechamento

Cada rodada deve deixar o repositório mais fácil de entender e continuar. Se um agente novo ainda precisar reconstruir a intenção pelo chat, a rodada não fechou corretamente.