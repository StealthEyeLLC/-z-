# Build Plan — SSH-Native Z

Status: **Normative implementation order**

## Dependency gate

The current implementation-host profile is recorded in [`reference/IMPLEMENTATION-HOST.md`](reference/IMPLEMENTATION-HOST.md). It is an input to preflight, not certification evidence and not an override of the selected reference-host tuple.

Before source implementation or asset construction:

1. Verify [`reference/DEPENDENCIES.md`](reference/DEPENDENCIES.md) and [`../assets/dependencies.lock.json`](../assets/dependencies.lock.json) agree.
2. Verify signed Debian snapshot metadata, package-index hashes, Cloud Hypervisor, firmware, and Rust channel-manifest digests.
3. Use candidate tuple `z-debian-13.6-amd64-ch53-v1` without live-mirror, backport, or floating-version substitution.
4. Treat any version or digest change as a new candidate tuple.
5. Record complete transitive package and Cargo closures when they first exist.

Selection is not certification.

## Phase 0 — Semantics gates

1. Prove native OpenSSH descriptor handoff against Cloud Hypervisor vsock mux.
2. Prove compatibility stdio relay against one embedded SSH client.
3. Prove strict prebound host-key lookup.
4. Prove static AF_VSOCK `sshd -i` service.
5. Prove SMBIOS system credentials through the private VMM API, including OEM-string count/size preflight and exact binary round-trip; do not depend on `vmm.notify_socket` for Cloud Hypervisor v52.0/v53.0.
6. Prove the exact host kernel is patched for applicable KVM isolation advisories, including CVE-2026-53359 on x86; explicitly configure the pinned Cloud Hypervisor x86 equivalent of `nested=off` and prove the effective guest CPU exposure.
7. Prove exact noninteractive systemd argv and result semantics.
8. Prove serial reconnect across reboot.

No architecture scaffold counts as completion without a real booted computer.

## Phase 1 — First usable computer

Implement only:

- Exact asset verification.
- Machine directory and raw disk.
- Identity generation.
- Transient host systemd VMM service.
- Fail-closed confinement.
- SMBIOS credentials.
- Static guest SSH.
- Bare root shell.
- Persistent change.
- Guest reboot and reconnect.
- Graceful stop and abrupt recovery.
- Zero processes at rest.

Checkpoint result:

```text
$ z
root@z:~#
```

A file created before reboot remains afterward.

## Phase 2 — Complete local baseline

Add:

- Named machines.
- Native and compatibility SSH config export/install/remove.
- SFTP copy with durable replacement mode.
- Exact systemd execution.
- Explicit shell mode.
- Status, inspect, doctor, and explicit repair.
- Network None.
- `passt` connected profile with `--tcp-ports none`, `--udp-ports none`, convenience host mappings disabled, strict sandbox setup required, and direct host-address reachability inventoried as residual authority.
- Cold snapshot, restore, fork, export, and import.
- Serial console and logs.

## Phase 3 — SSH power surface

Add one at a time with certification:

- Local TCP portals.
- Local Unix portals.
- Exact reverse portals.
- Dynamic SOCKS.
- Durable portal transient units.
- VS Code Remote SSH.
- JetBrains compatibility profile.
- Git, rsync, scp, sftp, and selected systemd remote tools.
- Optional SSHFS/rclone composition.

## Phase 4 — Advanced machine capability

- Virtiofs.
- Bridge/TAP.
- Dedicated host identity.
- Additional disks and encryption profiles.
- Resource changes.
- VFIO and devices.
- SSH TUN/TAP.
- Live snapshots and migration.
- QEMU compatibility only after a concrete need.

## Operational completeness requirements

Before the first large Z mutation on an implementation host:

- capture the sanitized implementation-host profile;
- prove sufficient operation-specific storage and bounded failure headroom;
- resolve pending reboot or package state that would invalidate evidence;
- distinguish nested development evidence from release-certification evidence;
- allocate separate Z source, build, machine, runtime, cache, and evidence roots;
- preserve unrelated project state and never clean by age, prefix, or size alone.

The first usable computer implementation must include the smallest machine-scoped mutation coordination and durable staging protocol needed to prevent two writers or an interrupted writer from corrupting identity or disk truth. It must test ENOSPC, OOM, signals, abrupt VMM/helper loss, partial copy, failed synchronization, and cleanup obstruction.

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
