#!/bin/bash
set -euo pipefail
umask 077

RUN_ID=${1:?usage: build-phase-0b-guest.sh RUN_ID}
if [[ ${2:-} != --private-mount-namespace ]]; then
    exec unshare --mount --propagation private -- "$0" "$RUN_ID" --private-mount-namespace
fi

SOURCE_COMMIT=685d7683be9ba60562d3b9eaed663608b8baa5ab
VMM=/var/lib/z-implementation/assets/cloud-hypervisor-v53.0
FIRMWARE=/var/lib/z-implementation/assets/CLOUDHV.fd
BUILDER=/var/lib/z-implementation/build/debian-builder-root
REPOSITORY=/var/cache/z-implementation/phase-0b/guest-repository
STAGING=/var/lib/z-implementation/staging/phase-0b-$RUN_ID
EVIDENCE=/var/lib/z-implementation/evidence/phase-0b-$RUN_ID
BUILD=/var/lib/z-implementation/build/phase-0b
SHARE=$STAGING/guest-build-share
OUT=$SHARE/output
ROOTFS=$OUT/rootfs
MOUNT_ROOT=$OUT/mount-root
FINAL_IMAGE=$BUILD/z-debian-13.6-amd64-ch53-v1-phase0b-proof.raw
FINAL_META=$BUILD/z-debian-13.6-amd64-ch53-v1-phase0b-proof.json
LOOP=

cleanup() {
    set +e
    if mountpoint -q "$MOUNT_ROOT/boot/efi"; then umount "$MOUNT_ROOT/boot/efi"; fi
    for p in run sys proc dev; do
        if mountpoint -q "$MOUNT_ROOT/$p"; then umount -R "$MOUNT_ROOT/$p"; fi
    done
    if mountpoint -q "$MOUNT_ROOT"; then umount "$MOUNT_ROOT"; fi
    if [[ -n ${LOOP:-} ]]; then losetup -d "$LOOP" 2>/dev/null || true; fi
    if mountpoint -q "$BUILDER/tmp/repository"; then umount "$BUILDER/tmp/repository"; fi
    for p in run sys proc dev; do
        if mountpoint -q "$BUILDER/$p"; then umount -R "$BUILDER/$p"; fi
    done
    if mountpoint -q "$BUILDER/tmp"; then umount "$BUILDER/tmp"; fi
}
trap cleanup EXIT INT TERM HUP

[[ $(git rev-parse HEAD) == "$SOURCE_COMMIT" ]]
[[ $(git branch --show-current) == build/z-v1 ]]
[[ $(sha256sum "$VMM" | awk '{print $1}') == 448af3d4e59b22c2987f7df94c213ad40fb53a10d437e42b5ee6c4fce7c29ecc ]]
[[ $(sha256sum "$FIRMWARE" | awk '{print $1}') == 9fb511fc0dd423d90a79615a90a8ace9b9e078b4a115ea2c459e0ac2f4e60218 ]]
[[ $(jq -r .package_count "$REPOSITORY/guest-closure.json") == 188 ]]
[[ ! -e $FINAL_IMAGE && ! -e $FINAL_META ]]
[[ ! -e $SHARE ]]

AVAILABLE=$(df -B1 --output=avail /var/lib | tail -n1 | tr -d ' ')
MAX_TEMP=$((6 * 1024 * 1024 * 1024))
MAX_DURABLE=$((3 * 1024 * 1024 * 1024))
ROLLBACK=$((3 * 1024 * 1024 * 1024))
EVIDENCE_BYTES=$((1 * 1024 * 1024 * 1024))
FAILURE_RESERVE=$((4 * 1024 * 1024 * 1024))
WORST=$((MAX_TEMP + MAX_DURABLE + ROLLBACK + EVIDENCE_BYTES + FAILURE_RESERVE))
EXPECTED=$((AVAILABLE - WORST))
FLOOR=32212254720
(( EXPECTED >= FLOOR ))
jq -n --argjson available "$AVAILABLE" --argjson max_temporary "$MAX_TEMP" --argjson max_durable "$MAX_DURABLE" --argjson rollback "$ROLLBACK" --argjson evidence "$EVIDENCE_BYTES" --argjson failure_reserve "$FAILURE_RESERVE" --argjson worst "$WORST" --argjson expected "$EXPECTED" --argjson floor "$FLOOR" '{available_bytes:$available,max_temporary_bytes:$max_temporary,max_durable_bytes:$max_durable,rollback_bytes:$rollback,evidence_bytes:$evidence,failure_reserve_bytes:$failure_reserve,worst_simultaneous_bytes:$worst,expected_remaining_bytes:$expected,maintenance_floor_bytes:$floor,result:"pass"}' > "$EVIDENCE/raw/guest-build-capacity.json.stage"
mv -T "$EVIDENCE/raw/guest-build-capacity.json.stage" "$EVIDENCE/raw/guest-build-capacity.json"

