# ADR-0003 — Runner e helper images como conjunto atômico

Status: `ACCEPTED`  
Data: 2026-07-16

## Contexto

O Runner usa helper images em jobs e o baseline declara pacotes separados. Atualizar somente o binário ou somente helpers pode criar incompatibilidade difícil de detectar no install superficial.

## Decisão

- uma versão proposta deve resolver o pacote Runner e helper images correspondentes;
- todos os assets obrigatórios por arquitetura devem existir;
- versões devem corresponder por regra documentada;
- qualquer ausência, mismatch ou hash inválido aborta sem escrita parcial;
- lifecycle deve incluir job/executor que realmente use helper image ou prova equivalente;
- manifest e fixtures são atualizados atomicamente.

## Consequências

A release mais nova pode ser recusada se helper assets estiverem incompletos. O updater não pode tratar helper images como etapa manual posterior.