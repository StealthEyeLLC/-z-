# Compatibility and Support Policy

Status: **Normative support interpretation**

## 1. No compatibility by implication

A configuration option, successful build, or one manual connection does not make a stack supported. Support attaches only to an exact certified tuple recorded with evidence.

## 2. Required tuple fields

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

## 3. SSH client classes

- **Native supported client:** Invokes an OpenSSH client with the certified fd-passing configuration.
- **Compatibility supported client:** Uses the generated inventory and certified transparent stdio relay.
- **Unverified client:** May connect, but has not passed the integration suite.

No client is described as supported merely because it implements an SSH protocol library.

## 4. Initial state

No tuple is certified at repository initialization. Candidate component selections in architecture or research documents remain implementation targets until evidence exists.

## 5. Compatibility changes

A component upgrade creates a new candidate tuple. It must not inherit certification automatically from an earlier tuple, especially for snapshots, credentials, SSH configuration, confinement, or serial recovery.

## 6. Current candidate observations

As of 2026-07-31, no tuple is certified.

- OpenSSH 10.4/10.4p1 is the current upstream release observed by this audit. Its Linux sandbox, packaging, forwarding, rekey, SFTP, and SCP fixes make the exact patched host/client and guest/server packages part of the tuple.
- Cloud Hypervisor v53.0 is the current upstream release observed by this audit. It is a new candidate, not an inherited certification from v52.0.
- Cloud Hypervisor v52.0 and v53.0 use a stream-only Unix vsock mux; they cannot carry systemd's datagram/sequenced-packet `vmm.notify_socket` readiness channel.
- The connected `passt` profile is supportable only with exact host-mapping, publication, and sandbox options recorded and negatively tested. Those controls do not establish host-address isolation; direct reachability to real host addresses is tuple evidence, while Network None supplies the no-general-network profile.
- Cloud Hypervisor's current x86 nested-virtualization option defaults to `on`; the baseline candidate must explicitly configure and verify `nested=off`.

These observations narrow candidate selection. They do not certify any combination.
