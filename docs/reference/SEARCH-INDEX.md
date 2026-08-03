# -Z- Search Index

Status: **Discovery aid; not normative authority**

## Project aliases

`-Z-`, `Z`, `z`, `StealthEyeLLC/-z-`, SSH-native computer, sovereign Linux computer, lifecycle-aware SSH, SSH over vsock, AF_VSOCK SSH.

## Question-to-document map

| Search question or phrase | Read first |
|---|---|
| What is Z? | `README.md`, `docs/SCOPE.md` |
| What can never be changed casually? | `docs/INVARIANTS.md`, `docs/ANTI-INVARIANTS.md` |
| Why SSH? | `docs/ARCHITECTURE.md`, `docs/research/SSH-RESEARCH-AND-ARCHITECTURE.md` |
| What changed in the final upstream audit? | `docs/research/FINAL-DELTA-RESEARCH-2026-07-31.md` |
| How does SSH reach a machine without an IP? | `docs/ARCHITECTURE.md`, search `AF_VSOCK`, `vsock mux` |
| Why does Z exit after connection? | Search `ProxyUseFdpass`, `descriptor handoff`, `fd passing` |
| How are IDEs supported? | `docs/VARIANTS.md`, search `compatibility profile`, `stdio relay` |
| How is exact argv preserved? | `docs/INVARIANTS.md`, `docs/ARCHITECTURE.md`, search `exact execution` |
| What does Network None mean? | `docs/DECISIONS.md`, `docs/VARIANTS.md`, search `no virtual NIC` |
| How are host keys and identity handled? | `docs/SECURITY.md`, `docs/DECISIONS.md`, search `prebound`, `host key` |
| How are credentials injected? | `docs/ARCHITECTURE.md`, search `SMBIOS`, `system credentials` |
| What is prohibited? | `docs/ANTI-INVARIANTS.md` |
| What limitations are accepted? | `docs/SACRIFICES.md` |
| What should be built first? | `docs/BUILD.md` |
| What are the official dependencies? | `docs/reference/DEPENDENCIES.md`, `assets/dependencies.lock.json` |
| Which exact versions, packages, sources, and hashes are selected? | `assets/dependencies.lock.json` |
| What proves a release? | `docs/CERTIFICATION.md`, `evidence/README.md` |
| How do I amend architecture? | `docs/CHANGE-CONTROL.md` |
| What is the exact current status? | `docs/STATUS.md` |
| What kernel is running and why was it chosen? | `docs/STATUS.md`, `docs/reference/IMPLEMENTATION-HOST.md`, `docs/DECISIONS.md` |
| What exactly was completed in the host transition? | `docs/STATUS.md`, `evidence/checkpoints/host-kernel-transition-20260801/RESULT.md` |
| What proves the later implementation-host maintenance reboot? | `docs/STATUS.md`, `docs/reference/IMPLEMENTATION-HOST.md`, `evidence/checkpoints/host-maintenance-reboot-20260802/RESULT.md` |
| What proves continuity after the subsequent owner-initiated reboot? | `docs/STATUS.md`, `docs/reference/IMPLEMENTATION-HOST.md`, `evidence/checkpoints/host-reboot-readback-20260803/RESULT.md` |
| What does Phase 0B certify? | `docs/STATUS.md`, `docs/BUILD.md`, `evidence/checkpoints/phase-0b-reboot-repair-20260802/RESULT.md` |
| What should happen next? | `docs/STATUS.md`, `docs/BUILD.md` |
| Is this implemented? | `docs/MANIFEST.md`, `docs/STATUS.md`, `evidence/README.md` |

## High-value keywords

`current status`, `Phase 0A complete`, `Phase 0B certified`, `Phase 1 next`, `host maintenance reboot`, `implementation roots`, `sparse-copy fallback`, `host kernel transition`, `CVE-2026-53359`, `Januscape`, `6.8.0-9001-generic`, `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`, `dependency lock`, `candidate tuple`, `Debian Snapshot`, `Rust 1.97.1`, `Cloud Hypervisor v53.0`, `CLOUDHV.fd`, `OpenSSH`, `ProxyCommand`, `ProxyUseFdpass`, `HostKeyAlias`, `KnownHostsCommand`, `AF_VSOCK`, `vsock-mux`, `sshd -i`, `systemd socket activation`, `SMBIOS Type 11`, `ImportCredential`, `exact argv`, `SFTP`, `capability portal`, `Network None`, `passt`, `virtiofsd`, `Cloud Hypervisor`, `Landlock`, `seccomp`, `raw disk`, `reflink`, `cold snapshot`, `fork identity`, `unknown outcome`, `zero processes at rest`.

## Indexing rule

When adding a new architectural term, capability, or variant, update this file and `docs/MANIFEST.md` in the same change.

## Operational completeness and implementation host

| Question or alias | Read |
|---|---|
| Complete current result, exact checkpoint, maintenance duties, recommended next mission | `../STATUS.md` |
| OVH VPS settings, implementation host, host readiness, maintenance reboot, storage cleanup | `IMPLEMENTATION-HOST.md`, `../../evidence/checkpoints/host-maintenance-reboot-20260802/RESULT.md` |
| competing operations, ENOSPC, OOM, interruption, crash consistency | `../INVARIANTS.md`, `../ARCHITECTURE.md`, `../CERTIFICATION.md` |
| update, rollback, tuple transition, offline bundle | `../VARIANTS.md`, `../BUILD.md`, `../CERTIFICATION.md` |
| backup, disaster recovery, independent restore | `../INVARIANTS.md`, `../VARIANTS.md`, `../CERTIFICATION.md` |
| support bundle, diagnostics, telemetry | `../VARIANTS.md`, `../SECURITY.md`, `../CERTIFICATION.md` |
| Baby boundary, GitHub authority, implementation tooling | `../../AGENTS.md`, `../ARCHITECTURE.md`, `../DECISIONS.md` |
| operational upgrade strategy | `../research/OPERATIONAL-COMPLETENESS-STRATEGY-2026-07-31.md` |

## Phase 0A lookups

- Where are implementation roots defined? [`IMPLEMENTATION-ROOTS.md`](IMPLEMENTATION-ROOTS.md) and [`../../assets/implementation-roots.json`](../../assets/implementation-roots.json).
- Where is Phase 0A proved? [`../../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/`](../../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/).

## Phase 0B and host-maintenance lookups

- Where is Phase 0B semantic-lab certification proved? [`../../evidence/checkpoints/phase-0b-reboot-repair-20260802/`](../../evidence/checkpoints/phase-0b-reboot-repair-20260802/).
- Where is the retained-host maintenance reboot proved? [`../../evidence/checkpoints/host-maintenance-reboot-20260802/`](../../evidence/checkpoints/host-maintenance-reboot-20260802/).
- Where is the later owner-initiated reboot readback proved? [`../../evidence/checkpoints/host-reboot-readback-20260803/`](../../evidence/checkpoints/host-reboot-readback-20260803/).
