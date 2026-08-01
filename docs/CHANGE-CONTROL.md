# Change Control

Status: **Supporting governance procedure**

## 1. When this process is required

Use this process for any proposal that adds, removes, weakens, or reclassifies a normative requirement, anti-invariant, sacrifice, architecture boundary, variant, security control, build gate, or certification claim.

## 2. Required change record

Every architectural change must state:

1. The exact current behavior or rule.
2. The exact proposed behavior or rule.
3. The owner-visible capability added or removed.
4. Why native Linux, OpenSSH, systemd, Cloud Hypervisor, or an existing standard cannot already provide the result.
5. New permanent processes, privileges, durable state, protocols, dependencies, or trust boundaries.
6. Complexity deleted or made unnecessary by the change.
7. Failure and recovery behavior.
8. Positive and negative certification additions.
9. Affected documents in precedence order.
10. Explicit owner approval.

## 3. Required document updates

A change must update every affected file in one coherent review. At minimum inspect:

- `INVARIANTS.md`
- `ANTI-INVARIANTS.md`
- `SACRIFICES.md`
- `SCOPE.md`
- `ARCHITECTURE.md`
- `VARIANTS.md`
- `SECURITY.md`
- `DECISIONS.md`
- `BUILD.md`
- `CERTIFICATION.md`
- `reference/SEARCH-INDEX.md`

## 4. Decision recording

Accepted decisions receive the next `D###` entry in `DECISIONS.md`. A superseded decision remains visible and points to its replacement. History is not silently rewritten.

## 5. No implementation-first amendment

Code, tests, benchmarks, convenience, or upstream behavior cannot amend governing law retroactively. A conflicting implementation is a defect until the owner explicitly approves the architectural change.

## 6. Operational and host-profile changes

A change affecting concurrency, durable commit boundaries, disk-space preflight, update/rollback, backup/restore, support collection, implementation tooling, certification-host eligibility, or device passthrough must identify:

- the exact new process, descriptor, path, durable state, privilege, network authority, cleanup authority, and failure mode;
- how prior committed truth survives interruption and capacity exhaustion;
- how the change affects zero-at-rest;
- whether the implementation-host profile or compatibility tuple changes;
- the positive and negative tests added to `docs/CERTIFICATION.md`;
- whether the claim is baseline, variant, research, or implementation-host-only.

A point-in-time host or strategy document cannot amend normative law by itself.

## 7. Completed implementation-host transitions

A completed host transition that does not alter product architecture must still update, in one coherent checkpoint:

1. `docs/STATUS.md` with the full result, boundaries, maintenance obligations, and next recommended mission.
2. `docs/reference/IMPLEMENTATION-HOST.md` with exact point-in-time host facts and refresh rules.
3. `docs/reference/DEPENDENCIES.md` and `assets/dependencies.lock.json` with distinct implementation-host identity.
4. `docs/BUILD.md`, `docs/CERTIFICATION.md`, `docs/SECURITY.md`, and `docs/reference/COMPATIBILITY.md` with honest claim boundaries.
5. `docs/DECISIONS.md` when the owner accepts a durable operational choice or maintenance obligation.
6. `evidence/` with digest-verifiable proof and exact repository checkpoint identities.
7. Discovery, search, manifest, folder-tree, and checksum documents whose prior state declarations became stale.

Historical evidence is not rewritten merely to improve later prose. A later documentation checkpoint must point to it and preserve its original identities.