install -d -m 0700 "$SHARE" "$OUT" "$SHARE/repository" "$MOUNT_ROOT"
mount --bind "$SHARE" "$BUILDER/tmp"
mount --bind "$REPOSITORY" "$BUILDER/tmp/repository"
mount --rbind /dev "$BUILDER/dev"
mount --make-rslave "$BUILDER/dev"
mount -t proc proc "$BUILDER/proc"
mount --rbind /sys "$BUILDER/sys"
mount --make-rslave "$BUILDER/sys"
mount --rbind /run "$BUILDER/run"
mount --make-rslave "$BUILDER/run"

(
    cd "$REPOSITORY"
    chroot "$BUILDER" /bin/bash -c 'cd /tmp/repository && /usr/bin/dpkg-scanpackages packages /dev/null > Packages.full.stage'
    mv -T Packages.full.stage Packages
    chmod 0400 Packages
)

INCLUDE=$(jq -r '[.packages[] | .package+"="+.version] | join(",")' "$REPOSITORY/guest-closure.json")
chroot "$BUILDER" /usr/bin/mmdebstrap \
    --mode=root \
    --variant=custom \
    --architectures=amd64 \
    --include="$INCLUDE" \
    --components=main \
    --aptopt='Acquire::Languages "none"' \
    --aptopt='APT::Install-Recommends "false"' \
    --aptopt='APT::Install-Suggests "false"' \
    --aptopt='Acquire::Retries "0"' \
    --aptopt='Acquire::http::Proxy "false"' \
    --aptopt='Acquire::https::Proxy "false"' \
    --customize-hook='printf "#!/bin/sh\nexit 101\n" > "$1/usr/sbin/policy-rc.d"; chmod 755 "$1/usr/sbin/policy-rc.d"' \
    --customize-hook='rm -f "$1/usr/sbin/policy-rc.d"' \
    trixie \
    /tmp/output/rootfs \
    'deb [trusted=yes] copy:///tmp/repository ./'

chroot "$ROOTFS" dpkg-query -W -f='${binary:Package}=${Version}\n' | sed 's/:amd64=/=/' | LC_ALL=C sort > "$OUT/guest-packages.actual"
jq -r '.resolved_package_closures.guest_seed.package_versions[]' assets/dependencies.lock.json | LC_ALL=C sort > "$OUT/guest-packages.expected"
diff -u "$OUT/guest-packages.expected" "$OUT/guest-packages.actual" > "$EVIDENCE/raw/guest-package-diff.txt" || {
    cat "$EVIDENCE/raw/guest-package-diff.txt" >&2
    exit 1
}
cp "$OUT/guest-packages.actual" "$EVIDENCE/raw/guest-package-manifest.txt"

cp tools/phase-0b/proof-target.c "$SHARE/proof-target.c"
chroot "$BUILDER" /usr/bin/gcc -std=c11 -Wall -Wextra -Werror -O2 -o /tmp/output/proof-target /tmp/proof-target.c
install -D -m 0755 "$OUT/proof-target" "$ROOTFS/usr/local/libexec/z-phase0b-proof-target"

printf 'z-phase0b-proof\n' > "$ROOTFS/etc/hostname"
cat > "$ROOTFS/etc/hosts" <<'EOF'
127.0.0.1 localhost
127.0.1.1 z-phase0b-proof
::1 localhost ip6-localhost ip6-loopback
EOF
: > "$ROOTFS/etc/machine-id"
rm -f "$ROOTFS/var/lib/dbus/machine-id"
rm -f "$ROOTFS/etc/ssh/ssh_host_"*
awk -F: 'BEGIN{OFS=":"} $1=="root"{$2=""} {print}' "$ROOTFS/etc/shadow" > "$ROOTFS/etc/shadow.stage"
mv -T "$ROOTFS/etc/shadow.stage" "$ROOTFS/etc/shadow"
chmod 0640 "$ROOTFS/etc/shadow"

