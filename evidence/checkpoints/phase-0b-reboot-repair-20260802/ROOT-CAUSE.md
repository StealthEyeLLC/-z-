# Root Cause

The first divergent stage was guest service shutdown. `z-phase0b-loopback-server` installed a SIGTERM handler with `signal()` and then blocked in `accept4()`. On this libc/runtime, the call restarted after the signal, so the process never returned to inspect its stop flag. systemd waited its default 90 seconds and killed it.

Two fixture-state defects amplified the result: socket-activated stock `sshd -i` status 255 was treated as failure, and the regular network SSH service was enabled without generic host keys. Neither firmware, EFI variables, GRUB selection, kernel, initramfs, root UUID, disk durability, SMBIOS credentials, CID, nor host-key continuity caused the failure.

The prior `kernel_command_line_observed: "B"` was not supported by raw serial evidence. The corresponding post-API serial file was empty. On every observed actual boot, including repaired Boots A, B, and C, the complete command line was the fixed GRUB line recorded in `KERNEL-CMDLINE.md`.

Cloud Hypervisor `vm.reboot` is an abrupt VM-object recreation, not the supported orderly reboot operation for this design. It re-entered firmware and preserved configuration, but the tested reset dirtied mounted filesystems and failed stable authenticated readiness.
