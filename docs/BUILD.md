# Build Plan — SSH-Native Z

Status: **Normative implementation order**

## Current implementation readiness

Point-in-time host facts are recorded in [`reference/IMPLEMENTATION-HOST.md`](reference/IMPLEMENTATION-HOST.md). They route implementation work and do not certify the selected release tuple.

As of `2026-08-01T19:08:00Z`:

- The authoritative clean-room branch is `build/z-v1-cleanroom`; historical `build/z-v1` remains unchanged.
- The verified implementation-host tuple is `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`.
- The retained OVH VPS remains Ubuntu 24.04.4 LTS and is running `6.8.0-9001-generic` from package `6.8.0-9001.1+zcve2026533591`.
- The kernel was built from Ubuntu Noble `linux 6.8.0-136.136` with CVE-2026-53359 fix commit `81ccda30b4e83d8f5cc4fd50503c44e3a33abfeb` and exact digest-bound source/package/module evidence.
- KVM API 12, VM/vCPU creation, AF_VSOCK, TAP, Unix descriptor passing, transient systemd, loop devices, mount namespaces, Landlock ABI 4, seccomp, and OpenSSH fd-passing passed on the running kernel.
- Baby, SSH, Caddy, package health, NTP, and systemd returned cleanly after the controlled reboot; failed units are zero.
- `6.8.0-9001-generic` is the persistent GRUB default. `6.8.0-136-generic` remains installed as the tested explicit rollback entry.
- The root filesystem is ext4 without reflink; `90,960,056,320` bytes are available on `/` and `680,804,352` bytes on `/boot`.
- Transition-owned build helpers, temporary units, mounts, and large staging trees were removed after durable evidence and package preservation.
- The preserved release candidate remains `z-debian-13.6-amd64-ch53-v1`; it is distinct from the Ubuntu implementation-host tuple.
- Clean-room Phase 0A is complete and verified.
- Exact roots and materialized inputs are recorded in `reference/IMPLEMENTATION-ROOTS.md` and `../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/`.
- Phase 0B, Phase 1, and product source have not started.
- The verified host-transition repository checkpoint is commit `96853e15f7a8cab1efc178d03a4d3e027b0b28cc`, tree `b4308f82a5329542450de3a4cbfabf3300414068`.
- The complete current-state and next-step ledger is [`STATUS.md`](STATUS.md).

Missing ambient binaries remain materialization work, not authority blockers. Implementation MUST use locked identities and MUST NOT silently inherit global host versions.

## Same-VPS host-kernel gate — PASSED

Decision date: `2026-08-01`.

The authorized gate completed on the existing OVH VPS without a reimage, operating-system replacement, second server, Baby migration, or control-plane relocation.

Completed proof:

1. The exact pre-transition boot, GRUB, initramfs, KVM, Baby, Caddy, SSH, storage, and rollback state was captured.
2. Ubuntu Noble `linux 6.8.0-136.136` and fix commit `81ccda30b4e83d8f5cc4fd50503c44e3a33abfeb` were source- and digest-bound.
3. The candidate preserved the required Z host primitives and all modules loaded on the rollback boot.
4. `6.8.0-9001-generic` was installed side-by-side; `6.8.0-136-generic` was not removed or overwritten.
5. Initramfs, GRUB entries, package health, explicit rollback selection, and one-time candidate selection were verified before reboot.
6. One controlled reboot returned the same VPS on `6.8.0-9001-generic` with boot ID `b6e10e21-9737-4ded-ad1e-a437eea41ace`.
7. Runtime KVM, AF_VSOCK, TAP, descriptor passing, systemd, loop, namespace, Landlock, seccomp, OpenSSH, service, and cleanup gates passed.
8. The actual host tuple was recorded in `assets/dependencies.lock.json` and the repository evidence checkpoint.
9. `6.8.0-9001-generic` is now the persistent default; kernel 136 remains the tested rollback entry.

This gate authorized the now-complete Phase 0A mission on the same VPS. It does not waive Phase 0B semantic/negative gates, Phase 1 authorization, or release certification.

## Next recommended mission

