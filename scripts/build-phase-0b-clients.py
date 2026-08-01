#!/usr/bin/env python3
"""Resolve and materialize the exact Phase 0B certification-client universe."""
from __future__ import annotations
import argparse, hashlib, json, lzma, os, re, subprocess, sys, tempfile, urllib.request
from pathlib import Path

FIELD = re.compile(r"^([A-Za-z0-9-]+):\s*(.*)$")
DEP = re.compile(r"^([a-z0-9][a-z0-9+.-]*)(?::[a-z0-9-]+)?(?:\s*\((<<|<=|=|>=|>>)\s*([^\)]+)\))?")

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def parse_packages(path: Path, source: str, archive: str) -> list[dict]:
    text=lzma.open(path,'rt',encoding='utf-8',errors='strict').read()
    out=[]
    for para in text.split('\n\n'):
        if not para.strip(): continue
        d:dict[str,str]={}; current=None
        for line in para.splitlines():
            if line.startswith((' ','\t')) and current:
                d[current]+=' '+line.strip(); continue
            m=FIELD.match(line)
            if m: current=m.group(1); d[current]=m.group(2)
        if {'Package','Version','Architecture','Filename','Size','SHA256'} <= d.keys():
            d['_source']=source; d['_archive']=archive; out.append(d)
    return out

def cmpver(a: str, op: str, b: str) -> bool:
    return subprocess.run(['dpkg','--compare-versions',a,op,b],check=False).returncode==0

def best(records: list[dict]) -> dict:
    chosen=records[0]
    for r in records[1:]:
        if cmpver(r['Version'],'gt',chosen['Version']): chosen=r
    return chosen

def deps(value: str) -> list[list[tuple[str,str|None,str|None]]]:
    groups=[]
    for group in value.split(','):
        alts=[]
        for raw in group.split('|'):
            raw=re.sub(r'\[[^\]]*\]','',raw)
            raw=re.sub(r'<[^>]*>','',raw).strip()
            m=DEP.match(raw)
            if m: alts.append((m.group(1),m.group(2),m.group(3)))
        if alts: groups.append(alts)
    return groups

def satisfies(version: str, op: str|None, wanted: str|None) -> bool:
    return True if not op else cmpver(version,op,wanted or '')

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--repository',type=Path,required=True)
    p.add_argument('--metadata',type=Path,required=True)
    p.add_argument('--snapshot',required=True)
    a=p.parse_args()
    repo=a.repository; metadata=a.metadata
    index_specs=[
      ('debian-main',metadata/'trixie-main-amd64.Packages.xz','debian'),
      ('debian-updates',metadata/'trixie-updates-main-amd64.Packages.xz','debian'),
      ('debian-security',metadata/'trixie-security-main-amd64.Packages.xz','debian-security'),
    ]
    all_records=[]
    for name,path,archive in index_specs:
        if not path.is_file(): raise RuntimeError(f'missing verified index: {path}')
        all_records.extend(parse_packages(path,name,archive))
    by_name:dict[str,list[dict]]={}
    for r in all_records:
        if r['Architecture'] in ('amd64','all'): by_name.setdefault(r['Package'],[]).append(r)
    guest=json.loads((repo/'guest-closure.json').read_text())
    guest_by={r['package']:r for r in guest['packages']}
    root=json.loads((repo/'compatibility-client.json').read_text())
    candidates=[r for r in by_name.get(root['package'],[]) if r['Version']==root['version'] and r['Architecture']==root['architecture'] and r['SHA256']==root['sha256'] and int(r['Size'])==root['size'] and r['Filename']==root['filename']]
    if len(candidates)!=1: raise RuntimeError('compatibility root does not bind uniquely to signed indexes')
    root_record=candidates[0]
    selected:dict[str,dict]={root['package']:root_record}
    queue=[root['package']]
    while queue:
        name=queue.pop(0); r=selected[name]
        for field in ('Pre-Depends','Depends'):
            for group in deps(r.get(field,'')):
                choice=None
                for dep_name,op,wanted in group:
                    if dep_name in guest_by and satisfies(guest_by[dep_name]['version'],op,wanted):
                        choice=('guest',dep_name,guest_by[dep_name]); break
                    recs=[x for x in by_name.get(dep_name,[]) if satisfies(x['Version'],op,wanted)]
                    if recs:
                        choice=('compat',dep_name,best(recs)); break
                if choice is None: raise RuntimeError(f'unresolved dependency for {name}: {group!r}')
                kind,dep_name,rec=choice
                if kind=='compat' and dep_name not in selected:
                    selected[dep_name]=rec; queue.append(dep_name)
    packages=[]; package_dir=repo/'packages'; package_dir.mkdir(mode=0o700,exist_ok=True)
    for name in sorted(selected):
        r=selected[name]; digest=r['SHA256']; target=package_dir/(digest+'.deb')
        url=f"https://snapshot.debian.org/archive/{r['_archive']}/{a.snapshot}/{r['Filename']}"
        if not target.exists():
            fd,tmp_name=tempfile.mkstemp(prefix=digest+'.',suffix='.partial',dir=package_dir)
            os.close(fd); tmp=Path(tmp_name)
            try:
                req=urllib.request.Request(url,headers={'User-Agent':'z-phase0b/1'})
                with urllib.request.urlopen(req,timeout=120) as src,tmp.open('wb') as dst:
                    while True:
                        b=src.read(1024*1024)
                        if not b: break
                        dst.write(b)
                    dst.flush(); os.fsync(dst.fileno())
                if tmp.stat().st_size!=int(r['Size']) or sha256(tmp)!=digest: raise RuntimeError(f'digest/size mismatch: {name}')
                os.chmod(tmp,0o400); os.replace(tmp,target)
            finally:
                if tmp.exists(): tmp.unlink()
        if target.stat().st_size!=int(r['Size']) or sha256(target)!=digest: raise RuntimeError(f'cached package mismatch: {name}')
        packages.append({'package':name,'version':r['Version'],'architecture':r['Architecture'],'size':int(r['Size']),'sha256':digest,'filename':r['Filename'],'cache_name':target.name,'source_index':r['_source'],'source_url':url,'depends':r.get('Depends',''),'pre_depends':r.get('Pre-Depends','')})
    guest_dependencies=sorted({dep for r in selected.values() for field in ('Pre-Depends','Depends') for group in deps(r.get(field,'')) for dep,op,wanted in group if dep in guest_by and satisfies(guest_by[dep]['version'],op,wanted)})
    manifest={'schema_version':'1.0.0','purpose':'phase-0b-certification-consumer-only','snapshot_timestamp':a.snapshot,'root_package':root['package'],'root_version':root['version'],'package_count':len(packages),'packages':packages,'satisfied_by_locked_guest_universe':guest_dependencies,'live_mirror_used':False,'runtime_dependency':False}
    raw=(json.dumps(manifest,sort_keys=True,indent=2)+'\n').encode()
    out=repo/'compatibility-closure.json'; tmp=out.with_suffix('.json.stage'); tmp.write_bytes(raw); os.chmod(tmp,0o400); os.replace(tmp,out)
    print(json.dumps({'result':'pass','package_count':len(packages),'packages':[x['package']+'='+x['version'] for x in packages],'guest_dependencies':guest_dependencies,'manifest_sha256':hashlib.sha256(raw).hexdigest()},sort_keys=True))
    return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as e:
        print(f'client closure refused: {e}',file=sys.stderr); raise SystemExit(1)
