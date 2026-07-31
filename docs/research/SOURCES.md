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
- `systemd.socket(5)`: <https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html>
- `systemd-ssh-proxy(1)`: <https://www.freedesktop.org/software/systemd/man/latest/systemd-ssh-proxy.html>
- `systemd-stdio-bridge(1)`: <https://www.freedesktop.org/software/systemd/man/latest/systemd-stdio-bridge.html>
- `systemd-run(1)`: <https://www.freedesktop.org/software/systemd/man/latest/systemd-run.html>

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
- Coder SSH configuration: <https://coder.com/docs/user-guides/workspace-access/ssh>

## Kernel and confinement

- Landlock: <https://docs.kernel.org/userspace-api/landlock.html>
- `openat2(2)`: <https://man7.org/linux/man-pages/man2/openat2.2.html>
- AF_VSOCK: <https://man7.org/linux/man-pages/man7/vsock.7.html>
