# -Z- Repository Index

This file is the root navigation entry point for the repository.

## Identity

- Product mark: **-Z-**
- Spoken name: **Z**
- CLI: `z`
- Canonical repository: `StealthEyeLLC/-z-`
- Authoritative clean-room branch: `build/z-v1-cleanroom`

## Current state

- The same-VPS host-kernel transition is complete and verified.
- The running implementation-host tuple is `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`.
- Kernel `6.8.0-9001-generic` is the persistent boot default; `6.8.0-136-generic` remains the tested rollback entry.
- The host-transition checkpoint is commit `96853e15f7a8cab1efc178d03a4d3e027b0b28cc`, tree `b4308f82a5329542450de3a4cbfabf3300414068`.
- The preserved release/reference candidate remains `z-debian-13.6-amd64-ch53-v1` and is not certified.
- Phase 0A and Z product implementation have not started.

Read [`docs/STATUS.md`](docs/STATUS.md) for the complete enumerated result, boundaries, maintenance obligations, and recommended next mission.

## Governing documents

Read the governing documents in the precedence order defined by [`docs/INDEX.md`](docs/INDEX.md):

1. `docs/INVARIANTS.md`
2. `docs/ANTI-INVARIANTS.md`
3. `docs/SACRIFICES.md`
4. `docs/SCOPE.md`
5. `docs/ARCHITECTURE.md`
6. `docs/VARIANTS.md`
7. `docs/SECURITY.md`
8. `docs/DECISIONS.md`
9. `docs/BUILD.md`
10. `docs/CERTIFICATION.md`

## Operational and evidence entry points

- `docs/STATUS.md` — current canonical operational status and next recommended mission.
- `docs/reference/IMPLEMENTATION-HOST.md` — exact verified implementation-host tuple.
- `docs/reference/DEPENDENCIES.md` — preserved release candidate and implementation-host binding.
- `assets/dependencies.lock.json` — machine-readable identities and digests.
- `evidence/checkpoints/host-kernel-transition-20260801/` — digest-verifiable host-transition proof.

## Research and provenance

- `docs/research/SSH-RESEARCH-AND-ARCHITECTURE.md`
- `docs/research/CHANGES-FROM-ORIGINAL.md`
- `docs/research/SOURCES.md`
- `SHA256SUMS.txt`
- `AGENTS.md`

## Repository areas

- `docs/` — governing architecture, operational status, reference, and research
- `src/` — implementation source; currently boundary documentation only
- `tests/` — automated tests and certification harnesses; currently boundary documentation only
- `scripts/` — deterministic development and release commands; currently boundary documentation only
- `evidence/` — verified host checkpoint and future release evidence
- `assets/` — pinned machine-readable locks and future materialized asset provenance

## Claim boundary

The implementation host is verified for the recorded transition claims. Z itself is not implemented, certified, or released. The next recommended mission is Phase 0A only.
