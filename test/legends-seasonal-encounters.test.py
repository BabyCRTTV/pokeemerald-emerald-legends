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
water_weights=next(f['encounter_rates'] for f in g['fields'] if f['type']=='water_mons');assert water_weights==[60,30,5,4,1]
water_native={int(x['map'][-3:]):x['water_mons'] for x in g['encounters'] if x['map'] in [f'MAP_ROUTE{i}' for i in range(105,109)]}
water_tables=re.findall(r'static const struct WildPokemon sRoute(10[5-8])(Spring|Summer|Autumn|Winter)WaterMons.*?=\s*\{(.*?)\};',data,re.S);assert len(water_tables)==16
water_visitors=set()
for route,season,body in water_tables:
 route=int(route);rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body);assert len(rows)==5
 assert [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in water_native[route]['mons']]
 residents={m['species'] for m in water_native[route]['mons']};odds={}
 for (_,_,species),weight in zip(rows,water_weights):odds[species]=odds.get(species,0)+weight
 assert residents<=odds.keys() and sum(odds[x] for x in residents)==65
 visitors=set(odds)-residents;assert len(visitors)==2 and sorted(odds[x] for x in visitors)==[5,30]
 assert 'SPECIES_DA_BUG' not in visitors;water_visitors|=visitors
assert len(water_visitors)==32
# Next numbered routes keep the same exact native slots/rates and all residents.
extra_visitors=set()
for route in range(109,113):
 method='water_mons' if route==109 else 'land_mons';suffix='Water' if route==109 else '';ww=water_weights if route==109 else weights
 original=next(e[method] for e in g['encounters'] if e['map']==f'MAP_ROUTE{route}')
 for season in ['Spring','Summer','Autumn','Winter']:
  body=re.search(rf'sRoute{route}{season}{suffix}Mons.*?=\s*\{{(.*?)\}};',data,re.S)[1]
  rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body);assert len(rows)==len(ww)
  assert [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in original['mons']]
  residents={m['species'] for m in original['mons']};odds={}
  for (_,_,species),weight in zip(rows,ww):odds[species]=odds.get(species,0)+weight
  visitors=set(odds)-residents
  assert residents<=odds.keys() and sum(odds[x] for x in residents)==(65 if route==109 else 70)
  assert len(visitors)==2 and sorted(odds[x] for x in visitors)==([5,30] if route==109 else [10,20])
  assert 'SPECIES_DA_BUG' not in visitors;extra_visitors|=visitors
assert len(extra_visitors)==32
# Next numbered routes keep the same exact native slots/rates and all residents.
next_visitors=set()
for route in range(113,117):
 method='water_mons' if route==109 else 'land_mons';suffix='Water' if route==109 else '';ww=water_weights if route==109 else weights
 original=next(e[method] for e in g['encounters'] if e['map']==f'MAP_ROUTE{route}')
 for season in ['Spring','Summer','Autumn','Winter']:
  body=re.search(rf'sRoute{route}{season}{suffix}Mons.*?=\s*\{{(.*?)\}};',data,re.S)[1]
  rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body);assert len(rows)==len(ww)
  assert [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in original['mons']]
  residents={m['species'] for m in original['mons']};odds={}
  for (_,_,species),weight in zip(rows,ww):odds[species]=odds.get(species,0)+weight
  visitors=set(odds)-residents
  assert residents<=odds.keys() and sum(odds[x] for x in residents)==(65 if route==109 else 70)
  assert len(visitors)==2 and sorted(odds[x] for x in visitors)==([5,30] if route==109 else [10,20])
  assert 'SPECIES_DA_BUG' not in visitors;next_visitors|=visitors
