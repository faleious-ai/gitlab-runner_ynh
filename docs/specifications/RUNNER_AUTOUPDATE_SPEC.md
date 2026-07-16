# Especificação do autoupdate GitLab Runner

Status: `PLANNED`  
Work package: `WP-02`

## Objetivo

Descobrir a versão estável elegível mais recente do GitLab Runner e gerar atualização atômica, reproduzível e testável do pacote principal e de suas helper images para todas as arquiteturas declaradas.

## Entradas

- versão atual do manifest;
- fonte oficial de releases;
- assets Runner por arquitetura;
- pacote/helper images correspondente;
- distribuições e arquiteturas suportadas;
- templates/scripts atuais;
- regras de compatibilidade e registro.

## Saídas

- versão proposta do pacote YunoHost;
- URLs versionadas do Runner por arquitetura;
- URL/pacote helper images da mesma versão compatível;
- SHA256 de todos os assets;
- diff determinístico;
- relatório de compatibilidade, testes e falhas;
- evidência de provenance.

## Resolução atômica

Uma versão só é elegível quando:

1. é release estável;
2. possui assets Runner para amd64, arm64 e armhf enquanto essas arquiteturas permanecerem declaradas;
3. possui helper images compatíveis e identificáveis;
4. todos os assets têm URL estável e hash verificável;
5. o conjunto corresponde à mesma versão sem ambiguidade;
6. a versão é compatível com o ambiente YunoHost/Debian suportado ou a incompatibilidade é tratada explicitamente.

Ausência em qualquer célula obrigatória aborta sem escrever arquivos.

## Algoritmo normativo

1. ler baseline e matriz;
2. consultar fonte oficial;
3. excluir pre-releases, releases revogadas ou incompatíveis;
4. selecionar candidata;
5. resolver assets Runner por arquitetura;
6. resolver helper images correspondentes;
7. verificar versão, tamanho, URL e SHA256;
8. gerar alterações em ordem estável;
9. validar coerência em manifest/scripts/templates/fixtures;
10. executar testes unitários e negativos;
11. executar lifecycle proporcional;
12. persistir evidência e commit de rodada.

## Invariantes

- runtime não consulta `latest`;
- nenhuma arquitetura fica sem asset;
- Runner/helper images não divergem;
- falha de rede ou parse não deixa diff parcial;
- repetição contra mesma release não produz diff;
- tokens nunca aparecem em fixtures/logs persistidos;
- registration flow segue semântica suportada pela versão alvo;
- rollback do pacote preserva ou trata explicitamente configuração/identidade.

## Casos de teste unitário

- release válida completa;
- pre-release ignorada;
- asset Runner ausente por arquitetura;
- helper images ausentes;
- mismatch de versão;
- hash divergente;
- redirect/URL inesperada;
- erro de rede;
- schema upstream alterado;
- execução repetida idempotente;
- output determinístico;
- manifest incoerente detectado;
- nenhuma escrita parcial.

## Lifecycle mínimo

### Install

- pacote instalado;
- serviço criado e estado esperado;
- Docker/dependências disponíveis conforme contrato;
- config sem segredo exposto.

### Registration

- usar token efêmero em ambiente controlado;
- verificar configuração resultante;
- redigir logs;
- considerar mudanças upstream entre registration token e runner authentication token.

### Job/executor

- executar job mínimo Docker;
- demonstrar uso/obtenção de helper image compatível;
- capturar sucesso e falha diagnóstica.

### Upgrade

- preservar configuração e identidade conforme contrato;
- validar serviço e job após upgrade;
- testar caminho de versão anterior suportada.

### Backup/restore

- declarar exatamente o que é persistido;
- restaurar sem vazar token;
- verificar serviço e configuração.

### Remove

- remover serviço e recursos conforme política;
- não revogar/desregistrar produção sem gate explícito;
- tratar dados persistentes conforme contrato YunoHost.

## Segurança

- secrets somente por variável/secret store efêmero;
- redaction de token, headers e config sensível;
- logs de teste publicados devem ser inspecionados;
- Docker socket e executor são superfície privilegiada e exigem threat analysis em WP-01/02.

## Critério de aceite

WP-02 fecha quando o updater é determinístico, idempotente, falha fechado, cobre todos os assets, possui testes positivos/negativos e demonstra lifecycle proporcional com evidência indexada.