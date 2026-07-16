# Rodada ativa

Charter-ID: `CHR-WP02-001`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Unidade: `WP-02 — Segurança e fundação determinística do autoupdate do Runner`

## Autorização

`Leia AGENTS.md e continue` autoriza a execução integral deste charter. O Codex deve atribuir um novo `Round-ID`, concluir todo o trabalho não bloqueado e usar o mesmo identificador no coordenador `faleious-ai/gitlab_ynh` quando houver escrita cross-repo.

## Revisão anterior

`CHR-WP01-001` foi `ACCEPTED`. Registro: `continuity/reviews/REV-RND-20260716-003.md`.

## Objetivo

Remediar o risco de credencial na árvore atual, tornar a action `register` coerente e testável e implementar um updater determinístico que trate os binários Runner e helper images como uma unidade atômica. A rodada não promove versão nem registra Runner real.

## Escopo completo

### S1 — Fixture e prevenção de segredo

- remover de `tests.toml` o literal credential-like sem reproduzi-lo em commit, log ou documentação;
- substituir por entrada segura compatível com testes, preferencialmente secret/env efêmero ou placeholder que faça o cenário ser explicitamente não executável sem provisionamento;
- adicionar secret scan automatizado para árvore e fixtures;
- testar redaction de comandos, logs e erros relacionados a token;
- documentar que o valor histórico deve ser tratado como exposto até revogação/expiração confirmada.

### S2 — Registro administrativo

- pesquisar a versão atual do contrato de actions YunoHost e registrar fontes/rationale;
- corrigir `actions.json` e implementar `scripts/actions/register`, ou remover a action se a plataforma atual não a suportar, com atualização consistente de docs e testes;
- evitar duplicação: install, restore e action devem reutilizar uma única função/entry point de registro;
- validar que listas de URL/token/imagem têm cardinalidade consistente;
- falhar sem registro parcial quando uma entrada for inválida;
- não imprimir token; reduzir exposição por argumento de processo quando houver mecanismo suportado pelo Runner;
- criar testes com stub/fake do binário `gitlab-runner`, sem rede nem credencial real.

### U1 — Fonte e proveniência

- selecionar uma fonte oficial para release estável e assets;
- registrar ADR com critérios de stable/pre-release, versão mínima, timeout, retries, proveniência e falha fechada;
- criar fixtures offline versionadas sem incluir segredos;
- não confiar apenas em existência HTTP de asset.

### U2 — Resolver atômico

- resolver exatamente uma versão para amd64, arm64, armhf e helper images;
- exigir que todos os assets pertençam à mesma release;
- obter checksums oficiais quando disponíveis ou baixar/recalcular SHA256 com tamanho/limites controlados;
- rejeitar asset ausente, duplicado, arquitetura inesperada, helper incompatível e checksum inválido;
- produzir catálogo machine-readable da resolução.

### U3 — Generator determinístico

- implementar dry-run/check como padrão e write explícito;
- gerar alterações em staging temporário e substituir o conjunto apenas após validação completa;
- limitar o diff a versão, URLs, SHA256 e documentação gerada autorizada;
- garantir determinismo e idempotência;
- não alterar `manifest.toml` para uma versão candidata nesta rodada;
- produzir relatório de drift/candidata sem promoção.

### A1 — Testes e CI

Cobrir no mínimo:

- release estável e pre-release;
- asset ausente/duplicado;
- mismatch Runner/helper;
- amd64/arm64/armhf;
- checksum divergente;
- timeout/retry/rede indisponível;
- staging e ausência de escrita parcial;
- determinismo/idempotência;
- action target existente;
- cardinalidade de registro;
- redaction e secret scan;
- manutenção do baseline quando executado em dry-run.

Adicionar workflow de CI compatível com `master` que execute validações e drift check sem criar branch, PR ou commit automático.

## DAG paralelo

### Onda 1

- Frente A — S1: fixture segura, secret scan e redaction.
- Frente B — S2: contrato YunoHost, action e helper compartilhado de registro.
- Frente C — U1: fonte, proveniência, ADR e fixtures.
- Frente D — U2/U3: resolver e generator.
- Frente E — A1: suíte de testes e CI.

Subagentes não fazem commit. Cada frente recebe ownership de paths; arquivos compartilhados são alterados somente pelo executor principal durante integração.

### Gate de integração 1

- reconciliar interfaces e schemas;
- garantir que nenhum segredo esteja no diff ou outputs;
- executar testes focais de cada frente;
- resolver contradições antes da integração final.

### Onda 2

- integrar updater ao manifest em dry-run;
- executar a suíte completa;
- produzir relatório da candidata sem promoção;
- atualizar docs, ADR, evidências e continuidade;
- atualizar o coordenador com o mesmo `Round-ID`.

## Fora de escopo

- usar, testar ou reproduzir o valor histórico;
- registrar ou remover Runner real;
- executar contra GitLab de produção;
- promover versão candidata no manifest;
- publicar release;
- reescrever histórico, force push, branch, PR ou worktree;
- executar `unregister --all-runners` fora de ambiente efêmero;
- alterar ruleset, visibilidade, licença ou fork network.

## Gate humano

`HG-RUN-SEC-01`: o administrador do projeto GitLab usado pelo package_check deve confirmar revogação, rotação ou expiração do valor histórico.

O Codex não possui autorização para usar o valor ou verificar sua validade por autenticação. O gate não bloqueia S1, S2, U1, U2, U3 ou A1. Antes de declarar `BLOCKED_HUMAN`, todo o restante deve estar concluído e em estado seguro.

## Outputs obrigatórios

- código do updater/resolver/generator;
- implementação ou remoção justificada da action;
- helper compartilhado de registro;
- fixtures e testes;
- workflow CI read-only;
- ADR de release/proveniência;
- documentação de segurança, uso e limitações;
- relatório de drift/candidata sem promoção;
- `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, `EVIDENCE_INDEX` e round record;
- síntese cross-repo no coordenador.

## Definition of Done

- nenhum credential-like literal permanece na árvore atual ou nos novos outputs;
- secret scan e testes de redaction passam;
- action e target são consistentes, ou a remoção foi justificada e todos os contratos atualizados;
- fluxo de registro compartilhado é testado sem rede/segredo;
- resolver exige conjunto completo Runner/helper da mesma versão;
- generator é determinístico, idempotente, atômico e dry-run por padrão;
- nenhuma versão candidata foi promovida;
- CI e suíte local passam, ou limitações ambientais estão explicitamente separadas;
- documentação e evidências correspondem ao comportamento demonstrado;
- todos os itens não bloqueados foram concluídos;
- um commit em `master` neste repositório e, se atualizado, um no coordenador, ambos com o mesmo `Round-ID`;
- saída `EXECUTED_AWAITING_REVIEW`, ou `BLOCKED_HUMAN` apenas após todo o trabalho independente.

## Pacote de revisão

Entregar commits, matriz tarefa → output → evidência, comandos, testes, coverage relevante, diff de segurança, decisão da action, proveniência, relatório de candidata, limitações, riscos residuais e estado de `HG-RUN-SEC-01`. Não declarar `ACCEPTED`.