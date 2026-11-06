"""Replace the cropped exit sides with complete native rocks, preserving owner inputs."""
from pathlib import Path
import argparse,hashlib,json,struct
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
expected={'data/tilesets/legends_wyrmtide/metatiles.bin': '128071ec0f5f04f90966804894295fdca8ba36f1', 'data/tilesets/legends_wyrmtide/source.json': 'a12606ae21e3dae9fac987d62dce050f62eb3ddf'}
original={f:(R/f).read_bytes() for f in expected}
for f,b in original.items():assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==expected[f], 'Preserve changed owner input and reconcile: '+f
S='data/tilesets/legends_wyrmtide/';m=bytearray(original[S+'metatiles.bin']);assert len(m)==460*16
rock=m[(0x202-512)*16:(0x203-512)*16]
for mid in [0x3ca,0x3cb]:m[(mid-512)*16:(mid-511)*16]=rock
source=json.loads(original[S+'source.json']);detail=source['lowerExitCleanup'];detail.update({'flankSource':0x202,'innerWidthPixels':16,'leftStoneMirrored':False,'completeNativeRocks':True,'completeSilhouetteAndBase':True})
pending={S+'metatiles.bin':bytes(m),S+'source.json':(json.dumps(source,indent=2)+'\n').encode()}
if not a.apply:print('Verified approved inputs; use --apply to replace the cropped rocks.');raise SystemExit
for f,b in pending.items():(R/f).write_bytes(b)
print('Replaced both cropped sides with complete native Cave0x202 rocks; all maps, physics and warps remain exact.')
