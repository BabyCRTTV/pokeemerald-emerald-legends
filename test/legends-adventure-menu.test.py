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
code+='\n'+function('BuildStartMenuActions','void','void')+'\n'+function('DrawStartMenuScrollHints','void','void')+'\n'+function('PrintStartMenuActions','bool32','s8 *pIndex, u32 count')+'\n'+function('MoveStartMenuCursor','void','s8 delta')
code+='\n'+function('ShowTrackedQuestReminder','void','void')
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
#define FONT_SMALL 0
#define COMPOUND_STRING(s) ((const u8 *)(s))
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
static int sJournalPage;
static u32 hintMinY, hintMaxY;
static unsigned restricted, reminderCalls;
static void LegendsShowTrackedQuestReminder(void){reminderCalls++;}
static bool32 IsOverworldLinkActive(void){return restricted&1;}
static bool32 InUnionRoom(void){return restricted&2;}
#define PYRAMID_LOCATION_NONE 0
#define DEBUG_OVERWORLD_MENU 0
#define DEBUG_OVERWORLD_IN_MENU 0
static bool32 GetSafariZoneFlag(void){return restricted&4;}
static bool32 InBattlePike(void){return restricted&8;}
static bool32 CurrentBattlePyramidLocation(void){return restricted&16;}
static bool32 InMultiPartnerRoom(void){return restricted&32;}
static void BuildLinkModeStartMenu(void){}
static void BuildUnionRoomStartMenu(void){}
static u8 GetStartMenuWindowId(void){return 0;}
static void FillWindowPixelBuffer(u8 w,u8 color){}
static void FillWindowPixelRect(u8 w,u8 color,u32 x,u32 y,u32 a,u32 b){
 assert(x+a<=96&&y+b<=min(sNumStartMenuActions,START_MENU_VISIBLE_ROWS)*16u+16u);
 if(x<90){if(y<hintMinY)hintMinY=y;if(y>hintMaxY)hintMaxY=y;}
}
static void StringExpandPlaceholders(u8 *d,const char *s){strcpy((char*)d,s);}
static void PrintPlayerNameOnWindow(u8 w,const char *s,u32 x,u32 y){assert(y+16<=144);}
static void AddTextPrinterParameterized(u8 w,u8 f,const u8 *text,u32 x,u32 y,u32 speed,void *cb){
 if(f==FONT_SMALL){assert(x==8&&y==min(sNumStartMenuActions,8)*16u+4);assert(!strcmp((const char*)text,sJournalPage?"LEFT/RIGHT 2/2":"LEFT/RIGHT 1/2"));hintMinY=y+3;hintMaxY=y+11;assert(y+12<=min(sNumStartMenuActions,8)*16u+16);}
 else assert(y+16<=144);
 assert(x+strlen((const char*)text)*6<=96);
}
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
// Each page has exactly its intended entries, including before any unlocks.
for(int mask=0;mask<16;mask++){
 for(int i=0;i<4;i++)flags[i]=(mask>>i)&1;
 sJournalPage=0;BuildStartMenuActions();
 int adventureCount=0;
 for(int i=0;i<sNumStartMenuActions;i++)adventureCount+=sCurrentStartMenuActions[i]==MENU_ACTION_ADVENTURE;
 assert(adventureCount==1&&sCurrentStartMenuActions[0]==MENU_ACTION_ADVENTURE);
 sJournalPage=1;BuildStartMenuActions();
 assert(sNumStartMenuActions==3);
 assert(sCurrentStartMenuActions[0]==MENU_ACTION_QUESTS);
 assert(sCurrentStartMenuActions[1]==MENU_ACTION_ACHIEVEMENTS);
 assert(sCurrentStartMenuActions[2]==MENU_ACTION_EXIT);
 sStartMenuTop=sStartMenuCursorPos=0;
 MoveStartMenuCursor(-1);assert(sStartMenuCursorPos==2);
 MoveStartMenuCursor(1);assert(sStartMenuCursorPos==0);
}
for(int rows=1;rows<=8;rows++)for(int page=0;page<2;page++){
 sNumStartMenuActions=rows;sStartMenuTop=0;sJournalPage=page;
 hintMinY=UINT32_MAX;hintMaxY=0;DrawStartMenuScrollHints();
 // EXIT's native glyph ink ends 12 pixels below its text origin.
 u32 exitInkBottom=(rows-1)*16+9+12;
 assert(hintMinY>exitInkBottom); // Small-font ink starts below the last action.
 assert(hintMaxY-hintMinY==8&&hintMaxY<rows*16u+16u);
}
for(unsigned mask=0;mask<64;mask++){
 restricted=mask;reminderCalls=0;ShowTrackedQuestReminder();assert(reminderCalls==(mask==0));
}
puts("Pause menu builders, scrolling, footer clearance, reminder exclusions and pixel bounds passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'menu.c').write_text(preamble+enum+code+main)
 subprocess.run(['cc','-std=gnu99','-Wall','-Wextra','-Wno-unused-function','-Wno-unused-parameter','-Werror',str(p/'menu.c'),'-o',str(p/'menu')],check=True)
 subprocess.run([str(p/'menu')],check=True)
# Menu, day panel and standard text windows have disjoint tile allocations.
assert '0, 17, 1, 12, (numActions * 2) + 2, 15, 0x139' in (R/'src/menu.c').read_text()
assert 0x139+12*18<=0x214

# Measure native footer ink, including the slash's extra top pixel and shadow.
from PIL import Image
chars={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)}
font=Image.open(R/'graphics/fonts/latin_small.png')
rows=[]
for char in 'LEFT/RIGHT 1/2':
 i=chars[char];glyph=font.crop((i%16*16,i//16*16,i%16*16+16,i//16*16+16))
 rows.extend(y for y in range(16) if any(v in (1,2) for v in glyph.crop((0,y,16,y+1)).getdata()))
assert min(rows)==3 and max(rows)==11
assert 4+min(rows)>5+1 and 4+max(rows)<16
