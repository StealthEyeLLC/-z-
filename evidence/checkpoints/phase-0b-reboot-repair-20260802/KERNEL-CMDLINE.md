# Kernel Command Line

Boots A, B, and C in both certification runs used this byte-for-byte command line:

```text
BOOT_IMAGE=/boot/vmlinuz-6.12.96+deb13-amd64 root=LABEL=ZROOT ro console=ttyS0,115200n8 console=tty0 systemd.show_status=yes
```

The historical one-character `B` was not a kernel command line. It appeared only in generated JSON while the named raw serial capture had zero bytes. In this checkpoint, "Boot B" names the second real boot and carries the complete line above.
