"""Compile the native DexNav proximity guard with deterministic terrain fixtures."""
from pathlib import Path
import subprocess,tempfile,re
root=Path(__file__).resolve().parents[1]
source=(root/'src/dexnav.c').read_text();start=source.index('bool8 DexNavHasNearbyEncounterArea(void)');end=source.index('\n}',start)+2
function=source[start:end]
pre=r'''
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint32_t u32;typedef int16_t s16;typedef int bool8;
#define TRUE 1
#define FALSE 0
#define HEADER_NONE 65535
#define SCANSIZE_X 12
#define SCANSIZE_Y 12
#define WILD_AREA_LAND 0
#define WILD_AREA_WATER 1
struct {struct {s16 x,y;}pos;} save,*gSaveBlock1Ptr=&save;
struct {struct {void*landMonsInfo;void*waterMonsInfo;}encounterTypes[1];}gWildMonHeaders[1];
static int header,tiles[32][32],blocked[32][32];
u32 GetCurrentMapWildMonHeaderId(void){return header;}
int GetTimeOfDayForEncounters(int h,int area){return 0;}
u8 MapGridGetMetatileBehaviorAt(s16 x,s16 y){assert(x>=0&&x<32&&y>=0&&y<32);return tiles[y][x];}
int MapGridGetCollisionAt(int x,int y){return blocked[y][x];}
int MetatileBehavior_IsLandWildEncounter(int v){return v==1||v==3;}
int MetatileBehavior_IsSurfableWaterOrUnderwater(int v){return v==2;}
'''
main=r'''
int main(void){
 save.pos.x=save.pos.y=4;header=HEADER_NONE;assert(!DexNavHasNearbyEncounterArea());
 header=0;assert(!DexNavHasNearbyEncounterArea());
 tiles[10][10]=1;assert(!DexNavHasNearbyEncounterArea());gWildMonHeaders[0].encounterTypes[0].landMonsInfo=(void*)1;assert(DexNavHasNearbyEncounterArea());
 blocked[10][10]=1;assert(!DexNavHasNearbyEncounterArea());blocked[10][10]=0;
 tiles[10][10]=3;assert(DexNavHasNearbyEncounterArea()); // cave floor
 tiles[10][10]=2;assert(!DexNavHasNearbyEncounterArea());gWildMonHeaders[0].encounterTypes[0].waterMonsInfo=(void*)1;assert(DexNavHasNearbyEncounterArea());
 tiles[10][10]=0;tiles[25][25]=1;assert(!DexNavHasNearbyEncounterArea());
 puts("No-table, distant grass, cave floor, water and collision proximity checks passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'dexnav.c';p.write_text(pre+function+main)
 subprocess.run(['cc','-std=gnu17','-Werror=implicit-function-declaration',str(p),'-o',d+'/dexnav'],check=True);subprocess.run([d+'/dexnav'],check=True)
onstep=source[source.index('bool32 OnStep_DexNavSearch(void)'):source.index('bool32 OnStep_DexNavSearch(void)')+6000]
assert 'EventScript_MovedTooFast' not in onstep.split('\nbool')[0]
assert 'if (frameCount > DEXNAV_TIMEOUT * 60)' in onstep
assert re.search(r'#define DEXNAV_TIMEOUT\s+45\b',(root/'include/config/dexnav.h').read_text())
menu=(root/'src/start_menu.c').read_text()
assert '!DexNavHasNearbyEncounterArea()' in menu and 'ShowDexNavHelp();' in menu
assert 'gMenuCallback = HandleStartMenuInput;' in menu[menu.index('static bool8 HandleDexNavHelp(void)'):]
assert '.baseBlock = 0x250' in menu # outside main menu 0x139..0x211