cat > "$ROOTFS/etc/ssh/sshd_config_phase0b" <<'EOF'
Port 22
PermitRootLogin prohibit-password
PasswordAuthentication no
KbdInteractiveAuthentication no
ChallengeResponseAuthentication no
PermitEmptyPasswords no
UsePAM no
GSSAPIAuthentication no
HostbasedAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
StrictModes yes
AllowAgentForwarding no
AllowTcpForwarding yes
GatewayPorts no
PermitTunnel no
X11Forwarding no
PermitUserEnvironment no
PermitTTY yes
PrintMotd no
PrintLastLog no
LogLevel VERBOSE
Subsystem sftp /usr/lib/openssh/sftp-server
EOF

cat > "$ROOTFS/etc/systemd/system/z-phase0b-sshd-runtime.service" <<'EOF'
[Unit]
Description=Z Phase 0B OpenSSH privilege-separation runtime
Before=z-phase0b-sshd.socket

[Service]
Type=oneshot
ExecStart=/usr/bin/true
RemainAfterExit=yes
RuntimeDirectory=sshd
RuntimeDirectoryMode=0755
EOF
cat > "$ROOTFS/etc/systemd/system/z-phase0b-sshd.socket" <<'EOF'
[Unit]
Description=Z Phase 0B static AF_VSOCK OpenSSH socket
Requires=z-phase0b-sshd-runtime.service
After=z-phase0b-sshd-runtime.service
Before=sockets.target

[Socket]
ListenStream=vsock::2222
Accept=yes
MaxConnections=64
SocketMode=0600

[Install]
WantedBy=sockets.target
EOF
cat > "$ROOTFS/etc/systemd/system/z-phase0b-sshd@.service" <<'EOF'
[Unit]
Description=Z Phase 0B stock sshd -i connection
After=systemd-credentials-setup.service

[Service]
Type=simple
StandardInput=socket
StandardOutput=socket
StandardError=journal
LoadCredential=ssh_host_ed25519_key
LoadCredential=authorized_keys
LoadCredential=binary_sentinel
ExecStartPre=/usr/bin/test -r %d/ssh_host_ed25519_key
ExecStartPre=/usr/bin/test -r %d/authorized_keys
ExecStartPre=/usr/bin/test -r %d/binary_sentinel
ExecStart=-/usr/sbin/sshd -i -e -f /etc/ssh/sshd_config_phase0b -h %d/ssh_host_ed25519_key -o AuthorizedKeysFile=%d/authorized_keys
NoNewPrivileges=yes
PrivateTmp=yes
RestrictAddressFamilies=AF_UNIX AF_VSOCK AF_INET AF_INET6
EOF
install -d -m 0755 "$ROOTFS/etc/systemd/system/sockets.target.wants" "$ROOTFS/etc/systemd/system-generators"
ln -s ../z-phase0b-sshd.socket "$ROOTFS/etc/systemd/system/sockets.target.wants/z-phase0b-sshd.socket"
ln -s /dev/null "$ROOTFS/etc/systemd/system-generators/systemd-ssh-generator"
for unit in ssh.service sshd.service ssh.socket; do
    ln -sfn /dev/null "$ROOTFS/etc/systemd/system/$unit"
done
chmod 0644     "$ROOTFS/etc/ssh/sshd_config_phase0b"     "$ROOTFS/etc/systemd/system/z-phase0b-sshd-runtime.service"     "$ROOTFS/etc/systemd/system/z-phase0b-sshd.socket"     "$ROOTFS/etc/systemd/system/z-phase0b-sshd@.service"
install -d -m 0755 "$ROOTFS/etc/systemd/system/getty.target.wants"
ln -s /lib/systemd/system/serial-getty@.service "$ROOTFS/etc/systemd/system/getty.target.wants/serial-getty@ttyS0.service"

