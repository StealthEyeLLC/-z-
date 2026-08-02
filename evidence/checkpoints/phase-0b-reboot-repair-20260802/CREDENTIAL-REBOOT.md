# Credential Reboot

The same SMBIOS credential configuration remained bound to the same VMM through each orderly reboot. Guest hashes for `ssh.hostkey` and `ssh.authorized_keys` matched their run-specific source hashes on Boots A, B, and C. The host private key, public fingerprint, and owner authorization were constant within a run and unique between runs. No private credential was read from or stored in the generic image, argv, environment, repository evidence, or public logs. `vmm.notify_socket` remained absent.