The next permitted mission is Phase 0B only after separate authorization. It MUST begin from the exact Phase 0A checkpoint, reconfirm the authoritative branch, clean workspace, materialized inputs, roots, capacity reserve, and unchanged implementation-host tuple, and stop before Phase 1. Phase 0B may prove semantics but MUST NOT create the first real machine unless a later Phase 1 mission is separately authorized.

The full recommended sequence and fail-closed stop conditions are recorded in [`STATUS.md`](STATUS.md). That operational status document does not override the normative phase definitions below.

## Dependency gate

Before source implementation or asset construction:

1. Verify [`reference/DEPENDENCIES.md`](reference/DEPENDENCIES.md) and [`../assets/dependencies.lock.json`](../assets/dependencies.lock.json) agree.
2. Verify signed Debian snapshot metadata, package-index hashes, Cloud Hypervisor, firmware, and Rust channel-manifest digests.
3. Use candidate tuple `z-debian-13.6-amd64-ch53-v1` without a live-mirror, backport, or floating-version substitution.
4. Treat any version or digest change as a new candidate tuple.
5. Record complete transitive package and Cargo closures when they first exist.

Selection is not certification.

## Phase 0A — implementation bootstrap

Perform this before the first large mutation:

1. Reconfirm the authoritative source commit/tree and a clean workspace.
2. Select and record exact absolute source, build, asset, machine, runtime, cache, staging, and evidence roots, including owner, mode, cleanup authority, and minimum free-space policy.
3. Verify the locked Debian `InRelease`, package indexes, and package closure before installing or extracting anything.
4. Materialize the locked Rust `1.97.1` toolchain in the implementation build root and prove the channel-manifest digest, compiler identity, target, edition, and absence of undeclared crates.
5. Materialize the locked Cloud Hypervisor v53.0 binary and matching EDK2 `CLOUDHV.fd` in the implementation asset root; verify size, digest, executable identity, and immutable source provenance before use.
6. Materialize the locked `mmdebstrap` package and its declared builder closure from the Debian snapshot. Do not substitute the host's `debootstrap` merely because it is already installed.
7. Use independent raw disks and the locked builder closure. `qemu-img` is not an ambient prerequisite and MUST NOT become a dependency without a lock and tuple change.
8. Defer `passt` materialization until the connected profile is implemented. Phase 1 uses Network None and does not require a guest NIC.
9. Detect reflink honestly. On the current host, use sparse-copy fallback and verify logical size, allocated size, contents, interruption behavior, and cleanup.
10. Refuse any operation whose declared temporary space, durable result, rollback copy, evidence, and failure reserve do not fit simultaneously.
11. Keep Baby, GitHub applications, CI workers, repository credentials, and implementation-only tooling outside Z release artifacts, installed files, guest images, runtime authority, and offline operation.

Phase 0A completion means the exact selected inputs and build environment exist and verify. It is not a product checkpoint.

## Phase 0B — semantics gates

1. Prove native OpenSSH descriptor handoff against the Cloud Hypervisor vsock mux.
2. Prove compatibility stdio relay against one embedded SSH client.
3. Prove strict prebound host-key lookup.
4. Prove static AF_VSOCK `sshd -i` service.
5. Prove SMBIOS system credentials through the private VMM API, including OEM-string count/size preflight and exact binary round-trip; do not depend on `vmm.notify_socket` for Cloud Hypervisor v52.0/v53.0.
6. Reverify that the running implementation host still matches the locked kernel/fix tuple for applicable KVM isolation advisories, including CVE-2026-53359 on x86; explicitly configure the pinned Cloud Hypervisor x86 equivalent of `nested=off` and prove the effective guest CPU exposure.
7. Prove exact noninteractive systemd argv and result semantics.
8. Prove serial reconnect across reboot.

No architecture scaffold counts as completion without a real booted computer.

## Phase 1 — first usable computer

Implement only:

