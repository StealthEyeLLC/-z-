# Current Status — Verified Host Kernel Transition and Phase 0A Readiness

Status: **Canonical operational status; implementation-host-only; not release certification**
Status date: **2026-08-01**
Authoritative branch: **`build/z-v1-cleanroom`**
Host-transition checkpoint commit: **`96853e15f7a8cab1efc178d03a4d3e027b0b28cc`**
Host-transition checkpoint tree: **`b4308f82a5329542450de3a4cbfabf3300414068`**

## 1. Executive result

1. The same retained OVH VPS was transitioned from Ubuntu kernel `6.8.0-136-generic` to the verified side-by-side kernel `6.8.0-9001-generic`.
2. The replacement was built from Ubuntu Noble source package `linux 6.8.0-136.136` with the exact upstream KVM fix for CVE-2026-53359 applied.
3. The host completed a real controlled reboot and returned on the replacement kernel with the required KVM, AF_VSOCK, TAP, descriptor-passing, systemd, loop, namespace, Landlock, seccomp, and OpenSSH primitives working.
4. The replacement kernel is the persistent GRUB default.
5. Kernel `6.8.0-136-generic` remains installed as the tested explicit rollback entry.
6. The resulting implementation-host tuple is `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`.
7. The preserved guest/reference candidate remains separately identified as `z-debian-13.6-amd64-ch53-v1`.
8. The host-kernel blocker is closed for implementation-host purposes.
9. Phase 0A has not started.
10. No Z product source, guest disk, machine, or Cloud Hypervisor runtime was created or launched.

## 2. Mission authority and boundaries

1. Baby was used only as the authorized private implementation executor.
2. The connected Z GitHub Authority and ordinary authenticated Git transport were used for repository publication and independent remote verification.
3. Baby, GitHub applications, credentials, receipts, and implementation jobs are not Z components or runtime dependencies.
4. No Termius session, user-supplied SSH path, second server, VPS reimage, operating-system replacement, or control-plane migration was used.
5. The historical branch `build/z-v1` was preserved unchanged at `4e17ead436949b32d245c15df5bcf2418f2f8968`.
6. The mission stopped before clean-room Phase 0A, exactly as authorized.

## 3. Starting repository checkpoint

1. The pre-transition authorization checkpoint was commit `9a9acc00a165edb1cb86a4f34e8058badfb3f881`.
2. Its tree was `6293a4aff1a3863d96eea45068222ac42f74fcff`.
3. The authoritative branch was and remains `build/z-v1-cleanroom`.
4. The authoritative workspace was `/var/lib/baby-quirt/workspaces/dash-z-build-plan-current-20260731`.
5. The origin was verified as `https://github.com/StealthEyeLLC/-z-.git`.

## 4. Kernel selection and why it is the correct plan

1. The replacement did not jump to an unrelated mainline or HWE kernel.
2. It retained the same Ubuntu Noble 6.8 source family already proven compatible with the VPS.
3. The exact base source was Ubuntu Noble `linux 6.8.0-136.136`.
4. The exact upstream fix commit was `81ccda30b4e83d8f5cc4fd50503c44e3a33abfeb`.
5. The replacement package version was `6.8.0-9001.1+zcve2026533591`.
6. The installed kernel release was `6.8.0-9001-generic`.
7. A separate ABI and side-by-side package set avoided overwriting the known-good rollback kernel.
8. The approach satisfies the original plan's actual requirements: a fixed KVM isolation boundary, compatible host primitives, a real reboot, reproducible provenance, explicit rollback, and a locked implementation-host identity.
9. The locally built Ubuntu-compatible package is not a downgrade from the original plan. It is the least-disruptive realization of that plan while a suitable stock Canonical binary was unavailable for the exact required fix state.
10. This choice creates a maintenance obligation: the local package remains part of the locked tuple until a later owner-approved tuple transition deliberately replaces it.

## 5. Supply-chain and patch binding

