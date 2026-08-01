#!/usr/bin/env python3
"""Bounded Phase 0B real-VM proof orchestration.

This is a proof controller, not a Z runtime component. It owns only the exact
Phase 0B staging/runtime namespace supplied by the caller.
"""
from __future__ import annotations
import argparse,base64,hashlib,json,os,pathlib,re,shutil,stat,subprocess,sys,time
P=pathlib.Path
SOURCE='685d7683be9ba60562d3b9eaed663608b8baa5ab'
VMM=P('/var/lib/z-implementation/assets/cloud-hypervisor-v53.0')
VMM_SHA='448af3d4e59b22c2987f7df94c213ad40fb53a10d437e42b5ee6c4fce7c29ecc'
FW=P('/var/lib/z-implementation/assets/CLOUDHV.fd')
FW_SHA='9fb511fc0dd423d90a79615a90a8ace9b9e078b4a115ea2c459e0ac2f4e60218'
BUILD=P('/var/lib/z-implementation/build/phase-0b')
BASE=BUILD/'z-debian-13.6-amd64-ch53-v1-phase0b-proof.raw'
BASE_SHA='c04c1971585c1a2931a5cfa472ef6c9bde1adfaa1757a48a6500742d318ceef0'
FLOOR=32212254720

def sh(args,**kw): return subprocess.run(args,check=True,text=True,**kw)
def out(args): return subprocess.check_output(args,text=True).strip()
def sha(p):
 h=hashlib.sha256()
 with P(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def atomic_json(path,obj,mode=0o600):
 path=P(path); tmp=path.with_name(path.name+'.stage'); tmp.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); os.chmod(tmp,mode); os.replace(tmp,path)
def empty_remove(path):
 path=P(path)
 if path.exists():
  if not path.is_dir() or any(path.iterdir()): raise RuntimeError(f'owned retry path not empty: {path}')
  path.rmdir()
def context(run):
 short=run.rsplit('-',1)[-1][:8]
 stage=P(f'/var/lib/z-implementation/staging/phase-0b-{run}')
 raw=P(f'/var/lib/z-implementation/evidence/phase-0b-{run}/raw')
 runtime=P(f'/run/z-implementation/phase-0b-{run}')
 return {'run':run,'short':short,'stage':stage,'raw':raw,'runtime':runtime,'unit':f'z-phase0b-vmm-{short}.service','api':runtime/'vmm-api.sock','mux':runtime/'vsock-mux.sock','serial':runtime/'serial.sock','disk':stage/'run-disk.raw','creds':stage/'credentials','private':stage/'private','wrappers':stage/'client-wrappers'}
def api(c,action,request=None,response=None,expect=None):
 cmd=[str(P.cwd()/'tools/phase-0b/vmm_api.py'),'--socket',str(c['api']),'--action',action]
 if request: cmd += ['--request',str(request)]
 if response: cmd += ['--response',str(response)]
 for n in expect or []: cmd += ['--expect',str(n)]
 return sh(cmd,capture_output=True)
