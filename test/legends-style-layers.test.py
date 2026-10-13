"""Run the real sparse compositor on every native pose; protect actual faces.
Reproduce masks, check every ROM edit bound, exercise scarf order and defaults.
"""
import sys,re,struct,subprocess,tempfile,ctypes,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools/legends'))
import build_style_layers as art
from hair_pixels import MALE, FEMALE, WORLD_MALE, WORLD_FEMALE
assert len(MALE) == len(FEMALE) == len(WORLD_MALE) == len(WORLD_FEMALE) == 10
assert all(m != f for m,f in zip(MALE,FEMALE))
assert all(m != f for m,f in zip(WORLD_MALE,WORLD_FEMALE))
assert len({tuple(r) for r in WORLD_MALE}) == len({tuple(r) for r in WORLD_FEMALE}) == 10
from build_appearance import frames,pack,STATES,FILES
walking=frames(root/'graphics/object_events/pics/people/brendan/walking.png',16,32)[0]
assert art.hair_edits(walking,0,'overworld',0,1)[10][10]==0, 'clear native hat tip above new crown'
# The reported glitch changed facing on alternate steps. Check against the
# actual native animation commands, not a second copy of the authoring table.
anims=(root/'src/data/object_events/object_event_anims.h').read_text()
for name,direction in (('South',0),('North',2),('West',1),('East',1)):
 for motion in ('Go','GoFast','GoFaster','GoFastest','Run'):
  body=re.search(r'sAnim_'+motion+name+r'\[\]\s*=\s*\{(.*?)\};',anims,re.S)[1]
  for frame in map(int,re.findall(r'ANIMCMD_FRAME\((\d+)',body)):
   assert art.WORLD_DIRECTIONS['walking'][frame]==direction,(motion,name,frame)
   if motion!='Run':assert art.WORLD_DIRECTIONS['mach_bike'][frame]==direction
# Read every native trick sequence; lateral back-wheel poses 23/24 face north.
for motion in ('BunnyHopBackWheel','BunnyHopFrontWheel','StandingWheelieBackWheel','StandingWheelieFrontWheel','MovingWheelie'):
 for name,direction in (('South',0),('North',2),('West',1),('East',1)):
  body=re.search(r'sAnim_'+motion+name+r'\[\]\s*=\s*\{(.*?)\};',anims,re.S)[1]
  for frame in map(int,re.findall(r'ANIMCMD_FRAME\((\d+)',body)):
   assert art.WORLD_DIRECTIONS['acro_bike'][frame]==direction,(motion,name,frame)
for state in ('surfing','watering'):
 assert [art.WORLD_DIRECTIONS[state][i] for i in (0,2,4)]==[0,2,1]
