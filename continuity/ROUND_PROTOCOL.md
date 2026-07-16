# Protocolo de rodada de IA

Identificador: `RND-YYYYMMDD-NNN`.

A rodada só fica disponível para revisão quando o commit final está publicado e verificável em `origin/master`. Commit apenas local não é persistência MAESTRO.

## ORCHESTRATE

O ChatGPT reconcilia estado/decisões/evidências e HEADs remotos, pergunta ao usuário o que possa alterar consequência prática, decide questões técnicas reversíveis e só marca `ACTIVE_ROUND` como `READY` quando escopo, DAG, critérios, validações, gates e plano de sincronização remota estiverem completos.

## START — Codex

1. confirmar repositório e `master`;
2. executar `git fetch origin`;
3. registrar `baseline_head = origin/master`;
4. verificar árvore limpa e HEAD local reconciliado;
5. ler `AGENTS.md`, `HANDOFF_CURRENT.md`, `STATUS.md` e `ACTIVE_ROUND.md`;
6. confirmar charter `READY`, atribuir `Round-ID` e registrar orientação adicional;
7. decompor DAG e paralelismo seguro.

## EXECUTE

- executar todo o charter;
- usar tentativa-erro-aprendizado e testes;
- registrar fatos em arquivos/evidências;
- não usar tokens reais persistidos;
- tratar Runner/helper images como conjunto;
- não confundir download com lifecycle validado;
- não parar para progresso, tarefa longa, pesquisa, teste falho ou primeira estratégia malsucedida.

## PARALLELIZE

Delegar frentes independentes com ownership de paths/outputs. Subagentes não fazem commit, push, não alteram documentos canônicos compartilhados sem ownership e retornam fatos, mudanças, validações, riscos e desconhecidos. O Codex integra e valida.

## VALIDATE

Aplicar conforme escopo: schema/lint, integridade/hashes, determinismo, install/service, registration redigido, Docker/helper image, upgrade, backup/restore, remove, falhas negativas, diff e ausência de segredo.

## BLOCKER SWEEP

Antes de parar, concluir todos os nós independentes, tentar alternativas técnicas e registrar condição, evidência, tentativas, decisão humana exata e grafo restante. Tarefa longa e teste falho não são bloqueios. Problema de push é sincronização remota, não aceite.

## PERSIST LOCAL

Atualizar no fechamento: código/docs, `STATUS`, `HANDOFF_CURRENT`, `ACTIVE_ROUND`, decisões/ADRs, round record e `EVIDENCE_INDEX`. Executar `git fetch origin`, reconciliar novamente o HEAD, revisar diff/segredos e repetir checks impactados. Criar exatamente um commit local da rodada.

Após o commit local, o estado máximo permitido é `LOCAL_COMPLETE_AWAITING_SYNC`.

## REMOTE SYNC

Para este repositório e qualquer coordenador afetado:

1. executar `git fetch origin`;
2. verificar `git rev-list --left-right --count origin/master...HEAD`;
3. com resultado `0 1`, executar `git push origin master`;
4. se o remoto avançou, nunca force: rebasear ou recriar apenas o commit ainda não publicado sobre o novo `origin/master`, resolver conflitos, repetir checks e preservar um único commit final;
5. se o push falhar por acesso, divergência ou indisponibilidade, registrar `REMOTE_SYNC_BLOCKED` com comando, erro, tentativas e ação necessária;
6. após push, executar novo fetch e confirmar `git rev-parse HEAD == git rev-parse origin/master`;
7. confirmar SHA completo recuperável no GitHub e todos os paths de evidência presentes no remoto.

## ESTADOS DE SAÍDA

- `LOCAL_COMPLETE_AWAITING_SYNC`: execução e commit concluídos apenas localmente.
- `REMOTE_SYNC_BLOCKED`: resultado local seguro, mas publicação remota não concluída.
- `BLOCKED_HUMAN`: todo trabalho independente e persistência possível concluídos; resta gate humano real.
- `EXECUTED_AWAITING_REVIEW`: commits publicados, HEADs coincidentes, árvores limpas, evidências remotas e pacote de revisão completo.

O Codex não marca `ACCEPTED`.

## PACOTE REMOTO DE REVISÃO

Informar repositórios, SHAs completos, `Round-ID`, `Charter-ID`, matriz tarefa-output-evidência, comandos/resultados, paths/URLs do GitHub, riscos, gates e confirmação de `HEAD == origin/master`. Links locais `C:/...` não contam como evidência do orquestrador.

## REVIEW

O ChatGPT aplica `REVIEW_PROTOCOL.md` apenas sobre material remoto e registra aceite, correção ou gate humano. Após resolução com o usuário, revisa o charter e libera nova rodada.