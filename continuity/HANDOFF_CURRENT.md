# Handoff atual

Estado: `READY_FOR_CODEX_FULL_ROUND`  
Charter ativo: `CHR-WP02-004`  
Revisão anterior: `REV-RND-20260716-010 — CORRECTION_REQUIRED`  
Processo vigente: `ADR-0006` + process backprop `RND-20260717-011`  
Branch: `master`

## Prompt

```text
Leia AGENTS.md e continue.
```

## Retomada

1. Ler `AGENTS.md`.
2. Reconciliar `origin/master` deste Runner e do coordenador.
3. Confirmar `CHR-WP02-004 READY` nos dois repositórios.
4. Ler `continuity/reviews/REV-RND-20260716-010.md`.
5. Carregar `maestro-research`, `maestro-tdd`, `maestro-check`, `maestro-review`, `maestro-backprop` e `maestro-guardrails` conforme cada tarefa.
6. Atribuir novo `Round-ID` e executar T01–T07 integralmente.

## Findings a resolver

- P1-F01: o URL oficial da chave redireciona para CloudFront, mas o validator atual rejeita o redirect antes do GPG;
- P1-F02: evidência histórica recebeu `key_validity=valid` por edição documental, sem nova observação;
- P2-F03: continuidade T08 contém texto/HEADs pré-publicação;
- P2-F04: config panel usa `alpine:latest`, divergindo do default versionado do install.

## Invariantes

- preservar correções aceitas de `RND-20260716-010`;
- nenhum wildcard genérico de origem;
- GPG/GPGV e fingerprint final são autoridade, não a documentação isolada;
- novo resultado live gera novo artefato ligado ao commit produtor;
- não editar semanticamente observação antiga;
- manifest permanece `18.6.2~ynh1`;
- não registrar Runner real, usar segredo histórico ou alterar settings do GitHub;
- um commit remoto por tarefa, sem squash/branch/PR/worktree/force push.

## Gate

`HG-RUN-SEC-01` permanece risco histórico externo e não bloqueia. Nenhuma pergunta humana está pendente.
