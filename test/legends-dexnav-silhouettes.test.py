"""Execute the real icon selector with mixed shared palettes and failure guards."""
from pathlib import Path
import subprocess,tempfile
R=Path(__file__).resolve().parents[1];s=(R/'src/dexnav.c').read_text();a=s.index('#define DEXNAV_SILHOUETTE_PAL_TAG');b=s.index('static void DrawSpeciesIcons(void)\n{',a);functions=s[a:b]
pre=r'''
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int16_t s16;
enum Species {SPECIES_NONE,KNOWN,UNSEEN,FORM,NUM_SPECIES};
#define RGB_BLACK 0
#define MAX_SPRITES 64
#define FLAG_GET_SEEN 0
struct SpritePalette {const u16 *data;u16 tag;};
struct Sprite {struct {u8 paletteNum;}oam;}gSprites[64];
static unsigned palette=6,allocated=3,seen,lastSpecies,noData,created,flags;
static void SpriteCB_MonIcon(struct Sprite *s){}
static u8 IndexOfSpritePaletteTag(unsigned tag){assert(tag==0x4011);return palette;}
static void CreateNoDataIcon(s16 x,s16 y){noData++;}
static unsigned SpeciesToNationalPokedexNum(enum Species species){return species;}
static unsigned GetSetPokedexFlag(unsigned dex,unsigned mode){assert(mode==FLAG_GET_SEEN);return seen;}
static u8 CreateMonIcon(enum Species species,void(*cb)(struct Sprite*),s16 x,s16 y,unsigned p,u32 personality){
 assert(cb==SpriteCB_MonIcon&&personality==0xffffffff);created++;lastSpecies=species;
 if(allocated!=MAX_SPRITES)gSprites[allocated].oam.paletteNum=1;return allocated;
}
'''
pre += r'''
static u8 CreateDexNavMonIcon(enum Species species,s16 x,s16 y){return CreateMonIcon(species,SpriteCB_MonIcon,x,y,0,0xffffffff);}
'''
main=r'''
int main(void){
 assert(sSilhouettePalette.tag==0x4011);for(unsigned i=0;i<16;i++)assert(!sSilhouettePalette.data[i]);
 seen=0;TryDrawIconInSlot(UNSEEN,0,0);assert(lastSpecies==UNSEEN&&gSprites[3].oam.paletteNum==6&&!noData);
 allocated=4;seen=1;TryDrawIconInSlot(KNOWN,0,0);assert(lastSpecies==KNOWN&&gSprites[4].oam.paletteNum==1&&gSprites[3].oam.paletteNum==6);
 allocated=5;seen=0;TryDrawIconInSlot(FORM,0,0);assert(lastSpecies==FORM&&gSprites[5].oam.paletteNum==6&&gSprites[4].oam.paletteNum==1);
 unsigned n=created;TryDrawIconInSlot(SPECIES_NONE,0,0);TryDrawIconInSlot(NUM_SPECIES,0,0);assert(noData==2&&created==n);
 palette=255;TryDrawIconInSlot(UNSEEN,0,0);assert(noData==3&&created==n);
 palette=6;allocated=MAX_SPRITES;TryDrawIconInSlot(UNSEEN,0,0);assert(created==n+1&&!flags);
 puts("PASS: native species/animation callback, isolated black palette, mixed known/unseen/forms, empty slots and allocation guards");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(pre+functions+main)
 subprocess.run(['cc','-std=gnu17','-Werror=implicit-function-declaration',str(p),'-o',d+'/test'],check=True);subprocess.run([d+'/test'],check=True)
draw=s[s.index('static void DrawSpeciesIcons(void)\n{'):s.index('static enum Species DexNavGetSpecies(void)')]
assert 'LoadSpritePalette(&sSilhouettePalette);' in draw and 'CreateMonIcon(SPECIES_NONE' not in draw
assert 'TintPalette' not in functions and 'LoadPalette' not in functions
get=s[s.index('static enum Species DexNavGetSpecies(void)'):s.index('static void SetSpriteInvisibility')]
assert 'FLAG_GET_SEEN' in get and '!FlagGet(DN_FLAG_DETECTOR_MODE)' in get
