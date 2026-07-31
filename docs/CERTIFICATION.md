# Certification — SSH-Native Z

Status: **Normative certification plan**  
Date: **2026-07-31**

## 1. Certification rule

A release is not SSH-native because it contains an SSH client, launches `sshd`, or can open one shell.

Certification requires end-to-end proof that a real KVM computer has unique prebound identity, can be reached through stock OpenSSH over AF_VSOCK, preserves ordinary SSH semantics, supports a separate exact execution plane, survives lifecycle failure, and leaves no Z process or authority behind when stopped.

Mocks, protocol simulators, fake guests, and loopback-only tests cannot satisfy release certification.

## 2. Evidence format

Every certification run MUST record:

- Z source commit and tree.
- Z binary digest.
- Host distribution and package snapshot.
- Host kernel version and required security features.
- Host systemd version.
- Host OpenSSH version.
- Cloud Hypervisor version, commit, feature set, and digest.
- Firmware version and digest.
- Guest image build identity and digest.
- Guest kernel version.
- Guest systemd version.
- Guest OpenSSH version and complete package layout.
- Network helper version and digest where used.
- Host filesystem type and reflink behavior.
- CPU vendor, model, and exposed feature profile.
- Test start and end time.
- Exact commands, exits, relevant logs, and retained evidence paths.

A claim is scoped to that tuple unless wider compatibility is separately proven.

## 3. Gate A — host prerequisites

Prove:

- `/dev/kvm` is available and usable by the selected identity.
- Required host kernel floor is satisfied.
- Required seccomp behavior is available.
- Required Landlock ABI and every relied-upon access right are available.
- Pre-sandbox file descriptors are inventoried and no undeclared descriptor retains ambient host authority.
- The exact host-kernel build includes applicable KVM isolation fixes, including CVE-2026-53359 on x86.
- The pinned Cloud Hypervisor x86 equivalent of `nested=off` is explicit and nested virtualization is absent from the effective baseline guest CPU exposure.
- Unix descriptor passing works.
- Host systemd user or system manager can own transient services as designed.
- User lingering behavior is explicitly configured and verified if user services must survive logout.
- Machine and runtime roots have exact owner and mode.
- Reflink capability is detected honestly.
- Sparse-copy fallback preserves disk content and allocated-size expectations.

Negative tests:

- KVM absent.
- Landlock unavailable.
- Wrong machine-root owner.
- Runtime root writable by another user.
- Required executable digest mismatch.
- Insufficient disk space.
- Unsupported host filesystem behavior.

Expected result: fail closed before machine mutation where possible.

## 4. Gate B — materialization, identity, and credential bootstrap

Prove before first authenticated connection:

- Machine UUID is unique.
- Machine name passes strict grammar.
- SSH host key is unique and generated before first connection.
- Owner authentication public key is exact.
- Private host-key authority exists in exactly one durable machine-directory path.
- Public host-key evidence matches the private key.
- Machine configuration refers to exact immutable assets.
- Disk is a complete independent raw image with no hidden mutable backing chain.
- Metadata writes are crash-safe.
- Cloud Hypervisor receives the complete VM configuration through the exact private API socket.
- Reusable secret material is absent from process arguments, environment dumps, public logs, and unit descriptions.
- SMBIOS Type 11 OEM-string count and encoded table size are preflighted before launch; overflow, truncation, count wrap, or over-limit data fail before machine mutation.
- SMBIOS Type 11 binary credentials preserve the exact host key and authorized-keys bytes.
- Cloud Hypervisor v52.0/v53.0 does not configure or depend on `vmm.notify_socket`; any future notification tuple proves the required datagram or sequenced-packet transport separately.

Negative tests:

- Reused image host key.
- Corrupt host key.
- Mismatched public host key.
- Duplicate UUID.
- Invalid alias containing shell characters, slash, whitespace, control byte, Unicode confusable, or traversal.
- Missing or malformed SMBIOS credential.
- Truncated Base64 credential.
- Wrong machine API socket.
- API socket symlink or replacement race.
- Secret included in Cloud Hypervisor argv.
- Interrupted metadata rename.

Expected result: fail closed without trusting or silently regenerating an unknown identity.

