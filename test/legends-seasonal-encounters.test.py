"""Exercise shipped seasonal resolver/data, native odds and dependent consumers."""
from pathlib import Path
import re,json,subprocess,tempfile
R=Path(__file__).resolve().parents[1]
s=(R/'src/wild_encounter.c').read_text();a=s.index('const struct WildPokemonInfo *GetLandMonsInfo(');b=s.index('\nenum TimeOfDay GetTimeOfDayForEncounters(',a);function=s[a:b]
data=(R/'src/data/legends_seasonal_encounters.h').read_text()
dexnav=(R/'src/dexnav.c').read_text();a=dexnav.index('static u8 GetEncounterLevelFromMapData(enum Species species, enum EncounterType environment)\n{');b=dexnav.index('\n///////////',a);level_function=dexnav[a:b]
g=json.loads((R/'src/data/wild_encounters.json').read_text())['wild_encounter_groups'][0]
weights=next(f['encounter_rates'] for f in g['fields'] if f['type']=='land_mons');assert sum(weights)==100
native={int(x['map'][-3:]):x['land_mons'] for x in g['encounters'] if x['map'] in [f'MAP_ROUTE{i}' for i in range(101,105)]}
tables=re.findall(r'static const struct WildPokemon sRoute(10[1-4])(Spring|Summer|Autumn|Winter)Mons.*?=\s*\{(.*?)\};',data,re.S);assert len(tables)==16
all_visitors=set()
for route,season,body in tables:
 route=int(route);rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body);assert len(rows)==12
 assert [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in native[route]['mons']]
 residents={m['species'] for m in native[route]['mons']};odds={}
 for (_,_,species),weight in zip(rows,weights):odds[species]=odds.get(species,0)+weight
 assert residents<=odds.keys(),(route,season,'lost resident')
 assert sum(odds[x] for x in residents)==70,(route,season,odds)
 visitors=set(odds)-residents;assert len(visitors)==2 and sorted(odds[x] for x in visitors)==[10,20]
 assert 'SPECIES_DA_BUG' not in visitors;all_visitors|=visitors
