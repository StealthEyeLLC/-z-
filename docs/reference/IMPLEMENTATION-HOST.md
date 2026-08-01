# OVH VPS Implementation Host Settings

Status: **Verified implementation-host tuple; implementation-host-only, not release certification**

Captured: `2026-08-01T19:08:00Z`

Implementation-host tuple: `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`

Machine-readable authority: [`../../assets/dependencies.lock.json`](../../assets/dependencies.lock.json) under `implementation_host`

Evidence checkpoint: [`../../evidence/checkpoints/host-kernel-transition-20260801/RESULT.md`](../../evidence/checkpoints/host-kernel-transition-20260801/RESULT.md)

## 1. Purpose and boundary

This record binds Z implementation work to the actual retained OVH VPS after the authorized Ubuntu host-kernel transition. It is a point-in-time operational authority for implementation routing and reproducibility.

It does not certify a Z release, a guest image, Cloud Hypervisor, firmware, networking, or the preserved Debian release candidate. Clean-room Phase 0A has not started.

Baby remains implementation infrastructure only. It is not a Z runtime component, dependency, guest service, protocol, or product surface.

## 2. Transition result

The same OVH VPS and Ubuntu 24.04 installation were retained. No reimage, operating-system replacement, second server, Baby migration, or control-plane relocation occurred.

The host is running:

- kernel release `6.8.0-9001-generic`;
- package version `6.8.0-9001.1+zcve2026533591`;
- Ubuntu Noble base source `linux 6.8.0-136.136`;
- upstream CVE-2026-53359 fix commit `81ccda30b4e83d8f5cc4fd50503c44e3a33abfeb`;
- patch SHA-256 `84d5f450aaff799e1e7cf9392a137cb9afc9702baa3c6c5dbc9343e6d6c05c6c`.

The built source passed reverse-apply proof for the fix, rejected a duplicate forward apply, and matched the recorded exact MMU hunk. The installed KVM module is byte-bound to the validated package output and its loaded srcversion matches the installed module.

Kernel `6.8.0-9001-generic` is the persistent GRUB default. Kernel `6.8.0-136-generic` remains installed as the tested explicit rollback entry. The controlled one-time candidate selection was consumed; no `next_entry` remains.

## 3. Exact host identity

| Field | Exact value |
|---|---|
| Provider role | OVH-hosted KVM VPS |
| Host label | `vps-c9f04f5e` |
| Machine ID SHA-256 | `cd189817b39fea60d338b73878240a6fe7db71374c7a0f35ad60f8eb641e8817` |
| Machine-ID file SHA-256 | `e12bd35a8576ac2dfe2da93c2e827fa3a4efcf4285beecd961adefbe63e08f32` |
| Boot ID | `b6e10e21-9737-4ded-ad1e-a437eea41ace` |
| Distribution | Ubuntu 24.04.4 LTS |
| Architecture | `x86_64` |
| systemd | `255` |
| `libc6` | `2.39-0ubuntu8.8` |
| CPU | Intel Core Processor (Haswell, no TSX) |
| vCPUs | `6` |
| Memory | `11,956,740 kB` |
| Swap | `0 kB` |
| Root filesystem | `ext4`; reflink unsupported |
| Root total | `102,888,095,744` bytes |
| Root available | `90,960,056,320` bytes |
| `/boot` available | `680,804,352` bytes |

Public addresses, MAC addresses, credentials, private keys, tokens, and unrelated retained host state are intentionally excluded.

## 4. Kernel and supply-chain binding

| Item | Exact identity |
|---|---|
| Ubuntu source orig | `26512115972bdf017a4ac826cc7d3e9b0ba397d4f85cd330e4e4ff54c78061c8` |
| Ubuntu source delta | `ccce6d47f36bc749d69a5faa41237c3269e5345d3852d6afe868a5629ac8c316` |
| Ubuntu source DSC | `9bf54e2fc501c2f37b48d03dc268ef601e911f9be15df5cfb1e5d9f8d6174fba` |
| KVM modules package | `98f184d88d076c5d3458eb921a92a2ebb2c44119b71df3191b9607da13ea88ed` |
| Installed compressed `kvm.ko` | `27c53953087080c7baf9119d62f2e61ef3a81f2faed12eb086359b5cf40580b8` |
| Decompressed KVM ELF | `dc6faf80d06f5314c259b59c8be40faaf6d32449645d4110344a1379909ea7c9` |
| KVM ELF build ID | `1a9bcf21095ea9daa3a8277907a9beddb9274273` |
| KVM srcversion | `403F1A311A13D8B84CC56BF` |
| Nested KVM | `Y` |

The package outputs, source artifacts, patch, build logs, rollback snapshot, cleanup proof, and durable evidence manifest remain under `/var/lib/z-kernel-transition/20260801` on the implementation host. Repository-safe proof is stored in the evidence checkpoint linked above.

## 5. Verified implementation primitives

| Primitive | Result |
|---|---|
| KVM API | `12` |
| KVM VM creation | PASS |
| KVM vCPU creation | PASS |
| `/dev/kvm` and loaded `kvm_intel` | PASS |
| `/dev/vhost-vsock` and AF_VSOCK bind/listen | PASS |
| TAP create and cleanup through `/dev/net/tun` | PASS |
| Unix `SCM_RIGHTS` descriptor transfer | PASS |
| OpenSSH `ProxyUseFdpass=yes` | PASS |
| Transient systemd unit lifecycle | PASS |
| Loop attach/detach | PASS |
| Mount namespace creation | PASS |
| Landlock ABI | `4` |
| seccomp and seccomp-filter configuration | PASS |

These checks prove host capability only. They do not prove Z product behavior or release compatibility.

## 6. Retained service and package health

- Baby Quirt socket: active.
- Baby MCP edge: active.
- SSH socket: active.
- Caddy: active.
- systemd state: `running`.
- failed systemd units: `0`.
- NTP synchronized: `yes`.
- reboot required: `false`.
- `dpkg --audit`: clean.
- APT repair simulation: no changes required.

Temporary build helpers, temporary proof units, transition mounts, and large transition-owned build trees were removed after evidence preservation.

## 7. Repository authority

The authoritative implementation branch is `build/z-v1-cleanroom`. The historical `build/z-v1` branch remains unchanged and must not be rewritten or reused as the clean-room implementation branch.

The preserved release candidate remains `z-debian-13.6-amd64-ch53-v1`. The actual Ubuntu implementation host uses the distinct tuple `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1` and cannot claim the Debian-host identity.

## 8. Readiness decision

The same-VPS host-kernel blocker is closed for implementation-host purposes. The running kernel, applicable KVM fix state, rollback path, required host primitives, service recovery, storage headroom, and cleanup state are verified.

This mission ends at that checkpoint. Phase 0A was not started. A later implementation mission must still perform its own dependency, capacity, provenance, cleanup, and compatibility gates before creating implementation roots or product source.

## 9. Refresh rule

Recapture this record and create a new implementation-host tuple before relying on any changed kernel, package set, machine identity, CPU exposure, filesystem, boot policy, KVM behavior, Landlock ABI, seccomp behavior, OpenSSH behavior, or retained control-plane state.
