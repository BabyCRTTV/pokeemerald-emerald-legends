"""Exercise the actual one-time gift module and its ROM asset contract."""
from pathlib import Path
import re, subprocess, tempfile, wave
from PIL import Image
root = Path(__file__).resolve().parents[1]
source = '\n'.join(l for l in (root/'src/legends_da_bug.c').read_text().splitlines() if not l.startswith('#include'))
stub = r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
typedef uint8_t u8; typedef uint32_t u32; typedef int bool32;
#define TOTAL_BOXES_COUNT 14
#define IN_BOX_COUNT 30
#define FLAG_LEGENDS_DA_BUG_RECEIVED 0
#define SPECIES_NONE 0
#define SPECIES_DA_BUG 1573
#define MON_DATA_SPECIES 0
#define MON_DATA_IS_SHINY 1
#define OTID_STRUCT_PLAYER_ID 0
#define RNG_NONE 0
#define MOVE_TACKLE 1
#define MOVE_LEER 2
#define MOVE_MEAN_LOOK 3
#define MOVE_ABSORB 4
#define NATIONAL_DEX_DA_BUG 1026
#define FLAG_SET_SEEN 1
#define FLAG_SET_CAUGHT 2
struct BoxPokemon {int species,level,shiny,moves[4],pp[4];};
struct Pokemon {struct BoxPokemon box;};
static struct BoxPokemon boxes[14][30];
static int received,created,stored,seen,caught,draws,roll,ordinaryShiny;
int FlagGet(int f) {return received;}
void FlagSet(int f) {received=1;}
int GetBoxMonDataAt(u8 b,u8 s,int field) {return boxes[b][s].species;}
u32 Random32(void) {draws++;return 0x12345678;}
u32 RandomUniform(int tag,u32 lo,u32 hi) {assert(lo==0 && hi==9);draws++;return roll;}
void CreateMon(struct Pokemon *m,int species,int level,u32 p,int ot) {
 memset(m,0,sizeof(*m));m->box.species=species;m->box.level=level;
 m->box.shiny=ordinaryShiny;created++;
}
void SetMonData(struct Pokemon *m,int field,const void *v) {assert(field==MON_DATA_IS_SHINY);m->box.shiny=*(const bool32*)v;}
void SetMonMoveSlot(struct Pokemon *m,int move,u8 slot) {m->box.moves[slot]=move;m->box.pp[slot]=10;}
void SetBoxMonAt(u8 b,u8 s,struct BoxPokemon *m) {boxes[b][s]=*m;stored++;}
void GetSetPokedexFlag(int dex,int kind) {assert(dex==1026);if(kind==1)seen++;else caught++;}
'''
tests = r'''
static void reset(void) {memset(boxes,0,sizeof(boxes));received=created=stored=seen=caught=draws=0;}
int main(void) {
 int shinies=0;
 // Both directions override ordinary odds, including boosted Options results.
 for(int prior=0;prior<2;prior++) for(int r=0;r<10;r++) {
  reset();roll=r;ordinaryShiny=prior;LegendsEnsureDaBugGift();
  assert(received && stored==1 && created==1 && draws==2 && seen==1 && caught==1);
  struct BoxPokemon *m=&boxes[0][0];assert(m->species==1573 && m->level==5);
  assert(m->shiny==(r==0));shinies+=m->shiny;
  for(int i=0;i<4;i++) assert(m->moves[i]==i+1 && m->pp[i]>0);
  // Withdrawal/release must not produce another gift or another shiny roll.
  memset(m,0,sizeof(*m));LegendsEnsureDaBugGift();
  assert(stored==1 && draws==2 && m->species==0);
 }
 assert(shinies==2);
 reset();for(int b=0;b<14;b++)for(int s=0;s<30;s++)boxes[b][s].species=25;
 LegendsEnsureDaBugGift();assert(!received && !created && !draws);
 // Full-box migration retries and never overwrites an existing Pokémon.
 boxes[8][17].species=0;roll=5;LegendsEnsureDaBugGift();
 assert(received && boxes[8][17].species==1573 && boxes[0][0].species==25);
 assert(created==1 && stored==1);
 puts("Da Bug gift: level/moves, exactly 1/10 shiny, duplicate guard, full-box retry passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'gift.c').write_text(stub+source+tests)
 subprocess.run(['cc','-std=c99','-Wall','-Werror',str(p/'gift.c'),'-o',str(p/'gift')],check=True)
 subprocess.run([str(p/'gift')],check=True)
assets=root/'graphics/pokemon/da_bug'
for file,size in [('anim_front.png',(64,128)),('back.png',(64,64)),('overworld.png',(192,32)),('icon.png',(32,64)),('footprint.png',(16,16))]:
 im=Image.open(assets/file);assert im.mode=='P' and im.size==size
 assert max(im.getdata())<(2 if file=='footprint.png' else 16)
front=Image.open(assets/'anim_front.png');changed=[]
for y in range(64):
 for x in range(64):
  a,b=front.getpixel((x,y)),front.getpixel((x,y+64))
  if a!=b:changed.append((a,b));assert a in (12,13) and b in (14,15)
assert changed and all(a!=0 and b!=0 for a,b in changed)
normal=(assets/'normal.pal').read_text().splitlines();shiny=(assets/'shiny.pal').read_text().splitlines()
assert len(normal)==len(shiny)==19 and normal[18]==shiny[18] # glimmer remains red
with wave.open(str(root/'sound/direct_sound_samples/cries/da_bug.wav')) as w:
 assert w.getnchannels()==1 and w.getsampwidth()==1 and w.getframerate()==13379
 assert .3<w.getnframes()/w.getframerate()<.4
 data=w.readframes(w.getnframes());assert min(data)>0 and max(data)<255
# The 1026th dex entry still fits the existing 129-byte save bitfields.
assert (1025+1+7)//8 == (1026+1+7)//8 ==129
orders=(root/'src/data/pokemon/pokedex_orders.h').read_text();assert orders.count('NATIONAL_DEX_DA_BUG,')==3
meta=(root/'src/data/pokemon/species_info/legends_families.h').read_text()
assert '.evolutions' not in meta and 'TYPE_BUG, TYPE_GRASS' in meta
entry=''.join(re.findall(r'"([^"\n]*)"',meta.split('.description = COMPOUND_STRING(')[1].split('),')[0])).replace('\\n',' ')
assert entry=='It sways in the breeze to mimic a fallen leaf. If its disguise fails, it flashes its red eyes and springs away.'
learn=(root/'src/data/pokemon/legends_learnsets.h').read_text()
assert re.findall(r'LEVEL_UP_MOVE\(\s*1, (MOVE_\w+)\)',learn)==['MOVE_TACKLE','MOVE_LEER','MOVE_MEAN_LOOK','MOVE_ABSORB']
for p in (root/'data').rglob('*'):
 if p.is_file() and ('wild' in p.name or p.suffix=='.inc'):assert 'SPECIES_DA_BUG' not in p.read_text(errors='ignore')
print('Da Bug assets, localized red glimmer, cry, exact dex text, no evolution/wild placement passed')
# Exercise actual player-side animation callback: bounded sway, eye-only blend,
# palette restoration and native task handoff, across all object palette slots.
anim=(root/'src/pokemon_animation.c').read_text().split('// Da Bug\'s player-side send-out:')[1]
anim=anim[anim.index('static void Anim_LegendsDaBugSway'):]
anim_stub=r'''
#include <assert.h>
#include <stdint.h>
typedef uint16_t u16;typedef int16_t s16;
struct Sprite {s16 data[8],x2;struct {int paletteNum;} oam;void (*callback)(struct Sprite*);};
#define OBJ_PLTT_ID(n) (256+(n)*16)
#define RGB_RED 31
static int expectedPalette,lastCoeff,calls;
static void WaitAnimEnd(struct Sprite *s) {(void)s;}
static int Sin(int phase,int amplitude) {assert(phase>=0 && phase<=256);return phase==0 ? 0 : amplitude;}
static void BlendPalette(int start,int count,int coeff,int color) {
 assert(start==expectedPalette && count==2 && coeff>=0 && coeff<=16 && color==RGB_RED);
 calls++;lastCoeff=coeff;
}
'''
anim_test=r'''
int main(void) {
 for(int p=0;p<16;p++) {
  struct Sprite s={0};s.oam.paletteNum=p;expectedPalette=256+p*16+12;calls=0;
  for(int n=0;n<49;n++){Anim_LegendsDaBugSway(&s);assert(s.x2>=-3 && s.x2<=3);}
  assert(calls==49 && lastCoeff==0 && s.x2==0 && s.callback==WaitAnimEnd);
 }
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'anim.c').write_text(anim_stub+anim+anim_test)
 subprocess.run(['cc','-std=c99','-Wall','-Werror',str(p/'anim.c'),'-o',str(p/'anim')],check=True)
 subprocess.run([str(p/'anim')],check=True)
print('Da Bug player send-out sway: eye-only blend, palette restoration and completion passed')

new_game=(root/"src/new_game.c").read_text().split("void NewGameInitData(void)")[1]
assert new_game.index("ResetPokemonStorageSystem();") < new_game.index("WarpToTruck();") < new_game.index("LegendsEnsureDaBugGift();")
