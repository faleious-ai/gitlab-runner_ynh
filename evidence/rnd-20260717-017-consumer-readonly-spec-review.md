# Spec review — T-GOV-ARCHITECTURE-V2-READONLY-CONSUMER

Reviewer role: independent specification review by the Executor; acceptance remains with the Orchestrator.

Verdict: `PASS` for the Runner-side contract.

- The consumer uses a context-managed temporary directory.
- `refresh-queue`, `doctor` and `plan` receive the same explicit temporary `--queue` path.
- The acceptance fixture records all engine calls and proves the tracked queue sentinel is byte-identical after execution.
- The protected consumer inventory entry remains present and is updated to the SHA-256 of the published bytes.
- No path-protection or fail-closed behavior was weakened.
