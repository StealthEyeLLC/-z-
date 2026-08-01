# Decisions — SSH-Native Z

Status: **Normative architectural decision record**

## D001 — Product category

Z is an SSH-native sovereign Linux computer runtime, not a local cloud or command-runner.

## D002 — Primary transport

OpenSSH over Cloud Hypervisor AF_VSOCK is the baseline control and ecosystem surface. Guest IP networking is optional.

## D003 — Descriptor handoff

Native OpenSSH uses `ProxyUseFdpass=yes`; Z exits after passing the connected descriptor.

## D004 — Compatibility profile

Clients without descriptor passing receive explicit inventory entries and a connection-scoped transparent stdio relay. Compatibility is separate and honestly weaker.

## D005 — Static guest SSH

The certified image contains static AF_VSOCK systemd socket units and stock `sshd -i`. Automatic `systemd-ssh-generator` behavior is not the sole control path.

## D006 — Credential bootstrap

Cloud Hypervisor SMBIOS OEM strings supplied through the private VMM API carry systemd credentials. No credential disk is baseline.

## D007 — Identity

Machine UUID plus SSH host key define computer identity. Alias is a label. Restart/rename/restore preserve; fork/import-as-new rotate.

## D008 — Execution split

Interactive PTY behavior is native SSH. Exact argv is noninteractive remote systemd. Explicit shell mode remains separate.

## D009 — Host supervision

Host systemd directly owns the VMM and helpers in transient units. No custom machine supervisor is baseline.

## D010 — Network None

Network None means no virtual NIC. SSH over AF_VSOCK and explicit portals remain available.

## D011 — Capability portals

Standard SSH forwarding is the service-exposure primitive. There is no portal registry or custom tunnel protocol.

## D012 — Storage

The baseline uses independent raw disks with reflink cloning and sparse fallback. Cold snapshots precede live snapshots.

## D013 — Trust

Host keys are prebound; TOFU and silent replacement are rejected.

## D014 — Internal SSH

Z's own control operations use a hermetic SSH configuration and do not inherit ambient owner SSH behavior.

## D015 — Certification tuple

Support attaches to an exact tuple of Z, Cloud Hypervisor, firmware, image, guest kernel, systemd, OpenSSH, helpers, host kernel floor, and host filesystem behavior.

## D016 — Remote and AI access

Any MCP or remote edge invokes the same local Z binary and SSH paths. No second executor or machine database is permitted.

## D017 — Cloud Hypervisor readiness notification boundary

For Cloud Hypervisor v52.0 and v53.0, `vmm.notify_socket` is not a baseline credential because systemd sends readiness over AF_VSOCK datagram or sequenced-packet sockets while the VMM's Unix mux accepts stream traffic only. Authenticated SSH remains the final readiness authority. A later tuple may enable notification only after exact transport certification.

## D018 — No implicit host mapping in the connected profile

The certified `passt` profile disables host-loopback, gateway, and guest-address convenience mappings, explicitly disables inbound TCP/UDP publication, and does not allow sandbox fallback. These controls do not claim to block outbound access to services bound on the host's real external addresses. The connected profile records that residual authority; Network None is required for host-network isolation.

## D019 — Patched host kernel and no baseline nested virtualization

The host kernel and KVM security-fix state are part of every compatibility tuple. The x86 baseline must prove it is not vulnerable to CVE-2026-53359. Because Cloud Hypervisor's x86 `nested` option defaults to `on` in current releases, the baseline explicitly sets `nested=off` (or the exact pinned-version equivalent) and proves the effective configuration. Nested virtualization requires separate authorization and certification.

## D020 — Initial dependency and asset tuple

The first implementation candidate is `z-debian-13.6-amd64-ch53-v1`, defined by `docs/reference/DEPENDENCIES.md` and `assets/dependencies.lock.json`. It uses one signed Debian 13.6 snapshot for the x86-64 reference host and guest, Cloud Hypervisor v53.0's verified static binary, the matching Cloud Hypervisor EDK2 `CLOUDHV.fd` release, Debian's patched kernel/systemd/OpenSSH/`passt` packages, and Rust 1.97.1.

The selection optimizes end-to-end coherence and reproducibility rather than independently maximizing every version number. It is a candidate, not a support claim. Any dependency, package, asset, digest, configuration-sensitive fact, source crate, or snapshot change creates a new tuple and repeats affected certification.

## D021 — Implementation infrastructure is not product architecture

Baby, GitHub applications, CI, build workers, and repository connectors may implement and publish Z but are excluded from the runtime, guest, owner identity, update path, release verifier, and offline-operability contract.

## D022 — Competing operations and interrupted mutations

Each machine has one mutation authority at a time. Coordination is ephemeral rather than a durable controller. Durable replacement is staged, validated, synchronized as required, and atomically installed. Resource exhaustion or interruption cannot report success or erase prior committed truth.

## D023 — Explicit offline tuple transition

Z has no updater daemon. Tuple planning, verification, application, status, rollback, and any persistent-machine migration are explicit foreground operations bound to exact source and destination tuples.

## D024 — Backup requires independent restore

Snapshot and clone are not automatically backup. A backup claim requires an owner-visible export, manifest, digests, identity policy, and successful restoration on an independently prepared host or storage authority.

## D025 — Local support evidence without telemetry

Support collection is a foreground, read-only, redacted local bundle. It uploads nothing and creates no resident collector, metrics service, support listener, or remote authority.

## D026 — Implementation-host profile does not confer certification

The current OVH VPS is a shared implementation host. Its observed settings are recorded in `docs/reference/IMPLEMENTATION-HOST.md`. Successful work on that host is scoped to its exact profile and does not certify the selected Debian reference-host tuple or bare-metal properties.

## D027 — Same-VPS clean-room host transition

The clean-room restart uses the existing OVH VPS. It does not purchase a second server or reimage the current VPS. Ubuntu 24.04, Baby, GitHub authority support, Caddy, SSH, and unrelated retained host state remain in place.

Before Phase 0A, an exact Ubuntu/Noble-compatible kernel containing the applicable CVE-2026-53359 KVM fix is installed side-by-side with `6.8.0-136-generic`. The current kernel remains an intact rollback entry. Provider recovery access, boot selection, package/source/patch/configuration provenance, module set, initramfs, and rollback procedure are verified before reboot. After reboot, certification proves the exact running kernel, loaded KVM modules, KVM API 12, required Z host primitives, zero failed units, and the applicable security-fix state.

That kernel and host state form a new candidate host tuple. The tuple receives a new identity and exact machine-readable lock before release certification; it does not inherit the Debian-host identity `z-debian-13.6-amd64-ch53-v1`. Unchanged guest, VMM, firmware, Rust, and package pins may carry forward only after digest and compatibility verification. Once the host gate passes, Z may proceed at full planned authority on `build/z-v1-cleanroom`. The historical `build/z-v1` branch remains frozen evidence.