assert len(next_visitors)==32
# Five-route batch: every original resident remains, with exact native levels/rates.
latest_visitors=set()
for route in range(117,122):
 original=next(e['land_mons'] for e in g['encounters'] if e['map']==f'MAP_ROUTE{route}')
 assert original['encounter_rate']==(15 if route==119 else 20)
 residents={m['species'] for m in original['mons']}
 for season in ['Spring','Summer','Autumn','Winter']:
  body=re.search(rf'sRoute{route}{season}Mons.*?=\s*\{{(.*?)\}};',data,re.S)[1]
  rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body);assert len(rows)==12
  assert [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in original['mons']]
  odds={}
  for (_,_,species),weight in zip(rows,weights):odds[species]=odds.get(species,0)+weight
  visitors=set(odds)-residents
  assert residents<=odds.keys() and sum(odds[x] for x in residents)==70
  assert len(visitors)==2 and sorted(odds[x] for x in visitors)==[10,20]
  assert not (visitors & (all_visitors|water_visitors|extra_visitors|next_visitors))
  assert 'SPECIES_DA_BUG' not in visitors;latest_visitors|=visitors
assert len(latest_visitors)==40
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
#define MAP_ROUTE105 105
#define MAP_ROUTE106 106
#define MAP_ROUTE107 107
#define MAP_ROUTE108 108
#define MAP_ROUTE109 109
#define MAP_ROUTE110 110
#define MAP_ROUTE111 111
#define MAP_ROUTE112 112
#define MAP_ROUTE113 113
#define MAP_ROUTE114 114
#define MAP_ROUTE115 115
#define MAP_ROUTE116 116
#define MAP_ROUTE117 117
#define MAP_ROUTE118 118
#define MAP_ROUTE119 119
#define MAP_ROUTE120 120
#define MAP_ROUTE121 121
#define NUM_LAND_MONS_ENCOUNTER_SLOTS 12
#define NUM_WATER_MONS_ENCOUNTER_SLOTS 5
#define HEADER_NONE 65535
enum TimeOfDay {MORNING,DAY,EVENING,NIGHT,TIMES_OF_DAY_COUNT};
enum {LEGENDS_SPRING,LEGENDS_SUMMER,LEGENDS_AUTUMN,LEGENDS_WINTER,LEGENDS_SEASON_COUNT};
struct WildPokemon {u8 minLevel,maxLevel;enum Species species;};
struct WildPokemonInfo {u8 encounterRate;const struct WildPokemon *wildPokemon;};
struct WildEncounterTypes {const struct WildPokemonInfo *landMonsInfo,*waterMonsInfo,*hiddenMonsInfo;};
struct WildPokemonHeader {u8 mapGroup,mapNum;struct WildEncounterTypes encounterTypes[TIMES_OF_DAY_COUNT];};
static struct WildPokemonInfo fallback[4],waterFallback[4];
static struct WildPokemonHeader gWildMonHeaders[23];
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
 for(unsigned h=0;h<22;h++){gWildMonHeaders[h].mapNum=101+h;for(unsigned t=0;t<4;t++){gWildMonHeaders[h].encounterTypes[t].landMonsInfo=&fallback[t];gWildMonHeaders[h].encounterTypes[t].waterMonsInfo=&waterFallback[t];}}
 for(unsigned season=0;season<4;season++)for(unsigned t=0;t<4;t++){
  active=season;pending=(season+1)%4;
  for(unsigned h=0;h<22;h++){
   currentHeader=h;
   for(unsigned area=0;area<2;area++){
    const struct WildPokemonInfo *expected=area?&waterFallback[t]:&fallback[t],*previous=NULL;
    unsigned rate=0,slots=area?5:12;
    if(area){for(unsigned i=0;i<ARRAY_COUNT(sLegendsSeasonalWater);i++)if(sLegendsSeasonalWater[i].map==101+h){expected=&sLegendsSeasonalWater[i].seasons[season];previous=&sLegendsSeasonalWater[i].seasons[(season+3)%4];rate=4;}}
    else {for(unsigned i=0;i<ARRAY_COUNT(sLegendsSeasonalLand);i++)if(sLegendsSeasonalLand[i].map==101+h){expected=&sLegendsSeasonalLand[i].seasons[season];previous=&sLegendsSeasonalLand[i].seasons[(season+3)%4];rate=(h==10?10:h==18?15:20);}}
    unsigned before=reads;const struct WildPokemonInfo *p=area?GetWaterMonsInfo(h,t):GetLandMonsInfo(h,t);
    assert(p==expected);assert(active==season&&pending==(season+1)%4);
    if(!previous){assert(reads==before);continue;}assert(p->encounterRate==rate);
    unsigned absent=0;
    for(unsigned i=0;i<slots;i++){
     assert(GetEncounterLevelFromMapData(p->wildPokemon[i].species,area?ENCOUNTER_TYPE_WATER:ENCOUNTER_TYPE_LAND)!=255);
     enum Species species=previous->wildPokemon[i].species;unsigned present=0;
     for(unsigned j=0;j<slots;j++)if(p->wildPokemon[j].species==species)present=1;
     if(!present){assert(GetEncounterLevelFromMapData(species,area?ENCOUNTER_TYPE_WATER:ENCOUNTER_TYPE_LAND)==255);absent++;}
    }assert(absent);
   }
  }
 }
 assert(!GetLandMonsInfo(HEADER_NONE,0)&&!GetLandMonsInfo(22,0)&&!GetLandMonsInfo(0,4)&&!GetLandMonsInfo(0,(enum TimeOfDay)-1));
 assert(!GetWaterMonsInfo(HEADER_NONE,0)&&!GetWaterMonsInfo(22,0)&&!GetWaterMonsInfo(0,4)&&!GetWaterMonsInfo(0,(enum TimeOfDay)-1));
 active=255;for(unsigned h=0;h<22;h++){assert(GetLandMonsInfo(h,0)==&fallback[0]);assert(GetWaterMonsInfo(h,0)==&waterFallback[0]);}
 currentHeader=HEADER_NONE;assert(GetEncounterLevelFromMapData(SPECIES_WURMPLE,ENCOUNTER_TYPE_LAND)==255);
 puts("PASS: all 84 seasonal tables, exact rates including desert, all TODs, committed vs pending, unrelated map/method parity, bounds/fallback and absent prior-season DexNav targets");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(pre+data+function+level_function+main)
 subprocess.run(['cc','-std=gnu17','-Wall','-Werror','-I'+str(R/'include'),str(p),'-o',d+'/test'],check=True);subprocess.run([d+'/test'],check=True)
