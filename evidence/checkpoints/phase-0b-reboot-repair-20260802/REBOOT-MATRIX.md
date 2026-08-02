# Reboot Matrix

| Variant | Classification | Result |
|---|---|---|
| Guest `systemctl reboot --no-block` | Supported orderly same-machine reboot | Run 1 and replay both passed A-B-C with strict SSH and persistence |
| Historical blocking `systemctl reboot` over socket-activated SSH | Diagnostic | Eventual reboot, but loopback fixture caused a 90-second stop timeout |
| Cloud Hypervisor `vm.reboot` after guest reboot | Abrupt VM-object recreation, not supported orderly contract | Firmware/kernel/config returned; filesystems recovered; stable authenticated readiness failed |
| Guest poweroff plus clean VMM stop/start | Separate lifecycle semantic | New VMM PID/start/sockets; same disk/UUID/CID/key/marker; strict SSH passed |
| Firmware re-entry without disk replacement | Reboot-adjacent proof | Passed on each certified reboot |
