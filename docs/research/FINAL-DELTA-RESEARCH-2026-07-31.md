# Final Architecture Delta Research — 2026-07-31

Status: **Canonical dated research audit; non-normative except through the explicit documentation corrections listed below**  
Repository: `StealthEyeLLC/-z-`  
Branch: `main`  
Access date: **2026-07-31**

## 1. Executive result

Final classification: **DOCUMENTATION_CORRECTIONS_ONLY**

The SSH-native architecture remains sound. The research did not justify a new protocol, guest agent, permanent controller, database, network controller, alternate VMM framework, or broader variant catalog.

The pass found four areas where existing wording could permit a false-positive implementation or certification result:

1. systemd's `vmm.notify_socket` cannot operate through the stream-only Cloud Hypervisor v52.0/v53.0 Unix vsock mux.
2. `passt` convenience mappings must be disabled, but current upstream behavior still provides no documented destination filter for services bound on the host's real external addresses; connected mode must disclose that residual authority.
3. The exact host-kernel security state must block known KVM isolation defects, including CVE-2026-53359 on x86, and nested virtualization must not be exposed by the baseline.
4. SMBIOS credential limits and Landlock's ABI/pre-opened-descriptor limits require explicit preflight and negative certification.

These are corrections and tuple qualifications, not changes to the product category or core architecture.

## 2. Scope and method

The audit read the governing hierarchy and supporting research before testing existing assumptions against current upstream manuals, specifications, source, release notes, and security disclosures.

Research was restricted to OpenSSH, systemd, Cloud Hypervisor, Linux/KVM/AF_VSOCK, `passt`, Landlock, VS Code Remote SSH, JetBrains Gateway, and directly relevant security information. Secondary summaries were not used as the basis for normative corrections.

For each material finding, the audit asked whether the claim was confirmed, corrected, qualified, unresolved, or obsolete; whether implementation behavior changed; and whether documentation required modification.

## 3. Exact repository baseline

- Starting commit: `71f861c4d0558670a52f47ee0516afbdb0bf4022`
- Starting tree: `eeddc168c1b4a6b279070ec0eea67234bc09ae83`
- Origin: `https://github.com/StealthEyeLLC/-z-.git`
- Starting workspace: clean
- Starting tracked/untracked changes: none
- Starting ignored work products: none
- Implementation status: not started

## 4. Primary sources reviewed

The audit reviewed **25 upstream primary sources**, plus the exact repository baseline. The complete link ledger is in [SOURCES.md](SOURCES.md).

| Area | Primary source or exact version | Date/version tested | Accessed |
|---|---|---:|---:|
| OpenSSH | Upstream release notes | 10.4/10.4p1, 2026-07-06 | 2026-07-31 |
| OpenSSH | Current OpenBSD `ssh_config(5)` | current manual | 2026-07-31 |
| OpenSSH | Current OpenBSD `sshd(8)` | current manual | 2026-07-31 |
| SSH | RFC 4254 | January 2006 | 2026-07-31 |
| systemd | Credentials | current | 2026-07-31 |
| systemd | VM Interface | current | 2026-07-31 |
| systemd | `systemd.socket(5)` | current | 2026-07-31 |
| systemd | `systemd-stdio-bridge(1)` | current | 2026-07-31 |
| systemd | `systemd-run(1)` | current | 2026-07-31 |
| Cloud Hypervisor | v53.0 release notes | 2026-07-12 | 2026-07-31 |
| Cloud Hypervisor | v52.0 release notes | 2026-05-14 | 2026-07-31 |
| Cloud Hypervisor | v50.0 nested-virtualization default | 2025-12-19 | 2026-07-31 |
| Cloud Hypervisor | v53.0 Unix vsock mux source | tag `v53.0` | 2026-07-31 |
| Cloud Hypervisor | v53.0 SMBIOS source | tag `v53.0` | 2026-07-31 |
| Cloud Hypervisor | Stability policy | current | 2026-07-31 |
| Linux | `vsock(7)` | current | 2026-07-31 |
| Virtio | Virtio 1.3 specification | 1.3 | 2026-07-31 |
| Linux | Landlock userspace API | current | 2026-07-31 |
| KVM | Januscape disclosure | CVE-2026-53359 | 2026-07-31 |
| KVM | Upstream fix | `81ccda30b4e8...` | 2026-07-31 |
| passt | Current `passt(1)` manual | current build | 2026-07-31 |
| passt | Upstream user-list host-address reachability report | 2026-05-04 | 2026-07-31 |
| Microsoft | VS Code Remote SSH | current | 2026-07-31 |
| JetBrains | Gateway SSH workflow | 2026.2 help | 2026-07-31 |
| JetBrains | SSH configurations | 2026.2 help | 2026-07-31 |
| -Z- | Existing architecture and research hierarchy | start tree above | 2026-07-31 |

