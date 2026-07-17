# Contrato do consumidor Runner v2

## Seam

```text
python scripts/program_consumer.py --coordinator-root ../gitlab_ynh --runner-root .
```

O consumer executa `refresh-queue`, `doctor` e `plan` no motor do coordenador e filtra apenas tarefas cujo campo `repositories` contém `runner`.

## Receipt

Cada task Runner inclui `continuity/task_receipts/<Task-ID>.json` no mesmo commit. O planner do coordenador deriva `task_remote_verified` somente após o commit estar em `origin/master`, conter o Task-ID, respeitar ownership e carregar evidências/gates pass.

## Findings

Falha determinística ou CI vermelho deve ser registrada no coordenador com tarefa corretiva. Bloqueio ambiental exige condição, evidência, fallbacks, estado seguro e retomada; não se converte em sucesso.
