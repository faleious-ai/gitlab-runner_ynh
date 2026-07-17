---
name: maestro-tdd
description: Test-drive every behavioral change through a predeclared public seam. Require an exact red-capable oracle, observed RED before the fix, minimal GREEN implementation and proportional regression validation, including shell, YunoHost packaging and lifecycle work.
---

# MAESTRO TDD

Behavioral change without observed RED→GREEN is implementation with tests, not test-driven development.

## Seam first

The task contract must name the public seam before any test or implementation:

- CLI invocation and exit/output;
- YunoHost config controller function;
- install/upgrade/backup/restore/remove entry point;
- manifest/updater command and produced file/diff;
- service/process invocation and environment;
- file or configuration contract;
- external API adapter;
- security boundary observable through argv, env, logs or filesystem.

Tests and callers cross the same seam. Do not test private helpers when the defect exists only in the integrated path.

## Red-capable oracle

Before coding, name one exact unattended command already capable of catching the missing behavior or defect. It must be:

- specific to the claim, not merely “does not crash”;
- deterministic or have a pinned high reproduction rate;
- fast enough for repeated cycles;
- independent of the implementation’s own calculation;
- able to fail when the old/broken behavior is present.

Record invocation and observed failure in versioned evidence or the round record.

## Vertical slice loop

For one claim at a time:

1. write the smallest behavior-level test at the seam;
2. run it and confirm the expected RED reason;
3. implement only enough to make that test pass;
4. run it and confirm GREEN;
5. run adjacent existing tests;
6. refactor only after GREEN, preserving behavior;
7. repeat for the next claim.

Do not write all imagined tests first and then all implementation. Each slice should teach the next.

## Project seam examples

### Config panel

Source `scripts/config` in a controlled shell, invoke the real `run__<id>` function, provide ephemeral inputs and capture the call to the shared helper. Searching for the function name is not a behavioral test.

### Registration and secret transport

Use a stub `gitlab-runner` executable that records argv, selected environment names and redacted output. Assert the credential is absent from argv/logs and available only through the approved environment channel. Never persist a real token.

### Backup/restore

Use a temporary filesystem and stub YunoHost helpers. Invoke the real scripts; assert identity/config paths are backed up/restored and registration is not called.

### Updater

Invoke the public CLI with deterministic fixtures. Assert exact candidate manifest/diff, atomic failure behavior, allowlisted fields, provenance and no promotion of the live manifest.

### Network/provenance

Fixtures test parsing and failure modes. A separate controlled live probe establishes current external behavior; fixture success never proves freshness.

When the production caller follows redirects or delegates transport:

1. capture the current official redirect/final-origin chain or a sanitized fixture derived from it;
2. make the baseline caller fail against that chain for the intended reason;
3. keep parser/unit mocks, but do not let them replace the public transport seam;
4. publish the functional commit;
5. run the live probe with that published commit;
6. create a new versioned evidence artifact tied to the commit and command.

Never edit an older observation to add `valid`, `verified`, `passed` or equivalent. Schema completion is not a new experiment.

## Anti-patterns

- grep or AST presence used as behavior proof;
- mocks that bypass the real entry point;
- transport tests that replace the redirect/final-origin layer under review;
- tautological expected values computed like production code;
- snapshots without an independent source of truth;
- test written after the fix and described as RED without observing failure;
- swallowing expected failure or weakening assertion until green;
- testing an easy unit seam while the defect requires lifecycle/integration;
- manually strengthening historical evidence after code changes.

## Non-code changes

Documentation-only work may mark TDD `NOT_APPLICABLE`, but still needs a verifiable contract such as link/ID/state/contradiction checks. TOML, JSON, workflows and packaging scripts are behavior and normally require parser, contract or harness tests.

A documentation or evidence task may normalize shape, but factual values remain those emitted by the original observation. Changed facts require a new observation and artifact.

## Completion

A behavioral task is ready for internal review only when:

- RED evidence matches the intended missing behavior;
- GREEN proves the same seam;
- negative and error cases required by the claim pass;
- external transport changes have a captured-chain test and a post-commit live probe plan;
- full proportional suite passes;
- no test or production secret is persisted;
- evidence level and provenance are stated honestly.
