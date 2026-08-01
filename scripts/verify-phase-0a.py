#!/usr/bin/env python3
"""Verify the Z Phase 0A host materialization without mutating it."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import stat
import subprocess
import sys
from typing import Any

REPO = Path(__file__).resolve().parents[1]
LOCK_PATH = REPO / "assets/dependencies.lock.json"
MANIFEST_PATH = REPO / "assets/phase-0a-materialization.json"


class VerificationError(RuntimeError):
    pass


def fail(message: str) -> None:
    raise VerificationError(message)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        fail(f"cannot read JSON {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"JSON root is not an object: {path}")
    return value


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def run(argv: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(argv, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if check and result.returncode != 0:
        fail(f"command failed ({result.returncode}): {' '.join(argv)}: {result.stderr.strip()}")
    return result


def tree_sha256(root: Path) -> str:
    require(root.is_dir() and not root.is_symlink(), f"tree root missing or unsafe: {root}")
    digest = hashlib.sha256()
    entries = sorted(root.rglob("*"), key=lambda path: os.fsencode(str(path.relative_to(root))))
    for path in entries:
        rel = str(path.relative_to(root))
        info = path.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if path.is_symlink():
            digest.update(f"L\0{rel}\0{mode:o}\0{os.readlink(path)}\0".encode())
        elif path.is_dir():
            digest.update(f"D\0{rel}\0{mode:o}\0".encode())
        elif path.is_file():
            digest.update(f"F\0{rel}\0{mode:o}\0{info.st_size}\0{sha256_file(path)}\0".encode())
        else:
            fail(f"unsupported object in materialized tree: {path}")
    return digest.hexdigest()


def absolute_file_tree_sha256(root: Path) -> str:
    require(root.is_dir() and not root.is_symlink(), f"protected evidence missing or unsafe: {root}")
    digest = hashlib.sha256()
    for path in sorted((p for p in root.rglob("*") if p.is_file()), key=lambda p: os.fsencode(str(p))):
        digest.update(f"{sha256_file(path)}  {path}\n".encode())
    return digest.hexdigest()


def verify_git(materialization: dict[str, Any]) -> None:
    source = materialization["source"]
    require(run(["git", "-C", str(REPO), "remote", "get-url", "origin"]).stdout.strip() == source["origin"], "origin mismatch")
    require(run(["git", "-C", str(REPO), "branch", "--show-current"]).stdout.strip() == source["branch"], "branch mismatch")
    require(run(["git", "-C", str(REPO), "rev-parse", f"{source['commit']}^{{tree}}"]).stdout.strip() == source["tree"], "source tree mismatch")
    ancestry = run(["git", "-C", str(REPO), "merge-base", "--is-ancestor", source["commit"], "HEAD"], check=False)
    require(ancestry.returncode == 0, "source commit is not an ancestor of HEAD")


def verify_roots(materialization: dict[str, Any]) -> None:
    roots_path = Path(materialization["root_authority"]["roots_manifest"]["path"])
    cleanup_path = Path(materialization["root_authority"]["cleanup_manifest"]["path"])
    require(sha256_file(roots_path) == materialization["root_authority"]["roots_manifest"]["sha256"], "ROOTS.json digest mismatch")
    require(sha256_file(cleanup_path) == materialization["root_authority"]["cleanup_manifest"]["sha256"], "cleanup authority digest mismatch")
    roots = load_json(roots_path)
    for entry in roots["roots"]:
        path = Path(entry["path"])
        require(path.exists() and not path.is_symlink(), f"root missing or symlink: {path}")
        info = path.stat()
        require(info.st_uid == entry["owner_uid"] and info.st_gid == entry["group_gid"], f"root owner mismatch: {path}")
        require(f"{stat.S_IMODE(info.st_mode):o}" == entry["mode"], f"root mode mismatch: {path}")
        require(str(info.st_dev) == entry["device"], f"root device mismatch: {path}")
    for path_text in materialization["empty_roots"]:
        path = Path(path_text)
        require(path.is_dir() and not path.is_symlink(), f"empty root missing or unsafe: {path}")
        require(not any(path.iterdir()), f"root is not empty: {path}")


def verify_debian(lock: dict[str, Any], materialization: dict[str, Any]) -> None:
    debian = materialization["debian"]
    closure_path = Path(debian["closure_manifest"]["path"])
    closure = load_json(closure_path)
    require(sha256_file(closure_path) == debian["closure_manifest"]["sha256"], "closure manifest digest mismatch")
    require(closure["package_count"] == 212 == debian["package_count"], "builder closure count mismatch")
    require(closure["candidate_tuple"] == lock["tuple"]["id"], "closure tuple mismatch")
    require(closure["snapshot_timestamp"] == lock["debian_snapshot"]["timestamp"], "snapshot timestamp mismatch")
    package_root = Path(debian["package_cache"])
    expected = {entry["cache_name"]: entry for entry in closure["packages"]}
    actual = {path.name for path in package_root.iterdir() if path.is_file()}
    require(actual == set(expected), "package cache file set mismatch")
    total = 0
    for name, entry in expected.items():
        path = package_root / name
        require(path.stat().st_size == entry["size"], f"package size mismatch: {entry['package']}")
        require(sha256_file(path) == entry["sha256"], f"package digest mismatch: {entry['package']}")
        require(stat.S_IMODE(path.stat().st_mode) == 0o400, f"package mode mismatch: {entry['package']}")
        total += path.stat().st_size
    require(total == debian["package_bytes"], "package byte total mismatch")
    builder = Path(debian["builder_root"]["path"])
    require(tree_sha256(builder) == debian["builder_root"]["tree_sha256"], "builder root tree digest mismatch")
    closure_lines = (builder / "var/lib/z-package-closure.txt").read_text(encoding="utf-8").splitlines()
    expected_lines = sorted(f"{entry['package']}={entry['version']}" for entry in closure["packages"])
    require(closure_lines == expected_lines, "builder root package closure mismatch")


def verify_rust(lock: dict[str, Any], materialization: dict[str, Any]) -> None:
    rust = materialization["rust"]
    channel = Path(rust["channel_manifest"]["path"])
    require(sha256_file(channel) == lock["toolchain"]["rust"]["channel_manifest_sha256"] == rust["channel_manifest"]["sha256"], "Rust channel manifest mismatch")
    components = Path(rust["component_cache"])
    evidence = load_json(Path(rust["verification_evidence"]["path"]))
    for entry in evidence["component_archives"]:
        path = components / entry["name"]
        require(path.is_file() and sha256_file(path) == entry["sha256"], f"Rust component mismatch: {entry['name']}")
    root = Path(rust["toolchain_root"]["path"])
    require(tree_sha256(root) == rust["toolchain_root"]["tree_sha256"], "Rust toolchain tree digest mismatch")
    rustc = run([str(root / "bin/rustc"), "--version"]).stdout.strip()
    cargo = run([str(root / "bin/cargo"), "--version"]).stdout.strip()
    require(rustc.startswith("rustc 1.97.1 "), f"unexpected rustc: {rustc}")
    require(cargo.startswith("cargo 1.97.1 "), f"unexpected cargo: {cargo}")
    require(evidence["offline_dependency_free_edition_2024_library_build"] == "pass", "offline Rust probe did not pass")


def verify_runtime_assets(lock: dict[str, Any], materialization: dict[str, Any]) -> None:
    for key in ("cloud_hypervisor", "firmware"):
        expected = lock["runtime_assets"][key]
        observed = materialization["runtime_assets"][key]
        path = Path(observed["path"])
        require(path.is_file() and not path.is_symlink(), f"runtime asset missing or unsafe: {path}")
        require(path.stat().st_size == expected["size"] == observed["size"], f"runtime asset size mismatch: {key}")
        require(sha256_file(path) == expected["sha256"] == observed["sha256"], f"runtime asset digest mismatch: {key}")
        require(f"{stat.S_IMODE(path.stat().st_mode):04o}" == observed["mode"], f"runtime asset mode mismatch: {key}")
    ch = Path(materialization["runtime_assets"]["cloud_hypervisor"]["path"])
    require(run([str(ch), "--version"]).stdout.startswith("cloud-hypervisor v53.0\n"), "Cloud Hypervisor version mismatch")


def verify_evidence(materialization: dict[str, Any]) -> None:
    for label, entry in materialization["host_evidence"].items():
        path = Path(entry["path"])
        require(path.is_file(), f"host evidence missing: {label}: {path}")
        require(sha256_file(path) == entry["sha256"], f"host evidence digest mismatch: {label}")
    fs = load_json(Path(materialization["host_evidence"]["filesystem_behavior"]["path"]))
    require(fs["sparse_fallback_result"] == "pass", "sparse fallback not certified")
    require(fs["interrupted_final_absent"] is True and fs["interrupted_owned_partial_cleaned"] is True, "interrupted copy semantics failed")
    require(fs["same_filesystem_staging"] is True, "staging is not same-filesystem")
    require(fs["backup_claim_made"] is False, "Phase 0A incorrectly claims a backup")
    final_entry = materialization["final_host_certification"]
    final_path = Path(final_entry["path"])
    require(final_path.is_file() and sha256_file(final_path) == final_entry["sha256"], "final host certificate digest mismatch")
    final = load_json(final_path)
    require(final["result"] == "pass", "final host certificate did not pass")
    require(final["deterministic_host_drift_result"] == "pass", "deterministic host drift gate failed")
    require(all(row["match"] is True for row in final["deterministic_comparisons"].values()), "final host comparison mismatch")
    require(final["firewall"]["policy_structure_match"] is True, "firewall policy structure mismatch")
    require(final["firewall"]["policy_drift_result"] == "pass", "firewall policy drift gate failed")
    require(final["firewall"]["phase_0a_firewall_mutations_performed"] is False, "Phase 0A recorded a firewall mutation")
    require(final["public_health_http_status"] == 200 and final["capacity_result"] == "pass", "final health or capacity gate failed")
    require(final["cloud_hypervisor_process_count"] == 0 and final["z_materialization_process_count"] == 0, "final process absence gate failed")
    require(final["phase_0b_entered"] is False and final["phase_1_entered"] is False, "later phase was entered")
    require(final["release_claim"] is False and final["runtime_capability_claim"] is False, "forbidden capability claim present")


def verify_protected_evidence(materialization: dict[str, Any]) -> None:
    protected = materialization["protected_reclamation_evidence"]
    root = Path(protected["path"])
    require(absolute_file_tree_sha256(root) == protected["tree_sha256"], "protected reclamation evidence tree digest mismatch")
    artifact_keys = (
        "deletion_manifest",
        "deletion_sizes",
        "completion_result",
        "completion_checksums",
        "final_checksums",
        "final_current_checksums",
        "wave5_checksums",
        "final_certification",
        "final_certification_sha256",
        "certification_marker",
    )
    for key in artifact_keys:
        entry = protected[key]
        path = Path(entry["path"])
        require(path.is_file() and sha256_file(path) == entry["sha256"], f"protected evidence digest mismatch: {key}")
    require(Path(protected["certification_marker"]["path"]).name == "CERTIFICATION-PASSED", "wrong certification marker binding")


def verify_host_baseline(materialization: dict[str, Any]) -> None:
    baseline = {}
    for line in Path(materialization["host_baseline"]["path"]).read_text(encoding="utf-8").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            baseline[key] = value
    require(sha256_file(Path(materialization["host_baseline"]["path"])) == materialization["host_baseline"]["sha256"], "host baseline digest mismatch")
    package_hash = hashlib.sha256(run(["bash", "-c", "dpkg-query -W -f='${binary:Package}\\t${Version}\\n' | LC_ALL=C sort"]).stdout.encode()).hexdigest()
    require(package_hash == baseline["package_state_sha256"], "global package state changed")
    require(sha256_file(Path("/etc/passwd")) == baseline["passwd_sha256"], "global passwd changed")
    require(sha256_file(Path("/etc/group")) == baseline["group_sha256"], "global group changed")
    for unit in materialization["protected_units"]:
        require(run(["systemctl", "is-active", unit]).stdout.strip() == "active", f"protected unit is not active: {unit}")
    failed = run(["systemctl", "--failed", "--no-legend", "--plain"]).stdout.strip()
    require(not failed, f"failed systemd units exist: {failed}")
    statvfs = os.statvfs("/var/lib")
    available = statvfs.f_bavail * statvfs.f_frsize
    require(available >= materialization["capacity"]["maintenance_floor_bytes"], "maintenance capacity floor violated")
    require(shutil.which("qemu-img") is None, "ambient qemu-img unexpectedly present")
    require(shutil.which("passt") is None, "ambient passt unexpectedly present")
    final = load_json(Path(materialization["final_host_certification"]["path"]))
    retained_path = Path(final["firewall"]["retained_post_reclamation_ruleset_path"])
    require(retained_path.is_file(), "retained firewall evidence missing")
    def canonical_firewall(text: str) -> str:
        text = re.sub(r"counter packets \d+ bytes \d+", "counter packets 0 bytes 0", text)
        return re.sub(
            r"(set addr-set-sshd \{.*?elements = \{).*?(\}\s*\n\s*\})",
            r"\1 <dynamic-fail2ban-members> \2",
            text,
            flags=re.S,
        )
    retained_policy = canonical_firewall(retained_path.read_text(encoding="utf-8"))
    current_policy = canonical_firewall(run(["nft", "list", "ruleset"]).stdout)
    retained_sha = hashlib.sha256(retained_policy.encode()).hexdigest()
    current_sha = hashlib.sha256(current_policy.encode()).hexdigest()
    require(retained_sha == final["firewall"]["retained_policy_structure_sha256"], "retained firewall policy digest mismatch")
    require(current_sha == retained_sha, "live firewall policy structure drifted")


def main() -> int:
    lock = load_json(LOCK_PATH)
    materialization = load_json(MANIFEST_PATH)
    require(materialization["schema_version"] == "1.0.0", "unsupported materialization schema")
    require(materialization["candidate_tuple"] == lock["tuple"]["id"] == "z-debian-13.6-amd64-ch53-v1", "candidate tuple mismatch")
    require(materialization["phase"] == "0A", "wrong phase manifest")
    require(materialization["release_claim"] is False, "Phase 0A must not claim release certification")
    verify_git(materialization)
    verify_roots(materialization)
    verify_debian(lock, materialization)
    verify_rust(lock, materialization)
    verify_runtime_assets(lock, materialization)
    verify_evidence(materialization)
    verify_protected_evidence(materialization)
    verify_host_baseline(materialization)
    print("PHASE_0A_VERIFY=PASS")
    print(f"CANDIDATE_TUPLE={materialization['candidate_tuple']}")
    print(f"SOURCE_COMMIT={materialization['source']['commit']}")
    print(f"SOURCE_TREE={materialization['source']['tree']}")
    print("RELEASE_CLAIM=false")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationError as exc:
        print(f"PHASE_0A_VERIFY=FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
