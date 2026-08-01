# Scripts

`verify-phase-0a.py` is a read-only verifier for the designated Phase 0A implementation host. It checks repository ancestry, root authority, the signed Debian closure and package cache, the isolated builder root, Rust, runtime assets, filesystem evidence, protected reclamation evidence, protected services, and the maintenance capacity floor.

It is an inspectable verification helper, not a controller, daemon, scheduler, installer, or product API.

<!-- phase-0b-checkpoint -->
## Phase 0B

The `build-phase-0b-*` scripts materialize isolated proof inputs. `run-phase-0b.py` executes the private proof. `verify-phase-0b.py` validates the committed record and optionally checks the preserved raw evidence tree.
