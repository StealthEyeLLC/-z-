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

`passt` is convenient connectivity, not hostile-code containment. Bridge/TAP, TUN/TAP, and passthrough expand host authority and require separate certification.

## 10. Failure rules

- Unknown is never success.
- Connection loss before exact outcome is unknown/recoverable.
- Missing final output bytes prevent success reporting.
- Cleanup preserves durable data when ownership is ambiguous.
- Read-only inspection never repairs or rotates identity.

## 11. Nonclaims

Z does not claim perfect containment, resistance to host compromise, universal snapshot portability, universal SSH-client compatibility, or confidential-computing protection from a malicious hypervisor.
