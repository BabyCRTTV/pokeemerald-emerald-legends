"""Exercise shipped seasonal resolver/data, native odds and dependent consumers."""
from pathlib import Path
import re,json,subprocess,tempfile
R=Path(__file__).resolve().parents[1]
s=(R/'src/wild_encounter.c').read_text();a=s.index('static const struct WildPokemonInfo *GetSeasonalMonsInfo(');b=s.index('\nenum TimeOfDay GetTimeOfDayForEncounters(',a);function=s[a:b]
a=s.index('static u8 GetMaxLevelOfSpeciesInWildTable(',s.index('#include "data.h"'));b=s.index('\n#ifdef BUGFIX',a);max_level_function=s[a:b]
wild_header=(R/'include/wild_encounter.h').read_text();a=wild_header.index('enum WildPokemonArea {');b=wild_header.index('};',a)+2;wild_area=wild_header[a:b]
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
# Routes 122–126 append one grass and four Surf methods without revising old arrays.
receipt=json.loads((R/'docs/qa/seasonal-routes-v0.0.72-source.json').read_text())
import hashlib
for match in re.finditer(r'static const struct WildPokemon (sRoute\w+Mons)\[.*?=\s*\{.*?\};',data,re.S):
 if match[1] in receipt['protected_array_sha256']:
  assert hashlib.sha256(match[0].encode()).hexdigest()==receipt['protected_array_sha256'][match[1]],match[1]
new_visitors=set()
old_species=set(re.findall(r'SPECIES_(\w+)', '\n'.join(m[0] for m in re.finditer(r'static const struct WildPokemon (sRoute\w+Mons)\[.*?=\s*\{.*?\};',data,re.S) if m[1] in receipt['protected_array_sha256'])))
for route in range(122,127):
 water=route!=123;method='water_mons' if water else 'land_mons';suffix='Water' if water else '';ww=water_weights if water else weights
 original=next(e[method] for e in g['encounters'] if e['map']==f'MAP_ROUTE{route}')
 assert original['encounter_rate']==(4 if water else 20)
 for season in ['Spring','Summer','Autumn','Winter']:
  body=re.search(rf'sRoute{route}{season}{suffix}Mons.*?=\s*\{{(.*?)\}};',data,re.S)[1]
  rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body)
  assert len(rows)==len(ww)
  assert [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in original['mons']]
  residents={m['species'] for m in original['mons']};odds={}
  for (_,_,species),weight in zip(rows,ww):odds[species]=odds.get(species,0)+weight
  visitors=set(odds)-residents
  assert residents<=odds.keys() and sum(odds[x] for x in residents)==(65 if water else 70)
  assert sorted(odds[x] for x in visitors)==([5,30] if water else [10,20])
  assert {v.removeprefix('SPECIES_') for v in visitors}==set(receipt['routes'][str(route)]['visitors'][season.lower()])
  assert not(old_species&{v.removeprefix('SPECIES_') for v in visitors})
  assert not(new_visitors&visitors);new_visitors|=visitors
assert len(new_visitors)==40
# Routes 127–131: protect every preceding array and rare native Wailord.
latest=json.loads((R/'docs/qa/seasonal-routes-v0.0.73-source.json').read_text())
for match in re.finditer(r'static const struct WildPokemon (sRoute\w+Mons)\[.*?=\s*\{.*?\};',data,re.S):
 if match[1] in latest['protected_array_sha256']:
  assert hashlib.sha256(match[0].encode()).hexdigest()==latest['protected_array_sha256'][match[1]],match[1]
