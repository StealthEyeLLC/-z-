# OVH VPS Implementation Host Settings

Status: **Point-in-time operational reference; not normative; not certification evidence**

Captured: `2026-07-31T20:07:01Z`

Host label: `vps-c9f04f5e`

Role: dedicated private Baby-and-Z implementation host

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
| Boot ID | `4f39061a-161e-434a-af57-a2554feb2207` |
| Loaded `libc6` | `2.39-0ubuntu8.8` |
| Pending reboot | **no** |

The authorized controlled reboot completed before this capture. The boot ID changed, `/var/run/reboot-required` is absent, the loaded `libc6` matches the installed package, systemd reports zero failed units, and the previous boot reached `reboot.target` before shutdown synchronization.

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
| Root filesystem used | `5,450,244,096` bytes |
| Root filesystem available | `97,421,074,432` bytes |
| Reported use | 6% |
| Provisional maintenance floor | `32,212,254,720` bytes (30 GiB) |
| Difference from floor | **65,208,819,712 bytes above** |

The host is above the provisional maintenance floor after the authorized exact-manifest reclamation. Independent certification recorded `36,603,695,104` bytes available before cleanup, `97,421,299,712` bytes available at certification, and `60,817,604,608` net bytes recovered. This does not waive the stronger operation-specific gate: no large image, clone, snapshot, package, or build mutation may start until its exact capacity plan proves that temporary data, durable output, rollback material, evidence, and failure reserve fit simultaneously.

Because ext4 reflink is unavailable, this host must use sparse-copy fallback where the design permits it. Tests must verify logical and allocated size, data identity, interrupted-copy behavior, synchronization, atomic installation, and cleanup. A same-filesystem reflink must never be reported as available here.

## 6. Tooling status

### Present ambient tools

- Rust/Cargo `1.88.0` and rustup `1.26.0`;
- OpenSSH `9.6p1` client and server;
- systemd `255`;
- nftables `1.0.9`;
- `debootstrap` `1.0.134ubuntu1`;
- `sfdisk`, `mkfs.ext4`, Git, curl, jq, and ordinary filesystem utilities.
- Node `24.18.0`, retained only as implementation infrastructure for Baby MCP and the Z GitHub App credential helper; `/usr/local/bin/node`, `npm`, and `npx` resolve into `/opt/node-v24.18.0-linux-x64`.

### Not globally installed

- Cloud Hypervisor;
- `passt`;
- `mmdebstrap`;
- `qemu-img`.

Docker, containerd, and snapd are intentionally absent. They are not Z prerequisites and MUST NOT be silently reintroduced as implementation or runtime dependencies.

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

- commit `44236b1c5c189925d81393945921dddc2dd1ad9c`;
- tree `1f935f374b417a90642846e4df80adf94f0d1c37`;
- origin `https://github.com/StealthEyeLLC/-z-.git`.

The repository contains the canonical architecture, dependency lock, build plan, and certification plan. Z source implementation has not started. The first source checkpoint must deliver a real KVM computer rather than schemas, interfaces, mocks, or placeholder commands.

## 8. Appliance boundaries

Baby Quirt, its socket, its MCP edge, SSH socket activation, and the Baby-only Caddy route were active and healthy during capture. Baby MCP runs as the retained `fix-mcp` Unix identity and requires the credentials and state owned by that identity; the legacy name does not make it part of the retired Fix stack. Baby durable jobs, streams, deployment records, maintenance/recovery material, and rollback releases remain because removing them would weaken Baby operation, audit, or recovery. Exactly one Baby workspace remains: the authoritative Z workspace. SMP, Fix execution/operator/OAuth, StealthEye Shell/Quirt/CI, Baby-X, EHJINT, Index, Docker, containerd, and snapd are positively absent.

Z implementation must:

- create and record distinct source, build, asset, machine, runtime, cache, staging, and evidence roots;
- use exact owner, mode, quota or headroom, and cleanup rules;
- avoid mutating Baby runtime, credentials, durable records, retained recovery material, the public edge, administrative access, or base-host security state;
- do not reintroduce any retired project stack or inherit its former paths, users, services, packages, listeners, mounts, loops, interfaces, routes, or certificates;
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
2. the locked Rust, Cloud Hypervisor, firmware, `mmdebstrap`, and required builder closure are materialized and verified;
3. dedicated Z roots and machine-scoped mutation/staging rules are installed.

This host is not automatically a release-certification host. Release certification must independently prove every Gate A host prerequisite and label nested evidence truthfully.

## 10. Refresh rule

Recapture this document after any host kernel, distribution, hypervisor exposure, CPU profile, filesystem, disk layout, service, firewall, KVM, Landlock, AppArmor, package, reboot, storage-remediation, or implementation-root change. A changed host profile creates new evidence; it never silently inherits the old profile's claims.
