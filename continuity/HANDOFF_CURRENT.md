# Handoff Runner v2

Estado: `READY_FOR_EXECUTOR`
Charter: `CHR-PROGRAM-V2-CONTINUE-001`

1. Fast-forward `gitlab_ynh` e `gitlab-runner_ynh` em `master`.
2. Confirmar árvores limpas.
3. Rodar o consumer.
4. Executar tasks Runner elegíveis com lanes/receipts.
5. Não encerrar por queue vazia, CI vermelho ou primeira falha.