fresh=set();grotto=json.loads((R/'src/data/legends/grotto_encounters.json').read_text())
grotto_species={m['species'] for room in grotto['rooms'] for pool in room['seasons'].values() for m in pool}
prior=set(re.findall(r'SPECIES_(\w+)', '\n'.join(m[0] for m in re.finditer(r'static const struct WildPokemon (sRoute\w+Mons)\[.*?=\s*\{.*?\};',data,re.S) if m[1] in latest['protected_array_sha256'])))
for route in range(127,132):
 original=next(e['water_mons'] for e in g['encounters'] if e['map']==f'MAP_ROUTE{route}')
 residents={m['species'] for m in original['mons']}
 for season in ['Spring','Summer','Autumn','Winter']:
  body=re.search(rf'sRoute{route}{season}WaterMons.*?=\s*\{{(.*?)\}};',data,re.S)[1]
  rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body)
  assert len(rows)==5 and [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in original['mons']]
  odds={}
  for (_,_,species),weight in zip(rows,water_weights):odds[species]=odds.get(species,0)+weight
  visitors=set(odds)-residents
  assert residents<=odds.keys() and sum(odds[x] for x in residents)==(70 if route==129 else 65)
  assert sorted(odds[x] for x in visitors)==([30] if route==129 else [5,30])
  if route==129:assert odds['SPECIES_WAILORD']==1
  stripped={s.removeprefix('SPECIES_') for s in visitors}
  assert stripped==set(latest['routes'][str(route)]['visitors'][season.lower()])
  assert not(stripped&(prior|grotto_species|fresh));fresh|=stripped
assert len(fresh)==36
# Final numbered Hoenn sea routes retain every preceding array and native method.
current=json.loads((R/'docs/qa/seasonal-routes-v0.0.74-source.json').read_text())
prior=set()
for match in re.finditer(r'static const struct WildPokemon (sRoute\w+Mons)\[.*?=\s*\{.*?\};',data,re.S):
 if match[1] in current['protected_array_sha256']:
  assert hashlib.sha256(match[0].encode()).hexdigest()==current['protected_array_sha256'][match[1]],match[1]
  prior.update(re.findall(r'SPECIES_(\w+)',match[0]))
fresh=set()
for route in range(132,135):
 original=next(e['water_mons'] for e in g['encounters'] if e['map']==f'MAP_ROUTE{route}')
 residents={m['species'] for m in original['mons']};assert original['encounter_rate']==4
 for season in ['Spring','Summer','Autumn','Winter']:
  body=re.search(rf'sRoute{route}{season}WaterMons.*?=\s*\{{(.*?)\}};',data,re.S)[1];rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body)
  assert len(rows)==5 and [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in original['mons']]
  odds={}
  for (_,_,species),weight in zip(rows,water_weights):odds[species]=odds.get(species,0)+weight
  visitors=set(odds)-residents;stripped={x.removeprefix('SPECIES_') for x in visitors}
  assert residents<=odds.keys() and sum(odds[x] for x in residents)==65 and sorted(odds[x] for x in visitors)==[5,30]
  assert stripped==set(current['routes'][str(route)]['visitors'][season.lower()])
  assert not(stripped&(prior|grotto_species|fresh));fresh|=stripped
assert len(fresh)==24 and 'FEEBAS' not in fresh
# The Kanto tables retain native per-slot levels, the rate and each original resident.
kanto_visitors=set()
prior_visitors=all_visitors|water_visitors|extra_visitors|next_visitors|latest_visitors|{'SPECIES_'+name for name in prior|grotto_species|fresh}
for route in range(1,5):
 original=next(e['land_mons'] for e in g['encounters'] if e['map']==f'MAP_LEGENDS_KANTO_ROUTE{route}')
 assert original['encounter_rate']==21
 residents={m['species'] for m in original['mons']}
 for season in ('Spring','Summer','Autumn','Winter'):
  body=re.search(rf'sKantoRoute{route}{season}Mons.*?=\s*\{{(.*?)\}};',data,re.S)[1]
  rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body)
  assert len(rows)==12 and [(int(a),int(b)) for a,b,_ in rows]==[(m['min_level'],m['max_level']) for m in original['mons']]
  odds={}
  for (_,_,species),weight in zip(rows,weights):odds[species]=odds.get(species,0)+weight
  visitors=set(odds)-residents
  assert residents<=odds.keys() and sum(odds[x] for x in residents)==70
  assert sorted(odds[x] for x in visitors)==[10,20] and not(visitors&(prior_visitors|kanto_visitors))
  kanto_visitors|=visitors
