# Handoff atual

Estado: `READY_FOR_CODEX_FULL_ROUND`  
Charter ativo: `CHR-WP02-001`  
Revisão anterior: `REV-RND-20260716-003 — ACCEPTED`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Retomada mínima

1. Ler `AGENTS.md`.
2. Confirmar HEAD de `master` neste repositório e no coordenador.
3. Ler `continuity/STATUS.md` e `continuity/ACTIVE_ROUND.md`.
4. Confirmar `CHR-WP02-001` em estado `READY`.
5. Atribuir novo `Round-ID`, construir o DAG de execução e trabalhar até concluir tudo que não dependa de gate humano.

## Trabalho autorizado

- retirar a credencial da árvore atual sem reproduzir o valor;
- adicionar secret scan e testes de redaction;
- reparar ou remover justificadamente a action `register` e centralizar o fluxo de registro;
- implementar fonte, proveniência, resolver atômico e generator determinístico para Runner + helper images;
- adicionar fixtures offline, testes negativos e CI read-only;
- gerar relatório de candidata sem promover versão;
- atualizar continuidade/evidência e síntese no coordenador.

## Paralelismo

As frentes S1, S2, U1, U2/U3 e A1 podem ser distribuídas a subagentes com ownership exclusivo de paths. O Codex mantém integração, arquivos canônicos, validação final e commit.

## Restrições

Não usar token histórico, não registrar Runner real, não executar `unregister --all-runners`, não promover versão, não publicar release, não criar branch/PR/worktree e não reescrever histórico.

## Gate humano

`HG-RUN-SEC-01`: revogação, rotação ou confirmação de expiração do valor histórico deve ser feita por quem administra o projeto GitLab do package_check.

O Codex não interrompe o trabalho por esse gate antes de concluir todas as tarefas técnicas independentes.

## Saída

- `EXECUTED_AWAITING_REVIEW` quando o charter técnico estiver demonstrado e o estado do gate estiver registrado;
- `BLOCKED_HUMAN` somente se o gate for necessário para fechar o critério de segurança, após todo o restante estar concluído.

Entregar commits, testes, matriz tarefa-output-evidência, proveniência, relatório de candidata, riscos residuais e estado do gate. Não declarar `ACCEPTED`.
