# Repair

1. Replace `signal()` with `sigaction()` handlers that do not set `SA_RESTART` in the disposable loopback server.
2. Add `TimeoutStopSec=5s` to the loopback fixture unit.
3. Add `SuccessExitStatus=255` to the socket-activated stock `sshd -i` service.
4. Remove the regular `ssh.service` enablement symlink from the generic semantic-lab image.
5. Trigger orderly reboot with `systemctl reboot --no-block` and require three consecutive strict authenticated SSH sessions on the new boot before readiness.
6. Re-stat and revalidate API, vsock, and serial sockets after each reboot; refuse stale inodes and descriptors.

The candidate tuple, Cloud Hypervisor v53.0, firmware, host kernel, guest kernel, initramfs, bootloader, and package closure did not change.
