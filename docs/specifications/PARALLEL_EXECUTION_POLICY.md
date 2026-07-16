# Política de paralelismo e subagentes

## Regra

Paralelizar somente frentes com dependências, paths e outputs separáveis. O Codex permanece responsável pelo resultado integrado, pelos commits de tarefa e pela sincronização remota.

## DAG mínimo

Cada tarefa/frente declara:

- `Task-ID` e dependências;
- entradas e claims;
- seam e verificação local;
- outputs e paths autorizados;
- arquivos compartilhados proibidos;
- critério de integração;
- commit de tarefa que absorverá o resultado.

## Frentes adequadas no Runner

- manifest/sources e matriz de assets;
- lifecycle e service/config;
- tokens, redaction e segurança;
- Docker/executor/helper images;
- testes/workflows;
- upstream/divergência;
- documentação oficial e deprecações.

## Frentes sequenciais

- decisões que redefinem contrato;
- edição de documentos canônicos compartilhados;
- integração Runner/helper images;
- revisão adversarial final;
- atualização de continuidade;
- criação e publicação de commits;
- operações de registro real, publicação ou destrutivas.

## Ownership

Subagentes não criam commit, branch, PR, worktree ou push. Não editam simultaneamente o mesmo path. O executor pode receber patches/arquivos de múltiplas frentes, mas integra somente uma tarefa por vez e executa seus gates antes do commit.

## Retorno do subagente

- escopo e Task-ID;
- fatos com paths/fontes;
- alterações propostas ou realizadas;
- comandos/testes e resultados;
- unknowns, riscos e dead ends;
- confirmação de ausência de commit, push e expansão de escopo.

## Integração

1. conferir ownership e dependências;
2. aplicar outputs da tarefa;
3. executar TDD/gates no seam real;
4. fazer revisão Spec/Charter e Engineering;
5. criar um único commit da tarefa;
6. publicar e verificar remotamente antes da próxima tarefa que escreva no repositório.

## Falha parcial

Uma frente falha não suspende as demais. O Codex tenta alternativas, executa backprop quando aplicável, conclui trabalho independente e só então registra bloqueio válido. Falha de sincronização impede novos commits no mesmo repositório, mas não impede pesquisa ou trabalho independente sem escrita.
