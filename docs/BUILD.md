# Build Plan — SSH-Native Z

Status: **Normative implementation order**

## Phase 0 — Semantics gates

1. Prove native OpenSSH descriptor handoff against Cloud Hypervisor vsock mux.
2. Prove compatibility stdio relay against one embedded SSH client.
3. Prove strict prebound host-key lookup.
4. Prove static AF_VSOCK `sshd -i` service.
5. Prove SMBIOS system credentials through the private VMM API.
6. Prove exact noninteractive systemd argv and result semantics.
7. Prove serial reconnect across reboot.

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
- `passt` connected profile.
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
