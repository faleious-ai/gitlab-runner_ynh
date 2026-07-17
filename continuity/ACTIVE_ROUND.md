# Rodada ativa

Charter-ID: `CHR-WP02-004`  
Estado: `READY`  
Preparado em: 2026-07-17  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Unidade: `WP-02E — confiança live, proveniência e fechamento consistente`

## Autorização

`Leia AGENTS.md e continue` autoriza a execução integral deste charter, tarefa por tarefa, conforme ADR-0006 e as skills locais atualizadas em `RND-20260717-011`.

Atribua novo `Round-ID`. Cada tarefa concluída gera um commit atômico publicado em `origin/master` antes da próxima tarefa que escreva neste repositório.

Baseline: resolver `origin/master` no START e confirmar que contém:

- revisão `continuity/reviews/REV-RND-20260716-010.md`;
- process backprop commit `4cefe926732c95344c3d7d129aa9dbe110dcae72`;
- estado `CHR-WP02-004 READY` nos dois repositórios.

## Revisão anterior

`CHR-WP02-003`, executado em `RND-20260716-010`, recebeu `CORRECTION_REQUIRED`.

Preservar integralmente:

- `run__register()` e inputs efêmeros;
- credencial fora do argv e redaction;
- remoção de `scripts/actions/register`;
- backup/restore sem re-registro;
- falha fechada para estados GPG/GPGV adversos;
- self-link e paths exatos de release/assets;
- manifest candidato completo e diff allowlist;
- workflow read-only com actions por SHA;
- `manifest.toml` em `18.6.2~ynh1`.

## Objetivo

Tornar o caminho live de confiança compatível com a entrega oficial atual sem abrir a fronteira de origem, produzir evidência nova e verificável pelo código corrigido, reparar a semântica dos artefatos históricos, alinhar o default Docker e fechar continuidade/CI sem overclaim.

## Tarefas

### `T-WP02E-01-official-key-transport`

Resultado: o updater consome a chave oficial pela cadeia de entrega atual e continua fail-closed.

- Dependências: nenhuma.
- Seam: `discover_current()` → `_official_fetch(OFFICIAL_KEY_URL, "key", ...)` → GPG/GPGV.
- Pesquisa obrigatória: consultar documentação oficial GitLab e observar o redirect atual do URL fixado; registrar host/path final sem copiar query efêmera para documentos permanentes.
- Claims:
  - URL inicial permanece exatamente o endpoint oficial `packages.gitlab.com`;
  - redirects são HTTPS, limitados e aceitos somente em allowlist explícita de host/path oficial observada;
  - destinos privados, IP literal, host/path divergente e excesso de redirects falham antes do consumo;
  - bytes finais são confrontados com o fingerprint fixado antes de sustentar confiança;
  - `gpgv` ainda decide assinatura/expiração/revogação; documentação não substitui o verificador;
  - diagnósticos não registram conteúdo da chave, query efêmera ou saída sensível.
- RED: fixture sanitizada da cadeia oficial atual é rejeitada pelo baseline com `unexpected key origin`.
- GREEN: a mesma cadeia atravessa o transport, fingerprint é conferido e casos adversos falham fechado.
- Paths: `scripts/autoupdate.py`, fixtures/testes de transport e documentação técnica estritamente necessária.
- Evidência alvo: `LOCAL_VERIFIED`.
- Pre-build challenge: obrigatório.
- Rollback: reverter somente este commit.

### `T-WP02E-02-live-trust-observation`

Resultado: uma nova observação live é gerada pelo commit funcional T01 já publicado.

- Dependência: T01 remoto e `HEAD == origin/master`.
- Seam: CLI público `scripts/autoupdate.py discover` com rede/GPG reais.
- Claims:
  - usa exatamente o SHA publicado de T01;
  - produz novo artefato versionado, sem editar semanticamente relatórios antigos;
  - registra `producer_commit`, comando, `observed_at`, URL inicial, final host/path sanitizado, hash do documento da chave/checksum, fingerprint, validade/status e limitações;
  - resultado real pode ser `verified`, `failed` ou `unverified-environment`; nenhum estado é forçado;
  - chave expirada/revogada, assinatura inválida ou entrega incompatível impede `generate --refresh`;
  - não promove manifest nem baixa os pacotes completos.
- TDD: mudança comportamental `NOT_APPLICABLE`; é uma observação pós-commit. Validar schema/proveniência por teste antes de persistir.
- Paths: novo artefato em `evidence/`, evidence index e teste de schema/proveniência.
- Evidência alvo: conforme resultado real, nunca acima dele.
- Rollback: remover somente o novo artefato e sua indexação.

### `T-WP02E-03-historical-evidence-repair`

Resultado: evidência antiga recupera sua semântica original e é supersedida honestamente.

- Dependência: T02 remoto, mesmo que o resultado live seja falha ou limitação.
- Seam: auditoria de provenance sobre `evidence/*.json` e histórico Git.
- Claims:
  - recuperar de Git as versões anteriores a T06 dos relatórios observados em RND-20260716-007, ou preservar cópia histórica equivalente;
  - remover factualidade acrescentada manualmente sem nova execução;
  - marcar relatórios anteriores `SUPERSEDED` ou manter seu nível original;
  - o novo artefato T02 é a única fonte para o estado live atual;
  - testes falham quando `valid/verified/passed` não possuem produtor, comando e observação correspondentes;
  - nenhuma evidência histórica é apagada silenciosamente.
