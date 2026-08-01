# Contributing to -Z-

## Read before changing anything

Start with `AGENTS.md`, `docs/INDEX.md`, and `docs/STATUS.md`. Architecture changes require `docs/CHANGE-CONTROL.md` and explicit owner approval. Implementation work must also verify the current implementation-host tuple before relying on host state.

## Contribution classes

- **Documentation correction:** fixes wording without changing behavior.
- **Operational-status update:** records a completed host or implementation checkpoint without claiming product certification.
- **Research addition:** adds source-backed information under `docs/research/`.
- **Implementation change:** must map to an existing build phase and certification requirement.
- **Architecture change:** changes normative behavior and requires the full change-control record.

## Pull request requirements

Every change must state:

- What user-visible capability or correctness property changes.
- Which governing documents apply.
- Tests or evidence added.
- New privileges, processes, durable state, protocols, dependencies, or trust boundaries.
- Cleanup and recovery behavior.
- Whether any sacrifice is introduced.

Documentation must never claim a feature is implemented or certified without matching repository evidence.