## 5. Gate C — host systemd machine ownership

Prove:

- One transient service directly owns Cloud Hypervisor.
- Exact executable and launch arguments are visible.
- The unit is bound to one machine directory and runtime root.
- VMM process cgroup membership is exact.
- Selected helper units have explicit dependencies.
- CLI exit does not terminate the machine.
- Host logout does not terminate the machine under the supported configuration.
- Guest poweroff causes the expected VMM and unit transition.
- Hard-stop escalation is bounded and reported.
- Machine stop leaves no VMM or helper.

Negative tests:

- Stale unit with no VMM.
- Wrong executable under expected PID.
- PID reuse.
- Wrong API socket.
- VMM with a different disk.
- Helper started outside the machine slice.
- Unit restart loops after deterministic configuration failure.

## 6. Gate D — static AF_VSOCK SSH server and service credentials

Prove:

- The guest contains static socket and service units.
- The socket binds the expected AF_VSOCK port without runtime CID discovery.
- `Accept=yes` creates one standard service instance per connection.
- The service runs stock `sshd -i`.
- Required OpenSSH server helper binaries for the selected distribution are present.
- `ImportCredential=` imports the exact host-key and authorized-keys credentials.
- `sshd` receives explicit credential-file paths.
- Credential files are immutable for the service lifetime and inaccessible to unrelated unprivileged services as certified.
- Password, keyboard-interactive, GSSAPI, hostbased authentication, agent forwarding, X11 forwarding, and user environment behavior match the declared profile.
- SFTP is enabled.
- Multiple concurrent connections work.
- No `systemd-ssh-generator` output is required.

Negative tests:

- Missing host-key credential.
- Missing authorized-keys credential.
- Wrong credential name.
- Malformed private key.
- Unauthorized public key.
- Generator disabled entirely.
- Early-boot connection race.
- Repeated failed authentication.
- Concurrent connection flood within declared bounds.
- Attempt to read service credentials from an unrelated service.

## 7. Gate E — descriptor-pass lifecycle connector

Prove:

- `ProxyUseFdpass=yes` is effective in `ssh -G` output.
- Z resolves only `z-<valid-name>`.
- Existing stopped machine starts.
- Existing running machine is adopted only after exact verification.
- Vsock mux socket is validated against owner, inode, runtime root, VMM process start identity, API socket, and machine binding.
- Z connects the requested guest port.
- Z passes the connected file descriptor through the expected Unix descriptor-passing mechanism.
- Z exits immediately after successful handoff.
- The SSH session remains functional after Z exits.
- No Z relay process exists in the connection data path.

Negative tests:

- Nonexistent machine.
- Invalid alias.
- Arbitrary port outside the allowed SSH connector policy.
- Stale mux socket.
- Socket symlink.
- Socket replacement race.
- Mux socket owned by wrong process.
- VMM executable digest mismatch.
- VMM API reports different machine.
- Descriptor-transfer failure.
- Client cancellation during startup.

## 7.1 Gate E2 — compatibility inventory and stdio relay

Prove with at least one certified embedded SSH client that lacks descriptor passing:

- Explicit per-machine entries are discoverable by the client.
- The generated host-key inventory binds the exact machine key.
- The stdio relay is byte-transparent for handshake, PTY, SFTP, and forwarding.
- Relay cancellation and half-close behavior are correct.
- The relay exits when the connection exits.
- No durable connection record or background relay remains.
- Native OpenSSH continues to use descriptor handoff rather than the compatibility relay.

Negative tests:

- Stale generated inventory.
- Changed host key.
- Relay crash during handshake.
- Client disconnect during large SFTP transfer.
- Attempt to use the compatibility profile as a trust bypass.

## 8. Gate F — strict host verification

Prove:

- `KnownHostsCommand` is read-only.
- It returns the exact machine public host key.
- It handles ORDER, HOSTNAME, and applicable request reasons correctly.
- It may be called repeatedly without mutation.
- `StrictHostKeyChecking=yes` is effective.
- User and global known-host files do not override machine identity.
- Host verification succeeds on the correct machine.
- Wrong machine key fails.
- Changed key fails.
- Missing key fails.
- Corrupt helper output fails.
- Helper nonzero exit aborts the connection.

