# Anti-Invariants — SSH-Native Z

Status: **Normative prohibition list**  
Applies to: **Architecture, implementation, tests, packaging, documentation, product claims, and SSH integrations**

## 1. Purpose

This file names designs Z rejects even when they appear convenient, enterprise-ready, extensible, secure, or SSH-compatible.

An anti-invariant is not a preference. It is a prohibited direction because it reconstructs Linux or SSH, adds a second authority, lowers machine power, introduces hidden host authority, or adds permanent architecture without owner value.

## 2. No reconstruction of Linux as product APIs

Z MUST NOT create mandatory product operations for ordinary Linux concepts such as:

- Processes.
- Packages.
- Services.
- Users.
- Filesystem navigation or editing.
- Jobs and schedules.
- Logs.
- Shells and terminals.
- Containers.
- Environment management.
- Network service management inside the guest.

Convenience wrappers MAY invoke native tools. They MUST NOT become the only path or a second semantic authority.

## 3. No operation registry

The baseline MUST NOT contain a canonical operation registry, generated capability catalog, provider registry, handler registry, schema compiler, or tool inventory for ordinary computer use.

CLI, SSH, systemd, SFTP, remote, and automation surfaces SHOULD remain thin paths into the same machine.

## 4. No custom SSH protocol

Z MUST NOT invent:

- An SSH replacement.
- An SSH extension required for baseline operation.
- A custom channel protocol.
- A custom PTY protocol.
- A custom signal protocol.
- A custom terminal-resize protocol.
- A custom file-transfer protocol.
- A custom forwarding protocol.
- A custom authentication exchange.
- A custom host-key protocol.

The baseline MUST use stock OpenSSH behavior.

## 5. No fake SSH wrapper

A Z command that invokes SSH MUST NOT hide materially different semantics while presenting itself as equivalent to native OpenSSH.

Z MUST NOT implement a permanently incomplete shadow of:

- `ssh` options.
- SFTP.
- SCP.
- Forwarding.
- Jump hosts.
- Multiplexing.
- IDE integration.

When users need full SSH behavior, Z MUST expose native OpenSSH configuration and allow native clients to connect.

## 6. No unnecessary Z SSH byte proxy

The native OpenSSH profile MUST use descriptor handoff when the certified client supports `ProxyUseFdpass`.

A Z process MUST NOT remain in the byte path merely because a conventional proxy implementation is easier.

A connection-scoped stdio relay is permitted only in the explicit compatibility profile for an SSH client or library that cannot receive a passed descriptor. Such a relay MUST:

- Remain byte-transparent.
- Avoid parsing or terminating SSH.
- Carry no independent authentication semantics.
- Exit with the connection.
- Create no durable state.
- Never become the baseline for native OpenSSH clients.

## 7. No custom guest protocol

Z MUST NOT invent a guest frame protocol, message envelope, replay protocol, execution RPC, file RPC, PTY handshake, signal handshake, or agent transport for capabilities already supplied by OpenSSH, systemd, SFTP, D-Bus, or ordinary files.

## 8. No custom guest agent

The baseline guest MUST NOT run a Z-authored agent, helper daemon, scheduler, update service, monitor, broker, lifecycle service, or protocol server.

Static configuration of standard systemd and OpenSSH facilities is not a Z guest agent.

A guest helper MUST NOT be added merely to combine exact `argv[]` and PTY semantics in one operation.

## 9. No dependency on automatic SSH generator behavior

The sole baseline access path MUST NOT depend on `systemd-ssh-generator` detecting, synthesizing, or overriding the guest SSH configuration correctly at early boot.

The certified image MUST use explicit static socket and service units or another exact certified standard configuration.

## 10. No reusable image identity

A distributed image MUST NOT contain:

- A reusable SSH host private key.
- A reusable owner authentication private key.
- A known password.
- A shared authorized key intended for production access.
- A machine UUID copied across installations.

Every machine MUST receive unique identity before first authenticated connection.

## 11. No trust-on-first-use baseline

The baseline MUST NOT use:

