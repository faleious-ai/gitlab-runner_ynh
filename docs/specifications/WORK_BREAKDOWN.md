# Divisão do trabalho local

| ID | Unidade | Depends | Gate | Saída |
|---|---|---|---|---|
| WP-00 | Bootstrap MAESTRO | — | A | estrutura de continuidade |
| WP-01B-01 | Inventário de arquivos e manifest | WP-00 | A | baseline estrutural |
| WP-01B-02 | Lifecycle scripts/service | 01 | A | mapa install/upgrade/etc. |
| WP-01B-03 | Tokens, registration e segurança | 02 | B | threat/lifecycle map |
| WP-01B-04 | Docker/executor/helpers | 02 | B | compatibility map |
| WP-01B-05 | Testes e workflows | 01 | A | assurance gap report |
| WP-01B-06 | Divergência upstream | 01 | A | drift matrix |
| WP-01B-07 | Backlog derivado | 03/04/05/06 | B | plano executável |
| WP-02A | Fonte de release | WP-01B | B | ADR + fixtures |
| WP-02B | Resolver de assets Runner | 02A | A | matriz completa |
| WP-02C | Resolver helper images | 02A | B | unidade compatível |
| WP-02D | Gerador determinístico | 02B/02C | A | alteração atômica |
| WP-02E | Testes unitários/negativos | 02D | A | suíte do updater |
| WP-02F | Lifecycle controlado | 02E | B/C para produção | evidência operacional |
| WP-02G | Automação recorrente | 02F | B | detecção e commit |
| WP-09 | Monitoramento de drift | WP-02 | B | manutenção contínua |

## Gate classes

- `A`: decisão técnica autônoma.
- `B`: autonomia com ADR/evidência reforçada.
- `C`: aprovação humana antes da ação.

## Definition of Done da auditoria

- todos os scripts e resources inventariados;
- lifecycle descrito sem inferência não marcada;
- tokens/privilegios mapeados;
- relação Runner/helper images explicada;
- testes atuais e ausentes registrados;
- divergências upstream classificadas;
- backlog derivado com critérios;
- status, handoff, evidence e round record atualizados.

## Definition of Done do updater

- fonte oficial e schema tratados;
- todos os assets obrigatórios resolvidos;
- hashes verificados;
- Runner/helper images atômicos;
- output determinístico e idempotente;
- falha sem escrita parcial;
- testes positivos/negativos;
- lifecycle proporcional;
- documentação e evidência.

## Regra de granularidade

Executar a maior unidade coerente possível. Não criar uma rodada por arquivo; dividir apenas por dependência, risco, ambiente ou gate real.