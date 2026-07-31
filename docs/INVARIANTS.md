# Invariants — SSH-Native Z

Status: **Normative — SSH-native architecture revision**  
Applies to: **Every implementation, release, variant, interface, and certification claim**

## 1. Purpose

Z exists to give its owner a real, persistent, unrestricted Linux computer with almost nothing between the user and root.

A Z machine is also a first-class OpenSSH host. Its lifecycle may be entered through Z, but its shell, terminal, file-transfer, forwarding, and ordinary SSH behavior remain standard OpenSSH behavior.

Z is not a command-runner product, orchestration platform, hosted sandbox, workflow engine, synthetic Linux API, or new operating system. It is a minimal delivery, identity, transport-establishment, and lifecycle layer around an ordinary sovereign computer.

Every design decision MUST be judged first by whether it preserves that directness and second by whether it expands capability through mature native primitives rather than project-authored machinery.

## 2. Normative language

The terms **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

A lower-precedence document, test, implementation convenience, benchmark, compatibility claim, or external project behavior MUST NOT override this file.

## 3. Document precedence

When documents conflict, the following order controls:

1. `docs/INVARIANTS.md`
2. `docs/ANTI-INVARIANTS.md`
3. `docs/SACRIFICES.md`
4. `docs/SCOPE.md`
5. `docs/ARCHITECTURE.md`
6. `docs/VARIANTS.md`
7. `docs/SECURITY.md`
8. `docs/DECISIONS.md`
9. `docs/BUILD.md`
10. `docs/CERTIFICATION.md`

Tests prove implementation behavior. They do not legitimize a violation of a higher-precedence document.

## 4. Product invariants

### 4.1 The product is the computer

The primary product MUST be a real Linux computer, not an API representation of one.

The guest MUST be able to run ordinary Linux software without product-specific adaptation, including:

- Package managers.
- Compilers and build systems.
- Databases.
- Containers.
- System services.
- Timers and scheduled jobs.
- VPNs and network tools.
- Interactive shells and terminal applications.
- Long-running background processes.
- Filesystem tools.
- User and permission management.
- Kernel and device tooling permitted by the selected machine variant.

Z MUST NOT require those capabilities to be re-expressed as product operations before they can be used.

### 4.2 Unrestricted root inside the guest

The owner MUST have unrestricted root authority inside the guest.

Z MUST NOT impose an application-level allowlist on root actions inside the guest.

Security controls MAY restrict the guest's authority over the host. They MUST NOT silently convert guest root into a restricted shell, policy-constrained command subset, or simulated administrator account.

### 4.3 Persistent, ordinary Linux

The default machine MUST use a persistent writable Linux filesystem.

Changes made inside the machine MUST survive ordinary shell exit, client disconnect, machine reboot, and host process restart unless the owner explicitly selected an ephemeral variant.

The guest MUST remain recognizable and maintainable as ordinary Linux. Product-specific runtime dependencies inside the guest MUST be zero in the baseline.

### 4.4 Local sovereignty

Core operation MUST NOT require:

- A hosted model API.
- A hosted sandbox.
- A vendor control plane.
- A cloud account.
- An always-on internet connection.
- A proprietary remote service.
- A remote license check.

The owner MUST be able to locate, inspect, copy, back up, and delete every machine and its durable state using local filesystem access.

### 4.5 One direct user surface

The baseline MUST provide one user-facing Z executable.

Bare invocation MUST select the default machine, create it if absent, start it if stopped, wait until authenticated Linux access is available, and open an interactive root shell.

The ordinary path MUST NOT require the owner to manually perform separate create, prepare, boot, wait, attach, authenticate, and shell steps.

Advanced commands MAY expose those phases for inspection or recovery, but they MUST NOT become prerequisites for ordinary use.

### 4.6 SSH-native computer identity

Every machine MUST be representable as a native OpenSSH destination under a reserved Z alias namespace.

The baseline alias form SHOULD be:

```text
z-<machine-name>
```

