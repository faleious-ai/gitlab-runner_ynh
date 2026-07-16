# ADR-0006 — Síntese MAESTRO–Cavekit e commits por tarefa

Data: 2026-07-16  
Estado: `ACCEPTED`  
Decisor: Maestro Diretor

## Contexto

A revisão das rodadas WP-02 mostrou avanço técnico real, porém claims excessivos e lacunas previsíveis chegavam ao commit final da rodada. O Cavekit v4 oferece spec durável, verificação explícita, revisão adversarial e backpropagation, mas remove paralelismo, subagentes e memória em camadas. O Cavekit v3.1.0 preserva DAG, validação progressiva, revisão por outro modelo, tracking e convergência, porém usa branches, commits por tarefa do agente e gates humanos mais frequentes que o mandato MAESTRO.

## Decisão

Adotar uma síntese local, sem instalar runtime ou hooks externos.

1. A rodada permanece unidade de autorização, escopo, baseline e veredito.
2. A tarefa passa a ser unidade de implementação, commit, sincronização e reversão.
3. Cada tarefa concluída gera exatamente um commit atômico publicado em `origin/master` antes da próxima tarefa que escreva no mesmo repositório.
4. Commits usam `Round-ID` e `Task-ID`; não são squashados nem reescritos após publicação.
5. Subagentes não fazem commit. O executor integra os outputs e cria o commit da tarefa.
6. Mudança comportamental exige TDD no seam público: RED observado, implementação mínima, GREEN observado e regressão completa proporcional.
7. Falha inesperada ativa backpropagation: causa, classificação da lacuna, invariante/critério, teste RED, correção GREEN e memória durável.
8. Backprop técnico é autônomo. Alteração de comportamento externo, produto, custo, privilégio, risco ou irreversibilidade volta ao Maestro Diretor.
9. Mudança de alto impacto recebe revisão adversarial pré-build e todo commit recebe revisão interna pré-publicação em dois eixos independentes: conformidade com charter/spec e engenharia/segurança/lifecycle.
10. Compressão Caveman é limitada a matrizes, ledgers e handoffs machine-oriented; não se aplica a segurança, gates humanos, ADRs, recuperação ou instruções destrutivas.
11. Convergência é acompanhada por coverage de claims, gates, findings, bloqueios e estabilidade; volume de diff nunca é prova isolada.
12. O ChatGPT continua como revisor externo independente do intervalo remoto completo da rodada.

## Consequências

- Maior rastreabilidade e reversão seletiva por tarefa.
- Falha de uma tarefa não contamina um commit monolítico da rodada.
- O revisor avalia commits individualmente e também o comportamento integrado.
- O custo de sincronização aumenta; em troca, cada ponto remoto é recuperável e auditável.
- O protocolo anterior de um commit por rodada fica `SUPERSEDED`.

## Proveniência

Síntese inspirada no Cavekit de Julius Brussee, versões v4 e v3.1.0, sob licença MIT. A arquitetura, terminologia, gates e adaptações deste repositório são locais e governados pelo MAESTRO.