- RED: teste de provenance demonstra que os relatórios atuais contêm campo factual adicionado por tarefa sem rede.
- GREEN: índice e artefatos distinguem observação antiga, supersessão e nova observação.
- Paths: `evidence/`, `tests/test_evidence_portability.py` ou teste dedicado, learning ledger somente por novo finding.
- Evidência alvo: `LOCAL_VERIFIED` para a reparação documental.
- Rollback: reverter somente este commit.

### `T-WP02E-04-docker-default-consistency`

Resultado: config panel e instalação não divergem silenciosamente no default da imagem Docker.

- Dependências: nenhuma.
- Seam: parser do `manifest.toml` + parser do `config_panel.toml` + controller harness.
- Decisão técnica autorizada: usar default versionado consistente com o install (`alpine:3.20`) ou remover o default e exigir input explícito; escolher a opção mais simples e justificar no round record.
- Claims:
  - nenhum default mutável `latest` é introduzido pelo pacote;
  - action e install têm comportamento consistente ou diferença explicitamente documentada/testada;
  - token/argv e controller permanecem inalterados.
- RED: contrato detecta `alpine:latest` no panel versus `alpine:3.20` no manifest.
- GREEN: contrato e controller passam com a decisão escolhida.
- Paths: `config_panel.toml`, testes focais e documentação mínima.
- Evidência alvo: `LOCAL_VERIFIED`.
- Rollback: reverter somente este commit.

### `T-WP02E-05-remote-ci-observation`

Resultado: CI do SHA funcional final é observado ou classificado objetivamente.

- Dependências: T01–T04 publicados.
- Seam: workflow `Validation` associado ao SHA de T04 ou ao último commit funcional aplicável.
- Claims:
  - workflow continua read-only e actions permanecem fixadas por SHA;
  - consultar run/status pelo SHA correto;
  - se o ambiente não recuperar run, registrar `UNVERIFIED` com mecanismo/limitação exatos;
  - não criar sucesso presumido, não alterar settings/ruleset e não reexecutar indefinidamente;
  - executar localmente todos os comandos equivalentes como nível separado.
- TDD: `NOT_APPLICABLE`, salvo correção real do workflow.
- Paths: evidência CI e workflow somente se finding demonstrado.
- Rollback: reverter somente o commit documental ou funcional desta tarefa.

### `T-WP02E-06-integration-gates`

Resultado: intervalo funcional corrigido passa os gates integrados sem promoção.

- Dependências: T01–T05 concluídos ou bloqueados validamente.
- Seam: suíte completa, secret scan, parsers, Bash, updater offline, live result T02, candidate diff e lifecycle harness.
- Claims:
  - manifest permanece `18.6.2~ynh1`;
  - nenhuma credencial, registro real ou operação destrutiva ocorreu;
  - todos os commits de tarefa são lineares, remotos e seletivamente reversíveis;
  - P1-F01, P1-F02, P2-F03 e P2-F04 possuem resolução rastreável;
  - nenhum P0/P1 interno permanece aberto.
- TDD: `NOT_APPLICABLE` para a integração; reexecutar oracles das tarefas.
- Paths: relatório de integração e, somente se necessário, correção demonstrada via backprop.
- Rollback: reverter somente este commit de integração.

### `T-WP02E-07-final-continuity`

Resultado: estado final usa somente commits já publicados e fica pronto para revisão externa.

- Dependência: T06 remoto.
- Seam: reconciliação GitHub dos dois `master` e memória canônica.
- Claims:
  - status, handoff, active round, evidence index, learning ledger e round record concordam;
  - matriz Task-ID→SHA→claim→evidência usa SHAs finais T01–T06;
  - nenhuma frase future/pending descreve commit já publicado;
  - o próprio commit T07 pode ser identificado como `this task commit`; o coordenador, publicado depois do Runner, registra o SHA Runner T07 real;
  - CI/lifecycle permanecem no nível efetivamente observado;
  - saída é `EXECUTED_AWAITING_REVIEW`, nunca `ACCEPTED`.
- TDD: contrato documental/parsing e auditoria de contradição.
- Paths: continuidade/evidência no Runner e síntese no coordenador.
- Rollback: reverter T07 no coordenador e Runner conforme dependência explícita.

## DAG

Onda 1 paralela: T01 e T04.  
Onda 2: T02 após T01.  
Onda 3: T03 após T02; T05 após T01–T04.  
Onda 4 sequencial: T06.  
Onda 5 sequencial: T07 Runner, depois T07 coordenador.

Subagentes podem pesquisar/testar frentes independentes, sem commit ou ownership de arquivos canônicos. O Executor integra e publica uma tarefa por vez.

## Fora de escopo

- promover qualquer versão candidata;
- registrar Runner real;
- usar/testar credencial histórica;
- ampliar hosts/paths por wildcard genérico;
- confiar em documentação como substituto de GPG/GPGV;
- editar settings/rulesets do GitHub;
- branch, PR, worktree, squash, force push ou reescrita;
- implementação MCP.

## Gate humano

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY` e não bloqueia as tarefas. Nenhuma nova decisão humana é necessária.

## Definition of Done

- T01–T07 concluídas ou bloqueadas conforme contrato;
- cadeia oficial da chave coberta por RED/GREEN e resultado live pós-commit;
- evidência histórica não contém factualidade retrospectiva;
- default Docker consistente/reproduzível;
- manifest sem promoção;
- nenhum P0/P1 aberto;
- commits remotos por tarefa e pacote final revisável.

## Pacote de revisão

Entregar baselines, SHAs completos por Task-ID, RED/GREEN, live artifact/provenance, resolução de cada finding, gates integrados, CI/lifecycle, riscos, `HG-RUN-SEC-01`, confirmação dos HEADs e paths remotos. Não declarar `ACCEPTED`.