The alias is a mutable label. The machine UUID and SSH host key are durable identity.

The following identity semantics are REQUIRED:

- Restart preserves identity.
- Full stop and start preserves identity.
- Rename preserves identity.
- Snapshot restoration of the same computer preserves identity.
- Fork or import-as-new creates new identity.
- An unproved host-key change is a hard identity failure.

### 4.7 Native SSH ecosystem compatibility

A Z SSH alias MUST work through the host's certified OpenSSH client without a Z-specific SSH implementation.

The baseline MUST support, through the same machine identity and transport where applicable:

- `ssh` interactive shell.
- SFTP.
- SCP using the certified OpenSSH implementation.
- `rsync` over SSH.
- SSH TCP forwarding.
- SSH Unix-socket forwarding.
- Standard IDEs and tools that consume OpenSSH configuration.
- Standard systemd remote tools that are supported by the certified systemd tuple.

Z MAY provide convenience wrappers. The native SSH path MUST remain available.

### 4.8 Complementary execution planes

Z MUST distinguish three execution semantics.

#### Interactive SSH execution

Interactive SSH MUST preserve native OpenSSH behavior for:

- PTY allocation.
- Terminal resizing.
- Interactive signals.
- Standard input.
- Standard output.
- Standard error as represented by SSH.
- Shell and terminal applications.
- SSH exit status and exit signal where the protocol and client expose them.

#### Native SSH remote-command execution

An ordinary SSH remote command uses SSH command-string semantics and the guest user's shell behavior. Z MUST NOT represent it as exact argument-array execution.

#### Exact argument-safe execution

Z's exact execution surface MUST preserve:

- Exact executable and argument boundaries.
- Explicit working directory.
- Explicit environment selection.
- Standard input bytes.
- Separate standard output and standard error bytes.
- Exact normal exit status or terminating signal.
- No implicit shell.

The baseline exact path SHOULD use remote systemd transient services and standard file transfer for noninteractive standard streams.

Shell interpretation MUST be explicit.

### 4.9 Honest combined-mode boundary

The baseline is not required to provide arbitrary exact `argv[]` execution directly attached to a live PTY in one operation when stock SSH and remote systemd cannot jointly provide that semantic without a guest helper.

This exact absence MUST be documented in `docs/SACRIFICES.md`.

Z MUST NOT add a guest agent or custom protocol merely to conceal this standard boundary.

### 4.10 No fake success

Z MUST NOT report success when:

- The machine did not start.
- The SSH connection was not authenticated.
- The command was not accepted by the guest.
- The guest command returned failure.
- The connection ended before outcome was known.
- Required output could not be completely retrieved.
- File transfer or atomic finalization was incomplete.
- A requested stop left a verified VMM running.
- Cleanup removed only part of an owned resource set.

Unknown is not success.

## 5. SSH architecture invariants

### 5.1 OpenSSH owns the SSH data plane

The baseline MUST use the certified OpenSSH client and server for SSH protocol behavior.

When the host supports descriptor passing, Z's SSH `ProxyCommand` MUST use `ProxyUseFdpass=yes` or equivalent descriptor handoff.

After successful descriptor transfer:

- Z MUST exit from the SSH data path.
- Z MUST NOT relay SSH bytes.
- Z MUST NOT terminate encryption.
- Z MUST NOT parse SSH channels.
- Z MUST NOT reproduce PTY, SFTP, forwarding, signal, or terminal semantics.

A stdio relay MAY exist only as an explicitly named compatibility variant whose extra process and limitations are certified.

### 5.2 Lifecycle-aware connection establishment

The SSH connector MAY:

- Resolve an existing machine alias.
- Inspect machine state.
- Start a stopped existing machine.
- Wait for exact VMM transport availability.
- Verify the VMM, runtime socket, and machine binding.
- Connect the Cloud Hypervisor vsock mux to the requested guest port.
- Pass the connected descriptor to OpenSSH.

The connector MUST NOT:

