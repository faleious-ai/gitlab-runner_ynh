# Learning ledger

Append-only registry for failures, dead ends and process lessons that must survive context resets. This file complements, but does not duplicate, `STATUS`, `HANDOFF_CURRENT`, round records or the evidence index.

## Entry schema

| Field | Required content |
|---|---|
| Backprop-ID | `BP-YYYYMMDD-NNN` |
| Round/Task | source `Round-ID` and `Task-ID` |
| classification | implementation bug, criterion gap, requirement gap, environment, dependency or process gap |
| pattern | stable category used to detect recurrence |
| symptom | exact observed failure, without secrets |
| root cause | technical cause, not merely failed command |
| contract change | criterion/invariant/interface/process amendment, or `none` with reason |
| RED | command/oracle and observed failing result |
| GREEN | command/oracle and observed passing result |
| commit | final task SHA when available |
| systemic action | none, candidate task or required human decision |

## Entries

### BP-20260716-001

| Field | Value |
|---|---|
| Backprop-ID | `BP-20260716-001` |
| Round/Task | `RND-20260716-010` / `T-WP02D-01-config-controller` |
| classification | `PROCESS_GAP` |
| pattern | task-start review ordering |
| symptom | O teste RED do seam de configuração foi criado antes do registro formal do pre-build challenge. |
| root cause | A retomada priorizou criar o oracle público para medir o baseline antes de persistir a revisão adversarial; a ordem documental da skill não foi aplicada explicitamente. |
| contract change | Antes do primeiro edit de cada tarefa de alto impacto, registrar GO/NO_GO, seam, invariantes, gates e rollback no round record ou saída versionada; só então criar o oracle RED. |
| RED | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_config_controller -v` — falhou por inputs ausentes e por `unknown GitLab Runner config action`. |
| GREEN | O mesmo comando após a implementação — 2 testes passaram. |
| commit | pendente até a publicação de T01 |
| systemic action | nenhuma; aplicar a ordem em T02–T08 |

### BP-20260716-002

| Field | Value |
|---|---|
| Backprop-ID | `BP-20260716-002` |
| Round/Task | `RND-20260716-010` / `T-WP02D-01-config-controller` |
| classification | `INCOMPLETE_CRITERION` |
| pattern | stale public seam in regression harness |
| symptom | A suíte existente falhou com `FileNotFoundError` porque invocava `scripts/config` sem dispatch e esperava logs do fake Runner. |
| root cause | O oracle herdado exercitava a interface CLI legada, enquanto o contrato ativo exige o controlador `run__register()` do ConfigPanel. |
| contract change | Testes de registro devem invocar o seam público vigente; a remoção de interfaces legadas fica explicitamente em `T-WP02D-02`. |
| RED | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` — 15 passaram e `test_registration_redaction_never_returns_token` falhou antes de criar `argv.log`. |
| GREEN | O mesmo comando após migrar o harness — suíte completa passa. |
| commit | pendente até a publicação de T01 |
| systemic action | nenhuma; auditar seams herdados nas tarefas seguintes |

### BP-20260716-003

| Field | Value |
|---|---|
| Backprop-ID | `BP-20260716-003` |
| Round/Task | `RND-20260716-010` / `T-WP02D-06-evidence-portability` |
| classification | `INCOMPLETE_CRITERION` |
| pattern | heterogeneous evidence report schema |
| symptom | O primeiro teste de portabilidade levantou `KeyError: 'release'` ao tratar `wp02-checksum-trust.json`, que é um relatório resumido sem o objeto `release`. |
| root cause | O oracle assumiu que todos os JSONs de evidência compartilhavam o schema de relatório completo do updater; o índice contém artefatos completos e resumidos. |
| contract change | O scanner deve percorrer campos opcionais por schema e validar cada assinatura disponível, sem exigir estrutura de relatório que o artefato não declara. |
| RED | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_evidence_portability -v` — erro `KeyError: 'release'` antes dos asserts de confiança. |
| GREEN | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_evidence_portability -v` — 4 testes passaram após tratar schemas resumidos e corrigir os artefatos portáveis. |
| commit | pendente até a publicação de T06 |
| systemic action | nenhuma; manter testes schema-aware para evidência |

## Rules

- Never delete entries. Corrections append a superseding note.
- Never reproduce credentials, tokens or sensitive payloads.
- One unexpected failure produces one entry; do not bulk unrelated failures.
- Expected RED in a planned TDD slice is not logged unless it exposes an unmodeled gap.
- Three entries in the same pattern category require a dedicated systemic task proposal.
- Link large logs/evidence rather than copying them here.
- `STATUS` records current state; this ledger records why a failed approach must not be repeated.
