# -Z- Documentation Migration Record

Target repository: `StealthEyeLLC/-z-`
Original target branch: `main`
Current clean-room implementation branch: `build/z-v1-cleanroom`

## Completion status

The initial documentation migration is complete. The following formerly manual files are present at their canonical paths:

1. `docs/INVARIANTS.md`
2. `docs/ANTI-INVARIANTS.md`
3. `docs/ARCHITECTURE.md`
4. `docs/VARIANTS.md`
5. `docs/CERTIFICATION.md`
6. `docs/research/SSH-RESEARCH-AND-ARCHITECTURE.md`

The repository identity has been normalized to **-Z-** as the product mark, **Z** as the spoken name, `z` as the CLI, and `StealthEyeLLC/-z-` as the canonical repository.

## Verification record

The completed initialization requires:

1. Every link in `docs/INDEX.md` resolves.
2. All six canonical paths above exist on `main`.
3. No stale former repository or product identity remains.
4. `StealthEyeLLC/-z-`, `-Z-`, `ProxyUseFdpass`, `AF_VSOCK`, `Network None`, and `zero Z processes` remain discoverable in the appropriate documents.
5. At initialization, `evidence/README.md` stated that no implementation evidence existed. That historical condition was superseded on 2026-08-01 by the verified host-kernel checkpoint; it did not create Z product evidence.
6. Every entry in `SHA256SUMS.txt` matches the current normalized documentation and control-file set.

The initial documentation migration remains complete. The implementation host is now verified, while Phase 0A and Z product implementation have not started. Current status is recorded in `docs/STATUS.md`.