- Silently create a missing machine from an ordinary third-party SSH probe.
- Repair durable state without an explicit repair command.
- Rotate credentials.
- Trust a PID or socket path alone.
- Accept arbitrary host paths supplied through an SSH alias.
- Remain as a byte proxy after handoff.

### 5.3 Strict alias grammar

Machine names and SSH aliases MUST use a grammar that is safe in every command-bearing OpenSSH configuration context.

The baseline machine-name grammar SHOULD be limited to lowercase ASCII letters, digits, and interior hyphens, with bounded length.

Every SSH helper MUST validate the alias independently.

A matching `Host z-*` stanza is not validation.

### 5.4 No shell-unsafe SSH configuration

Z-generated SSH configuration MUST NOT use arbitrary owner strings inside:

- `ProxyCommand`.
- `KnownHostsCommand`.
- `LocalCommand`.
- `RemoteCommand`.
- `Match exec`.

The Z executable path used by command directives MUST be absolute.

Z MUST account for OpenSSH's rule that token expansion is not shell-escaped.

### 5.5 Strict prebound host verification

Every machine MUST have a unique host key before its first authenticated SSH connection.

The host MUST verify the guest against durable prebound identity.

The baseline MUST use:

- `StrictHostKeyChecking=yes` or stricter equivalent.
- A machine-bound host key lookup.
- No trust-on-first-use.
- No automatic acceptance of changed keys.
- No `ssh-keyscan` result as an independent trust decision.
- No disabling host verification because transport is local.

A read-only `KnownHostsCommand` MAY expose machine-bound public keys to OpenSSH.

That command MUST return nonzero on internal error and MUST NOT mutate state.

### 5.6 Explicit owner authentication

The base image MUST contain no reusable owner private key, host private key, password, or shared machine secret.

The baseline SHOULD use one dedicated Z owner key for seamless wildcard SSH configuration.

A per-machine owner key and hardware-backed owner key MAY be supported as stricter variants.

The generated baseline profile MUST prevent ambient identity use by selecting the intended key explicitly, enabling `IdentitiesOnly`, and disabling implicit ssh-agent use.

### 5.7 Hermetic internal SSH

Z's internal control operations MUST NOT inherit arbitrary semantics from the owner's general SSH configuration.

Internal SSH MUST explicitly control at least:

- Configuration-file source.
- Proxy path.
- Host-key source and strictness.
- Identity file.
- Agent use.
- Password and keyboard-interactive authentication.
- Forwarding.
- X11.
- Local commands.
- Remote commands.
- Environment forwarding.
- Connection timeouts.

The owner-facing native SSH profile MAY remain configurable because it is an owner interface, not product control authority.

### 5.8 Explicit SSH-config mutation

Z MUST NOT silently rewrite the owner's global SSH configuration.

Z SHOULD provide:

- Print.
- Dry-run or diff.
- Explicit install.
- Explicit remove.
- Effective-config verification using the certified OpenSSH client.

Install and remove MUST be atomic, marker-bounded, idempotent, and data-preserving.

Inspection MUST remain non-mutating.

### 5.9 Static standard guest SSH service

The baseline guest MUST use standard OpenSSH and standard systemd socket activation over AF_VSOCK.

The certified configuration SHOULD use:

- A static socket unit.
- `Accept=yes`.
- A per-connection service.
- Stock `sshd -i`.
- Explicit host-key and authorized-key paths.

The baseline MUST NOT depend on `systemd-ssh-generator` auto-detection for the sole control path.

No Z binary or Z daemon may run inside the guest.

### 5.10 Standard credential bootstrap

Machine identity and owner admission MUST be delivered through standard systemd system credentials supplied by the pinned VMM through SMBIOS Type 11 OEM strings.

The baseline MUST:

- Keep the machine UUID and SSH host private key authoritative in the machine directory.
- Supply credentials through Cloud Hypervisor's private machine-specific API socket rather than exposing reusable secrets in process arguments.
- Use binary credentials for binary key material.
- Import credentials into the socket-activated SSH service with standard systemd `ImportCredential=` semantics.
- Pass explicit host-key and authorized-key paths to stock `sshd -i`.
- Ensure credentials are unavailable to unrelated guest services through service credential isolation where supported.
- Treat authenticated SSH as final readiness evidence even when a `vmm.notify_socket` boot notification is used.

