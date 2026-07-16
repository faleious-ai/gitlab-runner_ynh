# Protocolo de rodada de IA

Identificador: `RND-YYYYMMDD-NNN`.

## ORCHESTRATE

O ChatGPT reconcilia estado/decisões/evidências, pergunta ao usuário o que possa alterar consequência prática, decide questões técnicas reversíveis e só marca `ACTIVE_ROUND` como `READY` quando escopo, DAG, critérios, validações e gates estiverem completos.

## START — Codex

1. confirmar repositório e `master`;
2. resolver `baseline_head` e reconciliar remoto;
3. verificar árvore limpa;
4. ler `AGENTS.md`, `HANDOFF_CURRENT.md`, `STATUS.md` e `ACTIVE_ROUND.md`;
5. confirmar charter `READY`, atribuir `Round-ID` e registrar orientação adicional;
6. decompor DAG e paralelismo seguro.

## EXECUTE

- executar todo o charter;
- usar tentativa-erro-aprendizado e testes;
- registrar fatos em arquivos/evidências;
- não usar tokens reais persistidos;
- tratar Runner/helper images como conjunto;
- não confundir download com lifecycle validado;
- não parar para progresso, tarefa longa, pesquisa, teste falho ou primeira estratégia malsucedida.

## PARALLELIZE

Delegar frentes independentes com ownership de paths/outputs. Subagentes não fazem commit, não alteram documentos canônicos compartilhados sem ownership e retornam fatos, mudanças, validações, riscos e desconhecidos. O Codex integra e valida.

## VALIDATE

Aplicar conforme escopo: schema/lint, integridade/hashes, determinismo, install/service, registration redigido, Docker/helper image, upgrade, backup/restore, remove, falhas negativas, diff e ausência de segredo.

## BLOCKER SWEEP

Antes de parar, concluir todos os nós independentes, tentar alternativas técnicas e registrar condição, evidência, tentativas, decisão humana exata e grafo restante. Tarefa longa e teste falho não são bloqueios.

## PERSIST

Atualizar no fechamento: código/docs, `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, decisões/ADRs, round record e `EVIDENCE_INDEX`. Reconciliar novamente HEAD e repetir checks impactados.

## COMMIT

Política normativa para rodadas futuras: um commit por rodada neste repositório.

```text
<type>(<scope>): <resultado observável>

Round-ID: RND-YYYYMMDD-NNN
Charter-ID: CHR-...
Work-Package: WP-XX
Evidence: EVD-...
```

Trabalho cross-repo repete o mesmo `Round-ID`.

## EXECUTOR END

O Codex termina somente com todas as tarefas não bloqueadas concluídas, commit em `master`, evidência/handoff reconciliados e estado `EXECUTED_AWAITING_REVIEW` ou `BLOCKED_HUMAN`. Não marca `ACCEPTED`.

## REVIEW

O ChatGPT aplica `REVIEW_PROTOCOL.md` e registra aceite, correção ou gate humano. Após resolução com o usuário, revisa o charter e libera nova rodada.
