"""Build only Wyrmtide's contextual tile variants from existing native pixels.

Original shared art and layouts are never written. Explicit refresh is required
because the owner's later Porymap edits must survive routine builds.
"""
from pathlib import Path
import argparse,json,struct
from PIL import Image
R=Path(__file__).resolve().parents[2]
CAVE=R/'data/tilesets/secondary/cave';DEW=R/'data/tilesets/secondary/dewford';GENERAL=R/'data/tilesets/primary/general'
POOL_SOURCES=[0x289,0x291,0x281,0x28A,0x288,0x26C,0x26B,0x26A]
POOL_IDS={n:0x3A0+i for i,n in enumerate(POOL_SOURCES)}
TABLETS=[0x208,0x209,0x20A,0x218,0x235,0x21A]
def meta(folder,n):return list(struct.unpack_from('<8H',(folder/'metatiles.bin').read_bytes(),(n-(512 if folder!=GENERAL else 0))*16))
def tile_pixels(image,n):
 x=n%16*8;y=n//16*8
 return image.crop((x,y,x+8,y+8))
def layer_pixels(words,layer):
 out=Image.new('P',(16,16),0)
 for i,w in enumerate(words[layer*4:layer*4+4]):
  if not w:continue
  tid=w&1023;png=Image.open((GENERAL if tid<512 else CAVE)/'tiles.png');im=tile_pixels(png,tid%512)
  if w&1024:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if w&2048:im=im.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  assert w>>12==6
  out.paste(im,(i%2*8,i//2*8))
 return out
class Slots:
 def __init__(self,native):
  self.original=Image.open(native/'tiles.png');self.image=Image.new('P',(128,256),0);self.image.putpalette(self.original.getpalette());self.image.paste(self.original,(0,0));self.next=944
 def add(self,pixels):
  words=[]
  for i in range(4):
   assert self.next<1024,'Review free tile allocation before adding more art'
   target=self.next;self.next+=1
   self.image.paste(pixels.crop((i%2*8,i//2*8,i%2*8+8,i//2*8+8)),((target-512)%16*8,(target-512)//16*8))
   words.append(0x6000|target)
  return words
 def save(self,out):
  # Every native pixel, including the animation-reserved rows, stays exact.
  assert self.image.crop((0,0,*self.original.size)).tobytes()==self.original.tobytes() if self.original.height<256 else True
  self.image.save(out/'tiles.png')
def shore_tileset():
 out=R/'data/tilesets/legends_wyrmtide_shore';out.mkdir(parents=True,exist_ok=True)
 original=(DEW/'metatiles.bin').read_bytes();nativewords=struct.unpack('<%dH'%(len(original)//2),original)
 assert not {w&1023 for w in nativewords}&set(range(944,1024))
 assert 6 not in {w>>12 for w in nativewords}
 slots=Slots(DEW);sand=meta(GENERAL,0x124)[:4]
 # Trace the existing rock's own dark outline. Only the surrounding cave-floor
 # matte is removed; the inscription/stone pixels and small native shadow stay.
 monument=Image.new('P',(48,32),0)
 for i,n in enumerate(TABLETS):monument.paste(layer_pixels(meta(CAVE,n),0),(i%3*16,i//3*16))
 spans=[]
 for y in range(32):
  outline=[x for x in range(48) if monument.getpixel((x,y))%16==7]
  assert outline,'Native monument outline changed; review its cutout'
  left=max(0,min(outline)-1);right=min(47,max(outline)+1);spans.append([left,right])
  for x in range(48):
   if x<left or x>right:monument.putpixel((x,y),0)
 extra=[];ids={}
 for i,n in enumerate(TABLETS):
  fore=monument.crop((i%3*16,i//3*16,i%3*16+16,i//3*16+16))
  extra.append(struct.pack('<8H',*(sand+slots.add(fore))));ids[n]=512+len(original)//16+i
 for n in [0x2BC,0x2C4]:
  # Native columns already have transparent foregrounds: replace only their
  # buried cave-floor underlay with the shore's actual sand.
  extra.append(struct.pack('<8H',*(sand+meta(CAVE,n)[4:])));ids[n]=512+len(original)//16+len(extra)-1
 # Dewford's flag animation writes 682..687; authored cells start at 944.
 slots.image.save(out/'tiles.png')
 (out/'metatiles.bin').write_bytes(original+b''.join(extra));(out/'metatile_attributes.bin').write_bytes((DEW/'metatile_attributes.bin').read_bytes()+bytes(16))
 (out/'source.json').write_text(json.dumps({'native':'Dewford','metatiles':ids,'palette':6,'nativeUsedPixelsPreserved':True,'animationReserved':[682,687],'authoredTileRange':[944,slots.next-1],'sandUnderlay':'General 0x124','inscriptionSource':'Cave 0x208/209/20A/218/235/21A','nativeOutlineSpans':spans,'columns':'Native Cave foreground over General sand; no cave-floor matte'},indent=2)+'\n')
 return ids
def cave_tileset():
 out=R/'data/tilesets/legends_wyrmtide';out.mkdir(parents=True,exist_ok=True);slots=Slots(CAVE)
 native=(CAVE/'metatiles.bin').read_bytes();attrs=(CAVE/'metatile_attributes.bin').read_bytes();assert len(native)//16==414
 tread=struct.pack('<8H',*meta(CAVE,0x204));extra=[];attributes=[];ground=layer_pixels(meta(CAVE,0x201),0)
 # General's native enclosed-pond family is a complete, matching nine-slice.
 # Cave's concave sea-cliff caps cannot be substituted as convex pool corners.
 # Reuse that native outline with the real cave floor and existing Cave shades.
 lake_sources=[0x0C8,0x0C9,0x0CA,0x0D0,0x0D2,0x0D8,0x0D9,0x0DA]
 general_png=Image.open(GENERAL/'tiles.png')
 palette=[tuple(map(int,l.split())) for l in (GENERAL/'palettes/03.pal').read_text().splitlines()[3:19]]
 colors={(98,65,82):7,(131,90,90):6,(156,115,115):5}
 for source,lake in zip(POOL_SOURCES,lake_sources):
  fore=Image.new('P',(16,16),0)
  for i,w in enumerate(meta(GENERAL,lake)[4:]):
   if not w:continue
   assert w>>12==3 and (w&1023)<512
   tile=tile_pixels(general_png,w&1023)
   if w&1024:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if w&2048:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   for y in range(8):
    for x in range(8):
     v=tile.getpixel((x,y))%16
     if not v:continue
     xx=i%2*8+x;yy=i//2*8+y;rgb=palette[v]
     if rgb==(115,197,164):v=ground.getpixel((xx,yy))%16
     else:
      assert rgb in colors,('Review native pond rim colors',rgb)
      v=colors[rgb]
     fore.putpixel((xx,yy),v)
  extra.append(struct.pack('<8H',*(meta(CAVE,0x27B)[:4]+slots.add(fore))))
  attributes.append(struct.unpack_from('<H',attrs,(source-512)*2)[0])
 slots.save(out)
 (out/'metatiles.bin').write_bytes(native+tread+tread+b''.join(extra));(out/'metatile_attributes.bin').write_bytes(attrs+struct.pack('<10H',0x61,0,*attributes))
 (out/'source.json').write_text(json.dumps({'native':'Cave','nativePixelsPreserved':True,'animationReserved':[928,931],'authoredTileRange':[944,slots.next-1],'stairs':'Exact Cave 0x204 geometry and palette 6','poolMetatiles':POOL_IDS,'nativePondOutline':lake_sources,'ground':'Cave 0x201 replaces the native pond’s grass matte','rim':'Existing Cave palette 6 dark/medium/light stone shades','water':'Original animated General water indices'},indent=2)+'\n')
def main():
 p=argparse.ArgumentParser();p.add_argument('--refresh-review',action='store_true');a=p.parse_args()
 if not a.refresh_review:raise SystemExit('Owner tileset edits preserved. --refresh-review is an explicit authoring operation.')
 cave_tileset();shore_tileset();print('Authored contextual sand bases, cave-floor water banks and native brown stairs; shared art untouched.')
if __name__=='__main__':main()