A separate read-only standard credential medium MAY exist only as a certified fallback variant when the exact VMM, firmware, kernel, systemd, or distribution tuple cannot consume the required SMBIOS credentials.

The fallback MUST NOT create a second durable authority for the same private host key.

## 6. Architectural invariants

### 6.1 Real hardware virtualization

The baseline MUST use KVM hardware-assisted virtualization on supported Linux hosts.

A container, namespace, chroot, process sandbox, or userspace syscall emulation layer MUST NOT be presented as equivalent to the baseline virtual machine.

### 6.2 Preserve the machine capability ceiling

The baseline VMM MUST remain capable of supporting a general-purpose Linux machine and declared advanced variants, including the applicable combination of:

- Persistent block storage.
- Multiple virtual CPUs.
- Configurable memory.
- Virtio devices.
- AF_VSOCK transport.
- User-mode and bridged networking.
- Explicit host directory sharing.
- Device passthrough.
- Snapshot and restore.
- Hotplug where proven.
- Migration where proven.

A smaller VMM MUST NOT replace the baseline merely because it reduces code or startup time if it materially lowers this capability ceiling.

### 6.3 The host owns lifecycle, identity, and transport establishment only

The host-side product MUST own only the minimum functions required to:

- Materialize a machine.
- Verify required assets.
- Establish machine identity.
- Start, supervise, inspect, stop, and recover the VMM.
- Establish authenticated SSH transport.
- Copy files through standard SFTP.
- Configure explicitly selected host integrations.

Packages, services, users, jobs, logs, shells, files, and application processes inside the guest MUST remain Linux responsibilities.

The host MUST NOT mirror ordinary guest state into a second control model.

### 6.4 No permanent custom control plane

The baseline MUST have:

- No permanent custom controller daemon.
- No permanent custom broker.
- No custom scheduler.
- No custom guest agent.
- No custom guest protocol.
- No product database.
- No mandatory relay.

All project processes MUST exit when all machines are stopped and no explicit foreground command is active.

### 6.5 Native service-manager supervision

The baseline SHOULD use the host service manager directly to own each running machine and its selected helpers.

A custom machine supervisor MUST NOT exist when a host systemd transient service can provide the required ownership, cgroup, logging, restart, and cleanup semantics.

The host service manager is runtime authority, not a product database.

### 6.6 Zero project processes at rest

When every machine is stopped, the baseline MUST leave zero project-owned background processes running.

Operating-system facilities such as systemd itself are not project-owned processes.

### 6.7 Native primitives before product code

A mature operating-system or protocol primitive MUST be preferred when it supplies the required semantics without unacceptable loss.

The baseline SHOULD compose:

- OpenSSH for authentication, shells, PTYs, SFTP, forwarding, and ecosystem compatibility.
- AF_VSOCK for control independent of guest IP networking.
- systemd for host supervision and guest services.
- `systemd-stdio-bridge` and native remote systemd tools where certified.
- Filesystem directories and atomic files for durable metadata.
- File locks for local mutation exclusion.
- Reflinks or sparse copies for disk cloning.
- Seccomp and Landlock for VMM confinement.

### 6.8 One durable authority per fact

Baseline durable authorities are:

- Machine directory for configuration, identity artifacts, and owned files.
- Guest disk for guest state.
- Identity volume or certified equivalent for private machine host identity.
- Host service manager and VMM API for current process state.
- Authenticated SSH transport for guest readiness.

Derived public keys, fingerprints, indexes, and diagnostics MUST NOT become competing authority.

### 6.9 Derive runtime state

Machine state SHOULD be derived from observable reality rather than speculative labels.

Concise states MAY be reported only when each state is derived from concrete evidence.

