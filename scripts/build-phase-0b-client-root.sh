#!/bin/bash
set -euo pipefail
umask 077
RUN_ID=${1:?usage: build-phase-0b-client-root.sh RUN_ID}
if [[ ${2:-} != --private-mount-namespace ]]; then
    exec unshare --mount --propagation private -- "$0" "$RUN_ID" --private-mount-namespace
fi
REPOSITORY=/var/cache/z-implementation/phase-0b/guest-repository
BUILD=/var/lib/z-implementation/build/phase-0b
EVIDENCE=/var/lib/z-implementation/evidence/phase-0b-$RUN_ID/raw
STAGE=$BUILD/certification-client-root.stage
FINAL=$BUILD/certification-client-root
DEV_MOUNTED=false
cleanup(){ set +e; if $DEV_MOUNTED; then umount -R "$STAGE/dev" 2>/dev/null || true; fi; }
trap cleanup EXIT INT TERM HUP
[[ -f $REPOSITORY/guest-closure.json ]]
[[ -f $REPOSITORY/compatibility-closure.json ]]
[[ ! -e $STAGE && ! -e $FINAL ]]
install -d -m 0700 "$STAGE"
mapfile -t guest_files < <(jq -r '.packages|sort_by(.package)|.[].cache_name' "$REPOSITORY/guest-closure.json")
for f in "${guest_files[@]}"; do
    [[ -f $REPOSITORY/packages/$f ]]
    expected=$(jq -r --arg f "$f" '.packages[]|select(.cache_name==$f)|.sha256' "$REPOSITORY/guest-closure.json")
    [[ $(sha256sum "$REPOSITORY/packages/$f" | cut -d' ' -f1) == "$expected" ]]
    dpkg-deb -x "$REPOSITORY/packages/$f" "$STAGE"
done
mapfile -t compatibility_files < <(jq -r '.packages|sort_by(.package)|.[].cache_name' "$REPOSITORY/compatibility-closure.json")
for f in "${compatibility_files[@]}"; do
    [[ -f $REPOSITORY/packages/$f ]]
    expected=$(jq -r --arg f "$f" '.packages[]|select(.cache_name==$f)|.sha256' "$REPOSITORY/compatibility-closure.json")
    [[ $(sha256sum "$REPOSITORY/packages/$f" | cut -d' ' -f1) == "$expected" ]]
    dpkg-deb -x "$REPOSITORY/packages/$f" "$STAGE"