1. Ubuntu source orig SHA-256: `26512115972bdf017a4ac826cc7d3e9b0ba397d4f85cd330e4e4ff54c78061c8`.
2. Ubuntu source delta SHA-256: `ccce6d47f36bc749d69a5faa41237c3269e5345d3852d6afe868a5629ac8c316`.
3. Ubuntu source DSC SHA-256: `9bf54e2fc501c2f37b48d03dc268ef601e911f9be15df5cfb1e5d9f8d6174fba`.
4. Exact fix patch SHA-256: `84d5f450aaff799e1e7cf9392a137cb9afc9702baa3c6c5dbc9343e6d6c05c6c`.
5. The pristine MMU source and one-hunk fix diff were preserved.
6. Reverse-apply and forward-reapply checks proved that the source contained the fix exactly once.
7. Signed Ubuntu source-index and package provenance were retained with the durable host evidence.

## 6. Build and package result

1. Thirteen Debian packages were built from the bound Ubuntu source and patch.
2. Four packages were installed as the minimum side-by-side runtime set:
   1. `linux-headers-6.8.0-9001`;
   2. `linux-headers-6.8.0-9001-generic`;
   3. `linux-modules-6.8.0-9001-generic`;
   4. `linux-image-unsigned-6.8.0-9001-generic`.
3. KVM modules package SHA-256: `98f184d88d076c5d3458eb921a92a2ebb2c44119b71df3191b9607da13ea88ed`.
4. Installed compressed `kvm.ko` SHA-256: `27c53953087080c7baf9119d62f2e61ef3a81f2faed12eb086359b5cf40580b8`.
5. Decompressed KVM ELF SHA-256: `dc6faf80d06f5314c259b59c8be40faaf6d32449645d4110344a1379909ea7c9`.
6. KVM ELF build ID: `1a9bcf21095ea9daa3a8277907a9beddb9274273`.
7. KVM srcversion: `403F1A311A13D8B84CC56BF`.
8. The installed and running KVM module was proven byte-identical to the validated package output.
9. The loaded module srcversion matched the installed module.

## 7. Boot transition and rollback

1. The pre-transition boot, GRUB, initramfs, package, service, storage, KVM, and rollback state was captured before mutation.
2. The candidate kernel was first armed as a one-time boot selection while kernel 136 remained the persistent safety default.
3. Initramfs and GRUB entries were verified before reboot.
4. The controlled reboot returned the same host on `6.8.0-9001-generic`.
5. The post-transition boot ID was `b6e10e21-9737-4ded-ad1e-a437eea41ace`.
6. After runtime verification, `6.8.0-9001-generic` was promoted to the persistent GRUB default.
7. `6.8.0-136-generic` remains installed and selectable as the tested rollback kernel.
8. The one-time boot entry was consumed and `next_entry` is empty.
9. A second reboot was neither required nor authorized.

## 8. Runtime host proof

The running replacement kernel passed all of the following implementation-host checks:

1. KVM API version `12`.
2. KVM VM creation.
3. KVM vCPU creation.
4. Loaded `/dev/kvm` and `kvm_intel` path.
5. `/dev/vhost-vsock` availability.
6. Explicit AF_VSOCK bind and listen.
7. Transient TAP creation and exact cleanup through `/dev/net/tun`.
8. Unix `SCM_RIGHTS` descriptor transfer.
9. OpenSSH `ProxyUseFdpass=yes` support.
10. Transient systemd unit lifecycle.
11. Loop-device attach and detach.
12. Mount-namespace creation.
13. Landlock ABI `4`.
14. seccomp and seccomp-filter availability.

These are host-capability proofs only. They do not prove Z product behavior, Cloud Hypervisor behavior, a guest boot path, or release compatibility.

## 9. Service and package health after reboot

1. `baby-quirt.socket` was active.
2. `baby-quirt-mcp.service` was active.
3. `ssh.socket` was active.
4. `caddy.service` was active.
5. systemd reported state `running`.
6. Failed systemd units: `0`.
7. NTP synchronization: `yes`.
8. Reboot required: `false`.
9. `dpkg --audit`: clean.
10. APT repair simulation required no changes.

## 10. Cleanup and retained evidence

