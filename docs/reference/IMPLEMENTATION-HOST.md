# OVH VPS Implementation Host Settings

Status: **Point-in-time operational reference; not normative; not certification evidence**

Captured: `2026-07-31T15:20:08Z`
Host label: `vps-c9f04f5e`
Role: shared private implementation host for Baby and Z

## 1. Purpose and disclosure boundary

This document records the sanitized settings and storage state of the OVH VPS selected for Z implementation work. It exists to prevent hidden environmental assumptions and to make host-readiness decisions reviewable.

It deliberately excludes public IP addresses, MAC addresses, credentials, private keys, tokens, encrypted systemd credentials, exact secret-bearing paths, and raw configuration that would create unnecessary attack-surface disclosure. A public repository is not the authority for secrets.

This host profile does not certify Z. A release claim remains bound to the exact host, kernel, CPU exposure, filesystem, VMM, guest, client, dependency, and evidence tuple exercised by `docs/CERTIFICATION.md`.

## 2. Current host identity

| Setting | Observed value |
|---|---|
| Provider role | OVH-hosted KVM VPS |
| Virtualization observed by guest | KVM, full virtualization |
| Distribution | Ubuntu 24.04.4 LTS |
| Architecture | `x86_64` |
| Kernel | `6.8.0-136-generic` |
| systemd | `255.4-1ubuntu8.16` |
| CPU model exposed | Intel Core Processor, Haswell, no TSX |
| vCPUs | 6 |
| NUMA nodes | 1 |
| Memory | 12,243,673,088 bytes |
| Swap | 0 bytes |
| Time zone | UTC |
| NTP synchronized | yes |
| Pending reboot | yes |

## 3. Virtualization and kernel settings

| Setting | Observed value | Z consequence |
|---|---|---|
| `/dev/kvm` | present, character device | nested development tests are possible |
| `/dev/kvm` ownership | `root:kvm`, mode `0660` | selected execution identity must be explicitly authorized |
| Intel nested KVM | `Y` | development-host fact only; baseline certification requires the effective Z guest configuration to prove nested virtualization absent unless separately authorized |
| AMD nested KVM | unavailable | not applicable to this host exposure |
| Landlock LSM | present | exact ABI and relied-upon rights still require runtime preflight |
| AppArmor | enabled | host profile must account for effective policy |
| Kernel lockdown | not active | no Secure Boot or measured-boot claim follows |
| cgroup hierarchy | unified cgroup v2 | compatible with transient systemd ownership |
| IPv4 forwarding | enabled | existing host networking must not be silently treated as Z authority |
| IPv6 forwarding | enabled | same constraint as IPv4 |

Loaded kernel facilities include KVM/KVM-Intel, nftables/netfilter, overlayfs, and the existing host networking modules. Presence is not proof of correct Z confinement or certification.

## 4. Storage and filesystem

| Setting | Observed value |
|---|---|
| Block device | virtual QEMU hard disk |
| Nominal disk size | 107,374,182,400 bytes |
| Root partition | 106,299,375,104 bytes |
| Root filesystem | ext4 1.0 |
| Root mount | `rw,relatime,discard,errors=remount-ro,commit=30` |
| Root filesystem total | 102,888,095,744 bytes |
| Root filesystem used | 102,460,608,512 bytes |
| Root filesystem available | 410,710,016 bytes |
| Reported use | 100% |
| Inode use | 17% |

**Current verdict: the host is storage-blocked for safe Z image construction and certification work.** No large image, clone, snapshot, package, or build operation should begin at this capacity.

### 4.1 Top-level allocated storage

| Path | Approximate allocated bytes | Ownership note |
|---|---:|---|
| `/var` | 53,016,924,160 | mixed Baby, container, SMP, Fix, logs, and package state |
| `/home` | 41,022,210,048 | separate user/application build ownership; not a Z cleanup target by default |
| `/usr` | 4,029,689,856 | operating-system packages |
| `/root` | 2,121,379,840 | administrator-owned state; preserve unless individually proven disposable |
| `/opt` | 1,161,445,376 | installed releases and tools |
| `/tmp` | 1,033,134,080 | mixed temporary build state |

