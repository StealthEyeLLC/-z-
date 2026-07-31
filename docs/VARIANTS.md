# Variants — SSH-Native Z

Status: **Normative variant catalog**  
Applies to: **Supported deviations from the minimal SSH-native baseline**

## 1. Purpose

The baseline delivers the smallest honest system that opens a persistent unrestricted root Linux computer and exposes it as a strongly identified native OpenSSH destination.

Variants keep additional capability, privilege, compatibility, and runtime cost outside the ordinary path until the owner explicitly selects them.

A variant is not a plugin, provider registry, second control plane, alternate executor, or replacement product architecture. It is a documented configuration of the same machine lifecycle, identity, OpenSSH, systemd, and durable-state model.

## 2. Variant rules

Every variant MUST declare:

- Purpose.
- Status: baseline, supported, experimental, or future.
- Added host processes.
- Added guest components.
- Added privileges or host authority.
- Added durable state.
- Added capabilities.
- Lost or changed capabilities.
- Security consequences.
- Compatibility requirements.
- Composition rules.
- Certification requirements.
- Exact cleanup.

Every variant MUST fail closed when prerequisites are absent.

A disabled variant MUST leave no helper, mount, listener, firewall rule, bridge membership, device binding, secret, control socket, SSH master, tunnel, or durable control-plane state.

Variants MUST NOT introduce a second controller, database, operation registry, guest protocol, SSH implementation, executor, or machine authority.

## 3. Required baseline: SSH-Native Sovereign Computer

Status: **Required baseline**

### Purpose

Provide the ordinary owner experience with maximum computer power, native SSH compatibility, strict identity, and minimal project machinery.

### Configuration

- Linux host with KVM.
- One user-facing Z binary.
- Host systemd used directly for transient machine supervision.
- Pinned and verified Cloud Hypervisor.
- Pinned firmware.
- One pinned ordinary Linux image.
- Persistent raw guest disk.
- Reflink clone with sparse-copy fallback.
- Machine-specific SSH host identity before first connection.
- Standard read-only identity bootstrap artifact.
- Static systemd AF_VSOCK socket activation.
- Stock OpenSSH `sshd -i` per connection.
- Native OpenSSH client access through `ProxyCommand` and descriptor handoff.
- Strict machine-bound host verification.
- One dedicated owner authentication key.
- SFTP.
- Exact noninteractive execution through guest systemd.
- Reconnecting serial recovery.
- VMM seccomp.
- Required VMM filesystem confinement.
- No host shares.
- No device passthrough.
- No remote internet listener.
- `passt` connected profile as the ordinary network default.
- Network None available from the first release.
- No Z guest binary.
- No Z database.
- No permanent Z service.

### Runtime footprint

When stopped:

- Zero Z processes.
- No machine helper.
- No SSH master.
- No portal.
- No network helper.

When running with default connected networking:

- One Cloud Hypervisor process owned by a host systemd transient service.
- One `passt` process owned by an exact sibling or dependent transient service.
- Standard guest processes.
- Per-connection stock OpenSSH server processes only while SSH sessions exist.
- No long-lived Z SSH relay after descriptor handoff.

### Required capabilities

- Bare `z` opens root.
- `z <name>` selects or creates a named machine and opens root.
- `ssh z-<name>` starts an existing stopped machine and connects through native OpenSSH.
- Persistent filesystem.
- Reboot persistence.
- Strict SSH identity.
- Interactive PTY and resize.
- Signals.
- SFTP copy.
- Native SSH forwarding.
- Exact non-shell command execution through the separate systemd plane.
- Explicit shell command mode.
- Clean stop and restart.
- Serial recovery.
- Abrupt client and VMM recovery.
- Control independent of guest IP networking.

### Baseline limits

- Direct third-party SSH does not silently create a nonexistent machine.
- Native SSH remote command execution uses command-string and shell semantics.
- Exact `argv[]` execution is noninteractive and does not attach a live PTY.
- No automatic agent, X11, desktop socket, or host-home forwarding.
- No ControlMaster by default.

### Certification

Must pass all baseline gates in the SSH architecture report and `docs/CERTIFICATION.md`.