assert len(kanto_visitors)==32
new_kanto=set()
kanto_land=[*(str(r) for r in range(6,19)),'21_NORTH']
kanto_water=['19','20','21_NORTH','21_SOUTH']
for routes,method,suffix,slot_weights,resident_share,visitor_weights in (
    (kanto_land,'land_mons','',weights,70,[10,20]),
    (kanto_water,'water_mons','Water',water_weights,65,[5,30]),
):
 for route in routes:
  original=next(e[method] for e in g['encounters'] if e['map']==f'MAP_LEGENDS_KANTO_ROUTE{route}')
  native_rate=2 if suffix else 14 if route.startswith('21_') else 21
  assert original['encounter_rate']==native_rate
  residents={m['species'] for m in original['mons']}
  for season in ('Spring','Summer','Autumn','Winter'):
   label=f'sKantoRoute{route}{season}{suffix}Mons'
   body=re.search(rf'{label}.*?=\s*\{{(.*?)\}};',data,re.S)[1]
   rows=re.findall(r'\{(\d+), (\d+), (SPECIES_\w+)\}',body)
   assert len(rows)==len(slot_weights)
   assert [(int(lo),int(hi)) for lo,hi,_ in rows]==[(m['min_level'],m['max_level']) for m in original['mons']]
   odds={}
   for row,weight in zip(rows,slot_weights):
    odds[row[2]]=odds.get(row[2],0)+weight
   visitors=set(odds)-residents
   assert residents<=odds.keys() and sum(odds[x] for x in residents)==resident_share
   assert sorted(odds[x] for x in visitors)==visitor_weights
   assert not visitors&(kanto_visitors|new_kanto|{'SPECIES_'+name for name in grotto_species}|{'SPECIES_DA_BUG'})
   new_kanto|=visitors