Lifecycle identity tests:

- Restart preserves key.
- Stop/start preserves key.
- Rename preserves key.
- Same-computer snapshot restore preserves key.
- Fork produces a different key.
- Import-as-new produces a different key.
- Explicit rotation proves continuity and retires old key only after new-key verification.

## 9. Gate G — owner authentication

Prove:

- Only the intended Z owner key is offered by the baseline profile.
- `IdentitiesOnly=yes` is effective.
- `IdentityAgent=none` is effective.
- A busy ambient ssh-agent cannot alter authentication.
- Password and keyboard-interactive fallback do not occur.
- Wrong owner key fails.
- Removed owner key fails.
- Owner public-key update is explicit and recoverable.

Per-machine and hardware-backed variants require separate evidence.

## 10. Gate H — native SSH behavior

Using the native OpenSSH client, prove:

- Interactive root shell.
- PTY allocation.
- Initial terminal dimensions.
- Resize propagation.
- Ctrl-C and other interactive signal behavior.
- Full-screen terminal program behavior.
- Binary-clean non-PTY streams where applicable.
- stdout and stderr behavior.
- Normal exit status.
- Signal exit behavior.
- Server-alive failure detection.
- Client disconnect does not stop guest services or the machine.
- Reconnect after disconnect.

Document that native SSH remote commands use command-string and shell semantics.

## 11. Gate I — hermetic Z internal SSH

Construct a hostile owner `~/.ssh/config` containing:

- Alternate `ProxyCommand`.
- `ProxyJump`.
- `LocalCommand` with side effect.
- `RemoteCommand`.
- `Match exec`.
- Local, remote, and dynamic forwards.
- Agent forwarding.
- X11 forwarding.
- Alternate identity files.
- Relaxed host-key verification.
- Environment forwarding.
- ControlMaster.

Then prove Z internal operations:

- Ignore or override every hostile directive.
- Use the exact Z transport and identity.
- Create no undeclared listener.
- Execute no local side effect.
- Forward no agent, X11, or environment.
- Remain deterministic.

Native owner `ssh z-name` may honor owner-selected options because it is an owner surface, but Z-generated security-critical defaults must remain effective unless the owner explicitly overrides them on that native interface.

## 12. Gate J — SFTP and copy correctness

Prove:

- Small text transfer.
- Large binary transfer.
- Zero-length file.
- File names with spaces and non-shell-special safe filesystem bytes.
- Recursive directory transfer.
- Symlinks handled according to declared policy.
- Permissions and timestamps where requested.
- Upload to unique temporary destination.
- Flush using `fsync@openssh.com` where supported.
- Atomic rename into final path.
- No false success if flush or rename fails.
- Interrupted transfer leaves only exact temporary artifact.
- Retry does not corrupt an unrelated destination.
- Download integrity verification.
- Remote `copy-data` use only when capability is negotiated.

Negative tests:

- Disk full.
- Permission denied.
- Destination replaced by symlink.
- Parent directory renamed during finalization.
- Client disconnect.
- Guest reboot during transfer.
- Partial local write.

## 13. Gate K — exact systemd execution

Prove:

- Exact executable path.
- Exact empty argument.
- Arguments containing spaces, quotes, dollar signs, glob characters, newlines, and non-ASCII bytes where the interface permits them.
- No shell expansion.
- Explicit working directory.
- Explicit environment, including empty value and removal policy.
- Binary stdin file.
- Separate binary stdout and stderr files.
- Exit code 0.
- Nonzero exit code.
- Terminating signal.
- Timeout and explicit cancellation.
- Detached guest-native unit.
- Guest reboot behavior according to selected unit properties.
- Unit properties queried for final outcome.
- Final output retrieved before temporary cleanup.

Negative tests:

- Remote systemd unavailable.
- SFTP upload incomplete.
- Unit accepted but connection lost.
- Unit vanished before result query.
- Output retrieval incomplete.
- Cleanup failure.

Expected result: unknown or recoverable state, never fabricated success.

## 14. Gate L — native systemd remote tools

For each claimed tool, prove through `root@z-name`:

