# -Z- — SSH-Native Sovereign Linux Computers

Z is a lifecycle-aware SSH fabric for persistent, unrestricted local Linux computers.

> A Z machine is a real KVM Linux computer with a stable SSH identity, reachable without guest IP networking, and compatible with the ordinary OpenSSH ecosystem.

Canonical repository: `StealthEyeLLC/-z-`  
Product mark: **-Z-**  
Spoken name: **Z**  
CLI: **`z`**

## Current state

This repository contains the complete governing architecture and documentation system. Documentation initialization is complete. The initial Debian-host candidate tuple `z-debian-13.6-amd64-ch53-v1` remains preserved as an unmodified reference candidate and is not certified. The authoritative clean-room restart branch is `build/z-v1-cleanroom`.

The same-VPS host-kernel gate is complete. The retained Ubuntu 24.04 OVH VPS is running verified kernel `6.8.0-9001-generic`, built from Ubuntu Noble `linux 6.8.0-136.136` with the exact CVE-2026-53359 KVM fix. It passed the controlled reboot and runtime KVM/AF_VSOCK host gates, is the persistent boot default, and has the distinct locked implementation-host tuple `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`. Kernel `6.8.0-136-generic` remains installed as the tested rollback entry. The verified checkpoint is commit `96853e15f7a8cab1efc178d03a4d3e027b0b28cc`, tree `b4308f82a5329542450de3a4cbfabf3300414068`. No second server or VPS reimage was used.

**Phase 0A is complete; Phase 0B was executed but is not certified.** The non-reboot semantic gates passed in an isolated KVM/Cloud Hypervisor lab, but the required persistent guest reboot and authenticated reconnect through the same machine identity failed. The blocking checkpoint is [`evidence/checkpoints/phase-0b-semantic-blocker-20260801/`](evidence/checkpoints/phase-0b-semantic-blocker-20260801/). Phase 1 has not started, no product guest or machine exists, and no runtime or release claim is made. The next permitted mission is a bounded Phase 0B reboot-path repair and recertification only. The complete ledger is [`docs/STATUS.md`](docs/STATUS.md).

## Product contract

Z composes KVM, Cloud Hypervisor, OpenSSH, AF_VSOCK, systemd, ordinary files, and narrowly scoped optional helpers. It does not reconstruct Linux as a product API.

The baseline requires:

- unrestricted root inside an ordinary persistent Linux guest;
- OpenSSH over AF_VSOCK as the primary access surface;
- exact non-shell execution through guest-native systemd transient units;
- no Z guest agent or custom guest protocol;
- no product database, permanent controller, or hidden scheduler;
- ordinary raw disks and owner-visible machine directories;
- zero Z processes when all machines are stopped.

## Start here

- [`AGENTS.md`](AGENTS.md) — mandatory entry point for agents and implementers.
- [`docs/INDEX.md`](docs/INDEX.md) — canonical documentation map.
- [`docs/MANIFEST.md`](docs/MANIFEST.md) — document status and purpose.
- [`docs/STATUS.md`](docs/STATUS.md) — complete verified host-transition result, boundaries, maintenance obligations, and recommended next mission.
- [`docs/reference/SEARCH-INDEX.md`](docs/reference/SEARCH-INDEX.md) — aliases and question-to-document lookup.
- [`docs/reference/DEPENDENCIES.md`](docs/reference/DEPENDENCIES.md) — official dependency authority, preserved release candidate, and verified implementation-host binding.
- [`assets/dependencies.lock.json`](assets/dependencies.lock.json) — exact machine-readable release-candidate and implementation-host identities, sources, digests, packages, and configuration bindings.

- [`docs/reference/IMPLEMENTATION-HOST.md`](docs/reference/IMPLEMENTATION-HOST.md) — verified point-in-time OVH implementation-host tuple, kernel/fix binding, boot policy, and readiness.
- [`docs/research/OPERATIONAL-COMPLETENESS-STRATEGY-2026-07-31.md`](docs/research/OPERATIONAL-COMPLETENESS-STRATEGY-2026-07-31.md) — non-normative operational upgrade strategy.
- [`llms.txt`](llms.txt) — compact machine-readable discovery surface.

## Normative precedence

1. [`docs/INVARIANTS.md`](docs/INVARIANTS.md)
2. [`docs/ANTI-INVARIANTS.md`](docs/ANTI-INVARIANTS.md)
3. [`docs/SACRIFICES.md`](docs/SACRIFICES.md)
4. [`docs/SCOPE.md`](docs/SCOPE.md)
5. [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
6. [`docs/VARIANTS.md`](docs/VARIANTS.md)
7. [`docs/SECURITY.md`](docs/SECURITY.md)
8. [`docs/DECISIONS.md`](docs/DECISIONS.md)
9. [`docs/BUILD.md`](docs/BUILD.md)
10. [`docs/CERTIFICATION.md`](docs/CERTIFICATION.md)

Research, reference material, issue templates, tests, and implementation convenience cannot override that order.

## SSH-native architecture in one paragraph

OpenSSH owns established sessions end to end. Native clients use descriptor handoff so Z starts and verifies the computer, connects the Cloud Hypervisor vsock mux, passes the connected descriptor to OpenSSH, and exits from the byte path. A separate transparent stdio compatibility profile supports SSH libraries that cannot accept descriptor passing. Static AF_VSOCK socket activation and stock `sshd -i` provide the guest endpoint. Interactive SSH, exact systemd execution, SFTP, and SSH forwarding remain complementary standard planes rather than a custom guest protocol.

## Repository layout

See [`FOLDER-TREE.md`](FOLDER-TREE.md). The major areas are:

- `docs/` — governing law and architecture.
- `docs/research/` — non-normative research and source ledger.
- `docs/reference/` — glossary, compatibility policy, and search map.
- `evidence/` — digest-verifiable implementation checkpoints and future release evidence.
- `assets/` — future pinned asset manifests and provenance.
- `src/`, `tests/`, `scripts/` — implementation areas, currently intentionally empty except for boundary documentation.
- `.github/` — agent instructions and change templates.
