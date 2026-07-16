# Divergência contra upstream — GitLab Runner YunoHost

Round-ID: RND-20260716-003
Snapshot da fork: master em 00db3a0d455db06f54305fef13d6ea596ad6967e
Snapshot YunoHost-Apps: master em a4ac5b53a5c15546acde60d45616a7ecdb92cd3a

## Método e resultado

O fork e YunoHost-Apps/gitlab-runner_ynh foram clonados e comparados. O
merge-base é exatamente o HEAD atual do upstream comparado. Os arquivos
funcionais são iguais:

- manifest.toml, actions.json e tests.toml;
- scripts/_common.sh, install, upgrade, backup, restore e remove;
- documentação gerada do pacote e arquivos de licença.

A fork acrescenta apenas AGENTS.md, CONTEXT.md, continuity/, arquitetura,
ADRs, especificações e evidence/. Não há patch local do comportamento do
Runner.

## Classificação

| Classe | Fatos |
|---|---|
| Herdada | fontes v18.6.2, scripts de lifecycle, Docker bullseye, ação declarada e fixture de teste vêm do upstream YunoHost-Apps |
| Local deliberada | contratos MAESTRO, handoff, protocolos, ADRs e charter WP-01 |
| Atualização pendente | foram observados tags do upstream de produto até v19.2.0; os três assets binários e o helper image de v19.2.0 retornaram HTTP 200, mas nenhum hash foi resolvido nem alteração aplicada |
| Incompatibilidade de governança | README herdado orienta PRs para a branch testing do YunoHost-Apps, enquanto a fork opera exclusivamente em master |
| Falha herdada | actions.json aponta para scripts/actions/register ausente; o upstream de pacote auditado contém o mesmo estado |

## Histórico relevante

O histórico do upstream de pacote contém commits anteriores de auto-updater,
incluindo implementação e ajustes/reversão, mas o snapshot atual não possui
workflow ativo nem script de atualização no Runner. Essa diferença histórica
é evidência de tentativa anterior, não de capacidade atual demonstrada.

## Upstreams de produto

O pacote referencia gitlab-org/gitlab-runner e usa o bucket
gitlab-runner-downloads.s3.amazonaws.com para os binários. O upstream de
produto expôs o tag v19.2.0 no levantamento de refs. O helper image tem URL
separada e precisa ser resolvido como parte da mesma release.

Não foi feita comparação integral do código do grande repositório do produto;
foram comparados refs e assets públicos e a árvore do pacote YunoHost. A
proveniência e os SHA256 da candidata v19.2.0 continuam UNVERIFIED.

## Estado de branches

A fork auditada expõe apenas master e não possui tags publicadas. Não há
branch testing local para compatibilizar o README ou receber um PR automático.
