"""Explicit native passage edit. Reject changed owner inputs before any write."""
from pathlib import Path
import argparse,hashlib,json,struct,io
from PIL import Image
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
expected={'data/tilesets/legends_wyrmtide/metatiles.bin': '380e87f90337a945d90f735bb5893eb3b8c3385d', 'data/tilesets/legends_wyrmtide/metatile_attributes.bin': '0b3ce7209a3f9f9f37f5f53361e9384febbca152', 'data/tilesets/legends_wyrmtide/source.json': 'c14e662e8f01378de210a69085cd8dee03b39934', 'data/layouts/LegendsWyrmtide_Heart/map.bin': '0a28989e98a1fe5aced3323344f9b4fbc222c523', 'data/layouts/LegendsWyrmtide_Descent1/map.bin': 'ce1af4da60a76e50f5007d050efc8f44f48cae4e', 'data/layouts/LegendsWyrmtide_Descent2/map.bin': 'aab8ced4bd5179cb6708df38ed81bbc2dfc5c315', 'data/layouts/LegendsWyrmtide_Descent3/map.bin': '33c591442bbb1bc17d11141dc44bf37047974e5d', 'data/layouts/LegendsWyrmtide_Descent4/map.bin': '6c3ab2d2bb6bc2ffb428e7f024e9030db175974e', 'data/tilesets/legends_wyrmtide/tiles.png': '9d7b010fc5d66b9cc9fd8228c8de3ef4158f19d6', 'data/tilesets/secondary/cave/tiles.png': 'cd9a8370190b695bfdef79ab3cc7b8acfc3a6a5a'}
original={p:(R/p).read_bytes() for p in expected}
for p,b in original.items():assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==expected[p], 'Preserve changed owner input and reconcile: '+p
if not a.apply:print('All approved baseline inputs verified; use --apply for authorized passage edit.');raise SystemExit
S='data/tilesets/legends_wyrmtide/'
m=original[S+'metatiles.bin'];at=original[S+'metatile_attributes.bin'];assert len(m)==453*16
w=lambda mid:list(struct.unpack_from('<8H',m,(mid-512)*16))
source_arch=w(0x2fe)
new=[w(0x306)[:2]+w(mid)[2:4]+[0]*4 for mid in [0x3b1,0x3b2]]+[w(0x3b8)[:2]+w(0x306)[2:4]+[0]*4, [source_arch[0],0xa000+1012,source_arch[2],0xa000+1013]+[0]*4, [0xa000+1012,source_arch[1],0xa000+1013,source_arch[3]]+[0]*4]
pixels=Image.open(io.BytesIO(original[S+'tiles.png']));native=Image.open(io.BytesIO(original['data/tilesets/secondary/cave/tiles.png']))
assert not {x[0]&1023 for x in struct.iter_unpack('<H',m)}&{1012,1013}
for tile,word in [(1012,source_arch[0]),(1013,source_arch[2])]:
 index=(word&1023)-512
 for y in range(8):
  for x in range(8):pixels.putpixel(((tile-512)%16*8+x,(tile-512)//16*8+y),native.getpixel((index%16*8+7,index//16*8+y)))
image_bytes=io.BytesIO();pixels.save(image_bytes,format='PNG')
pending={S+'metatiles.bin':m+b''.join(struct.pack('<8H',*x) for x in new),S+'metatile_attributes.bin':at+struct.pack('<5H',0,0,0x65,0,0)}
pending[S+'tiles.png']=image_bytes.getvalue()
source=json.loads(original[S+'source.json']);source['interiorPassages']={'upperNativeAssembly':[[0x30e,0x3c8,0x3c9,0x2ff],[0x316,0x3c5,0x3c6,0x307]],'topLeft':[7,1],'upperTreadSources':[0x3b1,0x3b2],'shadowSource':0x306,'southStair':0x3c7,'southBehavior':0x65,'southTreadSource':0x3b8,'newPixelArt':False,'extendedArchInnerColumn':{'source':0x2fe,'x':7,'tiles':[1012,1013],'metatiles':[0x3c8,0x3c9]},'southFootShadeSource':0x306}
pending[S+'source.json']=(json.dumps(source,indent=2)+'\n').encode()
for i in range(1,5):
 path=f'data/layouts/LegendsWyrmtide_Descent{i}/map.bin';cells=list(struct.unpack('<456H',original[path]))
 for dy,row in enumerate(source['interiorPassages']['upperNativeAssembly']):
  for dx,mid in enumerate(row):
   idx=(1+dy)*19+7+dx;cells[idx]=(cells[idx]&0xfc00)|mid
 cells[20*19+11]=(cells[20*19+11]&0xfc00)|0x3c7;pending[path]=struct.pack('<456H',*cells)
path='data/layouts/LegendsWyrmtide_Heart/map.bin';cells=list(struct.unpack('<483H',original[path]));cells[16*23+11]=0x33b7;cells[17*23+11]=0x33c7;pending[path]=struct.pack('<483H',*cells)
for path,b in pending.items():(R/path).write_bytes(b)
print('Applied bounded native passage assembly; original warps/collision and all other terrain retained.')
