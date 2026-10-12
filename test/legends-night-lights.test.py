"""Audit day-identical tile cells and run the shipped C DNS color mixer."""
from pathlib import Path
from PIL import Image
import json,struct,sys,subprocess,tempfile,ctypes
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'tools/legends'))
import build_night_lights as art
out=R/'data/tilesets/legends_lights';assets=list(out.iterdir())+list((R/'src/data/tilesets').glob('*.h'))+[R/'src/graphics.c']
before={str(p):p.read_bytes() for p in assets};art.main();assert before=={str(p):p.read_bytes() for p in assets},'Non-reproducible light assets'
m=json.loads((out/'manifest.json').read_text())
for name,f in m['families'].items():
 native=R/'data/tilesets/primary'/name;im=Image.open(native/'tiles.png');lit=Image.open(out/(name+'_tiles.png'))
 a=art.words(native/'metatiles.bin');b=art.words(out/(name+'_metatiles.bin'));changed={c['metatile']*8+c['cell'] for c in f['cells']}
 assert all(x==y for i,(x,y) in enumerate(zip(a,b)) if i not in changed),'An unlit roof/path/wall changed'
 palettes=[art.palette(native/'palettes'/f'{i:02}.pal') for i in range(7)];newpal=art.palette(out/(name+'.pal'))
 reserved={c['tile'] for c in f['cells']};used={e&1023 for e in a}
 for s in m['secondary']:
  if s['family']==name:used.update(e&1023 for e in art.words(R/s['metatiles']))
 assert not (reserved&used),'Light art overwrote a live tile'
 assert not reserved&set(range(416,512)),'Light art overlaps animation DMA'
 for cell in f['cells']:
  x=art.tile(im,cell['source_tile']);y=art.tile(lit,cell['tile']);p=palettes[cell['source_palette']]
  for yy in range(8):
   for xx in range(8):
    old=x.getpixel((xx,yy));new=y.getpixel((xx,yy))
    assert bool(old)==bool(new),'Transparent cell changed'
    if old:assert p[old]==newpal[new],(name,cell,'Daytime RGB changed')
 flags={int(l) for l in (out/(name+'.pla')).read_text().splitlines() if l and not l.startswith('#')}
 assert flags=={i+1 for i,c in enumerate(f['colors']) if c['light']}
 assert flags and 0 not in flags
 # Walls and sign borders remain ordinary tinted colors in the same palette.
 assert len(flags)<len(f['colors'])
for g in m['glass_palettes']:
 assert art.palette(R/g['native'])==art.palette(R/g['palette'])
 assert set(g['lights'])=={8,9,10}
# Exercise the real mixer, including night tint and dawn/day interpolation.
source=(R/'src/palette.c').read_text().split('#define DEFAULT_LIGHT_COLOR')[1].split('// Apply weighted average')[0]
source='#define DEFAULT_LIGHT_COLOR'+source
pre='''
#include <stdint.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int32_t s32;typedef uint8_t bool8;
#define RGB2(r,g,b) ((r)|((g)<<5)|((b)<<10))
#define RGB2GBA(r,g,b) RGB2((r)>>3,(g)>>3,(b)>>3)
struct BlendSettings {u32 blendColor;u8 coeff;bool8 isTint;};
'''
class Blend(ctypes.Structure):_fields_=[('blendColor',ctypes.c_uint32),('coeff',ctypes.c_uint8),('isTint',ctypes.c_uint8)]
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'mix.c').write_text(pre+source);subprocess.run(['cc','-Wall','-Werror','-shared','-fPIC',str(p/'mix.c'),'-o',str(p/'mix.so')],check=True)
 fn=ctypes.CDLL(str(p/'mix.so')).TimeMixPalettes;day=Blend(0,0,0);night=Blend(116|(116<<8)|(157<<16),10,1)
 for name,f in m['families'].items():
  rgb=art.palette(out/(name+'.pal'));flags={int(l) for l in (out/(name+'.pla')).read_text().splitlines() if l and not l.startswith('#')}
  colors=[(r>>3)|((g>>3)<<5)|((b>>3)<<10)|(0x8000 if i in flags else 0) for i,(r,g,b) in enumerate(rgb)]
  src=(ctypes.c_uint16*16)(*colors);dst=(ctypes.c_uint16*16)(*colors)
  fn(1,src,dst,ctypes.byref(day),ctypes.byref(day),256)
  assert list(dst)[1:]==[c&0x7fff for c in colors[1:]],'Daytime lights alter native colors'
  fn(1,src,dst,ctypes.byref(night),ctypes.byref(night),256)
  for i in range(1,len(f['colors'])+1):
   channels=lambda c:(c&31,(c>>5)&31,(c>>10)&31)
   original=channels(colors[i]);actual=channels(dst[i])
   if i in flags:assert sum(actual[:2])>=sum(original[:2]),(name,i,'Dark light')
   else:assert all(x<=y for x,y in zip(actual,original)),(name,i,'Unlit cell brightened')
  dawn=(ctypes.c_uint16*16)(*colors);fn(1,src,dawn,ctypes.byref(day),ctypes.byref(night),128)
  for i in range(1,16):assert all(min(x,y)<=z<=max(x,y) for x,y,z in zip(channels(colors[i]),channels(dst[i]),channels(dawn[i])))
for family in ('general','general_frlg'):
 text='\n'.join((R/f).read_text() for f in ('src/graphics.c','src/data/tilesets/graphics.h','src/data/tilesets/legends_kanto.h'))
 assert 'data/tilesets/legends_lights/'+family+'_tiles.png' in text,('Unwired runtime art',family)
assert 'data/tilesets/legends_lights/*.pla' in (R/'Makefile').read_text()
print('29 window/sign cells: native daytime RGB, isolated night emission, free tile/palette slots, dawn blending and reproducible assets passed')
