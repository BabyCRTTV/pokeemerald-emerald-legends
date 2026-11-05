"""Explicit review-only water edit. Refuse changed inputs before writing.
Uses native metatile pixels and animated water, private palette13, and native
night/day palette entries5/12. Never regenerates the approved shore or Heart.
"""
from pathlib import Path
import hashlib,json,struct
R=Path(__file__).resolve().parents[2]
expected={"data/layouts/LegendsWyrmtide_Descent2/map.bin":"d69e5f79ea2a6a2dca4554caefa38549b0566071","data/tilesets/legends_wyrmtide/metatiles.bin":"48b0ed899160938e06c435dd7fba75126f132db5","data/tilesets/legends_wyrmtide/metatile_attributes.bin":"13813447956849ffb6dbc699130446097a461307"}
for f,h in expected.items():
 b=(R/f).read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==h,'Preserve changed map/art and reconcile: '+f
S=R/'data/tilesets/legends_wyrmtide'
m=(S/'metatiles.bin').read_bytes();at=(S/'metatile_attributes.bin').read_bytes()
assert len(m)==6784 and len(at)==848
assert 13 not in {v[0]>>12 for v in struct.iter_unpack('<H',m)}
water=[0xd1c6,0xd1c7,0xd1c7,0xd1c6];extras=[];attrs=[]
for n in range(0x3a0,0x3a8):
 extras.extend(water+list(struct.unpack_from('<8H',m,(n-512)*16))[4:])
 attrs.append(struct.unpack_from('<H',at,(n-512)*2)[0])
extras.extend(water+[0]*4);attrs.append(struct.unpack_from('<H',at,(0x27b-512)*2)[0])
(S/'metatiles.bin').write_bytes(m+struct.pack('<72H',*extras))
(S/'metatile_attributes.bin').write_bytes(at+struct.pack('<9H',*attrs))
general=(R/'data/tilesets/primary/general/palettes/04.pal').read_text().splitlines()[3:19]
cave=(R/'data/tilesets/secondary/cave/palettes/03.pal').read_text().splitlines()[3:19]
colors=[cave[8]]*16
colors[11]=general[9];colors[12]=general[10];colors[13]=cave[7];colors[14]=cave[8]
(S/'water.pal').write_text('JASC-PAL\n0100\n16\n'+'\n'.join(colors)+'\n')
p=R/'data/layouts/LegendsWyrmtide_Descent2/map.bin';a=list(struct.unpack('<456H',p.read_bytes()))
def put(x,y,t,solid=False):a[y*19+x]=0x3000|(0x400 if solid else 0)|t
for y in range(6,11):
 for x in range(11,16):put(x,y,0x201)
for y in range(6,10):
 for x in range(12,16):
  t=0x3b0
  if y==6:t=0x3a8 if x==12 else 0x3aa if x==15 else 0x3a9
  elif y==9:t=0x3ad if x==12 else 0x3af if x==15 else 0x3ae
  elif x==12:t=0x3ab
  elif x==15:t=0x3ac
  put(x,y,t,True)
put(10,9,0x209,True);put(10,10,0x219,True)
put(11,9,0x20a,True);put(11,10,0x21a,True)
p.write_bytes(struct.pack('<456H',*a))
print('Authored pool-only palette and complete rock-bank join; source pixels unchanged.')
