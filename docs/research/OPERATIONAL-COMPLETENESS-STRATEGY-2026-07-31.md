# Operational Completeness and Compatible Upgrade Strategy — 2026-07-31

Status: **Non-normative, point-in-time implementation strategy**

Reviewed repository commit: `e0412564182018f1a8b58660e993e8d50bacc494`

This document does not amend the canonical hierarchy. Recommendations become product authority only through `docs/CHANGE-CONTROL.md`, coherent updates to every affected normative document, owner approval, implementation, and certification. Legal, regulatory, dependency, vulnerability, upstream-support, schedule, and cost statements must be revalidated when acted upon.

## 1. Purpose

The architecture is already narrow and coherent. The missing work is operational completeness: proving that the computer remains truthful and recoverable under competing operations, resource exhaustion, interruption, tuple upgrades, host loss, support collection, and optional device authority.

No recommendation in this document authorizes a controller, database, guest agent, custom SSH implementation, hosted dependency, updater daemon, automatic telemetry, or second execution authority.

## 2. Implementation-tool boundary

Baby may be used as implementation infrastructure to edit, build, test, and execute certification procedures for Z, but Baby is not the certification authority and must never be shipped, embedded, installed, required, or represented as a Z component.

The Z GitHub Authority application may manage repository objects and checkpoints, but it is not a Z runtime dependency, owner identity authority, release-verification dependency, product control plane, or offline-operability requirement.

A released Z installation and its offline verifier must function without Baby, GitHub, or any hosted service.

## 3. Baseline operational-failure matrix

The first implementation must test and retain evidence for:

| Failure domain | Required cases | Required outcome |
|---|---|---|
| Competing operations | concurrent create, start, stop, reboot, rename, snapshot, restore, fork, import, delete, and duplicate starts | one mutation authority wins; losers receive truthful bounded results; read-only inspection cannot mutate |
| Storage exhaustion | ENOSPC during image construction, clone, transfer, snapshot, metadata replacement, evidence write, and cleanup | prior durable truth remains; incomplete output is retained or removed by exact ownership; success is impossible |
| Process interruption | SIGTERM, SIGKILL, cgroup kill, OOM, VMM exit, helper exit, and CLI disappearance | lifecycle truth is re-derived; no fabricated success; owned residue is exact |
| Host interruption | abrupt reboot or power loss, suspend/resume, kernel failure, and wall-clock discontinuity | durable state is crash-consistent; time is evidence, never authority by itself |
| Filesystem races | symlink, hard-link, mount, rename, replacement, partial reflink, sparse copy, fsync, and directory-fsync failures | no escape, cross-machine mutation, or silent partial commit |
| Resource pressure | CPU, memory, PID, file descriptor, disk, inode, I/O, socket, CID, unit-name, and temporary-path pressure | fail closed or degrade honestly without identity reuse or corruption |
| Multi-machine pressure | simultaneous starts and transfers across several machines | machine-scoped authority and cleanup remain exact |

Ambiguous state remains retained and inspectable. Unknown is never success.

## 4. Immediate compatible upgrades

### 4.1 Real-hardware certification and immutable evidence

Build certification beside the first usable computer. Every run binds source, tree, binary, host, kernel, CPU, filesystem, dependencies, commands, exits, logs, positive tests, negative tests, cleanup, and human release decision. Evidence is ordinary content-addressed files, not runtime authority.

### 4.2 Offline-verifiable supply chain

Extend the locked tuple with reproducible build comparison, provenance, SBOM, license inventory, advisory disposition, signed release manifest, and offline verification. Hosted CI or transparency services may assist production but cannot be required to run or verify Z locally.

### 4.3 Fail-closed host confinement

Implement exact descriptor inventory, seccomp, Landlock ABI/rights preflight, descriptor-relative path resolution, and negative race tests. Host protection must not be achieved by weakening guest root.

### 4.4 Explicit offline tuple transition and rollback

Provide foreground plan, verify, apply, status, and rollback operations. No updater daemon and no silent machine conversion are permitted. Every transition identifies source and destination tuples, exact assets, disk-space requirements, durable-format impact, rollback boundary, and retained evidence.

### 4.5 Independently restorable backup and disaster recovery

A cold snapshot is not automatically a backup. A backup claim requires an independently stored artifact, manifest, digests, identity policy, and a successful restore on an independently prepared host. Same-computer recovery preserves identity; import-as-new rotates collision-prone identity.

### 4.6 Local support bundle without telemetry

A foreground support command may collect exact local diagnostics into an owner-readable archive. It must preview collection, redact secrets and payloads, never upload, never remain resident, and have no authority over machine state.

### 4.7 Exact device passthrough

The existing VFIO and USB variants should be certified only after the baseline. Certification must cover IOMMU groups, host-driver unbind/rebind, reset behavior, multifunction devices, DMA/interrupt isolation, host-console preservation, crash recovery, and exact absence when disabled.

## 5. Threat-coverage guide

