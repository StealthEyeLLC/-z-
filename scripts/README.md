# Scripts

Scripts are thin implementation and verification helpers. They are not a controller, daemon, scheduler, runtime authority, product protocol, or substitute for the Z executable.

## Phase 0A helpers

- `check-phase-0a-capacity.sh` — fail-closed byte and inode reserve check. It supports explicitly marked simulated values for negative testing and emits one JSON result.
- `verify-phase-0a.sh` — read-only verification of the machine-readable root authority, exact installed Rust, builder closure and mmdebstrap, Cloud Hypervisor, firmware, empty roots, and product-absence gates.

Both helpers use strict shell mode, fixed authorities, no live-mirror fallback, no secret handling, no broad cleanup, no background persistence, and no service installation. Materialization remains separate from read-only verification.

## Phase 0B helper

- `verify-phase-0b.sh` — read-only, fail-closed verification of the repaired image digest, source basis, Phase 0A and blocker checksums, both Boot A-B-C runs, identity continuity, persistence, strict SSH and serial/vsock reconnect, regression gates, 60 negative cases, exact cleanup, and continued absence of product source, private keys, permanent services, and listeners.
