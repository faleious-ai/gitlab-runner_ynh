# Revisão Runner v2

A revisão usa receipt e commit remoto. Confirma Task-ID, ownership, acceptance, evidence, CI/lifecycle e ausência de segredo. `LOCAL_VERIFIED` não implica `REMOTE_CI_VERIFIED` nem `LIFECYCLE_VERIFIED`. Findings executáveis retornam ao backlog do coordenador.
