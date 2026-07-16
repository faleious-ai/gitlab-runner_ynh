# Limites cross-repo

## Autoridade local

Este repositório é autoridade sobre:

- manifest e scripts do pacote Runner;
- versão do Runner e helper images;
- serviço, configuração, registration e executor;
- testes e evidências do lifecycle Runner;
- implementação do updater Runner.

## Autoridades externas

### `faleious-ai/gitlab_ynh`

Coordenação temporária do programa, pacote GitLab, políticas de upgrade GitLab e síntese cross-repo.

### futuro `faleious-ai/gitlab-mcp`

Servidor MCP, catálogo de API, tools, autorização e contract tests.

### upstream YunoHost

Referência do empacotamento comunitário. Divergências locais devem ser classificadas e justificadas.

### upstream GitLab Runner

Fonte de produto e releases. Mirror futuro é somente leitura.

## Coordenação

Mudança cross-repo usa o mesmo `Round-ID`, registra ordem dos commits e atualiza handoff de cada repositório. Cada repositório deve permanecer compreensível e seguro mesmo se o segundo commit falhar.

## Compatibilidade

A versão mais recente do Runner não é automaticamente a versão correta para qualquer GitLab, executor ou helper package. Compatibilidade deve ser demonstrada por fonte, teste ou matriz explícita.

## Drift monitorado

- fork vs upstream YunoHost;
- manifest vs release oficial;
- Runner vs helper images;
- pacote vs Debian/YunoHost suportados;
- registration flow vs mudanças upstream;
- Docker/executor vs dependências;
- status/handoff vs HEAD.