"""Fit native bedroom floor beneath the existing Nightmare furniture, privately."""
from pathlib import Path
import argparse,hashlib,json,struct
from PIL import Image
R=Path(__file__).resolve().parents[2]
P=R/'data/tilesets/legends_nightmare/room'
PINS={
'data/tilesets/secondary/generic_building/tiles.png':'7783d199aaaaa51db286c745ddc6907a576f2930767a2f52862128c39cf15be8',
'data/tilesets/secondary/generic_building/metatiles.bin':'c3401446239749a25f6abc1daab0c19cd43eb6333a7ec5335bb7e1580d002b1d',
'data/tilesets/secondary/generic_building/metatile_attributes.bin':'eb3e942c013770224ffc7d99c469cdaf9cd31243f71ce3fb05a70b278dc5a509',
'data/tilesets/secondary/generic_building/palettes/06.pal':'baa86b1e51a10ae1d9dd06d23d3bb2ce9e9d433cdf2db2725ad7f8eaf5ec436b',
'data/tilesets/secondary/brendans_mays_house/tiles.png':'6e1cd90a6a16c2d280798000a2c91dbf72f18330517afa105b756d438ca3f7ac',
'data/tilesets/secondary/brendans_mays_house/metatiles.bin':'8f3a35edbbe4147ff7eb6869d1c50073ec71397bbe325f976bc04726c8628aff',
'data/tilesets/secondary/brendans_mays_house/palettes/06.pal':'77742cc1b2fcf7491dc6371155303454437c2d8416ea592b04c05658d1e74630',
}
def write(p,b):
 p.parent.mkdir(parents=True,exist_ok=True)
 if not p.exists() or p.read_bytes()!=b:p.write_bytes(b)
