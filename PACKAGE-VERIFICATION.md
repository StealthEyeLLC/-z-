# Repository Documentation and Checkpoint Verification

- Canonical repository: `StealthEyeLLC/-z-`
- Authoritative branch: `build/z-v1-cleanroom`
- Product mark: **-Z-**
- Spoken name: **Z**
- CLI: `z`
- Current repository files including checksum manifest: **55**
- Markdown documents: **44**
- Root checksum entries: **54**
- Pending manual uploads: **0**
- Documentation initialization: **complete**
- Identity normalization: **complete**
- Same-VPS host-kernel transition: **verified**
- Implementation-host tuple: `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`
- Running/default kernel: `6.8.0-9001-generic`
- Tested rollback kernel: `6.8.0-136-generic`
- Host-transition checkpoint commit: `96853e15f7a8cab1efc178d03a4d3e027b0b28cc`
- Host-transition checkpoint tree: `b4308f82a5329542450de3a4cbfabf3300414068`
- Phase 0A status: **complete**
- Phase 0B status: **not started**
- Phase 1 status: **not started**
- Z product implementation status: **not started**
- Z release status: **not certified**

`SHA256SUMS.txt` covers every current repository file except itself, including governing documents, operational status, the machine-readable lock, workflow documents, and the immutable host-transition evidence checkpoint.

The complete current-state ledger is `docs/STATUS.md`. The root checksum manifest must be regenerated after any later content change.

## Phase 0A verification

Run `scripts/verify-phase-0a.sh` on the locked implementation host. Verify `evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/SHA256SUMS.txt`, then verify the repository root `SHA256SUMS.txt`. The helper is read-only and fails closed on root, toolchain, builder, asset, empty-root, process, source, Cargo, or disk drift.
