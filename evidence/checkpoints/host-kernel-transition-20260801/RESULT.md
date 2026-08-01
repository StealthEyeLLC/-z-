# Same-VPS host-kernel transition result

Status: **PASS — implementation-host gate completed; release certification not claimed**

Checkpoint parent: commit `9a9acc00a165edb1cb86a4f34e8058badfb3f881`, tree `6293a4aff1a3863d96eea45068222ac42f74fcff`.

The existing OVH VPS remains on Ubuntu 24.04.4 LTS. A replacement kernel was built from the exact Ubuntu Noble `linux 6.8.0-136.136` source with upstream KVM fix commit `81ccda30b4e83d8f5cc4fd50503c44e3a33abfeb` for CVE-2026-53359, packaged as `6.8.0-9001.1+zcve2026533591`, installed side-by-side, and selected for one controlled reboot.

The host returned on `6.8.0-9001-generic` with boot ID `b6e10e21-9737-4ded-ad1e-a437eea41ace`. KVM API 12, VM/vCPU creation, AF_VSOCK, TAP, descriptor passing, transient systemd, loop, mount namespaces, Landlock, seccomp, Baby, SSH, Caddy, package health, and zero failed units verified. The built source, package, installed KVM module, and loaded KVM srcversion are digest-bound in this checkpoint.

Kernel `6.8.0-136-generic` remains installed, its pre-transition boot artifacts were unchanged, it had already passed the rollback-preflight boot, and it remains the tested explicit rollback entry. After candidate verification, `6.8.0-9001-generic` was promoted to the persistent GRUB default; the one-time `next_entry` is empty.

The verified implementation-host tuple is `z-impl-ovh-noble-amd64-k6.8.0-9001-januscape-v1`. It is distinct from the preserved Debian guest/reference candidate `z-debian-13.6-amd64-ch53-v1` and does not certify a Z release.

All transition-owned build trees and temporary proof tooling were removed after preserving 13 package outputs, source artifacts, patch evidence, logs, rollback material, and a 208-file durable evidence manifest. The final transition evidence root uses `968,757,248` bytes. At tuple capture, the host had `90,960,056,320` bytes free on `/` and `680,804,352` bytes free on `/boot`.

`build/z-v1` remains unchanged. Clean-room Phase 0A was not started.