assert len(all_visitors)==32
pre=r'''
#include <stdint.h>
#include <stddef.h>
#include <assert.h>
#include <stdio.h>
#include "constants/species.h"
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define MAP_GROUP(x) ((x)>>8)
#define MAP_NUM(x) ((x)&255)
#define MAP_ROUTE101 101
#define MAP_ROUTE102 102
#define MAP_ROUTE103 103
#define MAP_ROUTE104 104
#define NUM_LAND_MONS_ENCOUNTER_SLOTS 12
#define HEADER_NONE 65535
enum TimeOfDay {MORNING,DAY,EVENING,NIGHT,TIMES_OF_DAY_COUNT};
enum {LEGENDS_SPRING,LEGENDS_SUMMER,LEGENDS_AUTUMN,LEGENDS_WINTER,LEGENDS_SEASON_COUNT};
struct WildPokemon {u8 minLevel,maxLevel;enum Species species;};
struct WildPokemonInfo {u8 encounterRate;const struct WildPokemon *wildPokemon;};
struct WildEncounterTypes {const struct WildPokemonInfo *landMonsInfo,*waterMonsInfo,*hiddenMonsInfo;};
struct WildPokemonHeader {u8 mapGroup,mapNum;struct WildEncounterTypes encounterTypes[TIMES_OF_DAY_COUNT];};
static struct WildPokemonInfo fallback[4];
static struct WildPokemonHeader gWildMonHeaders[6];
static unsigned active,reads,pending,currentHeader;
#define MAX_LEVEL 100
#define MON_LEVEL_NONEXISTENT 255
#define NUM_WATER_MONS_ENCOUNTER_SLOTS 5
#define NUM_HIDDEN_MONS_ENCOUNTER_SLOTS 3
#define WILD_AREA_LAND 0
#define WILD_AREA_WATER 1
#define WILD_AREA_HIDDEN 2
#define RNG_DEXNAV_ENCOUNTER_LEVEL 0
enum EncounterType {ENCOUNTER_TYPE_LAND,ENCOUNTER_TYPE_WATER,ENCOUNTER_TYPE_HIDDEN};
static struct {enum EncounterType environment;}searchData,*sDexNavSearchDataPtr=&searchData;
u32 GetCurrentMapWildMonHeaderId(void){return currentHeader;}
enum TimeOfDay GetTimeOfDayForEncounters(u32 h,unsigned area){return MORNING;}
u8 RandomUniform(unsigned rng,u8 min,u8 max){return min;}
u8 LegendsGetActiveSeason(void){reads++;return active;}
'''
main=r'''
int main(void){
 for(unsigned h=0;h<5;h++){gWildMonHeaders[h].mapNum=101+h;for(unsigned t=0;t<4;t++)gWildMonHeaders[h].encounterTypes[t].landMonsInfo=&fallback[t];}
 for(unsigned season=0;season<4;season++)for(unsigned h=0;h<4;h++)for(unsigned t=0;t<4;t++){
  active=season;pending=(season+1)%4;const struct WildPokemonInfo *p=GetLandMonsInfo(h,t);
  assert(p==&sLegendsSeasonalLand[h].seasons[season]&&p->encounterRate==20);
  assert(active==season&&pending==(season+1)%4);
  currentHeader=h;
  for(unsigned i=0;i<12;i++)assert(GetEncounterLevelFromMapData(p->wildPokemon[i].species,ENCOUNTER_TYPE_LAND)!=255);
  const struct WildPokemonInfo *previous=&sLegendsSeasonalLand[h].seasons[(season+3)%4];unsigned absent=0;
  for(unsigned i=0;i<12;i++){
   enum Species species=previous->wildPokemon[i].species;unsigned present=0;
   for(unsigned j=0;j<12;j++)if(p->wildPokemon[j].species==species)present=1;
   if(!present){assert(GetEncounterLevelFromMapData(species,ENCOUNTER_TYPE_LAND)==255);absent++;}
  }
  assert(absent);

 }
 unsigned n=reads;for(unsigned t=0;t<4;t++)assert(GetLandMonsInfo(4,t)==&fallback[t]);assert(reads==n);
 assert(!GetLandMonsInfo(HEADER_NONE,0)&&!GetLandMonsInfo(5,0)&&!GetLandMonsInfo(0,4));
 active=255;assert(GetLandMonsInfo(0,0)==&fallback[0]);
 currentHeader=HEADER_NONE;assert(GetEncounterLevelFromMapData(SPECIES_WURMPLE,ENCOUNTER_TYPE_LAND)==255);
 puts("PASS: 16 seasonal tables, all TODs, committed vs pending, unrelated-map pointer parity, invalid bounds/fallback, absent prior-season DexNav targets");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(pre+data+function+level_function+main)
 subprocess.run(['cc','-std=gnu17','-Wall','-Werror','-I'+str(R/'include'),str(p),'-o',d+'/test'],check=True);subprocess.run([d+'/test'],check=True)
for f in ['dexnav.c','wild_encounter_ow.c','match_call.c']:
 text=(R/'src'/f).read_text();assert not re.search(r'gWildMonHeaders\[[^\]]+\]\.encounterTypes\[[^\]]+\]\.landMonsInfo',text),f
 assert 'GetLandMonsInfo(' in text
assert s.count('gWildMonHeaders[headerId].encounterTypes[timeOfDay].landMonsInfo')==1 # getter fallback only
assert 'encounters.landMonsInfo = GetLandMonsInfo(i, gAreaTimeOfDay);' in (R/'src/pokedex_area_screen.c').read_text()
assert 'LegendsGetSeason()' not in function and 'VarSet(' not in function
print('PASS: original residents/levels/rates, 70/20/10 base distribution, 32 visitors and all dependent land readers')
