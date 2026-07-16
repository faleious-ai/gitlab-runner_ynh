# Contexto canônico

## Propósito

Este repositório mantém o empacotamento YunoHost do GitLab Runner. Seu foco é o lifecycle seguro do Runner e a atualização coordenada do binário com `gitlab-runner-helper-images`.

## Relações

- Repositório: `faleious-ai/gitlab-runner_ynh`.
- Upstream do pacote: `YunoHost-Apps/gitlab-runner_ynh`.
- Upstream do produto: `gitlab-org/gitlab-runner` no GitLab.
- Coordenador temporário do programa: `faleious-ai/gitlab_ynh`.
- Issue coordenadora do programa: `faleious-ai/gitlab_ynh#1`.
- Futuro responsável pelo MCP: `faleious-ai/gitlab-mcp`.

## Baseline observado

- versão declarada: `18.6.2~ynh1`;
- architectures: amd64, arm64 e armhf;
- package principal aponta para assets versionados;
- bloco de autoupdate está comentado;
- helper images usam versão fixa, mas não têm estratégia automática definida no baseline.

Esses fatos ainda devem ser confirmados por `WP-01B` com inventário completo e evidência por arquivo.

## Autoridades

- comportamento real: manifest, scripts, templates, configs e testes;
- contrato de autoupdate: `docs/specifications/RUNNER_AUTOUPDATE_SPEC.md`;
- rationale: ADRs e `continuity/DECISIONS.md`;
- estado atual: `continuity/STATUS.md`;
- retomada: `continuity/HANDOFF_CURRENT.md`;
- prova: `evidence/EVIDENCE_INDEX.md`;
- proveniência: round records e Git.

## Restrições permanentes

- branch única `master`;
- um commit por rodada;
- sem force push;
- sem segredos;
- sem `latest` dinâmico;
- sem atualização desacoplada de Runner/helper images;
- sem declarar executor funcional sem job real ou teste equivalente;
- master deve permanecer executável após cada commit.

## Continuidade

Um agente novo deve conseguir retomar lendo `AGENTS.md`, `HANDOFF_CURRENT.md` e `STATUS.md`, ampliando o contexto sob demanda. Chats são transitórios e não substituem arquivos versionados.