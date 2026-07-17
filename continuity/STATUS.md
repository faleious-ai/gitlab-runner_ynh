# Status atual

Atualizado em: 2026-07-17  
Branch autorizada: `master`  
Round-ID: `RND-20260717-012`
Fase: `WP02E_EXECUTED_AWAITING_REVIEW`

## Charter

`CHR-WP02-004 — confiança live, proveniência e fechamento consistente` foi executado pelo Codex em sete tarefas atômicas, com um commit remoto por tarefa. A revisão anterior `REV-RND-20260716-010` permanece registrada como `CORRECTION_REQUIRED`; suas correções aceitas foram preservadas.

## Matriz Task-ID → SHA → claim

| Task-ID | SHA publicado | Claim e estado |
|---|---|---|
| T-WP02E-01-official-key-transport | `6fb500ec3474c07137fcb8962512ed0adc59a9bb` | cadeia oficial capturada e allowlist fail-closed; `LOCAL_VERIFIED` |
| T-WP02E-02-live-trust-observation | `8c0c52592d2ccd3f9ebd706d56e63f9b12410f69` | falha no checksum antes da chave/GPG; trust `not-observed`; `UNVERIFIED` |
| T-WP02E-03-historical-evidence-repair | `ea9774001fbf181b5fc210a17fad6a1208a83d4c` | provenance histórica restaurada e supersedida; `LOCAL_VERIFIED` |
| T-WP02E-04-docker-default-consistency | `2563fc31e1b71db89315fd8c707235ed98659962` | defaults panel/install iguais a `alpine:3.20`; `LOCAL_VERIFIED` |
| T-WP02E-05-remote-ci-observation | `978ec18218e38920a169aa15490ec0cab4399133` | nenhum run/status remoto recuperado; `UNVERIFIED` |
| T-WP02E-06-integration-gates | `08563cbd2c957e6cca16ae6535a56ef9b2d52b9e` | 37 testes, lifecycle harness, gates offline e manifest inalterado; `LOCAL_VERIFIED` |
| T-WP02E-07-final-continuity | `this task commit` | arquivos canônicos reconciliados para revisão; `LOCAL_VERIFIED` |

## Estado preservado

- `manifest.toml`: `18.6.2~ynh1`, sem promoção;
- confiança live: não observada porque T02 falhou em `official-checksum-fetch` antes da chave/GPG;
- CI remoto: `UNVERIFIED` por `workflow_runs=[]`, `statuses=[]` e ausência de `gh`;
- lifecycle: harness local passou, host YunoHost/Docker real não observado;
- nenhum registro real, credencial histórica, download de pacote ou operação destrutiva foi usado;
- `HG-RUN-SEC-01`: `UNRESOLVED_NO_AUTHORITY`, não bloqueante.

## Evidência e revisão

Artefatos atuais: `evidence/wp02e-live-trust-observation.json`, `evidence/wp02e-remote-ci-observation.json` e `evidence/wp02e-integration-gates.json`. O índice canônico e o round record registram provenance, limitações e SHAs completos.

Estado final: `EXECUTED_AWAITING_REVIEW`. O executor não declara `ACCEPTED`; a revisão independente pertence ao orquestrador.
