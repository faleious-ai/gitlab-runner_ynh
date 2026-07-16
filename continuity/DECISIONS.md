# Registro de decisões

| ID | Estado | Decisão |
|---|---|---|
| ADR-0001 | ACCEPTED | trabalhar somente em `master`, um commit normativo por rodada futura |
| ADR-0002 | ACCEPTED | repositório persistido prevalece sobre chat |
| ADR-0003 | ACCEPTED | Runner e helper images são unidade atômica de versão |
| ADR-0004 | ACCEPTED | autonomia técnica com gates humanos proporcionais |
| ADR-0005 | ACCEPTED | ChatGPT orquestra/revisa; Codex executa charters completos e integra subagentes |

## Derivações vigentes

- `Leia AGENTS.md e continue` executa apenas o charter `READY`.
- O orquestrador resolve perguntas humanas antes de liberar a rodada.
- O Codex conclui todo trabalho não bloqueado antes de parar.
- Subagentes não fazem commit nem integração final.
- O Codex encerra aguardando revisão; aceite pertence ao orquestrador.
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
