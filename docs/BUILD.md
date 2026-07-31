# Build Plan — SSH-Native Z

Status: **Normative implementation order**

## Current implementation readiness

Point-in-time host facts are recorded in [`reference/IMPLEMENTATION-HOST.md`](reference/IMPLEMENTATION-HOST.md). They route implementation work and do not certify the selected release tuple.

As of `2026-07-31T20:07:01Z`:

- Z GitHub Authority has repository-wide write/admin authority for `StealthEyeLLC/-z-`, and an ordinary Git temporary branch create/read/delete cycle passed.
- The implementation host has root, usable KVM API version 12, `/dev/vhost-vsock`, AF_VSOCK stream sockets, Unix descriptor passing, transient systemd units, TAP create/delete, loop attach/detach, mount namespaces, and OpenSSH `ProxyUseFdpass=yes` support.
- No additional GitHub or host permission is required to begin Z implementation.
- Repository-level commit and tag signing is intentionally not required. Account-level SSH signing-key registration is outside GitHub App repository authority and is not a build blocker.
- The host has Rust/Cargo `1.88.0`, not the locked Rust `1.97.1`. Cloud Hypervisor, `passt`, `mmdebstrap`, and `qemu-img` are not globally installed.
- Node `24.18.0` is retained as implementation infrastructure for Baby MCP and the Z GitHub App credential helper; global `node`, `npm`, and `npx` resolve into that exact retained runtime.
- The root filesystem is ext4 and does not support reflink. Sparse-copy fallback is therefore the implementation-host baseline.
- The host has `97,421,074,432` bytes available, which is `65,208,819,712` bytes above the provisional 30 GiB maintenance floor. The independent reclamation certification recorded `60,817,604,608` net bytes recovered from its pre-cleanup baseline. Every large image or clone mutation still MUST pass its exact operation-specific capacity and failure-headroom preflight immediately before mutation.
- The authorized controlled host reboot completed successfully. The boot ID changed to `4f39061a-161e-434a-af57-a2554feb2207`, the `libc6` runtime is `2.39-0ubuntu8.8`, `/var/run/reboot-required` is absent, systemd reports zero failed units, and the host profile has been recaptured on the new boot.
- The host is now a certified Baby-plus-Z implementation appliance. Baby Quirt, its socket, its MCP edge, the required `fix-mcp` runtime identity, the Baby-only Caddy route, SSH access, the base operating system, one authoritative Z workspace, and required build/virtualization primitives remain. SMP, the Fix execution/operator/OAuth stack, StealthEye Shell/Quirt/CI, Baby-X, EHJINT, Index, Docker, containerd, and snapd are absent.

Missing ambient binaries are materialization work, not authority blockers. Implementation MUST use the locked candidate tuple and MUST NOT silently inherit global host versions.

## Dependency gate

Before source implementation or asset construction:

1. Verify [`reference/DEPENDENCIES.md`](reference/DEPENDENCIES.md) and [`../assets/dependencies.lock.json`](../assets/dependencies.lock.json) agree.
2. Verify signed Debian snapshot metadata, package-index hashes, Cloud Hypervisor, firmware, and Rust channel-manifest digests.
3. Use candidate tuple `z-debian-13.6-amd64-ch53-v1` without a live-mirror, backport, or floating-version substitution.
4. Treat any version or digest change as a new candidate tuple.
5. Record complete transitive package and Cargo closures when they first exist.

Selection is not certification.

## Phase 0A — implementation bootstrap

Perform this before the first large mutation:

1. Reconfirm the authoritative source commit/tree and a clean workspace.
2. Select and record exact absolute source, build, asset, machine, runtime, cache, staging, and evidence roots, including owner, mode, cleanup authority, and minimum free-space policy.
3. Verify the locked Debian `InRelease`, package indexes, and package closure before installing or extracting anything.
4. Materialize the locked Rust `1.97.1` toolchain in the implementation build root and prove the channel-manifest digest, compiler identity, target, edition, and absence of undeclared crates.
5. Materialize the locked Cloud Hypervisor v53.0 binary and matching EDK2 `CLOUDHV.fd` in the implementation asset root; verify size, digest, executable identity, and immutable source provenance before use.
6. Materialize the locked `mmdebstrap` package and its declared builder closure from the Debian snapshot. Do not substitute the host's `debootstrap` merely because it is already installed.
7. Use independent raw disks and the locked builder closure. `qemu-img` is not an ambient prerequisite and MUST NOT become a dependency without a lock and tuple change.
8. Defer `passt` materialization until the connected profile is implemented. Phase 1 uses Network None and does not require a guest NIC.
9. Detect reflink honestly. On the current host, use sparse-copy fallback and verify logical size, allocated size, contents, interruption behavior, and cleanup.
10. Refuse any operation whose declared temporary space, durable result, rollback copy, evidence, and failure reserve do not fit simultaneously.
11. Keep Baby, GitHub applications, CI workers, repository credentials, and implementation-only tooling outside Z release artifacts, installed files, guest images, runtime authority, and offline operation.

Phase 0A completion means the exact selected inputs and build environment exist and verify. It is not a product checkpoint.

## Phase 0B — semantics gates

