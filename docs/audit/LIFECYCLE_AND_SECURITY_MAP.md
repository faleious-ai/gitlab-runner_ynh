# Mapa de lifecycle e segurança — GitLab Runner YunoHost

Round-ID: RND-20260716-003
Estado: baseline auditado estaticamente

## Fluxo operacional

| Evento | Caminho | Efeitos principais | Verificação atual |
|---|---|---|---|
| Install | scripts/install | normaliza listas, garante Docker, instala Runner/helper, registra Runners, checksum e serviço | bash/TOML; runtime UNVERIFIED |
| Upgrade | scripts/upgrade | garante Docker, instala dois assets, workaround dpkg para <17.7, serviço | bash/TOML; runtime UNVERIFIED |
| Backup | scripts/backup | não declara arquivo; depende do comportamento padrão do YunoHost | leitura estática; persistência UNVERIFIED |
| Restore | scripts/restore | reinstala dois assets, registra novamente, checksum e serviço | leitura estática; sem token real |
| Remove | scripts/remove | remove serviço, unregister all-runners, pacote e /etc/gitlab-runner | não executado por ser destrutivo |
| Ação register | actions.json | chama scripts/actions/register como root | FAILED: arquivo ausente |

## Delta WP-02 — estado após RND-20260716-005

O literal credential-like da fixture foi removido e substituído por um
placeholder não funcional. `scripts/secret_scan.py` cobre a árvore atual e
`scripts/_register.sh` redige tokens em diagnósticos. A ação agora possui
target, valida cardinalidade antes do primeiro registro e é reutilizada por
install e restore. O lifecycle real e a validade do valor histórico continuam
sem prova; `HG-RUN-SEC-01` permanece aberto.

## Fluxo de credenciais

1. manifest.toml solicita gitlab_url, token e docker_image; token está tipado
   como string em manifest.toml:42-48.
2. actions.json tipa token como password, mas a ação aponta para um script
   inexistente.
3. install recebe token e o passa a gitlab-runner register como argumento em
   scripts/install:62-73.
4. O Runner grava sua configuração em /etc/gitlab-runner/config.toml; o
   repositório não demonstra redaction, rotação ou backup seguro.
5. restore repete o registro com os mesmos parâmetros em scripts/restore:28-39.
6. remove executa unregister --all-runners em scripts/remove:16.

O token de fixture em tests.toml:21 não é repetido neste documento. Ele é
credential-like e deve ser tratado como exposto até prova de expiração.

## Riscos priorizados

| ID | Nível | Condição | Consequência | Prova necessária |
|---|---|---|---|---|
| RUN-R-01 | P0 | token literal público em fixture | abuso/registro remoto se ainda válido | revogação ou expiração confirmada, remoção e secret scan |
| RUN-R-02 | P0 | token em argumento de processo e registro | exposição em process listing/logs de erro | teste de redaction e inspeção de processos |
| RUN-R-03 | P1 | helper image separado sem resolver atômico | incompatibilidade Runner/helper em job | fixture de release e job Docker real |
| RUN-R-04 | P1 | Docker socket/daemon reiniciado e executor root | superfície privilegiada no host | threat model, permissões e isolamento |
| RUN-R-05 | P1 | backup vazio e restore por re-registro | perda/duplicação de identidade ou segredo | backup/restore com token efêmero e estado esperado |
| RUN-R-06 | P1 | unregister all-runners no remove | ação remota destrutiva fora de gate | teste em namespace efêmero e confirmação explícita |
| RUN-R-07 | P2 | imagem alpine:latest | jobs não determinísticos | política de tag/digest e documentação |
| RUN-R-08 | P2 | Docker repo bullseye fixo | instalação incompatível em outro Debian | matriz YunoHost/Debian/arquitetura |
| RUN-R-09 | P2 | serviço só é adicionado, não aguardado/verificado | instalação pode terminar com Runner inoperante | health check e job mínimo pós-lifecycle |

## Cobertura atual versus necessária

| Área | Estado | Lacuna |
|---|---|---|
| Sintaxe | VERIFIED | não substitui package_linter |
| Assets | HTTP 200 e hashes com forma válida | falta recálculo de hashes e conteúdo |
| Registration | código lido, nenhum token usado | falta token efêmero e redaction |
| Executor Docker | configuração declarada | falta job mínimo e ameaça do socket |
| Upgrade | workaround de versão observado | falta matriz de origem/destino |
| Backup/restore | scripts observados | persistência real não provada |
| Remove | código observado | não executar sem ambiente efêmero/gate |
| Ação | JSON válido | target ausente, falha estrutural |