- Connection uses the generated OpenSSH alias.
- Host verification remains strict.
- Operation reaches the intended guest manager.
- Exit status is honest.
- Unsupported remote options are rejected and not hidden by Z.

Candidate tools include `systemctl`, `loginctl`, `hostnamectl`, `busctl`, and `systemd-run`. Certification must list exact supported commands rather than claiming universal `-H` support.

## 15. Gate M — local TCP portal

Prove:

- Default bind is `127.0.0.1` and applicable IPv6 loopback behavior is explicit.
- `ExitOnForwardFailure=yes` fails on collision.
- Guest service is reachable through the portal.
- A failed destination is not reported healthy.
- Machine stop terminates the foreground or durable portal as declared.
- External bind requires explicit address.
- Cleanup leaves no listener.

Negative tests:

- Host port occupied.
- Guest service absent.
- Guest service starts later.
- Guest reboot.
- SSH disconnect.
- Attempted wildcard bind through a safe-default wrapper.

## 16. Gate N — Unix-socket portal

Prove:

- Socket is below private runtime root.
- Parent mode is restrictive.
- Socket umask is restrictive.
- Existing unrelated socket is not removed.
- Exact owned stale socket may be removed only after verification.
- Guest Unix destination works.
- Guest TCP destination through host Unix socket works if supported.
- Cleanup removes only owned socket.

Negative tests:

- Symlink socket path.
- Parent traversal.
- Socket owned by another process.
- Runtime directory writable by another user.

## 17. Gate O — reverse exact host-service portal

Prove:

- Guest receives only the selected host endpoint.
- Guest listener is loopback or exact Unix path by default.
- No host-home or agent socket is exposed implicitly.
- Network None remains without a NIC.
- Portal teardown removes guest listener.
- Host endpoint disappearance is reported through actual connection failures, not false portal teardown.

## 18. Gate P — Network None

Prove inside and outside the guest:

- No virtio-net device.
- No other undeclared NIC.
- No IPv4 or IPv6 external traffic.
- No DHCP.
- No host bridge membership.
- No `passt` process.
- SSH shell over AF_VSOCK works.
- SFTP works.
- Exact systemd execution works.
- Selected portals work.

Guest root attempts to create or enable an undeclared virtual interface must not obtain host connectivity.

## 19. Gate Q — `passt` connected profile

Prove:

- Outbound TCP, UDP, DNS, IPv4, and IPv6 as claimed.
- Host-loopback, gateway, and guest-address convenience mappings are disabled with the exact pinned-version options.
- Guest attempts through those convenience aliases fail to reach host services.
- The exact pinned-version equivalents of `--tcp-ports none` and `--udp-ports none` are active; no inbound listeners exist without explicit publication.
- The stricter `pivot_root()` sandbox succeeds and no `--chroot-fallback` equivalent is active.
- Direct connection attempts to every real host address and relevant wildcard-bound host service are tested and recorded. Reachability is treated as residual connected-profile authority, not false isolation.
- The Network None profile proves absence of any general IP path to host services.
- Explicit host-port publication.
- Collision failure.
- Correct cleanup.
- No global firewall or routing mutation in ordinary mode.

Document that this is not hostile-code network containment.

## 20. Gate R — serial recovery

Prove:

- Serial is available when SSH is broken.
- Client automatically reconnects across Cloud Hypervisor serial socket recreation where supported by the chosen design.
- Buffered serial output is consumed without duplication beyond declared limits.
- Early boot logs are retained as far as the VMM supports.
- Serial access does not depend on guest IP or SSH.
- A broken guest sshd can be repaired manually from serial.

## 21. Gate S — snapshot, restore, and fork identity

Cold snapshot:

- Guest gracefully powers off.
- VMM exits.
- Disks and identity artifacts are copied or reflinked.
- Source remains unchanged.
- Restore boots with the same machine identity and host key.

Fork:

- Source is stopped or otherwise captured through a certified path.
- New machine UUID.
- New SSH host key.
- New vsock identity.
- New MAC addresses.
- New guest machine ID as applicable.
- New firmware/SMBIOS identity as applicable.
- No external network until new identity is complete.
- Source and fork cannot be mistaken for each other by SSH.

## 22. Gate T — optional ControlMaster

Prove:

