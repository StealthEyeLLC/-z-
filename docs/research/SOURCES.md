# Primary Research Sources

The architecture report draws primarily from upstream documentation and source code.

## OpenSSH

- OpenSSH project and current release notes: <https://www.openssh.com/>
- `ssh_config(5)`: <https://man.openbsd.org/ssh_config>
- `sshd_config(5)`: <https://man.openbsd.org/sshd_config>
- `sshd(8)`: <https://man.openbsd.org/sshd>
- `sftp(1)`: <https://man.openbsd.org/sftp>
- SSH Connection Protocol: <https://www.rfc-editor.org/rfc/rfc4254>

## systemd

- System and service credentials: <https://systemd.io/CREDENTIALS/>
- VM interface: <https://systemd.io/VM_INTERFACE/>
- `systemd.socket(5)`: <https://github.com/systemd/systemd/blob/main/man/systemd.socket.xml>
- `systemd-ssh-proxy(1)`: <https://github.com/systemd/systemd/blob/main/man/systemd-ssh-proxy.xml>
- `systemd-stdio-bridge(1)`: <https://github.com/systemd/systemd/blob/main/man/systemd-stdio-bridge.xml>
- `systemd-run(1)`: <https://github.com/systemd/systemd/blob/main/man/systemd-run.xml>

## Cloud Hypervisor

- Repository: <https://github.com/cloud-hypervisor/cloud-hypervisor>
- VSOCK documentation: <https://github.com/cloud-hypervisor/cloud-hypervisor/blob/main/docs/vsock.md>
- v26 SMBIOS OEM-string release: <https://www.cloudhypervisor.org/blog/cloud-hypervisor-v26.0-released/>
- Release history and security notes: <https://www.cloudhypervisor.org/blog/>

## Ecosystem references

- VS Code Remote SSH: <https://code.visualstudio.com/docs/remote/ssh>
- JetBrains remote development: <https://www.jetbrains.com/help/idea/remote-development-overview.html>
- Lima SSH configuration export implementation: <https://github.com/lima-vm/lima>
- Vagrant `ssh-config`: <https://developer.hashicorp.com/vagrant/docs/cli/ssh_config>
- Coder SSH configuration: <https://coder.com/docs/reference/cli/config-ssh>

## Kernel and confinement

- Landlock: <https://docs.kernel.org/userspace-api/landlock.html>
- `openat2(2)`: <https://man7.org/linux/man-pages/man2/openat2.2.html>
- AF_VSOCK: <https://man7.org/linux/man-pages/man7/vsock.7.html>

## Final delta audit — accessed 2026-07-31

### OpenSSH and SSH protocol

- OpenSSH release notes: <https://www.openssh.com/releasenotes.html>
- Current `ssh_config(5)`: <https://man.openbsd.org/ssh_config.5>
- Current `sshd(8)`: <https://man.openbsd.org/sshd.8>
- SSH Connection Protocol, RFC 4254: <https://www.rfc-editor.org/rfc/rfc4254.html>

### systemd

- Credentials: <https://systemd.io/CREDENTIALS/>
- VM interface: <https://systemd.io/VM_INTERFACE/>
- `systemd.socket(5)`: <https://github.com/systemd/systemd/blob/main/man/systemd.socket.xml>
- `systemd-stdio-bridge(1)`: <https://github.com/systemd/systemd/blob/main/man/systemd-stdio-bridge.xml>
- `systemd-run(1)`: <https://github.com/systemd/systemd/blob/main/man/systemd-run.xml>

### Cloud Hypervisor

- v53.0 release: <https://www.cloudhypervisor.org/blog/cloud-hypervisor-v53.0-released/>
- v52.0 release and CVE-2026-45782 fix: <https://www.cloudhypervisor.org/blog/cloud-hypervisor-v52.0-released/>
- v50.0 release documenting the x86 `nested=on` default: <https://www.cloudhypervisor.org/blog/cloud-hypervisor-v50.0-released/>
- v53.0 Unix vsock mux source: <https://github.com/cloud-hypervisor/cloud-hypervisor/blob/v53.0/virtio-devices/src/vsock/unix/muxer.rs>
- v53.0 SMBIOS source: <https://github.com/cloud-hypervisor/cloud-hypervisor/blob/v53.0/arch/src/x86_64/smbios.rs>
- Stability policy: <https://github.com/cloud-hypervisor/cloud-hypervisor#3-status>

### Linux, KVM, AF_VSOCK, and confinement

- `vsock(7)`: <https://man7.org/linux/man-pages/man7/vsock.7.html>
- Virtio 1.3 specification: <https://docs.oasis-open.org/virtio/virtio/v1.3/virtio-v1.3.html>
- Landlock userspace API: <https://docs.kernel.org/userspace-api/landlock.html>
- CVE-2026-53359 Januscape disclosure: <https://www.openwall.com/lists/oss-security/2026/07/06/7>
- Upstream Januscape fix: <https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/commit/?id=81ccda30b4e83d8f5cc4fd50503c44e3a33abfeb>

### Networking and native clients

- Current `passt(1)`: <https://passt.top/builds/latest/web/passt.1.html>
- Upstream `passt-user` record of residual host-external-address reachability: <https://lists.passt.top/hyperkitty/list/passt-user%40passt.top/thread/ZMG4ZWRAYYYRS3UEAUVYJKVYWJOI5GIP/>
- VS Code Remote SSH: <https://code.visualstudio.com/docs/remote/ssh>
- JetBrains Gateway SSH workflow: <https://www.jetbrains.com/help/idea/remote-development-a.html>
- JetBrains SSH configurations: <https://www.jetbrains.com/help/idea/settings-tools-ssh-configurations.html>

## Initial dependency tuple — accessed 2026-07-31

### Debian reference host and guest

- Debian 13.6 release announcement: <https://www.debian.org/News/2026/20260711>
- Debian 13 release information: <https://www.debian.org/releases/trixie/>
- Debian Snapshot service: <https://snapshot.debian.org/>
- Debian archive signing keys and published fingerprints: <https://ftp-master.debian.org/keys.html>
- Locked Debian archive state: <https://snapshot.debian.org/archive/debian/20260731T120000Z/>
- Locked Debian security archive state: <https://snapshot.debian.org/archive/debian-security/20260731T120000Z/>
- Debian security tracker for CVE-2026-53359: <https://security-tracker.debian.org/tracker/CVE-2026-53359>

### Cloud Hypervisor and firmware

- Cloud Hypervisor v53.0 release: <https://www.cloudhypervisor.org/blog/cloud-hypervisor-v53.0-released/>
- Cloud Hypervisor v53.0 release assets: <https://github.com/cloud-hypervisor/cloud-hypervisor/releases/tag/v53.0>
- Cloud Hypervisor v53.0 source identity: <https://github.com/cloud-hypervisor/cloud-hypervisor/tree/v53.0>
- Cloud Hypervisor EDK2 release `ch-1e1b96f126`: <https://github.com/cloud-hypervisor/edk2/releases/tag/ch-1e1b96f126>

### Rust toolchain

- Rust 1.97.1 release: <https://blog.rust-lang.org/2026/07/16/Rust-1.97.1/>
- Rust 1.97.1 channel manifest: <https://static.rust-lang.org/dist/channel-rust-1.97.1.toml>
- Rust 1.97.1 channel-manifest digest: <https://static.rust-lang.org/dist/channel-rust-1.97.1.toml.sha256>