def colors(path):return [tuple(map(int,x.split())) for x in path.read_text().splitlines()[3:19]]
def pal(cs):return ('JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in cs)+'\n').encode()
def apply():
 for f,h in PINS.items():assert hashlib.sha256((R/f).read_bytes()).hexdigest()==h,'Changed native source: '+f
 native=R/'data/tilesets/secondary/generic_building';bedroom=R/'data/tilesets/secondary/brendans_mays_house'
 image=Image.open(native/'tiles.png');original=image.copy();wood=Image.open(bedroom/'tiles.png')
 metas=bytearray((native/'metatiles.bin').read_bytes());used=set()
 for room in ['Home','Bedroom']:
  p=R/f'data/layouts/LegendsNightmare_{room}/map.bin';cells=list(struct.unpack('<120H',p.read_bytes()))
  # Restore the continuous north-wall contact shadow, not a floating wall strip.
  for x in range(7,10):cells[2*12+x]=0x3224
  write(p,struct.pack('<120H',*cells));used.update(x&1023 for x in cells)
  border=(p.parent/'border.bin').read_bytes();used.update(x&1023 for x in struct.unpack('<%dH'%(len(border)//2),border))
 words=[w for m in used if m>=512 for w in struct.unpack_from('<8H',metas,(m-512)*16)]
 occupied={w&1023 for w in words};free=iter(t for t in range(512,1024) if t not in occupied)
 floorwords=struct.unpack_from('<8H',(bedroom/'metatiles.bin').read_bytes(),16)[:4]
 newtiles={};changed=[]
 for m in sorted(used):
  if m<512:continue
  for k in range(4):
   offset=(m-512)*16+k*2;w=struct.unpack_from('<H',metas,offset)[0];t=w&1023
   # Only native floor/background tiles, including floor baked into bed sides.
   # All other furniture, its upper layer, bed frame and sprite stay exact.
   if w>>12!=6 or t not in [0x230,0x231,0x240,0x241,0x3c2,0x3c5,0x3f5]:continue
   pixels=[];fw=floorwords[k];ft=(fw&1023)-512
   for y in range(8):
    for x in range(8):
     n=t-512;v=original.getpixel((n%16*8+(7-x if w&1024 else x),n//16*8+(7-y if w&2048 else y)))%16
     ox=7-x if w&1024 else x;oy=7-y if w&2048 else y
     background=t in [0x230,0x231,0x240,0x241] or t==0x3c2 and ox<5 or t==0x3c5 and ox>=3 or t==0x3f5 and (oy>=5 or ox>=(4 if oy<2 else 3 if oy<4 else 2))
     if background:
      v=wood.getpixel((ft%16*8+x,ft//16*8+y))%16
      assert v in [1,5,6,7,8]
      if m==0x224 and v!=1:v=7 if v in [5,7] else 8
      if v==1:v=13 # Native wood join color; retain bed-frame colors1..4 exactly.
     pixels.append(v)
   key=bytes(pixels)
   if key not in newtiles:
    dest=next(free);newtiles[key]=dest;n=dest-512
    for j,v in enumerate(pixels):image.putpixel((n%16*8+j%8,n//16*8+j//8),v)
   struct.pack_into('<H',metas,offset,0xc000|newtiles[key]);changed.append([m,k])
 P.mkdir(parents=True,exist_ok=True)
 from io import BytesIO
 encoded=BytesIO();image.save(encoded,format='PNG');write(P/'tiles.png',encoded.getvalue())
 write(P/'metatiles.bin',bytes(metas));write(P/'metatile_attributes.bin',(native/'metatile_attributes.bin').read_bytes())
 cs=colors(native/'palettes/06.pal');wc=colors(bedroom/'palettes/06.pal');cs[5:9]=wc[5:9];cs[13]=wc[1]
 write(P/'12.pal',pal(cs));cold=[(round(r*.43+b*.08),round(g*.46+b*.08),min(255,round(b*.63+r*.08))) for r,g,b in cs]
 write(R/'data/tilesets/legends_nightmare/interior/12.pal',pal(cold))
 header=['// Private room floor; native furniture and all shared tilesets retained.',
 'const u32 gNightmareRoomTiles[] = INCGFX_U32("data/tilesets/legends_nightmare/room/tiles.png", ".4bpp.fastSmol");',
 'const u16 gNightmareRoomMetatiles[] = INCBIN_U16("data/tilesets/legends_nightmare/room/metatiles.bin");',
 'const u16 gNightmareRoomAttributes[] = INCBIN_U16("data/tilesets/legends_nightmare/room/metatile_attributes.bin");',
 'const u16 gNightmareRoomPalettes[][16] = {']
 for i in range(16):
  path='data/tilesets/legends_nightmare/room/12.pal' if i==12 else f'data/tilesets/secondary/generic_building/palettes/{i:02d}.pal'
  header.append(f'    INCGFX_U16("{path}", ".gbapal"),')
 header+=['};','const struct Tileset gTileset_NightmareHomeInterior = {',
 '    .isCompressed = TRUE, .isSecondary = TRUE, .tiles = gNightmareRoomTiles, .palettes = gNightmareRoomPalettes,',
 '    .metatiles = gNightmareRoomMetatiles, .metatileAttributes = gNightmareRoomAttributes, .callback = NULL,','};']
 write(R/'src/data/tilesets/legends_nightmare_room.h',('\n'.join(header)+'\n').encode())
 h=R/'src/data/tilesets/legends_nightmare.h';s=h.read_text();start=s.index('const struct Tileset gTileset_NightmareInterior =');s=s[:start]+s[start:].replace('gTilesetTiles_GenericBuilding','gNightmareRoomTiles').replace('gMetatiles_GenericBuilding','gNightmareRoomMetatiles').replace('gMetatileAttributes_GenericBuilding','gNightmareRoomAttributes');write(h,s.encode())
 h=R/'src/tilesets.c';s=h.read_text();include='#include "data/tilesets/legends_nightmare_room.h"\n'
 if include not in s:s=s.replace('#include "data/tilesets/legends_nightmare.h"',include+'#include "data/tilesets/legends_nightmare.h"')
 write(h,s.encode())
 h=R/'data/layouts/layouts.json';v=json.loads(h.read_text())
 for l in v['layouts']:
  if l['id']=='LAYOUT_LEGENDS_NIGHTMARE_HOME':l['secondary_tileset']='gTileset_NightmareHomeInterior'
 write(h,(json.dumps(v,indent=2)+'\n').encode())
 write(P/'source.json',(json.dumps(dict(nativeInputs=PINS,wood='Native BrendansMaysHouse floor0x201 pixels and palette6 colors5..8',changedMetatileQuadrants=changed,allocatedTiles=sorted(newtiles.values()),scope='Private Home/dream only. Floor backgrounds replaced; all bed/furniture non-floor pixels, upper layers, attributes, scripts, sprites and walkability retained.'),indent=2)+'\n').encode())
 print('Fitted native room floor beneath unchanged furniture:',len(newtiles),'private tiles')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');a=p.parse_args()
 if not a.apply:raise SystemExit('Explicit authoring only: --apply required')
 apply()
