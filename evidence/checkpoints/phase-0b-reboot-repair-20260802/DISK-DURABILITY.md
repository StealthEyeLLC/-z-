# Disk Durability

Each run used one writable independent raw disk copy for its complete A-B-C sequence. The disk path and inode remained constant within each run; no backing file, read-only attachment, replacement, or fresh-machine substitution occurred. Root UUID `0b0b0000-0000-4000-8000-000000000004` and ESP UUID `0B0B-0001` remained constant. fsync, directory fsync, and filesystem sync preceded reboot. The marker and the full persistence object set survived both reboots. Clean VMM stop/start independently preserved the same disk inode and state.
