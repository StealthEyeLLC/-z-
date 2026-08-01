#!/usr/bin/env python3
"""Bounded binary-safe reconnecting client for the private serial socket."""
from __future__ import annotations
import argparse, json, os, socket, stat, sys, time
from pathlib import Path

def safe_socket(path: Path, runtime: Path) -> None:
    if path.parent!=runtime or not path.is_absolute(): raise RuntimeError('serial path outside runtime')
    st=path.lstat()
    if stat.S_ISLNK(st.st_mode) or not stat.S_ISSOCK(st.st_mode) or st.st_uid!=0: raise RuntimeError('unsafe serial socket')

def main() -> int:
    p=argparse.ArgumentParser(); p.add_argument('--socket',type=Path,required=True); p.add_argument('--runtime',type=Path,required=True); p.add_argument('--output',type=Path,required=True); p.add_argument('--events',type=Path,required=True); p.add_argument('--timeout',type=float,default=180); p.add_argument('--retry',type=float,default=.2); a=p.parse_args()
    deadline=time.monotonic()+a.timeout; offset=0; attempts=0; last_identity=None
    with a.output.open('ab',buffering=0) as out, a.events.open('a',encoding='utf-8',buffering=1) as ev:
        while time.monotonic()<deadline:
            attempts+=1
            try:
                safe_socket(a.socket,a.runtime); st=a.socket.stat(); ident=(st.st_dev,st.st_ino)
                s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(min(2,max(.1,deadline-time.monotonic()))); s.connect(str(a.socket))
                ev.write(json.dumps({'event':'connect','attempt':attempts,'identity':ident,'recreated':last_identity is not None and ident!=last_identity,'offset':offset,'monotonic_ns':time.monotonic_ns()},sort_keys=True)+'\n'); last_identity=ident
                while time.monotonic()<deadline:
                    try: b=s.recv(65536)
                    except socket.timeout: continue
                    if not b: break
                    out.write(b); offset+=len(b); ev.write(json.dumps({'event':'data','bytes':len(b),'offset':offset,'monotonic_ns':time.monotonic_ns()},sort_keys=True)+'\n')
                s.close(); ev.write(json.dumps({'event':'eof','offset':offset,'monotonic_ns':time.monotonic_ns()},sort_keys=True)+'\n')
            except (FileNotFoundError,ConnectionRefusedError,ConnectionResetError,OSError,RuntimeError) as e:
                ev.write(json.dumps({'event':'retry','error':type(e).__name__,'offset':offset,'monotonic_ns':time.monotonic_ns()},sort_keys=True)+'\n')
            time.sleep(a.retry)
    return 0
if __name__=='__main__': raise SystemExit(main())