### 4.2 Major `/var` owners

| Path | Approximate allocated bytes | Initial classification |
|---|---:|---|
| `/var/lib/baby-quirt` | 22,257,135,616 | preserve active release, jobs, streams, credentials, and authoritative work; classify workspace-by-workspace |
| `/var/lib/containerd` | 11,368,849,408 | high-value cleanup candidate only after active consumers and snapshots are proven absent |
| `/var/lib/baby-quirt-nspawn` | 9,589,415,936 | high-value candidate only after nspawn evidence and active mounts are reconciled |
| `/var/lib/stealtheye-fix-execution` | 2,974,486,528 | separate project authority; do not delete from a Z cleanup pass |
| `/var/lib/smp` | 2,848,874,496 | separate project assets and persistent machine state; require SMP-specific approval |
| `/var/log` | 1,436,348,416 | journal is about 1.1 GiB and may be bounded through normal retention policy |
| `/var/cache` | 453,226,496 | package/cache cleanup candidate after package operations are idle |

### 4.3 Baby storage

| Area | Approximate allocated bytes |
|---|---:|
| Workspaces | 11,396,947,968 |
| Streams | 147,279,872 |
| Jobs | 9,433,088 |
| Installed Baby release | 48,295,936 |

The largest Baby workspaces are older SMP and EHJINT missions. Size alone is not deletion authority. Every workspace must be checked for origin, HEAD, dirty/staged/untracked state, remote anchoring, retained evidence, active jobs, mounts, and explicit project ownership before removal.

The active Z documentation workspace is small and clean. A separate older Z audit workspace contains uncommitted state and must be preserved until reconciled.

### 4.4 Large logical artifacts

The host contains large sparse or allocated disk images, including:

- a 12 GiB StealthEye Fix execution filesystem;
- a 12 GiB Baby nspawn pool device;
- two 8 GiB SMP root filesystems;
- several 4 GiB SMP build and smoke-test copies;
- containerd blobs and snapshots;
- user-owned CUDA, Python, Rust, browser, and build caches under `/home`.

Logical file size and allocated disk usage are different for sparse files. Cleanup decisions must use allocated size, active mounts, open-file checks, and project ownership rather than filename or apparent size alone.

## 5. Network and firewall shape

- Primary interface: one DHCP-managed Ethernet interface plus loopback.
- Public addresses and MAC addresses are intentionally omitted.
- UFW/nftables effective base policy: input drop, output accept, forward drop.
- Host ingress currently permits SSH, HTTP, and HTTPS.
- Additional project-owned nftables tables exist for StealthEye Fix, SMP, and other host services.
- The host has active forwarding and NAT capability.

Z must never assume ownership of unrelated host firewall tables or existing services. Any Z networking variant must use exact machine-scoped ownership markers, preflight conflicts, and exact cleanup.

## 6. Relevant service state

The host currently runs more than Baby. Active service families include:

- Baby Quirt, its MCP edge, and Baby-X components;
- SMP;
- StealthEye Fix execution, broker, operator, OAuth, and shell services;
- containerd;
- Caddy, SSH, fail2ban, cron, journald, timesync, networkd, and resolver services;
- index and remote-browser worker services;
- ordinary OVH/QEMU guest services.

Baby Quirt is socket activated: its socket is enabled and active; its service is active on demand. Docker is disabled and inactive, while containerd remains enabled and active. Therefore containerd storage is not presumed disposable.

Baby release observed during this capture:

- version `0.1.0`;
- commit `b3a7119fb9321d74fee9a730517f519ed0d351c4`;
- tree `9ebab95f7f136c8480495f812796ac0bdc558a21`.

