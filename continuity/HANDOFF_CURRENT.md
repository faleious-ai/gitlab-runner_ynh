# Handoff atual

Estado: `EXECUTED_AWAITING_REVIEW`
Charter ativo: `CHR-WP02-003`  
Revisão anterior: `REV-RND-20260716-007 — CORRECTION_REQUIRED`  
Processo vigente: `ADR-0006`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Resultado persistido

`RND-20260716-010` executou T01–T07 e fechou T08 no Runner/coordenador, com um commit remoto por Task-ID e HEADs reconciliados. A implementação funcional permanece no Runner; este arquivo é o handoff para revisão independente.

Runner funcional antes de T08: `2d9cb41f41f292f3b4bd19513b91ca66720457d6`. O commit T08 do Runner será o novo `round_head` após publicação.

Evidência final: 32 testes locais, secret scan limpo, parsers JSON/TOML, Bash, dry-run e allowlist passam; `manifest.toml` permanece `18.6.2~ynh1`. CI remoto continua `UNVERIFIED` porque o run/status não foi recuperável neste ambiente; lifecycle YunoHost real também não foi observado.

Para a revisão, usar `continuity/rounds/RND-20260716-010.md`, `evidence/EVIDENCE_INDEX.md` e o intervalo completo de commits remotos. Não usar links locais como prova.

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
