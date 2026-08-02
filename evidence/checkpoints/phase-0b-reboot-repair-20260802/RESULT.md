# Phase 0B Reboot Repair Result

Status: **PASS - Phase 0B certified; Phase 1 not started; no product machine or release exists.**

The repaired semantic-lab image completed two independent same-machine sequences: Boot A, orderly reboot, Boot B, orderly reboot, Boot C. Strict prebound-host-key SSH, owner authentication, persistent filesystem state, static AF_VSOCK `sshd -i`, serial observation, and fresh socket validation passed after both reboots in both runs.

The confirmed first divergence was guest service shutdown. The disposable loopback forwarding fixture used restarting signal semantics while blocked in `accept4()`, causing a 90-second stop timeout. Stock socket-activated `sshd -i` exit status 255 and an incorrectly enabled regular `ssh.service` also produced false failed-unit state. The historical one-character `B` was not present in the raw serial capture and is classified as an evidence-generation artifact.

The repair uses `sigaction()` without `SA_RESTART`, bounds loopback shutdown to five seconds, accepts stock `sshd -i` status 255, removes the unrelated regular SSH enablement, and treats guest `systemctl reboot --no-block` as the supported orderly reboot contract. The generic test image changed from `6ad28bd69f8bcbe8d32281f8e7f66cb11702b80057b75325d84b80bfa06423a3` to `a6f60c4d3a060305ff710c3bee4f3ee33f11dfcdd4e3ec87d9ebabd17f224697` without changing the candidate, VMM, firmware, kernel, package closure, bootloader, or initramfs tuple.

Run 1 UUID: `725dcc1b-1f18-465b-a12c-07a06b98102c`; Boot IDs: `82243259-fcad-4f11-8dd2-f9fc91457581, 4800bb80-724b-4d00-aa3c-828d402c17b3, bcf942fa-b1ab-403d-8c87-778f462ec4c1`. Run 2 UUID: `4994fc7c-2536-4aa7-9997-9a25a89e5f27`; Boot IDs: `5ab9f437-d4a3-42d7-a772-25215f50a465, 74738c61-1769-46e3-ba52-380bd8642cb4, 562dcb4b-3e40-4b0b-9f0a-2b57003b41cd`. The two runs used distinct UUIDs, CIDs, host keys, owner keys, disks, and runtime paths. Sixty fail-closed negative cases passed. Final Cloud Hypervisor, run-disk, private-identity, loop, mount, runtime-entry, and TAP counts are zero.

Cloud Hypervisor `vm.reboot` remains truthfully distinguished from orderly guest reboot: v53 recreates the VM object from saved configuration, and the tested abrupt reset caused filesystem recovery and unstable readiness. Clean VMM stop/start with the same identity passed separately and is not mislabeled as in-guest reboot.
