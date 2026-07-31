# Security — SSH-Native Z

Status: **Normative threat model and controls**

## 1. Protected assets

- Host files unrelated to the selected machine.
- Host devices and network authority not explicitly delegated.
- Machine disk and durable metadata.
- SSH machine identity and owner credentials.
- VMM/API/runtime socket integrity.
- Truthful lifecycle and command outcome.

## 2. Trusted computing base

The certified baseline trusts the host kernel, KVM, selected systemd/OpenSSH packages, pinned Cloud Hypervisor and firmware, the owner account, and explicitly selected helpers.

The guest is untrusted with respect to the host. Guest root is fully trusted only to control the guest itself.

## 3. Machine identity

- Host key is generated before first connection.
- No TOFU, `accept-new`, or `ssh-keyscan` trust decision.
- Host verification binds the SSH key to the machine UUID, not an IP address.
- Changed or unknown keys fail closed.
- Alias rename does not rotate identity.
- Fork and import-as-new rotate identity.

## 4. Owner authentication

The default uses a dedicated Z owner Ed25519 key whose public half is injected into the guest. The private half remains host-side and is never copied into the guest.

Per-machine keys and hardware-backed keys are supported variants. Agent forwarding is disabled by default.

## 5. Bootstrap secret handling

- Reusable private material is absent from base images.
- Cloud Hypervisor argv and public unit metadata contain no reusable private key.
- Credentials travel through the owner-only local API socket into SMBIOS OEM strings.
- VMM memory and API socket are secret-bearing boundaries.
- Guest root can read its own host key; this is explicit.

## 6. SSH configuration safety

- Reserved aliases use bounded lowercase ASCII grammar.
- Command-bearing directives use an absolute trusted Z path.
- Every helper revalidates the alias.
- No arbitrary metadata is interpolated into shell commands.
- No `Match exec` is required.
- Install validates executable ownership, mode, and parent directories.
- Host-key lookup is read-only.

## 7. Host confinement

The VMM and helpers receive only exact paths, descriptors, sockets, devices, and network authority. The baseline requires effective seccomp and fail-closed Landlock or equivalent certified confinement.

Each certified tuple declares the minimum Landlock ABI and every access right relied upon. It inventories and closes or deliberately retains all file descriptors opened before sandboxing because Landlock does not retroactively restrict them. Unsupported rights, exhausted ruleset layers, or failed confinement are hard failures rather than best-effort degradation.

Managed paths use descriptor-relative operations and `openat2()`-style beneath/no-symlink/no-magic-link resolution where available. PID or pathname alone never proves ownership.

## 8. Portal security

- Forwarding is disabled unless explicitly requested.
- Listeners bind loopback or private Unix paths by default.
- External bind requires explicit authority.
- `ExitOnForwardFailure=yes` proves listener setup only, not destination health.
- Reverse forwarding targets exact host services.
- Durable portals are exact transient units with bounded lifetime.
- Future delegated portal keys use standard SSH restrictions such as `restrict`, `permitopen`, and `permitlisten`.

## 9. Network modes

Network None attaches no virtual NIC. AF_VSOCK SSH remains available.

`passt` is convenient connectivity, not hostile-code containment. The certified connected profile disables host-loopback, gateway, and guest-address convenience mappings, explicitly disables TCP/UDP publication, and fails if the stricter filesystem sandbox cannot be installed. Those controls do not block ordinary outbound connections to services bound on the host's real external addresses. The connected profile must inventory and disclose that residual authority; Network None is the required profile when no general guest-to-host network-service path is acceptable. Bridge/TAP, TUN/TAP, and passthrough expand host authority and require separate certification.

## 9.1 Host-kernel isolation state

The host kernel and KVM are active isolation boundaries. Every certified tuple records the exact host kernel build and relevant security-fix state. For x86 KVM, certification must prove the host is not vulnerable to CVE-2026-53359 (Januscape), including the applicable upstream or distribution fix. Cloud Hypervisor's x86 `nested` CPU option defaults to `on` in current releases, so the baseline MUST set the pinned-version equivalent of `nested=off` explicitly and prove the effective guest CPU exposure. Nested virtualization requires a separate variant and security gate.

## 10. Threat coverage by profile

| Adversary or failure | Baseline | Hardened confinement | Encrypted storage | Confidential-computing variant |
|---|---|---|---|---|
| Malicious guest root | host/VMM boundary is relied upon | stronger path, descriptor, device, and syscall containment | no additional running-state protection | hardware-dependent improvement within a separate threat model |
| Compromised VMM or helper | limited by baseline confinement | primary software mitigation | disk confidentiality only | partial hardware-backed mitigation |
| Stolen powered-off disk | not necessarily protected | unchanged | primary mitigation | depends on key design |
| Malicious host administrator | not protected | not protected | unlocked state is generally observable | addressed only within explicit attestation limits |
| Compromised host kernel | not protected | not protected by Landlock or seccomp | limited | partially addressed only when separately proven |
| Malicious firmware | not protected | not protected | not protected | depends on measured-boot and platform assumptions |
| Supply-chain compromise | exact tuple, provenance, and verification | same | same | enlarged hardware and firmware chain must be included |
| Resource exhaustion or interruption | truthful failure and data preservation | same | same plus key-state handling | same plus attestation and recovery handling |

Sandboxed, encrypted, and confidential are separate claims.

## 11. Operational security

- Competing mutations must have one machine-scoped authority.
- Capacity exhaustion, OOM, signal, host loss, partial copy, failed synchronization, and failed cleanup are security-relevant failure modes because they can corrupt identity or durable truth.
- Update bundles are verified offline and applied only by explicit foreground action.
- A backup is trusted only after manifest verification and independent restore evidence.
- Support bundles are local, declared, redacted, non-uploading, and non-mutating.
- Implementation tools and repository credentials are excluded from release artifacts and runtime authority.

## 12. Failure rules

- Unknown is never success.
- Connection loss before exact outcome is unknown/recoverable.
- Missing final output bytes prevent success reporting.
- Cleanup preserves durable data when ownership is ambiguous.
- Read-only inspection never repairs or rotates identity.

## 13. Nonclaims

Z does not claim perfect containment, resistance to host compromise, universal snapshot portability, universal SSH-client compatibility, or confidential-computing protection from a malicious hypervisor.
