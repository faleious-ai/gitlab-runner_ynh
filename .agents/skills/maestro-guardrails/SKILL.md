---
name: maestro-guardrails
description: Enforce think-before-code, minimal and surgical changes, explicit assumptions, exact verification, secret safety, task atomicity and honest completion before every task commit.
---

# MAESTRO Guardrails

Apply before the first edit and again against the final task diff.

## 1. Think before coding

State:

- Task-ID and one-sentence result;
- public seam;
- assumptions;
- claims/invariants;
- exact verification commands;
- affected paths and dependencies;
- rollback boundary.

A load-bearing unknown is researched or escalated. It is never guessed into implementation.

## 2. Minimum sufficient change

- Implement only what the task claims require.
- No speculative features, compatibility layers, abstractions or dependencies.
- No “while here” cleanup.
- Duplication is acceptable until a demonstrated repeated decision justifies a shared module.
- If the diff is larger than the task contract implies, split the task or explain every additional path.

## 3. Surgical ownership

Every changed line maps to:

- a task claim/invariant;
- required test/evidence;
- necessary integration or canonical continuity update.

Unrelated bugs become future tasks or learning-ledger candidates. Do not smuggle them into the current commit.

## 4. Behavior before structure

- Test the public seam, not the presence of implementation details.
- Do not accept grep, file existence or mocked internal calls as proof of runtime behavior.
- Preserve RED and GREEN evidence for behavioral work.
- Do not weaken/delete tests to obtain green.

## 5. Security and trust

- Never read, print, test or persist real credentials unless explicitly authorized in a safe environment.
- Check argv, env, logs, fixtures, reports and git diff for secrets.
- Trust failures fail closed; unavailable verification is not equivalent to successful verification.
- External artifacts remain pinned by exact version, URL and hash/provenance.
- Destructive operations require explicit gate and rollback.

## 6. Lifecycle reality

A unit test does not prove install, upgrade, service, backup, restore or removal. Claims about lifecycle require the corresponding harness or environment. Mark missing levels `UNVERIFIED`, not completed.

## 7. Commit integrity

Before commit:

- current diff contains one Task-ID;
- dependencies are already published or cross-repo synchronized;
- focal and proportional gates pass;
- both review axes have no unresolved P0/P1;
- claims match evidence levels;
- no local path or transient artifact is cited as remote proof;
- rollback by reverting the task commit is understood;
- commit message uses Round-ID and Task-ID.

After commit, publish and verify before another writing task.

## 8. Honest completion

Do not declare a task or round complete because:

- the code looks plausible;
- tests were claimed but not run;
- CI exists but no run is tied to the SHA;
- a function/file is present;
- the implementation works only in a fixture;
- the task is long or the session is ending.

Completion follows the protocol state and evidence, not confidence.

## Final report

List assumptions resolved/unresolved, scope check, test/evidence map, review findings, secret scan, rollback and remote SHA. Any exception to these guardrails is a finding, not an invisible shortcut.