Baby is an implementation executor only. It is not part of Z, is not shipped with Z, and is not a runtime or release-verification dependency.

## 7. Relevant installed packages

Observed host packages include:

- OpenSSH `9.6p1-3ubuntu13.18`;
- systemd `255.4-1ubuntu8.16`;
- nftables `1.0.9-1build1` and iptables `1.8.10-3ubuntu2`;
- AppArmor `4.0.1really4.0.1-0ubuntu0.24.04.7`;
- cryptsetup `2.7.0-1ubuntu4.2`;
- Git `2.43.0-1ubuntu7.3`;
- rsync `3.2.7-1ubuntu1.5`;
- curl, jq, xz, zstd, FUSE 3, and iproute2.

Cloud Hypervisor, `passt`, and the pinned Rust toolchain are not established as system-package authorities by this snapshot. Z must use the locked candidate assets and exact verification rules rather than inheriting ambient host packages.

## 8. Readiness decision

### 8.1 Suitable uses after storage remediation

This VPS may be used for:

- source editing and deterministic builds;
- dependency and supply-chain verification;
- unit, integration, and negative tests that do not claim bare-metal properties;
- nested-KVM development and smoke tests explicitly labelled as nested;
- evidence generation whose claim is scoped to this exact host profile.

### 8.2 Not automatically suitable for release certification

This host is not the selected Debian 13.6 reference host. It is itself a KVM guest, exposes nested virtualization, has a pending reboot, and currently has insufficient storage headroom. It cannot inherit release-certification authority from successful development tests.

A release certification run must independently prove every Gate A host requirement, including exact kernel security-fix state, effective nested-virtualization absence for the baseline guest, seccomp, Landlock ABI and rights, filesystem behavior, CPU exposure, KVM usability, and sufficient storage.

## 9. Required remediation before Z implementation

1. Produce and approve an exact cleanup manifest; do not delete by age or size alone.
2. Recover enough space for image construction plus bounded failure headroom. The provisional maintenance target is at least 30 GiB free; the implementation must calculate its exact operation-specific requirement.
3. Preserve active Baby releases, credentials, jobs, streams, mounted paths, authoritative evidence, dirty worktrees, and unpushed commits.
4. Reconcile containerd and nspawn consumers before pruning either store.
5. Treat SMP, Fix, Baby-X, EHJINT, and user-home artifacts as separately owned.
6. Complete the pending host reboot in a separately authorized maintenance window and re-capture this profile afterward.
7. Create distinct Z source, build, machine, runtime, cache, and evidence roots with explicit owners, modes, quotas or headroom policy, and cleanup ownership.
8. Re-run the dependency gate and host preflight before the first Z mutation.

## 10. Cleanup classes

### Class A — ordinary bounded maintenance

Potentially reclaimable after confirming no package transaction or active diagnostic need:

- package archives and stale package lists;
- bounded journal retention;
- stale `/tmp` and `/var/tmp` products with proven creators and no open files;
- superseded kernels through normal package-manager removal after boot verification.

### Class B — high-value, proof-required cleanup

- containerd blobs, snapshots, and content;
- Baby nspawn pool state;
- old Baby workspaces;
- duplicate SMP rootfs/build outputs;
- old project build caches and browser artifacts.

These require an ownership and remote/evidence check before deletion.

### Class C — preserve

- active service roots and mounted images;
- Baby release and credential authorities;
- current or dirty workspaces;
- unpushed Git objects;
- retained certification or mission evidence;
- persistent SMP or other project machines;
- any path whose authority is unknown.

Unknown is preserve, not delete.

## 11. Refresh rule

Re-capture and review this document after any host kernel, distribution, hypervisor exposure, CPU profile, filesystem, disk layout, service, firewall, KVM, Landlock, AppArmor, package, reboot, or storage-remediation change. A changed host profile creates new test evidence; it never silently inherits the old profile's claims.