1. Prove native OpenSSH descriptor handoff against the Cloud Hypervisor vsock mux.
2. Prove compatibility stdio relay against one embedded SSH client.
3. Prove strict prebound host-key lookup.
4. Prove static AF_VSOCK `sshd -i` service.
5. Prove SMBIOS system credentials through the private VMM API, including OEM-string count/size preflight and exact binary round-trip; do not depend on `vmm.notify_socket` for Cloud Hypervisor v52.0/v53.0.
6. Prove the exact host kernel is patched for applicable KVM isolation advisories, including CVE-2026-53359 on x86; explicitly configure the pinned Cloud Hypervisor x86 equivalent of `nested=off` and prove the effective guest CPU exposure.
7. Prove exact noninteractive systemd argv and result semantics.
8. Prove serial reconnect across reboot.

No architecture scaffold counts as completion without a real booted computer.

## Phase 1 — first usable computer

Implement only:

- exact asset verification;
- recorded implementation-root layout;
- machine-scoped mutation lock and durable staging/commit boundaries;
- machine directory and independent raw disk;
- identity generation;
- Network None guest configuration;
- transient host systemd VMM service;
- fail-closed seccomp/Landlock confinement with exact pre-opened descriptor inventory;
- SMBIOS credentials;
- static guest SSH;
- native descriptor-pass connector;
- bare root shell;
- persistent change;
- guest reboot and authenticated reconnect;
- graceful stop and abrupt VMM recovery;
- zero Z processes at rest.

The implementation order inside this phase is:

1. Create the exact host layout and failure-headroom ledger.
2. Build the deterministic Debian guest image with no reusable machine identity and no Z guest binary.
3. Create one machine directory with UUID, host key, owner authorization, configuration, disk, and crash-safe metadata.
4. Launch the pinned Cloud Hypervisor through one transient systemd unit with `nested=off`, exact assets, private API/vsock/serial sockets, and mandatory confinement.
5. Establish authenticated SSH readiness through the exact prebound host key.
6. Pass the connected vsock descriptor to native OpenSSH and exit Z from the byte path.
7. Create a file, reboot the guest, reconnect, and prove the file and machine identity persist.
8. Stop cleanly, exercise abrupt VMM loss and reconciliation, then prove no Z, VMM, helper, listener, mount, TAP, or runtime-socket residue remains.
9. Run the machine-scoped competing-writer, ENOSPC, OOM, signal, partial-copy, failed-fsync, failed-rename, and obstructed-cleanup tests required by certification.

Checkpoint result:

```text
$ z
root@z:~#
```

A file created before reboot remains afterward.

## Phase 2 — complete local baseline

Add:

- named machines;
- native and compatibility SSH config export/install/remove;
- SFTP copy with durable replacement mode;
- exact systemd execution;
- explicit shell mode;
- status, inspect, doctor, and explicit repair;
- Network None;
- locked `passt` connected profile with `--tcp-ports none`, `--udp-ports none`, convenience host mappings disabled, strict sandbox setup required, and direct host-address reachability inventoried as residual authority;
- cold snapshot, restore, fork, export, and import;
- serial console and logs.

## Phase 3 — SSH power surface

Add one at a time with certification:

- local TCP portals;
- local Unix portals;
- exact reverse portals;
- dynamic SOCKS;
- durable portal transient units;
- VS Code Remote SSH;
- JetBrains compatibility profile;
- Git, rsync, scp, sftp, and selected systemd remote tools;
- optional SSHFS/rclone composition.

## Phase 4 — advanced machine capability

- virtiofs;
- bridge/TAP;
- dedicated host identity;
- additional disks and encryption profiles;
- resource changes;
- VFIO and devices;
- SSH TUN/TAP;
- live snapshots and migration;
- QEMU compatibility only after a concrete need.

## Operational completeness requirements

Before the first large Z mutation on an implementation host:

- capture the sanitized implementation-host profile;
- prove sufficient operation-specific storage and bounded failure headroom;
- resolve pending reboot or package state that would invalidate evidence;
- distinguish nested development evidence from release-certification evidence;
- allocate separate Z source, build, asset, machine, runtime, cache, staging, and evidence roots;
- preserve unrelated project state and never clean by age, prefix, or size alone.

The first usable computer MUST include the smallest machine-scoped mutation coordination and durable staging protocol needed to prevent two writers or an interrupted writer from corrupting identity or disk truth. It MUST test ENOSPC, OOM, signals, abrupt VMM/helper loss, partial copy, failed synchronization, and cleanup obstruction.

The complete local baseline adds:

- foreground offline tuple plan, verify, apply, status, and rollback;
- independently verifiable backup and restoration on a separately prepared host;
- a local non-uploading support bundle with redaction tests;
- exact storage-capacity reporting and refusal before unsafe mutation.

Device passthrough, encrypted storage, virtiofs, confidential computing, and live migration remain separately promoted variants and cannot delay the first real computer.

## Engineering rules

- Full files and deterministic builds.
- Pinned dependency and asset digests.
- No speculative provider interfaces.
- No hidden mutation in inspection.
- Negative tests accompany every authority expansion.
- Stable checkpoints prove complete user-visible behavior.
