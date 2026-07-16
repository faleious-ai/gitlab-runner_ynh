# Rodada ativa

Charter-ID: `CHR-WP01-001`  
Estado: `EXECUTED_AWAITING_REVIEW`
Round-ID: `RND-20260716-003`
Orquestrador: ChatGPT com o Maestro Diretor  
Executor: Codex  
Unidade local: `WP-01B — Auditoria baseline Runner`

## Invocação

`Leia AGENTS.md e continue` autoriza este charter. O mesmo `Round-ID` deve ser usado no repositório coordenador quando a sessão possuir acesso aos dois.

## Perguntas prévias

Nenhuma pergunta humana adicional é necessária: a rodada é investigativa, reversível e não modifica comportamento.

## Objetivo

Produzir baseline verificável do pacote Runner, lifecycle, segurança de tokens, Docker/executor, relação Runner/helper images, divergência upstream, gaps de autoupdate e backlog derivado.

## Escopo

- manifest, sources, arquiteturas e assets;
- scripts install/upgrade/remove/backup/restore/config/change-url existentes;
- service e configuração;
- registration/authentication token lifecycle e redaction;
- executor Docker, dependências e helper images;
- testes, workflows e documentação;
- upstream/divergência;
- riscos, desconhecidos, gaps de assurance e backlog.

## Fora de escopo

Implementar updater, mudar versão/hash/URL, usar token real, registrar Runner em produção, criar mirror, alterar ruleset ou publicar release.

## DAG paralelo

### Onda 1

- A: manifest, sources, arquiteturas e matriz de assets.
- B: scripts, service, config e lifecycle.
- C: tokens, redaction e modelo de segurança.
- D: Docker/executor/helper images.
- E: testes, workflows, docs e upstream.

Subagentes não fazem commit e não editam arquivos canônicos compartilhados sem ownership.

### Integração

O Codex reconcilia fatos, paths e versões; resolve contradições e identifica lacunas.

### Onda 2

- baseline consolidado;
- divergência upstream;
- gaps de autoupdate;
- mapa lifecycle/segurança;
- backlog com dependências e critérios.

## Outputs

- `docs/audit/RUNNER_PACKAGE_BASELINE.md`;
- `docs/audit/UPSTREAM_DIVERGENCE.md`;
- `docs/audit/AUTOUPDATE_GAPS.md`;
- `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md`;
- status, handoff, evidence index e round record.

## Definition of Done

Todos os itens possuem path/fonte e estado de verificação; matrizes não omitem combinações; desconhecidos estão explícitos; nenhuma implementação foi misturada; backlog tem critérios; coordenação cross-repo foi atualizada quando acessível; commit em `master`; estado `EXECUTED_AWAITING_REVIEW`.

## Bloqueio

Somente segredo indispensável, operação irreversível, mudança de missão/licença/visibilidade, consequência material de privilégio ou fonte indispensável inacessível após tentativas. Antes de parar, concluir todas as frentes independentes.

## Fechamento da execução

As frentes de inventário, lifecycle, tokens/redaction, Docker/helper images,
testes/workflows/docs e upstream foram concluídas. Foram produzidos:

- docs/audit/RUNNER_PACKAGE_BASELINE.md
- docs/audit/UPSTREAM_DIVERGENCE.md
- docs/audit/AUTOUPDATE_GAPS.md
- docs/audit/LIFECYCLE_AND_SECURITY_MAP.md

O pacote funcional não foi alterado. Versão, URLs, hashes, scripts,
actions.json, Docker e fixtures permaneceram iguais ao HEAD de entrada.
Validações estáticas passaram; package_linter e lifecycle real permanecem
UNVERIFIED por limitações ambientais.

Foi registrado um achado P0 em tests.toml:21: literal com aparência de token.
O valor não foi usado ou reproduzido. A ação register também tem falha
estrutural porque o target declarado não existe.

Não há bloqueio humano ativo. Estado de saída:
EXECUTED_AWAITING_REVIEW.
