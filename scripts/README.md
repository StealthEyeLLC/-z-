# Scripts

`verify-phase-0a.py` is a read-only verifier for the designated Phase 0A implementation host. It checks repository ancestry, root authority, the signed Debian closure and package cache, the isolated builder root, Rust, runtime assets, filesystem evidence, protected reclamation evidence, protected services, and the maintenance capacity floor.

It is an inspectable verification helper, not a controller, daemon, scheduler, installer, or product API.
