# Protocolo de revisão

## Fronteira remota

O ChatGPT revisa somente charter, commits, diffs, evidências e validações publicados no GitHub. Estado exclusivamente local não é revisável.

`EXECUTED_AWAITING_REVIEW` exige:

1. SHAs completos publicados em `origin/master` de todos os repositórios afetados;
2. commits recuperáveis pelo GitHub;
3. paths citados existentes no remoto;
4. continuidade com o mesmo `Round-ID`/`Charter-ID`;
5. pacote sem links locais `C:/...`.

Sem isso, o estado é `NOT_REVIEWABLE_REMOTE_SYNC_REQUIRED`, derivado de `LOCAL_COMPLETE_AWAITING_SYNC` ou `REMOTE_SYNC_BLOCKED`. Isso não é julgamento da qualidade técnica.

## Revisão

O ChatGPT:

1. reconcilia HEADs remotos;
2. confirma os SHAs completos e sua posição em `origin/master`;
3. compara o charter com entregas e evidências remotas;
4. inspeciona diff, testes, segurança, compatibilidade e continuidade;
5. verifica integração de subagentes e ausência de outputs órfãos;
6. distingue lacuna técnica, gate humano e falha de sincronização;
7. persiste o resultado.

## Resultados

- `ACCEPTED`: critérios demonstrados.
- `CORRECTION_REQUIRED`: lacuna técnica; gerar rodada corretiva completa.
- `HUMAN_GATE`: decisão, acesso, custo, privilégio ou consequência prática depende do usuário.
- `REJECTED_UNSAFE`: exigir reversão/compensação segura.

O Codex não aceita o próprio trabalho. Encerra conforme o estado real em `EXECUTED_AWAITING_REVIEW`, `BLOCKED_HUMAN`, `LOCAL_COMPLETE_AWAITING_SYNC` ou `REMOTE_SYNC_BLOCKED`.

## Sincronização pendente

Quando o trabalho estiver apenas local, o Codex deve buscar `origin/master`, reconciliar o commit ainda não publicado sem force push, repetir checks impactados, publicar, confirmar `HEAD == origin/master` e então fornecer os SHAs completos e paths remotos.

## Bloqueio humano

O orquestrador apresenta ao usuário a decisão exata, alternativas, consequências e recomendação. Após resposta, persiste a resolução, revisa o charter e libera nova execução. O Codex continua todo trabalho restante até conclusão ou próximo bloqueio válido.

## Persistência

Revisões que mudem estado, decisão ou plano geram round record e commit próprio publicado em `origin/master`. Comentário de issue não substitui memória versionada.