# Runner consumer contract

The consumer merges static backlog tasks with dynamic correction tasks from PROGRAM_FINDINGS.json. Unknown eligible identifiers fail closed.

Lane validation uses distinct workspaces, artifacts, logs, identities and baselines. Completion remains derived from a published task receipt.
