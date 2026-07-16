# Política de paralelismo e subagentes

## Regra

Paralelizar somente frentes com dependências e outputs separáveis. O Codex permanece responsável pelo resultado integrado.

## DAG mínimo

Cada frente declara tarefa, entradas, outputs, paths autorizados, arquivos compartilhados proibidos, validação local, dependências e critério de integração.

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
- validação final;
- atualização de continuidade e commit;
- operações de registro real, publicação ou destrutivas.

## Retorno do subagente

Escopo, fatos com paths/fontes, alterações, comandos/testes, desconhecidos/riscos e confirmação de ausência de commit/expansão de escopo.

## Falha parcial

Uma frente falha não suspende as demais. O Codex tenta alternativas, conclui o trabalho independente e só então registra bloqueio humano válido.
