# Official Dependencies and Initial Candidate Tuple

Status: **Preserved release candidate selected; implementation host verified; release not certified**
Machine-readable authority: [`../../assets/dependencies.lock.json`](../../assets/dependencies.lock.json)
Preserved release candidate tuple: `z-debian-13.6-amd64-ch53-v1`
Verified implementation-host tuple: `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`

## 1. Authority and honesty

This document defines the official direct dependencies, immutable sources, roles, exclusions, and upgrade rules for the first -Z- implementation candidate. The JSON lock contains the exact versions, package records, source locations, sizes, digests, tag identities, repository metadata digests, and configuration-sensitive facts.

This selection does not claim that the tuple works merely because its components are individually valid. Support begins only after the complete positive and negative certification suite passes against these exact identities. Until then the tuple is **candidate, not certified**.

Higher-precedence architecture remains controlling. A dependency cannot authorize a guest agent, custom protocol, permanent controller, product database, weaker host-key policy, attached NIC in Network None, or any other prohibited design.

## 2. Selection result

The first candidate is deliberately one cohesive x86-64 stack:

| Layer | Selected candidate | Why this selection is cohesive |
|---|---|---|
| Reference host | Debian GNU/Linux 13.6 `amd64` | One stable, signed, reproducible package universe for the kernel, systemd, OpenSSH client, `passt`, image tools, and security fixes. |
| Guest | Debian GNU/Linux 13.6 `amd64` | Matches the host's systemd/OpenSSH packaging generation and reduces avoidable interoperability variables. |
| Archive state | Debian Snapshot `20260731T120000Z`, `main` only | Immutable signed metadata; no live mirror, backport, testing, unstable, `contrib`, or `non-free` drift. |
| Host kernel | Debian security `linux-image-amd64` `6.12.96-1` | Stable-series kernel with the required KVM security-fix state for the initial x86 tuple. |
| VMM | Cloud Hypervisor `v53.0`, upstream static x86-64 binary | Current audited release, immutable tag/commit, independently verified release-asset digest, and no runtime shared-library drift. |
| Firmware | Cloud Hypervisor EDK2 `CLOUDHV.fd`, tag `ch-1e1b96f126` | Full ordinary UEFI path for a persistent general-purpose Linux disk; selected over the smaller Rust firmware to preserve the machine capability ceiling. |
| Host/guest service manager | Debian systemd `257.13-1~deb13u1` | Same package generation on both sides; includes the required native systemd facilities without a Z guest service. |
| Host/guest SSH | Debian OpenSSH `1:10.0p1-7+deb13u4` | Patched distribution packages with one package layout and security lifecycle; avoids mixing an upstream client/server tarball with Debian service integration. |
| Networking | Debian `passt` `0.0~git20250503.587980c-2+deb13u1` | Exact package and exact security-sensitive invocation; Network None remains the no-general-IP profile. |
| Z implementation toolchain | Rust `1.97.1`, edition 2024, `x86_64-unknown-linux-gnu` | Current stable compiler manifest, strong systems support, direct Unix descriptor/socket access, and the least speculative path to one auditable binary. |

### 2.1 Verified same-VPS implementation-host tuple

The preserved Debian table above remains the initial release/reference candidate. The actual clean-room implementation host is the retained Ubuntu 24.04.4 OVH VPS and has the distinct tuple `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`. The machine-readable lock stores it under `implementation_host`; the preserved release candidate remains under `tuple`.

The implementation host is bound to:

| Field | Exact value |
|---|---|
| Running kernel | `6.8.0-9001-generic` |
| Kernel package | `6.8.0-9001.1+zcve2026533591` |
| Ubuntu base source | `linux 6.8.0-136.136` |
| CVE fix | `CVE-2026-53359`, commit `81ccda30b4e83d8f5cc4fd50503c44e3a33abfeb` |
| Fix patch SHA-256 | `84d5f450aaff799e1e7cf9392a137cb9afc9702baa3c6c5dbc9343e6d6c05c6c` |
| Source orig SHA-256 | `26512115972bdf017a4ac826cc7d3e9b0ba397d4f85cd330e4e4ff54c78061c8` |
| Source delta SHA-256 | `ccce6d47f36bc749d69a5faa41237c3269e5345d3852d6afe868a5629ac8c316` |
| Source DSC SHA-256 | `9bf54e2fc501c2f37b48d03dc268ef601e911f9be15df5cfb1e5d9f8d6174fba` |
| KVM modules package SHA-256 | `98f184d88d076c5d3458eb921a92a2ebb2c44119b71df3191b9607da13ea88ed` |
| Installed compressed `kvm.ko` SHA-256 | `27c53953087080c7baf9119d62f2e61ef3a81f2faed12eb086359b5cf40580b8` |
| KVM ELF build ID | `1a9bcf21095ea9daa3a8277907a9beddb9274273` |
| Persistent boot default | `6.8.0-9001-generic` |
| Tested rollback entry | `6.8.0-136-generic` |

