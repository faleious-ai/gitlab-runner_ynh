# Runner parallel execution contract

Task ownership is prefix-aware, so parent and descendant paths conflict. A valid parallel wave contains distinct worker identities, distinct isolated workspaces, matching task and baseline identity, nonempty artifacts, nonempty command logs, verified hashes and real interval overlap.

The coordinator journal records lane start and finish events. Subagent outputs are preparation artifacts only; canonical integration, validation, receipt creation and publication remain serial per task.
