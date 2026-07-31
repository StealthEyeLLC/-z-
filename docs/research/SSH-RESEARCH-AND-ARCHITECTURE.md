# Z SSH-Native Architecture Research and Upgrade Report

Status: **Canonical research synthesis for the SSH-native architecture**  
Date: **2026-07-31**  
Project: **Z / zssh (`StealthEyeLLC/zssh`)**

## 1. Executive decision

Z should fully commit to being an **SSH-native sovereign computer runtime**.

This does **not** mean inventing “Virtual SSH,” extending the SSH wire protocol, or hiding a proprietary guest agent behind familiar commands. It means making each Z machine a real, strongly identified OpenSSH host whose lifecycle is integrated with connection establishment.

The central product contract becomes:

> A Z machine is a persistent unrestricted Linux computer with a stable SSH identity, reachable without guest IP networking, and compatible with the ordinary SSH ecosystem.

The strongest implementation is:

```text
OpenSSH client
    |
    | ProxyCommand + ProxyUseFdpass=yes
    v
Z lifecycle connector
    - validates the Z host name
    - finds and verifies the machine
    - starts it if stopped
    - waits for the VMM transport
    - connects to the Cloud Hypervisor vsock mux
    - passes the connected descriptor to OpenSSH
    - exits
    |
    v
Cloud Hypervisor vsock mux -> AF_VSOCK -> systemd socket -> stock sshd -i
```

Once the descriptor is passed, Z is no longer in the SSH data path. OpenSSH owns encryption, authentication, channels, PTYs, SFTP, forwarding, signals, terminal resizing, host-key verification, and connection multiplexing.

This is a strict architectural upgrade because it adds lifecycle-aware connectivity while deleting the need for a long-running Z proxy or a custom transport protocol.

## 2. Starting law from the original sources

The original normative sources define Z as:

- A real persistent unrestricted root Linux computer.
- One direct user-facing executable.
- KVM and pinned Cloud Hypervisor.
- Persistent raw disk with reflink or sparse-copy cloning.
- OpenSSH over AF_VSOCK.
- Standard systemd guest facilities.
- No project guest agent or guest protocol.
- No permanent project controller, database, scheduler, or broker.
- Zero project-owned processes when all machines are stopped.
- Native operating-system primitives before product code.
- Exact argument boundaries and no implicit shell for argument-safe execution.
- Strict machine identity, pinned assets, host confinement, honest failure, and data-preserving recovery.

The SSH-native design preserves those rules. It strengthens them by making OpenSSH compatibility a first-class product surface and by moving Z out of the established connection after descriptor handoff.

## 3. External research findings

### 3.1 SSH is a complete connection substrate, not only a shell

The SSH Connection Protocol already defines:

- Interactive shell sessions.
- PTY requests and terminal dimensions.
- Window-change requests.
- Standard output and a distinct standard-error channel.
- Signals.
- Exit status and exit signal.
- Subsystems such as SFTP.
- TCP forwarding.
- Unix-socket forwarding in OpenSSH.
- TUN/TAP forwarding in OpenSSH.

The protocol’s `exec` request carries one command string, not an argument vector. Therefore native SSH command execution must not be represented as exact `argv[]` execution. Z must retain a separate exact, noninteractive systemd execution plane.

### 3.2 OpenSSH can remove the ProxyCommand from the data plane

OpenSSH supports `ProxyUseFdpass=yes`. Under this mode the `ProxyCommand` returns an already connected file descriptor to `ssh(1)` and exits instead of copying bytes for the lifetime of the connection.

This enables a particularly clean division:

- Z owns machine lifecycle and transport establishment.
- OpenSSH owns the entire authenticated SSH session.
- No Z process remains merely to relay bytes.

This is the preferred Linux baseline.

Not every SSH implementation consumes OpenSSH configuration with full `ProxyUseFdpass` support. Z must therefore expose two explicit profiles:

1. **Native profile:** `ProxyUseFdpass=yes`, dynamic read-only host-key lookup, no Z process in the data plane after handoff.
2. **Compatibility profile:** explicit per-machine inventory entries and a transparent stdio relay for clients that support `ProxyCommand` but cannot receive a passed descriptor.

