# Handoff atual

Estado: `READY_FOR_CODEX_FULL_ROUND`  
Charter ativo: `CHR-WP02-003`  
Revisão anterior: `REV-RND-20260716-007 — CORRECTION_REQUIRED`  
Processo vigente: `ADR-0006`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Retomada mínima

1. Executar `git fetch origin` e confirmar árvore limpa/HEAD reconciliado.
2. Ler `AGENTS.md`, `continuity/STATUS.md`, `continuity/ACTIVE_ROUND.md` e `.agents/skills/README.md`.
3. Confirmar que `origin/master` contém `RND-20260716-009` e as 12 skills.
4. Atribuir novo `Round-ID`.
5. Executar `CHR-WP02-003` na ordem do DAG, com um commit remoto por Task-ID.
6. Após cada commit, confirmar `HEAD == origin/master` antes da próxima escrita.

## Direção funcional

Preservar descoberta, checksums, manifest candidato, pins do workflow e ausência de promoção. Corrigir:

- controlador `run__register()` e entradas efêmeras;
- interface legada de registro;
- backup/restore sem re-registro;
- trust criptográfico fail-closed;
- self-link e redirects;
- evidência canônica/portátil;
- CI remoto verificável ou bloqueio objetivo.

## Disciplina obrigatória

- TDD RED→GREEN por seam para toda mudança comportamental;
- backprop em falha inesperada;
- challenge pré-build nas tarefas T01, T03, T04 e T05;
- revisão interna em dois eixos antes de cada commit;
- matriz claim→prova e níveis de evidência honestos;
- nenhum squash, branch, PR, worktree ou force push.

## Gate

`HG-RUN-SEC-01` permanece risco histórico externo. Não usar nem testar a credencial antiga e não interromper trabalho técnico por esse gate.
