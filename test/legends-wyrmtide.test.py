"""Focused progression, ID allocation and topology checks for Wyrmtide Isle."""
from pathlib import Path
import re,json,struct,subprocess,tempfile,collections
R=Path(__file__).resolve().parents[1]
# Resolve the common Emerald/FRLG flag namespace, including symbolic aliases.
flags=(R/'include/constants/opponents.h').read_text()+'\n'+(R/'include/constants/flags.h').read_text();defs=dict(re.findall(r'^#define\s+(\w+)\s+([^\n/]+)',flags,re.M))
def value(k,seen=()):
 if k in seen:raise ValueError(k)
 s=re.sub(r'\b[A-Z_]\w*\b',lambda m:str(value(m[0],seen+(k,))),defs[k].strip())
 if not re.fullmatch(r'[\dxa-fA-F\s()+*<>&|~\-]+',s):raise ValueError(k)
 return eval(s,{'__builtins__':{}})
for n,name in enumerate(['CALL','LANDED','SEAL_OPEN','AWAKENED','CALMED','CAUGHT','REPORT'],0x493):
 aliases=set()
 for k in defs:
  try:
   if value(k)==n:aliases.add(k)
  except Exception:pass
 assert aliases=={f'FLAG_LEGENDS_WYRMTIDE_{name}',f'FLAG_UNUSED_0x{n:X}'},aliases
assert max(range(0x493,0x49A))<value('TRAINER_FLAGS_START') if 'TRAINER_FLAGS_START' in defs else True
assert 0x499<value('TRAINER_FLAGS_START') if 'TRAINER_FLAGS_START' in defs else 0x499<0x500
# Existing maps/layout IDs/section IDs and binary owner art remain intact.
import hashlib
baseline=json.loads((R/'docs/qa/wyrmtide-id-baseline.json').read_text())
hashlist=lambda xs:hashlib.sha256(json.dumps(xs,separators=(',',':')).encode()).hexdigest()
groups=json.loads((R/'data/maps/map_groups.json').read_text())
for k,v in baseline['mapGroups'].items():assert hashlist(groups[k][:v['count']])==v['sha256'],k
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];v=baseline['layoutIds'];assert hashlist([l['id'] for l in layouts[:v['count']]])==v['sha256']
secs=json.loads((R/'src/data/region_map/region_map_sections.json').read_text())['map_sections'];v=baseline['nativeMapSectionIds'];assert len(secs)==v['count'] and hashlist([s['id'] for s in secs])==v['sha256']
# No uncommitted native layout/tileset overwrite during local authoring; CI also
# verifies the immutable ID baseline and original/sibling asset relationship.
changed=subprocess.check_output(['git','diff','--name-only','HEAD','--','data/layouts','data/tilesets'],cwd=R,text=True).splitlines();assert all(x=='data/layouts/layouts.json' or 'LegendsWyrmtide_' in x or '/legends_wyrmtide/' in x for x in changed),changed
base=R/'data/tilesets/secondary/cave';sib=R/'data/tilesets/legends_wyrmtide'
assert (sib/'metatiles.bin').read_bytes()==(m:=(base/'metatiles.bin').read_bytes())+m[64:80]
assert (sib/'metatile_attributes.bin').read_bytes()==(base/'metatile_attributes.bin').read_bytes()+struct.pack('<H',0x61)
# Every stair landing is reachable on foot, and both directions retain exact pairs.
for key in ['Descent1','Descent2','Descent3','Descent4','Heart']:
 name='LegendsWyrmtide_'+key;m=json.loads((R/f'data/maps/{name}/map.json').read_text());l=next(x for x in layouts if x['id']==m['layout']);a=struct.unpack('<%dH'%(l['width']*l['height']),(R/l['blockdata_filepath']).read_bytes());w=l['width'];start=(8,3) if key!='Heart' else (11,17);goal=(11,20) if key!='Heart' else (11,8)
 q=collections.deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for xx,yy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if 0<=xx<w and 0<=yy<l['height'] and not a[yy*w+xx]&0xC00 and (xx,yy) not in seen:seen.add((xx,yy));q.append((xx,yy))
 assert goal in seen,(key,'unreachable descent')
 for i,warp in enumerate(m['warp_events']):
  destkey=warp['dest_map'].removeprefix('MAP_LEGENDS_WYRMTIDE_');destname='LegendsWyrmtide_'+({'ISLE':'Isle','HEART':'Heart'}.get(destkey,destkey.title()))
  dest=json.loads((R/f'data/maps/{destname}/map.json').read_text());back=dest['warp_events'][int(warp['dest_warp_id'])];assert back['dest_map']==m['id'] and int(back['dest_warp_id'])==i,(key,i)
