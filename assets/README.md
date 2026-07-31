# Assets

This directory will contain manifests and provenance for pinned Cloud Hypervisor, firmware, base-image, kernel, and helper assets. Large binaries should not be committed casually.

Every certified asset requires an immutable source identity, digest, retrieval or build provenance, license information, and exact compatibility-tuple binding. A mismatched asset must fail closed.

## Dependency lock

`dependencies.lock.json` is the exact machine-readable authority for the initial candidate tuple. It records immutable source identities, package records, asset digests, toolchain identity, required configuration, exclusions, and upgrade rules. It does not contain binary assets and does not claim certification.
