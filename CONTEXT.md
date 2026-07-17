# Contexto canônico Runner v2

Este repositório é autoridade sobre o pacote GitLab Runner YunoHost: manifest, updater, helper images, registro, Docker, lifecycle, testes e evidências. O coordenador `faleious-ai/gitlab_ynh` é autoridade sobre mandato, backlog, state e findings do programa.

A versão declarada permanece `18.6.2~ynh1` até uma tarefa de promoção aprovada. O objetivo imediato é produzir candidato live reproduzível, corrigir a suíte/CI e demonstrar lifecycle Linux sem expor credenciais.

`PROGRAM_QUEUE.json` do coordenador é derivado. A retomada usa `scripts/program_consumer.py`; nenhum status local substitui o planner.
