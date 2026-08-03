# Documentation Index

Status: **Canonical navigation document; not an authority override**

## 1. Governing hierarchy

Read these in order. Earlier documents control later ones.

| Order | Document | Purpose |
|---:|---|---|
| 1 | [INVARIANTS.md](INVARIANTS.md) | Required truths for every implementation and claim. |
| 2 | [ANTI-INVARIANTS.md](ANTI-INVARIANTS.md) | Prohibited directions and false shortcuts. |
| 3 | [SACRIFICES.md](SACRIFICES.md) | Explicitly accepted capability or convenience limits. |
| 4 | [SCOPE.md](SCOPE.md) | Product boundary and non-goals. |
| 5 | [ARCHITECTURE.md](ARCHITECTURE.md) | Normative SSH-native system design. |
| 6 | [VARIANTS.md](VARIANTS.md) | Supported optional capability profiles. |
| 7 | [SECURITY.md](SECURITY.md) | Threat model, trust boundaries, and controls. |
| 8 | [DECISIONS.md](DECISIONS.md) | Frozen architectural decisions. |
| 9 | [BUILD.md](BUILD.md) | Mandatory implementation order and gates. |
| 10 | [CERTIFICATION.md](CERTIFICATION.md) | Positive and negative proof required for release claims. |

## 2. Supporting governance and current state

- [MANIFEST.md](MANIFEST.md) — document inventory and authority classification.
- [STATUS.md](STATUS.md) — canonical operational status, completed host-transition ledger, maintenance obligations, and next recommended mission; not an authority override.
- [CHANGE-CONTROL.md](CHANGE-CONTROL.md) — procedure for amending architecture.

## 3. Reference

- [reference/GLOSSARY.md](reference/GLOSSARY.md) — canonical terms.
- [reference/COMPATIBILITY.md](reference/COMPATIBILITY.md) — support and certification tuple policy.
- [reference/DEPENDENCIES.md](reference/DEPENDENCIES.md) — official dependency authority and initial candidate tuple.
- [reference/IMPLEMENTATION-HOST.md](reference/IMPLEMENTATION-HOST.md) — sanitized settings and readiness record for the shared OVH implementation host.
- [`../assets/dependencies.lock.json`](../assets/dependencies.lock.json) — exact machine-readable dependency and asset lock.
- [reference/SEARCH-INDEX.md](reference/SEARCH-INDEX.md) — aliases and question-to-document map.

## 4. Research

Research explains why decisions were made but does not override governing law.

- [research/INDEX.md](research/INDEX.md)
- [research/SSH-RESEARCH-AND-ARCHITECTURE.md](research/SSH-RESEARCH-AND-ARCHITECTURE.md)
- [research/FINAL-DELTA-RESEARCH-2026-07-31.md](research/FINAL-DELTA-RESEARCH-2026-07-31.md)
- [research/OPERATIONAL-COMPLETENESS-STRATEGY-2026-07-31.md](research/OPERATIONAL-COMPLETENESS-STRATEGY-2026-07-31.md) — non-normative operational failure and upgrade strategy.
- [research/SOURCES.md](research/SOURCES.md)
- [research/CHANGES-FROM-ORIGINAL.md](research/CHANGES-FROM-ORIGINAL.md)

## 5. Repository-operational documents

- [`../AGENTS.md`](../AGENTS.md) — agent entry point.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — contribution and review rules.
- [`../UPLOAD-TO-GITHUB.md`](../UPLOAD-TO-GITHUB.md) — completed documentation migration record.
- [`../evidence/README.md`](../evidence/README.md) — verified host checkpoint and future release-evidence layout.
- [`../assets/README.md`](../assets/README.md) — release-candidate and implementation-host lock semantics.

## 6. State declaration

The same-VPS implementation-host kernel transition remains verified under `evidence/checkpoints/host-kernel-transition-20260801/`. Phase 0A is complete under `evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/`, Phase 0B is certified only for its disposable semantic-lab claims under `evidence/checkpoints/phase-0b-reboot-repair-20260802/`, the retained-host one-reboot maintenance continuation is verified under `evidence/checkpoints/host-maintenance-reboot-20260802/`, and the later owner-initiated reboot readback is verified under `evidence/checkpoints/host-reboot-readback-20260803/`. The exact root authority is `reference/IMPLEMENTATION-ROOTS.md`. Z product source, Phase 1, a durable product guest image, a product machine lifecycle, and release certification have not started. Until complete end-to-end release evidence exists under `evidence/releases/`, Z has no certified runtime release.
