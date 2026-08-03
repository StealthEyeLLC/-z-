# Pending reboot marker provenance

- `/var/run/reboot-required` and `/var/run/reboot-required.pkgs` were created at `2026-08-01T21:58:37Z`.
- The package-name file contains `dbus-broker`.
- Host `dbus-broker` is not installed; the host uses installed `dbus` `1.14.10-4ubuntu4.1` and `dbus-daemon`.
- `dpkg --audit` is empty, no APT/dpkg lock is held, no package transaction is active, and `needrestart` reports current and expected kernel `6.8.0-9001-generic`.
- Phase 0B evidence records the disposable probe rootfs completing configuration at the same second with Debian `dbus-broker` `37-2`; the host marker is therefore explained as an isolated-rootfs side effect in host `/run`, not a host package installation.
- This maintenance run does not delete or edit the marker. The single controlled reboot consumes `/run` naturally and then verifies that no reboot marker returns.
