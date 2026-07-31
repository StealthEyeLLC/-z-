# Changes from the Original Z Source Documents

## Preserved without weakening

- Real KVM virtual machine.
- Persistent unrestricted root Linux.
- One direct executable.
- Cloud Hypervisor capability ceiling.
- Raw inspectable disks.
- OpenSSH over AF_VSOCK.
- Standard systemd facilities.
- No guest agent or custom guest protocol.
- No permanent controller, database, scheduler, or relay.
- Zero Z processes at rest.
- Pinned assets, strict confinement, truthful state, exact cleanup, and explicit variants.

## Strengthened

- SSH identity is now a first-class machine identity.
- Native OpenSSH ecosystem compatibility is normative.
- Strict prebound host verification replaces any TOFU interpretation.
- Native connections use fd passing and remove Z from the data path.
- Internal Z SSH is hermetic rather than inheriting user configuration.
- Network None means physically no virtual NIC.
- Restore and fork identity semantics are separated.
- Host systemd directly owns VMM lifecycle.
- Landlock/equivalent confinement fails closed in the certified baseline.

## Corrected

- Lossless execution is defined across complementary native modes rather than falsely requiring exact argv plus PTY in one stock operation.
- Native SSH remote commands are documented as shell command strings.
- Cold restore preserves identity; fork rotates it.
- User-mode networking is not described as hostile-code containment.
- Variant statuses are concrete rather than unresolved.

## New strict upgrades

- SMBIOS-to-systemd credential bootstrap through the private Cloud Hypervisor API.
- Native and compatibility SSH profiles.
- Read-only dynamic host-key lookup and explicit inventory export.
- SSH capability portals over vsock.
- Guest-to-host boot notification over AF_VSOCK as supplemental evidence.
- SFTP durable replacement semantics.
- Exact compatibility tuples including OpenSSH and systemd versions.
- Future delegated restricted portal keys using standard SSH authorization options.
