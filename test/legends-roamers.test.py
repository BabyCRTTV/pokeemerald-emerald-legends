"""Exercise production dual-Eon state, legacy backfill and slot isolation."""
from pathlib import Path
import re,subprocess,tempfile
R=Path(__file__).resolve().parents[1]
s=(R/'src/roamer.c').read_text();s=re.sub(r'^#include .*$', '',s,flags=re.M).replace('enum Species','u16')
h=(R/'include/legends_roamers.h').read_text().replace('enum Species','u16')
maps=sorted(set(re.findall(r'MAP_(?:ROUTE\d+|UNDEFINED)',s)))
pre=r'''
#include <stdint.h>
#include <string.h>
#include <stddef.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef u8 bool8;typedef int bool32;
#define TRUE 1
#define FALSE 0
#define EWRAM_DATA
#define STATIC_ASSERT(c,n) _Static_assert(c,#n)
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define ROAMER_COUNT 2
#define MAP_NUM(x) (x)
#define SPECIES_LATIAS 380
#define SPECIES_LATIOS 381
#define FLAG_LATIOS_OR_LATIAS_ROAMING 1
#define FLAG_GET_SEEN 1
#define ROAMER_ORIGIN 0
#define RANDOM_UNOWN_LETTER 0
#define OTID_STRUCT_PLAYER_ID 0
#define USE_RANDOM_IVS 0
#define B_TRAINER_OPPONENT_A 1
enum {MON_DATA_IVS,MON_DATA_PERSONALITY,MON_DATA_MAX_HP,MON_DATA_COOL,MON_DATA_BEAUTY,MON_DATA_CUTE,MON_DATA_SMART,MON_DATA_TOUGH,MON_DATA_IS_SHINY,MON_DATA_HP,MON_DATA_STATUS};
struct Pokemon {u32 data[11];u16 species;};
struct Pokemon gParties[2][6];
static int roaming,seen,created;static u32 rng=7;u16 gSpecialVar_0x8004;
static u16 Random(void){rng=rng*1664525+1013904223;return rng>>16;}
static int FlagGet(int f){return roaming;}
static int GetSetPokedexFlag(int s,int f){return seen;}
static int SpeciesToNationalPokedexNum(int s){return s;}
static u32 GetMonPersonality(int s,int g,int n,int l){return Random();}
static int GetSynchronizedGender(int a,int b){return 0;}
static int GetSynchronizedNature(int a,int b){return 0;}
static void GiveMonInitialMoveset(struct Pokemon *p){}
static void CreateMonWithIVs(struct Pokemon *p,int s,int level,u32 personality,int ot,int ivs){memset(p,0,sizeof(*p));p->species=s;p->data[MON_DATA_IVS]=Random();p->data[MON_DATA_PERSONALITY]=personality;p->data[MON_DATA_MAX_HP]=123;created++;}
static void CreateMonWithIVsPersonality(struct Pokemon *p,int s,int l,u32 iv,u32 person){memset(p,0,sizeof(*p));p->species=s;p->data[MON_DATA_IVS]=iv;p->data[MON_DATA_PERSONALITY]=person;}
static u32 GetMonData(struct Pokemon *p,int n){return p->data[n];}
static void SetMonData(struct Pokemon *p,int n,const void *v){if(n==MON_DATA_HP)p->data[n]=*(const u16*)v;else if(n==MON_DATA_STATUS)p->data[n]=*(const u32*)v;else p->data[n]=*(const u8*)v;}
static void ZeroEnemyPartyMons(void){memset(gParties[1],0,sizeof(gParties[1]));}
void SetRoamerInactive(u32);void RoamerMoveToOtherLocationSet(u32);void RoamerMove(u32);
'''
pre+='\n'.join(f'#define {m} {i+1}' for i,m in enumerate(maps))+'\n'+h+r'''
struct {u8 prefix[992];struct LegendsEonSave eon;} sb3,*gSaveBlock3Ptr=&sb3;
struct {struct {u8 mapGroup,mapNum;}location;struct Roamer roamer[1];u8 suffix[512];}sb1,*gSaveBlock1Ptr=&sb1;
'''
test=r'''
static void begin(int choice){memset(&sb1,0,sizeof(sb1));memset(&sb3,0xA5,sizeof(sb3));roaming=seen=0;created=0;LegendsRoamerInit(TRUE);gSpecialVar_0x8004=choice;InitRoamer();assert(!created);roaming=1;InitRoamer();assert(created==1&&ROAMER(0)->active&&!ROAMER(1)->active&&!EON->unlocked);}
int main(void){
 assert(sizeof(struct Roamer)==28&&sizeof(struct LegendsEonSave)==40&&offsetof(typeof(sb3),eon)==992);
 for(int choice=0;choice<2;choice++)for(int resolved=0;resolved<2;resolved++){
  begin(choice);struct Roamer first=*ROAMER(0);struct Pokemon enemy=gParties[1][0];
  for(int i=0;i<992;i++)assert(sb3.prefix[i]==0xA5);
  InitRoamer();assert(created==1&&!memcmp(&first,ROAMER(0),28));
  // A generated/Repel-blocked roll is not an encounter completion.
  sb1.location.mapGroup=0;sb1.location.mapNum=sRoamerLocation[0][1];while(!TryStartRoamerEncounter()){}assert(!EON->unlocked);
  gParties[1][0].data[MON_DATA_HP]=42;gParties[1][0].data[MON_DATA_STATUS]=0x102;
  enemy=gParties[1][0];UpdateRoamerHPStatus(&gParties[1][0]);assert(!memcmp(&enemy,&gParties[1][0],sizeof(enemy)));
  assert(EON->unlocked&&ROAMER(1)->active&&ROAMER(1)->species!=(u16)first.species&&created==2);
  assert(ROAMER(0)->personality==first.personality&&ROAMER(0)->hp==42&&ROAMER(0)->statusA==2&&ROAMER(0)->statusB==1);
  struct Roamer second=*ROAMER(1);UpdateRoamerHPStatus(&gParties[1][0]);assert(created==2&&!memcmp(&second,ROAMER(1),28));
  if(resolved)SetRoamerInactive(0);
  assert(ROAMER(1)->active);
  // Reload valid state repeatedly; exact identities, HP/status and resolution retained.
  typeof(sb3) flash=sb3;LegendsRoamerInit(FALSE);assert(!memcmp(&flash,&sb3,sizeof(sb3)));
  memset(&sb3,0,sizeof(sb3));sb3=flash;LegendsRoamerInit(FALSE);assert(!memcmp(&flash,&sb3,sizeof(sb3)));
  gEncounteredRoamerIndex=1;CreateRoamerMonInstance(1);gParties[1][0].data[MON_DATA_HP]=13;gParties[1][0].data[MON_DATA_STATUS]=4;UpdateRoamerHPStatus(&gParties[1][0]);assert(ROAMER(1)->hp==13&&ROAMER(1)->statusA==4);
  struct Roamer retained=*ROAMER(0);SetRoamerInactive(1);assert(!memcmp(&retained,ROAMER(0),28));flash=sb3;
  for(int i=0;i<8;i++){LegendsRoamerInit(FALSE);InitRoamer();assert(!ROAMER(1)->active&&created==2&&!memcmp(&flash,&sb3,sizeof(sb3)));}
 }
 for(int choice=0;choice<2;choice++)for(int active=0;active<2;active++)for(int wasSeen=0;wasSeen<2;wasSeen++){
  begin(choice);ROAMER(0)->active=active;seen=wasSeen;struct Roamer original=*ROAMER(0);memset(EON,0xA5,sizeof(*EON));
  LegendsRoamerInit(FALSE);assert(!memcmp(&original,ROAMER(0),28));assert(!!EON->unlocked==(!active||wasSeen));
  typeof(sb3) valid=sb3;LegendsRoamerInit(FALSE);assert(!memcmp(&valid,&sb3,sizeof(sb3)));
 }
 puts("PASS production dual Eon: both choices, real-return unlock, Repel isolation, independent HP/status/identity/removal, legacy states, repeated reload and no revival");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'t.c').write_text(pre+s+test);subprocess.run(['cc','-std=gnu11','-Wall','-Wno-unused-parameter',str(p/'t.c'),'-o',str(p/'t')],check=True);subprocess.run([str(p/'t')],check=True)
# No native save-offset growth or direct indexing past its single legacy slot.
assert 'struct Roamer roamer[1];' in (R/'include/global.h').read_text()
for f in ['src/wild_encounter.c','src/pokedex_area_screen.c']:assert 'gSaveBlock1Ptr->roamer[' not in (R/f).read_text()
assert 'special InitRoamer' not in (R/'data/scripts/tv.inc').read_text()
