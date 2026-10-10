"""Exercise actual climate/forecast/clock C under native service mocks."""
import json, pathlib, subprocess, tempfile
root = pathlib.Path(__file__).resolve().parents[1]
source = (root / 'src/legends_weather.c').read_text()
source = '\n'.join(x for x in source.splitlines() if not x.startswith('#include'))
preamble = r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32;
typedef int bool32; typedef u32 rng_value_t;
#define EWRAM_DATA
#define WEATHER_PAL_STATE_IDLE 0
#define FLAG_LEGENDS_WEATHER_CLOCK_INITIALIZED 0
#define VAR_LEGENDS_WEATHER_SECONDS 0
#define VAR_LEGENDS_BASE_WEATHER 1
enum {TIME_MORNING,TIME_DAY,TIME_EVENING,TIME_NIGHT};
'''
for f in ['include/constants/weather.h','include/constants/map_types.h','include/legends_seasons.h','include/legends_weather.h']:
    preamble += (root/f).read_text() + '\n'
sections = json.loads((root/'src/data/region_map/region_map_sections.json').read_text())['map_sections']
ids = [s['id'] for s in sections]
assert ids[ids.index('MAPSEC_ROUTE_101'):ids.index('MAPSEC_ROUTE_134')+1] == [f'MAPSEC_ROUTE_{i}' for i in range(101,135)]
preamble += '\n'.join(f'#define {s} {i}' for i,s in enumerate(ids)) + '\n'
preamble += r'''
struct {u8 mapType;u16 regionMapSectionId;} gMapHeader;
struct {u32 dailySeed;u8 weather;} save1,*gSaveBlock1Ptr=&save1;
struct {u16 playTimeHours;u8 playTimeMinutes,playTimeSeconds;} save2,*gSaveBlock2Ptr=&save2;
struct {u8 currWeather,nextWeather,palProcessingState;} state,*gWeatherPtr=&state;
struct {u8 active;} gPaletteFade;
static u16 vars[2]; static int initialized,script,season,tod=TIME_DAY,savedCalls,nextCalls;
static u32 outcome,seedPieces[4];
u16 VarGet(int v){return vars[v];} void VarSet(int v,u16 x){vars[v]=x;}
int FlagGet(int f){return initialized;} void FlagSet(int f){initialized=1;}
u8 LegendsGetActiveSeason(void){return season;} int GetTimeOfDay(void){return tod;}
u32 Crc32B(const u8 *p,int n){assert(n==sizeof(seedPieces));memcpy(seedPieces,p,n);return 123;}
rng_value_t LocalRandomSeed(u32 s){return s;} u32 LocalRandom32(rng_value_t *s){return outcome;}
int ScriptContext_IsEnabled(void){return script;}
u8 GetCurrentWeather(void){return state.currWeather;}
u8 GetSavedWeather(void){return save1.weather;}
void SetSavedWeather(u8 w){savedCalls++;vars[1]=0x100+w;if(w==WEATHER_ROUTE119_CYCLE||w==WEATHER_ROUTE123_CYCLE)w=WEATHER_RAIN;save1.weather=LegendsChooseAmbientWeather(w);}
void SetNextWeather(u8 w){nextCalls++;state.nextWeather=w;}
'''
main = r'''
static void poll(void){for(int i=0;i<60;i++)LegendsWeatherTick();}
static int countWeather(int wanted){int n=0;for(outcome=0;outcome<100;outcome++)n+=LegendsChooseAmbientWeather(WEATHER_SUNNY)==wanted;return n;}
int main(void){
 gMapHeader.mapType=MAP_TYPE_ROUTE;gMapHeader.regionMapSectionId=MAPSEC_ROUTE_101;
 save2.playTimeHours=999;save2.playTimeMinutes=59;save2.playTimeSeconds=59;
 outcome=99;LegendsChooseAmbientWeather(WEATHER_SUNNY);
 assert(initialized&&vars[0]==(999u*3600+3599)%LEGENDS_WEATHER_CYCLE_SECONDS);
 vars[0]=1199;LegendsChooseAmbientWeather(WEATHER_SUNNY);assert(seedPieces[1]==0);
 LegendsAdvanceWeatherClock();LegendsChooseAmbientWeather(WEATHER_SUNNY);assert(seedPieces[1]==1);
 vars[0]=LEGENDS_WEATHER_CYCLE_SECONDS-1;LegendsAdvanceWeatherClock();assert(vars[0]==0);
 for(season=0;season<4;season++){
  gMapHeader.regionMapSectionId=MAPSEC_ROUTE_101;
  assert(countWeather(WEATHER_SNOW)==0);assert(countWeather(WEATHER_FOG_HORIZONTAL)==0);
  int dryRain=countWeather(WEATHER_RAIN);
  assert(dryRain==(season==LEGENDS_SPRING?30:season==LEGENDS_SUMMER?18:25));
  gMapHeader.regionMapSectionId=MAPSEC_ROUTE_119;
  assert(countWeather(WEATHER_RAIN)==dryRain+20);assert(countWeather(WEATHER_SNOW)==0);
  int dayFog=countWeather(WEATHER_FOG_HORIZONTAL);tod=TIME_NIGHT;
  assert(countWeather(WEATHER_FOG_HORIZONTAL)==dayFog+8);tod=TIME_MORNING;
  assert(countWeather(WEATHER_FOG_HORIZONTAL)==dayFog+8);tod=TIME_DAY;
  gMapHeader.regionMapSectionId=MAPSEC_ROUTE_114;
  assert(countWeather(WEATHER_SNOW)==(season==LEGENDS_WINTER?25:0));
  gMapHeader.regionMapSectionId=MAPSEC_ROUTE_124;gMapHeader.mapType=MAP_TYPE_OCEAN_ROUTE;
  assert(countWeather(WEATHER_SNOW)==0);gMapHeader.mapType=MAP_TYPE_ROUTE;
 }

 // Kanto forecasts: verify exact seasonal weights, coast snow exclusion and fog.
 const int areas[]={MAPSEC_CELADON_CITY,MAPSEC_VERMILION_CITY,MAPSEC_ROUTE_10};
 const int weights[3][4][4]={
  {{30,2,5,0},{20,5,0,0},{25,1,8,0},{12,0,6,15}},
  {{28,2,3,0},{22,6,0,0},{30,2,5,0},{18,0,5,0}},
  {{25,2,8,0},{18,4,4,0},{25,1,12,0},{8,0,10,30}}};
 for(int a=0;a<3;a++)for(season=0;season<4;season++){
  gMapHeader.regionMapSectionId=areas[a];tod=TIME_DAY;
  assert(countWeather(WEATHER_RAIN)==weights[a][season][0]);
  assert(countWeather(WEATHER_RAIN_THUNDERSTORM)==weights[a][season][1]);
  assert(countWeather(WEATHER_FOG_HORIZONTAL)==weights[a][season][2]);
  assert(countWeather(WEATHER_SNOW)==weights[a][season][3]);
  for(tod=TIME_MORNING;tod<=TIME_NIGHT;tod++)
   assert(countWeather(WEATHER_FOG_HORIZONTAL)==weights[a][season][2]+((tod==TIME_MORNING||tod==TIME_NIGHT)?5:0));
  tod=TIME_DAY;gMapHeader.mapType=MAP_TYPE_INDOOR;outcome=0;
  assert(LegendsChooseAmbientWeather(WEATHER_SUNNY)==WEATHER_SUNNY);
  gMapHeader.mapType=MAP_TYPE_ROUTE;
 }
 // Cover every Kanto route and every current outdoor map, including future IDs.
 for(int r=MAPSEC_ROUTE_1;r<=MAPSEC_ROUTE_25;r++){
  gMapHeader.regionMapSectionId=r;season=LEGENDS_SUMMER;outcome=0;
  assert(countWeather(WEATHER_RAIN_THUNDERSTORM)>0);
 }
 int protected[]={MAPSEC_ROUTE_111,MAPSEC_ROUTE_112,MAPSEC_ROUTE_113,MAPSEC_MT_CHIMNEY,MAPSEC_JAGGED_PASS,MAPSEC_FIERY_PATH,MAPSEC_LAVARIDGE_TOWN,MAPSEC_FALLARBOR_TOWN,MAPSEC_MT_PYRE,MAPSEC_BATTLE_FRONTIER,MAPSEC_MT_MOON,MAPSEC_SEAFOAM_ISLANDS,MAPSEC_KANTO_VICTORY_ROAD,MAPSEC_VIRIDIAN_FOREST,MAPSEC_POWER_PLANT};
 for(unsigned i=0;i<sizeof(protected)/sizeof(*protected);i++){
  gMapHeader.regionMapSectionId=protected[i];outcome=0;
  assert(LegendsChooseAmbientWeather(WEATHER_SUNNY)==WEATHER_SUNNY);
 }
 gMapHeader.regionMapSectionId=MAPSEC_ROUTE_101;
 int indoors[]={MAP_TYPE_INDOOR,MAP_TYPE_UNDERGROUND,MAP_TYPE_UNDERWATER,MAP_TYPE_SECRET_BASE};
 for(unsigned i=0;i<sizeof(indoors)/sizeof(*indoors);i++){gMapHeader.mapType=indoors[i];assert(LegendsChooseAmbientWeather(WEATHER_SUNNY)==WEATHER_SUNNY);}
 gMapHeader.mapType=MAP_TYPE_ROUTE;
 for(int w=0;w<WEATHER_COUNT;w++)if(w!=WEATHER_SUNNY&&w!=WEATHER_SUNNY_CLOUDS&&w!=WEATHER_RAIN&&w!=WEATHER_RAIN_THUNDERSTORM)assert(LegendsChooseAmbientWeather(w)==w);
 // Every forecast roll in every configured climate/time/season is cloud-free.
 // Native SUNNY_CLOUDS requests remain valid inputs for old saves/map triggers.
 int ordinary[]={MAPSEC_LITTLEROOT_TOWN,MAPSEC_OLDALE_TOWN,MAPSEC_PETALBURG_CITY,MAPSEC_RUSTBORO_CITY,MAPSEC_MAUVILLE_CITY,MAPSEC_VERDANTURF_TOWN,MAPSEC_DEWFORD_TOWN,MAPSEC_SLATEPORT_CITY,MAPSEC_ROUTE_119,MAPSEC_ROUTE_120,MAPSEC_ROUTE_114,MAPSEC_PETALBURG_WOODS,MAPSEC_VERMILION_CITY,MAPSEC_FUCHSIA_CITY,MAPSEC_LAVENDER_TOWN,MAPSEC_CELADON_CITY,MAPSEC_SAFFRON_CITY,MAPSEC_ROUTE_6,MAPSEC_ROUTE_10,MAPSEC_ROUTE_19};
 int requests[]={WEATHER_SUNNY,WEATHER_SUNNY_CLOUDS,WEATHER_RAIN,WEATHER_RAIN_THUNDERSTORM};
 for(unsigned area=0;area<sizeof(ordinary)/sizeof(*ordinary);area++)
  for(season=0;season<4;season++)for(tod=TIME_MORNING;tod<=TIME_NIGHT;tod++)
   for(unsigned req=0;req<sizeof(requests)/sizeof(*requests);req++)for(outcome=0;outcome<100;outcome++){
    gMapHeader.regionMapSectionId=ordinary[area];
    assert(LegendsChooseAmbientWeather(requests[req])!=WEATHER_SUNNY_CLOUDS);
   }
 // Keep native cloud reflections on protected maps (e.g. Faraway Island).
 gMapHeader.regionMapSectionId=MAPSEC_FARAWAY_ISLAND;
 assert(LegendsChooseAmbientWeather(WEATHER_SUNNY_CLOUDS)==WEATHER_SUNNY_CLOUDS);
 gMapHeader.regionMapSectionId=MAPSEC_ROUTE_101;season=LEGENDS_SPRING;tod=TIME_DAY;
 assert(countWeather(WEATHER_SUNNY)==68); // former 18% cloud share is now clear
 // An active cloud forecast from an older save transitions through native cleanup.
 outcome=99;vars[1]=0x100+WEATHER_SUNNY_CLOUDS;
 state.currWeather=state.nextWeather=WEATHER_SUNNY_CLOUDS;poll();
 assert(savedCalls==1&&nextCalls==1&&state.nextWeather==WEATHER_SUNNY);
 state.currWeather=state.nextWeather;poll();assert(savedCalls==2&&nextCalls==1);
 savedCalls=nextCalls=0;
 // A changing forecast goes through native saved/next-weather services only.
 season=LEGENDS_SPRING;outcome=10;vars[1]=0x100+WEATHER_SUNNY;
 state.currWeather=state.nextWeather=WEATHER_SUNNY;poll();
 assert(savedCalls==1&&nextCalls==1&&state.nextWeather==WEATHER_RAIN&&vars[1]==0x100+WEATHER_SUNNY);
 poll();assert(savedCalls==1); // unfinished transition
 state.currWeather=state.nextWeather;poll();assert(savedCalls==2&&nextCalls==1);
 script=1;poll();script=0;gPaletteFade.active=1;poll();gPaletteFade.active=0;
 state.palProcessingState=1;poll();state.palProcessingState=0;assert(savedCalls==2);
 vars[1]=0x100+WEATHER_DROUGHT;poll();assert(savedCalls==2);
 vars[1]=0x100+WEATHER_SUNNY;state.currWeather=state.nextWeather=WEATHER_ABNORMAL;poll();assert(savedCalls==2);
 state.currWeather=state.nextWeather=WEATHER_SUNNY;vars[1]=0;poll();assert(savedCalls==2);
 vars[1]=0x100+WEATHER_ROUTE119_CYCLE;poll();assert(savedCalls==3&&vars[1]==0x100+WEATHER_ROUTE119_CYCLE);
 // Kanto walking transitions use the same native guards and keep the baseline.
 gMapHeader.regionMapSectionId=MAPSEC_VERMILION_CITY;season=LEGENDS_SUMMER;
 state.currWeather=state.nextWeather=WEATHER_SUNNY;vars[1]=0x100+WEATHER_SUNNY;
 savedCalls=nextCalls=0;outcome=0;poll();
 assert(savedCalls==1&&nextCalls==1&&state.nextWeather==WEATHER_RAIN_THUNDERSTORM);
 script=1;poll();script=0;assert(savedCalls==1);
 state.currWeather=state.nextWeather;gMapHeader.mapType=MAP_TYPE_INDOOR;poll();
 assert(savedCalls==1);gMapHeader.mapType=MAP_TYPE_ROUTE;
 puts("Dynamic weather: climate probabilities, native exclusions, clock migration, cloud-free forecasts and old-save cleanup passed");
}
'''
with tempfile.TemporaryDirectory() as d:
    p=pathlib.Path(d);(p/'weather.c').write_text(preamble+source+main)
    subprocess.run(['cc','-std=c99','-Wall','-Werror','-Wno-unused-variable','-o',str(p/'weather'),str(p/'weather.c')],check=True)
    subprocess.run([str(p/'weather')],check=True)
assert 'LegendsWeatherTick();' in (root/'src/field_weather.c').read_text()
assert 'LegendsAdvanceWeatherClock();' in (root/'src/legends_seasons.c').read_text()
