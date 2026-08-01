# Agent Entry Point for -Z-

Canonical repository: `StealthEyeLLC/-z-`  
Product mark: `-Z-`  
Spoken name: `Z`  
CLI: `z`

Z is an SSH-native sovereign local Linux computer runtime. This repository contains its governing architecture and a verified implementation-host kernel checkpoint; Z product capability must never be inferred from either documentation or host readiness alone.

## Required first reads

1. `README.md`
2. `docs/INDEX.md`
3. `docs/MANIFEST.md`
4. `docs/STATUS.md`
5. `docs/INVARIANTS.md`
6. `docs/ANTI-INVARIANTS.md`
7. `docs/SACRIFICES.md`
8. `docs/SCOPE.md`
9. `docs/ARCHITECTURE.md`
10. `docs/VARIANTS.md`
11. `docs/SECURITY.md`
12. `docs/DECISIONS.md`
13. `docs/BUILD.md`
14. `docs/CERTIFICATION.md`
15. `docs/reference/DEPENDENCIES.md`
16. `docs/reference/IMPLEMENTATION-HOST.md`
17. `assets/dependencies.lock.json`

Lower-precedence documents, tests, upstream defaults, implementation convenience, or prior chat summaries cannot override higher-precedence law.

## Non-negotiable baseline

- Real KVM Linux computer with unrestricted guest root.
- Persistent ordinary guest filesystem.
- OpenSSH over AF_VSOCK as the native access surface.
- No Z guest agent, custom guest protocol, product database, permanent controller, or hidden scheduler.
- No implicit shell for argument-safe execution.
- Host systemd and guest systemd remain native lifecycle authorities.
- Every machine has a stable, prebound SSH host identity.
- Native fd-passing and stdio compatibility SSH profiles are distinct.
- Network None means no virtual NIC.
- Unknown execution or lifecycle outcome is never reported as success.
- Zero Z processes when all machines are stopped.

## Implementation rule

The verified host-kernel transition is an implementation-host checkpoint, not a product checkpoint. The next mission is Phase 0A only unless the owner explicitly authorizes a later phase. The first product checkpoint must boot the real machine, open unrestricted root, persist a filesystem change, reboot, reconnect through authenticated SSH, and preserve the change. Repository structure, interfaces, schemas, protocols, mocks, and placeholder commands are not a product checkpoint.

## Implementation tooling boundary

Baby may be used as the private implementation executor for Z. Baby must never become part of Z: do not add Baby code, protocol, services, credentials, job records, or runtime assumptions to the product, guest, release verifier, machine state, or offline path.

Use the Z GitHub Authority application for authorized repository verification and Git object transport. It is implementation infrastructure, not product architecture.

When working on the shared OVH host, read `docs/STATUS.md` and `docs/reference/IMPLEMENTATION-HOST.md` first. Reconfirm the locked tuple `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1` before relying on host state. Do not clean storage, reboot, replace either kernel, alter services, packages, networking, firewall, KVM settings, or other project state without a separately authorized, exact maintenance plan.

## Indexing and search

Use `docs/reference/SEARCH-INDEX.md` to map terms or questions to authoritative documents. Use `docs/research/SSH-RESEARCH-AND-ARCHITECTURE.md` only for rationale; it is not higher authority than the normative hierarchy.

## Change rule

Before changing architecture, follow `docs/CHANGE-CONTROL.md`. Any intentional loss of power, isolation, durability, portability, compatibility, or convenience must be recorded in `docs/SACRIFICES.md` before implementation depends on it.