A stale metadata field, control socket, SSH master, PID, or systemd unit name MUST NOT overrule verified process, API, disk, transport, and identity evidence.

### 6.10 Explicit optionality

Capabilities that add processes, privileges, host exposure, durable services, or maintenance burden MUST be optional unless required for the baseline root-computer experience.

Disabling an optional feature MUST remove its authority and runtime footprint.

## 7. Storage and identity invariants

### 7.1 The disk is the computer

The primary guest disk MUST be a normal inspectable disk image whose contents represent machine durable state.

The baseline MUST NOT depend on an opaque product datastore.

### 7.2 Simple cloning

The baseline SHOULD use raw disk images with reflink cloning where supported and sparse-copy fallback otherwise.

Backing chains, custom formats, and hidden block stores MUST NOT enter the baseline.

### 7.3 Restore is not fork

A snapshot restored as the same computer MUST preserve identity.

A fork or import-as-new MUST rotate identity, including at least:

- Machine UUID.
- SSH host key.
- Vsock identity allocation.
- MAC addresses.
- Guest machine ID as applicable.
- Firmware or SMBIOS machine identity as applicable.

### 7.4 Atomic metadata

Small metadata updates MUST use a crash-safe temporary-write, synchronization, atomic-rename, and parent-synchronization pattern appropriate to the host filesystem.

### 7.5 Owner-visible layout

Every durable machine artifact MUST have a documented location and role.

No durable truth may exist only in an undocumented cache, database, daemon-private path, or transient unit property.

## 8. SSH portal invariants

### 8.1 Portals are native SSH forwarding

A Z portal MUST be a thin expression of native OpenSSH forwarding.

Z MUST NOT invent a tunnel protocol or durable tunnel controller.

### 8.2 Safe default bind

A local TCP portal MUST bind to loopback by default.

A local Unix-socket portal MUST be created beneath an owner-private runtime directory with restrictive mode.

Binding to a wildcard, LAN address, or privileged port MUST be explicit.

### 8.3 Forward establishment honesty

Portal creation MUST use `ExitOnForwardFailure=yes` or equivalent behavior.

Successful listener creation MUST NOT be represented as proof that the ultimate destination service is healthy.

### 8.4 No implicit credential forwarding

Agent, X11, GSSAPI delegation, and arbitrary host environment forwarding MUST be disabled by default.

Agent forwarding MUST carry an explicit warning that guest root can request signatures from the forwarded agent.

### 8.5 No portal registry authority

Foreground portals require no durable Z state.

A durable portal MAY be represented as an exact host systemd transient service or explicit owner configuration. Z MUST NOT mirror it into a second job or tunnel lifecycle database.

## 9. Networking invariants

### 9.1 Control independent of guest networking

The owner MUST be able to boot, verify identity, open a shell, execute exact commands, and copy recovery files without a guest IP network.

### 9.2 Network None means no NIC

The certified Network None variant MUST attach no guest IP network device.

Guest-side administrative disablement is not equivalent because the owner has unrestricted root.

SSH over AF_VSOCK and explicit portals remain available.

### 9.3 Full-power network alternatives

The ordinary connected profile MAY use `passt`.

Bridge/TAP, SSH TUN/TAP, and device passthrough MAY exist as explicit variants.

No low-friction profile may permanently remove access to full-power alternatives.

## 10. Security invariants

### 10.1 Host protection without guest restriction

Host security MUST constrain the VMM, helpers, filesystem access, devices, and integrations. It MUST NOT weaken guest root.

### 10.2 Least host authority

Every host process MUST receive only the required files, descriptors, devices, namespaces, sockets, groups, and network authority.

The VMM MUST use certified seccomp and filesystem confinement. The certified baseline MUST fail closed if its required confinement cannot be applied.

### 10.3 Exact runtime socket authority

API, serial, control, vsock-mux, SSH-control, and forwarding sockets MUST reside under private machine runtime roots.

Path, owner, inode, process start identity, executable, and machine binding MUST be verified before adoption or use.

### 10.4 Path confinement

