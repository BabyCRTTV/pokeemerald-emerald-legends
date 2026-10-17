"""Exercise shipped Birch request and journal C, including legacy words and atomic rewards."""
from pathlib import Path
import subprocess,tempfile,re,hashlib,json
R=Path(__file__).resolve().parents[1]
ns={'__file__':str(R/'test/legends-journal.test.py')}
exec((R/'test/legends-journal.test.py').read_text().split('with tempfile.TemporaryDirectory()')[0],ns)
preamble='#define TEST_REAL_FIELD_REQUESTS\n'+ns['preamble'].replace('#define FLAG_GET_CAUGHT 1','#include "constants/pokedex.h"')
groups=json.loads((R/'data/maps/map_groups.json').read_text());map_lines=['#define MAP_UNDEFINED 0xffff']
for group_id,group in enumerate(groups['group_order']):
 for map_id,name in enumerate(groups[group]):
  info=json.loads((R/'data/maps'/name/'map.json').read_text())
  map_lines.append('#define '+info['id']+' '+str((group_id<<8)|map_id))
map_defines='\n'.join(map_lines)
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
''' + map_defines + r'''
#define MAP_GROUP(x) ((x)>>8)
#define MAP_NUM(x) ((x)&255)
struct Pokemon {u16 species;u8 egg;u16 moves[4];};
static struct Pokemon gParties[1][6];static u8 gPartiesCount[1];
static const struct {u8 types[2];} gSpeciesInfo[NUM_SPECIES]={
 [SPECIES_TREECKO]={{TYPE_GRASS,TYPE_GRASS}},[SPECIES_WURMPLE]={{TYPE_BUG,TYPE_BUG}},
 [SPECIES_WINGULL]={{TYPE_WATER,TYPE_FLYING}},[SPECIES_PELIPPER]={{TYPE_WATER,TYPE_FLYING}},
 [SPECIES_GEODUDE]={{TYPE_ROCK,TYPE_GROUND}},[SPECIES_ELECTRIKE]={{TYPE_ELECTRIC,TYPE_ELECTRIC}},
 [SPECIES_SANDSHREW]={{TYPE_GROUND,TYPE_GROUND}},[SPECIES_SHUPPET]={{TYPE_GHOST,TYPE_GHOST}},
 [SPECIES_SPHEAL]={{TYPE_ICE,TYPE_WATER}},[SPECIES_ARON]={{TYPE_STEEL,TYPE_ROCK}},
 [SPECIES_RALTS]={{TYPE_PSYCHIC,TYPE_FAIRY}},[SPECIES_NUMEL]={{TYPE_FIRE,TYPE_GROUND}},
 [SPECIES_ZIGZAGOON]={{TYPE_NORMAL,TYPE_NORMAL}},[SPECIES_POOCHYENA]={{TYPE_DARK,TYPE_DARK}},
};
static struct {struct {u8 mapGroup,mapNum;} location;} save1,*gSaveBlock1Ptr=&save1;
static u16 vars[256],caught[2048],berries,gSpecialVar_Result,gSpecialVar_0x8004;
static u8 gStringVar1[256],gStringVar2[256],gStringVar4[1000];static unsigned writes,removed;
u16 VarGet(u16 id){assert(id>=0x4000&&id<=0x40ff);return vars[id-0x4000];}
void VarSet(u16 id,u16 value){assert(id>=0x4000&&id<=0x40ff);vars[id-0x4000]=value;writes++;}
u32 GetMonData(struct Pokemon *m,u8 field){if(field==MON_DATA_SPECIES)return m->species;if(field==MON_DATA_IS_EGG)return m->egg;assert(field>=MON_DATA_MOVE1&&field<MON_DATA_MOVE1+4);return m->moves[field-MON_DATA_MOVE1];}
bool32 GetSetPokedexFlag(u16 id,u8 mode){assert(id<2048&&mode==FLAG_GET_CAUGHT);return caught[id];}
u16 GetHoennPokedexCount(u8 mode){return dex;}
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
 // Read-only research reflections: every count, both patrons, other-patron reports and legacy B7.
 for(unsigned patron=0;patron<2;patron++)for(unsigned n=0;n<=(patron?12:18);n++){
  Reset();u32 mask=n?((1u<<n)-1):0;
  u32 done=patron?((mask<<18)|0x3ffff):((0xfffu<<18)|mask);
  vars[VAR_LEGENDS_FIELD_REQUEST_STATE-0x4000]=0xB800;
  vars[VAR_LEGENDS_FIELD_REQUEST_DONE-0x4000]=done;
  vars[VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH-0x4000]=done>>16;
  if(patron)LegendsFieldRequestsBeginDevon();else LegendsFieldRequestsBeginBirch();
  u16 snapshot[256];memcpy(snapshot,vars,sizeof(vars));unsigned w=writes;
  LegendsFieldRequestsResearchNotes();unsigned expected=n==(patron?12:18)?3:n>=(patron?6:9)?2:n>=3?1:0;
  assert(gSpecialVar_Result==expected&&writes==w&&!memcmp(snapshot,vars,sizeof(vars)));
 }
 Reset();vars[VAR_LEGENDS_FIELD_REQUEST_STATE-0x4000]=0xB700;vars[VAR_LEGENDS_FIELD_REQUEST_DONE-0x4000]=0x3f;
 vars[VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH-0x4000]=0xffff;unsigned legacyWrites=writes;
 LegendsFieldRequestsBeginBirch();LegendsFieldRequestsResearchNotes();assert(gSpecialVar_Result==1);
 LegendsFieldRequestsBeginDevon();LegendsFieldRequestsResearchNotes();assert(gSpecialVar_Result==0&&writes==legacyWrites&&vars[VAR_LEGENDS_FIELD_REQUEST_STATE-0x4000]==0xB700);
 Reset();LegendsFieldRequestsBeginBirch();
 // Exhaustive legacy active words: readers never initialize or modify data.
 for(unsigned word=0;word<65536;word++){
  vars[VAR_LEGENDS_FIELD_REQUEST_STATE-0x4000]=word;
  unsigned n=writes;u16 before[256];memcpy(before,vars,sizeof(vars));
  LegendsFieldRequestActive();for(unsigned id=0;id<6;id++)LegendsFieldRequestComplete(id);
  assert(n==writes&&!memcmp(before,vars,sizeof(vars)));
 }
 Reset();flags[FLAG_SYS_POKEDEX_GET]=0;assert(LegendsFieldRequestAccept(0)==FIELD_REQUEST_INVALID);assert(writes==0);
 flags[FLAG_SYS_POKEDEX_GET]=1;linked=1;assert(LegendsFieldRequestAccept(0)==FIELD_REQUEST_INVALID);assert(writes==0);linked=0;
 assert(LegendsFieldRequestAccept(30)==FIELD_REQUEST_INVALID);
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

 // v0.0.58 signed words survive read-only initialization even with arbitrary high words.
 Reset();vars[0x6b]=0xb702;vars[0x6c]=0x25;vars[0x6d]=2;vars[0x7a]=0xdead;vars[0x77]=0xbeef;
 assert(LegendsFieldRequestActive()==1&&LegendsFieldRequestComplete(0)&&LegendsFieldRequestComplete(2)&&LegendsFieldRequestComplete(5));
 assert(NoteBits()==2&&DoneBits()==0x25&&vars[0x7a]==0xdead&&vars[0x77]==0xbeef);
 LegendsJournalInit(FALSE);assert(LegendsFieldRequestActive()==1&&NoteBits()==2);
 assert(LegendsFieldRequestAbandon());assert(vars[0x6b]==0xb800&&vars[0x6c]==0x25&&!vars[0x7a]&&vars[0x77]==0xbeef);
 assert(LegendsFieldRequestAccept(1)==0&&!LegendsQuestStepComplete(34,0));
 // Migration on successful v1 report preserves every prior completion.
 Reset();vars[0x6b]=0xb703;vars[0x6c]=0x23;vars[0x6d]=0;vars[0x7a]=0xdead;vars[0x77]=0xbeef;berries=3;
 full=1;assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_STORAGE_FULL&&vars[0x6b]==0xb703&&vars[0x7a]==0xdead);
 full=0;assert(LegendsFieldRequestSubmit()==0&&DoneBits()==0x27&&vars[0x6b]==0xb800&&!vars[0x7a]&&vars[0x77]==0xbeef);
 // New gates reject acceptance without mutating existing state or inventing completion.
 for(unsigned id=6;id<30;id++){
  Reset();u16 snapshot[256];memcpy(snapshot,vars,sizeof(vars));
  assert(!LegendsFieldRequestUnlocked(id)&&LegendsFieldRequestAccept(id)==FIELD_REQUEST_LOCKED);
  assert(!memcmp(snapshot,vars,sizeof(vars)));
  flags[sRequests[id].gate]=1;
  if(id>=18)flags[FLAG_RECEIVED_POKENAV]=1;
  if(id==17||id==29){
   assert(!LegendsFieldRequestUnlocked(id));
   vars[0x6b]=0xb800;u32 prior=id==17?((1u<<17)-1):(((1u<<29)-1)&~((1u<<18)-1));
   vars[0x6c]=prior;vars[0x7a]=prior>>16;
  }
  assert(LegendsFieldRequestUnlocked(id)&&LegendsFieldRequestAccept(id)==0);
  assert(LegendsFieldRequestActive()==id&&LegendsQuestTracked()==33+id);
  assert(LegendsFieldRequestAccept(id<18?18:0)==FIELD_REQUEST_BUSY);
  assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_NOT_READY);
  const struct FieldRequest *request=&sRequests[id];
  switch(request->proof){
  case PROOF_HABITAT_TYPE:{
   u16 sample=SPECIES_NONE;
   for(unsigned sp=1;sp<NUM_SPECIES;sp++)if(gSpeciesInfo[sp].types[0]==request->arg||gSpeciesInfo[sp].types[1]==request->arg){sample=sp;break;}
   assert(sample);Map(request->map);Mon(0,sample,1);LegendsFieldRequestsObserve();assert(!LegendsFieldRequestStepComplete(id,0));
   Mon(0,sample,0);Map(MAP_UNDEFINED);LegendsFieldRequestsObserve();assert(!LegendsFieldRequestStepComplete(id,0));
   Map(request->map2?request->map2:request->map);LegendsFieldRequestsObserve();assert(NoteBits()==(1u<<id));break;}
  case PROOF_HABITAT_SPECIES:Map(request->map);Mon(0,request->arg,1);LegendsFieldRequestsObserve();assert(!LegendsFieldRequestStepComplete(id,0));Mon(0,request->arg,0);LegendsFieldRequestsObserve();break;
  case PROOF_CAUGHT_PAIR:caught[request->arg]=1;assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_NOT_READY);caught[request->second]=1;break;
  case PROOF_MOVE:Mon(0,SPECIES_TREECKO,0);gParties[0][0].moves[3]=request->arg;break;
  case PROOF_TYPES:Mon(0,SPECIES_WINGULL,0);Mon(1,SPECIES_ARON,0);Mon(2,SPECIES_TREECKO,0);Mon(3,SPECIES_POOCHYENA,0);break;
  case PROOF_DEX_COUNT:dex=request->arg-1;assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_NOT_READY);dex++;break;
  default:assert(0);
  }
  assert(LegendsFieldRequestStepComplete(id,0));
  u16 snap[256];memcpy(snap,vars,sizeof(vars));full=1;assert(LegendsFieldRequestSubmit()==FIELD_REQUEST_STORAGE_FULL);assert(!memcmp(snap,vars,sizeof(vars)));full=0;
  assert(LegendsFieldRequestSubmit()==0&&pcItem==request->rewardItem&&pcQuantity==request->rewardCount);
  assert(LegendsFieldRequestComplete(id)&&LegendsQuestComplete(33+id)&&LegendsQuestTracked()==0xffff);
  assert(LegendsFieldRequestAccept(id)==FIELD_REQUEST_FINISHED&&LegendsFieldRequestSubmit()==FIELD_REQUEST_INVALID);
  if(id==29)assert(pcItem==ITEM_MASTER_BALL&&pcQuantity==1&&vars[0x7a]&(1u<<13));
  u16 saved[256];memcpy(saved,vars,sizeof(vars));memset(vars,0,sizeof(vars));memcpy(vars,saved,sizeof(vars));LegendsJournalInit(FALSE);assert(LegendsFieldRequestComplete(id));
 }
 // Both menus reject turning in/abandoning another patron's request.
 Reset();assert(LegendsFieldRequestAccept(2)==0);berries=3;LegendsFieldRequestsBeginDevon();LegendsFieldRequestsCanReview();assert(!gSpecialVar_Result);
 LegendsFieldRequestsSubmitSpecial();assert(gSpecialVar_Result==FIELD_REQUEST_INVALID&&!pcQuantity);
 LegendsFieldRequestsAbandonSpecial();assert(!gSpecialVar_Result&&LegendsFieldRequestActive()==2);
 LegendsFieldRequestsBeginBirch();LegendsFieldRequestsCanReview();assert(gSpecialVar_Result);
 // Page labels and mappings cover all 30 requests, without increasing native menu height.
 for(unsigned patron=0;patron<2;patron++){
  if(patron)LegendsFieldRequestsBeginDevon();else LegendsFieldRequestsBeginBirch();
  for(unsigned group=0;group<(patron?2:3);group++){
   gSpecialVar_0x8004=group;LegendsFieldRequestsSelectGroup();assert(gSpecialVar_Result);LegendsFieldRequestsPrepareMenu();
   for(unsigned row=0;row<6;row++){gSpecialVar_0x8004=row;LegendsFieldRequestsSelectRow();assert(gSpecialVar_Result&&gSpecialVar_0x8004==(patron?18:0)+group*6+row);}
  }
 }

 gSpecialVar_0x8004=127;LegendsFieldRequestsSelectGroup();assert(!gSpecialVar_Result);LegendsFieldRequestsPrepareMenu();
 // Linked sessions cannot abandon, accept or claim, even when proof is ready.
 Reset();assert(LegendsFieldRequestAccept(2)==0);berries=3;linked=1;state=VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE);
 assert(!LegendsFieldRequestAbandon()&&LegendsFieldRequestSubmit()==FIELD_REQUEST_INVALID);assert(berries==3&&!pcQuantity&&VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE)==state);
 assert(sizeof(struct LegendsJournalSave)==36&&offsetof(struct LegendsJournalSave,earned)==12&&offsetof(struct LegendsJournalSave,claimed)==24);
 puts("PASS: 30 requests, v1/v2 migration, story gates, capstones, patron ownership, paging, legacy words, one-active, retry/abandon, proof, full-PC costs, one-time rewards, journal pins and save snapshots");
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
  for line in re.split(r'\\[npl]',text.replace('{EACUTE}','é').replace('$','').replace('{STR_VAR_1}','3 RARE CANDIES').replace('{STR_VAR_2}','MR. STONE')):
   assert sum(widths[chars[c]] for c in line)<=208,line
