# Rodada ativa

Charter-ID: `CHR-WP02-003`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Unidade: `WP-02 Correção final — action, trust fail-closed e lifecycle seguro`

## Autorização

`Leia AGENTS.md e continue` autoriza a execução integral deste charter, tarefa por tarefa, conforme ADR-0006 e as skills locais. Atribua novo `Round-ID`. Cada tarefa concluída gera um commit atômico publicado em `origin/master` antes da próxima tarefa que escreva neste repositório.

Baseline: resolver `origin/master` no START e confirmar que contém integralmente `RND-20260716-009`, incluindo este charter, ADR-0006 e `.agents/skills/`.

## Revisão anterior

`CHR-WP02-002`, executado em `RND-20260716-007`, recebeu `CORRECTION_REQUIRED`. Registro: `continuity/reviews/REV-RND-20260716-007.md`.

Preserve descoberta paginada, allowlists de origem, parser/confronto de checksums, manifest candidato completo, diff allowlist, transporte principal por ambiente, SHA pins do workflow e ausência de promoção.

## Decisões de processo vigentes

- TDD obrigatório para toda mudança comportamental, inclusive shell/config/lifecycle;
- backprop técnico automático;
- challenge adversarial pré-build para tarefas de alto impacto;
- revisão pré-commit independente em Spec/Charter e Engineering/Security/Lifecycle;
- um commit remoto por tarefa, sem squash;
- compressão Caveman apenas em matrizes/ledgers;
- convergência medida por claims, gates, findings e bloqueios.

## Objetivo

Tornar a action realmente executável pelo YunoHost, eliminar interfaces legadas de credencial, preservar identidade em backup/restore sem senha persistida, fechar a verificação criptográfica, validar a origem canônica e reconciliar evidência/CI sem promover a versão candidata.

## Tarefas

### `T-WP02D-01-config-controller`

Resultado: botão YunoHost executa o registro seguro por controlador atual.

- Dependências: nenhuma.
- Seam: `scripts/config` carregado pelo contrato do config panel; chamada real `run__register()`.
- Claims:
  - função `run__register()` existe e chama somente `scripts/_register.sh`;
  - token é entrada efêmera `password` com `bind = "null"`;
  - URL/imagem são entradas efêmeras ou valores prepopulados com rationale;
  - nenhum segredo aparece em argv/log/output.
- RED: harness invoca o botão/controlador atual e falha no baseline pela ausência do caminho executável/inputs.
- GREEN: mesmo harness confirma helper, env seguro, redaction e erros.
- Paths: `config_panel.toml`, `scripts/config`, `scripts/_register.sh`, testes focais.
- Evidência alvo: `LOCAL_VERIFIED`.
- Pre-build challenge: obrigatório.

### `T-WP02D-02-remove-legacy-register`

Resultado: nenhum entry point legado aceita credencial por argumento.

- Dependência: `T-WP02D-01-config-controller` remoto.
- Seam: inventário de entry points + execução controlada dos caminhos remanescentes.
- Claims:
  - `scripts/actions/register` e referências associadas são removidos;
  - nenhum entry point recebe token posicional ou `--token`;
  - scanner e testes detectam regressão.
- RED: teste de contrato encontra o script/interface legada no baseline.
- GREEN: teste comportamental/inventário autorizado não encontra caminho e registro seguro continua funcional.
- Paths: interface legada, docs e testes correspondentes.

### `T-WP02D-03-lifecycle-identity`

Resultado: backup/restore preservam configuração e identidade sem re-registro.

- Dependências: nenhuma.
- Seam: invocação real de `scripts/backup` e `scripts/restore` em filesystem/harness temporário.
- Claims:
  - `/etc/gitlab-runner/config.toml` e paths necessários são preservados pelo contrato packaging v2;
  - restore não lê token, não chama register e restaura ownership/permissões adequadas;
  - install realiza registro inicial; upgrade/restore não regeneram identidade.
- RED: harness demonstra ausência de backup do config ou tentativa de registro no baseline.
- GREEN: backup→restore preserva identidade e não executa registro.
- Paths: `scripts/backup`, `scripts/restore`, install/upgrade somente quando necessário, testes.
- Pre-build challenge: obrigatório.

### `T-WP02D-04-signature-fail-closed`

Resultado: assinatura/chave inválida nunca é tratada como limitação ambiental.

- Dependências: nenhuma.
- Seam: resolver/updater público com adaptador GPG/GPGV controlado.
- Claims:
  - ferramenta ausente pode produzir `unverified-environment`, nunca `VERIFIED`;
  - ferramenta presente com retorno não zero, `VALIDSIG` ausente, fingerprint divergente, assinatura/chave expirada ou revogada falha fechado;
  - fingerprint é campo exato, não substring;
  - `generate --refresh` exige trust elegível;
  - validade observada da chave é registrada.
