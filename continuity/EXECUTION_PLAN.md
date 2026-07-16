# Plano de execução local

## Política

- branch única `master`;
- um commit por rodada;
- mesmo `Round-ID` para trabalho cross-repo;
- maior unidade coerente possível até bloqueio real;
- implementação somente após baseline persistido.

## WP-00 — Bootstrap MAESTRO

Status: `DONE`.

## WP-01B — Auditoria baseline Runner

Status: `NEXT`.

Saídas:

1. inventário estrutural e de lifecycle;
2. matriz versão × arquitetura × assets;
3. mapeamento Runner/helper images;
4. fluxo de tokens e redaction;
5. integração Docker/executor;
6. testes e workflows;
7. divergência upstream;
8. lacunas e backlog derivado.

Critério de saída: fatos por path/commit, desconhecidos explícitos e nenhuma implementação misturada.

## WP-02A — Fonte de verdade de release

Status: `PLANNED`.

Definir fonte oficial, regra de stable release, asset matching, autenticidade e falhas.

## WP-02B — Resolver atômico Runner/helper images

Status: `PLANNED`.

Resolver todos os assets da mesma versão e rejeitar conjunto incompleto ou incompatível.

## WP-02C — Gerador determinístico

Status: `PLANNED`.

Atualizar manifest/fixtures em ordem estável, com URLs e SHA256, sem escrita parcial.

## WP-02D — Testes unitários e negativos

Status: `PLANNED`.

Cobrir release inválida, asset ausente, hash divergente, arquitetura incompleta, mismatch de versão, rede, idempotência e determinismo.

## WP-02E — Lifecycle

Status: `PLANNED`.

Validar install, service, registration, executor/helper image, upgrade, backup/restore e remove em ambiente controlado.

## WP-02F — Automação recorrente

Status: `PLANNED`.

Criar rotina que detecta versão elegível, gera mudança e produz evidência, sem publicar automaticamente release de produção.

## WP-09 — Manutenção contínua

Status: `PLANNED`.

Monitorar drift, compatibilidade com GitLab, YunoHost/Debian, deprecações de token/executor e releases.