# Protocolo de revisão

## Fronteira remota

O ChatGPT revisa somente charter, commits, diffs, evidências e validações publicados no GitHub. Estado exclusivamente local não é revisável.

`EXECUTED_AWAITING_REVIEW` exige:

1. `baseline_head` e `round_head` completos;
2. todos os commits de tarefa publicados em `origin/master` e recuperáveis;
3. sequência ordenada `Task-ID → commit SHA → outputs → claims → evidências`;
4. continuidade com o mesmo `Round-ID`/`Charter-ID`;
5. paths remotos existentes e ausência de links locais;
6. HEADs local/remoto coincidentes em todos os repositórios afetados.

Sem isso, o estado é `NOT_REVIEWABLE_REMOTE_SYNC_REQUIRED`, derivado de tarefa local ou sincronização bloqueada. Isso não julga a qualidade técnica.

## Entrada

O pacote de revisão inclui:

- charter e baseline remoto;
- lista ordenada de Task-IDs e SHAs completos;
- matriz claim → seam → teste/comando → resultado → estado de evidência;
- evidência RED/GREEN de mudanças comportamentais;
- findings das duas revisões internas e resolução;
- classificação de CI, lifecycle e limitações;
- backprop e riscos residuais.

## Revisão por tarefa

Para cada commit de tarefa, o orquestrador:

1. confirma `Task-ID`, escopo e dependências;
2. verifica atomicidade e ausência de trabalho não relacionado;
3. compara o diff com claims, interfaces e invariantes;
4. exige teste comportamental no seam público quando aplicável;
5. confirma RED anterior e GREEN posterior, ou justificativa de não aplicabilidade;
6. verifica segurança, lifecycle, compatibilidade, reversibilidade e ausência de segredo;
7. confirma que claims não excedem o nível de evidência;
8. avalia se a reversão isolada do commit preserva estado coerente ou se dependências estão explicitadas.

## Revisão integrada

Após os commits individuais, o orquestrador revisa `baseline_head...round_head` para detectar:

- interação defeituosa entre tarefas;
- regressão causada por sequência de commits;
- interfaces divergentes;
- outputs órfãos de subagentes;
- inconsistência cross-repo;
- documentação, status ou evidência que não reflitam o código final;
- lacunas que testes focais não alcançam.

## Dois eixos obrigatórios

O veredito mantém separados:

1. **Spec/Charter:** requisito ausente, parcial, errado, scope creep, claim sem prova ou interface divergente.
2. **Engineering:** bug, segurança, lifecycle, compatibilidade, qualidade, simplicidade, operabilidade e reversibilidade.

Uma tarefa pode passar em um eixo e falhar no outro. Um eixo não mascara o outro.

## Estados de evidência

- `STRUCTURALLY_OBSERVED`: presença ou forma inspecionada; não demonstra execução.
- `LOCAL_VERIFIED`: comando comportamental executado localmente com resultado reproduzível.
- `REMOTE_CI_VERIFIED`: run remoto associado ao SHA e resultado final confirmado.
- `LIFECYCLE_VERIFIED`: fluxo install/upgrade/backup/restore/remove ou equivalente executado no ambiente proporcional.
- `UNVERIFIED`: não demonstrado.
- `FAILED`: demonstrado que não atende.

Busca textual, ausência de erro observada ou fixture isolada não promovem evidência comportamental.

## Resultados

- `ACCEPTED`: todos os critérios materiais demonstrados; limitações remanescentes estão corretamente classificadas.
- `CORRECTION_REQUIRED`: lacuna técnica executável; preparar tarefas corretivas rastreáveis.
- `HUMAN_GATE`: decisão, acesso, custo, privilégio ou consequência prática depende do Maestro Diretor.
- `REJECTED_UNSAFE`: resultado remoto não pode permanecer; exigir reversão seletiva de um ou mais commits ou compensação segura.

O Codex não aceita o próprio trabalho.

## Persistência

A revisão é uma rodada de orquestração com tarefas próprias. Cada decisão ou mudança normativa recebe commit de tarefa publicado em `origin/master`; não há squash. Comentários de issue resumem, mas não substituem memória versionada.