## 5. Material finding ledger

| Finding | Assumption tested | Result | Implementation impact | Documentation impact | Confidence |
|---|---|---|---|---|---|
| `ProxyUseFdpass=yes` passes a connected descriptor and allows the proxy helper to leave the data path. | Descriptor-handoff native profile. | Confirmed. | Keep the native OpenSSH architecture. | None beyond this audit record. | High |
| OpenSSH command-bearing token expansion is not shell-escaped. | Strict alias grammar and helper revalidation. | Confirmed. | Keep narrow ASCII aliases, absolute executable paths, and repeated validation. | None. | High |
| `KnownHostsCommand` may run repeatedly and nonzero exit aborts the connection. | Read-only prebound host-key projection. | Confirmed. | Keep lookup pure and repeatable. | None. | High |
| SSH `exec` carries a command string, not `argv[]`. | Separate interactive/native-string/exact-systemd execution planes. | Confirmed. | Keep the execution split. | None. | High |
| systemd imports text and binary credentials from SMBIOS Type 11 and exposes service credentials through `$CREDENTIALS_DIRECTORY`. | Zero-agent credential bootstrap. | Confirmed, tuple-bound. | Keep SMBIOS credential bootstrap. | Add exact count/size and binary round-trip gates. | High |
| systemd `vmm.notify_socket` uses AF_VSOCK `SOCK_DGRAM`, then `SOCK_SEQPACKET`. Cloud Hypervisor v52.0/v53.0 rejects non-stream vsock packets. | Optional boot notification through the selected VMM. | Corrected. | Do not configure or depend on this credential for v52.0/v53.0. | Correct invariants, architecture, variants, certification, decisions, and research. | High |
| Cloud Hypervisor v53.0 is newer than the original v52 candidate and contains new security, seccomp, SMBIOS, snapshot, and bug-fix behavior. | “Current Cloud Hypervisor” assumptions. | Qualified. | Treat v53.0 as a new candidate tuple, never inherited certification. | Record current candidate observation. | High |
| Cloud Hypervisor SMBIOS Type 11 count is represented in an 8-bit field and the table is finite. | Credential payload can be accepted without VMM-specific preflight. | Corrected. | Preflight count and encoded size; reject overflow/truncation before launch. | Add build and certification gates. | High |
| AF_VSOCK control does not require guest IP networking; stream connections disconnect on live migration and CIDs may change. | Network-independent control and migration behavior. | Confirmed and qualified. | Keep AF_VSOCK baseline; reconnect and revalidate after migration. | Existing exact migration certification remains sufficient. | High |
| `passt` convenience mappings can be disabled, but current upstream documentation exposes no host-destination filter and the upstream user list records reachability to services bound on real host addresses. | “Conservative host reachability” is sufficient or equivalent to isolation. | Corrected and qualified. | Pin exact no-map, no-publication, and strict-sandbox options; inventory residual reachability; require Network None for no general host-service path. | Update variants, sacrifices, security, decisions, build, compatibility, and certification. | High for mappings; medium-high for residual reachability pending tuple test |
| Landlock does not retroactively restrict file descriptors opened before sandboxing, and rights depend on ABI. | “Landlock available” is sufficient. | Corrected. | Pin minimum ABI/rights and inventory pre-sandbox descriptors. | Tighten security, compatibility, and certification. | High |
| CVE-2026-53359 permits x86 KVM guest-to-host escape through shadow-MMU use-after-free, especially where nested virtualization is exposed; Cloud Hypervisor's x86 `nested` option defaults to `on`. | A minimum kernel version or implicit VMM default is sufficient. | Corrected. | Record exact fix state; explicitly configure and verify `nested=off` in the baseline. | Add security, decision, build, compatibility, and certification gates. | High |
| VS Code Remote SSH uses an OpenSSH-compatible local client and explicit SSH config entries appear in its target list. | Native profile plus inventory compatibility profile. | Confirmed and qualified. | Certify actual client version, server prerequisites, and local-download/offline behavior. | No architecture change. | High |
| JetBrains documents its own SSH configuration UI but does not promise OpenSSH `ProxyUseFdpass` or `KnownHostsCommand` parity. | JetBrains can be assumed native-profile compatible. | Qualified. | Keep JetBrains in the explicit compatibility-inventory certification path until proven. | No architecture change. | High |

## 6. Confirmed assumptions

The following core assumptions remain supported:

- The product is a real persistent KVM Linux computer, not a synthetic command API.
- OpenSSH can own established sessions end to end while Z exits after descriptor handoff.
- Strict prebound host-key verification is compatible with a read-only `KnownHostsCommand`.
- Native SSH command-string semantics and exact non-shell `argv[]` execution must remain separate.
- Static systemd AF_VSOCK socket activation with stock `sshd -i` is a valid candidate design subject to exact distribution/package certification.
- SMBIOS Type 11 system credentials are a valid zero-agent bootstrap mechanism.
- AF_VSOCK control is independent of guest IP networking.
- Network None means no virtual NIC and remains architecturally valid.
- A compatibility inventory plus connection-scoped transparent relay is the honest path for clients that do not implement the native OpenSSH profile.
- No evidence justified a guest agent, custom protocol, permanent controller, database, operation registry, or hidden scheduler.

## 7. Corrections required

### 7.1 Remove unsupported readiness implication

For Cloud Hypervisor v52.0/v53.0, `vmm.notify_socket` is not part of the candidate baseline. The VMM's Unix mux accepts stream traffic while systemd uses datagram and then sequenced-packet sockets. Serial, VMM/API events, and logs may be observational; authenticated SSH remains final readiness authority.

### 7.2 Make `passt` host authority explicit

The connected profile must disable implicit host-loopback, gateway, and guest-address mapping; explicitly set TCP and UDP publication to `none`; and require the strict `pivot_root()` sandbox rather than `--chroot-fallback`.

Those controls do not make `passt` a destination firewall. Direct access to services bound on real host external or wildcard addresses must be tested and recorded as residual authority. Network None is required when no general guest-to-host network-service path is acceptable.

### 7.3 Bind support to security-fix state

An exact kernel version string is insufficient. The tuple records applicable security-fix state, including CVE-2026-53359 on x86. Because Cloud Hypervisor's current x86 nested-virtualization option defaults to `on`, the baseline explicitly sets and verifies `nested=off`.

OpenSSH and Cloud Hypervisor package/source fix state is likewise part of the exact tuple. Version upgrades create new candidates.

### 7.4 Preflight VMM and confinement limits

The implementation must preflight Cloud Hypervisor SMBIOS OEM-string count and encoded size and verify exact binary credential round-trip. It must also identify the minimum Landlock ABI and rights and prove that no descriptor opened before sandboxing retains undeclared host authority.

## 8. Compatibility qualifications

- OpenSSH 10.4/10.4p1 is the current upstream release observed on 2026-07-31. The architecture must not hard-code a stale algorithm list; it must pin patched packages and test current defaults, Linux sandbox behavior, packaging, forwarding, rekey, SFTP, and SCP.
- Cloud Hypervisor v53.0 is the current release observed by the audit. It is a candidate only. Snapshot, live-migration, SMBIOS, seccomp, and vsock behavior must be certified at the exact release and digest.
- systemd credential behavior is version-bound, including SMBIOS import, service isolation, and aggregate credential limits.
- VS Code support requires an exact supported OpenSSH client, remote OS/prerequisites, SFTP/command behavior, and a tested VS Code Server installation path. Network None may require local download and transfer.
- JetBrains support stays in the compatibility profile unless its exact version proves the native OpenSSH directives and discovery behavior.
- A wildcard SSH profile is not the same as client inventory discovery. Explicit generated entries remain required where the client UI enumerates configured hosts.

## 9. Security findings

### 9.1 KVM host escape

CVE-2026-53359 is directly relevant because guest root is unrestricted and the host relies on KVM isolation. Certification must verify the exact host kernel contains the applicable fix or is demonstrably unaffected. Baseline nested virtualization remains disabled.

### 9.2 VMM security cadence

Cloud Hypervisor v52.0 fixed CVE-2026-45782 and multiple guest-triggerable panic paths; v53.0 adds further fixes and behavior changes. Pinning the binary digest remains necessary but is not sufficient without a reviewed security-fix state.

### 9.3 Connected-network authority

`passt` is not a hostile-code containment boundary. Exact no-map/no-publication options remove convenience exposure, but they do not block ordinary outbound access to real host addresses. The connected profile must disclose and test this authority; the Network None profile is the isolation choice.

### 9.4 Filesystem confinement limits

Landlock protects newly mediated access according to its ABI and handled rights. It does not retroactively revoke authority already held through open file descriptors and does not mediate every filesystem-related operation. The certified boundary must combine descriptor discipline, namespace/systemd confinement, seccomp, path-safe operations, and fail-closed Landlock requirements.

## 10. Newly identified implementation risks

