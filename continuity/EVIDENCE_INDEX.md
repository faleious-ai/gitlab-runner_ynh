# Índice de evidências — RND-20260716-007

| ID | Estado | Path | Resultado |
|---|---|---|---|
| EVD-WP02-ONLINE-DISCOVERY | VERIFIED | `evidence/wp02-online-discovery.json` | API oficial paginada selecionou v19.2.0 e registrou observed_at/origem |
| EVD-WP02-CHECKSUM-TRUST | VERIFIED | `evidence/wp02-checksum-trust.json` | quatro hashes confrontados e assinatura release.sha256.asc verificada |
| EVD-WP02-OFFLINE-FIXTURE | VERIFIED | `evidence/wp02-candidate-report.json` | snapshot v19.0.1 separado da descoberta corrente, sem promoção |
| EVD-WP02-MANIFEST-CANDIDATE | VERIFIED | `evidence/wp02-manifest-diff.json` | cópia completa em staging e nove campos allowlisted |
| EVD-WP02-TOKEN-NOT-IN-ARGV | VERIFIED | `tests/test_autoupdate.py` | fake não encontrou token em argv/stdout/stderr |
| EVD-WP02-YUNOHOST-ACTION | VERIFIED | `config_panel.toml`, `scripts/config` | contrato atual main.registration.register |
| EVD-WP02-TESTS-CI | VERIFIED | `.github/workflows/validation.yml` | workflow_dispatch, SHA pins, testes, scanner, parsing, Bash e diff guard |

`HG-RUN-SEC-01` continua `UNRESOLVED_NO_AUTHORITY`. Nenhum claim de aceite é feito neste índice.
