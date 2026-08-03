# Non-mutating post-reboot record-generation anomalies

1. The first comprehensive post-boot read completed all substantive identity, service, package, repository, root, checksum, and zero-residue gates, then exited nonzero because GNU `df` rejects combining inode mode with `--output`. The byte-capacity evidence had already completed; a supported `df --output` form was used in the final record.
2. A follow-up capacity-only read repeated an incompatible `df -P --output` combination before capacity output. No state was changed.
3. The first final-sealing pass completed all live assertions and wrote `POST-REBOOT-HOST.txt`, then exited with status 141 because `journalctl | head` produced SIGPIPE under `pipefail`. The boot-history record was regenerated with `sed`, which consumes the full input, and sealing continued.

These were read/record-generation failures only. They did not alter packages, boot policy, services, networking, guests, implementation artifacts, repository content, or product state.
