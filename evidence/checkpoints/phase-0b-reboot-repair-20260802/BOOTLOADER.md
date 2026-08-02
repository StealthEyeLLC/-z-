# Bootloader

The image uses GRUB through `/EFI/BOOT/BOOTX64.EFI`. There is one primary entry, no alternate or one-shot entry, no boot counting, and an empty `grubenv`. The ESP UUID remained `0B0B-0001`; the root UUID remained `0b0b0000-0000-4000-8000-000000000004`. The repair did not change bootloader bytes or configuration.