done
install -d -m 0755 "$STAGE/usr/local/libexec/z-phase0b" "$STAGE/dev" "$STAGE/proc" "$STAGE/sys" "$STAGE/run" "$STAGE/tmp"
printf 'root:x:0:0:root:/root:/bin/sh\n' > "$STAGE/etc/passwd"
printf 'root:x:0:\n' > "$STAGE/etc/group"
chmod 0644 "$STAGE/etc/passwd" "$STAGE/etc/group"
install -d -m 0700 "$STAGE/root"
install -m 0755 tools/phase-0b/vsock_connector.py "$STAGE/usr/local/libexec/z-phase0b/vsock_connector.py"
install -m 0755 tools/phase-0b/known_hosts_command.py "$STAGE/usr/local/libexec/z-phase0b/known_hosts_command.py"
mount --rbind /dev "$STAGE/dev"; mount --make-rslave "$STAGE/dev"; DEV_MOUNTED=true
set +e
chroot "$STAGE" /usr/bin/ssh -V > "$EVIDENCE/openssh-client-version.stdout.stage" 2> "$EVIDENCE/openssh-client-version.stderr.stage"; ssh_rc=$?
chroot "$STAGE" /usr/bin/dbclient -V > "$EVIDENCE/dbclient-version.stdout.stage" 2> "$EVIDENCE/dbclient-version.stderr.stage"; db_rc=$?
set -e
[[ $ssh_rc -eq 0 ]]
grep -aF 'OpenSSH_10.0p2 Debian-7+deb13u4' "$EVIDENCE/openssh-client-version.stdout.stage" "$EVIDENCE/openssh-client-version.stderr.stage" >/dev/null
grep -aE '2025\.89|Dropbear' "$EVIDENCE/dbclient-version.stdout.stage" "$EVIDENCE/dbclient-version.stderr.stage" >/dev/null
umount -R "$STAGE/dev"; DEV_MOUNTED=false
install -d -m 0755 "$STAGE/dev"
for n in ssh_host_ed25519_key id_ed25519; do [[ ! -e $STAGE/etc/ssh/$n && ! -e $STAGE/root/.ssh/$n ]]; done
find "$STAGE" -xdev -type f -printf '%P\0' | LC_ALL=C sort -z | while IFS= read -r -d '' f; do sha256sum --tag "$STAGE/$f"; done > "$EVIDENCE/certification-client-root-files.sha256.stage"
tree_sha=$(sha256sum "$EVIDENCE/certification-client-root-files.sha256.stage" | cut -d' ' -f1)
logical=$(du -sb "$STAGE" | cut -f1)
compat_sha=$(sha256sum "$REPOSITORY/compatibility-closure.json" | cut -d' ' -f1)
guest_sha=$(sha256sum "$REPOSITORY/guest-closure.json" | cut -d' ' -f1)
openssh=$(cat "$EVIDENCE/openssh-client-version.stderr.stage" "$EVIDENCE/openssh-client-version.stdout.stage" | tr '\n' ' ' | sed 's/[[:space:]]*$//')
dropbear=$(cat "$EVIDENCE/dbclient-version.stderr.stage" "$EVIDENCE/dbclient-version.stdout.stage" | tr '\n' ' ' | sed 's/[[:space:]]*$//')
jq -n \
  --arg purpose phase-0b-certification-consumers-only \
  --arg openssh "$openssh" \
  --arg dropbear "$dropbear" \
  --arg guest_closure_sha256 "$guest_sha" \
  --arg compatibility_closure_sha256 "$compat_sha" \
  --arg tree_manifest_sha256 "$tree_sha" \
  --argjson logical "$logical" \
  --argjson guest_packages "${#guest_files[@]}" \
  --argjson compatibility_packages "${#compatibility_files[@]}" \
  --argjson openssh_version_exit "$ssh_rc" \
  --argjson dbclient_version_exit "$db_rc" \
  '{schema_version:"1.0.0",purpose:$purpose,openssh_version:$openssh,dropbear_version:$dropbear,guest_closure_sha256:$guest_closure_sha256,compatibility_closure_sha256:$compatibility_closure_sha256,tree_manifest_sha256:$tree_manifest_sha256,logical_bytes:$logical,guest_packages:$guest_packages,compatibility_packages:$compatibility_packages,openssh_version_exit:$openssh_version_exit,dbclient_version_exit:$dbclient_version_exit,installed_globally:false,runtime_dependency:false,reusable_identity:false}' > "$STAGE/PHASE-0B-CLIENT-ROOT.json"
chmod -R go-w "$STAGE"
mv -T "$EVIDENCE/openssh-client-version.stdout.stage" "$EVIDENCE/openssh-client-version.stdout"
mv -T "$EVIDENCE/openssh-client-version.stderr.stage" "$EVIDENCE/openssh-client-version.stderr"
mv -T "$EVIDENCE/dbclient-version.stdout.stage" "$EVIDENCE/dbclient-version.stdout"
mv -T "$EVIDENCE/dbclient-version.stderr.stage" "$EVIDENCE/dbclient-version.stderr"
mv -T "$EVIDENCE/certification-client-root-files.sha256.stage" "$EVIDENCE/certification-client-root-files.sha256"
mv -T "$STAGE" "$FINAL"
sync -f "$FINAL/PHASE-0B-CLIENT-ROOT.json"; sync -f "$BUILD"
printf 'CLIENT_ROOT=PASS\nPATH=%s\nOPENSSH=%s\nDROPBEAR=%s\nDROPBEAR_VERSION_EXIT=%s\nTREE_MANIFEST_SHA256=%s\nLOGICAL_BYTES=%s\n' "$FINAL" "$openssh" "$dropbear" "$db_rc" "$tree_sha" "$logical"