- `StrictHostKeyChecking=no`.
- `StrictHostKeyChecking=accept-new`.
- Automatic yes prompts.
- Localhost exemptions.
- IP-address trust in place of machine identity.
- `ssh-keyscan` output as self-authenticating evidence.

A host key MUST be prebound to machine identity.

## 12. No silent host-key acceptance or replacement

A changed, missing, malformed, or unexpected host key MUST NOT be silently inserted, replaced, ignored, or repaired.

Host-key rotation MUST prove continuity through an already trusted identity or require an explicit owner trust reset.

## 13. No alias-as-identity

A machine name, SSH alias, path, PID, vsock CID, MAC address, IP address, or systemd unit name MUST NOT be treated as the complete identity of a machine.

Rename MUST NOT rotate the machine. Fork MUST NOT preserve the original identity.

## 14. No shell-unsafe SSH aliasing

Z MUST NOT allow arbitrary strings to flow from an SSH target into a command-bearing directive.

Prohibited designs include:

- Arbitrary Unicode or whitespace in machine names used by SSH helpers.
- Quotes, shell metacharacters, slashes, control bytes, or path traversal in aliases.
- `Match exec` for machine discovery.
- Relative paths to the Z executable in `ProxyCommand`.
- Passing an unvalidated `%h`, `%n`, `%r`, `%p`, or `%H` to a shell command.

Every helper MUST validate again after OpenSSH matching.

## 15. No hidden machine creation from SSH discovery

Ordinary third-party actions such as:

- `ssh -G`.
- IDE host discovery.
- Config parsing.
- `KnownHostsCommand` execution.
- Tab completion.
- Connection probes.
- A mistyped alias.

MUST NOT silently allocate a new machine in the baseline.

Direct native SSH MAY start an existing stopped machine. Creation remains an explicit Z action.

An autocreate-on-SSH mode requires an explicit variant and unmistakable naming or configuration.

## 16. No mutating host-key lookup

`KnownHostsCommand` or equivalent host-key lookup MUST NOT:

- Create a machine.
- Start a machine merely to discover identity.
- Rotate a key.
- Repair metadata.
- Rewrite trust files.
- Accept a presented key.
- Contact an untrusted guest to decide what key to trust.

It is a read-only projection of durable prebound identity.

## 17. No ambient user SSH configuration for internal control

Z's internal lifecycle, exact execution, file copy, readiness, and stop operations MUST NOT inherit arbitrary user SSH directives.

Internal control MUST reject or override ambient:

- `ProxyCommand`.
- `ProxyJump`.
- `LocalCommand`.
- `RemoteCommand`.
- `Match exec`.
- Forwardings.
- Agent selection.
- Identity selection.
- Host-key policy.
- Environment forwarding.
- X11.
- Connection multiplexing.

The owner-facing native SSH surface may remain owner-configurable.

## 18. No automatic agent forwarding

The baseline MUST NOT automatically forward the owner's SSH agent.

Agent forwarding is an explicit variant because guest root can request authentication operations from the forwarded agent while the channel exists.

## 19. No automatic X11 or desktop credential forwarding

Z MUST NOT automatically forward:

- X11.
- Wayland sockets.
- D-Bus user sockets.
- GPG agents.
- Browser sessions.
- Desktop portals.
- Credential stores.

Each is a separate authority transfer requiring explicit selection and certification.

## 20. No implicit SSH forwarding

The baseline MUST NOT create local, remote, dynamic, Unix-socket, or TUN/TAP forwards merely because a machine starts.

A portal MUST be explicit.

## 21. No wildcard external bind by default

SSH local forwards MUST NOT bind to all host interfaces by default.

Remote forwards MUST NOT be made externally reachable by default.

Unix sockets MUST NOT be placed in shared writable directories.

External exposure requires an explicit bind address and authority statement.

## 22. No tunnel success overclaim

Creating an SSH forwarding listener MUST NOT be reported as proof that:

- The ultimate service is running.
- The destination is authorized by an application.
- The guest network is isolated.
- Data sent later will succeed.

Forward setup success and service health are different facts.

## 23. No portal registry or tunnel controller

The baseline MUST NOT create a durable portal database, reconciliation loop, port allocator service, tunnel controller, or background relay fabric.

