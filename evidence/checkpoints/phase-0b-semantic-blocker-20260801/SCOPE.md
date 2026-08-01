# Phase 0B checkpoint scope

This checkpoint records an executed but **not certified** Phase 0B semantic lab.

Included:

- the blocking same-machine reboot/reconnect failure;
- the clean replay with a fresh UUID, CID, keys, and disk copy;
- native OpenSSH and connection-scoped libssh2 relay semantics;
- exact remote-systemd argument, environment, stdin, output, status, lifecycle, cancellation, and fail-closed negative gates;
- final disposable-state cleanup.

Excluded:

- Phase 1 work;
- product source, a product guest, or a product machine;
- a runtime service, listener, release, or certification claim;
- private keys, raw OEM credential payloads, disks, sockets, and executor-specific state.

The clean replay proves reproducible non-reboot semantics. It does not prove persistence across reboot of the same guest identity, so Phase 0B remains blocked.