The controlled reboot, running module binding, KVM API 12, VM/vCPU creation, AF_VSOCK, TAP, descriptor passing, transient systemd, loop, namespaces, Landlock, seccomp, OpenSSH fd-passing, retained services, package health, and cleanup state passed. The exact proof is in [`../../evidence/checkpoints/host-kernel-transition-20260801/RESULT.md`](../../evidence/checkpoints/host-kernel-transition-20260801/RESULT.md).

This host verification does not certify the release tuple. Guest, Cloud Hypervisor, firmware, Rust, Debian snapshot, package closures, networking, persistence, recovery, and ecosystem compatibility remain subject to their later implementation and certification gates. Unchanged selections may be carried forward only after their exact digests and compatibility bindings are reverified.

A newer upstream component is not automatically better for either tuple. Coherence, stable security support, package layout, immutable provenance, and end-to-end certification outweigh mixing the newest release of every independent project.

## 3. Dependency classes

### 3.1 Baseline runtime dependencies

The reference host requires:

- Linux x86-64 with usable KVM.
- Debian 13.6 package state from the locked snapshot.
- The exact host kernel and KVM security-fix state.
- Host systemd for transient machine supervision.
- Debian OpenSSH client for native SSH behavior.
- The pinned Cloud Hypervisor static binary.
- The pinned Cloud Hypervisor EDK2 firmware.
- `passt` only when the connected profile is selected.
- Standard filesystem, process, and cryptographic facilities supplied by the reference distribution.

The Z process is not permitted to substitute a custom daemon for systemd, a custom SSH implementation for OpenSSH, or QEMU for the pinned baseline VMM.

### 3.2 Guest seed dependencies

The guest image is built from the same locked Debian snapshot with `--no-install-recommends`. Its direct seed includes:

- Debian base system and package manager.
- Debian security kernel metapackage.
- systemd, udev, resolved, timesyncd, and D-Bus broker.
- stock OpenSSH client, server, and SFTP server.
- initramfs and ordinary EFI GRUB boot components.
- shell, core utilities, process, module, and network diagnostics.
- CA certificates, `curl`, Git, rsync, compression tools, locale, timezone, and hostname support.

The lock contains the exact direct seed with full package-file records and each complete APT-resolved empty-system closure as sorted `package=version` identities. The locked signed Package-index hashes bind those identities to exact package-file digests without duplicating the archive metadata hundreds of times. Resolution used all Debian Essential packages plus the declared seed with `--no-install-recommends`. Image evidence must record the actual complete `dpkg-query` manifest and prove it matches the locked closure or explain an explicitly approved tuple change.

The image contains no reusable SSH private key, no Z binary, no Z agent, no cloud-init runtime dependency, and no dependency on `systemd-ssh-generator` for the sole access path.

### 3.3 Image-builder dependencies

Image construction uses the locked Debian versions of:

- `mmdebstrap` as the primary root-filesystem constructor.
- Debian archive keys and `gpgv` for metadata verification.
- raw-disk, GPT, EFI, ext filesystem, and inspection tools.
- unsigned ordinary GRUB EFI components; Secure Boot and shim are not part of the initial tuple.
- standard archive, download, Git, compiler, `pkgconf`, seccomp-development, and rsync tools.

`qemu-utils` is an inspection/build dependency. QEMU is not the baseline runtime VMM.

### 3.4 Z source dependencies

Rust `1.97.1` and its signed channel manifest are selected now. No third-party Rust crate is pre-authorized before implementation exists.

When source code begins:

