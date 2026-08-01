# Assets

This directory contains the machine-readable dependency lock and will later contain provenance manifests for materialized Cloud Hypervisor, firmware, base-image, kernel, and helper assets. Large binaries must not be committed casually.

Every certified asset requires an immutable source identity, digest, retrieval or build provenance, license information, and exact compatibility-tuple binding. A mismatched asset must fail closed.

## Dependency lock

`dependencies.lock.json` has two deliberately distinct authorities:

1. `tuple` records the preserved release/reference candidate `z-debian-13.6-amd64-ch53-v1`.
2. `implementation_host` records the verified same-VPS host tuple `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`.

The implementation-host object binds the running Ubuntu kernel, exact CVE-2026-53359 fix, source/package/module digests, boot policy, rollback kernel, runtime primitives, storage facts, and evidence checkpoint. It does not convert the Ubuntu host into the Debian release candidate or certify a Z release.

Phase 0A must verify the lock before materializing any binary, toolchain, firmware, package closure, or build root. Any identity or digest change requires a new tuple rather than silent mutation.
