#!/usr/bin/env bash
set -Eeuo pipefail
export LC_ALL=C

usage() {
    cat >&2 <<'USAGE'
usage: check-phase-0a-capacity.sh --root ABSOLUTE_PATH --operation ID \
  --required-bytes N --reserve-bytes N [--available-bytes N] \
  [--minimum-free-inodes N] [--available-inodes N]
USAGE
    exit 64
}

die() {
    printf 'phase-0a-capacity: %s\n' "$*" >&2
    exit 64
}

root=
operation=
required=
reserve=
available_override=
minimum_inodes=0
available_inodes_override=
while (($#)); do
    case "$1" in
        --root) root=${2-}; shift 2 ;;
        --operation) operation=${2-}; shift 2 ;;
        --required-bytes) required=${2-}; shift 2 ;;
        --reserve-bytes) reserve=${2-}; shift 2 ;;
        --available-bytes) available_override=${2-}; shift 2 ;;
        --minimum-free-inodes) minimum_inodes=${2-}; shift 2 ;;
        --available-inodes) available_inodes_override=${2-}; shift 2 ;;
        -h|--help) usage ;;
        *) die "unknown argument: $1" ;;
    esac
done

[[ $root == /* ]] || die '--root must be absolute'
[[ -n $operation ]] || die '--operation is required'
[[ $required =~ ^[0-9]+$ ]] || die '--required-bytes must be an unsigned integer'
[[ $reserve =~ ^[0-9]+$ ]] || die '--reserve-bytes must be an unsigned integer'
[[ $minimum_inodes =~ ^[0-9]+$ ]] || die '--minimum-free-inodes must be an unsigned integer'
[[ -d $root && ! -L $root ]] || die "root is not a real directory: $root"
resolved=$(realpath -e -- "$root")
[[ $resolved == "$root" ]] || die "root resolves outside its declared path: declared=$root resolved=$resolved"

if [[ -n $available_override ]]; then
    [[ $available_override =~ ^[0-9]+$ ]] || die '--available-bytes must be an unsigned integer'
    available=$available_override
    available_source=simulated
else
    available=$(df -B1 --output=avail -- "$root" | awk 'NR==2 {print $1}')
    available_source=filesystem
fi
if [[ -n $available_inodes_override ]]; then
    [[ $available_inodes_override =~ ^[0-9]+$ ]] || die '--available-inodes must be an unsigned integer'
    available_inodes=$available_inodes_override
    inode_source=simulated
else
    available_inodes=$(df --output=iavail -- "$root" | awk 'NR==2 {print $1}')
    inode_source=filesystem
fi

threshold=$((required + reserve))
status=pass
exit_status=0
if ((available < threshold)); then
    status=refused_insufficient_bytes
    exit_status=73
elif ((available_inodes < minimum_inodes)); then
    status=refused_insufficient_inodes
    exit_status=74
fi

printf '{"schema_version":"1.0.0","operation":"%s","root":"%s","required_bytes":%s,"reserve_bytes":%s,"threshold_bytes":%s,"available_bytes":%s,"available_source":"%s","minimum_free_inodes":%s,"available_inodes":%s,"inode_source":"%s","status":"%s"}\n' \
    "$operation" "$root" "$required" "$reserve" "$threshold" "$available" "$available_source" \
    "$minimum_inodes" "$available_inodes" "$inode_source" "$status"
exit "$exit_status"