1. `Cargo.lock` becomes the complete source dependency authority.
2. Every crate must serve a concrete implemented capability.
3. Duplicate libraries require written justification.
4. License and advisory review is mandatory.
5. Unused default features must be disabled.
6. A crate upgrade creates a new candidate source lock and repeats affected tests.

This prevents a speculative framework from becoming a dependency before the first real computer boots.

### 3.5 Certification consumers, not runtime dependencies

VS Code Remote SSH, JetBrains Gateway, selected systemd remote tools, SSHFS, and rclone are interoperability consumers. They are not installed as baseline Z runtime dependencies. Each receives an exact version only when its compatibility gate is executed.

## 4. Required configuration binding

Versions alone are insufficient. The tuple also binds these behaviors:

### Cloud Hypervisor

- Private machine-specific API and runtime sockets.
- Effective seccomp and fail-closed filesystem confinement.
- Explicit `nested=off` equivalent with effective CPU verification.
- SMBIOS Type 11 count and encoded-size preflight.
- No use of `vmm.notify_socket` in v53.0 because its Unix vsock mux is stream-only.
- No network device in Network None.

### OpenSSH

- Native descriptor handoff with `ProxyUseFdpass=yes` for the native profile.
- Strict prebound host-key verification.
- Exact dedicated owner identity and no ambient agent.
- Hermetic configuration for internal Z control.
- Stock guest `sshd -i` through static AF_VSOCK socket activation.

### `passt`

The connected profile records and tests the exact pinned-version equivalents of:

```text
--tcp-ports none
--udp-ports none
--map-host-loopback none
--no-map-gw
--map-guest-addr none
```

Sandbox fallback is prohibited. These settings remove convenience mappings and implicit publication, but do not turn `passt` into a destination firewall. Direct reachability to real host addresses remains residual authority that must be measured. Network None is required when no general IP path is acceptable.

## 5. Reproducibility contract

A valid build must:

1. Verify the Debian 13 archive, security, and stable-release key fingerprints listed in the lock.
2. Verify both signed `InRelease` files.
3. Verify the exact package-index digests.
4. Install only from the locked timestamp and components.
5. Verify every downloaded Debian package against its signed package index.
6. Verify Cloud Hypervisor and firmware size and SHA-256 before use.
7. Verify the Rust channel manifest before installing the compiler.
8. Resolve and compare the host, image-builder, and guest package sets against the complete closures already stored in the lock.
9. Record the complete host and guest package states used for certification and the image recipe.
10. Record `Cargo.lock`, compiler verbose identity, final binary digest, base-image digest, and final raw-disk digest.

A live mirror, a floating `latest` URL, a package from another Debian suite, or an asset with a different digest is a different tuple and must fail closed.

## 6. Upgrade policy

There are no in-place silent dependency upgrades.

Any change to Rust, a crate, Debian snapshot, package, kernel, systemd, OpenSSH, Cloud Hypervisor, firmware, `passt`, seccomp behavior, Landlock behavior, host filesystem assumption, or client version creates a new candidate tuple. The new tuple must document the reason, security impact, compatibility impact, changed digests, and certification gates repeated.

A security advisory affecting a selected component blocks release. It does not authorize mutating this lock while retaining the old tuple identity.

## 7. License and supply-chain obligations

- Preserve Rust toolchain MIT/Apache notices.
- Use Cloud Hypervisor's REUSE/SPDX license set at the pinned commit.
- Use the pinned EDK2 tree's license inventory, including component exceptions.
- Preserve Debian package copyright files for the complete resolved closure.
- Produce a release license inventory and SBOM from the final `Cargo.lock` and package manifests.
- Do not ship an asset whose source identity, license record, or digest cannot be proven.

## 8. Recorded limitations

The one-distribution x86-64 scope and absence of Secure Boot, measured boot, and TPM attestation in this initial tuple are recorded in [`../SACRIFICES.md`](../SACRIFICES.md). They are explicit limits, not accidental omissions or universal product restrictions.

## 9. What remains unproved

No release dependency tuple is certified. The implementation-host kernel and applicable KVM fix state are verified, but selection is not release certification.

Implementation must still prove the exact VMM/firmware/guest boot path, SMBIOS binary credentials, static AF_VSOCK `sshd -i`, descriptor handoff, guest-side Landlock rights, `passt` behavior, persistence, reboot, recovery, and ecosystem clients. A failure changes the tuple or implementation—not the evidence standard.
