# Evidence

Status: **Implementation-host checkpoint present; no Z release is certified.**

This directory holds immutable or digest-verifiable proof for implementation checkpoints and releases. Documentation, mocks, selected dependencies, and planned tests are not evidence that Z works.

## Current checkpoints

- [`checkpoints/host-kernel-transition-20260801/RESULT.md`](checkpoints/host-kernel-transition-20260801/RESULT.md) — verified same-VPS Ubuntu/Noble kernel transition, CVE-2026-53359 fix binding, runtime KVM/AF_VSOCK host primitives, rollback entry, cleanup, and implementation-host tuple.

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
