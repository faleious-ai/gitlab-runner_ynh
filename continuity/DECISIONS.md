# Registro de decisões

| ID | Estado | Decisão |
|---|---|---|
| ADR-0001 | ACCEPTED | trabalhar somente em `master`, um commit por rodada |
| ADR-0002 | ACCEPTED | repositório persistido prevalece sobre chat |
| ADR-0003 | ACCEPTED | Runner e helper images são unidade atômica de versão |
| ADR-0004 | ACCEPTED | autonomia técnica com gates humanos proporcionais |

## Derivações vigentes

- instalação nunca resolve `latest` em runtime;
- token real não entra em teste persistido;
- logs e evidências devem redigir tokens;
- executor só é considerado validado por execução controlada ou prova equivalente explícita;
- falha em qualquer asset obrigatório impede atualização completa;
- implementação local pertence a este repositório; coordenação transversal pertence temporariamente a `gitlab_ynh`.

## Decisões técnicas esperadas em WP-01/WP-02

- fonte de verdade de releases;
- método de resolução de helper images;
- esquema de fixtures;
- estratégia de hash/download;
- runner registration command compatível com versão atual;
- ambiente de teste Docker;
- semântica de backup/restore para configuração e identidade do Runner.