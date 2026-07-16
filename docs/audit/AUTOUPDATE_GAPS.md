# Lacunas de autoupdate — GitLab Runner YunoHost

Round-ID: RND-20260716-003
Estado: baseline; nenhuma correção implementada

As observações desta seção registram o baseline anterior à rodada
`RND-20260716-005`. O delta executado e suas provas estão em
`docs/autoupdate/README.md`, `evidence/wp02-candidate-report.json` e no índice
de evidências.

## Mecanismo atual

Não existe .github/workflows, script updater ou gerador ativo no snapshot.
manifest.toml contém somente comentários de autoupdate para o source main.
O source images está fixado manualmente, com a observação de que a estratégia
automática ainda não é conhecida.

A atualização atual é, portanto, uma edição manual coordenada de:

1. versão do manifest;
2. três URLs e SHA256 do Runner;
3. URL e SHA256 do helper images;
4. README/badge gerado;
5. scripts ou fixtures quando a release exigir compatibilidade.

O install e o upgrade consomem o source resolvido pelo YunoHost; nenhum deles
consulta latest em runtime.

## Lacunas observadas

| ID | Severidade | Evidência | Lacuna e consequência |
|---|---|---|---|
| RUN-AU-01 | P0 | tests.toml:17-22 | fixture contém literal com aparência de token Runner. O valor está no histórico público e precisa ser removido/rotacionado se ainda for válido; não foi usado nem reproduzido aqui. |
| RUN-AU-02 | P0 | manifest.toml:67-80 | autoupdate do binário está comentado e helper images não têm resolver, regra de compatibilidade ou fixture. Atualizar somente o binário pode quebrar jobs. |
| RUN-AU-03 | P1 | actions.json:1-6; árvore do repositório | ação register aponta para scripts/actions/register, caminho inexistente. A operação declarada não é executável no snapshot. |
| RUN-AU-04 | P1 | scripts/install:41-73; scripts/upgrade:18-33 | Docker é reiniciado automaticamente e o pacote tem acesso ao executor Docker; não há prova de matriz Debian/arquitetura nem threat test para socket/privilégios. |
| RUN-AU-05 | P1 | scripts/backup:7-17; scripts/restore:12-47 | backup não declara arquivos; restore depende de parâmetros/token para registrar novamente. Persistência de config, identidade e segredo não está demonstrada. |
| RUN-AU-06 | P1 | scripts/remove:16 | remove executa unregister --all-runners sem confirmação ou gate explícito, com efeito remoto potencialmente destrutivo. |
| RUN-AU-07 | P2 | manifest.toml:94-96 | repositório Docker é fixado em bullseye, sem matriz explícita para a distribuição real do host YunoHost. |
| RUN-AU-08 | P2 | manifest.toml:55; actions.json:45 | default docker_image é alpine:latest. O pacote é fixado, mas o job runtime não é reproduzível por digest/tag imutável. |
| RUN-AU-09 | P2 | tests.toml | não há testes do resolver, helper images, hashes, idempotência, redaction, registration sem vazamento ou job Docker mínimo. |
| RUN-AU-10 | P2 | README.md:31-39 | instruções referenciam o fluxo testing do upstream, não o master-only da fork; continuidade operacional fica ambígua. |

## Candidata observada, sem promoção

Refs públicos do upstream de produto mostraram v19.2.0. Os URLs
versionados para amd64, arm64, armhf e helper images responderam HTTP 200 no
levantamento. Isso prova disponibilidade HTTP, não elegibilidade: ainda
faltam SHA256, compatibilidade, conteúdo do helper package, mudanças de
registration e lifecycle.

## Backlog ordenado

| Ordem | Unidade | Dependências | Critério observável |
|---:|---|---|---|
| 1 | RUN-SEC-01: retirar fixture de credencial e definir rotação/redaction | decisão sobre validade do valor pode exigir gate humano | nenhum segredo/credential-like literal em fixtures, histórico operacional tratado e logs redigidos |
| 2 | WP-02A: resolver release oficial | baseline atual | release estável, assets por arquitetura e metadados de proveniência em fixture |
| 3 | WP-02B: resolver Runner + helper atomicamente | WP-02A | mesma versão, todos os assets obrigatórios, hashes verificados e falha sem escrita parcial |
| 4 | WP-02C: gerador de manifest | WP-02B | saída determinística/idempotente, diff limitado a campos permitidos e README gerado coerente |
| 5 | RUN-AU-03: reparar ou remover ação declarada | contrato de ação YunoHost | target existe, schema e comando concordam, token é password e logs/processos não o expõem |
| 6 | WP-02D: lifecycle/assurance | WP-02B/02C | install, upgrade, backup/restore, registration, job Docker e remove em ambiente efêmero |
| 7 | RUN-AU-04/07/08: matriz Docker e reprodutibilidade | WP-02D | distribuição suportada explicitamente, imagem default documentada/pinada e threat model aprovado |

## Fora desta rodada

Não foram alterados versão, URLs, hashes, token fixture, scripts, ação,
Docker ou comportamento de instalação. A próxima rodada deve tratar o
achado P0 de credencial antes de promover uma release.
