# Assets

This directory contains machine-readable authority and provenance for selected dependencies. Large binaries are not committed to Git.

- `dependencies.lock.json` is the exact candidate dependency lock.
- `phase-0a-materialization.json` binds that lock to the verified host-side Debian closure, isolated builder root, Rust toolchain, Cloud Hypervisor, firmware, filesystem behavior, and protected cleanup evidence.

The Phase 0A manifest records candidate materialization, not runtime or release certification. A mismatched asset must fail closed.

<!-- phase-0b-checkpoint -->
## Phase 0B

`phase-0b-semantics.json` records the candidate tuple and the exact native SSH, compatibility relay, credential, systemd, serial, identity, and zero-controller semantics. It contains no disk image or secret.
