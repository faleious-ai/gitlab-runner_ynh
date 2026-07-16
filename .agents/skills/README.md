# Skills MAESTRO de engenharia

Este diretório contém adaptações locais das práticas Cavekit para a arquitetura MAESTRO. Não é uma instalação do runtime Cavekit e não ativa hooks, branches, worktrees, stop loops ou agentes externos.

## Proveniência

- Cavekit v4: `JuliusBrussee/cavekit@c322f0bb6db82163041930467f3ce32754d42827`;
- Cavekit v3.1.0: tag `v3.1.0`;
- licença e atribuição: `docs/third_party/CAVEKIT_NOTICE.md`;
- decisão local: `docs/decisions/ADR-0006-TASK_COMMITS_AND_CAVEKIT_SYNTHESIS.md`.

## Skills

| Skill | Uso |
|---|---|
| `maestro-spec` | criar/amendar contrato técnico e ownership sem colapsar memória em um arquivo único |
| `maestro-build` | executar tarefa completa contra charter, com commit remoto por tarefa |
| `maestro-check` | detectar drift read-only entre claims, código, testes, evidência e estado |
| `maestro-grill` | esclarecer somente decisões humanas materiais, uma por vez, com recomendação |
| `maestro-research` | resolver unknown externo com fonte primária e registro durável |
| `maestro-review` | challenge pré-build e revisão pré-commit em dois eixos |
| `maestro-deepen` | refatorar um módulo por tarefa sem alterar comportamento |
| `maestro-caveman` | comprimir apenas matrizes e ledgers sem perder fatos |
| `maestro-backprop` | transformar falha em critério/invariante/teste/memória |
| `maestro-tdd` | RED→GREEN por seam público em toda mudança comportamental |
| `maestro-convergence` | distinguir convergência, ceiling, oscilação e retrabalho |
| `maestro-guardrails` | simplicidade, mudança cirúrgica, claims rastreáveis e verificação antes de commit |

## Ordem típica por tarefa

1. `maestro-grill` somente se houver decisão humana material não resolvida.
2. `maestro-research` para fatos externos incertos.
3. `maestro-spec` para tornar seam, claims, gates e Task-ID executáveis.
4. `maestro-review` em modo pre-build para alto impacto.
5. `maestro-tdd` + `maestro-build`.
6. `maestro-backprop` em qualquer falha inesperada.
7. `maestro-convergence` em loops com múltiplas tentativas.
8. `maestro-check` + `maestro-review` + `maestro-guardrails` antes do commit.
9. commit e sincronização conforme `continuity/ROUND_PROTOCOL.md`.

`maestro-deepen` ocorre apenas em tarefa estrutural própria e com comportamento congelado.

## Precedência

1. decisão humana explícita;
2. ADRs e charter ativo;
3. `AGENTS.md` e protocolos;
4. skill local;
5. fonte Cavekit.

Uma skill nunca amplia escopo, privilégio ou irreversibilidade.
