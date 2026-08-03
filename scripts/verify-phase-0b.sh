#!/usr/bin/env bash
set -Eeuo pipefail
export LC_ALL=C
repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
checkpoint=$repo/evidence/checkpoints/phase-0b-reboot-repair-20260802
maintenance=$repo/evidence/checkpoints/host-maintenance-reboot-20260802
base=86c7623277be8734b89dc5bdf874620e33744a26
fail(){ printf 'phase-0b-verify: FAIL: %s\n' "$*" >&2; exit 1; }
pass(){ printf 'phase-0b-verify: PASS: %s\n' "$*"; }
[[ -d $checkpoint && ! -L $checkpoint ]] || fail 'checkpoint missing or linked'
[[ -d $maintenance && ! -L $maintenance ]] || fail 'host-maintenance checkpoint missing or linked'
head=$(git -C "$repo" rev-parse HEAD)
if [[ $head != "$base" ]]; then [[ $(git -C "$repo" rev-parse HEAD^) == "$base" ]] || fail 'checkpoint parent mismatch'; fi
[[ $(git -C "$repo" rev-parse --abbrev-ref HEAD) == build/z-v1-cleanroom ]] || fail 'branch mismatch'
[[ $(git -C "$repo" remote get-url origin) == https://github.com/StealthEyeLLC/-z-.git ]] || fail 'origin mismatch'
( cd "$checkpoint" && sha256sum -c SHA256SUMS.txt >/dev/null ) || fail 'checkpoint checksum mismatch'
( cd "$maintenance" && sha256sum -c SHA256SUMS.txt >/dev/null ) || fail 'host-maintenance checkpoint checksum mismatch'
for cp in phase-0a-implementation-bootstrap-20260801 phase-0b-semantic-blocker-20260801 host-kernel-transition-20260801; do
  ( cd "$repo/evidence/checkpoints/$cp" && sha256sum -c SHA256SUMS.txt >/dev/null ) || fail "$cp checksum mismatch"
done
"$repo/scripts/verify-phase-0a.sh" >/dev/null || fail 'Phase 0A verifier failed'
"$repo/scripts/verify-host-maintenance-reboot.sh" >/dev/null || fail 'host-maintenance verifier failed'
[[ $(uname -r) == 6.8.0-9001-generic ]] || fail 'host kernel mismatch'
vmm=/var/lib/z-implementation/phase-0a-v1/assets/z-debian-13.6-amd64-ch53-v1/cloud-hypervisor-static
fw=/var/lib/z-implementation/phase-0a-v1/assets/z-debian-13.6-amd64-ch53-v1/CLOUDHV.fd
img=/var/lib/z-implementation/phase-0b-v1/lab/disks/probe-generic.raw
[[ $(sha256sum "$vmm" | awk '{print $1}') == 448af3d4e59b22c2987f7df94c213ad40fb53a10d437e42b5ee6c4fce7c29ecc ]] || fail 'VMM digest mismatch'
[[ $(sha256sum "$fw" | awk '{print $1}') == 9fb511fc0dd423d90a79615a90a8ace9b9e078b4a115ea2c459e0ac2f4e60218 ]] || fail 'firmware digest mismatch'
[[ $(sha256sum "$img" | awk '{print $1}') == a6f60c4d3a060305ff710c3bee4f3ee33f11dfcdd4e3ec87d9ebabd17f224697 ]] || fail 'generic image digest mismatch'
python3 - "$checkpoint" <<'PYV'
import json,pathlib,sys
p=pathlib.Path(sys.argv[1])
def j(n): return json.loads((p/n).read_text())
r=j('result.json'); assert r['status']=='pass' and r['phase_0b_status']=='certified'
assert r['phase_1_started'] is False and r['product_machine_created'] is False and r['release_certified'] is False
for rid in ('RUN1','RUN2'):
 d=j(f'SAME-MACHINE-{rid}.json'); assert d['status']=='pass' and len(d['boot_ids'])==3 and len(set(d['boot_ids']))==3
 assert d['identity_continuity_pass'] and d['disk_continuity_pass'] and d['credential_continuity_pass']
 assert d['strict_ssh_after_first_reboot'] and d['strict_ssh_after_second_reboot'] and d['serial_reconnect_pass'] and d['vsock_reconnect_pass']
 boots=[j(f'SAME-MACHINE-{rid}-BOOT-{x}.json') for x in 'ABC']
 assert len({x['boot_id'] for x in boots})==3
 assert len({x['machine_uuid'] for x in boots})==1
 assert len({x['disk_inode'] for x in boots})==1
 assert len({x['host_key_fingerprint'] for x in boots})==1
 assert all(x['kernel_command_line'].startswith('BOOT_IMAGE=') and x['af_vsock_socket_active']=='active' for x in boots)
 assert all(x['failed_unit_count']==0 and x['non_loopback_nic_count']==0 and x['vmx_count']==0 and x['svm_count']==0 and x['guest_dev_kvm']=='absent' for x in boots)
 ps=j(f'PERSISTENCE-{rid}.json'); assert ps['status']=='pass' and ps['boot_B']['status']=='pass' and ps['boot_C']['status']=='pass'
reg=j('PHASE-0B-REGRESSION.json'); assert reg['status']=='pass' and all(reg['security_critical_gates'].values())
neg=j('NEGATIVE-TESTS.json'); assert neg['status']=='pass' and neg['total']==60 and neg['passed']==60 and neg['failed']==0
c=j('FINAL-CLEANUP.json'); assert c['status']=='pass'
for k in ('cloud_hypervisor_process_count','disposable_run_disk_count','private_identity_entry_count','private_key_file_count','implementation_loop_device_count','implementation_mount_count','runtime_entry_count','tap_count'): assert c[k]==0
PYV
[[ $(ps -eo args= | awk -v v="$vmm" '$1==v{n++} END{print n+0}') == 0 ]] || fail 'Cloud Hypervisor process remains'
[[ $(find /var/lib/z-implementation/phase-0b-v1/lab/disks -maxdepth 1 -type f ! -name probe-generic.raw -print -quit | wc -l) == 0 ]] || fail 'disposable run disk remains'
[[ $(find /var/lib/z-implementation/phase-0b-v1/lab/identity -mindepth 1 -print -quit 2>/dev/null | wc -l) == 0 ]] || fail 'private identity remains'
[[ $(find /run/z-implementation/phase-0b-v1 -mindepth 1 -print -quit 2>/dev/null | wc -l) == 0 ]] || fail 'runtime entry remains'
[[ $(losetup -a | grep -Fc /var/lib/z-implementation/phase-0b-v1 || true) == 0 ]] || fail 'loop remains'
[[ $(findmnt -rn | grep -Fc /var/lib/z-implementation/phase-0b-v1 || true) == 0 ]] || fail 'mount remains'
[[ $(ip -o link show | awk -F': ' '$2 ~ /^(tap|ztap)/{n++} END{print n+0}') == 0 ]] || fail 'TAP remains'
[[ ! -e $repo/Cargo.toml && ! -e $repo/Cargo.lock ]] || fail 'root Cargo metadata exists'
[[ -z $(find "$repo/src" -type f ! -name README.md -print -quit) ]] || fail 'product source exists'
[[ -z $(grep -RIl --exclude=SHA256SUMS.txt -- 'BEGIN OPENSSH PRIVATE KEY' "$checkpoint" || true) ]] || fail 'private key in evidence'
[[ -z $(find "$repo" -path "$repo/.git" -prune -o -type f \( -name '*.service' -o -name '*.socket' \) -print -quit) ]] || fail 'permanent unit or listener tracked'
[[ -z $(find "$repo/src" -type f ! -name README.md -print -quit 2>/dev/null) ]] || fail 'guest agent, custom protocol, or other product source present'
pass 'Phase 0B reboot persistence, replay, regressions, negatives, and cleanup'