The compatibility relay is connection-scoped, byte-transparent, does not parse SSH, and exits with the connection. Z MUST NOT claim that one SSH stanza works with every SSH library.

### 3.3 OpenSSH provides dynamic strict host-key lookup

`KnownHostsCommand` can output ordinary `known_hosts` records and may be called multiple times during one connection. It accepts tokens including the searched host, execution reason, host-key type, and presented key. A nonzero exit aborts the connection.

Z can therefore provide a read-only command that resolves a Z alias to its durable machine identity and outputs the exact prebound host key. This avoids:

- Trust-on-first-use.
- `ssh-keyscan` as a trust decision.
- Disabling host-key checking.
- Writing all machine aliases into the user’s main `known_hosts` file.
- Coupling trust to an IP address.

The command must be read-only and must never create a machine, rotate a key, repair state, or accept a changed key.

### 3.4 OpenSSH configuration tokens are unescaped shell input

OpenSSH warns that tokens expanded inside command-bearing directives are not shell-escaped. `ProxyCommand`, `KnownHostsCommand`, and `Match exec` can therefore become injection surfaces if arbitrary host names are allowed.

Z must use:

- A narrow ASCII machine-name grammar.
- A reserved SSH alias prefix.
- An absolute path to the Z executable.
- No `Match exec` design.
- Validation inside every helper even after SSH pattern matching.
- No interpolation of arbitrary machine metadata into a shell command.

Recommended machine-name grammar:

```text
[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?
```

Recommended SSH alias namespace:

```text
z-<machine-name>
```

A machine name is a user-visible alias. The machine UUID and host key remain identity.

### 3.5 SSH config export is a proven ecosystem pattern

Vagrant exposes `ssh-config` so users can invoke native OpenSSH directly. Coder explicitly states that its wrapper does not have full SSH parity and recommends generated SSH configuration for the full OpenSSH feature set. Coder also provides dry-run, configurable file targets, wildcard or per-host entries, and optional autostart behavior.

The lesson for Z is direct:

- Do not wrap every SSH capability.
- Provide native OpenSSH configuration.
- Make changes explicit and previewable.
- Keep `z` as the easiest shell path.
- Let advanced users and third-party tools consume real SSH.

### 3.6 systemd already exposes a remote native control plane over SSH

Many systemd tools support `--host=` and use SSH to reach the remote system manager. `systemd-stdio-bridge` provides a standard D-Bus-over-stdio bridge.

A correctly configured Z SSH alias can therefore become a native target for applicable tools such as:

```text
systemctl -H root@z-work status
loginctl -H root@z-work
hostnamectl -H root@z-work
busctl -H root@z-work
systemd-run -H root@z-work ...
```

Exact support must be certified for the selected host and guest systemd versions. Z should not reproduce these operations as product APIs.

### 3.7 systemd socket activation and `sshd -i` are the right guest design

Current OpenSSH supports inetd mode with `sshd -i`. systemd supports per-connection socket activation and can pass the accepted socket as standard input/output.

The guest image should contain a static, Z-owned configuration of standard components:

- A fixed AF_VSOCK socket unit, using an address such as `vsock::22`.
- `Accept=yes`.
- A per-connection service running stock `sshd -i`.
- Explicit host-key and authorized-key paths.
- No dependency on `systemd-ssh-generator` auto-detection.

This avoids known generator races and distribution-template interactions while retaining zero project guest binaries.

### 3.8 Cloud Hypervisor SMBIOS credentials delete the bootstrap disk

Cloud Hypervisor has supported SMBIOS OEM strings through its `--platform` configuration and API since v26. The feature was added primarily to communicate metadata to systemd inside guests. Current systemd imports SMBIOS Type 11 strings using the standard forms:

```text
io.systemd.credential:NAME=VALUE
io.systemd.credential.binary:NAME=BASE64
```

This creates a stronger zero-agent bootstrap than a separate identity disk.

The durable machine directory remains the sole authority for:

