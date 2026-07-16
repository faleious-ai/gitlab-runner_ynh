# Status atual

Atualizado em: 2026-07-16  
Branch autorizada: `master`  
Última rodada executada pelo Codex: `RND-20260716-007`  
Última rodada do orquestrador: `RND-20260716-008`

## Fase

`WP02_CORRECTION_REQUIRED_CHR003_READY`

A revisão independente de `CHR-WP02-002` resultou em `CORRECTION_REQUIRED`. A base de descoberta/checksums/manifest candidato é preservada, mas action, lifecycle, trust criptográfico, evidência canônica e CI remoto ainda não atendem ao contrato.

Registro: `continuity/reviews/REV-RND-20260716-007.md`.

## Charter ativo

`CHR-WP02-003 — Action, trust fail-closed e lifecycle seguro`.

Estado: `READY`.

## Correções obrigatórias

- implementar controlador YunoHost `run__register()` com entradas efêmeras;
- remover a interface legada que aceita credencial por argumentos;
- preservar configuração/identidade em backup/restore sem re-registro;
- falhar fechado em assinatura ou chave inválida/expirada/revogada;
- validar self-link/origem/redirects;
- restaurar `evidence/EVIDENCE_INDEX.md` como único índice canônico;
- remover paths locais dos relatórios;
- obter CI remoto verificável ou registrar bloqueio objetivo.

## Componentes preservados

- descoberta API paginada e stable-only;
- parser/confronto de checksums;
- manifest candidato completo e diff allowlist;
- ambiente do subprocesso principal sem credencial em argv;
- workflow read-only com actions por SHA;
- manifest `18.6.2~ynh1`, sem promoção.

## Gate humano

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY`. Não bloqueia `CHR-WP02-003`.