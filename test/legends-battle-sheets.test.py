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

manifest=json.loads((root/'tools/legends/battle_sheets.json').read_text())
names=['pixie','side_part','soft_layers','side_sweep','wavy_bob','short_bob','long_bob','curls','ponytail','twin_braids']
assert [(r['hair_id'],r['name']) for r in manifest]==list(enumerate(names,1))
choices=(root/'src/legends_appearance.c').read_text()
assert all('COMPOUND_STRING("'+n.replace('_',' ').upper()+'")' in choices for n in names)
header=before[1].decode().replace('INCBIN_U8("graphics/legends/battle_may/frames.bin")','{'+','.join(map(str,raw))+'}')
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
  for(int s=0;s<5;s++){
   tone=s;const u16 *pal=LegendsBattleBackPalette(205);
   assert(!memcmp(pal+1,sSkinPalettes[s],6));
   for(int i=0;i<16;i++)if(i<1||i>3)assert(pal[i]==base[i]);
   assert(LegendsBattleBackImage(205)==im);
  }
  // Every outfit/accessory/costume trainer ID uses the same current cut.
  for(int pic=200;pic<244;pic++){
   int g=pic<210?(pic-200)/5:pic<240?((pic-210)/5)%2:(pic-240)%2;
   assert(LegendsBattleBackImage(pic)->data==(g?sMayBattleBits+(h-1)*8192:gTrainerBackPic_Brendan));
  }
 }
 hair=6;color=1;tone=3;
 const u8 *old=LegendsBattleBackImage(205)->data;
 u16 oldPal[16];memcpy(oldPal,LegendsBattleBackPalette(205),32);
 hair=10;color=7;tone=1; // A wardrobe change must never keep a cached old cut/color.
 assert(old!=LegendsBattleBackImage(205)->data);
 const u16 *now=LegendsBattleBackPalette(205);
 assert(memcmp(oldPal+4,now+4,8)&&!memcmp(now+1,sSkinPalettes[1],6));
 for(int i=8;i<16;i++)assert(now[i]==oldPal[i]);
 hair=0;assert(LegendsBattleBackImage(205)->data==gTrainerBackPic_May);
 assert(!LegendsBattleBackImage(199)&&!LegendsBattleBackPalette(199));
 assert(!LegendsBattleBackImage(244)&&!LegendsBattleBackPalette(244));
 puts("10 matching cuts, 40 frames, eight hair colors, five isolated skin ramps, fixed uniforms and wardrobe refresh passed");
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
