"""Explicit upper-return stair edit; reject changed owner inputs before writing."""
from pathlib import Path
import argparse, hashlib, json, struct
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
expected={
'data/tilesets/legends_wyrmtide/metatiles.bin':'2387a7f9f9d7291f6c4d92cd93bbccbb905bbbad',
'data/tilesets/legends_wyrmtide/metatile_attributes.bin':'3a96dc76d36d288720e9cb662381ad487bfd11b5',
'data/tilesets/legends_wyrmtide/source.json':'27199d5dff0a2fd7dc3772bec419fa8faf9eb061',
}
for i,(layout,events) in enumerate(zip(
['5944fea6a94364090a1f72c481c78c3bd523fd88','64e17d52cec4a26d7985aa5ae9b3d77f6f10ae7a','7625c9988b58e89ebea06e44d98ca76306dda0ff','338fc1d7d833d89023951bba9633573d70422b62'],
['c0a5c25569a46d1a5a0cd6718d91e9a76224abae','a8faad8818590bd7f91c122d09f8140be5a00804','8f93cfe4342719b3a4282a76d28ff53697985fee','e128309f8413bd95104991e4488fc612835595d7']),1):
 expected[f'data/layouts/LegendsWyrmtide_Descent{i}/map.bin']=layout
 expected[f'data/maps/LegendsWyrmtide_Descent{i}/map.json']=events
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
original={f:(R/f).read_bytes() for f in expected}
for f,h in expected.items():assert blob(original[f])==h,'Preserve changed owner input and reconcile: '+f
S='data/tilesets/legends_wyrmtide/'
m=original[S+'metatiles.bin'];at=original[S+'metatile_attributes.bin']
assert len(m)==449*16
words=lambda mid:list(struct.unpack_from('<8H',m,(mid-512)*16))
canopy=words(0x2f9)[4:6]
new=[words(0x3b1)[:4]+canopy+[0,0],words(0x3b2)[:4]+canopy+[0,0],words(0x3b3),words(0x3b4)]
pending={S+'metatiles.bin':m+b''.join(struct.pack('<8H',*w) for w in new),S+'metatile_attributes.bin':at+struct.pack('<4H',0,0,0x61,0x61)}
source=json.loads(original[S+'source.json'])
source['upperStairwell']={'metatiles':[0x3c1,0x3c4],'sourceTreads':[0x3b1,0x3b2,0x3b3,0x3b4],'canopySource':0x2f9,'nativeEndCaps':[0x2fa,0x2f8],'liveReturnColumns':[8,9],'warpRow':3,'originalWarpIndicesPreserved':True,'newAliasWarpIndex':2,'newPixelArt':False}
pending[S+'source.json']=(json.dumps(source,indent=2)+'\n').encode()
changes=[(7,2,0x2fa,True),(8,2,0x3c1,False),(9,2,0x3c2,False),(10,2,0x2f8,True),(8,3,0x3c3,False),(9,3,0x3c4,False)]
for i in range(1,5):
 f=f'data/layouts/LegendsWyrmtide_Descent{i}/map.bin';cells=list(struct.unpack('<456H',original[f]))
 for x,y,mid,solid in changes:cells[y*19+x]=(cells[y*19+x]&0xf000)|mid|(0x400 if solid else 0)
 pending[f]=struct.pack('<456H',*cells)
 f=f'data/maps/LegendsWyrmtide_Descent{i}/map.json';events=json.loads(original[f]);assert len(events['warp_events'])==2
 events['warp_events'].append({**events['warp_events'][0],'x':9})
 pending[f]=(json.dumps(events,indent=2)+'\n').encode()
if not a.apply:print('Verified all inputs. Use --apply for the authorized upper stairwell edit.');raise SystemExit
for f,b in pending.items():(R/f).write_bytes(b)
proof=R/'build/stairwell/authoring.json';proof.parent.mkdir(parents=True,exist_ok=True)
proof.write_text(json.dumps({'baseline':'9625cb0d51023f6b35bd25bd8b49bdfef7794146','before':expected,'after':{f:blob(b) for f,b in pending.items()},'collisionChange':'Only (9,2) becomes walkable in each descent room.','warpChange':'Append alias2 at (9,3), preserving original indices0/1.','newPixelArt':False},indent=2)+'\n')
print('Applied four fitted two-column upper return stairwells, preserving native art and original warp IDs.')