## 4. SSH access variants

## 4.1 SSH access: native ecosystem profile

Status: **Required baseline**

### Purpose

Expose every existing Z machine to native OpenSSH consumers.

### Behavior

Z generates a reserved `Host z-*` profile using:

- An absolute Z binary path.
- Descriptor-pass proxy mode.
- Read-only machine-bound host-key lookup.
- Strict host verification.
- Exact owner identity selection.
- No ambient agent.
- No default forwards.
- No X11.
- No ControlMaster.

### Added state

- One explicit owner-approved SSH include file.
- One dedicated Z owner keypair.
- Public host-key evidence per machine.

### Cleanup

`z ssh-config remove` removes only its marked include content and leaves unrelated user configuration untouched.

## 4.2 SSH access: per-machine owner key

Status: **Supported hardened variant**

### Purpose

Limit owner-authentication key reuse across machines.

### Added state

- One owner private key per machine.
- One public key in each machine identity artifact.
- Individual generated SSH host stanzas or a certified dynamic identity-selection mechanism.

### Capability changes

- Stronger per-machine revocation and backup separation.
- More machine-specific configuration and key management.

### Certification

Must prove no wrong-machine key use, correct import/export handling, and exact deletion behavior.

## 4.3 SSH access: hardware-backed owner key

Status: **Supported optional variant**

### Purpose

Authenticate with a FIDO/security-key-backed OpenSSH key.

### Added authority

- Access to the selected security-key provider or device.

### Capability changes

- May require physical presence or touch.
- May not suit unattended automation.

### Certification

Must cover interactive authentication, failed device access, IDE behavior, recovery key handling, and explicit fallback policy.

## 4.4 SSH access: multiplexed native fabric

Status: **Supported optional performance variant**

### Purpose

Reuse one stock OpenSSH connection for repeated shells, SFTP operations, IDE channels, and portals.

### Added processes

- One OpenSSH ControlMaster while active.

### Added runtime state

- One control socket in the private machine runtime directory.

### Requirements

- Bounded `ControlPersist`.
- Unique path including machine identity, user, and port.
- No master reuse after stop, fork, import, or key rotation.
- Master does not prove machine state.

### Cleanup

Close via native SSH control command, verify process exit, then remove only the exact owned socket.

## 4.5 SSH access: compatibility inventory profile

Status: **Supported compatibility variant**

### Purpose

Support IDEs and embedded SSH libraries that understand ordinary `ProxyCommand` but do not implement OpenSSH descriptor passing or dynamic host-key commands consistently.

### Behavior

- Z generates explicit per-machine SSH host entries in an owner-approved include file.
- Each entry uses a transparent stdio `ProxyCommand` such as `z ssh-stream <machine>`.
- Each entry points at an exact generated `known_hosts` file or exact host-key directive supported by the selected client.
- Discovery is inventory-based rather than a wildcard profile so IDE host explorers can enumerate machines.

### Added processes

- One connection-scoped Z relay per SSH transport.

### Changed properties

- Z remains in the byte path for that connection.
- Cancellation, buffering, and EOF behavior require separate certification.
- Descriptor-handoff zero-residency is lost for the connection.

### Rules

- Must never replace the native profile for OpenSSH clients that support descriptor passing.
- Must preserve byte transparency.
- Must not parse or terminate SSH.
- Must create no durable connection record.
- Must stop when the underlying transport stops.
- Configuration generation, installation, diff, and removal must be explicit and atomic.

## 4.6 SSH access: explicit autocreate alias

Status: **Future optional variant**

### Purpose

Permit creating a computer through an unmistakably explicit SSH destination.

### Requirements

- Must not use ordinary `z-<name>` aliases.
- Must not trigger from config discovery or host-key lookup.
- Must make disk and machine creation obvious before allocation.
- Must precreate identity before host-key verification.

### Status rationale

Deferred until the baseline proves that native SSH autostart is flawless. Silent autocreate remains prohibited.

## 5. Execution variants

## 5.1 Execution: interactive root shell

Status: **Required baseline**

Uses native OpenSSH shell and PTY behavior.

## 5.2 Execution: native SSH command string

