# Evidence

Status: **No implementation evidence exists at repository initialization.**

This directory will hold immutable or digest-verifiable proof for implementation checkpoints and releases. Documentation, mocks, and planned tests are not evidence that Z works.

## Proposed layout

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

Every result must identify the source commit, source tree, artifact digests, exact environment, commands executed, exit statuses, positive proofs, negative proofs, cleanup state, and unresolved limitations.
