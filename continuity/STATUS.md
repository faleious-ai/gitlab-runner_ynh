# Status atual

Atualizado em: 2026-07-16  
Branch autorizada: `master`  
Última rodada executada pelo Codex: `RND-20260716-007`
Última rodada do orquestrador: `RND-20260716-006`

## Fase

`WP02_EXECUTED_AWAITING_REVIEW`

`CHR-WP02-002` foi executado no repositório funcional primário. O resultado permanece aguardando revisão independente; não é `ACCEPTED`.

## Entregas

- descoberta online paginada pela Releases API oficial, com allowlist de projeto, release page, downloads e redirects;
- seleção corrente `v19.2.0`, com observação UTC, tamanhos e origem registrados;
- fixture `v19.0.1` identificada como snapshot offline, com quatro hashes confrontados ao documento oficial;
- assinatura `release.sha256.asc` verificada com a chave oficial e fingerprint registrado;
- gerador de cópia completa do manifest com diff determinístico e allowlist de nove campos;
- `manifest.toml` preservado em `18.6.2~ynh1`;
- token fora de `argv`, stdout e stderr no fake, através de `CI_SERVER_URL`, `CI_SERVER_TOKEN` e `REGISTER_NON_INTERACTIVE`;
- action atual YunoHost em `config_panel.toml`/`scripts/config`, mantendo `_register.sh` compartilhado;
- workflow com `workflow_dispatch`, permissões read-only, actions por SHA completo e guardas de diff.

## Validações locais

`14/14` testes: PASS; secret scan: clean; Bash: PASS; JSON/TOML: PASS; dry-run e diff guard: PASS; manifest: `18.6.2~ynh1`; assinatura online: VERIFIED.

O workflow remoto foi preparado para execução após publicação; qualquer estado remoto será reportado sem ser inferido do CI local.

## Gate humano

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY` e não foi exercitado.