- exact asset verification;
- recorded implementation-root layout;
- machine-scoped mutation lock and durable staging/commit boundaries;
- machine directory and independent raw disk;
- identity generation;
- Network None guest configuration;
- transient host systemd VMM service;
- fail-closed seccomp/Landlock confinement with exact pre-opened descriptor inventory;
- SMBIOS credentials;
- static guest SSH;
- native descriptor-pass connector;
- bare root shell;
- persistent change;
- guest reboot and authenticated reconnect;
- graceful stop and abrupt VMM recovery;
- zero Z processes at rest.

The implementation order inside this phase is:

1. Create the exact host layout and failure-headroom ledger.
2. Build the deterministic Debian guest image with no reusable machine identity and no Z guest binary.
3. Create one machine directory with UUID, host key, owner authorization, configuration, disk, and crash-safe metadata.
4. Launch the pinned Cloud Hypervisor through one transient systemd unit with `nested=off`, exact assets, private API/vsock/serial sockets, and mandatory confinement.
5. Establish authenticated SSH readiness through the exact prebound host key.
6. Pass the connected vsock descriptor to native OpenSSH and exit Z from the byte path.
7. Create a file, reboot the guest, reconnect, and prove the file and machine identity persist.
8. Stop cleanly, exercise abrupt VMM loss and reconciliation, then prove no Z, VMM, helper, listener, mount, TAP, or runtime-socket residue remains.
9. Run the machine-scoped competing-writer, ENOSPC, OOM, signal, partial-copy, failed-fsync, failed-rename, and obstructed-cleanup tests required by certification.

Checkpoint result:

```text
$ z
root@z:~#
```

A file created before reboot remains afterward.

## Phase 2 — complete local baseline

Add:

- named machines;
- native and compatibility SSH config export/install/remove;
- SFTP copy with durable replacement mode;
- exact systemd execution;
- explicit shell mode;
- status, inspect, doctor, and explicit repair;
- Network None;
- locked `passt` connected profile with `--tcp-ports none`, `--udp-ports none`, convenience host mappings disabled, strict sandbox setup required, and direct host-address reachability inventoried as residual authority;
- cold snapshot, restore, fork, export, and import;
- serial console and logs.

## Phase 3 — SSH power surface

Add one at a time with certification:

- local TCP portals;
- local Unix portals;
- exact reverse portals;
- dynamic SOCKS;
- durable portal transient units;
- VS Code Remote SSH;
- JetBrains compatibility profile;
- Git, rsync, scp, sftp, and selected systemd remote tools;
- optional SSHFS/rclone composition.

## Phase 4 — advanced machine capability

- virtiofs;
- bridge/TAP;
- dedicated host identity;
- additional disks and encryption profiles;
- resource changes;
- VFIO and devices;
- SSH TUN/TAP;
- live snapshots and migration;
- QEMU compatibility only after a concrete need.

## Operational completeness requirements

Before the first large Z mutation on an implementation host:

- capture the sanitized implementation-host profile;
- prove sufficient operation-specific storage and bounded failure headroom;
- resolve pending reboot or package state that would invalidate evidence;
- distinguish nested development evidence from release-certification evidence;
- allocate separate Z source, build, asset, machine, runtime, cache, staging, and evidence roots;
- preserve unrelated project state and never clean by age, prefix, or size alone.

The first usable computer MUST include the smallest machine-scoped mutation coordination and durable staging protocol needed to prevent two writers or an interrupted writer from corrupting identity or disk truth. It MUST test ENOSPC, OOM, signals, abrupt VMM/helper loss, partial copy, failed synchronization, and cleanup obstruction.

The complete local baseline adds:

- foreground offline tuple plan, verify, apply, status, and rollback;
- independently verifiable backup and restoration on a separately prepared host;
- a local non-uploading support bundle with redaction tests;
- exact storage-capacity reporting and refusal before unsafe mutation.

Device passthrough, encrypted storage, virtiofs, confidential computing, and live migration remain separately promoted variants and cannot delay the first real computer.

## Engineering rules

- Full files and deterministic builds.
- Pinned dependency and asset digests.
- No speculative provider interfaces.
- No hidden mutation in inspection.
- Negative tests accompany every authority expansion.
- Stable checkpoints prove complete user-visible behavior.
