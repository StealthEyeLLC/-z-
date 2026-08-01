# Phase 0A Implementation Roots

Status: **Materialized and verified implementation-only authority; not release certification**

## 1. Purpose and boundary

These roots bind the exact Phase 0A implementation environment to implementation-host tuple `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1` and preserved release-candidate tuple `z-debian-13.6-amd64-ch53-v1`. They separate source, durable inputs, caches, temporary staging, runtime scratch space, reserved future machine space, and evidence so ambient host state cannot silently become a Z dependency.

This authority records implementation infrastructure only. It does not certify a release, implement Z product source, create a guest disk, create a machine, or authorize Phase 0B or Phase 1.

## 2. Exact roots

| Name | Absolute path | Owner | Mode | Filesystem / mount / device | Allowed contents | Cleanup authority |
|---|---|---|---|---|---|---|
| `assets` | `/var/lib/z-implementation/phase-0a-v1/assets/z-debian-13.6-amd64-ch53-v1` | `root:root` | `0750` | `ext4` / `/` / `8:1` | verified Cloud Hypervisor and CLOUDHV.fd only | exact path after asset manifest verification |
| `build` | `/var/lib/z-implementation/phase-0a-v1/build` | `root:root` | `0750` | `ext4` / `/` / `8:1` | isolated builder and toolchains | exact manifest-listed child removal |
| `cache` | `/var/cache/z-implementation/phase-0a-v1` | `root:root` | `0750` | `ext4` / `/` / `8:1` | verified Phase 0A caches | exact manifest-listed cache content only |
| `debian_builder` | `/var/lib/z-implementation/phase-0a-v1/build/debian-builder-20260731T120000Z-amd64` | `root:root` | `0750` | `ext4` / `/` / `8:1` | exact 212-package Debian builder payload closure, unpacked state | exact path after package manifest verification |
| `debian_packages` | `/var/cache/z-implementation/phase-0a-v1/debian-packages` | `root:root` | `0750` | `ext4` / `/` / `8:1` | verified locked package files and indexes | exact package manifest only |
| `downloads` | `/var/cache/z-implementation/phase-0a-v1/downloads` | `root:root` | `0750` | `ext4` / `/` / `8:1` | verified metadata and component archives | exact download manifest only |
| `durable` | `/var/lib/z-implementation/phase-0a-v1` | `root:root` | `0750` | `ext4` / `/` / `8:1` | Phase 0A durable implementation outputs | exact manifest-listed child removal after separate authorization |
| `host_evidence` | `/var/lib/z-implementation/phase-0a-v1/evidence` | `root:root` | `0750` | `ext4` / `/` / `8:1` | sanitized Phase 0A evidence | exact manifest-listed evidence only |
| `machines_reserved` | `/var/lib/z-implementation/phase-0a-v1/machines-reserved` | `root:root` | `0750` | `ext4` / `/` / `8:1` | must remain empty in Phase 0A | exact empty path only |
| `runtime` | `/run/z-implementation/phase-0a-v1` | `root:root` | `0700` | `tmpfs` / `/run` / `0:24` | temporary runtime; empty or absent at completion | exact owned runtime path only |
| `rust_toolchain` | `/var/lib/z-implementation/phase-0a-v1/build/toolchains/rust-1.97.1-x86_64-unknown-linux-gnu` | `root:root` | `0550` | `ext4` / `/` / `8:1` | exact Rust 1.97.1 toolchain; read-only | exact path after digest and ownership verification |
| `source` | `/var/lib/baby-quirt/workspaces/dash-z-build-plan-current-20260731` | `root:root` | `0755` | `ext4` / `/` / `8:1` | authoritative repository only; preserve existing ownership and mode | repository-controlled cleanup only |
| `staging` | `/var/tmp/z-implementation/phase-0a-v1` | `root:root` | `0700` | `ext4` / `/` / `8:1` | owned temporary staging; empty at completion | exact owned staging entries only |

The source workspace keeps its pre-existing `0755` mode. Durable implementation roots use `0750`; staging and runtime use `0700`; the Rust root is hardened to `0550`; Cloud Hypervisor is `0555`; `CLOUDHV.fd` is `0444`.

## 3. Durable, temporary, and empty roots

Durable outputs are the build root, Rust toolchain, Debian builder, asset root, cache, and host evidence root. The staging and runtime roots are temporary and are empty at Phase 0A completion. `machines-reserved` is durable only as an empty reservation; it must not contain an actual machine until a separately authorized later phase.

## 4. Capacity policy

Before any materialization, `/` had `90,967,793,664` available bytes. The declared worst case was `34,359,738,368` bytes and the protected failure reserve was `21,474,836,480` bytes, requiring at least `55,834,574,848` available bytes and `500,000` free inodes. After materialization, `/` had `89,350,074,368` available bytes and `12,575,866` free inodes. Positive and simulated low-capacity tests passed without consuming disk to force failure.

## 5. Reflink and copy policy

The selected ext4 filesystem rejects `cp --reflink=always`. The required fallback is `cp --reflink=never --sparse=always` to an owned `.partial` path, followed by content, size, allocation, hole, owner, and mode verification, file and directory fsync, and atomic rename. An interrupted copy must never create the final name. Cleanup may remove only an exact owned partial path; it must refuse unrelated paths and preserve sentinels.

## 6. Cleanup, deletion, and migration

Cleanup is exact-path and manifest based. Age, filename prefix, wildcard searches outside an owned root, filesystem-wide discovery, and assumptions about other projects are prohibited. A durable root may be deleted or migrated only after its path, ownership, link state, mount boundary, and manifest identity are reverified and a separately authorized operation names the exact contents to remove or copy.

## 7. Refresh conditions

Recapture this authority if the implementation-host tuple, boot ID, kernel, mount, device, filesystem, ownership, mode, capacity policy, root path, dependency identity, or cleanup authority changes. Do not edit the existing tuple to match drift; create and authorize a new tuple.

## 8. Ambient-tool prohibition

The isolated Debian closure, Rust toolchain, Cloud Hypervisor binary, and firmware are authoritative. Host-installed Rust, host APT sources, Ubuntu packages, live mirrors, ambient Cargo registries, owner shell profiles, and unrelated caches are not accepted implementation inputs.

## 9. Evidence binding

Repository checkpoint: [`../../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/`](../../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/)

Host evidence: `/var/lib/z-implementation/phase-0a-v1/evidence`

Host payload-manifest SHA-256: `8be1e439c3bd93cb6a549df14b13bc8120410157c86d72914aac7af61cc14da2`

The machine-readable authority is [`../../assets/implementation-roots.json`](../../assets/implementation-roots.json).
