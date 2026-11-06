"""Clean only the lower exit detail; reject changed owner inputs before writing."""
from pathlib import Path
import argparse,hashlib,json,struct
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
expected={'data/tilesets/legends_wyrmtide/metatiles.bin': '2e267d2a6c8b4cece42cb2f13ccc59f0fc0803f0', 'data/tilesets/legends_wyrmtide/metatile_attributes.bin': '95ca65e316359eceb8eeb5bad800b01af2820a49', 'data/tilesets/legends_wyrmtide/source.json': '72fc8c74516414515683894a9d466f1b372e88bc', 'data/layouts/LegendsWyrmtide_Descent1/map.bin': 'ab624428232d730af4c8415b52959494e4851ac0', 'data/layouts/LegendsWyrmtide_Descent2/map.bin': '3983cc875fd7b6e9b962099bc77a09cdefef7ff9', 'data/layouts/LegendsWyrmtide_Descent3/map.bin': 'f9ce446371d684124a4107e30f076a6c413e4f2b', 'data/layouts/LegendsWyrmtide_Descent4/map.bin': 'c3cb66f102c0bb937c27f5bad1dc8a6258829677'}
original={f:(R/f).read_bytes() for f in expected}
for f,b in original.items():assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==expected[f], 'Preserve changed owner input and reconcile: '+f
S='data/tilesets/legends_wyrmtide/';m=bytearray(original[S+'metatiles.bin']);at=original[S+'metatile_attributes.bin'];assert len(m)==458*16
words=lambda mid:list(struct.unpack_from('<8H',m,(mid-512)*16))
floor=words(0x201);edge=words(0x218)
# Two compact stone returns use the native cap's inner half. Retain floor
# pixels outside the rim and mirror only the left return's stone edge.
left=[floor[0],edge[0]^0x400,floor[2],edge[2]^0x400]+[0]*4
right=[edge[0],floor[1],edge[2],floor[3]]+[0]*4
struct.pack_into('<8H',m,(0x3c7-512)*16,*(words(0x3b8)[:2]+words(0x206)[2:4]+[0]*4))
m.extend(struct.pack('<16H',*(left+right)))
pending={S+'metatiles.bin':bytes(m),S+'metatile_attributes.bin':at+struct.pack('<2H',0,0)}
source=json.loads(original[S+'source.json']);source['interiorPassages']['southFootShadeSource']=0x206
source['lowerExitCleanup']={'metatiles':[0x3ca,0x3cb],'flankSource':0x218,'floorSource':0x201,'innerWidthPixels':8,'leftStoneMirrored':True,'treadsSource':0x3b8,'shadeSource':0x206,'centerWarp':0x3c7,'nativeSouthBehavior':0x65,'newPixelArt':False,'newPalette':False,'collisionAndWarpsUnchanged':True}
pending[S+'source.json']=(json.dumps(source,indent=2)+'\n').encode()
for i in range(1,5):
 f=f'data/layouts/LegendsWyrmtide_Descent{i}/map.bin';cells=list(struct.unpack('<456H',original[f]))
 for x,old,new in [(10,0x218,0x3ca),(12,0x21a,0x3cb)]:
  idx=20*19+x;assert cells[idx]&1023==old;cells[idx]=(cells[idx]&0xfc00)|new
 pending[f]=struct.pack('<456H',*cells)
if not a.apply:print('All approved inputs verified; use --apply for the bounded exit cleanup.');raise SystemExit
for f,b in pending.items():(R/f).write_bytes(b)
print('Cleaned the lower exit rim/recess; native tread, behavior, collision, warps and all other approved assets retained.')
