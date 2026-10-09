"""Validate every layered pose, binary offset/geometry and native furniture reuse."""
from pathlib import Path
import sys,re,struct,json
from PIL import Image
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools/legends'))
import build_accessories as art
import build_wardrobe_furniture as furniture
files=[root/p for p in ['src/data/legends/overworld_accessories.h','src/data/legends/trainer_accessories.h','src/data/legends/accessory_trainers.inc','include/constants/legends_accessory_trainers.inc','graphics/legends/accessories/overworld.bin','graphics/legends/accessories/trainers.bin','tools/legends/accessory_asset_manifest.json']]
before=[p.read_bytes() for p in files];art.build();assert before==[p.read_bytes() for p in files]
count=0
for g,name in enumerate(('brendan','may')):
 cases=[('overworld',root/f'graphics/object_events/pics/people/{name}/{file}.png',16 if i==0 else 32) for i,file in enumerate(art.FILES)]
 cases+=[('overworld',root/f'graphics/object_events/pics/people/{name}/running.png',16)]
 cases += [(kind,root/f'graphics/trainers/{kind}_pics/{name}.png',64) for kind in ('front','back')]
 for kind,path,width in cases:
  for pose,frame in enumerate(art.frames(path,width,32 if kind=='overworld' else 64)):
   groups=art.skin_components(frame)
   face=(max(groups,key=len) if kind=='overworld' else min((c for c in groups if len(c)>30),key=lambda c:min(y for x,y in c))) if groups else set()
   for outfit in range(5):
    base=art.outfit_frame(frame,g,outfit,kind,pose,path.stem)
    for style in (1,2,3):
     result=art.accessory_frame(frame,g,outfit,style,kind,pose,path.stem)
     assert all(result[y][x]==frame[y][x] for x,y in face),(path,pose,'face')
     assert all((v==0)==(result[y][x]==0) for y,row in enumerate(frame) for x,v in enumerate(row))
     if kind!='overworld':
      for x,y in art.ball_pixels(g,kind,pose)|art.hand_pixels(g,kind,pose):
       assert result[y][x]==(9 if base[y][x]==14 else base[y][x]),(path,pose,'hands/ball')
     assert len(art.pack(result))==width*len(frame)//2
     count+=1
pose_count=count
# Binary C pointers cover the complete pack without out-of-bounds reads.
manifest=json.loads((root/'tools/legends/accessory_asset_manifest.json').read_text())
for h,binary,pattern in [('overworld_accessories.h','overworld.bin',r'#define (s\w+) \(sLegendsAccessoryOverworldData \+ (\d+)\)'),('trainer_accessories.h','trainers.bin',r'#define (g\w+) \(\(const \w+ \*\)\(gLegendsAccessoryTrainerData \+ (\d+)\)\)')]:
 data=(root/'graphics/legends/accessories'/binary).read_bytes();text=(root/'src/data/legends'/h).read_text();end=0
 for name,offset in re.findall(pattern,text):
  offset=int(offset);assert offset==end and offset%4==0
  entry=manifest[name];size=entry['bytes'];end=offset+(4+size+(size+7)//8+3)//4*4 if name.endswith('Front') else offset+size
  assert end<=len(data)
  if name.endswith('Front'):assert data[offset]==0x10 and int.from_bytes(data[offset+1:offset+4],'little')==2048
 assert end==len(data)
# Reserve only previously unreferenced blank primary tiles; preserve all native IDs.
primary=root/'data/tilesets/primary/secret_base';secondary=root/'data/tilesets/secondary/secret_base'
used={v&1023 for p,count in [(primary,2),(secondary,324)] for v in struct.unpack('<'+str(count*8)+'H',(p/'metatiles.bin').read_bytes()[:count*16])}
assert not set(range(464,472))&used
for p,count in [(secondary,326),(root/'data/tilesets/secondary/brendans_mays_house',198)]:
 assert len((p/'metatiles.bin').read_bytes())==count*16
 assert len((p/'metatile_attributes.bin').read_bytes())==count*2
paths=[primary/'tiles.png',secondary/'metatiles.bin',secondary/'metatile_attributes.bin']
paths += [root/'data/tilesets/secondary/brendans_mays_house'/f for f in ['tiles.png','metatiles.bin','metatile_attributes.bin']]
before=[p.read_bytes() for p in paths];furniture.build();assert before==[p.read_bytes() for p in paths]
print(f'{pose_count} accessory poses: faces/hands/balls, geometry, 300 binary blocks and cabinet reuse/reproducibility passed')