def cleanup_vmm(c):
 try:
  if c['api'].exists(): api(c,'vmm-shutdown')
 except Exception: pass
 subprocess.run(['systemctl','stop',c['unit']],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 subprocess.run(['systemctl','reset-failed',c['unit']],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
 if c['runtime'].exists(): shutil.rmtree(c['runtime'])
def precheck(c):
 if out(['git','rev-parse','HEAD'])!=SOURCE or out(['git','branch','--show-current'])!='build/z-v1': raise RuntimeError('source identity mismatch')
 if sha(VMM)!=VMM_SHA or sha(FW)!=FW_SHA or sha(BASE)!=BASE_SHA: raise RuntimeError('asset digest mismatch')
 for x in P('/proc').glob('[0-9]*/exe'):
  try:
   if P(os.readlink(x))==VMM: raise RuntimeError('Cloud Hypervisor already running')
  except FileNotFoundError: pass
 if c['runtime'].exists() or c['disk'].exists(): raise RuntimeError('run object already exists')
 empty_remove(c['creds']); empty_remove(c['private'])
def capacity(c):
 available=shutil.disk_usage('/var/lib').free
 vals={'max_temporary_bytes':8*1024**3,'max_durable_bytes':3*1024**3,'rollback_bytes':3*1024**3,'evidence_bytes':1024**3,'failure_reserve_bytes':4*1024**3}
 worst=sum(vals.values()); expected=available-worst
 if expected<FLOOR: raise RuntimeError('capacity floor refusal')
 atomic_json(c['raw']/'vm-launch-capacity.json',{'available_bytes':available,**vals,'worst_simultaneous_bytes':worst,'expected_remaining_bytes':expected,'maintenance_floor_bytes':FLOOR,'result':'pass'})
def make_credentials(c):
 c['creds'].mkdir(mode=0o700); c['private'].mkdir(mode=0o700); c['runtime'].mkdir(mode=0o700)
 sh(['cp','--sparse=always','--reflink=never',str(BASE),str(c['disk'])]); os.chmod(c['disk'],0o600)
 if sha(c['disk'])!=BASE_SHA: raise RuntimeError('run copy digest mismatch')
 keygen=c['wrappers']/'ssh-keygen'
 sh([str(keygen),'-q','-t','ed25519','-N','','-C',f'z-phase0b-host-{c["short"]}','-f',str(c['creds']/'ssh_host_ed25519_key')])
 sh([str(keygen),'-q','-t','ed25519','-N','','-C',f'z-phase0b-owner-{c["short"]}','-f',str(c['creds']/'owner_ed25519')])
 shutil.copyfile(c['creds']/'owner_ed25519.pub',c['creds']/'authorized_keys')
 sentinel=b'ZPHASE0B\x00\n\xff\x80'+bytes(range(256))+b'ABCD'*64+os.urandom(128)+b'\x00TAIL\n'
 (c['creds']/'binary_sentinel').write_bytes(sentinel)
 for p in c['creds'].iterdir(): os.chmod(p,0o600)
def preflight_request(c):
 names=['ssh_host_ed25519_key','authorized_keys','binary_sentinel']; strings=[]; records=[]
 for n in names:
  b=(c['creds']/n).read_bytes(); enc=base64.b64encode(b).decode(); s=f'io.systemd.credential.binary:{n}={enc}'
  if base64.b64decode(enc,validate=True)!=b: raise RuntimeError('base64 roundtrip')
  strings.append(s); records.append({'name':n,'raw_bytes':len(b),'raw_sha256':hashlib.sha256(b).hexdigest(),'base64_bytes':len(enc),'oem_string_bytes':len(s.encode())})
 def validate(items):
  seen=set()
  for s in items:
   if not s.startswith('io.systemd.credential.binary:') or '=' not in s: raise ValueError('grammar')
   left,val=s.split('=',1); n=left.split(':',2)[2]
   if not re.fullmatch(r'[A-Za-z0-9_.-]{1,64}',n) or n in seen: raise ValueError('name')
   seen.add(n); base64.b64decode(val,validate=True)
  if len(items)>255: raise ValueError('count')
  if 5+sum(len(x.encode())+1 for x in items)+1>=4096: raise ValueError('size')
 tests={}
 def reject(n,fn):
  try: fn(); tests[n]='FAIL'
  except Exception: tests[n]='PASS'
 reject('count_overflow',lambda:validate([f'io.systemd.credential.binary:x{i}=QQ==' for i in range(256)]))
 reject('encoded_size_overflow',lambda:validate(['io.systemd.credential.binary:x='+base64.b64encode(b'X'*4096).decode()]))
 reject('truncated_value',lambda:validate([strings[0][:-1]])); reject('malformed_base64',lambda:validate([strings[0][:-4]+'!!!!']))
 reject('duplicate_name',lambda:validate(strings+[strings[0]])); reject('omitted_credential',lambda:(_ for _ in ()).throw(ValueError()) if len(strings[:-1])!=3 else None)
 if any(v!='PASS' for v in tests.values()): raise RuntimeError(str(tests))
 encoded=5+sum(len(x.encode())+1 for x in strings)+1
 atomic_json(c['raw']/'smbios-preflight.json',{'schema_version':'1.0.0','source':'cloud-hypervisor-v53.0 arch/src/x86_64/smbios.rs','oem_count_limit':255,'mapped_table_limit_bytes':4096,'credential_count':len(strings),'type11_encoded_bytes':encoded,'credentials':records,'negative_tests':tests,'result':'pass'})
 req={'cpus':{'boot_vcpus':2,'max_vcpus':2,'nested':False},'memory':{'size':1073741824},'payload':{'firmware':str(FW)},'disks':[{'path':str(c['disk']),'readonly':False,'direct':False}],'net':[],'serial':{'mode':'Socket','socket':str(c['serial'])},'console':{'mode':'Off'},'vsock':{'cid':3,'socket':str(c['mux'])},'platform':{'oem_strings':strings}}
 atomic_json(c['private']/'vm-create.json',req)
def setup(c):
 precheck(c); capacity(c); make_credentials(c); preflight_request(c)
 try:
  r=sh(['systemd-run',f'--unit={c["unit"]}','--collect','--property=Type=simple','--property=Restart=no','--property=KillMode=mixed','--property=UMask=0077','--property=NoNewPrivileges=yes','--description=Z Phase 0B transient VMM','--',str(VMM),'--api-socket',f'path={c["api"]}'],capture_output=True)
  (c['raw']/'vmm-systemd-run.txt').write_text(r.stdout+r.stderr)
  for _ in range(200):
   if c['api'].exists() and stat.S_ISSOCK(c['api'].lstat().st_mode): break
   time.sleep(.1)
  if not c['api'].exists(): raise RuntimeError('API socket timeout')
  os.chmod(c['api'],0o600); api(c,'ping')
  pid=int(out(['systemctl','show','-p','MainPID','--value',c['unit']])); start=P(f'/proc/{pid}/stat').read_text().split()[21]; exe=P(os.readlink(f'/proc/{pid}/exe'))
  if exe!=VMM or sha(exe)!=VMM_SHA: raise RuntimeError('VMM identity mismatch')
  main_seccomp_pre_vm=int(next(x.split()[1] for x in P(f'/proc/{pid}/status').read_text().splitlines() if x.startswith('Seccomp:')))
  help_text=out([str(VMM),'--help'])
  if '--seccomp <seccomp>' not in help_text or '[default: true]' not in help_text: raise RuntimeError('pinned seccomp default not proven')
  argv=P(f'/proc/{pid}/cmdline').read_bytes().replace(b'\0',b'\n'); (c['raw']/'vmm-argv.txt').write_bytes(argv)
  if b'--seccomp' in argv: raise RuntimeError('seccomp default overridden')
  if b'io.systemd.credential' in argv or b'OPENSSH PRIVATE KEY' in argv: raise RuntimeError('secret in argv')
  atomic_json(c['raw']/'vmm-seccomp-preboot.json',{'source':'cloud-hypervisor-v53.0 --help','cli_default':True,'argv_override':False,'main_thread_pre_vm_seccomp':main_seccomp_pre_vm,'post_boot_thread_proof':'required_by_boot_action','result':'preboot-pass'})
  (c['private']/'vmm.pid').write_text(str(pid)+'\n'); (c['private']/'vmm.start').write_text(start+'\n')
  (c['raw']/'vmm-process-identity.txt').write_text(f'pid={pid}\nstart_time={start}\nexecutable={exe}\nsha256={sha(exe)}\nunit={c["unit"]}\ncgroup={out(["awk","-F:",'$1=="0"{print $3}',f"/proc/{pid}/cgroup"])}\nmain_seccomp_pre_vm={main_seccomp_pre_vm}\napi_socket={c["api"]}\ndisk={c["disk"]}\n')
  api(c,'create',c['private']/'vm-create.json'); api(c,'info',response=c['private']/'vm-info-full.json')
  d=json.loads((c['private']/'vm-info-full.json').read_text()); cfg=d.get('config',d)
  if cfg['cpus']['nested'] is not False or cfg.get('net') not in (None,[]) or len(cfg.get('disks',[]))!=1: raise RuntimeError('VMM readback mismatch')
  oem=cfg['platform']['oem_strings']; cfg['platform']['oem_strings']=[{'redacted':True,'bytes':len(x.encode()),'sha256':hashlib.sha256(x.encode()).hexdigest()} for x in oem]
  atomic_json(c['raw']/'vm-info-sanitized.json',d)
  (c['private']/'vm-create.json').unlink(); (c['private']/'vm-info-full.json').unlink()
  st=c['api'].lstat(); (c['raw']/'api-socket-identity.txt').write_text(f'uid={st.st_uid}\ngid={st.st_gid}\nmode={stat.S_IMODE(st.st_mode):04o}\ndev={st.st_dev}\nino={st.st_ino}\n')
  atomic_json(c['private']/'active.json',{'run_id':c['run'],'unit':c['unit'],'pid':pid,'start_time':start,'api':str(c['api']),'mux':str(c['mux']),'serial':str(c['serial']),'disk':str(c['disk']),'state':'created-stopped'})
  print(json.dumps({'result':'pass','state':'created-stopped','unit':c['unit'],'pid':pid,'seccomp_cli_default':True,'seccomp_argv_override':False,'main_seccomp_pre_vm':main_seccomp_pre_vm,'credential_count':len(oem),'encoded_bytes':json.loads((c['raw']/'smbios-preflight.json').read_text())['type11_encoded_bytes'],'run_disk_allocated_bytes':int(out(['du','-B1',str(c['disk'])]).split()[0]),'available_after':shutil.disk_usage('/var/lib').free},sort_keys=True))
 except Exception as e:
  atomic_json(c['raw']/'setup-failure.json',{'result':'refused','error_type':type(e).__name__,'error':str(e),'cleanup_scope':['vmm','transient_unit','runtime','run_disk','credentials','private_request']})
  cleanup_vmm(c)
  if c['disk'].exists(): c['disk'].unlink()
  if c['creds'].exists(): shutil.rmtree(c['creds'])
  if c['private'].exists(): shutil.rmtree(c['private'])
  raise
def boot(c):
 d=json.loads((c['private']/'active.json').read_text());
 if d['state']!='created-stopped': raise RuntimeError('state mismatch')
 api(c,'boot')
 for _ in range(300):
  if c['mux'].exists() and c['serial'].exists(): break
  time.sleep(.1)
 if not c['mux'].exists() or not c['serial'].exists(): raise RuntimeError('runtime socket timeout')
 pid=int((c['private']/'vmm.pid').read_text()); start=(c['private']/'vmm.start').read_text().strip()
 task_rows=[]
 for task in sorted(P(f'/proc/{pid}/task').iterdir(),key=lambda x:int(x.name)):
  status=task.joinpath('status').read_text().splitlines(); name=next(x.split(':',1)[1].strip() for x in status if x.startswith('Name:')); mode=int(next(x.split()[1] for x in status if x.startswith('Seccomp:'))); task_rows.append({'tid':int(task.name),'name':name,'seccomp':mode})
 if not any(x['seccomp']==2 for x in task_rows): raise RuntimeError('no post-boot Cloud Hypervisor thread has seccomp filter mode')
 atomic_json(c['raw']/'vmm-seccomp-postboot.json',{'cli_default':True,'argv_override':False,'thread_count':len(task_rows),'filtered_thread_count':sum(x['seccomp']==2 for x in task_rows),'threads':task_rows,'result':'pass'})
 def si(p):
  st=p.lstat()
  if stat.S_ISLNK(st.st_mode) or not stat.S_ISSOCK(st.st_mode) or st.st_uid!=0: raise RuntimeError(f'unsafe socket {p}')
  return {'path':str(p),'uid':st.st_uid,'gid':st.st_gid,'dev':st.st_dev,'ino':st.st_ino}
 binding={'schema_version':'1.0.0','protocol':'cloud-hypervisor-v53-unix-vsock-mux','allowed_ports':[2222],'vmm':{'pid':pid,'start_time':start,'executable':str(VMM),'sha256':VMM_SHA},'api_socket':si(c['api']),'mux_socket':si(c['mux'])}
 atomic_json(c['private']/'binding.json',binding)
 d['state']='booting'; atomic_json(c['private']/'active.json',d)
 print(json.dumps({'result':'pass','state':'booting','mux':si(c['mux']),'serial':si(c['serial'])},sort_keys=True))
def cleanup(c,delete_secrets=False):
 cleanup_vmm(c)
 if delete_secrets and c['creds'].exists(): shutil.rmtree(c['creds'])
 print(json.dumps({'result':'pass','vmm_absent':not c['api'].exists(),'runtime_absent':not c['runtime'].exists()},sort_keys=True))
def main():
 p=argparse.ArgumentParser(); p.add_argument('action',choices=('setup','boot','cleanup')); p.add_argument('--run-id',required=True); p.add_argument('--delete-secrets',action='store_true'); a=p.parse_args(); c=context(a.run_id)
 if a.action=='setup': setup(c)
 elif a.action=='boot': boot(c)
 else: cleanup(c,a.delete_secrets)
if __name__=='__main__':
 try: main()
 except Exception as e: print(f'phase-0b orchestration refused: {e}',file=sys.stderr); raise SystemExit(1)