1. Twenty-seven temporary build-helper packages were removed after verification.
2. Temporary build trees, proof units, mounts, and staging paths were removed.
3. Transition-owned data removed: `39,439,724,544` bytes.
4. Durable host evidence remains under `/var/lib/z-kernel-transition/20260801`.
5. Durable evidence size: `968,757,248` bytes.
6. Durable evidence manifest entries: `208` files.
7. Durable evidence manifest SHA-256: `696cd3dadebf8a4c25a77299091fde713de6ed26a105b4aa70e4f2cce9775db4`.
8. Repository-safe proof remains under `evidence/checkpoints/host-kernel-transition-20260801/`.
9. Cleanup removed only transition-owned material and preserved unrelated host and project state.

## 11. Storage state at tuple capture

1. Root filesystem: `ext4`.
2. Reflink support: unavailable.
3. Root total: `102,888,095,744` bytes.
4. Root used: `11,911,262,208` bytes.
5. Root available: `90,960,056,320` bytes.
6. `/boot` available: `680,804,352` bytes.
7. Phase 0A and later disk work must use the documented sparse-copy fallback and operation-specific capacity refusal rather than assuming reflink.

## 12. Repository checkpoint and remote verification

1. Host-transition checkpoint commit: `96853e15f7a8cab1efc178d03a4d3e027b0b28cc`.
2. Host-transition checkpoint tree: `b4308f82a5329542450de3a4cbfabf3300414068`.
3. Parent commit: `9a9acc00a165edb1cb86a4f34e8058badfb3f881`.
4. Commit subject: `checkpoint: verify Noble KVM host kernel transition`.
5. The branch was fast-forwarded to `build/z-v1-cleanroom`.
6. An explicit remote fetch proved the remote branch resolved to the same commit and tree.
7. GitHub independently resolved the commit object and compared it one commit ahead of the parent with zero commits behind.
8. GitHub independently fetched the remote `RESULT.md` blob `60a16c6835ef4365af7acbd3eca4e9da880abe96`.
9. GitHub independently fetched the remote `HOST-TUPLE.json` blob `ad9f7b257d336e6ee07c808f88ed611be205539f`.
10. Local committed blob identities matched the independently fetched GitHub blobs.
11. The worktree was clean after publication and verification.

## 13. What was deliberately not done

1. Phase 0A was not started.
2. No Rust implementation root was created for Z.
3. No Z product source was written.
4. No Debian guest image or raw machine disk was built.
5. No Z machine directory or identity was created.
6. No Cloud Hypervisor binary was launched.
7. No guest was booted.
8. No Z SSH path was exercised.
9. No product certification claim was made.
10. No historical branch was rewritten.

## 14. Original-plan equivalence decision

1. The completed result is accepted as the successful realization of the original host plan, not a fallback architecture.
2. The security requirement is met by the exact CVE-2026-53359 KVM fix binding.
3. The compatibility requirement is met by retaining the proven Noble 6.8 source family and passing the real post-reboot primitive suite.
4. The rollback requirement is stronger than an in-place package replacement because the prior kernel remains installed under a separate ABI.
5. The reproducibility requirement is met by source, patch, package, module, boot, runtime, cleanup, and repository evidence.
6. The only material difference from using a future stock Canonical binary is maintenance ownership of the locally built package.
7. That difference is explicitly recorded and does not reduce the verified implementation-host capability.

## 15. Current maintenance obligations

1. Do not silently upgrade, replace, or remove either kernel.
2. Do not remove `6.8.0-136-generic` until a later rollback policy explicitly supersedes it.
3. Treat any change to the running kernel, KVM modules, boot policy, CPU exposure, host distribution, package set, filesystem, Landlock, seccomp, OpenSSH, or retained control-plane state as implementation-host tuple drift.
4. Recapture the host profile and create a new tuple before relying on drifted state.
5. A future Canonical kernel containing the required fix may replace the local package only through a deliberate, evidence-backed tuple transition.
6. Host nested-KVM capability being available does not authorize nested virtualization inside the Z baseline. The pinned Cloud Hypervisor configuration must still set and prove `nested=off`.
7. Before every implementation mission, verify the running host still matches the locked tuple.

