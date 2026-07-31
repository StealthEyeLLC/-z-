# Build Plan — SSH-Native Z

Status: **Normative implementation order**

## Dependency gate

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

## Engineering rules

- Full files and deterministic builds.
- Pinned dependency and asset digests.
- No speculative provider interfaces.
- No hidden mutation in inspection.
- Negative tests accompany every authority expansion.
- Stable checkpoints prove complete user-visible behavior.