- The machine UUID.
- The SSH host private key.
- The corresponding host public key and fingerprint.
- The selected owner authorization public key or keys.

At each boot, Z starts the pinned Cloud Hypervisor process with a private machine-specific API socket, sends the complete VM configuration over that socket, and places system credentials in the platform OEM-string list. The Cloud Hypervisor command line contains no private host key or other reusable secret.

The guest's static socket-activated SSH service imports the credentials with `ImportCredential=` and launches stock `sshd -i` with explicit credential-file paths under `$CREDENTIALS_DIRECTORY`.

Recommended credential names:

```text
z.ssh.hostkey.ed25519
z.ssh.authorized_keys.root
vmm.notify_socket
```

The `vmm.notify_socket` credential may point to a host listener through AF_VSOCK so PID 1 can send boot progress and `READY=1`. This is useful boot evidence, but authenticated SSH remains the final readiness authority.

This design deletes:

- The identity block device.
- Identity-filesystem creation and repair.
- Mount ordering and label discovery.
- Identity-volume backup and snapshot semantics.
- A second guest-readable durable representation of machine identity.

Security boundaries remain honest:

- Guest root can read the host key used by its own SSH daemon. This is expected because guest root controls the guest.
- The VMM necessarily receives the credential material for the boot and therefore must remain tightly confined.
- The private local VMM API socket and process memory become part of the host-side secret boundary.
- SMBIOS credentials are not a confidential-computing channel and MUST NOT be used to claim protection from a malicious hypervisor.

A small read-only standard credential medium remains a supported fallback only if the exact certified Cloud Hypervisor, firmware, kernel, systemd, or distribution tuple cannot import the required SMBIOS credentials. It is not baseline authority.

### 3.9 OpenSSH forwarding creates capability portals

SSH forwarding can expose narrowly selected services without attaching a guest NIC.

Examples:

```text
# Host reaches a guest web service
ssh -N -L 127.0.0.1:8080:127.0.0.1:80 z-work

# Host exposes a local Unix socket backed by a guest Unix socket
ssh -N -L /run/user/1000/z/work/db.sock:/run/postgresql/.s.PGSQL.5432 z-work

# Guest receives access to one exact host service
ssh -N -R 127.0.0.1:9000:127.0.0.1:9000 z-work

# Host receives a SOCKS endpoint whose network perspective is the guest
ssh -N -D 127.0.0.1:1080 z-work
```

This creates a powerful sealed-computer mode:

- No virtio-net device.
- No DHCP.
- No IP route between guest and host.
- Full shell and SFTP.
- Explicit service channels only.

These are **capability portals**, not a claim of total containment. Guest root can control services within the guest, and forwarded access has exactly the authority selected by the owner.

### 3.10 OpenSSH supports TUN/TAP forwarding

OpenSSH can request point-to-point or Ethernet tunnel devices. This provides an advanced network option carried over the same authenticated vsock SSH connection.

It should remain an explicit privileged variant because it may require:

- Host `CAP_NET_ADMIN` or root.
- `PermitTunnel` in the guest.
- Exact interface ownership and cleanup.
- Routing or bridge configuration.
- Performance and MTU certification.

It is valuable because it can provide an IP or layer-2 path without a Cloud Hypervisor virtio-net backend, but it is not the baseline network.

### 3.11 SFTP is sufficient for robust file transfer

OpenSSH SFTP supports:

- Recursive transfer without following symlinks.
- Resume with documented caveats.
- `fsync@openssh.com` for flushing completed uploads.
- Remote rename.
- `copy-data` for server-side copies when available.

Z can implement reliable copy through standard SFTP:

1. Upload to a unique temporary path in the destination directory.
2. Request flush when supported.
3. Apply requested metadata.
4. Rename atomically inside the guest filesystem.
5. Report failure if finalization is incomplete.

No custom file-transfer protocol is needed.

### 3.12 SSHFS is useful but not baseline

SSHFS mounts an SFTP filesystem through FUSE and even documents direct vsock support. It remains useful for optional host access to the guest filesystem, but it has limited active development and interrupted connections may block filesystem operations until timeout or reconnect.