| Adversary or failure | Baseline | Hardened confinement | Encrypted storage | Confidential-computing variant |
|---|---|---|---|---|
| Malicious guest root | isolated by the host/VMM boundary | stronger host path, descriptor, device, and syscall containment | no added running-state protection | hardware-dependent improvement only within the declared threat model |
| Compromised VMM/helper | limited by baseline host confinement | primary software mitigation | disk confidentiality only | partial hardware-backed mitigation |
| Stolen powered-off disk | not necessarily protected | no material change | primary mitigation | depends on key and measurement design |
| Malicious host administrator | not protected | not protected | can usually observe unlocked guest state | addressed only within explicit hardware and attestation limits |
| Compromised host kernel | not protected | Landlock/seccomp do not protect against the kernel | limited | partially addressed only by a proven confidential-computing design |
| Malicious firmware | not protected | not protected | not protected | depends on measured-boot and platform assumptions |
| Supply-chain compromise | pinned tuple and provenance | same | same | larger firmware and hardware supply chain must be included |
| Resource exhaustion or interruption | truthful failure and recovery required | same | same plus key-state handling | same plus attestation/recovery handling |

Sandboxed, encrypted, and confidential are separate claims and must never be collapsed into one marketing statement.

## 6. Recommended order

1. Certification and evidence factory.
2. Supply-chain and vulnerability operations.
3. Host confinement and path safety.
4. Offline update and rollback.
5. Backup and disaster recovery.
6. Native SSH ecosystem and diagnostics.
7. Hardware-backed authentication.
8. Local performance and bounded multiplexing.
9. Virtiofs sharing.
10. Encrypted storage.
11. Device passthrough.
12. Confidential computing.
13. Certified appliance and support business.

The first five are part of operationally completing the baseline, not reasons to delay the first real computer behind a broad framework.

## 7. Schedule and estimate discipline

Any schedule is an analytical range, not a commitment or vendor quotation. A planning record must state team composition, available hardware, supported clients, target variants, certification breadth, regulatory markets, and confidence range.

A reasonable initial planning envelope for a senior five-to-eight-person systems team is:

- 50% confidence: baseline certification in approximately six to nine months;
- 80% confidence: baseline certification in approximately nine to twelve months;
- 50% confidence: selected advanced variants and commercial packaging in approximately eighteen months;
- 80% confidence: the broader program in approximately twenty-four months.

These estimates become invalid if the host platform, product category, VMM, guest-agent prohibition, SSH data plane, supported hardware, compliance geography, or certification scope changes materially.

## 8. Time-sensitive external claims

Regulatory dates, upstream support status, vulnerability state, package availability, and hardware support are non-normative research facts. They must live in dated evidence or research records and be rechecked against primary sources before release or market decisions. Legal applicability requires qualified review; architecture text is not legal advice.

## 9. Change-control record

1. **Current rule:** the frozen corpus defined the computer, lifecycle, identity, SSH, storage, confinement, variants, and release evidence, but did not state one consolidated normative rule for competing mutations, host-capacity exhaustion, explicit tuple transition, independent backup, local support collection, or the current implementation-host profile.
2. **Approved rule:** add machine-scoped mutation authority, crash-safe durable replacement, capacity preflight, foreground offline update and rollback, independently restorable backup, local non-uploading support evidence, an implementation-infrastructure boundary, and exact post-baseline passthrough certification.
3. **Owner-visible capability:** Z can refuse unsafe concurrent or capacity-starved mutation, transition exact tuples explicitly, produce independently restorable backups, and create a local redacted support archive without a service or upload.
4. **Why existing standards are insufficient alone:** Linux files, OpenSSH, systemd, Cloud Hypervisor, and standard backup tools supply primitives, but no single primitive defines Z's cross-primitive machine identity, mutation commit boundary, tuple transition, backup identity policy, or truthful result under interruption.
5. **New process, privilege, state, protocol, dependency, or trust:** no permanent process, custom protocol, hosted dependency, guest component, privilege, or new trust authority is added. Implementation may use an ephemeral machine lock and same-filesystem staging objects. Owner-requested update plans, backup artifacts, support bundles, and evidence are ordinary local files.
6. **Complexity deleted or prevented:** the rules prevent an updater daemon, telemetry collector, support backchannel, durable controller, last-writer-wins metadata, snapshot-as-backup ambiguity, and implementation tooling from becoming product architecture.
7. **Failure and recovery:** prior committed truth remains authoritative until atomic replacement completes; ENOSPC, OOM, interruption, host loss, partial copy, failed synchronization, or failed cleanup cannot report success; ambiguous state is retained; rollback and restore operate only inside declared evidence boundaries.
8. **Certification additions:** `docs/CERTIFICATION.md` Gate Z adds competing-operation, interruption, capacity, offline transition, independent restore, support-redaction, implementation-boundary, and passthrough tests.
9. **Affected documents:** `AGENTS.md`, `README.md`, `FOLDER-TREE.md`, `PACKAGE-VERIFICATION.md`, `SHA256SUMS.txt`, `llms.txt`, `docs/INVARIANTS.md`, `docs/ANTI-INVARIANTS.md`, `docs/SCOPE.md`, `docs/ARCHITECTURE.md`, `docs/VARIANTS.md`, `docs/SECURITY.md`, `docs/DECISIONS.md`, `docs/BUILD.md`, `docs/CERTIFICATION.md`, `docs/CHANGE-CONTROL.md`, discovery indexes and manifest, the implementation-host reference, and this dated strategy.
10. **Owner approval:** the repository owner explicitly approved making all proposed documentation additions and requested a VPS-settings document on `2026-07-31`. This approval covers documentation and governance only; it does not authorize storage deletion, reboot, package or service changes, deployment, or Z runtime implementation.

## 10. Completion rule

Do not create a generic operations framework before the computer works. Implement the smallest mechanisms that prove one real computer, then add only the operational controls required to preserve identity, data, truth, recovery, and owner sovereignty under failure.
