#!/usr/bin/env bash
set -Eeuo pipefail
export LC_ALL=C
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
checkpoint=$repo/evidence/checkpoints/host-maintenance-reboot-20260802
followup=$repo/evidence/checkpoints/host-reboot-readback-20260803
base=86c7623277be8734b89dc5bdf874620e33744a26
fail(){ printf 'host-maintenance-verify: FAIL: %s\n' "$*" >&2; exit 1; }
pass(){ printf 'host-maintenance-verify: PASS: %s\n' "$*"; }
[[ -d $checkpoint && ! -L $checkpoint ]] || fail 'checkpoint missing or linked'
[[ -d $followup && ! -L $followup ]] || fail 'follow-up checkpoint missing or linked'
head=$(git -C "$repo" rev-parse HEAD)
if [[ $head != "$base" ]]; then [[ $(git -C "$repo" rev-parse HEAD^) == "$base" ]] || fail 'checkpoint parent mismatch'; fi
[[ $(git -C "$repo" rev-parse --abbrev-ref HEAD) == build/z-v1-cleanroom ]] || fail 'branch mismatch'
[[ $(git -C "$repo" remote get-url origin) == https://github.com/StealthEyeLLC/-z-.git ]] || fail 'origin mismatch'
( cd "$checkpoint" && sha256sum -c SHA256SUMS.txt >/dev/null ) || fail 'checkpoint checksum mismatch'
( cd "$followup" && sha256sum -c SHA256SUMS.txt >/dev/null ) || fail 'follow-up checkpoint checksum mismatch'
python3 - "$checkpoint" <<'PYV'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1])
r=json.loads((p/'result.json').read_text())
assert r['schema_version']=='1.0.0' and r['status']=='pass'
assert r['mission']=='one controlled implementation-host maintenance reboot'
assert r['hostname']=='vps-c9f04f5e'
assert r['machine_id_sha256']=='cd189817b39fea60d338b73878240a6fe7db71374c7a0f35ad60f8eb641e8817'
assert r['machine_id_file_sha256']=='e12bd35a8576ac2dfe2da93c2e827fa3a4efcf4285beecd961adefbe63e08f32'
assert r['pre_boot_id']=='b6e10e21-9737-4ded-ad1e-a437eea41ace'
assert r['post_boot_id']=='68eb2755-8adb-4b54-91c5-8609a0cb1e67' and r['boot_id_changed']
assert r['requested_reboot_count']==1 and r['observed_new_boot_count']==1
assert r['previous_boot_clean_reboot_target'] and r['kernel']=='6.8.0-9001-generic'
assert r['rollback_kernel_installed'] and r['grub_default_unchanged']
assert r['reboot_required_before'] and r['reboot_required_after'] is False
assert r['package_state_clean'] and r['services_recovered'] and r['failed_unit_count']==0
assert r['required_primitives_pass_before'] and r['required_primitives_pass_after'] and r['primitive_residue_zero']
assert r['phase_0a_checkpoint_integrity'] and r['phase_0b_checkpoint_integrity']
assert r['repository_unchanged_during_reboot'] and r['protected_untracked_path_preserved']
assert r['runtime_root_state']=='absent-permitted' and r['z_runtime_residue_zero']
assert r['phase_1_started'] is False and r['product_machine_created'] is False and r['release_certified'] is False
PYV
python3 - "$followup" <<'PYF'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1]); r=json.loads((p/'result.json').read_text())
assert r['status']=='pass' and r['mission']=='read-only verification after later owner-initiated host reboot'
assert r['previous_checkpoint_post_boot_id']=='68eb2755-8adb-4b54-91c5-8609a0cb1e67'
assert r['boot_id_changed_again'] and r['kernel']=='6.8.0-9001-generic'
assert r['package_state_clean'] and r['services_recovered'] and r['required_primitives_pass']
assert r['z_runtime_residue_zero'] and r['phase_1_started'] is False and r['product_machine_created'] is False and r['release_certified'] is False
PYF
[[ $(hostname) == vps-c9f04f5e ]] || fail 'hostname mismatch'
[[ $(printf '%s' "$(cat /etc/machine-id)" | sha256sum | awk '{print $1}') == cd189817b39fea60d338b73878240a6fe7db71374c7a0f35ad60f8eb641e8817 ]] || fail 'machine identity mismatch'
[[ $(sha256sum /etc/machine-id | awk '{print $1}') == e12bd35a8576ac2dfe2da93c2e827fa3a4efcf4285beecd961adefbe63e08f32 ]] || fail 'machine-id file mismatch'
current_boot_id=$(cat /proc/sys/kernel/random/boot_id)
[[ -n $current_boot_id && $current_boot_id != b6e10e21-9737-4ded-ad1e-a437eea41ace ]] || fail 'live boot ID is invalid or pre-maintenance'
[[ $(uname -r) == 6.8.0-9001-generic ]] || fail 'kernel mismatch'
[[ ! -e /var/run/reboot-required && ! -e /var/run/reboot-required.pkgs ]] || fail 'reboot marker returned'
[[ -z $(dpkg --audit) ]] || fail 'dpkg audit not clean'
[[ $(systemctl is-system-running) == running ]] || fail 'systemd not running'
[[ $(systemctl --failed --no-legend --plain | sed '/^[[:space:]]*$/d' | wc -l) == 0 ]] || fail 'failed unit exists'
[[ $(systemctl list-jobs --no-legend | sed '/^[[:space:]]*$/d' | wc -l) == 0 ]] || fail 'systemd job exists'
[[ $(systemctl list-units --all --state=activating,deactivating --no-legend | sed '/^[[:space:]]*$/d' | wc -l) == 0 ]] || fail 'systemd transition exists'
for u in baby-quirt.socket baby-quirt-mcp.service caddy.service ssh.socket; do [[ $(systemctl is-active "$u") == active ]] || fail "$u inactive"; done
for p in linux-image-unsigned-6.8.0-9001-generic linux-modules-6.8.0-9001-generic linux-image-6.8.0-136-generic linux-modules-6.8.0-136-generic; do dpkg --verify "$p" >/dev/null || fail "$p verify failed"; done
grub-script-check /boot/grub/grub.cfg >/dev/null || fail 'GRUB syntax failed'
grep -Fqx 'GRUB_DEFAULT="gnulinux-advanced-d77f6a25-e90f-4292-a85d-9bcc1cecf9e2>gnulinux-6.8.0-9001-generic-advanced-d77f6a25-e90f-4292-a85d-9bcc1cecf9e2"' /etc/default/grub || fail 'GRUB default mismatch'
for token in kvm_create_vm=PASS kvm_create_vcpu=PASS vhost_vsock_get_features=PASS af_vsock_listen=PASS tun_tap_cleanup=PASS scm_rights=PASS landlock_abi=4 transient_systemd=PASS loop_attach_detach=PASS mount_namespace=PASS seccomp=PASS openssh_proxy_use_fdpass=PASS primitive_residue=0; do grep -Fq "$token" "$checkpoint/POST-REBOOT-PRIMITIVES.txt" || fail "primitive token missing: $token"; done
[[ ! -s $checkpoint/POST-REBOOT-PRIMITIVES.stderr ]] || fail 'primitive stderr not empty'
for p in z cloud-hypervisor passt virtiofsd; do [[ $(pgrep -x "$p" 2>/dev/null | wc -l) == 0 ]] || fail "$p process remains"; done
[[ $(findmnt -rn | grep -Ec 'z-implementation|/machines|virtiofs' || true) == 0 ]] || fail 'implementation mount remains'
[[ $(losetup -a | grep -Fc z-implementation || true) == 0 ]] || fail 'implementation loop remains'
[[ $(ip -o link show | awk -F': ' '$2 ~ /^(tap|ztap|zrp)/{n++} END{print n+0}') == 0 ]] || fail 'Z TAP remains'
[[ $(systemctl list-units --all --no-legend 'z-host-maintenance-reboot-20260802.*' | wc -l) == 0 ]] || fail 'reboot transient unit remains'
runtime=/run/z-implementation/phase-0a-v1
if [[ -e $runtime || -L $runtime ]]; then
  [[ -d $runtime && ! -L $runtime && $(realpath -e -- "$runtime") == "$runtime" ]] || fail 'runtime root invalid'
  [[ -z $(find "$runtime" -mindepth 1 -print -quit) ]] || fail 'runtime root not empty'
fi
[[ -z $(find "$repo/src" -type f ! -name README.md -print -quit) ]] || fail 'product source exists'
[[ ! -e $repo/Cargo.toml && ! -e $repo/Cargo.lock ]] || fail 'root Cargo metadata exists'
pass 'historical retained-host reboot evidence and current same-host health, primitives, integrity, and zero residue'
