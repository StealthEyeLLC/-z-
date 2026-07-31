# Tests

Tests must map to `../docs/CERTIFICATION.md` and cannot override governing law.

Unit tests may use mocks. Release certification must exercise a real KVM guest, pinned Cloud Hypervisor, authenticated SSH over AF_VSOCK, persistent disks, lifecycle recovery, confinement, and exact cleanup. Negative tests are required, not optional.
