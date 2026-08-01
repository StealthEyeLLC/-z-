#!/usr/bin/env python3
from __future__ import annotations
import argparse,hashlib,json,sys
from pathlib import Path

def sha256(p:Path)->str:
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()

def main()->int:
 ap=argparse.ArgumentParser()
 ap.add_argument("--repo",type=Path,default=Path(__file__).resolve().parents[1])
 ap.add_argument("--raw-evidence",type=Path)
 ap.add_argument("--require-ready",action="store_true")
 a=ap.parse_args(); repo=a.repo.resolve()
 cert=json.loads((repo/"evidence/phase-0b/CERTIFICATION.json").read_text())
 sem=json.loads((repo/"assets/phase-0b-semantics.json").read_text())
 assert cert["schema_version"]=="1.0.0" and sem["schema_version"]=="1.0.0"
 assert cert["phase"]==sem["phase"]=="0B"
 assert cert["source"]==sem["source"]
 assert cert["test_summary"]["executed"]==len(cert["test_ledger"])>=115
 assert cert["test_summary"]["passed"]==len(cert["test_ledger"])
 assert cert["test_summary"]["failed"]==0
 assert all(t["result"]=="pass" for t in cert["test_ledger"])
 assert len({t["id"] for t in cert["test_ledger"]})==len(cert["test_ledger"])
 gates={g["id"]:g["result"] for g in cert["gates"]}
 required={"image","smbios_credentials","static_vsock_sshd","native_fdpass_ssh","compatibility_stdio_ssh","strict_host_identity","exact_systemd_execution","connection_loss_recovery","serial_reboot_reconnect","fault_injection","vmm_abrupt_loss","zero_residue_cleanup","host_kernel_cve_2026_53359"}
 assert set(gates)==required
 assert all(v=="pass" for k,v in gates.items() if k!="host_kernel_cve_2026_53359")
 assert gates["host_kernel_cve_2026_53359"]=="blocked"
 assert cert["result"]=="blocked" and not cert["release_ready"] and cert["blockers"]
 assert sem["boundaries"]["baby_in_product"] is False and cert["scope"]["baby_in_z"] is False
 forbidden={".pyc",".raw",".qcow2",".img",".key"}
 bad=[]
 for p in repo.rglob("*"):
  if ".git" in p.parts or not p.is_file(): continue
  if p.suffix.lower() in forbidden or "__pycache__" in p.parts: bad.append(str(p.relative_to(repo)))
 assert not bad,bad
 if a.raw_evidence:
  eroot=a.raw_evidence.resolve()
  for name,expected in cert["raw_evidence"]["sha256"].items():
   p=eroot/name; assert p.is_file(),p; assert sha256(p)==expected,(name,sha256(p),expected)
 if a.require_ready:
  print("PHASE_0B=BLOCKED host-kernel-cve-2026-53359",file=sys.stderr); return 2
 print(f"PHASE_0B_RECORD=VERIFIED STATUS={cert['result']} TESTS={len(cert['test_ledger'])} BLOCKERS={len(cert['blockers'])}")
 return 0
if __name__=="__main__": raise SystemExit(main())
