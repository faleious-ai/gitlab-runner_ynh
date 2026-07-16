# ADR-0001 — Branch única e commit por rodada

Status: `ACCEPTED`  
Data: 2026-07-16

## Decisão

- desenvolvimento somente em `master`;
- nenhuma branch/worktree secundária;
- exatamente um commit por rodada e repositório;
- mesmo `Round-ID` em transações cross-repo;
- atualização de memória e evidência no mesmo commit;
- reconciliação do HEAD antes do commit;
- sem force push.

## Rationale

O usuário prioriza continuidade direta e baixa sobrecarga. A atomicidade da rodada substitui o isolamento de branch e permite revert completo por commit.

## Trade-offs e controles

Sem PR, revisão depende de escopo, testes, diff, evidência e round record. Concorrência deve ser detectada por HEAD e nunca resolvida sobrescrevendo histórico.