"""Nightmare progression, production call hook, stable IDs and native assemblies."""
from pathlib import Path
import re,json,struct,hashlib,subprocess,tempfile
R=Path(__file__).resolve().parents[1];BASE='2b99c6555954d6284a8d4ebee488e349a8e05a61'
def old(path):return subprocess.check_output(['git','show',BASE+':'+path],cwd=R)
def read(path):return (R/path).read_text()
# Resolve both Hoenn and FRLG flag aliases, not just unused-looking labels.
defs=dict(re.findall(r'^#define\s+(\w+)\s+([^\n/]+)',read('include/constants/opponents.h')+'\n'+read('include/constants/flags.h'),re.M))
def value(k,seen=()):
 if k in seen:raise ValueError(k)
 s=re.sub(r'\b[A-Z_]\w*\b',lambda m:str(value(m[0],seen+(k,))),defs[k].strip())
 if not re.fullmatch(r'[\dxa-fA-F\s()+*<>&|~\-]+',s):raise ValueError(k)
 return eval(s,{'__builtins__':{}})
names=['CALL','VISITED','WING','ENTERED','VOICE','RESOLVED','CAUGHT','REPORTED']
for n,name in enumerate(names,0x49a):
 aliases=set()
 for k in defs:
  try:
   if value(k)==n:aliases.add(k)
  except Exception:pass
 assert aliases=={'FLAG_LEGENDS_NIGHTMARE_'+name,f'FLAG_UNUSED_0x{n:X}'},aliases
assert 0x4a1<0x500
# All published map/layout/quest identifiers retain their old positions.
groups=json.loads(read('data/maps/map_groups.json'));previous=json.loads(old('data/maps/map_groups.json'))
for group,maps in previous.items():
 if isinstance(maps,list):assert groups[group][:len(maps)]==maps,group
layouts=json.loads(read('data/layouts/layouts.json'))['layouts'];previous_layouts=json.loads(old('data/layouts/layouts.json'))['layouts'];assert layouts[:len(previous_layouts)]==previous_layouts
oldquests=old('src/data/legends/journal.h').decode().split('static const struct LegendsAchievement')[0];quests=read('src/data/legends/journal.h').split('static const struct LegendsAchievement')[0]
titles=lambda s:re.findall(r'\{COMPOUND_STRING\("([^"]+)"\)',s)
assert titles(quests)[:len(titles(oldquests))]==titles(oldquests)
assert 'When Morning Never Comes' in quests and 'FLAG_LEGENDS_NIGHTMARE_REPORTED' in quests
# New item875 fits exactly the prior110-byte bitmap, preserving every following
# SaveBlock3 offset. Existing items and saved structs remain byte-for-byte.
items=read('include/constants/items.h');assert 'ITEM_LUNAR_WING = 875' in items
assert (875+7)//8==(876+7)//8==110
# Permit the two explicitly migrated extensions and compare the remaining native definitions.
current_global=read('include/global.h');old_global=old('include/global.h').decode()
record=r'struct Pokeblock\n\{.*?\n\};'
assert re.search(record,current_global,re.S)[0]==re.search(record,old_global,re.S)[0]
current_global=re.sub(record,'',current_global,flags=re.S)
old_global=re.sub(record,'',old_global,flags=re.S)
current_global=re.sub(r'#define LEGENDS_POFFIN_CAPACITY 40\n\nstruct LegendsPoffinSave\n\{.*?\n\};','',current_global,flags=re.S)
current_global=current_global.replace('    struct LegendsPoffinSave poffins;\n','')
assert 'u16 pocketSizes[POCKETS_COUNT];' in current_global
assert 'struct ItemSlot slots[LEGENDS_BAG_SLOTS];' in current_global
old_bag=re.search(r'struct Bag\n\{.*?\n\};',old_global,re.S)[0]
current_global=re.sub(r'struct Bag\n\{.*?\n\};',lambda _:old_bag,current_global,count=1,flags=re.S)
current_global=current_global.replace('#include "constants/item.h"\n','')
assert [l for l in current_global.splitlines() if l.strip()]==[l for l in old_global.splitlines() if l.strip()]
assert items[:items.index('    ITEM_INVITE_TICKET = 874,')]==old('include/constants/items.h').decode().split('    ITEM_INVITE_TICKET = 874,')[0]
# Bound the only old-map terrain patch to a complete house; retain old objects,
# coordinates, event scripts and warp IDs, including original Lilycove stories.
source=json.loads(read('data/tilesets/legends_nightmare/source.json'))
raw=bytearray((R/'data/layouts/LilycoveCity/map.bin').read_bytes())
for at,n in source['exteriorBefore'].items():struct.pack_into('<H',raw,int(at)*2,n)
assert raw==old('data/layouts/LilycoveCity/map.bin')
lily=json.loads(read('data/maps/LilycoveCity/map.json'));before=json.loads(old('data/maps/LilycoveCity/map.json'))
assert lily['object_events']==before['object_events'];assert lily['coord_events']==before['coord_events'];assert lily['bg_events']==before['bg_events'];assert lily['warp_events'][:-1]==before['warp_events']
assert lily['warp_events'][-1]['dest_map']=='MAP_LEGENDS_NIGHTMARE_HOME'
# Native coastline and approved cave artwork are never regenerated.
assert (R/'data/layouts/LegendsNightmare_Shore/map.bin').read_bytes()==(R/'data/layouts/SouthernIsland_Exterior/map.bin').read_bytes()
paths=subprocess.check_output(['git','ls-tree','-r','--name-only',BASE,'--','data/layouts','data/tilesets','graphics'],cwd=R,text=True).splitlines()
for path in paths:
 if '/LegendsWyrmtide_' in path or '/legends_wyrmtide/' in path or '/legends_wyrmtide_shore/' in path:
  assert (R/path).read_bytes().replace(b'\r\n',b'\n')==old(path).replace(b'\r\n',b'\n'),path
