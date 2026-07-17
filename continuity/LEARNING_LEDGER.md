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
| commit | `ada6b78ca4db00c1dcacda4eb01736f123f6040b` |
| systemic action | nenhuma; aplicar a ordem em tarefas futuras |

### BP-20260716-002

| Field | Value |
|---|---|
| Backprop-ID | `BP-20260716-002` |
| Round/Task | `RND-20260716-010` / `T-WP02D-01-config-controller` |
| classification | `INCOMPLETE_CRITERION` |
| pattern | stale public seam in regression harness |
| symptom | A suíte existente falhou com `FileNotFoundError` porque invocava `scripts/config` sem dispatch e esperava logs do fake Runner. |
| root cause | O oracle herdado exercitava a interface CLI legada, enquanto o contrato ativo exige o controlador `run__register()` do ConfigPanel. |
| contract change | Testes de registro devem invocar o seam público vigente; a remoção de interfaces legadas fica explicitamente em tarefa própria. |
| RED | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` — 15 passaram e `test_registration_redaction_never_returns_token` falhou antes de criar `argv.log`. |
| GREEN | O mesmo comando após migrar o harness — suíte completa passa. |
| commit | `ada6b78ca4db00c1dcacda4eb01736f123f6040b` |
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
| contract change | O scanner deve percorrer campos opcionais por schema e validar cada assinatura disponível, sem exigir estrutura que o artefato não declara. |
| RED | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_evidence_portability -v` — erro `KeyError: 'release'`. |
| GREEN | O mesmo comando — 4 testes passaram após tratar schemas resumidos. |
| commit | `2acc1a3ec1a6c42a81eacea02f7ae093131070de` |
| systemic action | superseded em parte por `BP-20260717-005`: schema-aware não autoriza promoção factual |

### BP-20260717-004

| Field | Value |
|---|---|
| Backprop-ID | `BP-20260717-004` |
| Round/Task | `RND-20260717-011` / revisão de `T-WP02D-04` e `T-WP02D-05` |
| classification | `INTEGRATION_CRITERION_GAP` |
| pattern | mocked transport hides official redirect contract |
| symptom | O URL oficial da chave redireciona para CloudFront, mas `_official_endpoint(..., "key")` aceita somente igualdade com o URL inicial; o caller live rejeita a entrega antes do GPG. |
| root cause | Os testes criptográficos mockaram `_official_fetch`, e a matriz de redirects não capturou a cadeia específica da chave oficial. |
| contract change | Mudança de transporte externo exige teste RED/GREEN da cadeia oficial capturada e live probe pós-commit; mocks permanecem apenas para parser/falhas isoladas. |
| RED | inspeção integrada: endpoint oficial redireciona para host/path não aceito pelo validator atual; nenhum teste cobre essa cadeia. |
| GREEN | pendente em `CHR-WP02-004`. |
| commit | esta retropropagação normativa; SHA mapeado no round record |
| systemic action | tarefa funcional dedicada à entrega oficial da chave |

### BP-20260717-005

| Field | Value |
|---|---|
| Backprop-ID | `BP-20260717-005` |
| Round/Task | `RND-20260717-011` / revisão de `T-WP02D-06` |
| classification | `PROCESS_GAP` |
| pattern | schema completion promoted historical evidence |
| symptom | T06 acrescentou `key_validity = "valid"` a relatórios observados em RND-20260716-007 sem nova execução live. |
| root cause | O teste de portabilidade tratou presença coerente de campos como suficiente, sem verificar provenance/producer commit da observação. |
| contract change | Evidência observada é semanticamente imutável; nova factualidade exige novo artefato versionado e supersessão explícita do anterior. |
| RED | diff de T06 mostra inserção manual do estado `valid` enquanto o round record declara tarefa documental e sem rede. |
| GREEN | skills `maestro-check`, `maestro-tdd` e `REVIEW_PROTOCOL` passam a proibir promoção retrospectiva; reparação dos artefatos fica em `CHR-WP02-004`. |
| commit | esta retropropagação normativa; SHA mapeado no round record |
| systemic action | teste de provenance obrigatório para evidência live |

### BP-20260717-006

| Field | Value |
|---|---|
| Backprop-ID | `BP-20260717-006` |
| Round/Task | `RND-20260717-011` / revisão de `T-WP02D-08` |
| classification | `PROCESS_GAP` |
| pattern | final continuity written before final SHAs existed |
| symptom | Handoff e evidence index mantiveram futuro/pending e HEADs anteriores ao commit T08 depois da publicação. |
| root cause | A continuidade final foi preparada dentro do mesmo commit cujo SHA deveria registrar, sem etapa posterior de reconciliação por commit já publicado. |
| contract change | Síntese final deve referenciar commits já publicados; quando o próprio commit é alvo, usar tarefa posterior de fechamento ou referência verificável a `this task commit` resolvida em novo artefato. |
| RED | revisão remota encontrou “será”/“será consolidado” e pre-T08 heads no estado final. |
| GREEN | pendente na tarefa de continuidade de `CHR-WP02-004`. |
| commit | esta retropropagação normativa; SHA mapeado no round record |
| systemic action | separar integração funcional de fechamento final de continuidade |

## Rules

- Never delete entries. Corrections append a superseding note.
- Never reproduce credentials, tokens or sensitive payloads.
- One unexpected failure produces one entry; do not bulk unrelated failures.
- Expected RED in a planned TDD slice is not logged unless it exposes an unmodeled gap.
- Three entries in the same pattern category require a dedicated systemic task proposal.
- Link large logs/evidence rather than copying them here.
- Observed evidence is immutable in meaning; schema edits cannot invent factual results.
- `STATUS` records current state; this ledger records why a failed approach must not be repeated.
