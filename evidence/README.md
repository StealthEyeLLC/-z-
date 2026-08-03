# Evidence

Status: **Implementation-host, Phase 0A, and Phase 0B semantic-lab checkpoints present; no Z release is certified.**

This directory holds immutable or digest-verifiable proof for implementation checkpoints and releases. Documentation, mocks, selected dependencies, and planned tests are not evidence that Z works.

## Current checkpoints

- [`checkpoints/host-kernel-transition-20260801/RESULT.md`](checkpoints/host-kernel-transition-20260801/RESULT.md) — verified same-VPS Ubuntu/Noble kernel transition, CVE-2026-53359 fix binding, runtime KVM/AF_VSOCK host primitives, rollback entry, cleanup, and implementation-host tuple. Repository checkpoint: commit `96853e15f7a8cab1efc178d03a4d3e027b0b28cc`, tree `b4308f82a5329542450de3a4cbfabf3300414068`.
- [`checkpoints/host-maintenance-reboot-20260802/RESULT.md`](checkpoints/host-maintenance-reboot-20260802/RESULT.md) — exactly one later controlled reboot of the retained host, clean boot-boundary proof, reboot-marker consumption, repeated host primitives, checkpoint integrity, and zero Z runtime residue. It is implementation-host maintenance only, not product or release certification.
- [`checkpoints/host-reboot-readback-20260803/RESULT.md`](checkpoints/host-reboot-readback-20260803/RESULT.md) — read-only verification after a subsequent owner-initiated reboot, proving same-host kernel, service, primitive, package-health, and zero-residue continuity.

The checkpoint directory also contains the exact host tuple, environment, tests, source and package hashes, runtime proof, cleanup proof, embedded exact kernel patch, and a checkpoint-local SHA-256 manifest. The complete human operational summary is [`../docs/STATUS.md`](../docs/STATUS.md).

## Required layout

```text
evidence/
  checkpoints/<checkpoint-id>/
    RESULT.md
    TESTS.md
    ENVIRONMENT.md
    SHA256SUMS.txt
  releases/<version>/
    CERTIFICATION.md
    COMPATIBILITY-TUPLE.md
    SHA256SUMS.txt
```

Every result must identify the source commit, source tree, artifact digests, exact environment, commands or equivalent durable operations, exit statuses, positive proofs, negative proofs, cleanup state, and unresolved limitations.

A host checkpoint proves only the claims it names. It does not certify product source, a guest image, a machine lifecycle, or a release.

- `checkpoints/phase-0a-implementation-bootstrap-20260801/` — exact implementation roots, Debian closure, Rust toolchain, Cloud Hypervisor, firmware, capacity, sparse-copy, negative, cleanup, and absence evidence. It is not product or release certification.
- `checkpoints/phase-0b-semantic-blocker-20260801/` — immutable historical blocker evidence.
- `checkpoints/phase-0b-reboot-repair-20260802/` — repaired real-KVM Boot A-B-C identity continuity, strict reconnect, persistence, replay, regressions, 60 negative tests, and exact cleanup. It is semantic-lab certification, not product or release certification.
