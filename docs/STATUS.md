# Current Status — Phase 0B Certified; Host Reboot Continuity Verified

Status: **Canonical operational status; Phase 0A complete and Phase 0B semantic certification complete; not product or release certification**

## 1. Executive result

Phase 0A is complete. Exact implementation roots and locked supply-chain inputs are materialized and verified on implementation-host tuple `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`. The evidence checkpoint is [`../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/`](../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/).

The preserved release candidate remains `z-debian-13.6-amd64-ch53-v1`, status candidate, certification inheritance false. The Ubuntu implementation host is not the Debian reference host.

Phase 0B is certified in the isolated semantic lab. Two fresh disposable identities each passed Boot A to B to C with one disk, UUID, CID, host key, and owner authorization, strict authenticated SSH after both reboots, persistent filesystem state, serial and vsock reconnect, fresh transport/systemd regressions, 60 fail-closed negative tests, and exact cleanup.

On 2026-08-02, exactly one controlled implementation-host maintenance reboot returned the same retained OVH VPS on the same locked kernel. The boot ID changed from `b6e10e21-9737-4ded-ad1e-a437eea41ace` to `68eb2755-8adb-4b54-91c5-8609a0cb1e67`; the previous boot reached `reboot.target`, the pending reboot marker did not return, all required host primitives passed again, and Phase 0A/0B checkpoint integrity and zero-residue gates remained valid. The checkpoint is [`../evidence/checkpoints/host-maintenance-reboot-20260802/`](../evidence/checkpoints/host-maintenance-reboot-20260802/). This is implementation-host maintenance only, not a new product or release certification.

A later owner-initiated host reboot was independently read back on 2026-08-03. The same host returned on the locked kernel with boot ID `6931af4d-d605-4743-a34c-abfcb59af94e`; package health, required services, KVM/vsock/TUN and descriptor-passing primitives, confinement prerequisites, and zero-residue gates passed. The follow-up is [`../evidence/checkpoints/host-reboot-readback-20260803/`](../evidence/checkpoints/host-reboot-readback-20260803/).

Phase 1 has not started. Z product source, a product guest disk, a product machine, a Z executable, runtime service, listener, and release do not exist.

## 2. Repository checkpoint basis

- Repository: `StealthEyeLLC/-z-`
- Branch: `build/z-v1-cleanroom`
- Phase 0A starting commit: `44d7abc7034c68d17171d089ec341e895f91a10b`
- Starting tree: `198f9c8e35c50071340bfc37915abc7c9bb4430d`
- Historical branch preserved at `4e17ead436949b32d245c15df5bcf2418f2f8968`
- Host-maintenance source commit: `86c7623277be8734b89dc5bdf874620e33744a26`
- Host-maintenance source tree: `c479417e841667dc981dfc7eff7b5c42212f3284`

## 3. Implementation host

The running kernel remains `6.8.0-9001-generic`; latest recorded boot ID is `6931af4d-d605-4743-a34c-abfcb59af94e`; rollback kernel `6.8.0-136-generic` remains installed. systemd is running, failed units are zero, NTP is synchronized, no reboot is required, dpkg audit is clean, and retained Baby, SSH, and Caddy units are active.

The original host-transition checkpoint remains immutable under [`../evidence/checkpoints/host-kernel-transition-20260801/`](../evidence/checkpoints/host-kernel-transition-20260801/). The later one-reboot maintenance proof is under [`../evidence/checkpoints/host-maintenance-reboot-20260802/`](../evidence/checkpoints/host-maintenance-reboot-20260802/), and the subsequent owner-initiated reboot readback is under [`../evidence/checkpoints/host-reboot-readback-20260803/`](../evidence/checkpoints/host-reboot-readback-20260803/).

## 4. Materialized implementation inputs

- Debian snapshot: `20260731T120000Z`, trixie amd64 main, exact signed metadata and indexes.
- Builder direct set: 23 packages.
- Builder closure: exactly 212 package identities and 212 verified package files.
- Builder state: exact package payloads, dpkg truth `install ok unpacked`, no maintainer scripts and no global Debian installation.
- mmdebstrap: exact `1.5.7-1+deb13u1`; in-root version, help, and syntax checks pass.
- Rust: exact `1.97.1`, target `x86_64-unknown-linux-gnu`, Edition 2024, five required components, no crates or Cargo state.
- Cloud Hypervisor: v53.0, commit `9ed824d6d08df3e96f7d5f50795d9449ac99f431`, exact static binary.
- Firmware: `CLOUDHV.fd`, tag `ch-1e1b96f126`, commit `1e1b96f1264a9c9532cbeb053c8c05885a7d2c78`.

## 5. Roots and capacity

The exact roots, ownership, modes, mount/device identities, cleanup authorities, sparse-copy method, and reserve policy are authoritative in [`reference/IMPLEMENTATION-ROOTS.md`](reference/IMPLEMENTATION-ROOTS.md) and [`../assets/implementation-roots.json`](../assets/implementation-roots.json).

The failure reserve is 20 GiB. Post-materialization available space is `89,350,074,368` bytes; the required-plus-reserve threshold is `55,834,574,848` bytes. Reflink is unavailable. The sparse fallback and interrupted-copy tests passed.

## 6. Negative and absence gates

All 35 required negative tests passed using disposable state. The reserved-machine root is empty; the volatile runtime root is empty or absent as its root authority permits at completion. There is no Cloud Hypervisor process, Z process, guest disk, machine, product Cargo file, new systemd unit, listener, Z TAP, or owned mount. Host APT sources, global package state, global Rust state, kernel, boot policy, and retained services were not changed.

## 7. Claim boundary

Phase 0A proves exact implementation inputs and environment materialization. Phase 0B additionally proves the named disposable semantic-lab machine, SSH, reboot, persistence, execution, compatibility, negative, replay, and cleanup gates. It does not create or certify product source, a durable product machine, confinement, networking, update, backup, ecosystem, or release behavior.

## 8. Phase 0B semantic checkpoint — certified

The historical blocker remains at [`../evidence/checkpoints/phase-0b-semantic-blocker-20260801/`](../evidence/checkpoints/phase-0b-semantic-blocker-20260801/). Repair evidence established that its one-character command-line value `B` was not present in the raw serial capture. The actual first divergence was the disposable loopback fixture: restarting signal semantics left `accept4()` blocked until systemd's 90-second stop timeout. Stock socket-activated `sshd -i` status 255 and an unrelated regular SSH enablement also produced false failed-unit state.

The repair uses non-restarting `sigaction()` handlers, a five-second loopback stop bound, `SuccessExitStatus=255`, no regular SSH enablement, guest `systemctl reboot --no-block`, fresh runtime-socket validation, and three consecutive strict authenticated sessions before readiness. Two independent Boot A-B-C runs passed with persistent state and complete identity continuity. Cloud Hypervisor `vm.reboot` is recorded separately as abrupt VM-object recreation, not the supported orderly reboot contract.

Checkpoint: [`../evidence/checkpoints/phase-0b-reboot-repair-20260802/`](../evidence/checkpoints/phase-0b-reboot-repair-20260802/)

## 9. Next permitted mission

The next permitted mission is Phase 1 only after separate authorization. No product machine exists, no release is certified, and the preserved candidate tuple remains a candidate rather than a release.
