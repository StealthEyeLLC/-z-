# Scope — SSH-Native Z

Status: **Normative product boundary**

## 1. Product definition

Z is a local runtime for persistent, unrestricted Linux computers that are first-class SSH hosts.

The baseline product owns only:

- Machine materialization and identity.
- Verified immutable asset selection.
- VMM lifecycle and recovery.
- Standard credential injection.
- Establishment of authenticated SSH transport over AF_VSOCK.
- Explicit file transfer, forwarding, networking, sharing, and device integrations.

Linux owns packages, processes, users, services, jobs, filesystems, containers, and application behavior.

## 2. Required baseline

The first certified release includes:

- Linux/KVM host.
- One Z executable.
- Pinned Cloud Hypervisor, firmware, base image, OpenSSH, systemd, and helper tuple.
- Persistent raw disk with reflink and sparse-copy fallback.
- Stable machine UUID and SSH host identity.
- SMBIOS-to-systemd credential bootstrap through the private VMM API.
- Static AF_VSOCK socket-activated OpenSSH.
- Bare root shell.
- Native OpenSSH profile with descriptor handoff.
- Compatibility inventory profile with transparent stdio relay.
- Hermetic internal SSH profile.
- SFTP copy.
- Exact noninteractive systemd execution.
- Serial recovery.
- Network None and `passt` profiles.
- Safe cold snapshot, restore, and fork.
- Read-only status/inspect/doctor and explicit repair.
- Zero Z processes at rest.

## 3. Supported post-baseline capabilities

After the baseline is certified, concrete variants may add:

- SSH capability portals.
- Durable portal units.
- SSHFS and rclone compositions.
- Bridge/TAP networking.
- Virtiofs shares.
- Additional disks.
- Dedicated host identities.
- Resource resizing.
- VFIO and device passthrough.
- Encryption profiles.
- Live snapshots and migration.
- Optional MCP edge invoking the same local binary.

## 4. Out of scope for the baseline

- Hosted control plane.
- Fleet manager.
- Multi-tenant authority.
- Web dashboard requirement.
- Permanent controller or relay.
- Guest agent.
- Product protocol.
- General workflow engine.
- Universal distribution support.
- Universal VMM framework.
- Compatibility claims not tested end to end.
- Protection from a malicious host hypervisor.

## 5. Product test

A feature belongs in Z only when it helps the owner obtain, connect to, preserve, recover, or explicitly extend the real computer. Ordinary Linux behavior remains inside Linux.
