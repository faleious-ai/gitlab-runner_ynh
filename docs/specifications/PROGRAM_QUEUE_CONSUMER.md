# Runner consumer of the canonical program queue

## Authority and seam

The coordinator repository is authoritative for `PROGRAM_MANDATE.json`, `PROGRAM_QUEUE.json` and `PROGRAM_STATE.json`. After the coordinator publishes the program engine, the Executor selects Runner work with:

```text
python3 scripts/maestro_program.py plan --mandate continuity/PROGRAM_MANDATE.json --queue continuity/PROGRAM_QUEUE.json --state continuity/PROGRAM_STATE.json
```

The output is a deterministic plan. `eligible_tasks` is the only source for the next reversible Runner task; a local chat claim or stale handoff is not sufficient.

## Runner ownership map

| Task family | Owned paths | Required evidence |
|---|---|---|
| supported Docker default | `manifest.toml`, `config_panel.toml`, upstream matrix | exact patch tag, coherent TOML and acceptance result |
| trust and CI observation | versioned `evidence/` artifacts and `evidence/EVIDENCE_INDEX.md` | source, timestamp, producer SHA and honest `UNVERIFIED`/`FAILED` limitation |
| Runner process adoption | `AGENTS.md`, `continuity/`, architecture and policy docs | planner output, lane ownership and remote task SHA |

## Gate policy

The Runner may prepare and publish reversible technical work while review is pending. It must stop and preserve a gate when a task requires credentials, real registration, release, deploy, promotion, destructive operation or a material human decision. Missing CI visibility or an unavailable preferred tool is evidence limitation, not a reason to abandon independent work.

## Persistence contract

Preparation lanes may overlap only when ownership and paths are separate. Integration, commit and push remain serial. Every completed Runner task uses one `RND-YYYYMMDD-NNN T-<id>:` commit on `master`, is pushed without force and is verified with `HEAD == origin/master` before another Runner write.
