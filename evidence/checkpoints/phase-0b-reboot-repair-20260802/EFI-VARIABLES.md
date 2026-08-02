# EFI Variables

The selected firmware asset is immutable and was never modified. The image does not depend on persistent NVRAM: it uses the standard fallback loader, has no BootNext or saved-entry requirement, and the EFI System Partition persists on the run disk. No per-machine writable firmware-state file was required. Clean VMM stop/start and both orderly reboot sequences re-entered firmware successfully.