- RED: casos criptográficos adversos são aceitos/rebaixados no baseline.
- GREEN: todos falham com diagnóstico não secreto; ferramenta realmente ausente mantém classificação limitada.
- Paths: updater/resolver, fixtures GPG e testes.
- Pre-build challenge: obrigatório.

### `T-WP02D-05-source-self-link-redirects`

Resultado: release e assets permanecem dentro da origem oficial exata.

- Dependências: nenhuma.
- Seam: descoberta HTTP/API por adaptador controlado e live probe separado.
- Claims:
  - self-link/projeto/tag canônicos são confrontados;
  - release page/API oficial é comprovada;
  - redirects têm limite efetivo e cada destino é validado;
  - excesso, host/path não permitido e tag divergente falham fechado.
- RED: fixtures adversas atravessam ou não são rejeitadas pelo baseline.
- GREEN: matriz negativa é rejeitada e caminho oficial passa.
- Paths: discovery/network adapter, fixtures e testes.
- Pre-build challenge: obrigatório.

### `T-WP02D-06-evidence-portability`

Resultado: evidência canônica, portátil e sem overclaim.

- Dependências: T01–T05 publicados ou explicitamente independentes.
- Seam: `maestro-check` sobre evidence index, relatórios, paths e claims.
- Claims:
  - `evidence/EVIDENCE_INDEX.md` é o único índice funcional;
  - relatórios não contêm paths absolutos locais;
  - cada claim usa estado estrutural/local/CI/lifecycle correto;
  - RED/GREEN e backprop são rastreáveis por Task-ID/commit.
- TDD: contrato documental/parsing; comportamento funcional `NOT_APPLICABLE` com justificativa.
- Paths: evidence, relatórios, docs e testes de portabilidade.

### `T-WP02D-07-remote-ci`

Resultado: CI remoto do SHA funcional é observado ou bloqueio objetivo é registrado.

- Dependências: T01–T06 publicados.
- Seam: GitHub Actions run/status associado ao commit HEAD anterior à tarefa.
- Claims:
  - workflow permanece read-only e actions fixadas por SHA;
  - run é associado ao SHA correto e resultado final recuperado;
  - ausência de Actions/permissão é `UNVERIFIED`/bloqueio ambiental, nunca sucesso presumido.
- RED/GREEN: não se aplica a mutação comportamental; validar workflow localmente e observar execução remota.
- Paths: workflow somente se correção necessária, evidência CI e relatório.

### `T-WP02D-08-integration-continuity`

Resultado: rodada integrada, sem promoção e pronta para revisão externa.

- Dependências: T01–T07 concluídos ou bloqueados validamente.
- Seam: suíte completa, dry-run updater, lifecycle harness e intervalo remoto completo.
- Claims:
  - manifest permanece `18.6.2~ynh1`;
  - nenhuma credencial, registro real ou operação destrutiva ocorreu;
  - todas as tarefas têm commit remoto e rollback conhecido;
  - status, handoff, active round, learning ledger, evidence index e round record concordam;
  - matriz task→commit→claim→evidência está completa.
- Gates: parse/lint, suíte completa, secret scan, dry-run determinístico, lifecycle proporcional, revisão interna integrada e confirmação remota cross-repo.
- Paths: apenas continuidade/evidência/síntese cross-repo, salvo fix de integração demonstrado e registrado por backprop.

## DAG

Onda 1 paralela: T01, T03, T04, T05.  
Onda 2: T02 após T01; T06 após outputs funcionais estáveis.  
Onda 3: T07 após commits funcionais.  
Onda 4 sequencial: T08.

Subagentes recebem ownership exclusivo e não fazem commit. O executor integra e publica uma tarefa por vez.

## Fora de escopo

- promover qualquer candidata;
- registrar Runner real;
- usar/testar credencial histórica;
- reescrever histórico, force push, branch, PR ou worktree;
- unregister destrutivo;
- alterar ruleset, visibilidade ou licença;
- instalar runtime/hooks Cavekit.

## Gate humano

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY`. Não bloqueia nenhuma tarefa técnica. Nunca usar ou testar o valor histórico.

## Definition of Done integrada

- T01–T08 concluídas ou bloqueadas conforme protocolo;
- todos os comportamentos novos demonstram RED→GREEN no seam correto;
- nenhum P0/P1 interno aberto;
- commits de tarefa publicados e recuperáveis em ordem;
- manifest sem promoção;
- evidências honestas e portáveis;
- saída `EXECUTED_AWAITING_REVIEW` ou bloqueio válido após todo trabalho independente.

## Pacote de revisão

Entregar `baseline_head`, `round_head`, SHAs completos por Task-ID, matriz claim/prova, RED/GREEN, findings internos/resoluções, backprop, gates, lifecycle, CI, riscos, `HG-RUN-SEC-01`, confirmação de HEADs/árvores e paths remotos. Não declarar `ACCEPTED`.