script=(R/'data/scripts/legends_wyrmtide.inc').read_text();assert 'specialvar VAR_RESULT, LegendsWyrmtideHasMaker' in script
assert 'BottomMid, FALSE' in script and 'B_OUTCOME_CAUGHT, Wyrmtide_Caught' in script and 'B_OUTCOME_WON, Wyrmtide_Calmed' in script
# Compile actual production C with deterministic native engine boundaries.
src=re.sub(r'^#include .*$', '',(R/'src/legends_wyrmtide.c').read_text(),flags=re.M)
names={k:i for i,k in enumerate(sorted(set(re.findall(r'FLAG_[A-Z0-9_]+',src))))}
prefix='''#include <assert.h>
#include <stdint.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;typedef int16_t s16;typedef unsigned u32;typedef int bool32;
#define EWRAM_DATA
#define TRUE 1
#define FALSE 0
#define IS_FRLG 0
#define B_TRAINER_PLAYER 0
#define MON_DATA_SPECIES 0
#define MON_DATA_IS_EGG 1
#define SPECIES_REGIGIGAS 486
#define MAP_TYPE_ROUTE 1
#define MAP_TYPE_CITY 2
#define MAP_TYPE_TOWN 3
#define MAP_DEWFORD_TOWN 1
#define MAP_GROUP(x) 0
#define MAP_NUM(x) 1
#define LOCALID_WYRMTIDE_BRINEY 6
#define LOCALID_WYRMTIDE_BOAT 7
static int bits[100],calls,partyCount,spawned;static s16 px=18,py=18;
struct ObjectEventTemplate{int localId,x,y;};
struct Events{int objectEventCount;struct ObjectEventTemplate *objectEvents;} ev;
struct ObjectEventTemplate templates[8];
struct {int mapType;struct Events *events;} gMapHeader;
struct {struct {int mapGroup,mapNum;} location;struct ObjectEventTemplate objectEventTemplates[8];} sb,*gSaveBlock1Ptr=&sb;
struct Mon{int species,egg;} gParties[1][6];
const u8 Wyrmtide_UnknownCall[]={0};
static int FlagGet(int f){return bits[f];}static void FlagClear(int f){bits[f]=0;}
static void ScriptContext_SetupScript(const u8 *s){assert(s==Wyrmtide_UnknownCall);calls++;}
static int CalculatePlayerPartyCount(void){return partyCount;}
static int GetMonData(struct Mon *m,int d){return d?m->egg:m->species;}
static void PlayerGetDestCoords(s16*x,s16*y){*x=px;*y=py;}
static int TryGetObjectEventIdByLocalIdAndMap(int a,int b,int c,u8*d){return 1;}
static void TrySpawnObjectEvent(int a,int b,int c){spawned++;}
void LegendsWyrmtideRefreshDewford(void);
'''+''.join(f'#define {n} {i}\n' for n,i in names.items())
test='''
int main(void){
 gMapHeader.mapType=MAP_TYPE_ROUTE;
 for(int i=0;i<20;i++)assert(!LegendsWyrmtideTryCall());
 bits[FLAG_RECEIVED_POKENAV]=1;bits[FLAG_LEGENDS_STORY_REGIGIGAS_CALMED]=1;
 for(int i=0;i<20;i++)assert(!LegendsWyrmtideTryCall());
 bits[FLAG_LEGENDS_STORY_WEATHER_REPORT]=1;
 for(int i=0;i<7;i++)assert(!LegendsWyrmtideTryCall());assert(LegendsWyrmtideTryCall()&&calls==1);
 bits[FLAG_LEGENDS_WYRMTIDE_CALL]=1;for(int i=0;i<20;i++)assert(!LegendsWyrmtideTryCall());assert(calls==1);
 bits[FLAG_LEGENDS_WYRMTIDE_CALL]=0;gMapHeader.mapType=99;for(int i=0;i<20;i++)assert(!LegendsWyrmtideTryCall());
 gMapHeader.mapType=MAP_TYPE_TOWN;bits[FLAG_SYS_SAFARI_MODE]=1;for(int i=0;i<20;i++)assert(!LegendsWyrmtideTryCall());
 bits[FLAG_SYS_SAFARI_MODE]=0;for(int i=0;i<7;i++)assert(!LegendsWyrmtideTryCall());assert(LegendsWyrmtideTryCall());
 assert(!LegendsWyrmtideHasMaker());partyCount=1;gParties[0][0].species=SPECIES_REGIGIGAS;assert(LegendsWyrmtideHasMaker());
 gParties[0][0].egg=1;assert(!LegendsWyrmtideHasMaker());gParties[0][0].egg=0;partyCount=0;assert(!LegendsWyrmtideHasMaker());
 gMapHeader.events=&ev;ev.objectEventCount=8;ev.objectEvents=templates;templates[6]=(struct ObjectEventTemplate){6,12,9};templates[7]=(struct ObjectEventTemplate){7,12,8};bits[FLAG_LEGENDS_WYRMTIDE_CALL]=1;
 sb.location.mapNum=1;bits[FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN]=1;bits[FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN]=1;
 px=19;py=16;spawned=0;LegendsWyrmtideRefreshDewford();assert(spawned==1); // occupied Briney square
 px=18;py=18;spawned=0;LegendsWyrmtideRefreshDewford();assert(spawned==2);
 puts("PASS production call prerequisites/eight-step delay/once-only/indoor/Safari gates, party/egg exclusion and safe dock spawn");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(prefix+src+test);subprocess.run(['cc','-std=c11','-O2',str(p),'-o',str(Path(d)/'test')],check=True);subprocess.run([str(Path(d)/'test')],check=True)
print('PASS native flag allocation, append-only IDs/layouts, protected owner assets, sibling stair art and all stair return pairs')
