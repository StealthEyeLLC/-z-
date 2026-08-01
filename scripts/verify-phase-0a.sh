#!/usr/bin/env bash
set -Eeuo pipefail
export LC_ALL=C

repo=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)
roots_json=$repo/assets/implementation-roots.json
lock=$repo/assets/dependencies.lock.json
checkpoint=$repo/evidence/checkpoints/phase-0a-implementation-bootstrap-20260801

fail() { printf 'phase-0a-verify: FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'phase-0a-verify: PASS: %s\n' "$*"; }
[[ -f $roots_json && -f $lock ]] || fail 'root authority or dependency lock missing'
python3 -m json.tool "$roots_json" >/dev/null
python3 -m json.tool "$lock" >/dev/null

readarray -t values < <(python3 - "$roots_json" <<'PY'
import json,sys
x=json.load(open(sys.argv[1]))
r=x['roots']
for key in ('source','durable','build','rust_toolchain','debian_builder','assets','machines_reserved','host_evidence','cache','debian_packages','downloads','staging','runtime'):
    print(r[key]['path'])
PY
)
source_root=${values[0]}; durable=${values[1]}; build=${values[2]}; rust=${values[3]}; builder=${values[4]}; assets=${values[5]}; machines=${values[6]}; host_evidence=${values[7]}; cache=${values[8]}; packages=${values[9]}; downloads=${values[10]}; staging=${values[11]}; runtime=${values[12]}

for p in "$source_root" "$durable" "$build" "$rust" "$builder" "$assets" "$machines" "$host_evidence" "$cache" "$packages" "$downloads" "$staging" "$runtime"; do
    [[ $p == /* && -d $p && ! -L $p ]] || fail "invalid root: $p"
    [[ $(realpath -e -- "$p") == "$p" ]] || fail "root escapes through symlink: $p"
done
[[ -z $(find "$machines" -mindepth 1 -print -quit) ]] || fail 'reserved machine root is not empty'
[[ -z $(find "$runtime" -mindepth 1 -print -quit) ]] || fail 'runtime root is not empty'

ch=$assets/cloud-hypervisor-static
fw=$assets/CLOUDHV.fd
[[ $(stat -c %s "$ch") == 7062256 ]] || fail 'Cloud Hypervisor size mismatch'
[[ $(sha256sum "$ch" | awk '{print $1}') == 448af3d4e59b22c2987f7df94c213ad40fb53a10d437e42b5ee6c4fce7c29ecc ]] || fail 'Cloud Hypervisor digest mismatch'
[[ $(stat -c %U:%G:%a:%h "$ch") == root:root:555:1 && ! -L $ch ]] || fail 'Cloud Hypervisor ownership/mode/link mismatch'
[[ $("$ch" --version | sed -n '1p') == 'cloud-hypervisor v53.0' ]] || fail 'Cloud Hypervisor version mismatch'
[[ $(stat -c %s "$fw") == 4194304 ]] || fail 'firmware size mismatch'
[[ $(sha256sum "$fw" | awk '{print $1}') == 9fb511fc0dd423d90a79615a90a8ace9b9e078b4a115ea2c459e0ac2f4e60218 ]] || fail 'firmware digest mismatch'
[[ $(stat -c %U:%G:%a:%h "$fw") == root:root:444:1 && ! -L $fw ]] || fail 'firmware ownership/mode/link mismatch'

[[ $("$rust/bin/rustc" --version) == rustc\ 1.97.1* ]] || fail 'Rust version mismatch'
[[ $("$rust/bin/cargo" --version) == cargo\ 1.97.1* ]] || fail 'Cargo version mismatch'
[[ $("$rust/bin/rustfmt" --version) == 'rustfmt 1.9.0-stable (8bab26f4f6 2026-07-14)' ]] || fail 'rustfmt identity mismatch'
"$rust/bin/clippy-driver" --version >/dev/null || fail 'clippy-driver unavailable'
[[ $("$rust/bin/rustc" --print sysroot) == "$rust" ]] || fail 'Rust sysroot mismatch'
[[ -z $(find "$rust" \( -name Cargo.toml -o -name Cargo.lock -o -name registry -o -name .git \) -print -quit) ]] || fail 'undeclared Rust state present'

[[ $(chroot "$builder" /usr/bin/mmdebstrap --version) == 'mmdebstrap 1.5.7' ]] || fail 'isolated mmdebstrap mismatch'
count=$(chroot "$builder" /usr/bin/dpkg-query -W -f='${binary:Package}=${Version}\n' | sed 's/:amd64=\([^=]*\)$/=\1/; s/:all=\([^=]*\)$/=\1/' | sort -u | wc -l)
[[ $count == 212 ]] || fail "builder package count mismatch: $count"
python3 - "$lock" "$builder" <<'PY'
import json,subprocess,sys
lock=json.load(open(sys.argv[1]))
expected=sorted(lock['resolved_package_closures']['image_builder_required']['package_versions'])
out=subprocess.check_output(['chroot',sys.argv[2],'/usr/bin/dpkg-query','-W','-f=${binary:Package}=${Version}\n'],text=True)
actual=[]
for line in out.splitlines():
    line=line.replace(':amd64=', '=').replace(':all=', '=')
    actual.append(line)
if sorted(set(actual)) != expected:
    raise SystemExit('builder closure mismatch')
PY

[[ $(pgrep -x cloud-hypervisor-static 2>/dev/null | wc -l || true) == 0 ]] || fail 'Cloud Hypervisor process remains'
[[ -z $(find "$repo/src" -type f ! -name README.md -print -quit) ]] || fail 'Z product source exists'
[[ ! -e $repo/Cargo.toml && ! -e $repo/Cargo.lock ]] || fail 'product Cargo metadata exists'
mapfile -t disk_suffixes < <(find "$durable" -xdev -type f \( -name '*.qcow2' -o -name '*.raw' -o -name '*.img' \) -print | LC_ALL=C sort)
expected_grub_payload="$builder/usr/lib/grub/x86_64-efi/kernel.img"
[[ ${#disk_suffixes[@]} -eq 1 && ${disk_suffixes[0]} == "$expected_grub_payload" ]] || fail 'unexpected guest-disk-like artifact exists'
[[ -d $checkpoint ]] || fail 'repository checkpoint missing'
pass 'isolated Phase 0A inputs and absence gates'