Status: **Supported native behavior**

### Purpose

Allow ordinary commands such as:

```text
ssh z-work 'make clean && make'
```

### Semantics

- One SSH command string.
- Guest shell interpretation.
- Not exact argv.
- Exit status follows SSH behavior.

Z documentation must label it accurately.

## 5.3 Execution: exact systemd command

Status: **Required baseline**

### Purpose

Execute an exact executable and argument vector without an implicit shell.

### Architecture

- Uses the same strict SSH identity and transport.
- Uses remote systemd transient services.
- Working directory and environment are explicit.
- Standard streams are represented by exact guest files transferred through SFTP.
- Result is read from systemd unit properties.
- No host job record.

### Limits

- No directly attached PTY.
- Connection or retrieval uncertainty returns unknown.

## 5.4 Execution: explicit shell

Status: **Required baseline**

Runs a declared shell expression with visibly shell-oriented syntax.

## 5.5 Execution: native durable unit

Status: **Supported convenience variant**

### Purpose

Start long-running work as a native guest systemd unit and return its stable guest unit name.

### Architecture

- No host job database.
- Logs remain in journald.
- Status and cancellation use systemd.
- Reboot behavior is declared in the guest unit.

### Limitation

No exactly-once or universal transaction claim.

## 6. File and filesystem variants

## 6.1 Transfer: SFTP

Status: **Required baseline**

### Capabilities

- Copy in and out.
- Recursive copy.
- Resume with documented caveats.
- Flush where supported.
- Atomic temporary upload and rename.
- Server-side copy where supported.

### Certification

Must include binary files, sparse-file behavior as declared, interrupted copy, final rename failure, permission handling, and symlink cases.

## 6.2 Filesystem: SSHFS guest mount on host

Status: **Supported optional external composition**

### Purpose

Mount an exact guest path on the host through SFTP and FUSE.

### Added processes

- One `sshfs` process while mounted.

### Added state

- One FUSE mount.

### Limitations

- Interrupted operations may block until timeout.
- Reconnect may lose in-flight operations.
- Not a backup, snapshot, or raw-disk recovery mechanism.
- SSHFS maintenance is limited.

### Requirements

- Run under owner identity.
- Exact mount path.
- Server-alive timeout.
- Optional reconnect only with explicit data-loss warning.
- Exact unmount and process cleanup.

## 6.3 Filesystem: rclone SFTP composition

Status: **External composition**

Rclone may consume the same SFTP identity for sync or mount workflows. It is not a Z baseline dependency and its own configuration remains owner state.

## 7. SSH capability portal variants

## 7.1 Portal: local TCP

Status: **Supported**

### Purpose

Expose an exact guest TCP service on a host loopback address.

### Added processes

- One foreground OpenSSH process, or one exact systemd transient service when requested durable.

### Default authority

- Loopback-only host listener.

### Certification

Must cover collision, failed guest destination, reconnect policy, machine stop, external bind rejection, and cleanup.

## 7.2 Portal: local Unix socket

Status: **Supported**

### Purpose

Expose a guest TCP or Unix service as an owner-private host Unix socket.

### Security properties

- Avoids a host TCP listener.
- Filesystem permissions control host-side access.

### Requirements

- Socket below private runtime root.
- Restrictive umask.
- Exact stale-socket handling.
- No parent or sibling path escape.

## 7.3 Portal: remote exact host service

Status: **Supported advanced**

### Purpose

Give the guest access to one selected host TCP or Unix service, including in Network None mode.

### Added authority

The guest gains the exact authority of the selected host endpoint for the lifetime of the portal.

### Requirements

- Exact host destination.
- Guest-side listener bound to loopback or exact Unix path by default.
- No wildcard host-service bridge.
- No automatic forwarding of host agents or credentials.

## 7.4 Portal: dynamic SOCKS

Status: **Supported optional**

### Purpose

Create a host SOCKS endpoint whose outgoing network perspective is the guest.

### Limits

- Requires guest networking for external destinations.
- Not a complete VPN.
- DNS behavior must be documented.

## 7.5 Portal: durable

Status: **Supported optional**

### Purpose