Foreground portals are native SSH processes. Durable portals may be exact systemd transient units or owner-authored SSH configuration.

## 24. No SSH multiplex master as lifecycle authority

A `ControlMaster` socket or live master connection MUST NOT prove that:

- The current VMM is correct.
- The disk is attached correctly.
- The guest identity is current.
- The machine is ready.
- A stopped machine is running.

A master connection MUST NOT survive machine identity replacement, fork, import-as-new, or trust rotation.

## 25. No compression by default on mixed-trust channels

Z SHOULD NOT enable SSH compression by default, especially when trusted interactive traffic and untrusted forwarded traffic may share one connection.

## 26. No native SSH command misrepresented as exact argv

SSH protocol `exec` carries a command string. OpenSSH normally invokes the remote user's shell for command execution.

Z MUST NOT concatenate an argument list into an SSH command and call the result exact argument execution.

Exact argument-safe execution must use its separate proven plane.

## 27. No guest helper to erase the exact-argv/PTY boundary

The baseline MUST NOT add a launcher, subsystem, shim, or manifest protocol solely to provide exact argument arrays and a live PTY in one operation.

The honest split between interactive SSH and exact noninteractive systemd execution is preferred.

## 28. No permanent controller

Z MUST NOT install or require an always-running custom controller, broker, socket activator, watcher, queue worker, reconciler, relay, or supervisor when all machines are stopped.

A machine-specific standard systemd unit may exist while its machine runs.

## 29. No custom machine supervisor when systemd suffices

The baseline MUST NOT add a Z-authored machine supervisor process if the host systemd manager can directly own the VMM and its selected helpers with correct lifecycle semantics.

## 30. No product database

The baseline MUST NOT use SQLite, PostgreSQL, BoltDB, RocksDB, an event store, or another database for machine, SSH identity, portal, or lifecycle authority.

Machine directories, disks, identity artifacts, atomic metadata, systemd state, VMM evidence, and authenticated SSH are sufficient.

## 31. No duplicated lifecycle state machine

Z MUST NOT maintain written lifecycle truth that can disagree with observed machine reality.

A metadata field, SSH master, or operation record MUST NOT overrule current verified evidence.

## 32. No hidden scheduler or job fabric

Z MUST NOT become a durable workflow engine, task queue, CI runner, transaction fabric, or distributed scheduler.

Durable work belongs inside Linux through systemd, timers, tmux, screen, application queues, and ordinary files.

## 33. No idempotency theater

Z MUST NOT require generalized idempotency keys, request digests, leases, replay journals, or exactly-once claims for ordinary computer use.

Safe repetition should come from inspection, locks, exact ownership, and native idempotence.

## 34. No architecture-first milestone

A repository layout, interface, SSH config generator, schema, protocol description, unit template, or test harness without a real booted root computer is not a product checkpoint.

The first checkpoint must open root, prove identity, persist state, reboot, reconnect, and preserve the state.

## 35. No speculative abstraction

Z MUST NOT create abstractions for unimplemented second distributions, VMMs, transports, key providers, portal backends, or remote edges.

A second concrete implementation may justify a narrow extracted interface afterward.

## 36. No generic plugin system

The trusted baseline MUST NOT load arbitrary plugins.

Optional capabilities should be compiled paths, explicit subprocesses, or configuration-selected known implementations.

## 37. No second execution path for ChatGPT or remote clients

An MCP, ChatGPT, web, relay, or remote interface MUST NOT create its own executor, SSH identity, guest protocol, lifecycle controller, or machine database.

It must invoke the same local Z binary and same standard SSH/systemd paths used locally.

## 38. No mandatory relay or hosted dependency

Core local use MUST NOT depend on a hosted relay, tunnel provider, web dashboard, OAuth service, cloud database, hosted queue, vendor secret store, telemetry endpoint, or remote license service.

## 39. No container substitution

Containers, namespaces, chroots, and syscall sandboxes MUST NOT be presented as equivalent to the KVM baseline.

## 40. No smaller VMM at the cost of power