## 16. Recommended next mission — Phase 0A only

The next mission should execute Phase 0A exactly and stop before Phase 0B or Phase 1:

1. Reconfirm `build/z-v1-cleanroom`, the exact source commit/tree, origin, and a clean workspace.
2. Reconfirm the running implementation host still matches `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`.
3. Define exact absolute source, build, asset, machine, runtime, cache, staging, and evidence roots.
4. Record owner, group, mode, cleanup authority, capacity policy, and minimum failure reserve for every root.
5. Verify the locked Debian Snapshot `InRelease`, signing keys, package indexes, and package closures before extraction or installation.
6. Materialize Rust `1.97.1` in an isolated implementation root and verify its channel-manifest digest, compiler identity, target, and edition.
7. Materialize the locked Cloud Hypervisor v53.0 binary and matching EDK2 `CLOUDHV.fd`; verify size, digest, executable identity, and immutable provenance.
8. Materialize the locked `mmdebstrap` package and builder closure from the Debian snapshot.
9. Record the host's no-reflink behavior and validate the sparse-copy fallback and interruption cleanup policy.
10. Prove that declared temporary space, durable results, rollback copies, evidence, and failure reserve fit simultaneously before any large mutation.
11. Keep Baby, GitHub applications, credentials, receipts, and implementation-only tooling outside release artifacts and all Z runtime paths.
12. Produce Phase 0A evidence, commit it as one clean checkpoint, fast-forward push it, and independently verify the remote objects.
13. Stop after the exact build environment and locked inputs exist and verify.
14. Do not create a guest disk, create a machine, launch Cloud Hypervisor, or claim a product checkpoint during Phase 0A.

## 17. Stop and escalation conditions for Phase 0A

Phase 0A must fail closed and preserve prior truth if any of these occur:

1. The source commit/tree or branch does not match authorization.
2. The implementation-host tuple has drifted.
3. A Debian signature, index hash, package identity, Rust manifest, Cloud Hypervisor binary, firmware, or builder-closure digest does not match the lock.
4. Required storage and failure reserve cannot fit simultaneously.
5. A root has the wrong owner, mode, filesystem behavior, or cleanup authority.
6. A tool would be inherited from ambient host state instead of the locked implementation root.
7. A cleanup operation cannot prove exact ownership.
8. Publication would require a non-fast-forward update or rewriting preserved history.

## 18. Path after Phase 0A

1. Phase 0B should prove the difficult transport and credential semantics before broad implementation: descriptor handoff, stdio compatibility, prebound host keys, static AF_VSOCK `sshd -i`, SMBIOS credentials, explicit `nested=off`, exact systemd argv, and serial reconnect.
2. Phase 1 should then build the first real persistent machine and prove root access, persistence, reboot, authenticated reconnect, recovery, and zero Z processes at rest.
3. No architecture scaffold, schema, provider abstraction, or mock-only test should be treated as the first product checkpoint.

## 19. Authoritative references

1. [`BUILD.md`](BUILD.md) — normative phase order.
2. [`CERTIFICATION.md`](CERTIFICATION.md) — exact evidence required for release claims.
3. [`DECISIONS.md`](DECISIONS.md) — accepted architectural and implementation-host decisions.
4. [`reference/IMPLEMENTATION-HOST.md`](reference/IMPLEMENTATION-HOST.md) — exact host tuple and refresh rule.
5. [`reference/DEPENDENCIES.md`](reference/DEPENDENCIES.md) — preserved release candidate and implementation-host dependency binding.
6. [`../assets/dependencies.lock.json`](../assets/dependencies.lock.json) — machine-readable lock.
7. [`../evidence/checkpoints/host-kernel-transition-20260801/RESULT.md`](../evidence/checkpoints/host-kernel-transition-20260801/RESULT.md) — checkpoint result.
8. [`../evidence/checkpoints/host-kernel-transition-20260801/HOST-TUPLE.json`](../evidence/checkpoints/host-kernel-transition-20260801/HOST-TUPLE.json) — exact captured tuple.
