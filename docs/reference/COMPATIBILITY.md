# Compatibility and Support Policy

Status: **Normative support interpretation**

## 1. No compatibility by implication

A configuration option, successful build, or one manual connection does not make a stack supported. Support attaches only to an exact certified tuple recorded with evidence.

## 2. Dependency authority

The selected initial candidate is defined by [`DEPENDENCIES.md`](DEPENDENCIES.md) and [`../../assets/dependencies.lock.json`](../../assets/dependencies.lock.json). The human document defines roles and policy; the JSON lock defines exact machine identities. A conflict fails closed and must be corrected before implementation proceeds.

Selection is not certification. A lock change creates a new candidate tuple and cannot inherit support automatically.

## 3. Required tuple fields

Every certified tuple records at least:

- Z source commit and release artifact digest.
- Cloud Hypervisor version and binary digest, including vsock packet-type support and SMBIOS Type 11 count/size behavior.
- Firmware identity and digest.
- Base-image identity and digest.
- Guest kernel version.
- Guest systemd version.
- Guest OpenSSH server package/version and applicable security-fix state.
- Host OpenSSH client package/version and applicable security-fix state.
- Network and sharing helper versions plus exact security-relevant invocation options when used.
- Host architecture, exact host-kernel build, applicable KVM security-fix state, and the effective VMM CPU setting proving whether nested virtualization is exposed.
- Host filesystem and required reflink/sparse-copy behavior.
- Effective seccomp mode and Landlock ABI, relied-upon rights, ruleset-layer behavior, and pre-sandbox descriptor inventory.

## 4. SSH client classes

- **Native supported client:** Invokes an OpenSSH client with the certified fd-passing configuration.
- **Compatibility supported client:** Uses the generated inventory and certified transparent stdio relay.
- **Unverified client:** May connect, but has not passed the integration suite.

No client is described as supported merely because it implements an SSH protocol library.

## 5. Initial state

No tuple is certified. The exact initial candidate `z-debian-13.6-amd64-ch53-v1` is selected and locked, but remains an implementation target until complete evidence exists.

## 5.1 Verified implementation-host observation

The retained OVH implementation host is separately locked as `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`. It runs the exact patched Noble kernel and passed the real reboot and host-primitive checkpoint recorded under `evidence/checkpoints/host-kernel-transition-20260801/`.

This is an implementation-host compatibility fact, not a certified release tuple. It proves neither the preserved Debian reference-host candidate nor Cloud Hypervisor, firmware, guest, SSH, persistence, lifecycle, networking, or ecosystem compatibility. Any drift in the implementation host creates a new host tuple before further evidence can rely on it.

## 6. Compatibility changes

A component upgrade creates a new candidate tuple. It must not inherit certification automatically from an earlier tuple, especially for snapshots, credentials, SSH configuration, confinement, or serial recovery.

## 7. Current candidate observations

As of 2026-07-31, no tuple is certified. The locked initial candidate uses Debian 13.6 for the reference host and guest, Cloud Hypervisor v53.0, Cloud Hypervisor EDK2 `CLOUDHV.fd`, Debian systemd 257.13, Debian OpenSSH 10.0p1 security packages, and Rust 1.97.1.

- OpenSSH 10.4/10.4p1 is the current upstream release observed by this audit. Its Linux sandbox, packaging, forwarding, rekey, SFTP, and SCP fixes make the exact patched host/client and guest/server packages part of the tuple.
- Cloud Hypervisor v53.0 is the current upstream release observed by this audit. It is a new candidate, not an inherited certification from v52.0.
- Cloud Hypervisor v52.0 and v53.0 use a stream-only Unix vsock mux; they cannot carry systemd's datagram/sequenced-packet `vmm.notify_socket` readiness channel.
- The connected `passt` profile is supportable only with exact host-mapping, publication, and sandbox options recorded and negatively tested. Those controls do not establish host-address isolation; direct reachability to real host addresses is tuple evidence, while Network None supplies the no-general-network profile.
- Cloud Hypervisor's current x86 nested-virtualization option defaults to `on`; the baseline candidate must explicitly configure and verify `nested=off`.

These observations narrow candidate selection. They do not certify any combination.
