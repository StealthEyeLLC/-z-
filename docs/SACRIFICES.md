# Sacrifices — SSH-Native Z

Status: **Normative record of intentional limits**

## 1. Purpose

This document records capability, convenience, compatibility, and security limits accepted to keep Z direct, sovereign, inspectable, and agentless.

## 2. Exact argv and PTY are separate baseline modes

Z does not promise arbitrary exact `argv[]` execution directly attached to a live PTY in one operation.

- Native SSH supplies shell, PTY, resize, signals, forwarding, and interactive programs.
- Remote systemd transient services supply exact noninteractive argv, environment, cwd, and outcome.
- Shell interpretation is explicit.

A guest launcher would erase this boundary, but would violate the no-agent and no-custom-protocol architecture. The computer itself loses no power; only one combined convenience operation is absent.

## 3. Linux/KVM host first

The certified baseline targets Linux hosts with KVM. macOS, Windows, and non-KVM hosts are not baseline-equivalent until concrete second implementations exist.

## 4. Guest root controls guest SSH

Unrestricted guest root can read or replace the guest SSH host key, modify `sshd`, change authorized keys, or disable access. This is a property of unrestricted root, not a Z defect.

Z protects the host and detects identity changes from outside the guest. It does not claim to protect a guest from its own root user.

## 5. Host hypervisor is trusted in the baseline

SMBIOS credentials and VMM memory are not confidential from the host hypervisor or owner account. Z does not claim confidential-computing protection from a malicious host or VMM.

## 6. Compatibility SSH relay remains in the data path

Clients that cannot use `ProxyUseFdpass` require a transparent stdio relay. In that profile Z remains in the byte path for the connection, with additional failure and buffering surface.

Native OpenSSH remains the preferred zero-residency profile.

## 7. Native SSH command strings are shell semantics

`ssh z-machine command...` is ordinary SSH remote-command behavior. It is not exact argv. Z documents this rather than pretending otherwise.

## 8. Network None still exposes selected SSH capabilities

A machine with no virtual NIC can still receive SSH, SFTP, and explicitly selected SSH forwarding through AF_VSOCK. Network None means no guest IP network device, not no communication whatsoever.

## 9. User-mode networking is not hostile-code containment

`passt` provides convenient networking under host-user authority. It is not represented as a complete boundary against malicious guest networking.

## 10. Cold snapshots trade availability for portability

The portable snapshot baseline requires a fully stopped machine. Live memory snapshots are version- and configuration-bound advanced artifacts.

## 11. SSHFS is convenience, not durable machine truth

SSHFS may fail open operations when connections break and must not become authoritative storage or a prerequisite for recovery.

## 12. Firmware behavior is only what is certified

Persistent UEFI-variable behavior is not claimed until proven for the exact firmware and Cloud Hypervisor tuple. A standard fallback boot path may be used and any missing NVRAM behavior remains an explicit limitation.