assert len(new_kanto)==144
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
#define MAP_ROUTE122 122
#define MAP_ROUTE123 123
#define MAP_ROUTE124 124
#define MAP_ROUTE125 125
#define MAP_ROUTE126 126
#define MAP_ROUTE127 127
#define MAP_ROUTE128 128
#define MAP_ROUTE129 129
#define MAP_ROUTE130 130
#define MAP_ROUTE131 131
#define MAP_ROUTE132 132
#define MAP_ROUTE133 133
#define MAP_ROUTE134 134
#define MAP_LEGENDS_KANTO_ROUTE1 0x4B01
#define MAP_LEGENDS_KANTO_ROUTE2 0x4B02
#define MAP_LEGENDS_KANTO_ROUTE3 0x4B03
#define MAP_LEGENDS_KANTO_ROUTE4 0x4B04
#define MAP_LEGENDS_KANTO_ROUTE6 0x4B05
#define MAP_LEGENDS_KANTO_ROUTE7 0x4B06
#define MAP_LEGENDS_KANTO_ROUTE8 0x4B07
#define MAP_LEGENDS_KANTO_ROUTE9 0x4B08
#define MAP_LEGENDS_KANTO_ROUTE10 0x4B09
#define MAP_LEGENDS_KANTO_ROUTE11 0x4B0A
#define MAP_LEGENDS_KANTO_ROUTE12 0x4B0B
#define MAP_LEGENDS_KANTO_ROUTE13 0x4B0C
#define MAP_LEGENDS_KANTO_ROUTE14 0x4B0D
#define MAP_LEGENDS_KANTO_ROUTE15 0x4B0E
#define MAP_LEGENDS_KANTO_ROUTE16 0x4B0F
#define MAP_LEGENDS_KANTO_ROUTE17 0x4B10
#define MAP_LEGENDS_KANTO_ROUTE18 0x4B11
#define MAP_LEGENDS_KANTO_ROUTE19 0x4B12
#define MAP_LEGENDS_KANTO_ROUTE20 0x4B13
#define MAP_LEGENDS_KANTO_ROUTE21_NORTH 0x4B14
#define MAP_LEGENDS_KANTO_ROUTE21_SOUTH 0x4B15
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
static struct WildPokemonHeader gWildMonHeaders[57];
static unsigned active,reads,pending,currentHeader;
#define MAX_LEVEL 100
#define MON_LEVEL_NONEXISTENT 255
#define NUM_WATER_MONS_ENCOUNTER_SLOTS 5
#define NUM_HIDDEN_MONS_ENCOUNTER_SLOTS 3
#define NUM_ROCK_SMASH_MONS_ENCOUNTER_SLOTS 5
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
 static const unsigned kantoMaps[]={MAP_LEGENDS_KANTO_ROUTE1,MAP_LEGENDS_KANTO_ROUTE2,MAP_LEGENDS_KANTO_ROUTE3,MAP_LEGENDS_KANTO_ROUTE4,MAP_LEGENDS_KANTO_ROUTE6,MAP_LEGENDS_KANTO_ROUTE7,MAP_LEGENDS_KANTO_ROUTE8,MAP_LEGENDS_KANTO_ROUTE9,MAP_LEGENDS_KANTO_ROUTE10,MAP_LEGENDS_KANTO_ROUTE11,MAP_LEGENDS_KANTO_ROUTE12,MAP_LEGENDS_KANTO_ROUTE13,MAP_LEGENDS_KANTO_ROUTE14,MAP_LEGENDS_KANTO_ROUTE15,MAP_LEGENDS_KANTO_ROUTE16,MAP_LEGENDS_KANTO_ROUTE17,MAP_LEGENDS_KANTO_ROUTE18,MAP_LEGENDS_KANTO_ROUTE19,MAP_LEGENDS_KANTO_ROUTE20,MAP_LEGENDS_KANTO_ROUTE21_NORTH,MAP_LEGENDS_KANTO_ROUTE21_SOUTH};
 for(unsigned h=0;h<56;h++){gWildMonHeaders[h].mapGroup=h<35?0:0x4B;gWildMonHeaders[h].mapNum=h<35?101+h:(kantoMaps[h-35]&255);for(unsigned t=0;t<4;t++){gWildMonHeaders[h].encounterTypes[t].landMonsInfo=&fallback[t];gWildMonHeaders[h].encounterTypes[t].waterMonsInfo=&waterFallback[t];}}
 for(unsigned season=0;season<4;season++)for(unsigned t=0;t<4;t++){
  active=season;pending=(season+1)%4;
  for(unsigned h=0;h<56;h++){
   currentHeader=h;
   unsigned map=(gWildMonHeaders[h].mapGroup<<8)|gWildMonHeaders[h].mapNum;
   for(unsigned area=0;area<2;area++){
    const struct WildPokemonInfo *expected=area?&waterFallback[t]:&fallback[t],*previous=NULL;
    unsigned rate=0,slots=area?5:12;
    if(area){for(unsigned i=0;i<ARRAY_COUNT(sLegendsSeasonalWater);i++)if(sLegendsSeasonalWater[i].map==map){expected=&sLegendsSeasonalWater[i].seasons[season];previous=&sLegendsSeasonalWater[i].seasons[(season+3)%4];rate=h>=35?2:4;}}
    else {for(unsigned i=0;i<ARRAY_COUNT(sLegendsSeasonalLand);i++)if(sLegendsSeasonalLand[i].map==map){expected=&sLegendsSeasonalLand[i].seasons[season];previous=&sLegendsSeasonalLand[i].seasons[(season+3)%4];rate=(h>=35?(map==MAP_LEGENDS_KANTO_ROUTE21_NORTH||map==MAP_LEGENDS_KANTO_ROUTE21_SOUTH?14:21):h==10?10:h==18?15:20);}}
    unsigned before=reads;const struct WildPokemonInfo *p=area?GetWaterMonsInfo(h,t):GetLandMonsInfo(h,t);
    assert(p==expected);assert(active==season&&pending==(season+1)%4);
    if(!previous){assert(reads==before);continue;}assert(p->encounterRate==rate);
    unsigned absent=0;
    for(unsigned i=0;i<slots;i++){
     assert(GetEncounterLevelFromMapData(p->wildPokemon[i].species,area?ENCOUNTER_TYPE_WATER:ENCOUNTER_TYPE_LAND)!=255);
     enum Species species=previous->wildPokemon[i].species;unsigned present=0;
     for(unsigned j=0;j<slots;j++)if(p->wildPokemon[j].species==species)present=1;
     if(!present){
      assert(GetEncounterLevelFromMapData(species,area?ENCOUNTER_TYPE_WATER:ENCOUNTER_TYPE_LAND)==255);
      unsigned next=GetNextWildEncounterSeason(h,area?WILD_AREA_WATER:WILD_AREA_LAND,species);
      // A visitor from last season must return within the next three seasons.
      assert(next<LEGENDS_SEASON_COUNT);
      const struct WildPokemonInfo *seasons=expected-season;
      for(unsigned offset=1;offset<LEGENDS_SEASON_COUNT;offset++){
       unsigned candidate=(season+offset)%LEGENDS_SEASON_COUNT, found=0;
       for(unsigned j=0;j<slots;j++)if(seasons[candidate].wildPokemon[j].species==species)found=1;
       if(found){assert(next==candidate);break;}
      }
      absent++;
     }
    }assert(absent);
   }
  }
 }
 assert(!GetLandMonsInfo(HEADER_NONE,0)&&!GetLandMonsInfo(56,0)&&!GetLandMonsInfo(0,4)&&!GetLandMonsInfo(0,(enum TimeOfDay)-1));
 assert(!GetWaterMonsInfo(HEADER_NONE,0)&&!GetWaterMonsInfo(56,0)&&!GetWaterMonsInfo(0,4)&&!GetWaterMonsInfo(0,(enum TimeOfDay)-1));
 active=LEGENDS_SPRING;
 assert(GetNextWildEncounterSeason(0,WILD_AREA_LAND,SPECIES_ROOKIDEE)==LEGENDS_WINTER);
 assert(GetNextWildEncounterSeason(0,WILD_AREA_WATER,SPECIES_ROOKIDEE)==LEGENDS_SEASON_COUNT);
 assert(GetNextWildEncounterSeason(0,WILD_AREA_HIDDEN,SPECIES_ROOKIDEE)==LEGENDS_SEASON_COUNT);
 assert(GetNextWildEncounterSeason(1,WILD_AREA_LAND,SPECIES_ROOKIDEE)==LEGENDS_SEASON_COUNT);
 assert(GetNextWildEncounterSeason(HEADER_NONE,WILD_AREA_LAND,SPECIES_ROOKIDEE)==LEGENDS_SEASON_COUNT);
 active=LEGENDS_WINTER;
 assert(GetNextWildEncounterSeason(0,WILD_AREA_LAND,SPECIES_ROOKIDEE)==LEGENDS_SEASON_COUNT);
 assert(GetNextWildEncounterSeason(4,WILD_AREA_WATER,SPECIES_FINNEON)==LEGENDS_SPRING);
 active=255;
 assert(GetNextWildEncounterSeason(0,WILD_AREA_LAND,SPECIES_ROOKIDEE)==LEGENDS_SEASON_COUNT);
 for(unsigned h=0;h<56;h++){assert(GetLandMonsInfo(h,0)==&fallback[0]);assert(GetWaterMonsInfo(h,0)==&waterFallback[0]);}
 currentHeader=HEADER_NONE;assert(GetEncounterLevelFromMapData(SPECIES_WURMPLE,ENCOUNTER_TYPE_LAND)==255);
 puts("PASS: all 224 seasonal tables, rates, committed season, native fallbacks and next-season DexNav visits");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(wild_area+pre+data+max_level_function+function+level_function+main)
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
print('PASS: original residents/levels/rates, 70/20/10 base distribution, 444 visitor selections, native 65/30/5 Surf odds and all dependent land/Surf readers')