for f in ['dexnav.c','wild_encounter_ow.c','match_call.c']:
 text=(R/'src'/f).read_text();assert not re.search(r'gWildMonHeaders\[[^\]]+\]\.encounterTypes\[[^\]]+\]\.landMonsInfo',text),f
 assert 'GetLandMonsInfo(' in text and 'GetWaterMonsInfo(' in text
 assert not re.search(r'gWildMonHeaders\[[^\]]+\]\.encounterTypes\[[^\]]+\]\.waterMonsInfo',text),f
assert s.count('gWildMonHeaders[headerId].encounterTypes[timeOfDay].landMonsInfo')==1 # getter fallback only
assert 'encounters.landMonsInfo = GetLandMonsInfo(i, gAreaTimeOfDay);' in (R/'src/pokedex_area_screen.c').read_text()
assert s.count('gWildMonHeaders[headerId].encounterTypes[timeOfDay].waterMonsInfo')==1
assert 'encounters.waterMonsInfo = GetWaterMonsInfo(i, gAreaTimeOfDay);' in (R/'src/pokedex_area_screen.c').read_text()
assert 'LegendsGetSeason()' not in function and 'VarSet(' not in function
print('PASS: original residents/levels/rates, 70/20/10 base distribution, 168 visitor selections, native 65/30/5 Surf odds and all dependent land/Surf readers')
