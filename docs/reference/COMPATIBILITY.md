# Compatibility and Support Policy

Status: **Normative support interpretation**

## 1. No compatibility by implication

A configuration option, successful build, or one manual connection does not make a stack supported. Support attaches only to an exact certified tuple recorded with evidence.

## 2. Required tuple fields

Every certified tuple records at least:

- Z source commit and release artifact digest.
- Cloud Hypervisor version and binary digest.
- Firmware identity and digest.
- Base-image identity and digest.
- Guest kernel version.
- Guest systemd version.
- Guest OpenSSH server package/version.
- Host OpenSSH client package/version.
- Network and sharing helper versions when used.
- Host architecture and minimum host-kernel version.
- Host filesystem and required reflink/sparse-copy behavior.
- Effective seccomp and Landlock ABI/behavior.

## 3. SSH client classes

- **Native supported client:** Invokes an OpenSSH client with the certified fd-passing configuration.
- **Compatibility supported client:** Uses the generated inventory and certified transparent stdio relay.
- **Unverified client:** May connect, but has not passed the integration suite.

No client is described as supported merely because it implements an SSH protocol library.

## 4. Initial state

No tuple is certified at repository initialization. Candidate component selections in architecture or research documents remain implementation targets until evidence exists.

## 5. Compatibility changes

A component upgrade creates a new candidate tuple. It must not inherit certification automatically from an earlier tuple, especially for snapshots, credentials, SSH configuration, confinement, or serial recovery.
