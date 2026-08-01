# Evidence

Phase 0A implementation-bootstrap evidence is present under `evidence/phase-0a/`.

- `CERTIFICATION.json` is the machine-readable gate result.
- `RESULT.md` is the concise human handoff.
- `assets/phase-0a-materialization.json` binds the repository checkpoint to the exact host-side inputs, roots, digests, and protected cleanup evidence.
- `scripts/verify-phase-0a.py` re-verifies the live materialization without mutating it.

This evidence certifies Phase 0A materialization only. It does not certify a booted machine, runtime behavior, Phase 0B, Phase 1, or a release.

<!-- phase-0b-checkpoint -->
## Phase 0B

`phase-0b/CERTIFICATION.json` contains the 119-test ledger, evidence digests, cleanup result, and release blocker. Raw machine evidence remains outside Git. `phase-0b/RESULT.md` is the human-readable handoff.