Keep an explicit SSH portal active independently of a terminal.

### Architecture

- Exact native OpenSSH invocation owned by a host systemd transient service.
- No Z tunnel database.
- Machine dependency expressed through systemd.

### Cleanup

Stop unit, verify SSH process exit, remove exact runtime sockets, and leave no listener.

## 7.6 Portal: SSH TUN point-to-point

Status: **Advanced privileged**

### Purpose

Create an IP path through the SSH connection independent of a virtio-net backend.

### Added authority

- Host TUN device.
- Guest TUN device.
- Host network administration.
- Explicit routes.

### Requirements

- Guest `PermitTunnel=point-to-point` or exact equivalent.
- Exact device ownership.
- No automatic global routes.
- MTU and performance certification.

## 7.7 Portal: SSH TAP Ethernet

Status: **Experimental privileged**

### Purpose

Carry Ethernet frames over SSH.

### Added authority

- TAP devices.
- Potential bridge membership.
- Layer-2 exposure.

### Limits

Performance and behavior differ from virtio-net. It must not be marketed as equivalent until certified.

## 8. Network variants

Only one primary guest network mode may own a given interface unless a tested multi-interface configuration is selected.

## 8.1 Network: `passt`

Status: **Recommended ordinary connected baseline profile**

### Purpose

Provide low-friction outbound networking and explicit inbound publishing.

### Added processes

- One machine-scoped `passt` process.

### Requirements

- No implicit inbound forwarding; the baseline invocation explicitly uses the pinned-version equivalents of `--tcp-ports none` and `--udp-ports none`.
- Host-loopback, gateway, and guest-address convenience mappings are disabled with the exact pinned-version equivalents of `--map-host-loopback none`, `--no-map-gw`, and `--map-guest-addr none`.
- The stricter `pivot_root()` sandbox must succeed; `--chroot-fallback` is prohibited in the certified baseline.
- Explicit published ports only.
- Negative tests prove the convenience aliases above do not reach host services and inventory direct reachability to every real host address.
- These options do not establish host-network isolation. Current upstream documentation exposes no destination filter for services bound to the host's real external addresses; such services may remain reachable as ordinary outbound destinations. Network None is required when the guest must have no general network path to host services.
- Exact process and socket cleanup.

### Limitation

User-mode networking is not hostile-code host isolation.

## 8.2 Network: None

Status: **Supported from first release**

### Behavior

- No virtio-net or other IP network device is attached.
- SSH over AF_VSOCK remains fully available.
- SFTP remains available.
- Capability portals remain available.

### Added processes

- None.

### Certification

Must prove absence of undeclared NICs and IP traffic while SSH, SFTP, and selected portals continue to work.

## 8.3 Network: sealed with selected host services

Status: **Supported security profile**

### Purpose

Combine Network None with one or more explicit reverse SSH portals.

### Example uses

- Package cache proxy.
- Exact license server.
- Exact local development service.
- Exact hardware-agent socket when separately approved.

### Security consequence

Each portal is an explicit capability. The guest still has no general NIC.

## 8.4 Network: isolated user-mode

Status: **Experimental until complete bypass testing**

User-mode restrictions must be proven against host loopback, host interface addresses, DNS, IPv4, IPv6, forwarded ports, and alternative routes.

## 8.5 Network: Bridge/TAP

Status: **Supported advanced**

Provides full layer-2 behavior with explicit privileged setup, ownership labels, isolation rules, and exact cleanup.

## 8.6 Network: physical or virtual NIC passthrough

Status: **Advanced hardware-dependent**

Requires exact PCI identity, IOMMU group validation, bind/unbind, reset, host recovery, and no sibling-device surprise.

## 9. Storage variants

## 9.1 Storage: raw persistent disk

Status: **Required baseline**

One primary raw disk, with optional explicit additional raw disks.

## 9.2 Bootstrap: SMBIOS system credentials

Status: **Required baseline**

### Purpose

Provide unique machine SSH identity and owner authorization without a guest agent, reusable image secret, command-line secret, or extra block device.

### Durable authority

The machine directory owns:

- Machine UUID.
- SSH host private key.
- SSH host public key and fingerprint.
- Selected owner authorization public key or keys.

