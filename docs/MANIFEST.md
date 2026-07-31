# Documentation Manifest

Status: **Canonical inventory; navigation only**

This file classifies documents. It cannot change their content or precedence.

| Path | Class | Status | Purpose |
|---|---|---|---|
| `README.md` | Discovery | Current | Human landing page and repository state. |
| `AGENTS.md` | Discovery | Current | Mandatory agent entry point. |
| `llms.txt` | Discovery | Current | Compact machine-readable index. |
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
| `docs/reference/*` | Reference | Current | Terms, support policy, and search map. |
| `docs/research/*` | Research | Historical/current rationale | Source-backed reasoning; not normative. |
| `evidence/*` | Evidence | Empty at initialization | Future checkpoint and release proof. |
| `.github/*` | Workflow | Current | Review and agent guidance. |

## Implementation status vocabulary

- **Documented:** specified in this repository.
- **Implemented:** present in source code and exercised locally.
- **Verified:** passed relevant tests with recorded results.
- **Certified:** passed the complete positive and negative requirements for an exact compatibility tuple.
- **Released:** certified artifacts are published with immutable identity.

These terms are not interchangeable. At initialization, the architecture is documented; no runtime is implemented or certified.
