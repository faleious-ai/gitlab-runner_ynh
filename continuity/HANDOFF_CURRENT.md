# Handoff atual

Estado: `READY_FOR_CODEX_FULL_ROUND`  
Charter: `CHR-WP01-001`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Retomada

1. Ler `AGENTS.md`.
2. Confirmar HEAD de `master` neste repositório e no coordenador quando acessível.
3. Ler `STATUS.md` e `ACTIVE_ROUND.md`.
4. Confirmar charter `READY`, atribuir `Round-ID` e executar o DAG completo.

## Trabalho autorizado

Auditar manifest/sources/assets, scripts/lifecycle, service/config, tokens/redaction, Docker/executor/helper images, testes/workflows/docs, upstream/divergência, riscos e backlog.

Frentes independentes devem ser paralelizadas por subagentes. Subagentes não fazem commit. O Codex integra, valida e persiste.

## Regra de parada

Não parar para progresso, tarefa longa, pesquisa ou teste falho. Ao bloquear uma frente, continuar todas as independentes. Parar apenas após conclusão integral ou depois de concluir todo trabalho independente e registrar gate humano válido.

## Fora de escopo

Updater, mudança de versão/hash/URL, token real, registro em produção, mirrors, ruleset ou release.

## Saída esperada

- quatro documentos de auditoria definidos no charter;
- status, handoff, evidence index e round record;
- commit em `master` e mesmo `Round-ID` cross-repo quando acessível;
- estado `EXECUTED_AWAITING_REVIEW`;
- pacote com commits, evidências, gaps, riscos e bloqueios.

O ChatGPT revisará e definirá aceite, correção ou gate humano.