- Control socket path is owner-private and identity-specific.
- Multiple SSH sessions reuse the connection.
- Agent and X11 state do not leak unexpectedly.
- Bounded idle expiration works.
- Machine stop closes master.
- Host-key rotation closes master before trust changes.
- Fork/import cannot reuse source master.
- Stale control socket is not lifecycle authority.

## 23. Gate U — optional SSHFS

Prove:

- Mount and unmount under owner identity.
- Read/write behavior as declared.
- Server-alive timeout.
- Reconnect behavior and in-flight data loss warning.
- Guest reboot.
- Machine stop.
- Stale mount cleanup.
- No claim that mount consistency equals snapshot consistency.

## 24. Gate V — SSH TUN/TAP

Point-to-point and Ethernet modes require separate certification covering:

- Exact host and guest device creation.
- Permissions and capabilities.
- MTU.
- Routes or bridge membership.
- Packet flow.
- Isolation.
- Machine reboot.
- SSH disconnect.
- Exact teardown.
- No unrelated host route, interface, or bridge mutation.

## 25. Gate W — VMM and vsock robustness

Exercise the exact pinned Cloud Hypervisor release with:

- Incomplete vsock mux header.
- Disconnect before port selection.
- Rapid connect/disconnect.
- Half-close.
- Client Ctrl-C during connection.
- Guest reboot during connection.
- VMM reboot behavior.
- Stale socket replacement.
- Multiple concurrent SSH connections.
- Serial plus SSH plus SFTP plus portal load.
- Non-stream vsock requests are handled exactly as documented by the pinned VMM; Cloud Hypervisor v52.0/v53.0 must not be treated as supporting systemd's datagram/sequenced-packet readiness channel.

No input sequence may panic the VMM or corrupt the disk.

## 26. Gate X — confinement

Prove the VMM and helpers cannot access undeclared owner files.

Attempt:

- Owner SSH keys.
- Browser profiles.
- Cloud credentials.
- Repository outside machine root.
- Parent and sibling machine directories.
- Symlink escape.
- Bind-mount escape.
- Renamed path race.
- Hard-link confusion where applicable.
- Access through every descriptor opened before Landlock restriction.
- Missing Landlock rights, older ABI behavior, and exhausted ruleset-layer capacity.

Certification must show fail-closed behavior when Landlock or required confinement cannot be installed.

## 27. Gate Y — zero at rest

After stopping every machine and optional component, prove absence of:

- Z processes.
- Cloud Hypervisor processes.
- `passt`.
- `virtiofsd`.
- OpenSSH ControlMaster processes.
- Portal SSH processes.
- SSHFS processes.
- Active FUSE mounts.
- Runtime sockets.
- Port listeners.
- TUN/TAP devices.
- Bridge membership.
- Temporary identity or transfer files outside declared recovery remnants.

Persistent machine directories, disks, metadata, snapshots, authoritative identity files, and explicit SSH include configuration are durable state, not background runtime.

## 27.1 Dependency and supply-chain gate

Release evidence MUST contain:

- Exact SHA-256 of `assets/dependencies.lock.json`.
- Proof that every selected upstream asset matches its locked size and digest.
- Valid signatures for the locked Debian `InRelease` metadata and matching package-index hashes.
- Complete reference-host package manifest used during certification.
- Complete guest `dpkg-query` manifest and proof that every package came from the locked snapshot.
- Exact `Cargo.lock`, Rust compiler verbose identity, target triple, enabled features, and final binary digest.
- Base-image recipe, package closure, partition/filesystem identities, and raw-image digest.
- License inventory, SBOM, and security-advisory review for the final source and binary closures.
- Positive absence evidence for live repositories, backports, testing/unstable packages, floating URLs, unverified assets, undeclared crates, and unrecorded guest packages.

Any mismatch creates a different candidate tuple and blocks release.

## 28. Release decision

A failure in identity, host verification, exact execution truth, confinement, data preservation, or cleanup is a release blocker.

A feature that has not passed its exact variant gate is unsupported even if it appears to work manually.

The release report MUST distinguish:

- Certified baseline.
- Certified variants.
- Experimental paths.
- External compositions.
- Known sacrifices.
- Open upstream blockers.