Z may support SSHFS as an optional external composition or supervised variant. It must not replace SFTP, raw-disk recovery, or explicit host sharing.

### 3.13 Current OpenSSH should be treated as a compatibility tuple

OpenSSH 10.4/10.4p1 was released on July 6, 2026. Current OpenSSH defaults include post-quantum hybrid key exchange. Recent releases also changed Linux server packaging and process separation.

Z should not hard-code a stale algorithm list merely to appear secure. Instead it should:

- Pin and certify exact host and guest OpenSSH packages.
- Retain current secure defaults.
- Explicitly disable legacy authentication paths not required by Z.
- Test socket activation against the distribution’s complete OpenSSH package layout.
- Record client/server version compatibility.

## 4. Final architecture

## 4.1 Four planes, one computer

Z should define four complementary planes.

### Plane A: interactive SSH

Used for:

- Bare root shell.
- PTY applications.
- Terminal resizing.
- Interactive signals.
- IDEs.
- Ordinary remote shell semantics.

Commands:

```text
z
z work
ssh z-work
```

### Plane B: exact systemd execution

Used for:

- Exact executable and argument boundaries.
- No implicit shell.
- Explicit working directory and environment.
- Exact exit/signal result.
- Guest-native detached durability.

Because remote systemd cannot directly receive the caller’s PTY or file descriptors, noninteractive standard streams use guest files transferred through SFTP. This plane must report unknown when completion or output retrieval cannot be proven.

### Plane C: SFTP data plane

Used for:

- File copy.
- Atomic upload.
- Directory transfer.
- Recovery material.
- Server-side copies where supported.

### Plane D: SSH capability portals

Used for:

- Local TCP forwarding.
- Local Unix-socket forwarding.
- Remote forwarding of selected host services.
- SOCKS forwarding.
- Optional TUN/TAP.

No plane invents a project guest protocol.

## 4.2 Lifecycle-aware FD-pass connection

The `z ssh-fdpass` helper must:

1. Receive only a validated reserved alias and expected SSH port.
2. Resolve the alias to one existing machine.
3. Acquire a short-lived mutation/start lock.
4. Inspect host systemd and VMM evidence.
5. Start the exact transient machine unit if stopped.
6. Wait for the exact machine-bound vsock mux socket.
7. Verify socket ownership, inode, runtime root, VMM start identity, executable digest, API socket, and machine binding.
8. Connect to the requested guest vsock port through the mux.
9. Pass the connected descriptor to OpenSSH using `SCM_RIGHTS`.
10. Exit immediately.

It must not:

- Relay SSH bytes after successful descriptor transfer.
- Accept arbitrary Unix socket paths.
- Create a missing machine from a read-only third-party probe.
- Repair or rotate credentials implicitly.
- Accept unverified stale runtime files.
- Become a readiness oracle separate from the SSH handshake.

The successful authenticated SSH handshake is the final readiness proof.

## 4.3 SSH namespace

Baseline alias:

```text
z-<machine-name>
```

Rules:

- Only the strict machine-name grammar is accepted.
- Names are unique within the owner’s Z root.
- Aliases are mutable labels.
- Machine UUID and SSH host key are identity.
- Rename does not rotate identity.
- Fork rotates identity.
- Restore preserves identity.
- Import requires explicit trust adoption.

Direct third-party SSH should start an existing machine but should not silently create a missing machine. Creation remains explicit through `z <name>` or `z create <name>`. This prevents IDE discovery, `ssh -G`, config inspection, or a typo from allocating a new computer.

An explicit future autocreate variant may be offered only if its mutation behavior is unmistakable.

## 4.4 Native SSH configuration

Z should generate a dedicated include file and ask the owner to include it explicitly.

Illustrative profile:

