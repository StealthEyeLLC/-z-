# Architecture — SSH-Native Z

Status: **Normative architecture**

## 1. Architectural thesis

Z turns a persistent local virtual computer into a native SSH resource.

```text
Human or tool
   |
   | OpenSSH configuration
   v
Z lifecycle connector
   |  verify/create/start/wait/connect
   |  pass connected fd, then exit
   v
Cloud Hypervisor vsock mux
   v
AF_VSOCK port 22
   v
systemd socket activation
   v
stock sshd -i
   v
ordinary unrestricted Linux
```

## 2. Four execution and transport planes

### 2.1 Interactive SSH plane

OpenSSH owns encryption, authentication, shell sessions, PTYs, resizing, signals, forwarding, multiplexing, and SFTP subsystem selection.

### 2.2 Exact execution plane

Z uses the same authenticated SSH transport to invoke the guest's standard systemd manager. The exact executable and argument vector are delivered as systemd D-Bus properties. Finite stdin and separate stdout/stderr use temporary guest files transferred through SFTP. Final truth comes from `Result`, `ExecMainCode`, and `ExecMainStatus` after all requested output is retrieved.

### 2.3 Data plane

SFTP is the baseline file-transfer mechanism. Durable destination replacement uses a same-directory temporary file, optional server flush, and atomic rename where certified.

### 2.4 Capability-portal plane

Standard SSH forwarding creates explicit, bounded channels:

- Host TCP or Unix listener to guest service.
- Guest listener to exact host service.
- Dynamic SOCKS.
- Optional TUN/TAP advanced networking.

No portal database exists. Foreground SSH owns ordinary portal lifetime; a durable portal is one exact transient host systemd service.

## 3. Machine durable layout

Illustrative layout:

```text
machines/<name>/
  machine.json
  disks/root.raw
  identity/machine.uuid
  identity/ssh_host_ed25519_key
  identity/ssh_host_ed25519_key.pub
  identity/known_hosts
  snapshots/
```

`machine.json` contains desired configuration only. It does not authoritatively claim running, ready, stopped, or broken.

## 4. Runtime layout

Each boot receives a private owner-only runtime directory containing:

- Cloud Hypervisor API socket.
- Vsock mux socket.
- Serial socket.
- Event monitor or boot-notify socket.
- Temporary helper sockets.

All paths are descriptor-relative and race-resistant. Runtime paths are never durable machine truth.

## 5. Host lifecycle ownership

The host systemd manager directly owns Cloud Hypervisor in a transient unit. Selected `passt`, `virtiofsd`, or durable portal helpers are sibling units in one machine slice with exact dependencies.

No Z-authored machine supervisor is baseline. CLI termination does not terminate the computer. Guest shutdown, VMM exit, systemd unit state, API evidence, process identity, and socket ownership are reconciled directly.

## 6. Credential bootstrap

Z generates machine identity before first boot. On start:

1. Create and verify private API/runtime sockets.
2. Start the pinned VMM process under systemd.
3. Submit the complete VM configuration over the API socket.
4. Include SMBIOS Type 11 system credentials for SSH host key, authorized keys, and optional boot notify socket.
5. Boot the VM.
6. PID 1 imports system credentials.
7. Static AF_VSOCK socket activation launches stock `sshd -i` per connection.
8. Z requires a strict authenticated SSH handshake before reporting ready.

## 7. SSH profiles

### 7.1 Native profile

- Reserved `z-*` namespace.
- Absolute Z executable path.
- `ProxyUseFdpass=yes`.
- Read-only strict host-key lookup.
- Z exits after descriptor transfer.

### 7.2 Compatibility profile

- Explicit generated machine entries.
- Transparent stdio proxy.
- Generated strict host-key inventory.
- Intended for embedded SSH libraries without fd passing.

### 7.3 Internal profile

- Ignores ambient owner SSH configuration.
- Exact identity and host key.
- No agent, X11, forwarding, jump host, local command, remote command, or environment inheritance.
- Bounded timeouts and deterministic options.

## 8. Identity lifecycle

- **Create:** new UUID and host key before connection.
- **Restart:** preserve identity.
- **Rename:** preserve identity; alias changes only.
- **Restore same computer:** preserve identity.
- **Fork/import as new:** rotate UUID, host key, vsock CID, SMBIOS UUID, MACs, disk serials, and collision-prone guest identity.
- **Host-key rotation:** explicit continuity-proven transition; unknown key change hard-fails.

## 9. State and recovery

Current state is derived from:

- Host systemd unit/cgroup.
- Process start identity and executable.
- VMM API and exact sockets.
- Disk and machine metadata.
- Authenticated SSH.
- Serial output.

Serial is independent recovery when SSH is unavailable. Cleanup removes only exactly owned runtime resources and preserves ambiguous durable state.

## 10. Zero-at-rest property

When every machine and optional edge is stopped, no Z process, relay, watcher, timer, socket activator, or helper remains. Host systemd itself is not a Z process.
