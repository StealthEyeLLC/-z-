# Phase 0A Tests

Status: **PASS**

1. Repository, branch, commit, tree, origin, remote, historical branch, and clean-start gates passed.
2. Root and preserved host-transition checksum manifests passed before mutation.
3. Live implementation-host tuple, kernels, boot policy, system health, retained services, and package health matched.
4. Root collision, ownership, mount, symlink, mode, capacity, and cleanup gates passed.
5. Debian InRelease digests, signatures, primary fingerprints, signed index declarations, and exact index digests passed.
6. Independent direct set and 212-package closure equality passed.
7. All 212 package files passed signed-index identity, size, SHA-256, metadata, atomic acquisition, and idempotent replay checks.
8. The isolated 212-package builder payload and truthful dpkg database matched the lock; exact mmdebstrap version, help, and Perl syntax checks passed.
9. Rust manifest and component digests passed; absolute-path identities, target, sysroot, Edition 2024 compile/run, rustfmt, and clippy identity passed.
10. Cloud Hypervisor and firmware size, SHA-256, upstream tag/commit, mode, ownership, link, ELF/static, and final-byte checks passed.
11. Reflink refusal, sparse fallback, hole preservation, interruption safety, retry, and cleanup tests passed.
12. Capacity positive, simulated byte refusal, and simulated inode refusal tests passed before mutation.
13. All 35 required negative tests passed.
14. Absence gates passed: no product source, Cargo metadata, guest disk, machine, VMM process, service, listener, TAP, or mount.
15. Host APT sources, dpkg status, global Rust state, boot state, firewall, networking, Caddy, SSH, and retained services were not mutated.

The sole `.img`-suffix file is the locked GRUB package payload `usr/lib/grub/x86_64-efi/kernel.img`; it is not a Z guest disk.
