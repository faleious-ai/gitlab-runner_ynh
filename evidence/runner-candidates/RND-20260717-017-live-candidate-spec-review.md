# Spec review — T-RUN-UPDATER-LIVE-CANDIDATE-001

Verdict: PASS, pending independent Orchestrator acceptance.

- The candidate contains fixed Runner and helper-image URLs and SHA-256 values for amd64, arm64 and armhf.
- The updater's allowlisted diff changes only the manifest version and source coordinates in an external candidate.
- The tracked manifest remains byte-identical and promotion is explicitly false.
- The live API timeout is preserved as a limitation; the fallback does not claim live GPG verification.