### Boot behavior

Z submits the complete machine configuration to the private Cloud Hypervisor API socket. Platform OEM strings carry systemd credentials including:

- `z.ssh.hostkey.ed25519`.
- `z.ssh.authorized_keys.root`.

The guest imports the credentials into the stock socket-activated SSH service. The implementation must preflight the selected VMM's OEM-string count and encoded table size and reject any value that could truncate, wrap, or exceed the certified tuple's limits.

`vmm.notify_socket` is not available in the Cloud Hypervisor v52.0/v53.0 candidate baseline because systemd requires AF_VSOCK datagram or sequenced-packet support while the VMM's Unix mux is stream-only. It remains a future exact-tuple option, never readiness authority.

### Security consequences

- The VMM receives the boot credentials and must be tightly confined.
- Guest root can read or replace its own SSH identity and therefore is not protected from itself.
- The API socket and VMM memory are host-side secret boundaries.

### Certification

Must prove exact binary preservation, no process-argument leakage, correct service isolation, strict host-key binding, restart persistence, fork rotation, and fail-closed behavior when a credential is missing or malformed.

## 9.2.1 Bootstrap fallback: read-only credential medium

Status: **Supported fallback only**

A small standard read-only filesystem or equivalent inspectable medium MAY be used only when the exact certified stack cannot import the required SMBIOS credentials.

It must be derived from the authoritative machine directory for the boot, attached read-only, deleted or replaced safely, and never become a second private-key authority.

## 9.3 Storage: ephemeral full clone

Status: **Supported optional**

A temporary reflink or sparse copy is preferred over a fragile custom overlay chain.

## 9.4 Storage: cold snapshot

Status: **Supported portable default snapshot**

### Behavior

- Machine fully stopped after graceful shutdown.
- All disks, identity artifacts, and required metadata copied or reflinked.
- Restore of the same snapshot preserves identity.
- Fork from the snapshot creates new identity.

### Correction from the original catalog

Restore and fork are separate operations.

## 9.5 Storage: application-consistent disk capture

Status: **Advanced**

A running machine may be quiesced through guest-native mechanisms before disk capture. This is not called a cold snapshot and its consistency scope must be explicit.

## 9.6 Storage: live VMM snapshot

Status: **Advanced exact-version-bound**

Must bind to exact Z, VMM, firmware, CPU, device, memory, disk, and helper compatibility tuple. Cross-version portability is not assumed.

## 9.7 Storage: encrypted machine

Status: **Split into explicit implementations**

### 9.7.1 Host-filesystem encryption

External composition; Z records no independent cryptographic claim.

### 9.7.2 Standard host encrypted block container

Supported optional after exact key and recovery design.

### 9.7.3 Guest-native full-disk encryption

Advanced; requires an explicit unlock path that does not embed secrets in the image or command line.

These are not interchangeable products.

## 10. Host sharing variants

## 10.1 Share: None

Status: **Required baseline**

Files move through SFTP. No host directory is mounted in the guest.

## 10.2 Share: explicit read-only virtiofs

Status: **Supported after helper reboot and confinement certification**

One `virtiofsd` process per exact export or certified arrangement. Read-only enforcement must occur at the host export boundary.

## 10.3 Share: explicit read-write virtiofs

Status: **Advanced**

Guest root receives destructive authority over the exact host path. Full home sharing remains prohibited by default.

## 10.4 Share: exact block device

Status: **Advanced**

Requires exact identity, mode, exclusive write ownership, detach safety, and no system-disk auto-attachment.

## 11. Device variants

## 11.1 Device: None

Status: **Required baseline**

No host passthrough device beyond certified virtual devices and KVM access.

## 11.2 Device: PCI VFIO

Status: **Advanced hardware-dependent**

Supports selected GPU, accelerator, storage controller, NIC, or USB controller with exact IOMMU and recovery certification.

## 11.3 Device: mediated or virtual function

Status: **Hardware-dependent experimental or supported after proof**

Isolation claims must match actual hardware and firmware boundaries.

## 11.4 Device: USB forwarding

Status: **Future**

No automatic forwarding of newly connected devices.

