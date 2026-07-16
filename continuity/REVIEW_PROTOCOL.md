# Protocolo de revisão

O ChatGPT revisa o charter executado, HEAD, diff, commits, evidências, validações, riscos e bloqueios.

## Resultados

- `ACCEPTED`: critérios demonstrados.
- `CORRECTION_REQUIRED`: lacuna técnica; gerar rodada corretiva completa.
- `HUMAN_GATE`: decisão, acesso, custo, privilégio ou consequência prática depende do usuário.
- `REJECTED_UNSAFE`: exigir reversão/compensação segura.

O Codex não aceita o próprio trabalho. Encerra em `EXECUTED_AWAITING_REVIEW` ou `BLOCKED_HUMAN`.

## Bloqueio

O orquestrador apresenta ao usuário a decisão exata, alternativas, consequências e recomendação. Após resposta, persiste a resolução, revisa o charter e libera nova execução. O Codex continua todo trabalho restante até conclusão ou próximo bloqueio válido.

## Persistência

Revisões que mudem estado, decisão ou plano geram round record e commit próprio. Comentário de issue não substitui memória versionada.
