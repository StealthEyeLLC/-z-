# Tests

Tests must map to `../docs/CERTIFICATION.md` and cannot override governing law.

The current evidence proves only the recorded implementation-host kernel transition and host primitives. It does not satisfy Z release certification.

Unit tests may use mocks. Product certification must exercise a real KVM guest, pinned Cloud Hypervisor, authenticated SSH over AF_VSOCK, persistent disks, lifecycle recovery, confinement, and exact cleanup. Negative tests are required, not optional. Phase 0A should test dependency, provenance, root ownership, capacity, sparse-copy, interruption, and cleanup gates without claiming a product checkpoint.
