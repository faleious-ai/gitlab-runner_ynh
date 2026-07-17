# AGENTS.md — GitLab Runner YunoHost

## Missão

Executar as tarefas Runner do programa canônico mantido em `faleious-ai/gitlab_ynh`, preservando atualização atômica Runner/helper images, segurança, lifecycle e evidência. O Git remoto e os receipts publicados prevalecem sobre chat e queue local.

## Invocação

`Leia AGENTS.md e continue` não significa “faça uma tarefa”. Significa atualizar coordenador e Runner, consumir o planner v2 e executar todas as tarefas Runner reversíveis elegíveis até `stop_allowed` ou `checkpoint_allowed` semanticamente válido.

## START obrigatório

1. `git fetch origin` e fast-forward seguro em `master`; não sobrescrever árvore suja.
2. Atualizar também o sibling coordenador `../gitlab_ynh` por fast-forward.
3. Ler `HANDOFF_CURRENT`, `STATUS`, `ACTIVE_ROUND` nos dois repos.
4. Executar:

```text
python scripts/program_consumer.py --coordinator-root ../gitlab_ynh --runner-root .
```

5. Se inválido, corrigir drift técnico ou persistir checkpoint; não improvisar queue.

## Execução

- Use somente tasks presentes em `PROGRAM_BACKLOG.json` ou criadas por `register-finding`.
- Quando houver duas lanes separáveis, use workers/subagentes distintos e journal do coordenador; preparação paralela, integração serial.
- Mudança comportamental usa RED→GREEN no seam público.
- Antes do commit, rode reviews Spec e Engineering, validate-change e gates.
- Execute `prepare-receipt` pelo motor do coordenador; receipt, código, testes e evidências entram no mesmo commit.
- Commit subject contém Round-ID e Task-ID; push sem force; fetch e `HEAD == origin/master`.
- Reexecute o consumer e continue.

## Proibições

Sem branch, PR, worktree, force push, segredo, registro real, deploy, promoção, release ou mutação destrutiva sem gate. Não editar acceptance tests ou specs protegidos. Não marcar task como completed por edição de JSON.

## Parada

Queue vazia não autoriza parada. `stop_allowed=true` vem somente do planner. `checkpoint_allowed=true` encerra a invocação sem declarar programa concluído. Falha técnica, CI vermelho ou ambiente Windows não é gate humano; deve produzir finding/tarefa ou checkpoint externo explícito.
