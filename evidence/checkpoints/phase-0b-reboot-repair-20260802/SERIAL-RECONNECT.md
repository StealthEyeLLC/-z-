# Serial Reconnect

Serial was observational only and never authorized readiness. The old serial connection closed or became unusable during reboot; the harness revalidated the replacement socket and reconnected to the same VMM process. Serial socket inodes changed without creating another VM. Firmware and kernel output were observed after reconnect, but readiness was withheld until strict SSH succeeded three consecutive times on the new boot.

Run 1 connection events:

```text
[2026-08-02T06:42:33.818083+00:00] CONNECT inode=3140 pid=89679 start=4251052
[2026-08-02T06:42:44.570244+00:00] EOF inode=3140
[2026-08-02T06:42:44.771630+00:00] CONNECT inode=3146 pid=89679 start=4251052
[2026-08-02T06:42:53.924901+00:00] EOF inode=3146
[2026-08-02T06:42:54.126651+00:00] CONNECT inode=3152 pid=89679 start=4251052
[2026-08-02T06:43:26.963035+00:00] EOF inode=3152
[2026-08-02T06:43:27.163361+00:00] STOP last_inode=3152
```

Run 2 connection events:

```text
[2026-08-02T06:45:46.428308+00:00] CONNECT inode=3167 pid=90426 start=4270313
[2026-08-02T06:45:56.982480+00:00] EOF inode=3167
[2026-08-02T06:45:57.183201+00:00] CONNECT inode=3173 pid=90426 start=4270313
[2026-08-02T06:46:06.576919+00:00] EOF inode=3173
[2026-08-02T06:46:06.777541+00:00] CONNECT inode=3179 pid=90426 start=4270313
[2026-08-02T06:46:26.281958+00:00] EOF inode=3179
[2026-08-02T06:46:26.482375+00:00] STOP last_inode=3179
```
