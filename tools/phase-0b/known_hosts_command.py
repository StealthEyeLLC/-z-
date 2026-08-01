#!/usr/bin/env python3
"""Read-only strict KnownHostsCommand for one bounded Phase 0B alias."""
from __future__ import annotations
import argparse, hashlib, json, re, stat, sys
from pathlib import Path
ALIAS=re.compile(r'\Az-proof-[a-z0-9]{16}\Z',re.ASCII)

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--inventory',type=Path,required=True); p.add_argument('--alias',required=True); p.add_argument('--reason',required=True); p.add_argument('--key',default=''); a=p.parse_args()
    try:
        if not ALIAS.fullmatch(a.alias): raise ValueError('invalid alias grammar')
        if a.reason not in ('ORDER','HOSTNAME','ADDRESS'): raise ValueError('unsupported lookup reason')
        if any(ord(c)<32 or ord(c)>126 for c in a.key): raise ValueError('invalid key token')
        st=a.inventory.lstat()
        if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode) or st.st_uid!=0 or stat.S_IMODE(st.st_mode)!=0o600: raise ValueError('unsafe inventory')
        d=json.loads(a.inventory.read_text())
        if d['alias']!=a.alias: raise ValueError('alias mismatch')
        line=d['known_hosts_line']
        if hashlib.sha256(line.encode()).hexdigest()!=d['line_sha256']: raise ValueError('inventory digest mismatch')
        if '\n' in line or '\r' in line or not line.startswith(a.alias+' '): raise ValueError('malformed inventory line')
        print(line); return 0
    except Exception as e:
        print(f'known-host lookup refused: {e}',file=sys.stderr); return 71
if __name__=='__main__': raise SystemExit(main())
