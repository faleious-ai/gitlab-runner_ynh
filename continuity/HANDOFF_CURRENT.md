# Handoff atual

Estado: `READY_FOR_WP_01B`  
Round anterior: `RND-20260716-001`  
Branch: `master`

## Retomada mínima

1. Leia `AGENTS.md`.
2. Confirme HEAD de `master`.
3. Leia `continuity/STATUS.md`.
4. Leia `WP-01B` em `continuity/EXECUTION_PLAN.md`.
5. Consulte `RUNNER_AUTOUPDATE_SPEC.md` apenas para identificar dados que a auditoria precisa levantar.

## Próxima unidade executável

### WP-01B — Inventário do pacote Runner

Produzir:

- `docs/audit/RUNNER_PACKAGE_BASELINE.md`;
- `docs/audit/UPSTREAM_DIVERGENCE.md`;
- `docs/audit/AUTOUPDATE_GAPS.md`;
- `docs/audit/LIFECYCLE_AND_SECURITY_MAP.md`.

Cobrir:

- manifest e sources;
- scripts install/upgrade/remove/backup/restore/config/change-url se existentes;
- service e configuração do Runner;
- registration/authentication token lifecycle;
- executor Docker e dependências;
- runner/helper-images compatibility;
- architectures;
- testes e workflows;
- divergências do upstream YunoHost;
- dados desconhecidos e riscos.

## Coordenação

Ao concluir, atualizar `faleious-ai/gitlab_ynh` com uma síntese cross-repo usando o mesmo `Round-ID`, se a sessão possuir acesso de escrita aos dois repositórios.

## Fora de escopo

- implementar updater;
- modificar versão;
- registrar Runner real em produção;
- usar token real;
- criar mirror;
- alterar ruleset.

## Condições de parada

Escalar somente por segredo ausente necessário, operação irreversível, mudança de missão/licença/visibilidade, impacto material de privilégio ou impossibilidade comprovada de acessar uma fonte indispensável.

## Fechamento

Um único commit em `master` com auditoria, status, handoff, evidence index e round record.