"""Exercise shipped Birch request and journal C, including legacy words and atomic rewards."""
from pathlib import Path
import subprocess,tempfile,re,hashlib,json
R=Path(__file__).resolve().parents[1]
ns={'__file__':str(R/'test/legends-journal.test.py')}
exec((R/'test/legends-journal.test.py').read_text().split('with tempfile.TemporaryDirectory()')[0],ns)
preamble='#define TEST_REAL_FIELD_REQUESTS\n'+ns['preamble'].replace('#define FLAG_GET_CAUGHT 1','#include "constants/pokedex.h"')
stubs=r'''
#include "constants/vars.h"
#include "constants/species.h"
#include "constants/moves.h"
#include "constants/pokedex.h"
#include "constants/pokemon.h"
#define PARTY_SIZE 6
#define MAX_MON_MOVES 4
#define B_TRAINER_PLAYER 0
#define MON_DATA_SPECIES 0
#define MON_DATA_IS_EGG 1
#define MON_DATA_MOVE1 2
#define MAP_PETALBURG_WOODS 0x101
#define MAP_ROUTE104 0x102
#define MAP_GROUP(x) ((x)>>8)
#define MAP_NUM(x) ((x)&255)
struct Pokemon {u16 species;u8 egg;u16 moves[4];};
static struct Pokemon gParties[1][6];static u8 gPartiesCount[1];
static const struct {u8 types[2];} gSpeciesInfo[NUM_SPECIES]={
 [SPECIES_TREECKO]={{TYPE_GRASS,TYPE_GRASS}},[SPECIES_WURMPLE]={{TYPE_BUG,TYPE_BUG}},
 [SPECIES_WINGULL]={{TYPE_WATER,TYPE_FLYING}},[SPECIES_PELIPPER]={{TYPE_WATER,TYPE_FLYING}},
 [SPECIES_ZIGZAGOON]={{TYPE_NORMAL,TYPE_NORMAL}},[SPECIES_POOCHYENA]={{TYPE_DARK,TYPE_DARK}},
};
static struct {struct {u8 mapGroup,mapNum;} location;} save1,*gSaveBlock1Ptr=&save1;
static u16 vars[256],caught[2048],berries,gSpecialVar_Result,gSpecialVar_0x8004;
static u8 gStringVar1[256],gStringVar4[1000];static unsigned writes,removed;
u16 VarGet(u16 id){assert(id>=0x4000&&id<=0x40ff);return vars[id-0x4000];}
void VarSet(u16 id,u16 value){assert(id>=0x4000&&id<=0x40ff);vars[id-0x4000]=value;writes++;}
u32 GetMonData(struct Pokemon *m,u8 field){if(field==MON_DATA_SPECIES)return m->species;if(field==MON_DATA_IS_EGG)return m->egg;assert(field>=MON_DATA_MOVE1&&field<MON_DATA_MOVE1+4);return m->moves[field-MON_DATA_MOVE1];}
bool32 GetSetPokedexFlag(u16 id,u8 mode){assert(id<2048&&mode==FLAG_GET_CAUGHT);return caught[id];}
bool32 CheckBagHasItem(u16 item,u16 n){assert(item==ITEM_ORAN_BERRY);return berries>=n;}
bool32 RemoveBagItem(u16 item,u16 n){assert(CheckBagHasItem(item,n));berries-=n;removed+=n;return TRUE;}
u8 *StringCopy(u8 *d,const u8 *s){return (u8*)strcpy((char*)d,(const char*)s);}
u8 *StringAppend(u8 *d,const u8 *s){return (u8*)strcat((char*)d,(const char*)s);}
'''
source='\n'.join(l for l in (R/'src/legends_field_requests.c').read_text().splitlines() if not l.startswith('#include')).replace(r'\p', r'\n')
main=r'''
static void Reset(void){memset(&data,0,sizeof(data));memset(flags,0,sizeof(flags));memset(stats,0,sizeof(stats));memset(vars,0,sizeof(vars));memset(caught,0,sizeof(caught));memset(gParties,0,sizeof(gParties));memset(&save1,0,sizeof(save1));gPartiesCount[0]=0;pcQuantity=pcItem=full=linked=dex=writes=removed=berries=0;flags[FLAG_SYS_POKEDEX_GET]=1;LegendsJournalInit(TRUE);}
static void Map(u16 map){save1.location.mapGroup=MAP_GROUP(map);save1.location.mapNum=MAP_NUM(map);}
static void Mon(u8 slot,u16 species,u8 egg){gParties[0][slot].species=species;gParties[0][slot].egg=egg;if(gPartiesCount[0]<=slot)gPartiesCount[0]=slot+1;}
int main(void){
 Reset();
 // Exhaustive legacy active words: readers never initialize or modify data.
 for(unsigned word=0;word<65536;word++){
  vars[VAR_LEGENDS_FIELD_REQUEST_STATE-0x4000]=word;
  unsigned n=writes;u16 before[256];memcpy(before,vars,sizeof(vars));
  LegendsFieldRequestActive();for(unsigned id=0;id<6;id++)LegendsFieldRequestComplete(id);
  assert(n==writes&&!memcmp(before,vars,sizeof(vars)));
 }
 Reset();flags[FLAG_SYS_POKEDEX_GET]=0;assert(LegendsFieldRequestAccept(0)==FIELD_REQUEST_INVALID);assert(writes==0);
 flags[FLAG_SYS_POKEDEX_GET]=1;linked=1;assert(LegendsFieldRequestAccept(0)==FIELD_REQUEST_INVALID);assert(writes==0);linked=0;
 assert(LegendsFieldRequestAccept(6)==FIELD_REQUEST_INVALID);
 // Every quest is selectable, one at a time; abandon/reselect does not touch inventory.
 for(unsigned id=0;id<6;id++){
  Reset();VarSet(VAR_LEGENDS_HOMECOMING_MEMORY,0xd666);vars[0x6b]=0xffff;vars[0x6c]=0xa5a5;vars[0x6d]=0xffff;
  assert(LegendsFieldRequestAccept(id)==FIELD_REQUEST_OK);assert(LegendsFieldRequestActive()==id);
  assert(LegendsQuestVisible(33+id)&&LegendsQuestTracked()==33+id);
  for(unsigned other=0;other<6;other++)assert(LegendsFieldRequestAccept(other)==FIELD_REQUEST_BUSY);
  assert(LegendsFieldRequestAbandon());assert(LegendsFieldRequestActive()==FIELD_REQUEST_NONE);
  assert(!LegendsQuestVisible(33+id)&&LegendsQuestTracked()==0xffff);assert(!pcQuantity&&!removed);
  assert(LegendsFieldRequestAccept(id)==FIELD_REQUEST_OK);assert(VarGet(VAR_LEGENDS_HOMECOMING_MEMORY)==0xd666);
 }
 // Existing pin and achievement claims survive accept/abandon.
 Reset();assert(LegendsQuestTrack(1));data.journal.claimed[0]=0x80;data.journal.checksum=Checksum();
 assert(LegendsFieldRequestAccept(0)==0&&LegendsQuestTracked()==1);assert(data.journal.claimed[0]==0x80);
 assert(LegendsFieldRequestAbandon()&&LegendsQuestTracked()==1);
 // Pokedex records are proof, not a Pokemon handover. Already recorded catches count.
 Reset();assert(LegendsFieldRequestAccept(0)==0);caught[NATIONAL_DEX_POOCHYENA]=1;
 assert(LegendsQuestStepComplete(33,0)&&!LegendsQuestStepComplete(33,1));assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_NOT_READY);
 caught[NATIONAL_DEX_ZIGZAGOON]=1;assert(LegendsQuestNextStep(33)==2);assert(LegendsFieldRequestSubmit()==0);
 assert(pcQuantity==5&&pcItem==ITEM_POKE_BALL&&LegendsQuestComplete(33)&&LegendsQuestTracked()==0xffff);
 assert(LegendsQuestVisible(33)&&LegendsQuestStepComplete(33,2));assert(LegendsFieldRequestAccept(0)==FIELD_REQUEST_FINISHED);
 assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_INVALID&&pcQuantity==5);
 LegendsFieldRequestsPrepareMenu();assert(!strncmp((char*)gLegendsFieldRequestMenuLabels[0],"Done: ",6));
 // Habitat notes require the active task, matching location and a non-egg partner.
 Reset();Map(MAP_PETALBURG_WOODS);Mon(0,SPECIES_WURMPLE,0);LegendsFieldRequestsObserve();assert(writes==0);
 assert(LegendsFieldRequestAccept(1)==0);Map(MAP_ROUTE104);LegendsFieldRequestsObserve();assert(!LegendsQuestStepComplete(34,0));
 Map(MAP_PETALBURG_WOODS);gParties[0][0].egg=1;LegendsFieldRequestsObserve();assert(!LegendsQuestStepComplete(34,0));
 gParties[0][0].egg=0;LegendsFieldRequestsObserve();assert(LegendsQuestNextStep(34)==1);unsigned n=writes;
 LegendsFieldRequestsObserve();assert(writes==n);Mon(0,SPECIES_TREECKO,0);Map(0);assert(LegendsQuestStepComplete(34,0));
 u16 savedVars[256];struct LegendsJournalSave savedJournal=data.journal;memcpy(savedVars,vars,sizeof(vars));memset(vars,0,sizeof(vars));
 assert(LegendsFieldRequestActive()==FIELD_REQUEST_NONE);memcpy(vars,savedVars,sizeof(vars));data.journal=savedJournal;LegendsJournalInit(FALSE);
 assert(LegendsFieldRequestActive()==1&&LegendsQuestStepComplete(34,0));
 assert(LegendsFieldRequestAbandon());assert(LegendsFieldRequestAccept(1)==0);assert(!LegendsQuestStepComplete(34,0));
 // Full PC is atomic for berry costs; successful turn-in is permanently once-only.
 Reset();berries=3;assert(LegendsFieldRequestAccept(2)==0);full=1;u16 state=VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE);
 assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_STORAGE_FULL&&berries==3&&removed==0&&pcQuantity==0);
 assert(VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE)==state&&!LegendsFieldRequestComplete(2));full=0;
 assert(LegendsFieldRequestSubmit()==0&&berries==0&&removed==3&&pcItem==ITEM_SUPER_POTION&&pcQuantity==2);
 assert(LegendsFieldRequestComplete(2)&&LegendsFieldRequestAccept(2)==FIELD_REQUEST_FINISHED);
 assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_INVALID&&removed==3&&pcQuantity==2);
 // Each coastal evolution qualifies; notes survive moving/boxing, not abandonment.
 for(unsigned species=SPECIES_WINGULL;species<=SPECIES_PELIPPER;species++){
  Reset();assert(LegendsFieldRequestAccept(3)==0);Map(MAP_ROUTE104);Mon(0,species,1);LegendsFieldRequestsObserve();assert(!LegendsQuestStepComplete(36,0));
  Mon(0,species,0);LegendsFieldRequestsObserve();assert(LegendsQuestStepComplete(36,0));assert(LegendsFieldRequestSubmit()==0&&pcItem==ITEM_NET_BALL&&pcQuantity==2);
 }
 // All draining-move slots/upgrades work; eggs never serve as research samples.
 for(unsigned move=0;move<4;move++){
  Reset();assert(LegendsFieldRequestAccept(4)==0);Mon(0,SPECIES_TREECKO,1);gParties[0][0].moves[move]=MOVE_GIGA_DRAIN;
  assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_NOT_READY);gParties[0][0].egg=0;
  assert(LegendsFieldRequestSubmit()==0&&pcItem==ITEM_HEAL_BALL&&pcQuantity==3);
 }
 // Unique types include both dual types but never double-count duplicates/eggs.
 Reset();assert(LegendsFieldRequestAccept(5)==0);Mon(0,SPECIES_WINGULL,0);Mon(1,SPECIES_PELIPPER,0);
 assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_NOT_READY);Mon(2,SPECIES_ZIGZAGOON,1);assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_NOT_READY);
 Mon(2,SPECIES_ZIGZAGOON,0);assert(LegendsFieldRequestSubmit()==0&&pcItem==ITEM_RARE_CANDY&&pcQuantity==1);
 // Linked sessions cannot abandon, accept or claim, even when proof is ready.
 Reset();assert(LegendsFieldRequestAccept(2)==0);berries=3;linked=1;state=VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE);
 assert(!LegendsFieldRequestAbandon()&&LegendsFieldRequestSubmit()==FIELD_REQUEST_INVALID);assert(berries==3&&!pcQuantity&&VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE)==state);
 assert(sizeof(struct LegendsJournalSave)==36&&offsetof(struct LegendsJournalSave,earned)==12&&offsetof(struct LegendsJournalSave,claimed)==24);
 puts("PASS: six requests, legacy words, one-active, retry/abandon, proof, full-PC costs, one-time rewards, journal pins and save snapshots");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'field.c').write_text(preamble+stubs+ns['s']+'\n'+source+'\n'+main)
 subprocess.run(['cc','-std=gnu11','-Wall','-Wextra','-Werror','-Wno-unused-parameter','-iquote',str(R/'include'),'-iquote',str(R),str(p/'field.c'),'-o',str(p/'field')],check=True)
 subprocess.run([str(p/'field')],check=True)
# Native font bounds, stable untouched native slots and catalogue identities.
chars={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)};chars["'"]=0xb4
widths=list(map(int,re.findall(r'\d+',(R/'src/fonts.c').read_text().split('gFontNormalLatinGlyphWidths[] = {')[1].split('};')[0])))
for path in ['src/legends_field_requests.c','data/scripts/legends_field_requests.inc']:
 s=(R/path).read_text();strings=re.findall(r'COMPOUND_STRING\("(.*?)"\)',s) if path.endswith('.c') else re.findall(r'\.string "(.*?)"',s)
 for text in strings:
  for line in re.split(r'\\[npl]',text.replace('{EACUTE}','é').replace('$','').replace('{STR_VAR_1}','2 SUPER POTIONS')):
   assert sum(widths[chars[c]] for c in line)<=208,line
for base in ['src','data']:
 for p in (R/base).rglob('*'):
  if p.suffix in ['.c','.inc','.s','.json']:
   s=p.read_text(errors='ignore')
   for name in ['VAR_ROUTE112_STATE','VAR_ROUTE113_STATE','VAR_ROUTE114_STATE']:assert name not in s,(p,name)
print('PASS: native text widths and verified-unused native save slots')

# The 33 previously published quests keep every byte and stable ID.
catalogue=(R/'src/data/legends/journal.h').read_text().split('static const struct LegendsAchievement')[0]
entries=re.findall(r'^    \{COMPOUND_STRING.*$',catalogue,re.M)
assert len(entries)==39 and hashlib.sha256(('\n'.join(entries[:33])+'\n').encode()).hexdigest()=='79a3781ce4a11339786e5d464da1e837e7f0bae28646f7c2feff77cf3b46674f'