1. Cloud Hypervisor's private API and SMBIOS serialization may reject or truncate an over-count or oversized credential set unless Z preflights it.
2. A developer may incorrectly wire `vmm.notify_socket`, wait forever, or treat its absence as a boot failure on the stream-only VMM tuple.
3. A default `passt` invocation may expose host-local services through convenience mappings, and even hardened mapping options may leave real host external addresses reachable.
4. Cloud Hypervisor may expose nested virtualization unless `nested=off` is set explicitly, while an old or distribution-patched kernel may lack the required KVM isolation fix.
5. A process may open host-sensitive files before applying Landlock, retaining authority after sandbox installation.
6. IDE discovery may fail even though a manually entered SSH destination works.
7. VS Code Server or JetBrains backend installation may require network or local-transfer behavior not available in Network None unless explicitly tested.
8. AF_VSOCK streams disconnect across live migration and require identity-preserving reconnect and runtime-socket revalidation.

## 11. Rejected changes

- **Custom readiness protocol or guest notifier:** rejected because authenticated SSH already supplies final readiness and the architecture prohibits a guest agent for this convenience.
- **Switch VMMs solely for `vmm.notify_socket`:** rejected because readiness notification is optional and does not justify lowering or rebuilding the capability baseline.
- **Permanent network controller or firewall manager:** rejected; the connected profile honestly records its residual authority, while Network None and explicit SSH portals provide the strict no-general-network mode without durable machinery.
- **Treat `passt` as containment:** rejected because upstream documents convenience mappings and the project already separates networking from host isolation.
- **Make IDE compatibility the native baseline:** rejected because clients differ in OpenSSH configuration support and discovery behavior.
- **Depend on `systemd-ssh-generator`:** rejected; explicit static socket/service units remain more deterministic for the sole control path.
- **Add generic VMM, distribution, or SSH-client provider interfaces:** rejected until a second concrete certified implementation proves the abstraction.

## 12. Exact documentation files changed

- `FOLDER-TREE.md`
- `PACKAGE-VERIFICATION.md`
- `docs/INDEX.md`
- `docs/MANIFEST.md`
- `docs/INVARIANTS.md`
- `docs/SACRIFICES.md`
- `docs/ARCHITECTURE.md`
- `docs/VARIANTS.md`
- `docs/SECURITY.md`
- `docs/DECISIONS.md`
- `docs/BUILD.md`
- `docs/CERTIFICATION.md`
- `docs/reference/COMPATIBILITY.md`
- `docs/reference/SEARCH-INDEX.md`
- `docs/research/INDEX.md`
- `docs/research/SOURCES.md`
- `docs/research/SSH-RESEARCH-AND-ARCHITECTURE.md`
- `docs/research/FINAL-DELTA-RESEARCH-2026-07-31.md`
- `SHA256SUMS.txt`

No implementation source, test harness, workflow, package manifest, VM image, service, or runtime asset was created.

## 13. Unresolved implementation experiments

The following are implementation gates, not reasons for another broad research pass:

1. Prove exact binary SMBIOS credential round-trip and determine safe count/encoded-size ceilings for the chosen Cloud Hypervisor, firmware, kernel, and systemd tuple.
2. Prove Cloud Hypervisor vsock mux framing, FD handoff, half-close, reboot, concurrency, and stale-socket behavior.
3. Prove the exact static AF_VSOCK `Accept=yes` and `sshd -i` package layout on the selected distribution.
4. Prove the selected host kernel includes the Januscape fix and that the VMM was explicitly started with the pinned-version equivalent of `nested=off`.
5. Prove the selected Landlock ABI/rights and pre-sandbox descriptor closure under the actual systemd transient-unit configuration.
6. Prove the exact Cloud Hypervisor-to-`passt` attachment, no-map/no-publication invocation, residual real-host-address reachability inventory, Network None isolation, and cleanup.
7. Prove VS Code Remote SSH through the native profile, including local server download and transfer in Network None.
8. Prove JetBrains Gateway through the compatibility inventory/relay profile before claiming support.
9. Prove selected remote systemd tools against the exact host/guest systemd tuple.

## 14. Architecture-freeze recommendation

Freeze the architecture after this correction commit.

The remaining uncertainty is empirical and tuple-specific. It belongs in implementation checkpoints and certification evidence, not another open-ended design pass. Research should reopen only when an implementation experiment fails, an upstream security advisory affects the chosen tuple, or a required capability cannot be delivered through the documented standard path.

## 15. Final classification

**DOCUMENTATION_CORRECTIONS_ONLY**

The architecture is ready for implementation. No further broad research pass is required before beginning the first real KVM/OpenSSH checkpoint.