cat > "$ROOTFS/etc/default/grub" <<'EOF'
GRUB_DEFAULT=0
GRUB_TIMEOUT=1
GRUB_TIMEOUT_STYLE=menu
GRUB_TERMINAL="serial console"
GRUB_SERIAL_COMMAND="serial --speed=115200 --unit=0 --word=8 --parity=no --stop=1"
GRUB_CMDLINE_LINUX_DEFAULT="console=ttyS0,115200n8 systemd.show_status=yes systemd.log_target=console"
GRUB_CMDLINE_LINUX=""
EOF
rm -f "$ROOTFS/etc/network/interfaces" "$ROOTFS/etc/systemd/network/"*.network 2>/dev/null || true
find "$ROOTFS" -xdev -type f \( -name 'ssh_host_*' -o -name '*private*key*' \) -print > "$EVIDENCE/raw/identity-file-scan-before-image.txt"
[[ ! -s $EVIDENCE/raw/identity-file-scan-before-image.txt ]]
find "$ROOTFS" -xdev -type f -exec sh -c 'grep -Il -- "BEGIN OPENSSH PRIVATE KEY" "$@" || true' sh {} + > "$EVIDENCE/raw/private-key-content-scan-before-image.txt"
[[ ! -s $EVIDENCE/raw/private-key-content-scan-before-image.txt ]]
! find "$ROOTFS" -xdev \( -iname '*baby*' -o -iname '*z-implementation*' \) -print | grep . > "$EVIDENCE/raw/prohibited-component-scan-before-image.txt"

chroot "$BUILDER" /usr/bin/qemu-img create -f raw /tmp/output/proof-image.stage.raw 6G
chroot "$BUILDER" /usr/sbin/sgdisk --clear \
    --new=1:2048:+256M --typecode=1:ef00 --change-name=1:EFI \
    --new=2:0:0 --typecode=2:8300 --change-name=2:root \
    /tmp/output/proof-image.stage.raw
LOOP=$(losetup --find --show --partscan "$OUT/proof-image.stage.raw")
for _ in $(seq 1 50); do [[ -b ${LOOP}p1 && -b ${LOOP}p2 ]] && break; sleep .1; done
[[ -b ${LOOP}p1 && -b ${LOOP}p2 ]]
chroot "$BUILDER" /usr/sbin/mkfs.vfat -F 32 -n ZEFI "${LOOP}p1"
chroot "$BUILDER" /usr/sbin/mkfs.ext4 -F -L zroot -m 0 "${LOOP}p2"
mount "${LOOP}p2" "$MOUNT_ROOT"
install -d -m 0755 "$MOUNT_ROOT/boot/efi"
mount "${LOOP}p1" "$MOUNT_ROOT/boot/efi"
cp -a --preserve=all "$ROOTFS/." "$MOUNT_ROOT/"
ROOT_UUID=$(blkid -s UUID -o value "${LOOP}p2")
EFI_UUID=$(blkid -s UUID -o value "${LOOP}p1")
cat > "$MOUNT_ROOT/etc/fstab" <<EOF
UUID=$ROOT_UUID / ext4 defaults,errors=remount-ro 0 1
UUID=$EFI_UUID /boot/efi vfat umask=0077 0 1
EOF
mount --rbind /dev "$MOUNT_ROOT/dev"; mount --make-rslave "$MOUNT_ROOT/dev"
mount -t proc proc "$MOUNT_ROOT/proc"
mount --rbind /sys "$MOUNT_ROOT/sys"; mount --make-rslave "$MOUNT_ROOT/sys"
mount --rbind /run "$MOUNT_ROOT/run"; mount --make-rslave "$MOUNT_ROOT/run"
chroot "$MOUNT_ROOT" /usr/sbin/update-initramfs -u -k all
chroot "$MOUNT_ROOT" /usr/sbin/grub-install --target=x86_64-efi --efi-directory=/boot/efi --boot-directory=/boot --removable --no-nvram --recheck
chroot "$MOUNT_ROOT" /usr/sbin/update-grub
sync