for key in ['Home','Bedroom','Street','Shore']:
 m=json.loads(read(f'data/maps/LegendsNightmare_{key}/map.json'));layout=next(x for x in layouts if x['id']==m['layout']);a=struct.unpack('<%dH'%((R/layout['blockdata_filepath']).stat().st_size//2),(R/layout['blockdata_filepath']).read_bytes());assert len(a)==layout['width']*layout['height']
 for w in m['warp_events']:
  assert 0<=w['x']<layout['width'] and 0<=w['y']<layout['height'];assert key=='Street' or not (a[w['y']*layout['width']+w['x']]&0xc00),(key,w)
# Native furniture-only bed silhouette in both rooms, with clear feet/side approaches.
# The previous two-cell assembly mistakenly selected floor/left-edge pieces.
for room in ['Home','Bedroom']:
 cells=struct.unpack('<120H',(R/f'data/layouts/LegendsNightmare_{room}/map.bin').read_bytes())
 assert [[cells[(y+3)*12+x+7]&0x3ff for x in range(3)] for y in range(2)]==[
  [0x2d2,0x2d3,0x2d4],[0x2da,0x2db,0x2dc]]
 assert all(cells[2*12+x]==0x3224 for x in range(4,12)) # Continue the existing top-row shadow across the gap above the bed.
 assert cells[3*12+8]>>12==4 # Head remains above the native opaque bedding layer.
 for x,y in [(8,5),(9,4),(7,5)]:assert not cells[y*12+x]&0xc00
 m=json.loads(read(f'data/maps/LegendsNightmare_{room}/map.json'))
 assert any(e['x']==8 and e['y']==4 and e['script'].endswith('Bed') for e in m['bg_events'])
 assert any(e['x']==6 and e['y']==3 and e['script'].endswith('Chair') for e in m['bg_events'])
# Repair only the two bedside floor backgrounds; all other metatiles, floor
# pattern, palettes, furniture and the complete upper layer remain native.
from PIL import Image
room=R/'data/tilesets/legends_nightmare/room';native=R/'data/tilesets/secondary/generic_building'
metas=(room/'metatiles.bin').read_bytes();base=(native/'metatiles.bin').read_bytes()
assert (room/'metatile_attributes.bin').read_bytes()==(native/'metatile_attributes.bin').read_bytes()
assert [i+512 for i in range(len(base)//16) if metas[i*16:(i+1)*16]!=base[i*16:(i+1)*16]]==[0x2d2,0x2d4]
for i in range(len(base)//16):assert metas[i*16+8:i*16+16]==base[i*16+8:i*16+16]
original=Image.open(native/'tiles.png');modified=Image.open(room/'tiles.png')
def tile_pixels(image, word):
 n=(word&1023)-512
 return [image.getpixel((n%16*8+(7-x if word&1024 else x),n//16*8+(7-y if word&2048 else y)))%16 for y in range(8) for x in range(8)]
floor=struct.unpack_from('<4H',base,(0x223-512)*16)
for metatile in [0x2d2,0x2d4]:
 for k in range(4):
  at=(metatile-512)*16+k*2
  old=struct.unpack_from('<H',base,at)[0];new=struct.unpack_from('<H',metas,at)[0]
  assert old&0xfc00==new&0xfc00 # Original palette, orientation and frame geometry.
  before=tile_pixels(original,old);after=tile_pixels(modified,new);background=tile_pixels(original,floor[k])
  for y in range(8):
   for x in range(8):
    is_floor=old&1023==0x240 or old&1023==0x3c2 and x<5 or old&1023==0x3c5 and x>=3
    assert after[y*8+x]==(background if is_floor else before)[y*8+x]
assert 'gTilesetPalettes_GenericBuilding' in read('src/data/tilesets/legends_nightmare_room.h')
assert not (room/'12.pal').exists()
# Original caretaker grant follows the added helper; wing progress follows only
# successful item receipt. Battle outcomes remain distinct, with a retry path.
scripts=read('data/scripts/legends_nightmare.inc');caretaker=read('data/maps/MtPyre_1F/scripts.inc')
assert '\tcall Nightmare_Keeper\n\tgoto_if_set FLAG_RECEIVED_CLEANSE_TAG' in caretaker
assert '\tgiveitem ITEM_LUNAR_WING\n\tgoto_if_eq VAR_RESULT, FALSE, Nightmare_WingBagFull' in scripts
assert 'B_OUTCOME_CAUGHT, Nightmare_Caught' in scripts and 'B_OUTCOME_WON, Nightmare_Resolved' in scripts
assert 'Nightmare_WingBagFull::\n\tmsgbox' in scripts
assert 'setflag FLAG_LEGENDS_NIGHTMARE_CAUGHT' not in scripts.split('Nightmare_Resolved::')[1].split('Nightmare_Wake::')[0]
# Execute the real production C, with only field-engine boundaries stubbed.
source='\n'.join(s for s in read('src/legends_nightmare.c').splitlines() if not s.startswith('#include'))
preamble='''#include <assert.h>
#include <stdint.h>
typedef unsigned int u32;typedef uint8_t u8;typedef int bool32;
#define TRUE 1
#define FALSE 0
#define EWRAM_DATA
#define IS_FRLG 0
#define PLAYER_AVATAR_FLAG_FORCED_MOVE 64
#define LAYOUT_LEGENDS_NIGHTMARE_SHORE 777
#define OBJECT_EVENTS_COUNT 16
#define MAP_LILYCOVE_CITY 5
#define MAP_GROUP(m) ((m)>>8)
#define MAP_NUM(m) ((m)&255)
struct Coords16 {short x,y;};
struct ObjectEvent {unsigned isPlayer; struct Coords16 initialCoords,currentCoords,previousCoords; unsigned currentElevation,previousElevation;};
static struct {struct {int mapGroup,mapNum;} location;struct Coords16 pos;struct ObjectEvent objectEvents[16];} saved,*gSaveBlock1Ptr=&saved;
struct {int mapType,mapLayoutId;} gMapHeader;
struct {unsigned flags;} gPlayerAvatar;
static unsigned bits[4096],scheduled;
int FlagGet(unsigned f){return bits[f];}
void ScriptContext_SetupScript(const u8 *s){scheduled++;}
const u8 Nightmare_UnknownCall[]={0};
'''+read('include/constants/map_types.h')+'\n'
for key in ['FLAG_LEGENDS_NIGHTMARE_CALL','FLAG_LEGENDS_WYRMTIDE_CALMED','FLAG_RECEIVED_POKENAV','FLAG_SYS_SAFARI_MODE']:
 preamble+=f'#define {key} {value(key)}\n'
main='''
static void reset(void){for(int i=0;i<4096;i++)bits[i]=0;scheduled=0;gMapHeader.mapType=MAP_TYPE_CITY;gPlayerAvatar.flags=0;LegendsNightmareTryCall();}
int main(void){
 reset();bits[FLAG_RECEIVED_POKENAV]=1;for(int i=0;i<20;i++)assert(!LegendsNightmareTryCall());
 bits[FLAG_LEGENDS_WYRMTIDE_CALMED]=1;for(int i=0;i<7;i++)assert(!LegendsNightmareTryCall());assert(LegendsNightmareTryCall()&&scheduled==1);
 bits[FLAG_LEGENDS_NIGHTMARE_CALL]=1;for(int i=0;i<20;i++)assert(!LegendsNightmareTryCall());assert(scheduled==1);
 reset();bits[FLAG_RECEIVED_POKENAV]=bits[FLAG_LEGENDS_WYRMTIDE_CALMED]=1;
 for(int i=0;i<7;i++)assert(!LegendsNightmareTryCall());bits[FLAG_SYS_SAFARI_MODE]=1;assert(!LegendsNightmareTryCall());bits[FLAG_SYS_SAFARI_MODE]=0;
 for(int i=0;i<7;i++)assert(!LegendsNightmareTryCall());assert(LegendsNightmareTryCall());
 gMapHeader.mapType=MAP_TYPE_INDOOR;for(int i=0;i<20;i++)assert(!LegendsNightmareTryCall());
 gMapHeader.mapType=MAP_TYPE_ROUTE;gPlayerAvatar.flags=64;for(int i=0;i<20;i++)assert(!LegendsNightmareTryCall());gPlayerAvatar.flags=0;
 for(int i=0;i<7;i++)assert(!LegendsNightmareTryCall());assert(LegendsNightmareTryCall());
 // Only the new solid footprint is repaired; every outside point and
 // every non-player actor remains unchanged, including repeated Continue.
 for(int x=47;x<=54;x++)for(int y=11;y<=17;y++){
  saved.location.mapGroup=0;saved.location.mapNum=5;saved.pos.x=x;saved.pos.y=y;
  saved.objectEvents[0].isPlayer=1;saved.objectEvents[1].isPlayer=0;
  saved.objectEvents[1].currentCoords.x=123;saved.objectEvents[1].currentCoords.y=45;
  LegendsNightmareRepairLegacyPosition();
  int inside=x>=49&&x<=52&&y>=13&&y<=15;
  assert(saved.pos.x==(inside?50:x)&&saved.pos.y==(inside?16:y));
  if(inside)assert(saved.objectEvents[0].currentCoords.x==57&&saved.objectEvents[0].currentCoords.y==23);
  assert(saved.objectEvents[1].currentCoords.x==123&&saved.objectEvents[1].currentCoords.y==45);
  LegendsNightmareRepairLegacyPosition();assert(saved.pos.x==(inside?50:x)&&saved.pos.y==(inside?16:y));
 }
 saved.location.mapNum=6;saved.pos.x=50;saved.pos.y=14;LegendsNightmareRepairLegacyPosition();assert(saved.pos.y==14);
 gMapHeader.mapLayoutId=776;assert(!LegendsNightmareIsShore());gMapHeader.mapLayoutId=777;assert(LegendsNightmareIsShore());return 0;
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'test.c').write_text(preamble+source+main);subprocess.run(['cc','-std=c11','-Wall','-Werror','-Wno-misleading-indentation',str(p/'test.c'),'-o',str(p/'test')],check=True);subprocess.run([str(p/'test')],check=True)
print('PASS Nightmare native flag allocation, stable IDs/save width, bounded house, complete native coast/cave preservation, reward/outcome paths and production-C call rules')