A VMM MUST NOT replace Cloud Hypervisor solely because it has fewer lines of code, faster boot, or fewer devices if it materially lowers the declared capability ceiling.

## 41. No full legacy emulation by default

A broad legacy emulator MUST NOT enter the baseline merely for theoretical compatibility.

A QEMU variant may exist separately after concrete need and distinct certification.

## 42. No mandatory SSH-over-IP control spine

Control MUST NOT depend on DHCP, guest IP discovery, DNS, routing, firewall rules, or TCP port forwarding.

The baseline control spine is OpenSSH over AF_VSOCK.

## 43. No claim that SSH forwarding is hostile-code containment

SSH forwarding is an authenticated capability channel, not proof of complete network isolation.

Network None must be enforced by absence of a NIC, and each portal must be described by its actual authority.

## 44. No guest-side-only Network None

An attached interface that guest root can re-enable is not equivalent to Network None.

The certified Network None variant must attach no IP network device.

## 45. No invisible device authority

Z MUST NOT auto-attach host devices, GPUs, USB devices, block devices, privileged sockets, or character devices.

Device authority must be exact and explicit.

## 46. No default host-home exposure

Z MUST NOT automatically share the owner's home, repository, SSH configuration, cloud credentials, browser data, secret stores, agent sockets, or host root filesystem.

SFTP from guest to host is not implied. Host-to-guest SFTP is owner-directed transfer.

## 47. No hidden host service exposure through reverse forwarding

A remote SSH forward from guest to host MUST expose only the exact selected host address or Unix socket.

Z MUST NOT offer a generic host-service bridge by default.

## 48. No custom bootstrap medium when standard credentials work

The baseline MUST NOT add an identity disk, cloud-init control disk, custom metadata filesystem, custom credential protocol, or first-boot mutator when Cloud Hypervisor SMBIOS OEM strings and systemd system credentials satisfy the exact bootstrap contract.

A read-only standard credential medium MAY exist only as a certified fallback variant and MUST NOT become a second durable authority.

Z MUST NOT place reusable private keys in the base image, process command line, source tree, release archive, or public examples.

## 49. No fragile backing chains by default

The default machine MUST remain independently readable without a mutable external backing image.

## 50. No snapshot overclaim

Live snapshots MUST NOT be claimed portable across arbitrary VMM, firmware, kernel, CPU, device, or host versions.

Cold disk snapshots and live VMM snapshots are different products.

## 51. No restore/fork identity confusion

Restoring the same computer MUST NOT silently rotate its SSH identity.

Forking a new computer MUST NOT silently reuse the source SSH identity.

## 52. No destructive cleanup to restore appearances

Z MUST NOT delete a guest disk, credential-medium fallback, snapshot, machine directory, or ambiguous durable artifact merely to return a clean status.

## 53. No PID-only or socket-only adoption

A PID, systemd unit, control socket, mux socket, API socket, or SSH control socket alone is insufficient for adoption, signaling, or killing.

## 54. No prefix-only path security

String-prefix checks MUST NOT be the sole managed-path defense.

Implementation must address symlinks, hard links, mount points, rename races, traversal, and time-of-check/time-of-use behavior.

## 55. No ambient owner-home access for the VMM

Running the VMM under the owner UID MUST NOT give it unrestricted access to everything the owner can read.

Certified filesystem and syscall confinement must fail closed.

## 56. No security by guest weakness

Host security MUST NOT be achieved by removing guest root, compilers, package installation, containers, networking tools, or ordinary Linux authority.

## 57. No security theater

Every control must identify:

- Threat.
- Protected asset.
- Enforcement boundary.
- Failure behavior.

Extra keys, signatures, prompts, policies, or logs without a distinct boundary are prohibited ceremony.

## 58. No certificate hierarchy without need

The single-owner local baseline MUST NOT create a per-machine certificate authority, enrollment service, or certificate-rotation control plane when direct SSH host keys and public-key authentication suffice.

An optional team or fleet certificate variant must prove the need first.

## 59. No enterprise theater

The baseline MUST NOT add tenants, organizations, roles without enforcement, approval chains, billing, policy engines, fleet dashboards, distributed consensus, high availability, service meshes, or Kubernetes operators.

