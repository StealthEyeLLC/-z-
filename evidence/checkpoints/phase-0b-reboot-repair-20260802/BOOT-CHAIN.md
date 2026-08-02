# Boot Chain

Pinned `CLOUDHV.fd` enters the x86_64 UEFI fallback path `/EFI/BOOT/BOOTX64.EFI`. GRUB has one fixed entry and an empty `grubenv`; there is no saved entry, BootNext dependency, boot counting, or writable variable-store requirement. The selected kernel is `/boot/vmlinuz-6.12.96+deb13-amd64`, the initramfs is `/boot/initrd.img-6.12.96+deb13-amd64`, and the root filesystem is resolved by `LABEL=ZROOT` / UUID `0b0b0000-0000-4000-8000-000000000004`.

Boot A, Boot B, and Boot C selected the same loader, entry, kernel, initramfs, and command line. Firmware re-entry was observed without disk replacement.
