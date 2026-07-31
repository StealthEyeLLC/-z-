# Glossary

Status: **Canonical terminology reference**

- **-Z- / Z / `z`:** **-Z-** is the product mark, **Z** is the spoken name, and `z` is the command-line interface. The canonical repository is `StealthEyeLLC/-z-`.
- **Z machine:** A persistent unrestricted Linux virtual computer with its own durable disk and SSH identity.
- **Machine identity:** The machine UUID plus SSH host key. A human-readable name is a label, not identity.
- **Native SSH profile:** OpenSSH configuration using descriptor handoff (`ProxyUseFdpass`) so Z exits after connecting the vsock endpoint.
- **Compatibility SSH profile:** Explicit per-machine SSH inventory using a transparent connection-scoped stdio relay for clients that cannot accept descriptor passing.
- **Hermetic internal SSH:** Z-controlled OpenSSH invocation that ignores ambient owner configuration and uses exact identity, host-key, and timeout settings.
- **AF_VSOCK:** Host/guest socket transport independent of guest IP networking.
- **Vsock mux:** Cloud Hypervisor endpoint through which a host client selects a guest vsock port.
- **Network None:** No virtual network interface is attached. AF_VSOCK SSH and explicit SSH portals remain possible.
- **Capability portal:** An explicitly requested standard SSH forwarding channel exposing one selected service or socket.
- **Interactive plane:** Native SSH shell or PTY behavior, including resize and signals.
- **Exact execution plane:** Noninteractive exact `argv[]`, environment, cwd, streams, and result through guest-native systemd mechanisms.
- **Data plane:** SFTP-based file transfer and durable replacement behavior.
- **Restore:** Reinstating the same computer; identity is preserved.
- **Fork:** Creating a new computer from another computer's durable state; collision-prone identities are rotated.
- **Ready:** A strict authenticated SSH handshake succeeded against the prebound machine host key.
- **Unknown:** The system cannot prove success or failure. Unknown must never be reported as success.
- **Certified tuple:** The exact tested combination of Z, VMM, firmware, image, kernel, systemd, OpenSSH, helpers, host kernel floor, and filesystem behavior.

## Candidate tuple

An exact selected combination of source, toolchain, host, VMM, firmware, image, packages, helpers, configuration-sensitive facts, and digests that is eligible for implementation and certification but is not yet supported.

## Dependency authority

`docs/reference/DEPENDENCIES.md`, which defines dependency roles, selection rules, exclusions, and upgrade policy for the selected candidate tuple.

## Dependency lock

`assets/dependencies.lock.json`, the exact machine-readable identity of the selected candidate tuple, including immutable archive metadata, complete resolved package closures, upstream asset identities and digests, and configuration bindings. A lock is selection evidence, not certification evidence.
