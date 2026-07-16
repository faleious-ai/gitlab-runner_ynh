# ADR-0004 — Autonomia técnica e gates humanos

Status: `ACCEPTED`  
Data: 2026-07-16

## Autonomia do agente

Decidir e executar escolhas técnicas reversíveis, testes, formatos, algoritmos, refactors e correções dentro dos contratos.

Criar ADR/evidência reforçada para dependência nova, mudança de contrato, compatibilidade, permissões ou persistência.

## Gate humano obrigatório

Interromper antes de:

- mudar missão, licença, visibilidade, fork network ou publicação;
- gerar custo novo;
- acessar segredo não provisionado;
- registrar/desregistrar Runner de produção;
- revogar/rotacionar credencial;
- destruir dados ou ampliar privilégio/exposição material;
- executar release/produção sem rollback;
- escolher entre consequências práticas mutuamente exclusivas relevantes.

Ao escalar, apresentar decisão concreta, alternativas, evidência e consequência prática.