# Runner evidence index

Evidence states: `STRUCTURALLY_OBSERVED`, `LOCAL_VERIFIED`, `REMOTE_CI_VERIFIED`, `LIFECYCLE_VERIFIED`, `FAILED`, `UNVERIFIED`, `SUPERSEDED`.

## Current architecture

| ID | State | Round / task | Evidence |
|---|---|---|---|
| EVD-ARCH-V2-RUNNER | LOCAL_VERIFIED | RND-20260717-016 / T-RUN-ARCHITECTURE-V2 | Runner consumer and contracts at `7dc24ccb8b539c052966eee4d22820e51e418433` |
| EVD-ARCH-V2-HARDEN-RUNNER | LOCAL_VERIFIED | RND-20260717-016 / T-GOV-ARCHITECTURE-V2-HARDEN | dynamic correction tasks, unknown-task rejection, v2 skills and receipt at `dafcac9a26e56d8c3731fae66e9e4cc5f5a0d015` |
| EVD-RUNNER-DOCKER-DEFAULT | LOCAL_VERIFIED | RND-20260717-015 | `alpine:3.24.1` in manifest and config panel at `40e3a0854da387ed51320afa15416abb1747009f` |
| EVD-RUNNER-LIVE-TRUST | LOCAL_VERIFIED | RND-20260717-015 | versioned trust observation; no promotion or lifecycle claim |
| EVD-RUNNER-REMOTE-CI | FAILED | RND-20260717-015 | public run failed; success remains `UNVERIFIED` |
| EVD-RUNNER-FULL-SUITE-LINUX | LOCAL_VERIFIED | RND-20260717-016 | architecture activation record reports 39/39 in the Linux sandbox |
| EVD-RND-20260717-017-CONSUMER-READONLY | LOCAL_VERIFIED | RND-20260717-017 / T-GOV-ARCHITECTURE-V2-READONLY-CONSUMER | temporary queue and byte-identical sentinel acceptance; receipt is SELF-bound |

## Historical evidence

Detailed evidence before architecture v2 remains in `continuity/rounds/`, `continuity/reviews/`, `docs/audit/`, versioned JSON artifacts and Git history. Superseded observations remain immutable and are not upgraded by editing this index.

Claims require a task, public seam, method, command, result, commit and limitation. Fixture data does not establish freshness. Acceptance remains owned by the Orchestrator.
