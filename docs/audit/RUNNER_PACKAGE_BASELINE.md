# Baseline verificável do pacote GitLab Runner YunoHost

Round-ID: RND-20260716-003
Charter: CHR-WP01-001
Snapshot: master em 00db3a0d455db06f54305fef13d6ea596ad6967e
Data da inspeção: 2026-07-16
Estado: EXECUTED_AWAITING_REVIEW

## Resultado executivo

O pacote declara GitLab Runner 18.6.2~ynh1 para amd64, arm64 e armhf. A
instalação e o restore instalam dois artefatos: o pacote Debian do Runner e
um pacote único de helper images. Depois registram um ou mais Runners contra
uma URL, token e imagem Docker, usando executor docker.

A fork é funcionalmente idêntica ao snapshot de
YunoHost-Apps/gitlab-runner_ynh. As adições locais são apenas documentação e
governança MAESTRO. O maior risco observado é de segurança e não de sintaxe:
tests.toml contém um literal com aparência de token na linha 21 e a cadeia de
registro passa o token como argumento de processo. O valor não foi usado,
copiado ou reproduzido nesta auditoria.

## Identidade e recursos

| Campo | Fato observado | Evidência |
|---|---|---|
| ID/formato | gitlab-runner, packaging format 2 | manifest.toml:3-10 |
| YunoHost/helpers | YunoHost >= 12.1.17; helpers 2.1 | manifest.toml:20-23 |
| Arquiteturas | amd64, armhf, arm64 | manifest.toml:20-24 |
| Recursos declarados | 50M de disco, build e runtime | manifest.toml:29-31 |
| Executor padrão | docker | scripts/install:9-12 |
| APT | ca-certificates, git, curl, tar | manifest.toml:86-92 |
| Docker externo | repositório bullseye, chave e docker-ce/docker-ce-cli/containerd.io | manifest.toml:94-96 |
| Ação declarada | register, executada como root | actions.json:1-12 |

## Matriz de assets

| Source ID | Artefato | Arquiteturas | Versão | Fixação |
|---|---|---|---|---|
| main | gitlab-runner.deb | amd64, arm64, armhf | 18.6.2 | URL S3 versionada e SHA256 por arquitetura |
| images | gitlab-runner-images.deb | pacote único | 18.6.2 | URL S3 versionada e SHA256 único |

Os três URLs do Runner, o URL do helper images e os quatro hashes possuem
forma válida. Requisições HEAD aos quatro assets retornaram HTTP 200 no
momento da auditoria. Não houve download nem recálculo dos hashes nesta
rodada.

O bloco autoupdate do source main está comentado e diz que a estratégia
latest_gitlab_release e os assets por arquitetura ainda não estão habilitados
(manifest.toml:67-71). O source images registra explicitamente que não há
estratégia automática conhecida e usa format = whatever
(manifest.toml:73-80).

## Arquivos e responsabilidades

| Área | Arquivos | Responsabilidade |
|---|---|---|
| Contrato | manifest.toml, actions.json, tests.toml | fontes, perguntas, ação administrativa e cenários package_check |
| Entrada/registro | scripts/install | normalização de listas, Docker, instalação e registro |
| Upgrade | scripts/upgrade | Docker, sources, workaround dpkg < 17.7 e serviço |
| Backup/restore | scripts/backup, scripts/restore | backup padrão vazio; reinstalação e novo registro |
| Remoção | scripts/remove | serviço, unregister all-runners, pacote e /etc/gitlab-runner |
| Helpers | scripts/_common.sh | backup de ação e restauração em falha |
| Documentação | README.md, doc/ADMIN.md, doc/DESCRIPTION.md | operação e origem upstream |

actions.json aponta para /bin/bash scripts/actions/register, mas o caminho
scripts/actions/register não existe no snapshot. A definição JSON é válida;
a implementação declarada não está presente.

## Mapa de lifecycle observado

### Install

scripts/install acrescenta vírgulas às três entradas para representar listas,
guarda executor=docker, reinicia Docker se necessário, instala os dois
packages e executa gitlab-runner register para cada tripla
URL/token/docker_image. Depois guarda checksum de /etc/gitlab-runner/config.toml
e registra o serviço YunoHost. Evidência: scripts/install:9-94.

### Upgrade

scripts/upgrade remove uma configuração antiga, reinicia Docker, instala
Runner e helper images e usa --force-overwrite quando o pacote instalado é
anterior a 17.7.0. Não há espera explícita pela saúde do serviço nem teste de
job após o upgrade. Evidência: scripts/upgrade:7-47.

### Backup

scripts/backup não declara arquivo com ynh_backup; imprime apenas a mensagem de
conclusão. O comentário afirma que o YunoHost copiará os arquivos, mas não há
prova no repositório de que config.toml, identidade ou tokens sejam
persistidos com segurança. Evidência: scripts/backup:7-17.

### Restore

scripts/restore reinstala os dois assets, reexecuta registro para cada URL,
token e imagem recebidos, recalcula checksum de config.toml e adiciona o
serviço. Isso pode criar novas identidades ou registros duplicados se a
configuração original não for restaurada antes da operação. Evidência:
scripts/restore:7-60.

### Remove

scripts/remove remove o serviço, executa unregister --all-runners, remove o
pacote e apaga /etc/gitlab-runner. unregister --all-runners é uma operação
externa com efeito em todos os Runners daquele host; não há confirmação,
namespace de teste ou gate no script. Evidência: scripts/remove:7-26.

## Verificações realizadas

| Verificação | Resultado |
|---|---|
| Parsing TOML de manifest e tests | VERIFIED |
| Parsing JSON de actions.json | VERIFIED |
| bash -n em todos os scripts | VERIFIED |
| Forma dos quatro hashes e URLs | VERIFIED estruturalmente |
| HEAD dos três binários Runner | VERIFIED, HTTP 200 |
| HEAD do helper images | VERIFIED, HTTP 200 |
| package_linter | UNVERIFIED: ambiente sem jsonschema |
| install/upgrade/registration/backup/restore/remove | UNVERIFIED: sem host YunoHost, Docker e token efêmero |
| ação register | FAILED estruturalmente: target scripts/actions/register ausente |

## Limitações

Não foi usado token, não foi registrado Runner e não foi executada operação
contra GitLab. O estado de persistência da configuração e o comportamento
exato do backup padrão precisam ser demonstrados em ambiente controlado.
