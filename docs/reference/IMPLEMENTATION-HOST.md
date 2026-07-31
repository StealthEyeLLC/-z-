# OVH VPS Implementation Host Settings

Status: **Point-in-time operational reference; not normative; not certification evidence**

Captured: `2026-07-31T18:30:16Z`

Host label: `vps-c9f04f5e`

Role: shared private implementation host

## 1. Purpose and boundary

This document records the sanitized current state of the OVH VPS selected for Z implementation. It prevents hidden host assumptions and routes work to the correct preflight gates.

It deliberately excludes public addresses, MAC addresses, credentials, private keys, tokens, encrypted credential paths, and secret-bearing configuration.

This host profile does not certify Z. Release claims remain bound to the exact host, kernel, CPU exposure, filesystem, VMM, firmware, guest, client, dependency, and evidence tuple exercised by [`../CERTIFICATION.md`](../CERTIFICATION.md).

Baby and GitHub applications may implement and publish Z, but they are implementation infrastructure only. They are not Z components, release dependencies, guest contents, runtime authority, update authority, or offline-operation dependencies.

## 2. Authority verdict

**No additional authority or permission is required to begin implementation.**

Verified authority:

- Z GitHub Authority App ID `4380878`, installation ID `148647330`, account `StealthEyeLLC`, repository selection `all`.
- Repository authority includes write access for contents, workflows, actions, checks, statuses, issues, pull requests, deployments, environments, packages, secrets, hooks, administration, security events, attestations, and related repository controls.
- Repository `StealthEyeLLC/-z-`, default branch `main`.
- Ordinary Git created, read, and deleted a temporary remote branch successfully.
- The host execution identity is root and can access the required KVM, vhost-vsock, TUN/TAP, systemd, loop, mount-namespace, and Unix descriptor-passing primitives.

Repository rulesets and branch protection were absent at capture time. GitHub Actions were enabled with allowed actions set to `all`; the default workflow token permission was read-only and pull-request approval by workflows was disabled. These settings do not block local implementation or authenticated Git publication.

The GitHub App cannot register an account-level SSH signing key. Commit and tag signing are intentionally not required for implementation, so this is not a blocker. Repository commits remain bound by exact Git object IDs and remote verification.

## 3. Host identity

| Setting | Observed value |
|---|---|
| Provider role | OVH-hosted KVM VPS |
| Distribution | Ubuntu 24.04.4 LTS |
| Architecture | `x86_64` |
| Kernel | `6.8.0-136-generic` |
| systemd | `255.4-1ubuntu8.16` |
| CPU model exposed | Intel Core Processor, Haswell, no TSX |
| vCPUs | 6 |
| Memory | `11,956,712 kB` |
| Swap | `0 kB` |
| Time zone | UTC |
| NTP synchronized | yes |
| Pending reboot | **yes** |

The pending reboot means evidence that depends on the loaded kernel or package state must not be treated as final after package changes. Reboot requires a separately authorized maintenance action and a fresh host-profile capture.

## 4. Proven implementation primitives

| Primitive | Current result |
|---|---|
| `/dev/kvm` | present, `root:kvm`, mode `0660` |
| KVM API | version 12 |
| `/dev/vhost-vsock` | present, `root:kvm`, mode `0660`; open succeeded |
| `/dev/net/tun` | present, mode `0666` |
| AF_VSOCK stream socket | creation succeeded |
| Unix `SCM_RIGHTS` descriptor handoff | succeeded |
| OpenSSH `ProxyUseFdpass=yes` | parsed and effective |
| Transient systemd unit | create/wait/collect succeeded |
| TAP lifecycle | create/delete succeeded |
| Loop lifecycle | attach/detach succeeded |
| Mount namespace | creation succeeded |
| Root filesystem | ext4 |
| Reflink | unsupported |

These facts establish development feasibility, not release certification. Landlock ABI/rights, seccomp behavior, pre-opened descriptor inventory, exact KVM security-fix state, Cloud Hypervisor effective CPU configuration, and every negative gate still require implementation-time proof.

## 5. Storage and copy behavior

| Setting | Current value |
|---|---:|
| Root filesystem total | `102,888,095,744` bytes |
| Root filesystem used | `70,732,722,176` bytes |
| Root filesystem available | `32,138,596,352` bytes |
| Reported use | 69% |
| Provisional maintenance floor | `32,212,254,720` bytes (30 GiB) |
| Difference from floor | **73,658,368 bytes below** |

