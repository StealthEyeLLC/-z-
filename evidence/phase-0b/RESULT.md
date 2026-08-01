# Phase 0B Result

Status: **BLOCKED**

The Phase 0B implementation and semantic test suite completed. All **119** executed tests passed, including native OpenSSH descriptor handoff, Dropbear stdio compatibility, static AF_VSOCK `sshd -i`, SMBIOS credential round-trip, strict host identity, exact transient-systemd execution, in-flight connection-loss recovery, serial reconnect across reboot, VMM abrupt loss, fault injection, and zero-residue cleanup.

Release certification is blocked by one external host tuple requirement: the running implementation host is Ubuntu 24.04 LTS kernel `6.8.0-136-generic`, and the preserved Ubuntu CVE authority reports Noble as **Vulnerable, work in progress** for CVE-2026-53359. The locked Debian reference kernel is `6.12.96-1`. No host kernel replacement or reboot was performed.

## Exact identities

- Source commit: `685d7683be9ba60562d3b9eaed663608b8baa5ab`
- Source tree: `eabb67b3d58a2121cb99c6d02fda71c1bc64322c`
- Run: `20260801T072630Z-aa8e85c693f2333c`
- Proof image SHA-256: `c04c1971585c1a2931a5cfa472ef6c9bde1adfaa1757a48a6500742d318ceef0`
- Boot ID before reboot: `988e556c-2b0c-48fe-b64a-2f719ae6527b`
- Boot ID after reboot: `0557cf7d-b014-4207-9b6d-a75d44afebc7`
- Tests: `119 passed / 0 failed`
- Cleanup: pass; no Phase 0B stage, runtime, machine, VMM unit, process, mount, loop, TAP, or socket residue remains.

## Completion rule

Phase 1 is not authorized from this checkpoint. Replace or transition the implementation-host kernel only under explicit authorization, then rerun the host-kernel gate and the complete verifier.
