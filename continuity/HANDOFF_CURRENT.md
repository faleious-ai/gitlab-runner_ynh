# Handoff atual

Estado: `READY_FOR_CODEX_FULL_ROUND`  
Charter ativo: `CHR-WP02-003`  
Revisão anterior: `REV-RND-20260716-007 — CORRECTION_REQUIRED`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Retomada mínima

1. Ler `AGENTS.md`.
2. Confirmar `origin/master` neste repositório e no coordenador.
3. Ler `continuity/STATUS.md` e `continuity/ACTIVE_ROUND.md`.
4. Atribuir novo `Round-ID` e executar integralmente `CHR-WP02-003`.
5. Publicar e verificar remotamente conforme `ROUND_PROTOCOL.md`.

## Direção

Não reimplementar descoberta, checksum parser ou manifest candidato já demonstrados. Corrigir os pontos de integração que impedem o uso seguro:

- controlador `run__register()` e entradas efêmeras do config panel;
- remoção da interface legada de registro;
- backup/restore sem dependência de credencial não persistida;
- assinatura e chave fail-closed;
- self-link/redirects;
- índice de evidências canônico e relatórios portáveis;
- CI remoto verificável.

## Gate

`HG-RUN-SEC-01` permanece risco histórico externo. Não usar nem testar o valor antigo. Ele não autoriza interrupção antecipada da rodada.