## 12. Compute variants

## 12.1 Compute: fixed allocation

Status: **Required baseline**

Explicit vCPU and memory values. No autoscaler.

## 12.2 Compute: increase resources while running

Status: **Advanced**

CPU or memory increase only where exact VMM and guest behavior is proven.

## 12.3 Compute: resource removal

Status: **Experimental separately certified**

Decrease is not assumed symmetric with increase. Guest offlining, VMM support, failure behavior, and restart persistence require separate proof.

## 12.4 Compute: host CPU

Status: **Supported performance variant**

Maximizes local features; reduces snapshot and migration portability.

## 12.5 Compute: portable CPU model

Status: **Future until exact model and host set are certified**

Configuration availability is not support evidence.

## 13. Boot and image variants

## 13.1 Image: certified Linux baseline

Status: **Required baseline**

### Required contents

- Standard init system.
- Complete certified OpenSSH server package layout.
- Static AF_VSOCK socket/service units.
- Package manager.
- Filesystem and recovery tools.
- Serial console configuration.
- No reusable machine identity.
- No Z guest binary.

## 13.2 Image: alternate certified distribution

Status: **Future after second concrete implementation**

No generic distribution adapter may precede a second certified image.

## 13.3 Boot: pinned firmware

Status: **Required baseline after UEFI persistence gate**

Guest boot entries remain ordinary guest state. Any nonpersistent firmware-variable limitation must be recorded.

## 13.4 Boot: direct kernel

Status: **Advanced**

Exact kernel, initramfs, and command line. Does not silently replace firmware boot.

## 14. VMM variants

## 14.1 VMM: pinned Cloud Hypervisor

Status: **Required baseline**

Exact release and digest, seccomp, required Landlock, exact API/process identity, and compatibility tuple.

## 14.2 VMM: full QEMU compatibility

Status: **Future compatibility variant**

Separate launcher and certification only after a concrete guest or device need. No provider framework before implementation.

## 14.3 VMM: experimental alternate

Status: **Experimental only**

No equivalence claim until exact gains, losses, and tests exist.

## 15. Host identity and confinement variants

## 15.1 Identity: owner UID with fail-closed confinement

Status: **Required baseline**

The VMM runs as the owner but receives only exact machine assets, sockets, and devices. Landlock or equivalent required confinement must succeed.

## 15.2 Identity: dedicated machine account

Status: **Advanced hardened**

Provides stronger host identity separation with explicit privileged provisioning, ownership mapping, KVM access, and cleanup.

## 15.3 Isolation: hardened sealed computer

Status: **Supported profile**

- Network None.
- No host shares.
- No devices.
- Strict confinement or dedicated identity.
- Pinned assets.
- Read-only firmware and identity artifact.
- Optional ephemeral disk.
- Explicit portals only.

No perfect-containment claim.

## 16. Remote access variants

## 16.1 Remote: disabled

Status: **Required baseline**

No Z listener, tunnel, relay, cloud service, or remote authentication surface.

## 16.2 Remote: owner SSH to host

Status: **Supported external composition**

The owner connects to the host's independently managed SSH service, then uses Z exactly as locally. Z does not rewrite host SSH configuration.

## 16.3 Remote: nested OpenSSH composition

Status: **Supported after certification**

A remote OpenSSH client may reach the Z host and then invoke the same local descriptor-pass path. No guest SSH listener is exposed directly to the internet.

## 16.4 Remote: one-tool MCP edge

Status: **Future optional**

One edge invokes the same Z binary and same machine SSH/systemd paths. No separate executor, database, guest agent, or command semantics.

## 16.5 Remote: direct Z listener

Status: **Future or experimental only after concrete need**

Requires separate transport security, exposure, abuse, update, and lifecycle certification.

## 17. User experience variants

## 17.1 Experience: bare root shell

Status: **Required baseline**

```text
z
```

## 17.2 Experience: named computer

Status: **Required baseline**

```text
z work
```

Creates when absent because this command explicitly selects a machine through Z.

## 17.3 Experience: native SSH alias

Status: **Required baseline**

```text
ssh z-work
```

