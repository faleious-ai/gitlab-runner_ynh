# Handoff atual

Estado: `READY_FOR_CODEX_CORRECTION_ROUND`  
Charter ativo: `CHR-WP02-002`  
Revisão anterior: `REV-RND-20260716-005 — CORRECTION_REQUIRED`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Retomada mínima

1. Ler `AGENTS.md`.
2. Confirmar `master`, árvore limpa e `HEAD == origin/master` nos dois repositórios.
3. Ler `continuity/STATUS.md`, `continuity/ACTIVE_ROUND.md` e `continuity/reviews/REV-RND-20260716-005.md`.
4. Confirmar `CHR-WP02-002` em estado `READY`.
5. Atribuir novo `Round-ID` e executar integralmente o DAG corretivo.

## Trabalho autorizado

Completar descoberta oficial/freshness, cadeia de checksums, allowlists de origem, cópia candidata do manifest com diff guard, credencial fora de argv, contrato atual da action YunoHost, testes e CI remoto verificável.

Preservar o que já foi demonstrado na rodada anterior. Não reiniciar a arquitetura nem reduzir requisitos para encaixar a implementação existente.

## Regra de esforço

Não parar para progresso, pesquisa, teste falho ou primeira abordagem malsucedida. Ao bloquear uma frente, continuar todas as demais independentes. O gate histórico externo não justifica `BLOCKED_HUMAN`.

## Paralelismo

Use as cinco frentes da Onda 1 do charter. Subagentes não fazem commit nem editam arquivos canônicos compartilhados sem ownership. O executor principal integra, revisa segredo/diff, executa a suíte completa e publica.

## Fora de escopo

Sem promoção de versão, registro real, ação destrutiva, uso da credencial histórica, branch, PR, worktree, release, force push, reescrita de histórico ou alteração de ruleset.

## Fechamento remoto

A rodada só termina depois de:

- um commit publicado em `origin/master` por repositório afetado, mesmo `Round-ID`;
- `HEAD == origin/master` e árvores limpas;
- todos os arquivos/evidências recuperáveis pelo GitHub;
- pacote remoto de revisão com SHAs completos e URLs remotas;
- estado `EXECUTED_AWAITING_REVIEW`.
