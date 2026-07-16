# ADR-0005 — ChatGPT orquestra/revisa; Codex executa

Estado: `ACCEPTED`  
Data: 2026-07-16

## Contexto

O usuário iniciará o Codex com `Leia AGENTS.md e continue` e resolverá decisões/bloqueios com o ChatGPT. É necessário separar mandato, execução e aceite.

## Decisão

- usuário: Maestro Diretor e autoridade dos gates humanos;
- ChatGPT: orquestrador/revisor via repositório;
- Codex: executor de charters completos;
- subagentes: frentes independentes sem commit ou integração final;
- o Codex conclui tudo que não depende de bloqueio humano;
- bloqueio só é escalado após terminar o restante do DAG;
- saída do Codex é revisão pendente, nunca autoaceite.

## Consequências

O prompt pode permanecer mínimo, a continuidade reside no repositório, o trabalho pode ser paralelo e o aceite permanece independente da execução.
