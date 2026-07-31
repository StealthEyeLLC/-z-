# Decisions — SSH-Native Z

Status: **Normative architectural decision record**

## D001 — Product category

Z is an SSH-native sovereign Linux computer runtime, not a local cloud or command-runner.

## D002 — Primary transport

OpenSSH over Cloud Hypervisor AF_VSOCK is the baseline control and ecosystem surface. Guest IP networking is optional.

## D003 — Descriptor handoff

Native OpenSSH uses `ProxyUseFdpass=yes`; Z exits after passing the connected descriptor.

## D004 — Compatibility profile

Clients without descriptor passing receive explicit inventory entries and a connection-scoped transparent stdio relay. Compatibility is separate and honestly weaker.

## D005 — Static guest SSH

The certified image contains static AF_VSOCK systemd socket units and stock `sshd -i`. Automatic `systemd-ssh-generator` behavior is not the sole control path.

## D006 — Credential bootstrap

Cloud Hypervisor SMBIOS OEM strings supplied through the private VMM API carry systemd credentials. No credential disk is baseline.

## D007 — Identity

Machine UUID plus SSH host key define computer identity. Alias is a label. Restart/rename/restore preserve; fork/import-as-new rotate.

## D008 — Execution split

Interactive PTY behavior is native SSH. Exact argv is noninteractive remote systemd. Explicit shell mode remains separate.

## D009 — Host supervision

Host systemd directly owns the VMM and helpers in transient units. No custom machine supervisor is baseline.

## D010 — Network None

Network None means no virtual NIC. SSH over AF_VSOCK and explicit portals remain available.

## D011 — Capability portals

Standard SSH forwarding is the service-exposure primitive. There is no portal registry or custom tunnel protocol.

## D012 — Storage

The baseline uses independent raw disks with reflink cloning and sparse fallback. Cold snapshots precede live snapshots.

## D013 — Trust

Host keys are prebound; TOFU and silent replacement are rejected.

## D014 — Internal SSH

Z's own control operations use a hermetic SSH configuration and do not inherit ambient owner SSH behavior.

## D015 — Certification tuple

Support attaches to an exact tuple of Z, Cloud Hypervisor, firmware, image, guest kernel, systemd, OpenSSH, helpers, host kernel floor, and host filesystem behavior.

## D016 — Remote and AI access

Any MCP or remote edge invokes the same local Z binary and SSH paths. No second executor or machine database is permitted.

## D017 — Cloud Hypervisor readiness notification boundary

For Cloud Hypervisor v52.0 and v53.0, `vmm.notify_socket` is not a baseline credential because systemd sends readiness over AF_VSOCK datagram or sequenced-packet sockets while the VMM's Unix mux accepts stream traffic only. Authenticated SSH remains the final readiness authority. A later tuple may enable notification only after exact transport certification.

## D018 — No implicit host mapping in the connected profile

The certified `passt` profile disables host-loopback, gateway, and guest-address convenience mappings, explicitly disables inbound TCP/UDP publication, and does not allow sandbox fallback. These controls do not claim to block outbound access to services bound on the host's real external addresses. The connected profile records that residual authority; Network None is required for host-network isolation.

## D019 — Patched host kernel and no baseline nested virtualization

The host kernel and KVM security-fix state are part of every compatibility tuple. The x86 baseline must prove it is not vulnerable to CVE-2026-53359. Because Cloud Hypervisor's x86 `nested` option defaults to `on` in current releases, the baseline explicitly sets `nested=off` (or the exact pinned-version equivalent) and proves the effective configuration. Nested virtualization requires separate authorization and certification.