find "$MOUNT_ROOT" -xdev -type f \( -name 'ssh_host_*' -o -name '*private*key*' \) -print > "$EVIDENCE/raw/identity-file-scan-final.txt"
[[ ! -s $EVIDENCE/raw/identity-file-scan-final.txt ]]
find "$MOUNT_ROOT" -xdev -type f -exec sh -c 'grep -Il -- "BEGIN OPENSSH PRIVATE KEY" "$@" || true' sh {} + > "$EVIDENCE/raw/private-key-content-scan-final.txt"
[[ ! -s $EVIDENCE/raw/private-key-content-scan-final.txt ]]
[[ ! -e $MOUNT_ROOT/usr/local/bin/z && ! -e $MOUNT_ROOT/usr/bin/z ]]
[[ ! -e $MOUNT_ROOT/opt/baby-quirt && ! -e $MOUNT_ROOT/var/lib/baby-quirt ]]

for p in run sys proc dev; do if mountpoint -q "$MOUNT_ROOT/$p"; then umount -R "$MOUNT_ROOT/$p"; fi; done
umount "$MOUNT_ROOT/boot/efi"
umount "$MOUNT_ROOT"
losetup -d "$LOOP"; LOOP=

IMAGE_SHA=$(sha256sum "$OUT/proof-image.stage.raw" | awk '{print $1}')
LOGICAL=$(stat -c %s "$OUT/proof-image.stage.raw")
ALLOCATED=$(du -B1 "$OUT/proof-image.stage.raw" | awk '{print $1}')
PACKAGE_MANIFEST_SHA=$(sha256sum "$EVIDENCE/raw/guest-package-manifest.txt" | awk '{print $1}')
RECIPE_SHA=$(sha256sum scripts/build-phase-0b-guest.sh | awk '{print $1}')
jq -n \
    --arg candidate_tuple z-debian-13.6-amd64-ch53-v1 \
    --arg purpose phase-0b-proof-only-identity-free \
    --arg snapshot 20260731T120000Z \
    --arg image_sha256 "$IMAGE_SHA" \
    --argjson logical_bytes "$LOGICAL" \
    --argjson allocated_bytes "$ALLOCATED" \
    --arg package_manifest_sha256 "$PACKAGE_MANIFEST_SHA" \
    --arg recipe_sha256 "$RECIPE_SHA" \
    --arg root_uuid "$ROOT_UUID" \
    --arg efi_uuid "$EFI_UUID" \
    '{schema_version:"1.0.0",candidate_tuple:$candidate_tuple,purpose:$purpose,snapshot_timestamp:$snapshot,image_sha256:$image_sha256,logical_bytes:$logical_bytes,allocated_bytes:$allocated_bytes,package_count:188,package_manifest_sha256:$package_manifest_sha256,recipe_sha256:$recipe_sha256,root_uuid:$root_uuid,efi_uuid:$efi_uuid,reusable_machine_identity:false,reusable_ssh_host_key:false,owner_private_key:false,baby_component:false,z_binary:false,guest_agent:false,network_configuration:false}' > "$OUT/proof-image.json.stage"
chmod 0400 "$OUT/proof-image.json.stage"

mv -T "$OUT/proof-image.stage.raw" "$FINAL_IMAGE"
mv -T "$OUT/proof-image.json.stage" "$FINAL_META"
chmod 0400 "$FINAL_IMAGE" "$FINAL_META"
sync -f "$FINAL_IMAGE"; sync -f "$FINAL_META"; sync -f "$BUILD"

printf 'GUEST_BUILD=PASS\nIMAGE=%s\nIMAGE_SHA256=%s\nLOGICAL_BYTES=%s\nALLOCATED_BYTES=%s\nPACKAGE_COUNT=188\nPACKAGE_MANIFEST_SHA256=%s\nKERNEL=%s\nSYSTEMD=%s\nOPENSSH=%s\nAVAILABLE_AFTER=%s\n' \
    "$FINAL_IMAGE" "$IMAGE_SHA" "$LOGICAL" "$ALLOCATED" "$PACKAGE_MANIFEST_SHA" \
    "$(chroot "$ROOTFS" dpkg-query -W -f='${Version}' linux-image-amd64)" \
    "$(chroot "$ROOTFS" dpkg-query -W -f='${Version}' systemd)" \
    "$(chroot "$ROOTFS" dpkg-query -W -f='${Version}' openssh-server)" \
    "$(df -B1 --output=avail /var/lib | tail -n1 | tr -d ' ')"