for base in ['src','data']:
 for p in (R/base).rglob('*'):
  if p.suffix in ['.c','.inc','.s','.json']:
   s=p.read_text(errors='ignore')
   for name in ['VAR_ROUTE112_STATE','VAR_ROUTE113_STATE','VAR_ROUTE114_STATE','VAR_ROUTE127_STATE','VAR_0x407A']:assert name not in s,(p,name)
print('PASS: native text widths and verified-unused native save slots')

# The 33 previously published quests keep every byte and stable ID.
catalogue=(R/'src/data/legends/journal.h').read_text().split('static const struct LegendsAchievement')[0]
entries=re.findall(r'^    \{COMPOUND_STRING.*$',catalogue,re.M)
assert len(entries)==63 and hashlib.sha256(('\n'.join(entries[:33])+'\n').encode()).hexdigest()=='79a3781ce4a11339786e5d464da1e837e7f0bae28646f7c2feff77cf3b46674f'

assert hashlib.sha256(('\n'.join(entries[:39])+'\n').encode()).hexdigest()=='cb08a14e4f2c7133eb2a6abd5bf27f223a9ad36e045631785c6a0ada411f65bd'

# Resolve symbolic aliases too: the Seafoam entry aliases an unused-looking route slot.
definitions={}
for f in ['include/constants/vars.h','include/constants/vars_frlg.h']:
 definitions.update(re.findall(r'^#define\s+(VAR_\w+)\s+(0x[0-9A-Fa-f]+|VAR_\w+)\b',(R/f).read_text(),re.M))
def value(name,seen=()):
 if name in seen or name not in definitions:return None
 expression=definitions[name]
 return int(expression,16) if expression.startswith('0x') else value(expression,seen+(name,))
aliases=[n for n in definitions if value(n)==0x407a and n!='VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH']
for base in ['src','data','include']:
 for path in (R/base).rglob('*'):
  if path.suffix in ['.c','.inc','.s','.json','.h'] and path.name not in ['vars.h','vars_frlg.h']:
   text=path.read_text(errors='ignore')
   for alias in aliases:assert not re.search(r'\b'+alias+r'\b',text),(path,alias)
