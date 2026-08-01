# Source

Z product source has not started.

The same-VPS implementation-host gate is complete and recorded in `../docs/STATUS.md`, but Phase 0A has not yet materialized the isolated toolchain or implementation roots. No source should be added before the Phase 0A dependency and capacity checkpoint is complete.

The first product checkpoint must implement the real end-to-end machine path defined by `../docs/BUILD.md`: boot a real KVM computer, open unrestricted root through authenticated SSH over AF_VSOCK, persist a filesystem change, reboot, reconnect, and preserve the change. Scaffolding, provider interfaces, schemas, protocol definitions, or placeholder commands do not satisfy that checkpoint.
