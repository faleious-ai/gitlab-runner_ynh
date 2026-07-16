# Rodada ativa

Charter-ID: `CHR-WP02-002`  
Estado: `READY`  
Preparado em: 2026-07-16  
Orquestrador: ChatGPT com o Maestro Diretor  
Executor principal: Codex  
Unidade: `WP-02 Correção — confiança, manifest candidato e registro seguro`

## Autorização

`Leia AGENTS.md e continue` autoriza a execução integral deste charter. Atribua novo `Round-ID`, conclua todo trabalho não bloqueado e publique um commit em `origin/master` por repositório afetado, com o mesmo identificador.

## Revisão anterior

`CHR-WP02-001` recebeu `CORRECTION_REQUIRED`. Registro: `continuity/reviews/REV-RND-20260716-005.md`.

Preserve as partes demonstradas: remoção da credencial da árvore atual, scanner, redaction, helper compartilhado, validação prévia das listas, matriz Runner/helper, escrita atômica auxiliar, testes existentes e ausência de promoção.

## Objetivo

Completar descoberta oficial, proveniência dos checksums, geração da cópia candidata do manifest, transporte seguro da credencial de registro, contrato atual da action YunoHost e CI verificável. Não promover versão nesta rodada.

## Escopo

### T1 — Descoberta e origem

- integrar modo de descoberta/refresh pela Releases API do projeto oficial;
- tratar paginação, timeout, retries, limite de resposta, JSON inválido e schema alterado;
- selecionar semanticamente a release estável elegível mais recente;
- validar exatamente projeto, API, release page, host de downloads, tag e redirects;
- distinguir fixture offline, snapshot e candidata corrente;
- registrar momento e fonte da observação.

### T2 — Checksums confiáveis

- buscar o documento oficial de checksums da mesma tag;
- interpretar e exigir exatamente os assets necessários para amd64, arm64, armhf e helper images;
- confrontar os hashes do catálogo com a fonte oficial;
- rejeitar ausência, duplicidade, tag/filename divergente e hash incompatível;
- verificar assinatura oficial quando tecnicamente disponível ou documentar estratégia equivalente de recálculo integral;
- criar fixtures offline para parser e falhas negativas sem baixar assets grandes no CI.

### T3 — Manifest candidato

- ler o `manifest.toml` real e produzir em staging uma cópia candidata completa;
- alterar somente versão, URLs e hashes dos sources Runner/helper e documentação gerada autorizada;
- exigir matches únicos e abortar em estrutura inesperada;
- produzir diff determinístico e relatório machine-readable dos campos alterados;
- dry-run por padrão e escrita somente para destino explícito fora do manifest rastreado;
- manter `manifest.toml` em `18.6.2~ynh1` nesta rodada.

### T4 — Registro seguro e action YunoHost

- retirar a credencial da linha de comando usando o mecanismo de ambiente suportado pelo Runner;
- provar por fake que ela não aparece em argumentos, stdout, stderr ou tracing;
- manter validação completa antes do primeiro subprocesso;
- demonstrar com fonte primária/teste qual mecanismo de action é suportado por YunoHost `>= 12.1.17`;
- migrar para config panel/controller atual quando o legado não for suportado, ou documentar e testar o suporte legado;
- manter um único entry point compartilhado por install, restore e action.

### T5 — Testes e CI

Cobrir API paginada, stable/pre-release, fixture stale, origem inesperada, redirect não permitido, checksum ausente/duplicado/divergente, assinatura/trust inválido, manifest inesperado, diff fora da allowlist, determinismo, idempotência, ausência de escrita parcial, credencial fora de argv e contrato de action.

No workflow:

- adicionar `workflow_dispatch`;
- manter permissões read-only, sem commit/branch/PR;
- fixar ações externas por SHA completo;
- executar testes, scanner, parsing, Bash, dry-run e diff guard;
- obter execução remota verificável ou registrar objetivamente a causa de `UNVERIFIED`.

### T6 — Evidência e coordenação

- revisar ou substituir ADR-0006;
- produzir relatórios separados de descoberta online, confiança dos checksums, fixture offline e diff do manifest;
- não reduzir a especificação para encaixar a implementação;
- atualizar status, handoff, active round, evidence index e round record;
- publicar síntese no coordenador com o mesmo `Round-ID`.

## DAG paralelo

### Onda 1

- Frente A: T1 — API, freshness e allowlists.
- Frente B: T2 — checksums, assinatura e fixtures.
- Frente C: T3 — manifest candidato e diff guard.
- Frente D: T4 — registro e action YunoHost.
- Frente E: T5 — testes e CI.

Subagentes não fazem commit. Cada frente possui ownership de outputs temporários; arquivos canônicos compartilhados são integrados apenas pelo executor principal.

### Gate de integração

Reconciliar interfaces, executar testes focais, confirmar ausência de segredo e de hash sem proveniência, validar que o manifest rastreado não mudou e resolver contradições.

### Onda 2

Executar descoberta oficial, atualizar fixture/relatórios sem promoção, rodar suíte completa e CI quando disponível, atualizar memória/evidência e publicar os dois repositórios.

## Fora de escopo

Promover versão, registrar/remover Runner real, usar a credencial histórica, executar operação destrutiva em produção, publicar release, criar branch/PR/worktree, force push, reescrever histórico ou alterar ruleset/licença/visibilidade.

## Gate humano

`HG-RUN-SEC-01` permanece `UNRESOLVED_NO_AUTHORITY`, como risco histórico externo. Não bloqueia este charter. Nenhuma pergunta humana adicional é necessária.

## Definition of Done

- descoberta online usa somente a fonte oficial e seleciona a release estável elegível mais recente;
- fixture possui provenance e freshness explícitas;
- hashes são confrontados com checksum oficial ou conteúdo recalculado;
- origem, redirects, tags e filenames falham fechados;
- generator produz cópia completa do manifest e diff limitado;
- manifest rastreado permanece em `18.6.2~ynh1`;
- credencial não aparece em argv ou outputs;
- action segue contrato YunoHost demonstrado;
- testes passam e CI remoto tem evidência ou estado `UNVERIFIED` honesto;
- todos os itens não bloqueados terminam;
- um commit remoto por repositório, mesmo `Round-ID`, `HEAD == origin/master` e árvores limpas;
- saída `EXECUTED_AWAITING_REVIEW`.

## Pacote de revisão

Entregar SHAs completos, URLs remotas, matriz tarefa-output-evidência, fontes oficiais, relatórios, comandos/resultados, testes, CI, decisão da action, prova de credencial fora de argv, limitações e estado do gate. Não declarar `ACCEPTED`.
