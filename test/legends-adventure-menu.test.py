"""Compile real pause-menu builders and scrolling; all ten actions stay reachable."""
from pathlib import Path
import subprocess,tempfile,re
R=Path(__file__).resolve().parents[1];source=(R/'src/start_menu.c').read_text()
def function(name,ret,args):
 start=source.index('static '+ret+' '+name+'('+args+')\n{');brace=source.index('{',start);end=brace+1;depth=1
 while depth:depth+=(source[end]=='{')-(source[end]=='}');end+=1
 return source[start:end]
enum=re.search(r'enum\s*\{\s*MENU_ACTION_POKEDEX,.*?\};',source,re.S).group(0)
builders=['BuildNormalStartMenu','BuildDebugStartMenu','BuildSafariZoneStartMenu','BuildBattlePikeStartMenu','BuildBattlePyramidStartMenu','BuildMultiPartnerRoomStartMenu']
code=function('AddStartMenuAction','void','u8 action')+'\n'+'\n'.join(function(n,'void','void') for n in builders)
code+='\n'+function('DrawStartMenuScrollHints','void','void')+'\n'+function('PrintStartMenuActions','bool32','s8 *pIndex, u32 count')+'\n'+function('MoveStartMenuCursor','void','s8 delta')
preamble=r'''
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8; typedef int8_t s8; typedef uint32_t u32; typedef int bool32;
#define TRUE 1
#define FALSE 0
#define START_MENU_VISIBLE_ROWS 8
#define FONT_NORMAL 1
#define TEXT_SKIP_DRAW 0
#define COPYWIN_FULL 3
#define PIXEL_FILL(x) ((x)|((x)<<4))
#define min(a,b) ((a)<(b)?(a):(b))
#define FLAG_SYS_POKEDEX_GET 0
#define FLAG_SYS_POKEMON_GET 1
#define FLAG_SYS_POKENAV_GET 2
#define DN_FLAG_DEXNAV_GET 3
static u8 flags[4],sNumStartMenuActions,sStartMenuTop,sStartMenuCursorPos,sCurrentStartMenuActions[10];
static u8 gStringVar4[128];
static u8 FlagGet(u32 f){return flags[f];}
static void AppendToList(u8 *a,u8 *n,u8 value){assert(*n<10);a[(*n)++]=value;}
static bool32 StartMenuPlayerNameCallback(void){return TRUE;}
struct MenuAction {const char *text;union {bool32 (*u8_void)(void);} func;};
static struct MenuAction sStartMenuItems[20];
static u8 GetStartMenuWindowId(void){return 0;}
static void FillWindowPixelBuffer(u8 w,u8 color){}
static void FillWindowPixelRect(u8 w,u8 color,u32 x,u32 y,u32 a,u32 b){assert(x+a<=96&&y+b<=144);}
static void StringExpandPlaceholders(u8 *d,const char *s){strcpy((char*)d,s);}
static void PrintPlayerNameOnWindow(u8 w,const char *s,u32 x,u32 y){assert(y+16<=144);}
static void AddTextPrinterParameterized(u8 w,u8 f,const u8 *text,u32 x,u32 y,u32 speed,void *cb){assert(y+16<=144&&x+strlen((const char*)text)*6<=96);}
static void CopyWindowToVram(u8 w,u8 flags){}
static u8 InitMenuNormal(u8 w,u8 f,u8 x,u8 y,u8 height,u8 count,u8 initial){assert(count>0&&count<=8&&initial<count);return initial;}
'''
main=r'''
int main(void){
for(int i=0;i<20;i++)sStartMenuItems[i].text="ADVENTURE LOG";
for(int mask=0;mask<16;mask++){
 for(int i=0;i<4;i++)flags[i]=(mask>>i)&1;
 for(int debug=0;debug<2;debug++){
  sNumStartMenuActions=0;sStartMenuTop=sStartMenuCursorPos=0;
  if(debug)BuildDebugStartMenu();else BuildNormalStartMenu();
  assert(sCurrentStartMenuActions[0]==MENU_ACTION_ADVENTURE);
  u8 seen[20]={0};int count=sNumStartMenuActions;
  for(int i=0;i<count;i++){seen[sCurrentStartMenuActions[sStartMenuCursorPos]]=1;MoveStartMenuCursor(1);}
  assert(sStartMenuCursorPos==0);
  for(int i=0;i<count;i++)assert(seen[sCurrentStartMenuActions[i]]);
  MoveStartMenuCursor(-1);assert(sStartMenuCursorPos==count-1);
  MoveStartMenuCursor(1);assert(sStartMenuCursorPos==0);
 }
}
puts("Pause menu builders, wrapping, scrolling and pixel bounds passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'menu.c').write_text(preamble+enum+code+main)
 subprocess.run(['cc','-std=gnu99','-Wall','-Wextra','-Wno-unused-function','-Wno-unused-parameter','-Werror',str(p/'menu.c'),'-o',str(p/'menu')],check=True)
 subprocess.run([str(p/'menu')],check=True)
# Menu, day panel and standard text windows have disjoint tile allocations.
assert '0, 17, 1, 12, (numActions * 2) + 2, 15, 0x139' in (R/'src/menu.c').read_text()
assert 0x139+12*18<=0x214
