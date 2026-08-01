# Current Status — Phase 0B Executed, Certification Blocked

Status: **Canonical operational status; implementation-input checkpoint only; not product or release certification**

## 1. Executive result

Phase 0A is complete. Exact implementation roots and locked supply-chain inputs are materialized and verified on implementation-host tuple `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`. The evidence checkpoint is [`../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/`](../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/).

The preserved release candidate remains `z-debian-13.6-amd64-ch53-v1`, status candidate, certification inheritance false. The Ubuntu implementation host is not the Debian reference host.

Phase 0B was executed in an isolated semantic lab but is not certified. The required same-machine persistent guest reboot and authenticated reconnect gate failed. Phase 1 has not started. Z product source, a product guest disk, a product machine, a Z executable, runtime service, listener, and release do not exist.

## 2. Repository checkpoint basis

- Repository: `StealthEyeLLC/-z-`
- Branch: `build/z-v1-cleanroom`
- Phase 0A starting commit: `44d7abc7034c68d17171d089ec341e895f91a10b`
- Starting tree: `198f9c8e35c50071340bfc37915abc7c9bb4430d`
- Historical branch preserved at `4e17ead436949b32d245c15df5bcf2418f2f8968`

## 3. Implementation host

The running kernel remains `6.8.0-9001-generic`; boot ID remains `b6e10e21-9737-4ded-ad1e-a437eea41ace`; rollback kernel `6.8.0-136-generic` remains installed. systemd is running, failed units are zero, NTP is synchronized, no reboot is required, dpkg audit is clean, and retained Baby, SSH, and Caddy units are active.

The host-transition checkpoint remains immutable under [`../evidence/checkpoints/host-kernel-transition-20260801/`](../evidence/checkpoints/host-kernel-transition-20260801/).

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

All 35 required negative tests passed using disposable state. Runtime and reserved-machine roots are empty. There is no Cloud Hypervisor process, Z process, guest disk, machine, product Cargo file, new systemd unit, listener, Z TAP, or owned mount. Host APT sources, global package state, global Rust state, kernel, boot policy, and retained services were not changed.

## 7. Claim boundary

This checkpoint proves exact implementation inputs and environment materialization only. It does not prove machine semantics, confinement, SSH control paths, guest persistence, lifecycle recovery, product behavior, compatibility, or certification.

## 8. Phase 0B semantic checkpoint — blocked

Phase 0B semantic and negative gates were executed on 2026-08-01. Native OpenSSH descriptor handoff, strict host-key trust, a connection-scoped libssh2 compatibility relay, exact remote-systemd `argv[]`, binary stdin and separate outputs, lifecycle recovery, cancellation, fail-closed negative states, clean replay, and complete teardown passed.

Certification is withheld because persistence across reboot of the same guest identity did not pass. The reboot transition produced kernel command line `B` and no guest SSH listener. A second run with a fresh UUID, CID, keys, and disk copy proves reproducible non-reboot semantics only.

Checkpoint: [`../evidence/checkpoints/phase-0b-semantic-blocker-20260801/`](../evidence/checkpoints/phase-0b-semantic-blocker-20260801/)

## 9. Next permitted mission

The next permitted mission is a bounded Phase 0B reboot-path repair and recertification only. Phase 1 may not start until the same-machine persistent reboot and authenticated reconnect gate passes. No release is certified and no Z product checkpoint is claimed.
