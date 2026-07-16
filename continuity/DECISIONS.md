# Registro de decisões

| ID | Estado | Decisão |
|---|---|---|
| ADR-0001 | SUPERSEDED_BY_ADR-0006 | trabalhar somente em `master`; política antiga de um commit por rodada substituída |
| ADR-0002 | ACCEPTED | repositório persistido prevalece sobre chat |
| ADR-0003 | ACCEPTED | Runner e helper images são unidade atômica de versão |
| ADR-0004 | ACCEPTED | autonomia técnica com gates humanos proporcionais |
| ADR-0005 | ACCEPTED | ChatGPT orquestra/revisa; Codex executa charters completos e integra subagentes |
| ADR-0006 | ACCEPTED | rodada autoriza; tarefa implementa, versiona e reverte; síntese MAESTRO–Cavekit com TDD, backprop, revisão adversarial, compressão limitada e convergência |

## Derivações vigentes

- `Leia AGENTS.md e continue` executa apenas o charter `READY`.
- O orquestrador resolve perguntas humanas materiais antes de liberar a rodada.
- Questões técnicas reversíveis e backprop técnico pertencem ao mandato autônomo.
- O Codex conclui todo trabalho não bloqueado antes de parar.
- Subagentes não fazem commit nem integração final.
- Cada tarefa concluída gera commit atômico próprio, publicado e verificado antes da próxima escrita no mesmo repositório.
- Commits publicados não são squashados nem reescritos.
- Mudança comportamental exige TDD no seam público com RED e GREEN observados.
- Revisão interna pré-commit ocorre nos eixos Spec/Charter e Engineering; aceite final pertence ao orquestrador externo.
- Falha inesperada é classificada e retropropagada para critério, invariante, teste e memória quando aplicável.
- instalação nunca resolve `latest` em runtime;
- token real não entra em teste persistido;
- logs/evidências redigem tokens;
- executor só é validado por execução controlada ou prova equivalente;
- falha em asset obrigatório impede atualização;
- implementação local pertence a este repositório; coordenação transversal pertence temporariamente a `gitlab_ynh`.

## Decisões técnicas esperadas em WP-01/WP-02

- fonte de verdade de releases;
- resolução de helper images;
- esquema de fixtures;
- hash/download;
- registration command compatível;
- ambiente Docker;
- backup/restore da configuração e identidade.
