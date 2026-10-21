"""Execute the production grotto state machine with deterministic engine boundaries."""
import json,re,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'src/legends_grottos.c').read_text()
source=re.sub(r'^#include .*$', '', source, flags=re.M)
# Keep the actual generated encounter table, with fake engine species constants.
table=(R/'src/data/legends/grotto_encounters.h').read_text()
species=sorted(set(re.findall(r'SPECIES_\w+',table)))
defines='\n'.join(f'#define {s} {i+1}' for i,s in enumerate(species))
prefix=r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
typedef uint8_t u8; typedef int8_t s8; typedef uint16_t u16; typedef int16_t s16;
typedef uint32_t u32; typedef int32_t s32; typedef int bool32;
#define TRUE 1
#define FALSE 0
#define EWRAM_DATA
#define STATIC_ASSERT(c,n) _Static_assert(c,#n)
#define SPECIES_NONE 0
#define NUM_SPECIES 2000
#define MAP_LEGENDS_GROTTO_LEAFSHADE 1
#define MAP_LEGENDS_GROTTO_STILLWATER 2
#define MAP_LEGENDS_GROTTO_RAINROOT 3
#define MAP_GROUP(x) 76
#define MAP_NUM(x) (x)
#define B_TRAINER_OPPONENT_A 1
#define OBJ_EVENT_MON 1000
#define ITEM_NONE 0
#define FLAG_TEMP_5 5
#define VAR_OBJ_GFX_ID_F 15
#define B_OUTCOME_WON 1
#define B_OUTCOME_CAUGHT 7
#include "legends_grottos.h"
struct BoxPokemon { u8 bytes[80]; };
struct Pokemon { struct BoxPokemon box; };
struct { struct { u8 mapGroup,mapNum; } location; } sb1, *gSaveBlock1Ptr=&sb1;
struct { u8 legacy[716]; struct LegendsGrottoSave grottos; } sb3, *gSaveBlock3Ptr=&sb3;
struct Pokemon gParties[2][6];
struct { u16 graphicsId; } gObjectEvents[16];
u16 gSpecialVar_Result,gSpecialVar_0x8004,gfx;
u8 gStringVar1[32];
static int season,roll,randomCalls,generated,hidden,exists,spawned;
static s16 playerX=16,playerY=16;
static u16 Random(void) { return randomCalls++%2 ? 0 : roll; }
static int LegendsGetActiveSeason(void) { return season; }
static void SetWildShinyGenerationContext(int active) { (void)active; }
static void CreateScriptedWildMon(u16 species,u8 level,u16 item) {
 generated++; for(int i=0;i<80;i++)gParties[1][0].box.bytes[i]=(species+i+generated*7+level)%256;
}
static void FlagSet(int f) { assert(f==5);hidden=1; }
static void FlagClear(int f) { assert(f==5);hidden=0; }
static void VarSet(int v,int value) { assert(v==15);gfx=value; }
static const u8 *GetSpeciesName(u16 s) { return (const u8 *)"Visitor"; }
static void StringCopy(u8 *a,const u8 *b) { strcpy((char *)a,(const char *)b); }
static void ZeroEnemyPartyMons(void) { memset(gParties[1],0,sizeof(gParties[1])); }
static void BoxMonToMon(const struct BoxPokemon *a,struct Pokemon *b) { memcpy(&b->box,a,80); }
static int TryGetObjectEventIdByLocalIdAndMap(int local,int num,int group,u8 *id) { assert(local==1);*id=1;return !exists; }
static void PlayerGetDestCoords(s16 *x,s16 *y) { *x=playerX;*y=playerY; }
static void TrySpawnObjectEvent(int local,int num,int group) { assert(local==1);spawned++;exists=1; }
'''
test=r'''
static void enter(int room,int selectedSeason,int selectedRoll) {
 sb1.location.mapGroup=76;sb1.location.mapNum=room+1;season=selectedSeason;roll=selectedRoll;
 randomCalls=0;exists=1;LegendsGrottoPrepareVisitor();assert(gSpecialVar_Result && !hidden);assert(gObjectEvents[1].graphicsId==gfx);
}
int main(void) {
 memset(&sb3,0xA5,sizeof(sb3));LegendsGrottoInit(FALSE);assert(Valid());
 for(int i=0;i<716;i++)assert(sb3.legacy[i]==0xA5);
 assert(sizeof(sb3.grottos)==276);
 for(int room=0;room<3;room++)for(int s=0;s<4;s++) {
  int counts[5]={0};
  for(int value=0;value<100;value++) {
   LegendsGrottoInit(TRUE);enter(room,s,value);
   struct LegendsGrottoRoomSave *r=&DATA->rooms[room];
   int slot=-1;for(int i=0;i<5;i++)if(r->species==sGrottoEncounters[room][s][i].species)slot=i;
   assert(slot>=0);counts[slot]++;assert(r->level>=sGrottoLevels[room][0]&&r->level<=sGrottoLevels[room][1]);
   assert(gfx==r->species+OBJ_EVENT_MON);
  }
  for(int i=0;i<5;i++)assert(counts[i]==sGrottoEncounters[room][s][i].weight);
 }
 for(int room=0;room<3;room++) {
  LegendsGrottoInit(TRUE);enter(room,0,45);struct LegendsGrottoSave original=*DATA;
  int before=generated;for(int i=0;i<5001;i++)LegendsGrottoStep();
  season=3;LegendsGrottoPrepareVisitor();assert(!memcmp(DATA,&original,sizeof(original))&&before==generated);
  sb1.location.mapGroup=0;LegendsGrottoPrepareVisitor();assert(!gSpecialVar_Result);
  LegendsGrottoInit(FALSE);enter(room,2,99);assert(!memcmp(DATA,&original,sizeof(original))&&before==generated);
  // Every outcome is exercised against the production consumer; only KO/catch count.
  for(int outcome=0;outcome<256;outcome++) {
   *DATA=original;LegendsGrottoInit(FALSE);LegendsGrottoFinishBattle(outcome);
   assert(!memcmp(DATA,&original,sizeof(original))); // unrelated battle
   assert(LegendsGrottoStartBattle());assert(!memcmp(&gParties[1][0].box,DATA->rooms[room].mon,80));
   LegendsGrottoFinishBattle(outcome);
   if(outcome==1||outcome==7)assert(DATA->rooms[room].state==2&&LegendsGrottoRemainingSteps(room)==4500);
   else assert(!memcmp(DATA,&original,sizeof(original)));
  }
  *DATA=original;LegendsGrottoInit(FALSE);assert(LegendsGrottoStartBattle());LegendsGrottoFinishBattle(7);
  // Independent room cooldowns and mid-countdown reload preserve their exact offsets.
  sb1.location.mapGroup=0;for(int i=0;i<500;i++)LegendsGrottoStep();
  enter((room+1)%3,1,20);assert(LegendsGrottoStartBattle());LegendsGrottoFinishBattle(1);
  sb1.location.mapGroup=0;struct LegendsGrottoSave saved=*DATA;memset(DATA,0,sizeof(*DATA));*DATA=saved;LegendsGrottoInit(FALSE);
  assert(LegendsGrottoRemainingSteps(room)==4000&&LegendsGrottoRemainingSteps((room+1)%3)==4500);
  for(int i=0;i<3999;i++)LegendsGrottoStep();assert(LegendsGrottoRemainingSteps(room)==1);
  assert(DATA->rooms[room].state==2);LegendsGrottoStep();assert(DATA->rooms[room].state==0);
  assert(LegendsGrottoRemainingSteps((room+1)%3)==500);
  sb1.location.mapGroup=76;sb1.location.mapNum=room+1;exists=0;spawned=0;playerX=16;playerY=13;
  LegendsGrottoStep();assert(!spawned&&DATA->rooms[room].state==0); // occupied spawn
  playerY=14;LegendsGrottoStep();assert(spawned==1&&DATA->rooms[room].state==1&&before<generated);
  for(int i=0;i<716;i++)assert(sb3.legacy[i]==0xA5);
 }
 LegendsGrottoInit(TRUE);DATA->magic^=1;LegendsGrottoInit(FALSE);assert(Valid());
 DATA->version++;Sign();LegendsGrottoInit(FALSE);assert(Valid()&&DATA->version==1);
 DATA->rooms[0].state=9;Sign();assert(!Valid());LegendsGrottoInit(FALSE);assert(Valid());
 DATA->checksum^=1;LegendsGrottoInit(FALSE);assert(Valid());
 puts("PASS: production state machine, all 12 weighted pools, 768 outcome cases, exact 4500 boundary, identity/save stability, independent cooldowns, legacy isolation, deferred spawn");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(prefix+defines+'\n'+source.replace('struct GrottoEncounter { u16 species; u8 weight; };', 'struct GrottoEncounter { u16 species; u8 weight; };\n'+table)+'\n'+test)
 subprocess.run(['cc','-std=c11','-O2','-iquote',str(R/'include'),str(p),'-o',str(Path(d)/'test')],check=True)
 subprocess.run([str(Path(d)/'test')],check=True)
# Canonical data is the single source for engine and reader odds.
manifest=json.loads((R/'src/data/legends/grotto_encounters.json').read_text())
wiki=json.loads((R/'docs/wiki/dex-data.json').read_text())
assert manifest['refreshSteps']==4500 and manifest['refreshAfter']==['caught','defeated']
for room in manifest['rooms']:
 m=next(m for m in wiki['maps'] if m['id']==room['map']);assert m['region']=='Grotto'
 for variant in m['methods'][0]['seasonalVariants']:
  assert [(e['id'],e['rate'],e['min'],e['max']) for e in variant['entries']]==[(e['species'],e['weight'],*room['levels']) for e in room['seasons'][variant['season']]]
print('PASS: canonical engine/LegendsDex roster, levels, seasons and odds agree')
