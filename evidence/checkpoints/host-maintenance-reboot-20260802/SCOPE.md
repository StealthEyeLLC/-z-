# Implementation-host maintenance reboot scope

Status before reboot: **authorized, bounded maintenance gate; no product or release claim**

This checkpoint records exactly one controlled reboot of the retained OVH implementation host after Phase 0B certification. The purpose is to consume the pending `/run/reboot-required` state and prove that the same machine returns on the already-locked `6.8.0-9001-generic` kernel with required control-plane services, implementation roots, Phase 0A inputs, Phase 0B artifacts, and zero Z runtime residue intact.

Allowed mutation: one host reboot and repository-safe evidence/status synchronization after successful return.

Forbidden: package installation, package removal, kernel replacement, GRUB policy change, service reconfiguration, networking/firewall change, Phase 1 work, product source, product machine creation, guest mutation, cleanup of preserved evidence, or release certification.