Product-managed path operations MUST use descriptor-relative and race-resistant handling where available.

String-prefix checks alone are prohibited.

### 10.5 Pinned executable assets

The VMM, firmware, base image, OpenSSH client/server tuple, systemd tuple, and required helper binaries MUST be pinned and digest-verifiable for a certified release.

### 10.6 Honest boundaries

Z MUST NOT claim perfect containment, universal snapshot portability, universal migration compatibility, or SSH semantics that the protocol does not provide.

## 11. Recovery invariants

### 11.1 SSH is primary; serial is independent recovery

SSH is the primary owner interface. A reconnecting serial console MUST remain available independently for recovery after guest SSH configuration or userspace failure.

### 11.2 No single fragile controller

Loss of the user-facing process, SSH client, FD-pass helper, or systemd client MUST NOT corrupt the disk or make the machine unrecoverable.

### 11.3 Process adoption is evidence-based

PID, unit name, socket path, or SSH control socket alone is insufficient for adoption, signaling, or killing.

### 11.4 Cleanup is exact

Cleanup MUST remove only exact owned resources and MUST be idempotent.

### 11.5 Data-preserving failure

When uncertain, preserve disks, identity artifacts, metadata, snapshots, and exports. A broken state is preferable to destructive guesswork.

## 12. Variant invariants

Every variant MUST:

- Preserve the core real-computer and SSH-native definitions unless explicitly non-core.
- Declare added processes, privileges, state, host exposure, and capability changes.
- Use the same machine identity and standard SSH transport where applicable.
- Fail closed when prerequisites are absent.
- Leave baseline authority and runtime unchanged when disabled.
- Avoid a second controller, database, executor, guest protocol, or SSH implementation.

## 13. Build and certification invariants

### 13.1 The first checkpoint is usable

The first checkpoint MUST:

- Boot a real KVM machine.
- Establish unique machine SSH identity before first connection.
- Open unrestricted root through stock OpenSSH over AF_VSOCK.
- Persist a filesystem change.
- Reboot.
- Reconnect through the same identity.
- Preserve the change.
- Stop cleanly.
- Leave zero Z processes at rest.

### 13.2 End-to-end evidence before variants

Before capability expansion, the baseline MUST demonstrate:

- Asset verification.
- Machine materialization.
- Host systemd supervision.
- Static vsock SSH socket activation.
- Strict host-key verification.
- Owner authentication.
- FD handoff with Z exiting the data path.
- Interactive PTY and resize.
- SFTP transfer.
- Exact non-shell execution.
- Persistent reboot.
- Serial recovery.
- Abrupt client and VMM recovery.
- Host-path confinement.

### 13.3 Ecosystem certification

A certified release MUST test its generated profile with selected native consumers, including OpenSSH tools and at least one major Remote SSH IDE.

### 13.4 Negative certification

Certification MUST attempt:

- SSH token and alias injection.
- Wrong-machine host key.
- Changed host key.
- Stale mux socket adoption.
- Ambient SSH config override of internal control.
- Ambient agent use.
- Undeclared forwarding.
- External port exposure without explicit bind.
- SFTP partial transfer and failed rename.
- Reuse of a multiplexed master across identity change.
- Guest access to undeclared host files.
- Residual helpers after stop.
- Unknown outcome misreported as success.

### 13.5 No simulated certification

Mocks may support unit tests. They cannot satisfy release certification.

### 13.6 Every sacrifice is explicit

Any intentional loss of power, portability, isolation, durability, compatibility, or convenience MUST be recorded before implementation acceptance.

## 14. Change control

A change to this file requires:

1. A precise statement of behavior added, removed, or weakened.
2. Comparison against the direct-root-computer and SSH-native purpose.
3. Updates to affected anti-invariants, variants, sacrifices, architecture, security, and certification.
4. Evidence that optional complexity has not silently become baseline complexity.
5. Explicit owner approval.

The burden of proof belongs to any proposal that adds architecture, state, processes, protocols, services, restrictions, or a second authority.
