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
changed=subprocess.check_output(['git','diff','--name-only','HEAD','--','data/layouts','data/tilesets'],cwd=R,text=True).splitlines();assert all(x=='data/layouts/layouts.json' or 'LegendsWyrmtide_' in x or '/legends_wyrmtide/' in x or '/legends_wyrmtide_shore/' in x for x in changed),changed
base=R/'data/tilesets/secondary/cave';sib=R/'data/tilesets/legends_wyrmtide'
native=(base/'metatiles.bin').read_bytes();authored=(sib/'metatiles.bin').read_bytes()
depth=json.loads((sib/'source.json').read_text())['terraceDepth']
assert authored[:len(native)]==native and len(authored)==len(native)+32+(36+len(depth['variants']))*16
base_mid=lambda mid:next((v['source'] for v in depth['variants'] if v['id']==mid),mid)
assert authored[len(native):len(native)+16]==authored[len(native)+16:len(native)+32]
assert (sib/'metatile_attributes.bin').read_bytes()[:len(native)//8+4]==(base/'metatile_attributes.bin').read_bytes()+struct.pack('<HH',0x61,0)
# Exact native Cave stair art, with no foreign palette or graphics allocation.
source=struct.unpack_from('<8H',native,4*16)
assert struct.unpack_from('<8H',authored,len(native))==source
# Pool-only palette11 leaves native day/night slots5/12 and all old cells intact.
for i in range(8):
 old=struct.unpack_from('<8H',authored,(0x3a0+i-512)*16)
 new=struct.unpack_from('<8H',authored,(0x3a8+i-512)*16)
 assert new[:4]==(0xb1c6,0xb1c7,0xb1c7,0xb1c6) and new[4:]==old[4:]
# Respect the engine's loaded field-palette range, not just unused atlas words.
loaded=int(next(line.split()[2] for line in (R/'include/fieldmap.h').read_text().splitlines() if line.startswith('#define NUM_PALS_TOTAL ')))
assert all(w[0]>>12<loaded for w in struct.iter_unpack('<H',authored[len(native)+32+8*16:])), 'Pool references a reserved/unloaded BG palette'
native_pals=(R/'src/data/tilesets/graphics.h').read_text().split('gTilesetPalettes_Cave[][16]',1)[1].split('};',1)[0]
private_pals=(R/'src/data/tilesets/legends_wyrmtide.h').read_text().split('gTilesetPalettes_LegendsWyrmtideCave[][16]',1)[1].split('};',1)[0]
paths=lambda text:[line.split('"')[1] for line in text.splitlines() if 'INCGFX_U16(' in line]
np,pp=paths(native_pals),paths(private_pals)
assert len(np)==len(pp)==16 and all(np[i]==pp[i] for i in range(16) if i not in [7,8,11]), 'A non-water Cave palette was changed'
pal=[tuple(map(int,line.split())) for line in (sib/'water.pal').read_text().splitlines()[3:19]]
assert len({tuple(c//8 for c in pal[i]) for i in [11,12,13,14]})==4, 'Native ripple shades collapse after RGB555 conversion'
# All old room cells leave field palette11 available for the isolated pool.
for key in ['Descent1','Descent2','Descent3','Descent4','Heart']:
 data=(R/f'data/layouts/LegendsWyrmtide_{key}/map.bin').read_bytes()
 for cell, in struct.iter_unpack('<H',data):
  mid=cell&1023
  if 512<=mid<0x3a8:
   assert all(w[0]>>12!=11 for w in struct.iter_unpack('<H',authored[(mid-512)*16:(mid-511)*16])),(key,mid,'palette11 is occupied')
# Shore: exact Dewford native prefix and every referenced pixel are retained.
from PIL import Image
shore=R/'data/tilesets/legends_wyrmtide_shore';dew=R/'data/tilesets/secondary/dewford'
dewmeta=(dew/'metatiles.bin').read_bytes();shoremeta=(shore/'metatiles.bin').read_bytes()
assert shoremeta[:len(dewmeta)]==dewmeta
pixels=Image.open(shore/'tiles.png');original=Image.open(dew/'tiles.png')
used={e[0]&1023 for e in struct.iter_unpack('<H',dewmeta)}|set(range(682,688))
for tile in used:
 if tile<512:continue
 i=tile-512;rect=(i%16*8,i//16*8,i%16*8+8,i//16*8+8)
 assert pixels.crop(rect).tobytes()==original.crop(rect).tobytes(),('Dewford pixel overwrite',tile)
assert (shore/'metatile_attributes.bin').read_bytes()[:(dew/'metatile_attributes.bin').stat().st_size]==(dew/'metatile_attributes.bin').read_bytes()
lights=json.loads((R/'data/tilesets/legends_lights/manifest.json').read_text())
assert not {e['tile'] for e in lights['families']['general']['cells']}&{e[0]&1023 for e in struct.iter_unpack('<H',shoremeta[len(dewmeta):]) if (e[0]&1023)<512},'Shore column pixels overlap night emission cells'
# Native cave pixels and animation cells remain exact in the expanded sibling.
cp=Image.open(sib/'tiles.png');original=Image.open(base/'tiles.png')
assert cp.crop((0,0,*original.size)).tobytes()==original.tobytes()
# Continuous stair modules occupy only new sibling slots; old definitions stay exact.
stair_bytes=authored[(0x3b1-512)*16:(0x3b9-512)*16]
assert len(stair_bytes)==8*16
assert not {w[0]&1023 for w in struct.iter_unpack('<H',authored[:(0x3b1-512)*16])}&set(range(976,1008)), 'Stair tiles overwrite existing art'
stair_attrs=struct.unpack_from('<8H',(sib/'metatile_attributes.bin').read_bytes(),(0x3b1-512)*2)
assert stair_attrs==(0,0,0,0,0,0,0,0x61), 'Ordinary/warp stair behavior changed'
for n in range(8):
 words=struct.unpack_from('<8H',stair_bytes,n*16)
 assert words[:4]==tuple(0x6000+976+n*4+i for i in range(4)) and words[4:]==(0,0,0,0)
# Decode the real authored art: native floor strips at both ends and no duplicate
# narrow-flight edges at the internal module seam.
def indexed_cell(pixels,words):
 im=Image.new('P',(16,16),0)
 for i,w in enumerate(words[:4]):
  t=(w&1023)-512;im.paste(pixels.crop((t%16*8,t//16*8,t%16*8+8,t//16*8+8)),(i%2*8,i//2*8))
 return im
floor=indexed_cell(original,struct.unpack_from('<8H',native,16))
original_steps=indexed_cell(original,source)
for width,rows in [(32,[[0x3b1,0x3b2],[0x3b3,0x3b4]]),(48,[[0x3b1,0x3b5,0x3b2],[0x3b3,0x3b6,0x3b4]])]:
 im=Image.new('P',(width,32),0)
 for y,row in enumerate(rows):
  for x,mid in enumerate(row):im.paste(indexed_cell(cp,struct.unpack_from('<8H',authored,(mid-512)*16)),(x*16,y*16))
 for y in list(range(8))+list(range(25,32)):
  assert all(im.getpixel((x,y))==floor.getpixel((x%16,y%16)) for x in range(width)), 'Stair landing floor mismatch'
 assert all(im.getpixel((x,24))==5 for x in range(2,width-2)), 'Stair-foot shadow missing'
 for y in range(8,24):
  # Preserve the native tread's actual gradients. Only source interior pixels,
  # with the documented native-material tone map, may cross module seams.
  tone={1:2,2:3,7:6}
  allowed={tone.get(original_steps.getpixel((x,y-8)),original_steps.getpixel((x,y-8))) for x in range(2,14)}
  assert all(im.getpixel((x,y)) in allowed for x in range(2,width-2)), 'An outer stair edge intrudes into the tread'
# Original step footprints and actual native warp behavior are retained.
for key in ['Descent1','Descent2','Descent3','Descent4']:
 a=struct.unpack('<456H',(R/f'data/layouts/LegendsWyrmtide_{key}/map.bin').read_bytes())
 assert all((a[y*19+x]&1023)==mid for x,y,mid in [(7,1,0x30e),(8,1,0x3c8),(9,1,0x3c9),(10,1,0x2ff),(7,2,0x316),(8,2,0x3c5),(9,2,0x3c6),(10,2,0x307),(8,3,0x3c3),(9,3,0x3c4),(11,19,0x3b7),(11,20,0x3c7)])
# Widened upper return uses accepted treads, native wall canopy and two live lanes.
attrs=(sib/'metatile_attributes.bin').read_bytes()
words=lambda mid:struct.unpack_from('<8H',authored,(mid-512)*16)
for n,origin in enumerate([0x3b1,0x3b2,0x3b3,0x3b4]):
 mid=0x3c1+n
 assert words(mid)[:4]==words(origin)[:4]
 assert words(mid)[4:]==(words(0x2f9)[4:6]+(0,0) if n<2 else words(origin)[4:])
 assert struct.unpack_from('<H',attrs,(mid-512)*2)[0]==(0 if n<2 else 0x61)
for i in range(1,5):
 m=json.loads((R/f'data/maps/LegendsWyrmtide_Descent{i}/map.json').read_text());ws=m['warp_events']
 assert len(ws)==3 and (ws[0]['x'],ws[0]['y'])==(8,3) and ws[2]=={**ws[0],'x':9}
 a=struct.unpack('<456H',(R/f'data/layouts/LegendsWyrmtide_Descent{i}/map.bin').read_bytes())
 assert all(not a[y*19+x]&0xc00 for x in [8,9] for y in [2,3])
# Each cut closes both adjacent rock banks with the complete native cap pair.
# Solid middle-face cells at these positions leave an uncapped side gap.
stair_flights={'Descent1':[(12,9,2),(5,15,2)],'Descent2':[(5,9,2)],'Descent3':[(12,7,2),(5,13,2)],'Descent4':[(8,7,3),(8,13,3)]}
for key,flights in stair_flights.items():
 a=struct.unpack('<456H',(R/f'data/layouts/LegendsWyrmtide_{key}/map.bin').read_bytes())
 for x,y,width in flights:
  for xx,yy,mid in [(x-1,y,0x20a),(x-1,y+1,0x21a),(x+width,y,0x208),(x+width,y+1,0x218)]:
   v=a[yy*19+xx]
   assert base_mid(v&1023)==mid and v&0xc00 and v>>12==3,(key,x,y,'incomplete stair-bank return')
  assert [a[y*19+x+i]&1023 for i in range(width)]==([0x3b1,0x3b2] if width==2 else [0x3b1,0x3b5,0x3b2])
  assert [a[(y+1)*19+x+i]&1023 for i in range(width)]==([0x3b3,0x3b4] if width==2 else [0x3b3,0x3b6,0x3b4])
# Depth variants retain native geometry, behavior and loaded field banks.
assert depth['paletteBanks']==[7,8] and len(depth['variants'])==8
for variant in depth['variants']:
 mid,origin=variant['id'],variant['source']
 old=struct.unpack_from('<8H',authored,(origin-512)*16)
 new=struct.unpack_from('<8H',authored,(mid-512)*16)
 assert struct.unpack_from('<H',(sib/'metatile_attributes.bin').read_bytes(),(mid-512)*2)==struct.unpack_from('<H',(sib/'metatile_attributes.bin').read_bytes(),(origin-512)*2)
 if variant['role'] in ['upper-rim','vertical-face']:
  bank=7 if variant['role']=='upper-rim' else 8
  assert new==tuple((w&0xfff)|(bank<<12) if w else 0 for w in old)
 else:
  assert new[:4]==old[:4] and new[6:]==(0,0)
  assert all(w>>12==6 and 1008<=w&1023<=1011 for w in new[4:6])
# The protected Heart does not reference either private depth bank.
a=(R/'data/layouts/LegendsWyrmtide_Heart/map.bin').read_bytes()
for cell, in struct.iter_unpack('<H',a):
 mid=cell&1023
 if mid>=512:assert not {w[0]>>12 for w in struct.iter_unpack('<H',authored[(mid-512)*16:(mid-511)*16])}&{7,8}
# Keep original floor colors around the face so there is no square floor matte.
original_pal=[tuple(map(int,l.split())) for l in (base/'palettes/06.pal').read_text().splitlines()[3:19]]
face_pal=[tuple(map(int,l.split())) for l in (sib/'ledge_face.pal').read_text().splitlines()[3:19]]
rim_pal=[tuple(map(int,l.split())) for l in (sib/'ledge_rim.pal').read_text().splitlines()[3:19]]
assert face_pal[:6]==original_pal[:6] and rim_pal[4:]==original_pal[4:]
assert rim_pal[3]==original_pal[2] and face_pal[6]==(90,65,57) and face_pal[7]==(49,32,32)
# Outdoor imported objects have the same sand underlay as their surroundings.
sand=struct.unpack_from('<4H',(R/'data/tilesets/primary/general/metatiles.bin').read_bytes(),0x124*16)
for i in range(8):assert struct.unpack_from('<4H',shoremeta,len(dewmeta)+i*16)==sand
# Every stair landing is reachable on foot, and both directions retain exact pairs.
for key in ['Descent1','Descent2','Descent3','Descent4','Heart']:
 name='LegendsWyrmtide_'+key;m=json.loads((R/f'data/maps/{name}/map.json').read_text());l=next(x for x in layouts if x['id']==m['layout']);a=struct.unpack('<%dH'%(l['width']*l['height']),(R/l['blockdata_filepath']).read_bytes());w=l['width'];start=(8,3) if key!='Heart' else (11,17);goal=(11,20) if key!='Heart' else (11,8)
 q=collections.deque([start]);seen={start}
 while q:
  x,y=q.popleft()
  for xx,yy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
   if 0<=xx<w and 0<=yy<l['height'] and not a[yy*w+xx]&0xC00 and (xx,yy) not in seen:seen.add((xx,yy));q.append((xx,yy))
 assert goal in seen,(key,'unreachable descent')
 if key in ['Descent1','Descent3']:assert (13,19) in seen,(key,'return path cannot reach the depth inscription')
 for i,warp in enumerate(m['warp_events']):
  destkey=warp['dest_map'].removeprefix('MAP_LEGENDS_WYRMTIDE_');destname='LegendsWyrmtide_'+({'ISLE':'Isle','HEART':'Heart'}.get(destkey,destkey.title()))
  dest=json.loads((R/f'data/maps/{destname}/map.json').read_text());back=dest['warp_events'][int(warp['dest_warp_id'])];assert back['dest_map']==m['id'] and int(back['dest_warp_id'])==(0 if i==2 else i),(key,i)
# All outdoor clue approaches are reachable from Briney's landing without Surf.
l=next(x for x in layouts if x['name']=='LegendsWyrmtide_Isle_Layout');w=l['width'];raw=(R/l['blockdata_filepath']).read_bytes();cells=struct.unpack('<%dH'%(len(raw)//2),raw)
objects=json.loads((R/'data/maps/LegendsWyrmtide_Isle/map.json').read_text())['object_events'];blocked={(o['x'],o['y']) for o in objects};seen={(14,21)};q=collections.deque(seen)
while q:
 x,y=q.popleft()
 for xx,yy in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
  if not (0<=xx<w and 0<=yy<l['height']) or (xx,yy) in seen|blocked:continue
  v=cells[yy*w+xx]
  if v&0xC00 or v>>12!=3:continue
  seen.add((xx,yy));q.append((xx,yy))
assert {(10,18),(23,15),(19,21),(16,11)}<=seen,'An island clue or the seal is cut off'
script=(R/'data/scripts/legends_wyrmtide.inc').read_text();assert 'specialvar VAR_RESULT, LegendsWyrmtideHasMaker' in script
assert 'METATILE_General_CaveEntrance_Bottom, FALSE' in script and 'B_OUTCOME_CAUGHT, Wyrmtide_Caught' in script and 'B_OUTCOME_WON, Wyrmtide_Calmed' in script
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

# Owner-requested interior feedback: live cave tables and stable native art/IDs.
preserved_text_hashes={'Wyrmtide_Text_ShoreTablet': '611356c9395a9c16ed0fbe0d24eb9f2a140432fb9d1f6df5727beda6cb1a0564', 'Wyrmtide_Text_DepthTablet': 'aecc5d074b72e9cc1a2c5466bafe0ea571e3c4d405a431a1d25810cf4970ba59', 'Wyrmtide_Text_FinalTablet': '78e7c63709611cb56e9ccbeea5627f2dd1cd86393fdabef45b078a1ff3655877'}
story=(R/'data/scripts/legends_wyrmtide.inc').read_text()
for name,h in preserved_text_hashes.items():
 content=story.split(name+':',1)[1].split('\nWyrmtide_',1)[0]
 assert hashlib.sha256(content.encode()).hexdigest()==h,(name,'preserved first/final text changed')
labels=['Shore','Maker','Sea','Depth','Threshold','Tidal','Deep','Final']
texts=[story.split('Wyrmtide_Text_'+name+'Tablet:',1)[1].split('\nWyrmtide_',1)[0] for name in labels]
assert len(set(texts))==len(texts)
wild=json.loads((R/'src/data/wild_encounters.json').read_text());group=next(g for g in wild['wild_encounter_groups'] if g['for_maps']);rates=next(f['encounter_rates'] for f in group['fields'] if f['type']=='land_mons')
dragons=[['BAGON','GIBLE'],['NOIBAT','AXEW'],['DRUDDIGON','DEINO'],['GABITE','FRAXURE']]
for i,names in enumerate(dragons,1):
 entry=[e for e in group['encounters'] if e['map']==f'MAP_LEGENDS_WYRMTIDE_DESCENT{i}'];assert len(entry)==1
 info=entry[0]['land_mons'];assert info['encounter_rate']==8 and len(info['mons'])==12
 assert sum(rate for rate,mon in zip(rates,info['mons']) if mon['species'] in ['SPECIES_'+n for n in names])==5
 assert all(48<=m['min_level']<=m['max_level']<=61 for m in info['mons'])
assert not any(e['map']=='MAP_LEGENDS_WYRMTIDE_HEART' for e in group['encounters'])
assert struct.unpack_from('<H',attrs,(0x201-512)*2)[0]&0xff==8
assert words(0x3c7)[:2]==words(0x3b8)[:2] and words(0x3c7)[2:4]==words(0x206)[2:4] and struct.unpack_from('<H',attrs,(0x3c7-512)*2)[0]==0x65
info=(R/'src/data/object_events/object_event_graphics_info.h').read_text().split('gObjectEventGraphicsInfo_WyrmtideRegidrago = {',1)[1].split('};',1)[0]
assert '.width = 64' in info and '.height = 64' in info and '.size = 2048' in info
assert 'graphics/pokemon/regidrago/front.png' in (R/'src/data/object_events/object_event_graphics.h').read_text()
assert '#define OBJ_EVENT_GFX_LEGENDS_WYRMTIDE_REGIDRAGO 0x0E00' in (R/'include/constants/event_objects.h').read_text()
print('PASS unique readable carvings, protected first/final text, 5% dragons, quiet Heart and dedicated 64px native legendary')

# Lower-exit correction: whole native rock silhouettes and bases, stable physics.
assert words(0x3ca)==words(0x202) and words(0x3cb)==words(0x202), "Exit rocks must retain every native quadrant, silhouette and base"
for i in range(1,5):
 cells=struct.unpack('<456H',(R/f'data/layouts/LegendsWyrmtide_Descent{i}/map.bin').read_bytes())
 for x,mid in [(10,0x3ca),(12,0x3cb)]:assert cells[20*19+x]&0xfc00==0x3400 and cells[20*19+x]&1023==mid
print('PASS complete native exit rocks and stable south-arrow collision/behavior')
