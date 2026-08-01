#!/usr/bin/env python3
"""Owner-only HTTP client for one bound Cloud Hypervisor v53.0 API socket."""
from __future__ import annotations
import argparse,json,os,socket,stat,sys
from pathlib import Path

ROUTES={
 'ping':('GET','/api/v1/vmm.ping'), 'create':('PUT','/api/v1/vm.create'),
 'boot':('PUT','/api/v1/vm.boot'), 'info':('GET','/api/v1/vm.info'),
 'reboot':('PUT','/api/v1/vm.reboot'), 'shutdown':('PUT','/api/v1/vm.shutdown'),
 'delete':('PUT','/api/v1/vm.delete'), 'vmm-shutdown':('PUT','/api/v1/vmm.shutdown')}

def safe_socket(path:Path)->None:
 st=path.lstat()
 if stat.S_ISLNK(st.st_mode) or not stat.S_ISSOCK(st.st_mode): raise RuntimeError('API path is not a direct socket')
 if st.st_uid!=0 or stat.S_IMODE(st.st_mode)&0o077: raise RuntimeError('API socket ownership or mode mismatch')
 if not path.is_absolute() or '..' in path.parts: raise RuntimeError('API socket path invalid')

def main()->int:
 p=argparse.ArgumentParser(); p.add_argument('--socket',type=Path,required=True); p.add_argument('--action',choices=ROUTES,required=True); p.add_argument('--request',type=Path); p.add_argument('--response',type=Path); p.add_argument('--expect',type=int,action='append'); a=p.parse_args()
 try:
  safe_socket(a.socket); method,route=ROUTES[a.action]; body=b''
  if a.request:
   st=a.request.lstat()
   if stat.S_ISLNK(st.st_mode) or not stat.S_ISREG(st.st_mode) or st.st_uid!=0 or stat.S_IMODE(st.st_mode)!=0o600: raise RuntimeError('unsafe request file')
   body=a.request.read_bytes(); json.loads(body)
  elif a.action=='create': raise RuntimeError('create requires request file')
  req=(f'{method} {route} HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n\r\n').encode('ascii')+body
  s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM); s.settimeout(30); s.connect(str(a.socket)); s.sendall(req)
  raw=bytearray()
  while b'\r\n\r\n' not in raw:
   b=s.recv(65536)
   if not b: raise RuntimeError('HTTP response ended before headers')
   raw.extend(b)
   if len(raw)>65536: raise RuntimeError('HTTP response headers too large')
  head,_,initial=bytes(raw).partition(b'\r\n\r\n')
  first=head.splitlines()[0].decode('ascii','strict'); status=int(first.split()[1])
  headers={}
  for line in head.splitlines()[1:]:
   if b':' not in line: raise RuntimeError('malformed HTTP header')
   k,v=line.split(b':',1); headers[k.strip().lower()]=v.strip()
  length=int(headers.get(b'content-length',b'0'))
  if length<0 or length>64*1024*1024: raise RuntimeError('invalid HTTP Content-Length')
  payload=bytearray(initial)
  while len(payload)<length:
   b=s.recv(min(65536,length-len(payload)))
   if not b: raise RuntimeError('HTTP response body truncated')
   payload.extend(b)
  s.close(); payload=bytes(payload[:length])
  allowed=a.expect or [200,204]
  if a.response:
   if not a.response.is_absolute() or '..' in a.response.parts: raise RuntimeError('response path invalid')
   tmp=a.response.with_name(a.response.name+'.stage'); tmp.write_bytes(payload); os.chmod(tmp,0o600); os.replace(tmp,a.response)
  print(json.dumps({'action':a.action,'status':status,'response_bytes':len(payload)},sort_keys=True))
  if status not in allowed:
   print(payload[:4096].decode('utf-8','replace'),file=sys.stderr); return 72
  return 0
 except Exception as e:
  print(f'VMM API refused: {e}',file=sys.stderr); return 72
if __name__=='__main__': raise SystemExit(main())
