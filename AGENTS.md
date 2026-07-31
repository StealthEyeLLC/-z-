# Agent Entry Point for -Z-

Canonical repository: `StealthEyeLLC/-z-`  
Product mark: `-Z-`  
Spoken name: `Z`  
CLI: `z`

Z is an SSH-native sovereign local Linux computer runtime. This repository currently contains its governing architecture; implementation capability must never be inferred from documentation alone.

## Required first reads

1. `README.md`
2. `docs/INDEX.md`
3. `docs/MANIFEST.md`
4. `docs/INVARIANTS.md`
5. `docs/ANTI-INVARIANTS.md`
6. `docs/SACRIFICES.md`
7. `docs/SCOPE.md`
8. `docs/ARCHITECTURE.md`
9. `docs/VARIANTS.md`
10. `docs/SECURITY.md`
11. `docs/DECISIONS.md`
12. `docs/BUILD.md`
13. `docs/CERTIFICATION.md`
14. `docs/reference/DEPENDENCIES.md`
15. `assets/dependencies.lock.json`

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

The first checkpoint must boot the real machine, open unrestricted root, persist a filesystem change, reboot, reconnect through authenticated SSH, and preserve the change. Repository structure, interfaces, schemas, protocols, mocks, and placeholder commands are not a product checkpoint.

## Indexing and search

Use `docs/reference/SEARCH-INDEX.md` to map terms or questions to authoritative documents. Use `docs/research/SSH-RESEARCH-AND-ARCHITECTURE.md` only for rationale; it is not higher authority than the normative hierarchy.

## Change rule

Before changing architecture, follow `docs/CHANGE-CONTROL.md`. Any intentional loss of power, isolation, durability, portability, compatibility, or convenience must be recorded in `docs/SACRIFICES.md` before implementation depends on it.