```sshconfig
Host z-*
    User root
    CanonicalizeHostname no
    CheckHostIP no

    ProxyCommand /absolute/path/to/z ssh-fdpass --host %h --port %p
    ProxyUseFdpass yes

    UserKnownHostsFile /dev/null
    GlobalKnownHostsFile /dev/null
    KnownHostsCommand /absolute/path/to/z ssh-known-hosts --host %H --reason %I --key-type %t
    StrictHostKeyChecking yes

    IdentityFile ~/.local/share/z/identity/owner_ed25519
    IdentitiesOnly yes
    IdentityAgent none
    AddKeysToAgent no

    PasswordAuthentication no
    KbdInteractiveAuthentication no
    GSSAPIAuthentication no
    HostbasedAuthentication no

    ForwardAgent no
    ForwardX11 no
    PermitLocalCommand no
    ControlMaster no
    Compression no

    RequestTTY auto
    ServerAliveInterval 15
    ServerAliveCountMax 3
```

The exact generated profile must be validated using `ssh -G` against the certified OpenSSH client.

Commands:

```text
z ssh-config print
z ssh-config diff
z ssh-config install
z ssh-config remove
z ssh-config verify
```

Only `install` and `remove` may mutate. They must be atomic, marker-bounded, idempotent, and previewable.

## 4.5 Hermetic internal SSH client

Z’s own operations must not inherit arbitrary user SSH behavior.

Internal invocations should use a dedicated configuration or `/dev/null` configuration plus explicit options including:

- Strict machine-bound host verification.
- Exact identity file.
- `IdentitiesOnly=yes`.
- `IdentityAgent=none`.
- `BatchMode=yes`.
- `ClearAllForwardings=yes`.
- `ForwardAgent=no`.
- `ForwardX11=no`.
- `PermitLocalCommand=no`.
- No `ProxyJump` or user `ProxyCommand`.
- No user `RemoteCommand`.
- No user environment forwarding.
- Bounded connection and server-alive behavior.

This keeps the ecosystem surface open while making product control deterministic.

## 4.6 Guest SSH contract

The certified image should use:

- A static AF_VSOCK socket unit.
- A per-connection `sshd -i` service.
- Root public-key login only.
- Password and keyboard-interactive authentication disabled.
- No reusable key in the base image.
- Host key and owner public key supplied from machine-specific standard artifacts.
- SFTP enabled.
- TCP and Unix-socket forwarding enabled because the owner already has unrestricted root.
- Agent and X11 forwarding available only by explicit client choice; disabled in Z defaults.
- TUN/TAP disabled unless its variant is selected.
- No Z binary or Z service in the guest.

Disabling forwarding on the server is not a meaningful restriction against an unrestricted root owner. Security comes from the host boundary and from which local SSH channels the owner opens.

## 4.7 Identity lifecycle

### Create

- Generate machine UUID.
- Generate unique host key.
- Generate or select the owner authentication public key.
- Build the machine identity artifact.
- Store the public host key and fingerprint as derived host evidence.
- Never connect before strict host identity is available.

### Restart

- Preserve machine UUID and host key.

### Snapshot restore

- Preserve identity because it is the same computer.

### Fork

- Clone disks while stopped.
- Generate a new machine UUID, SSH host key, vsock CID, MAC addresses, SMBIOS UUID, disk serials, and all other collision-prone identity.
- Boot without external networking until identity regeneration and validation complete.

### Rename

- Change alias only.
- Preserve machine UUID and host key.

### Host-key rotation

Rotation must be explicit and continuity-proven:

1. Add the new key while connected through the old trusted key.
2. Verify both keys through the authenticated old channel.
3. Update Z’s trust material atomically.
4. Reconnect and verify the new key.
5. Remove the old key only after success.

A changed key with no proved rotation is an identity failure, not a prompt to accept automatically.

## 4.8 Capability portals

Z may offer thin convenience commands that print and invoke their native SSH equivalent.

Examples:

```text
z portal local work 127.0.0.1:8080 127.0.0.1:80
z portal unix work /run/user/1000/z/work/db.sock /run/postgresql/.s.PGSQL.5432
z portal provide work 127.0.0.1:9000 127.0.0.1:9000
z portal socks work 127.0.0.1:1080
```

Rules:

- Foreground by default.
- `SessionType=none` / `ssh -N`.
- `ExitOnForwardFailure=yes`.
- Loopback or owner-only Unix socket by default.
- External bind requires an explicit address.
- Unix sockets reside under a private runtime directory with restrictive mode.
- No durable portal registry.
- A durable portal is a standard host systemd transient service containing the exact SSH invocation.
- A durable portal stops with its machine unless explicitly declared independent.
- Z does not claim a portal destination is healthy merely because the listener was created.

## 4.9 Optional multiplexed SSH fabric

`ControlMaster` can reduce latency for repeated sessions, but it creates a live SSH process and a control socket. It must not be baseline.

An optional multiplexed variant may:

- Store its control socket under a private machine runtime directory.
- Include `%C` or the complete machine/user identity in the path.
- Use a bounded `ControlPersist` interval.
- Close the master on machine stop, fork, import, host-key rotation, or identity failure.
- Never treat the master as proof that the VMM or guest is currently correct.
- Never reuse a master across identity change.

## 5. Strict upgrades synthesized from the constraints

### Upgrade 1: Descriptor handoff instead of proxying

Adds lifecycle-aware SSH while deleting the long-lived proxy process.

### Upgrade 2: Read-only dynamic host identity

`KnownHostsCommand` exposes durable Z identity to native OpenSSH without trust-on-first-use or global known-host mutation.

### Upgrade 3: Dual SSH personalities

- Native owner profile for full ecosystem power.
- Hermetic Z profile for deterministic product operations.

This prevents user configuration from corrupting lifecycle semantics without limiting owner power.

### Upgrade 4: SMBIOS-to-systemd credentials

Cloud Hypervisor OEM strings submitted through the private VMM API inject standard systemd credentials without a guest agent, reusable image key, secret-bearing command line, or extra block device. A read-only credential medium remains fallback-only.

### Upgrade 5: Capability portals in Network None

A machine can have no NIC yet remain useful for shells, IDEs, files, databases, web services, and exact selected host services.

### Upgrade 6: Native systemd tools as Z’s management API

Where systemd supports remote SSH operation, users can invoke Linux’s own control tools directly instead of Z wrappers.

### Upgrade 7: Explicit identity semantics across lifecycle

Restore, fork, rename, import, and rotation receive exact SSH identity rules, eliminating a common VM trust ambiguity.

### Upgrade 8: Native ecosystem certification

Z should certify not only its own CLI but also:

- `ssh`.
- `scp`.
- `sftp`.
- `rsync` over SSH.
- Git over SSH where applicable.
- VS Code Remote SSH.
- JetBrains Remote Development.
- Selected systemd `--host` tools.
- SSH TCP and Unix-socket forwarding.
- Optional SSHFS.

Z earns compatibility by remaining ordinary SSH.

## 6. Rejected ideas

The following were considered and rejected for the baseline:

- A custom exact-argv SSH subsystem.
- A guest launcher merely to combine exact argv and PTY.
- A project-specific SSH framing layer.
- A permanent SSH proxy daemon.
- A machine certificate authority for single-owner local use.
- Trust-on-first-use.
- `StrictHostKeyChecking=no` or `accept-new` as baseline.
- `ssh-keyscan` as trust establishment.
- Automatic agent forwarding.
- Automatic X11 forwarding.
- A durable host-side tunnel database.
- Silent machine creation from `ssh`, IDE discovery, or config evaluation.
- An SSH multiplex master as lifecycle authority.
- Treating SSH forwarding as complete network isolation.
- Making SSHFS the durable filesystem or recovery authority.

## 7. Implementation gates

### Gate S0: exact SSH semantics

Prove with the certified OpenSSH client/server tuple:

- FD passing works and Z exits after handoff.
- PTY, resize, signals, stdout, stderr, exit status, and SFTP are native OpenSSH behavior.
- Native SSH remote command remains documented as shell-string semantics.
- Exact systemd execution remains separate.

### Gate S1: machine identity before first connection

Prove:

- Unique host key before first SSH handshake.
- Strict verification without prompt or TOFU.
- Wrong-machine connection rejection.
- Alias rename preserves identity.
- Fork rotates identity.
- Restore preserves identity.
- Unproved key change hard-fails.

### Gate S2: static vsock SSH server

Prove:

- Static socket activation works on every boot.
- No dependency on `systemd-ssh-generator`.
- Complete OpenSSH package process layout is present.
- Multiple concurrent connections work.
- Reboot and full VMM stop/start work.

### Gate S3: ecosystem compatibility

Prove native operation through the generated SSH profile for:

- OpenSSH shell.
- SFTP.
- SCP.
- rsync.
- VS Code Remote SSH.
- JetBrains Remote Development.
- At least the selected systemd remote tools.
- TCP and Unix-socket portals.

### Gate S4: hermetic internal control

Prove hostile user SSH config cannot alter Z’s internal:

- Host-key policy.
- Identity selection.
- Proxy path.
- Remote command.
- Forwarding.
- Agent use.
- Local command execution.
- Environment forwarding.

### Gate S5: lifecycle and recovery

Prove:

- Direct SSH starts a stopped existing machine.
- Client death does not stop the computer.
- VMM death terminates or fails connections honestly.
- Reboot reconnect behavior is correct.
- Serial remains independent recovery.
- No Z relay process remains during established SSH.
- All project processes disappear when all machines stop.

### Gate S6: portal containment

Prove:

- Default local bind is loopback or owner-only Unix socket.
- External exposure requires explicit selection.
- Failed forward setup fails the command.
- Stale Unix socket behavior is exact.
- Remote forwarding exposes only the selected host endpoint.
- Network None still has no virtual NIC.
- Portal teardown leaves no listeners or sockets.

### Gate S7: negative SSH certification

Attempt:

- Shell injection through machine names and SSH tokens.
- Wrong alias to machine mapping.
- Stale vsock mux socket adoption.
- Changed host key.
- Ambient ssh-agent use.
- Ambient user `ProxyCommand`, `LocalCommand`, `RemoteCommand`, and forwards.
- ControlMaster reuse across identity rotation.
- External wildcard bind without explicit authority.
- SFTP partial-copy false success.
- SSHFS disconnect and stale mount behavior.
- Generator/package upgrade regression.

## 8. Product result

With these upgrades, Z is not merely a VM launcher with SSH inside it.

It becomes:

> **A lifecycle-aware namespace of sovereign Linux computers that are native OpenSSH resources.**

The owner gets:

- A real persistent computer.
- Unrestricted root.
- A stable machine identity.
- No IP dependency for control.
- No guest agent.
- No custom protocol.
- No permanent controller.
- No data-plane Z process after FD handoff.
- Native shells, IDEs, SFTP, rsync, Git, systemd tools, and service forwarding.
- A sealed no-NIC profile that still supports explicit service capability channels.
- Ordinary files and disks as durable truth.
- Full-power network and device variants when selected.

The system is more powerful because Z owns less.

## 9. Primary research sources

- Original Z `INVARIANTS.md`, `ANTI-INVARIANTS.md`, and `VARIANTS.md` supplied by the owner.
- RFC 4254, SSH Connection Protocol: https://www.rfc-editor.org/rfc/rfc4254.html
- OpenSSH current manuals: https://man.openbsd.org/ssh_config and https://man.openbsd.org/sshd
- OpenSSH release notes: https://www.openssh.com/releasenotes.html
- systemd SSH proxy: https://www.freedesktop.org/software/systemd/man/latest/systemd-ssh-proxy.html
- systemd socket units: https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html
- systemd credentials: https://systemd.io/CREDENTIALS/
- systemd stdio bridge: https://www.freedesktop.org/software/systemd/man/latest/systemd-stdio-bridge.html
- Cloud Hypervisor repository and release notes: https://github.com/cloud-hypervisor/cloud-hypervisor
- Coder SSH configuration documentation: https://coder.com/docs/reference/cli/config-ssh
- Vagrant SSH config documentation: https://developer.hashicorp.com/vagrant/docs/cli/ssh_config
- Lima `show-ssh` implementation: https://github.com/lima-vm/lima/blob/master/cmd/limactl/show-ssh.go
- SSHFS repository and manual: https://github.com/libfuse/sshfs and https://man7.org/linux/man-pages/man1/sshfs.1.html
