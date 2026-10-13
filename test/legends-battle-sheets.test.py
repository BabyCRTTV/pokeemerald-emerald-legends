"""Exercise the real fixed-uniform battle selector and independent palettes."""
from pathlib import Path
import json, re, subprocess, tempfile, sys

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools/legends'))
import import_battle_sheets as importer
paths=[root/'graphics/legends/battle_may/frames.bin',root/'src/data/legends/battle_sheets.h']
before=[p.read_bytes() for p in paths]
importer.build()
assert before==[p.read_bytes() for p in paths], 'checked-in art must reproduce exactly'
raw=before[0]
assert len(raw)==10*4*2048
assert len({raw[n*8192:(n+1)*8192] for n in range(10)})==10
for i in range(40):
 pixels=[v for b in raw[i*2048:(i+1)*2048] for v in (b&15,b>>4)]
 assert all(any(v==skin for v in pixels) for skin in (1,2,3)),('skin ramp',i)
 assert any(v==9 for v in pixels) or i%4==3,('glove highlights',i)

# Protect the native proportions against the rejected whole-image scaling.
# Every face/eye/hand cell and the lower torso remain on May's original grid.
native=importer.frames(importer.NATIVE_PATH,64,64)
for n in range(10):
 for pose,p in enumerate(native):
  frame=raw[(n*4+pose)*2048:(n*4+pose+1)*2048]
  def cell(x,y):
   offset=((y//8)*8+x//8)*32+(y%8)*4+(x%8)//2
   return frame[offset]>>(x%2*4)&15
  base,protected,_,face=importer.native_base(p,pose)
  for x,y in protected:
   assert cell(x,y)==base[y][x],('native face/hand geometry',n,pose,x,y)
  for y in range(60,64):
   for x in range(64):
    assert cell(x,y)==base[y][x],('native lower-body geometry',n,pose,x,y)
  # This uses only the shipped bitmap, not the importer's protection mask:
  # fingers, cuffs, neck and hair must belong to the same solid silhouette.
  occupied={(x,y) for y in range(64) for x in range(64) if cell(x,y)}
  reached={next(iter(occupied))};queue=list(reached)
  for x,y in queue:
   for dx,dy in ((-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)):
    q=(x+dx,y+dy)
    if q in occupied and q not in reached:reached.add(q);queue.append(q)
  assert reached==occupied,('detached glove/hair/neck pixels',n,pose,occupied-reached)
  if pose==1:
   # The original bug erased this native green cuff beneath the raised hand.
   for x,y in ((12,37),(13,37),(14,37),(15,37),(12,38),(13,38),(11,39)):
    assert cell(x,y)==10,('raised glove cuff',n,x,y)
  for x,y in importer.head(p,1,'back',pose)[0]:
   assert cell(x,y)==p[y][x],('native face skin',n,pose,x,y)

# Exercise male anatomy and static art without changing the approved May bank.
import import_brendan_battle_sheets as male
male_paths=[root/'graphics/legends/battle_brendan/frames.bin',root/'src/data/legends/battle_brendan_sheets.h']
male_before=[p.read_bytes() for p in male_paths]
male.build()
assert male_before==[p.read_bytes() for p in male_paths], 'male art must reproduce exactly'
male_raw=male_before[0]
assert len(male_raw)==81920 and len({male_raw[i*8192:(i+1)*8192] for i in range(10)})==10
for n in range(10):
 for pose,p in enumerate(male.frames(male.NATIVE_PATH,64,64)):
  bitmap=male.frames(root/('graphics/legends/battle_brendan/'+json.loads((root/'tools/legends/battle_brendan_sheets.json').read_text())[n]['name']+'.png'),64,64)[pose]
  base,protected,face=male.native_base(p,pose)
  for x,y in protected:assert bitmap[y][x]==base[y][x],('male native face/hand/collar',n,pose,x,y)
  for x,y in male.head(p,0,'back',pose)[0]:assert bitmap[y][x]==p[y][x],('male native skin',n,pose,x,y)
  for y in range(60,64):assert bitmap[y]==base[y],('male lower torso',n,pose,y)
  # Native red gloves, green cuffs and backpack must retain their materials.
  for y in range(64):
   for x in range(64):
    if base[y][x] in (10,11,12,13) and ((x,y) in protected or y>face[3]):
     assert bitmap[y][x]==base[y][x],('male native clothing/cuff',n,pose,x,y)
  occupied={(x,y) for y,row in enumerate(bitmap) for x,v in enumerate(row) if v}
  reached={min(occupied)};queue=list(reached)
  for x,y in queue:
   for q in male.neighbors({(x,y)})&occupied-reached:reached.add(q);queue.append(q)
  assert reached==occupied,('male detached anatomy',n,pose,occupied-reached)
  assert all(any(v==slot for row in bitmap for v in row) for slot in (1,2,3)),('male skin shades',n,pose)
  if pose==1:
   # Independently inspect the shipped bitmap. These seven cells were cap
   # edges joined to a raised finger, so silhouette connectivity missed them.
   for x,y in ((18,26),(17,27),(16,28),(15,29),(16,30),(17,30)):
    assert bitmap[y][x]==0,('raised-hand cap remnant',n,x,y)
   # Curls' genuine rear contour can reach the last former cap cell.
   assert bitmap[30][18] in (0,4,7,9,15),('raised-hand cap edge color',n)
   for x,y in ((13,27),(14,27),(12,28),(13,28),(14,28),(10,30),(11,30),(12,30),(15,36),(16,37)):
    value=p[y][x]
    assert bitmap[y][x]==(3 if value==4 else 8 if value==7 else 14 if value==9 else value),('preserved raised fingers/glove/cuff',n,x,y)
   if n==7:
    for x,y in ((48,22),(49,22),(49,23),(50,23)):
     assert bitmap[y][x]==0,('Curls reference brim',x,y)
    assert bitmap[28][34]==4, 'Curls inner strand must use hair shadow'
   if n==9:
    assert bitmap[30][32]==4, 'Undercut inner strand must use hair shadow'
male_names=['crew_cut','side_part','spiky','side_sweep','tousled','quiff','shag','curls','man_bun','undercut']
assert [(a['hair_id'],a['name']) for a in json.loads((root/'tools/legends/battle_brendan_sheets.json').read_text())]==list(enumerate(male_names,1))

manifest=json.loads((root/'tools/legends/battle_sheets.json').read_text())
names=['pixie','side_part','soft_layers','side_sweep','wavy_bob','short_bob','long_bob','curls','ponytail','twin_braids']
assert [(r['hair_id'],r['name']) for r in manifest]==list(enumerate(names,1))
choices=(root/'src/legends_appearance.c').read_text()
assert all('COMPOUND_STRING("'+n.replace('_',' ').upper()+'")' in choices for n in names)
header=before[1].decode().replace('INCBIN_U8("graphics/legends/battle_may/frames.bin")','{'+','.join(map(str,raw))+'}')
header+=male_before[1].decode().replace('INCBIN_U8("graphics/legends/battle_brendan/frames.bin")','{'+','.join(map(str,male_raw))+'}')
source='\n'.join(l for l in (root/'src/legends_battle_appearance.c').read_text().splitlines() if not l.startswith('#include'))
skin=re.search(r'static const u16 sSkinPalettes\[5\]\[3\] = \{.*?\n\};',(root/'src/data/legends/appearance_palettes.h').read_text(),re.S)[0]
pre=r'''
#include <stdint.h>
#include <stddef.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;
enum TrainerPicID {TRAINER_PIC_LEGENDS_BRENDAN_EMERALD=200,TRAINER_PIC_LEGENDS_ACCESSORY_0=210,TRAINER_PIC_LEGENDS_COSTUME_0=240};
#define LEGENDS_OUTFIT_COUNT 5
#define LEGENDS_HAIR_COUNT 11
#define FEMALE 1
#define TRUE 1
#define EWRAM_DATA
#define ALIGNED(n) __attribute__((aligned(n)))
struct SpriteFrameImage {const u8 *data;u16 size;u8 relativeFrames;};
u8 hair,color,tone;
u8 LegendsGetHair(void){return hair;}
u8 LegendsGetHairColor(void){return color;}
const u8 gTrainerBackPic_Brendan[8192]={1},gTrainerBackPic_May[8192]={2};
const u16 gTrainerPalette_Brendan[16]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
const u16 gTrainerPalette_May[16]={0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15};
'''
pre+=skin+'\nvoid LegendsCopySkinRamp(u16 *p){memcpy(p,sSkinPalettes[tone],6);}\n'
main=r'''
int main(void){
 for(int h=1;h<11;h++)for(int c=0;c<8;c++){
  hair=h;color=c;tone=0;
  const struct SpriteFrameImage *im=LegendsBattleBackImage(205);
  assert(im->data==sMayBattleBits+(h-1)*8192&&im->size==2048&&im->relativeFrames);
  u16 base[16];memcpy(base,LegendsBattleBackPalette(205),32);
  assert(base[4]==sBattleHairRamps[c][0]);
  assert(base[7]==sBattleHairRamps[c][1]);
  assert(base[11]==sBattleHairRamps[c][2]);
  for(int s=0;s<5;s++){
   tone=s;const u16 *pal=LegendsBattleBackPalette(205);
   assert(!memcmp(pal+1,sSkinPalettes[s],6));
   for(int i=0;i<16;i++)if(i<1||i>3)assert(pal[i]==base[i]);
   assert(LegendsBattleBackImage(205)==im);
  }
  // Every outfit/accessory/costume trainer ID uses the same current cut.
  for(int pic=200;pic<244;pic++){
   int g=pic<210?(pic-200)/5:pic<240?((pic-210)/5)%2:(pic-240)%2;
   assert(LegendsBattleBackImage(pic)->data==(g?sMayBattleBits+(h-1)*8192:sBrendanBattleBits+(h-1)*8192));
  }
 }
 for(int h=1;h<11;h++)for(int c=0;c<8;c++){
  hair=h;color=c;tone=0;
  const struct SpriteFrameImage *im=LegendsBattleBackImage(200);
  assert(im->data==sBrendanBattleBits+(h-1)*8192&&im->size==2048&&im->relativeFrames);
  u16 base[16];memcpy(base,LegendsBattleBackPalette(200),32);
  assert(base[4]==sBattleHairRamps[c][0]&&base[7]==sBattleHairRamps[c][1]&&base[9]==sBattleHairRamps[c][2]);
  for(int s=0;s<5;s++){
   tone=s;const u16 *pal=LegendsBattleBackPalette(200);assert(!memcmp(pal+1,sSkinPalettes[s],6));
   for(int i=0;i<16;i++)if(i<1||i>3)assert(pal[i]==base[i]);
   assert(LegendsBattleBackImage(200)==im);
  }
 }
 for(int g=0;g<2;g++){
  hair=1;color=1;tone=2;const u8 *old=LegendsBattleBackImage(200+g*5)->data;
  u16 oldPal[16];memcpy(oldPal,LegendsBattleBackPalette(200+g*5),32);
  hair=9;color=6;tone=4;assert(LegendsBattleBackImage(200+g*5)->data!=old);
  const u16 *now=LegendsBattleBackPalette(200+g*5);assert(!memcmp(now+1,sSkinPalettes[4],6));
  for(int i=0;i<16;i++)if(i>3&&i!=4&&i!=7&&i!=(g?11:9))assert(now[i]==oldPal[i]);
  hair=0;assert(LegendsBattleBackImage(200+g*5)->data==(g?gTrainerBackPic_May:gTrainerBackPic_Brendan));
 }
 hair=6;color=1;tone=3;
 const u8 *old=LegendsBattleBackImage(205)->data;
 u16 oldPal[16];memcpy(oldPal,LegendsBattleBackPalette(205),32);
 hair=10;color=7;tone=1; // A wardrobe change must never keep a cached old cut/color.
 assert(old!=LegendsBattleBackImage(205)->data);
 const u16 *now=LegendsBattleBackPalette(205);
 assert(memcmp(oldPal+4,now+4,8)&&!memcmp(now+1,sSkinPalettes[1],6));
 for(int i=4;i<16;i++)if(i!=4&&i!=7&&i!=11)assert(now[i]==oldPal[i]);
 hair=0;assert(LegendsBattleBackImage(205)->data==gTrainerBackPic_May);
 assert(!LegendsBattleBackImage(199)&&!LegendsBattleBackPalette(199));
 assert(!LegendsBattleBackImage(244)&&!LegendsBattleBackPalette(244));
 puts("20 matching cuts, 80 frames, eight hair colors, five isolated skin ramps, fixed uniforms and wardrobe refresh passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'check.c').write_text(pre+header+source+main)
 subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror',str(p/'check.c'),'-o',str(p/'check')],check=True)
 subprocess.run([str(p/'check')],check=True)
data=(root/'include/data.h').read_text()
assert 'LegendsBattleBackImage(trainerPic)' in data and 'LegendsBattleBackPalette(trainerPic)' in data
assert 'LegendsFootwearBackImages(trainerPicId,' not in (root/'src/pokemon.c').read_text()
assert 'LegendsFootwearBackPic(trainerPicId, dest, size);' not in (root/'src/trainer_pokemon_sprites.c').read_text()
