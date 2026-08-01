# Phase 0B result

**Verdict: not certified — blocked by the persistent guest reboot and authenticated reconnect gate.**

The KVM/Cloud Hypervisor semantic lab passed the non-reboot gates: strict UUID/CID binding, credential injection, zero guest NICs, disabled nested virtualization, native OpenSSH descriptor handoff, a connection-scoped libssh2 compatibility relay, PTY/SFTP/forwarding, exact remote-systemd `argv[]`, binary stdin and separate outputs, lifecycle result recovery, explicit cancellation, fail-closed negative states, clean replay, and complete teardown.

Certification is withheld because the required same-machine persistence gate failed. The reboot transition produced kernel command line `B` and no guest SSH listener. Run 2 used a fresh UUID (`e7abc59b-8f0a-4c46-a412-0c5f18370a5c`), fresh CID (`5002`), fresh keys, and a fresh disk copy; it proves reproducible non-reboot semantics, not persistence across reboot of the original machine identity.

No Phase 1 work was started. No product machine, runtime, or release is claimed. All disposable VMMs, run disks, identities, sockets, helper processes, loop devices, and mounts were removed. The reusable generic image remains at SHA-256 `6ad28bd69f8bcbe8d32281f8e7f66cb11702b80057b75325d84b80bfa06423a3`.
