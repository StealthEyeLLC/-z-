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