Starts existing machine if stopped. Does not create if missing.

## 17.4 Experience: exact command

Status: **Required baseline**

```text
z work -- executable argument
```

No implicit shell.

## 17.5 Experience: explicit shell

Status: **Required baseline**

Clearly distinct shell expression.

## 17.6 Experience: native systemd tools

Status: **Supported according to certified tuple**

Applicable systemd `--host` tools may target `root@z-work` through the same SSH alias.

## 18. Development and certification variants

## 18.1 Build: developer assets

Status: **Development only**

Locally built VMM, firmware, image, OpenSSH, or helper assets mark the machine uncertified.

## 18.2 Test: mock transport or VMM

Status: **Unit-test only**

Cannot satisfy end-to-end certification.

## 18.3 Test: nested KVM

Status: **Supported test mode on certified nested-KVM hosts**

Results record the nested environment and every unavailable hardware feature.

## 18.4 Test: OpenSSH interoperability matrix

Status: **Required release testing**

Tests exact host-client and guest-server versions, native tools, IDE clients, and configured variants.

## 19. Variant composition

### Expected supported compositions

- Baseline + `passt`.
- Baseline + Network None.
- Network None + local guest-service portals.
- Network None + exact reverse host-service portal.
- Baseline + cold snapshot.
- Baseline + per-machine owner key.
- Baseline + multiplexed SSH.
- Baseline + SSHFS.
- Baseline + explicit read-only virtiofs.
- Hardened identity + Network None + no shares.
- MCP edge + any locally certified machine, using the same Z binary.

### Compositions requiring explicit proof

- ControlMaster + host-key rotation.
- ControlMaster + fork or import.
- SSHFS + machine reboot.
- Live snapshot + active SSHFS.
- Live snapshot + durable portals.
- Live snapshot + VFIO.
- Live migration + host CPU.
- Live migration + writable host share.
- SSH TAP + host bridge.
- Dedicated host identity + arbitrary shares.
- User-mode networking + hostile-code containment claim.
- QEMU variant + Cloud Hypervisor snapshot.

## 20. Variant promotion

An experimental variant becomes supported only after:

1. Exact owner value is demonstrated.
2. Added processes and authority are documented.
3. Sacrifices are recorded.
4. Positive and negative certification passes.
5. Cleanup and recovery are proven.
6. Baseline behavior remains unchanged when disabled.

A supported variant becomes baseline only when:

1. The root-computer and SSH-native experience is materially incomplete without it.
2. Permanent complexity is less than the friction removed.
3. Capability ceiling is not lowered.
4. No permanent custom control plane is introduced.
5. The owner explicitly approves.

## 21. Initial frozen build selection

Unless amended through normative change control, the first build should target candidate tuple `z-debian-13.6-amd64-ch53-v1` from `docs/reference/DEPENDENCIES.md` and `assets/dependencies.lock.json`:

- Cloud Hypervisor v53.0 static x86-64 release asset at the locked digest.
- Cloud Hypervisor EDK2 `CLOUDHV.fd` at tag `ch-1e1b96f126` and the locked digest, subject to the UEFI persistence gate.
- Debian GNU/Linux 13.6 from snapshot `20260731T120000Z` for both the reference host and the first guest image.
- Rust 1.97.1, edition 2024, for the initial Z implementation toolchain.
- Raw persistent disk.
- SMBIOS-to-systemd credential bootstrap through the private VMM API; read-only credential medium only as a certified fallback.
- Reflink clone with sparse-copy fallback.
- Static OpenSSH over AF_VSOCK.
- Descriptor-pass lifecycle connector.
- Strict dynamic host-key lookup.
- Dedicated owner authentication key.
- Host systemd transient supervision.
- Owner UID with fail-closed VMM confinement.
- No host shares.
- No device passthrough.
- No remote access.
- `passt` ordinary connected profile.
- Network None available immediately.
- SFTP.
- Exact systemd execution.
- Serial recovery.
- Cold snapshot before live snapshot.
- Native SSH config export with explicit installation.
- Zero Z process in established SSH data paths.
- Zero Z processes while stopped.

The first implementation MUST certify this baseline before adding the broader catalog.
