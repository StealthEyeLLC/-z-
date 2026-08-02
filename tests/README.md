# Tests

Phase 0A dependency, provenance, root, capacity, sparse-copy, interruption, cleanup, negative, and absence tests are recorded in `../evidence/checkpoints/phase-0a-implementation-bootstrap-20260801/`.

No product test suite exists because Z product source and a durable product machine do not exist. Phase 0B semantic and fail-closed tests are recorded in `../evidence/checkpoints/phase-0b-reboot-repair-20260802/`: real KVM, pinned Cloud Hypervisor and firmware, strict SSH over AF_VSOCK, Boot A-B-C identity continuity, broad persistence, replay, transport/systemd regressions, 60 negative cases, and exact cleanup. Product certification must still exercise the later durable product implementation, confinement, networking, update, backup, and complete release gates.