## 60. No durability theater

Z MUST NOT claim exactly-once or transactional semantics for arbitrary guest commands.

Guest-native durability is honest. Host-side universal command transaction simulation is not.

## 61. No compatibility theater

Z MUST NOT claim support for untested combinations of:

- OpenSSH clients and servers.
- systemd versions.
- Distributions.
- Kernels.
- Cloud Hypervisor versions.
- Firmware.
- Host filesystems.
- IDEs.
- Forwarding modes.
- Snapshot formats.

Supported tuples must be certified.

## 62. No observability platform

Z MUST NOT build a metrics backend, trace service, log aggregator, event bus, or telemetry pipeline.

Native logs and concise diagnostics are sufficient.

## 63. No updater daemon

Z MUST NOT install a permanent automatic updater.

Updates must be explicit, verifiable, and reversible where practical.

## 64. No hidden mutation during inspection

Status, inspect, list, version, SSH host-key lookup, SSH-config print, dry-run, and verification MUST NOT create, start, repair, rotate, mount, forward, or rewrite unless their command explicitly promises mutation.

An SSH connection may start an existing stopped machine because connection establishment is explicitly mutating lifecycle behavior. Host-key lookup remains read-only.

## 65. No baseline dependency explosion

A baseline feature MUST NOT add a large dependency graph when Linux, OpenSSH, systemd, Cloud Hypervisor, SFTP, or a small dedicated helper already supplies it.

## 66. No implementation-language monoculture claim

One user-facing Z binary does not require reimplementing OpenSSH, systemd, SFTP, VMM, firmware, or networking helpers in Z's implementation language.

## 67. No documentation drift

Documentation MUST NOT describe:

- Planned SSH features as implemented.
- Native SSH command strings as exact argv.
- Network None as an attached disabled NIC.
- Restore as fork.
- A relay variant as descriptor handoff.
- Experimental IDE or systemd-tool compatibility as certified.

## 68. No tests as policy overrides

Passing tests do not excuse a violation of these rules.

## 69. No silent sacrifice

Any reduction in root authority, SSH compatibility, device capability, networking, persistence, recoverability, portability, identity guarantees, or host isolation must be recorded in `docs/SACRIFICES.md`.

## 70. No complexity without deletion pressure

Every proposal that adds a component, process, schema, protocol, service, durable state, privilege, or abstraction MUST answer:

1. Which owner-visible capability does it add?
2. Why cannot Linux, OpenSSH, systemd, the VMM, or another mature standard provide it?
3. What existing complexity does it delete?
4. What happens when disabled?
5. How is it certified end to end?

A weak answer prohibits baseline inclusion.

## 71. No competing mutation race

Two create, start, stop, rename, snapshot, restore, fork, import, update, backup, or delete attempts must not both believe they own the same mutation. Timestamp order, PID presence, or last-writer-wins metadata is not sufficient authority.

## 72. No success after interruption or exhaustion

ENOSPC, OOM, SIGKILL, host loss, partial copy, failed synchronization, failed rename, or incomplete cleanup must never be normalized into success. The product must not destroy the previous committed state merely to make an interrupted operation appear clean.

## 73. No snapshot-as-backup theater

A local snapshot or reflink is not called a backup without independent storage authority, a manifest, integrity verification, identity semantics, and a proven restore.

## 74. No updater daemon or silent tuple mutation

Z must not poll for updates, install in the background, change a machine format silently, rewrite a dependency identity in place, or require a hosted update service. Update planning, verification, application, rollback, and machine migration are explicit foreground operations.

## 75. No automatic support upload or telemetry collector

A diagnostic command must not become a resident collector, hidden metrics service, automatic crash uploader, or support backchannel. A bundle is local, declared, redacted, owner-visible, and shared only through a separate owner action.

## 76. No implementation tool in the product

Baby, the Z GitHub Authority application, CI systems, repository connectors, build workers, and implementation-only credentials must not be shipped as Z components or become runtime, identity, update, verification, or offline-operability dependencies. Implementation convenience cannot amend product architecture.
