"""Run the real sparse compositor on every native pose; protect actual faces.
Reproduce masks, check every ROM edit bound, exercise scarf order and defaults.
"""
import sys,re,struct,subprocess,tempfile,ctypes,json
from pathlib import Path
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools/legends'))
import build_style_layers as art
assert all(m!=f for m,f in zip(art.SHAPES,art.FEMALE_SHAPES)), 'ten independent contours per gender'
from PIL import Image,ImageDraw
for male,female in zip(art.SHAPES,art.FEMALE_SHAPES):
 masks=[]
 for contour in (male,female):
  im=Image.new('1',(18,20));ImageDraw.Draw(im).polygon(contour,fill=1)
  masks.append(im.resize((12,10),Image.Resampling.NEAREST).tobytes())
 assert masks[0]!=masks[1], 'gender contours must differ at overworld scale'
from build_appearance import frames,pack,STATES,FILES
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
#define TRUE 1
#define FALSE 0
u8 scarf;
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
   protected=set(face)
   if kind:protected |= {(x,y) for x,y in art.hand_pixels(g,'front' if kind==1 else 'back',native_index) if p[y][x] not in (4,7,8)}|art.ball_pixels(g,'front' if kind==1 else 'back',native_index)
   for hair in range(11):
    for coat in range(3):
     buf=(ctypes.c_uint8*len(native)).from_buffer_copy(native)
     painter(buf,w,g,kind,state,slot,hair,coat)
     raw=bytes(buf);out=unpack(raw,w,h)
     if not hair and not coat or kind==0 and state==4:assert raw==native
     for x,y in protected:assert out[y][x]==p[y][x],(name,kind,state,slot,hair,coat,'face/hand/ball',x,y)
     if coat==0:signatures.add(raw)
     # Same custom hair under both coats: accessories cannot repaint its crown.
     if hair and not (kind==0 and state==4):
      plain=(ctypes.c_uint8*len(native)).from_buffer_copy(native);painter(plain,w,g,kind,state,slot,hair,0)
      crown=unpack(bytes(plain),w,h)
      for y in range(h):
       for x in range(w):
        if crown[y][x]!=p[y][x] and crown[y][x] in (4,8):assert out[y][x]==crown[y][x]
   if kind==1:assert len(signatures)==11,(name,'distinct portraits')
   if (state!=4 or kind) and groups:assert len(signatures)>=5,(name,kind,state,slot,'distinct hairstyles')
   poses+=1
 # Invalid settings and diving are safely ignored.
 for g,kind,state,pose,hair,coat in ((2,0,0,0,1,2),(0,0,8,0,1,2),(0,0,4,0,1,2),(0,2,0,4,1,2),(0,1,0,0,11,2),(0,1,0,0,1,3)):
  buf=(ctypes.c_uint8*2048)();painter(buf,64,g,kind,state,pose,hair,coat);assert bytes(buf)==bytes(2048)
print(f'{poses} native table poses: reproducible sparse art, 11 portraits, face/hand/ball isolation, coat/hair order and diving defaults passed')