assets=[root/'graphics/legends/styles/edits.bin',root/'src/data/legends/style_layers.h']
before=[p.read_bytes() for p in assets];art.build();assert before==[p.read_bytes() for p in assets]
header=assets[1].read_text();edits=struct.unpack('<'+'H'*(len(before[0])//2),before[0])
header=re.sub(r'static const u16 sStylePixels\[\] = INCBIN_U16\([^;]+;', 'static const u16 sStylePixels[]={'+','.join(map(str,edits))+'};',header)
source='\n'.join(l for l in (root/'src/legends_style_layers.c').read_text().splitlines() if not l.startswith('#include'))
pre='''
#include <stdint.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef uint8_t bool8;
#define LEGENDS_HAIR_COUNT 11
#define LEGENDS_JACKET_COUNT 3
#define FEMALE 1
u8 LegendsGetLeggings(void){return 0;}
#define TRUE 1
#define FALSE 0
u8 scarf;u8 color;
u8 LegendsGetHairColor(void){return color;}
u8 LegendsGetScarf(void){return scarf;}
'''
def unpack(raw,w,h):
 return [[(raw[((y//8)*(w//8)+x//8)*32+(y%8)*4+(x%8)//2]>>((x%2)*4))&15 for x in range(w)] for y in range(h)]
mapping=json.loads((root/'tools/legends/appearance_frames.json').read_text())
with tempfile.TemporaryDirectory() as d:
 path=Path(d)/'style.c';path.write_text(pre+header+source)
 lib=Path(d)/'style.so';subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC',str(path),'-o',str(lib)],check=True)
 api=ctypes.CDLL(str(lib));painter=api.LegendsPaintStylePose
 painter.argtypes=[ctypes.POINTER(ctypes.c_uint8)]+[ctypes.c_uint8]*7
 poses=0
 for g,name in enumerate(('Brendan','May')):
  cases=[]
  for state,file in enumerate(FILES):
   w=16 if state==0 else 32;p=root/f'graphics/object_events/pics/people/{name.lower()}/{file}.png';src=frames(p,w,32)
   if state==0:src+=frames(p.with_name('running.png'),16,32)
   table=mapping[name][STATES[state]]['table'];idx=list(range(len(src))) if 'overworld_ascending_frames' in table else [int(v) for v in re.findall(r'overworld_frame\([^,]+,\s*\d+,\s*\d+,\s*(\d+)\)',table)]
   cases.extend((src[i],w,0,state,slot,i) for slot,i in enumerate(idx))
  cases.extend((f,64,kind,0,i,i) for kind,folder in ((1,'front'),(2,'back')) for i,f in enumerate(frames(root/f'graphics/trainers/{folder}_pics/{name.lower()}.png',64,64)))
  for p,w,kind,state,slot,native_index in cases:
   h=len(p);native=pack(p);signatures=set()
   groups=art.skin_components(p)
   face=(max(groups,key=len) if kind==0 else min((s for s in groups if len(s)>30),key=lambda s:min(y for x,y in s))) if groups else set()
   if kind==2:face=art.head(p,g,'back',native_index)[0]
   protected=set(face)
   if face:
    left,right=min(x for x,y in face),max(x for x,y in face)
    top,bottom=min(y for x,y in face),max(y for x,y in face)
    protected |= {(x,y) for y in range(top,bottom+1) for x in range(left,right+1) if p[y][x] in (5,8,9,14,15)}
   if kind:protected |= art.coat_hands(g,'front' if kind==1 else 'back',native_index)|art.ball_pixels(g,'front' if kind==1 else 'back',native_index)
   rear_walking = g == 0 and kind == 0 and state == 0 and art.WORLD_DIRECTIONS['walking'][native_index] == 2
   if rear_walking:
    # A rear head has ears/neck, not eyes or a forehead. The white native
    # cap between the ears must not be classified as protected face art.
    ear_y = min(y for y,row in enumerate(p) if any(v in (1,2,3) for v in row))
    protected = {(x,y) for y,row in enumerate(p) for x,v in enumerate(row) if v in (1,2,3) and y <= ear_y + 2}
    protected |= {(x,y) for y in (ear_y,ear_y+1) for x in (0,1,2,13,14,15) if p[y][x]}
   for hair in range(11):
    for coat in range(3):
     buf=(ctypes.c_uint8*len(native)).from_buffer_copy(native)
     painter(buf,w,g,kind,state,slot,hair,coat)
     raw=bytes(buf);out=unpack(raw,w,h)
     if not hair and not coat or kind==0 and state==4:assert raw==native
     if g==1 and kind==1 and hair:
      assert out[24][22] == out[26][21] == out[27][21] == 0,(name,hair,coat,'shoulder remnants')
     if g==1 and kind==2 and hair:
      # Retired native lock tips must not float beside a shorter custom cut.
      x,y=((55,41),(62,38),(49,35),(56,40))[native_index]
      assert p[y][x] and out[y][x]==0,(name,slot,hair,coat,'native lock remnant')
     if kind==0 and state==6:
      for x,y in art.fishing_rod(p,g,native_index):
       assert out[y][x]==p[y][x],(name,slot,hair,coat,'fishing rod',x,y)
     for x,y in protected:assert out[y][x]==p[y][x],(name,kind,state,slot,hair,coat,'face/hand/ball',x,y)
     if rear_walking and hair:
      assert all(out[y][x] not in (9,14) for y in range(ear_y-8,ear_y+2) for x in range(3,13)),(name,slot,hair,'native cap remnant')
     if coat and kind==2:
      for y,row in enumerate(p):
       for x,v in enumerate(row):
        if v in (1,2,3) and (x,y) not in protected:
         assert out[y][x] in (10,15), (name,slot,'exposed forearm',x,y)
     if coat==0:signatures.add(raw)
     # Same custom hair under both coats: accessories cannot repaint its crown.
     if hair and not (kind==0 and state==4):
      plain=(ctypes.c_uint8*len(native)).from_buffer_copy(native);painter(plain,w,g,kind,state,slot,hair,0)
      crown=unpack(bytes(plain),w,h)
      for y in range(h):
       for x in range(w):
        if crown[y][x]!=p[y][x] and crown[y][x] in (4,8):assert out[y][x]==crown[y][x]
   if kind==1:assert len(signatures)==11,(name,'distinct portraits')
   if rear_walking:assert len(signatures)==11,(name,slot,'eleven distinct rear cuts')
   if (state!=4 or kind) and (groups or kind==0 and art.WORLD_DIRECTIONS.get(FILES[state],())[native_index]==2):assert len(signatures)>=5,(name,kind,state,slot,'distinct hairstyles')
   if not (kind==0 and state==4):
    core=art.head_core(p,g,'overworld' if kind==0 else 'front' if kind==1 else 'back',native_index,FILES[state] if kind==0 else '')
    if rear_walking:
     # Check the skull interior anchored to actual native ears. The former
     # core included Brendan's protruding cap brim, which is now removed.
     core={(x,y) for y in range(ear_y-5,ear_y+2) for x in range(5,11)}
    for hair in range(1,11):
     buf=(ctypes.c_uint8*len(native)).from_buffer_copy(native);painter(buf,w,g,kind,state,slot,hair,0)
     out=unpack(bytes(buf),w,h)
     assert all(out[y][x] for x,y in core), (name,kind,state,slot,hair,'incomplete head')
   poses+=1
 # Invalid settings and diving are safely ignored.
 for g,kind,state,pose,hair,coat in ((2,0,0,0,1,2),(0,0,8,0,1,2),(0,0,4,0,1,2),(0,2,0,4,1,2),(0,1,0,0,11,2),(0,1,0,0,1,3)):
  buf=(ctypes.c_uint8*2048)();painter(buf,64,g,kind,state,pose,hair,coat);assert bytes(buf)==bytes(2048)
print(f'{poses} native table poses: reproducible sparse art, 11 portraits, face/hand/ball isolation, coat/hair order and diving defaults passed')
