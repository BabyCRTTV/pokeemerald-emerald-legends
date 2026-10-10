"""Host-exercise the actual region-switch task and displayed cursor lookup."""
from pathlib import Path
import subprocess,tempfile,re
R=Path(__file__).resolve().parents[1]
nav=(R/'src/pokenav_region_map.c').read_text();core=(R/'src/region_map.c').read_text()
def function(s,name):
 start=s.index(name+'(')
 while s[s.index('\n',start)-1]==';':start=s.index(name+'(',start+len(name))
 start=s.rfind('\n',0,start)+1;end=s.index('\n}',start)+2;return s[start:end]
task=function(nav,'LoopedTask_SwitchRegion');lookup=function(core,'GetMapSecIdAt')
stub=r'''
#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
typedef int s32;typedef unsigned int u32;typedef unsigned short u16;typedef unsigned short mapsec_u16_t;
#define FALSE 0
#define TRUE 1
#define REGION_MAP_HOENN 0
#define REGION_MAP_KANTO 1
#define REGION_MAP_SEVII123 2
#define REGION_MAP_SEVII45 3
#define REGION_MAP_SEVII67 4
#define MAPSEC_NONE 99
#define MAPCURSOR_X_MIN 1
#define MAPCURSOR_Y_MIN 2
#define MAPCURSOR_X_MAX 28
#define MAPCURSOR_Y_MAX 16
#define POKENAV_SUBSTRUCT_REGION_MAP_STATE 0
#define POKENAV_SUBSTRUCT_REGION_MAP_ZOOM 1
#define POKENAV_SUBSTRUCT_REGION_MAP 2
#define SE_SELECT 0
#define POKENAV_FADE_TO_BLACK 1
#define POKENAV_FADE_FROM_BLACK 0
#define POKENAV_GFX_MAP_MENU_ZOOMED_OUT 0
#define LT_PAUSE 1
#define LT_INC_AND_PAUSE 2
#define LT_FINISH 3
struct Pokenav_RegionMapMenu{int displayRegion;bool switchingFromZoom;};
struct Pokenav_RegionMapGfx{int unused;};
struct RegionMap{int displayRegion;};
static struct Pokenav_RegionMapMenu menu;
static struct Pokenav_RegionMapGfx gfx;
static struct RegionMap map,*sRegionMap=&map;
static const int sRegionMapBgTemplates[2]={0};
static int actualRegion,zoomed,zoomCalls,fadeBusy,bgBusy,freed,playerIcons,cursors,loads,changed;
static const mapsec_u16_t sRegionMapSections_Kanto[15][28]={{12}};
static const mapsec_u16_t sRegionMapSections_Sevii123[15][28]={{13}};
static const mapsec_u16_t sRegionMapSections_Sevii45[15][28]={{14}};
static const mapsec_u16_t sRegionMapSections_Sevii67[15][28]={{15}};
static const mapsec_u16_t sRegionMap_MapSectionLayout[15][28]={{11}};
static void *GetSubstructPtr(int id){return id==0?(void*)&menu:id==1?(void*)&gfx:(void*)&map;}
static void PlaySE(int x){}
static void PokenavFadeScreen(int x){}
static bool IsPaletteFadeActive(void){return fadeBusy;}
static bool IsRegionMapZoomed(void){return zoomed;}
static void ChangeBgYForZoom(bool x){changed++;}
static void SetRegionMapDataForZoom(void){}
static bool UpdateRegionMapZoom(void){zoomCalls++;zoomed=0;return false;}
static bool IsChangeBgYForZoomActive(void){return false;}
static void FreeRegionMapIconResources(void){freed++;}
static void InitRegionMapData(struct RegionMap *m,const int *t,bool z){m->displayRegion=actualRegion;zoomed=z;}
static void RegionMap_SetDisplayRegion(int region){map.displayRegion=region;}
static bool LoadRegionMapGfx(void){loads++;return false;}
static void CreateRegionMapCursor(int a,int b){cursors++;}
static bool RegionMap_IsViewingCurrentRegion(void){return map.displayRegion==actualRegion;}
static void CreateRegionMapPlayerIcon(int a,int b){playerIcons++;}
static void TrySetPlayerIconBlink(void){}
static void UpdateMapSecInfoWindow(struct Pokenav_RegionMapGfx *g){}
static void UpdateRegionMapHelpBarText(void){}
static void UpdateRegionMapRightHeaderTiles(int x){}
static bool IsDma3ManagerBusyWithBgCopy_(struct Pokenav_RegionMapGfx *g){return bgBusy;}
static bool WaitForHelpBar(void){return false;}
'''
main=r'''
int main(void){
 for(int origin=0;origin<=1;origin++)for(int z=0;z<=1;z++){
  actualRegion=origin;menu.displayRegion=origin;map.displayRegion=origin;zoomed=z;zoomCalls=freed=playerIcons=cursors=changed=loads=0;
  assert(LoopedTask_SwitchRegion(0)==LT_INC_AND_PAUSE);
  fadeBusy=1;assert(LoopedTask_SwitchRegion(1)==LT_PAUSE);assert(freed==0);
  fadeBusy=0;assert(LoopedTask_SwitchRegion(1)==LT_INC_AND_PAUSE);
  assert(LoopedTask_SwitchRegion(2)==LT_INC_AND_PAUSE);assert(zoomCalls==z);assert(changed==z);assert(freed==1);
  assert(actualRegion==origin);assert(map.displayRegion==1-origin);assert(!zoomed);
  assert(LoopedTask_SwitchRegion(3)==LT_INC_AND_PAUSE);assert(playerIcons==0);assert(cursors==1);
  assert(GetMapSecIdAt(1,2)==(origin==0?12:11));assert(GetMapSecIdAt(0,2)==MAPSEC_NONE);assert(GetMapSecIdAt(1,17)==MAPSEC_NONE);
  bgBusy=1;assert(LoopedTask_SwitchRegion(4)==LT_PAUSE);bgBusy=0;assert(LoopedTask_SwitchRegion(4)==LT_INC_AND_PAUSE);
  assert(LoopedTask_SwitchRegion(5)==LT_FINISH);
  LoopedTask_SwitchRegion(0);LoopedTask_SwitchRegion(1);LoopedTask_SwitchRegion(2);LoopedTask_SwitchRegion(3);
  assert(map.displayRegion==origin);assert(playerIcons==1);assert(zoomCalls==z);
 }
 return 0;
}
'''
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp);(p/'test.c').write_text(stub+'\n'+lookup+'\n'+task+'\n'+main)
 subprocess.run(['gcc','-std=c99','-Wall','-Werror','-Wno-unused-function','-Wno-unused-variable',str(p/'test.c'),'-o',str(p/'test')],check=True)
 subprocess.run([str(p/'test')],check=True)
# Both input modes expose SELECT; Fly and help only advertise actual-region travel.
assert core.count('input = MAP_INPUT_SELECT_BUTTON;')==2
assert 'RegionMap_IsViewingCurrentRegion() && regionMap->mapSecType' in nav
assert 'FlagGet(FLAG_SYS_GAME_CLEAR)' in nav
print('Region map task: fades, full/zoomed switches, cursor regions, marker and no travel mutation passed')
