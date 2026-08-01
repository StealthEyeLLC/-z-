# Z Phase 0A Result

Status: **complete — implementation bootstrap and supply-chain materialization**

The exact candidate tuple `z-debian-13.6-amd64-ch53-v1` is materialized on the designated implementation host and is independently re-verifiable with `scripts/verify-phase-0a.py`.

Verified inputs and environment:

- Debian 13.6 amd64 snapshot `20260731T120000Z`, with signed metadata and the exact 212-package builder closure;
- isolated package-script-free builder root with `mmdebstrap 1.5.7` and `qemu-img 10.0.11`;
- Rust 1.97.1 for `x86_64-unknown-linux-gnu`, including an offline dependency-free edition-2024 build probe;
- Cloud Hypervisor v53.0 and the locked `CLOUDHV.fd` firmware at their exact sizes and SHA-256 digests;
- ext4 sparse-copy fallback, atomic same-directory publication, interruption behavior, and exact cleanup;
- retained `minimal-baby-z-reclaim-20260731` cleanup evidence and its deletion/certification chain;
- final host-state certification: deterministic global state unchanged, protected health green, and firewall policy structurally identical to retained post-reclamation evidence. Fail2Ban ban-set membership changed as live runtime state and is recorded separately.

No host-global package, account, service, firewall, boot, or runtime dependency was installed or changed. No VM was launched and no machine state was created. This checkpoint makes **no runtime or release-certification claim**. Phase 0B and Phase 1 remain unstarted.
