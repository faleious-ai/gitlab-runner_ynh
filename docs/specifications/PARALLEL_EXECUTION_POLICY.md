# Paralelismo Runner v2

Tarefas Runner podem ser preparadas em paralelo somente quando ownership prefix-aware é disjunto. `tests/` conflita com `tests/lifecycle/`; paths diferentes por string não bastam.

Workers distintos usam o journal hash-chained do coordenador, artifacts e command logs hashados. Subagentes não editam manifest, state, handoff ou outros arquivos canônicos simultaneamente. O Executor integra, valida, prepara receipt, commita e publica uma tarefa por vez.
