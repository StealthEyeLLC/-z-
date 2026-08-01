# Host-kernel transition tests

Every result below passed on the running `6.8.0-9001-generic` boot.

| Gate | Result |
|---|---|
| Signed Ubuntu source artifacts matched recorded SHA-256 digests | PASS |
| Upstream fix commit `81ccda30b4e83d8f5cc4fd50503c44e3a33abfeb` matched the preserved patch | PASS |
| Patch reverse-apply check against built source | PASS |
| Forward reapply rejected because the patch was already present | PASS |
| Built MMU source matched the recorded exact hunk after path normalization | PASS |
| Installed compressed `kvm.ko` matched the validated package output | PASS |
| Loaded KVM srcversion matched the installed module | PASS |
| Candidate config matched kernel 136 except the version signature | PASS |
| 1,011 candidate modules checked; vermagic failures | `0` |
| All 80 modules loaded on the rollback boot were present in the candidate | PASS |
| KVM API version | `12` |
| KVM VM and vCPU creation | PASS |
| AF_VSOCK bind and listen | PASS |
| TAP create and automatic cleanup through `/dev/net/tun` | PASS |
| Unix `SCM_RIGHTS` descriptor transfer | PASS |
| OpenSSH `ProxyUseFdpass=yes` effective parsing | PASS |
| Transient systemd unit create/wait/collect | PASS |
| Loop attach/detach | PASS |
| Mount namespace creation | PASS |
| Landlock ABI query | `4` |
| seccomp and seccomp-filter kernel configuration | PASS |
| Baby, SSH, Caddy, and network returned after reboot | PASS |
| Failed systemd units | `0` |
| dpkg audit and APT repair simulation | PASS |
| Candidate one-time GRUB entry consumed | PASS |
| Kernel 136 retained and configured as persistent fallback | PASS |
| Temporary proof unit, build helpers, mounts, and transition staging cleaned | PASS |

The KVM module identities are:

- package SHA-256: `98f184d88d076c5d3458eb921a92a2ebb2c44119b71df3191b9607da13ea88ed`;
- compressed module SHA-256: `27c53953087080c7baf9119d62f2e61ef3a81f2faed12eb086359b5cf40580b8`;
- ELF SHA-256: `dc6faf80d06f5314c259b59c8be40faaf6d32449645d4110344a1379909ea7c9`;
- ELF build ID: `1a9bcf21095ea9daa3a8277907a9beddb9274273`;
- srcversion: `403F1A311A13D8B84CC56BF`.
