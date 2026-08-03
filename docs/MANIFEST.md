# Documentation Manifest

Status: **Canonical inventory; navigation only**

This file classifies documents. It cannot change their content or precedence.

| Path | Class | Status | Purpose |
|---|---|---|---|
| `README.md` | Discovery | Current | Human landing page and repository state. |
| `AGENTS.md` | Discovery | Current | Mandatory agent entry point. |
| `llms.txt` | Discovery | Current | Compact machine-readable index. |
| `docs/STATUS.md` | Operational status | Verified through 2026-08-03; not release certification | Current host, Phase 0A, Phase 0B, maintenance-reboot, boundaries, and next permitted mission ledger. |
| `docs/INVARIANTS.md` | Normative | Frozen until owner-approved change | Highest architectural law. |
| `docs/ANTI-INVARIANTS.md` | Normative | Frozen until owner-approved change | Prohibited designs and claims. |
| `docs/SACRIFICES.md` | Normative | Append or amend before accepting a loss | Intentional limitations. |
| `docs/SCOPE.md` | Normative | Current | Product boundary. |
| `docs/ARCHITECTURE.md` | Normative | Current | SSH-native composition. |
| `docs/VARIANTS.md` | Normative | Current | Optional capability catalog. |
| `docs/SECURITY.md` | Normative | Current | Threat model and enforcement boundaries. |
| `docs/DECISIONS.md` | Normative | Append-only except explicit supersession | Architectural decision ledger. |
| `docs/BUILD.md` | Normative | Current | Implementation sequence. |
| `docs/CERTIFICATION.md` | Normative | Current | Release evidence requirements. |
| `docs/CHANGE-CONTROL.md` | Governance | Current | Procedure for changes to normative law. |
| `docs/reference/DEPENDENCIES.md` | Reference authority | Preserved release candidate plus verified implementation host; release not certified | Official dependency roles, exclusions, selection rationale, host binding, and lock interpretation. |
| `docs/reference/IMPLEMENTATION-HOST.md` | Operational reference | Original tuple verified 2026-08-01; maintenance continuation verified 2026-08-02; not release certification | Sanitized OVH VPS identity, kernel/fix binding, runtime primitives, boot policy, storage, readiness, and one-reboot maintenance continuation. |
| `assets/dependencies.lock.json` | Machine-readable lock | Preserved release candidate plus verified implementation-host binding; release not certified | Exact release candidate, implementation host, archive metadata, packages, versions, sources, digests, and configuration bindings. |
| `docs/reference/*` | Reference | Current | Terms, support policy, and search map. |
| `docs/research/FINAL-DELTA-RESEARCH-2026-07-31.md` | Research | Current dated audit | Final targeted upstream delta, corrections, and freeze recommendation; not independently normative. |
| `docs/research/OPERATIONAL-COMPLETENESS-STRATEGY-2026-07-31.md` | Research | Current dated strategy | Non-normative operational failure, update, backup, support, and device-upgrade strategy. |
| `docs/research/*` | Research | Historical/current rationale | Source-backed reasoning; not normative. |
| `evidence/checkpoints/host-kernel-transition-20260801/*` | Evidence | Verified immutable host checkpoint | Source, package, patch, runtime, rollback, cleanup, and host-tuple proof for the completed same-VPS transition. |
| `evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/*` | Evidence | Verified immutable Phase 0A checkpoint | Exact roots, dependency materialization, capacity, negative, cleanup, and absence proof; not product certification. |
| `evidence/checkpoints/phase-0b-reboot-repair-20260802/*` | Evidence | Certified disposable semantic-lab checkpoint | Boot A-B-C identity continuity, SSH reconnect, persistence, replay, negatives, and cleanup; not product or release certification. |
| `evidence/checkpoints/host-maintenance-reboot-20260802/*` | Evidence | Verified host-maintenance checkpoint | Exactly one retained-host reboot, clean return, repeated primitives, marker consumption, integrity, and zero-residue proof; not product or release certification. |
| `evidence/checkpoints/host-reboot-readback-20260803/*` | Evidence | Verified later reboot readback | Same-host readback after a later owner-initiated reboot, with locked kernel, service, primitive, package-health, and zero-residue continuity; not product or release certification. |
| `evidence/releases/*` | Evidence | Absent | Future complete Z release proof. |
| `.github/*` | Workflow | Current | Review and agent guidance. |

## Implementation status vocabulary

- **Documented:** specified in this repository.
- **Implemented:** present in source code and exercised locally.
- **Verified:** passed relevant tests with recorded results.
- **Certified:** passed the complete positive and negative requirements for an exact compatibility tuple.
- **Released:** certified artifacts are published with immutable identity.

These terms are not interchangeable. The implementation host, Phase 0A materialized inputs, and one-reboot maintenance continuation are verified for their recorded claims. Phase 0B is certified only for its named disposable semantic-lab claims. Phase 1, Z product runtime, durable product guest image, product machine lifecycle, and release certification have not started.

## Implementation root authority

- `reference/IMPLEMENTATION-ROOTS.md` — human-readable Phase 0A root and cleanup authority.
- `../assets/implementation-roots.json` — machine-readable authority.
- `../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/` — durable Phase 0A checkpoint evidence.
- `../evidence/checkpoints/phase-0b-reboot-repair-20260802/` — disposable Phase 0B semantic-lab certification evidence.
- `../evidence/checkpoints/host-maintenance-reboot-20260802/` — retained-host maintenance reboot evidence.