The host is no longer broadly storage-blocked, but it is slightly below the provisional floor after the final authority audit and fresh workspace. No large image, clone, snapshot, package, or build mutation may start until its exact capacity plan proves that temporary data, durable output, rollback material, evidence, and failure reserve fit simultaneously.

Because ext4 reflink is unavailable, this host must use sparse-copy fallback where the design permits it. Tests must verify logical and allocated size, data identity, interrupted-copy behavior, synchronization, atomic installation, and cleanup. A same-filesystem reflink must never be reported as available here.

## 6. Tooling status

### Present ambient tools

- Rust/Cargo `1.88.0` and rustup `1.26.0`;
- OpenSSH `9.6p1` client and server;
- systemd `255`;
- nftables `1.0.9`;
- `debootstrap` `1.0.134ubuntu1`;
- `sfdisk`, `mkfs.ext4`, Git, curl, jq, and ordinary filesystem utilities.

### Not globally installed

- Cloud Hypervisor;
- `passt`;
- `mmdebstrap`;
- `qemu-img`.

### Build consequence

Ambient tools are not candidate-tuple authority.

- Materialize and verify the locked Cloud Hypervisor v53.0 static binary and matching EDK2 `CLOUDHV.fd` under the dedicated Z asset root.
- Materialize the locked Rust `1.97.1` toolchain and prove the channel-manifest digest before compiling Z. The installed Rust `1.88.0` is not an allowed substitute.
- Materialize the locked Debian `mmdebstrap` package and builder closure from snapshot `20260731T120000Z`; the installed Ubuntu `debootstrap` is not the selected root-filesystem constructor.
- Defer the locked `passt` package until the connected profile in Phase 2. The first computer uses Network None.
- Do not add `qemu-img` merely because it is absent. The baseline uses independent raw disks and the locked builder closure; introducing a QEMU image dependency requires an explicit lock and tuple change.

No selected tool may be inherited silently from the global PATH.

## 7. Repository and publication state

The fresh authoritative implementation workspace was clean at:

- commit `e90bac8b34b7736755a6f05809d5f46dd7e65a62`;
- tree `34f428238dedde64c1ed2b344093acd6d2f7c15b`;
- origin `https://github.com/StealthEyeLLC/-z-.git`.

The repository contains the canonical architecture, dependency lock, build plan, and certification plan. Z source implementation has not started. The first source checkpoint must deliver a real KVM computer rather than schemas, interfaces, mocks, or placeholder commands.

## 8. Shared-host boundaries

Baby Quirt, its socket, and its MCP edge were active and healthy during capture. Containerd was active. Other project roots and persistent machines remain separately owned.

Z implementation must:

- create and record distinct source, build, asset, machine, runtime, cache, staging, and evidence roots;
- use exact owner, mode, quota or headroom, and cleanup rules;
- avoid unrelated Baby, SMP, Fix, EHJINT, containerd, user-home, service, firewall, and machine state;
- never infer cleanup authority from age, name, prefix, or size;
- keep implementation credentials and executors out of release artifacts and runtime authority.

## 9. Readiness decision

The host is ready for:

- source implementation;
- dependency and supply-chain verification;
- bounded materialization after capacity preflight;
- unit, integration, and negative tests scoped honestly to this host;
- nested-KVM development and smoke evidence explicitly labelled as nested.

The host is not yet ready for the first large image mutation until:

1. the exact operation-specific capacity gate passes with bounded failure headroom;
2. the pending reboot is resolved when loaded-kernel/package-state evidence would otherwise be invalid;
3. the locked Rust, Cloud Hypervisor, firmware, `mmdebstrap`, and required builder closure are materialized and verified;
4. dedicated Z roots and machine-scoped mutation/staging rules are installed.

This host is not automatically a release-certification host. Release certification must independently prove every Gate A host prerequisite and label nested evidence truthfully.

## 10. Refresh rule

Recapture this document after any host kernel, distribution, hypervisor exposure, CPU profile, filesystem, disk layout, service, firewall, KVM, Landlock, AppArmor, package, reboot, storage-remediation, or implementation-root change. A changed host profile creates new evidence; it never silently inherits the old profile's claims.
