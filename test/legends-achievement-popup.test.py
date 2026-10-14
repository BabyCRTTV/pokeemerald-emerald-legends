"""Compile real nonblocking achievement field notice lifecycle."""
from pathlib import Path
import subprocess,tempfile
R=Path(__file__).resolve().parents[1]
source='\n'.join(l for l in (R/'src/legends_achievement_popup.c').read_text().splitlines() if not l.startswith('#include'))
stubs=r'''
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;
#define EWRAM_DATA
#define TRUE 1
#define FALSE 0
#define WINDOW_NONE 255
#define FONT_SMALL 0
#define TEXT_SKIP_DRAW 0
#define COPYWIN_FULL 3
#define COPYWIN_MAP 1
#define COMPOUND_STRING(x) ((const u8*)(x))
#define PIXEL_FILL(x) ((x)|((x)<<4))
struct WindowTemplate{int bg,tilemapLeft,tilemapTop,width,height,paletteNum,baseBlock;};
void CB2_Overworld(void){}
struct{void(*callback2)(void);}gMain={CB2_Overworld};
struct{int active;}gPaletteFade;
static int locked,script,linked,unionRoom,mapPopup,fail,windows,cleared,shown,dismissed;
static u16 pending[3]={4,80,94};static int next;
struct A{const u8 *title;};static struct A achievement={(const u8*)"Thunderwing Witness"};
int ArePlayerFieldControlsLocked(void){return locked;}
int ScriptContext_IsEnabled(void){return script;}
int IsOverworldLinkActive(void){return linked;}
int InUnionRoom(void){return unionRoom;}
int IsMapNamePopupActive(void){return mapPopup;}
u16 LegendsAchievementNotice(void){return next<3?pending[next]:0xFFFF;}
void LegendsAchievementNoticeDismiss(u16 id){assert(id==pending[next++]);dismissed++;}
const struct A *LegendsAchievementGet(u16 id){return &achievement;}
u8 AddWindow(const struct WindowTemplate *t){assert(t->tilemapLeft==1&&t->tilemapTop==1&&t->baseBlock>=0x260&&t->baseBlock+t->width*t->height<1024);if(fail)return 255;assert(!windows);windows++;shown++;return 2;}
void RemoveWindow(u8 id){assert(id==2&&windows);windows--;}
void ClearWindowTilemap(u8 id){assert(id==2);cleared++;}
void FillWindowPixelBuffer(u8 id,int fill){assert(id==2);}
void FillWindowPixelRect(u8 id,int fill,int x,int y,int w,int h){assert(id==2&&x+w<=144&&y+h<=32);}
void AddTextPrinterParameterized3(u8 id,int font,int x,int y,const u8 *ink,int speed,const u8 *text){assert(id==2&&x==5&&y+12<=32);}
void PutWindowTilemap(u8 id){assert(id==2);}
void CopyWindowToVram(u8 id,int copy){assert(id==2);}
'''
main=r'''
int main(void){
 for(int gate=0;gate<7;gate++){
  int *gates[]={&locked,&script,&linked,&unionRoom,&mapPopup,&gPaletteFade.active,&fail};
  *gates[gate]=1;LegendsAchievementPopupUpdate();assert(!windows&&shown==0&&next==0);*gates[gate]=0;
 }
 LegendsAchievementPopupUpdate();assert(windows==1&&sNoticeFrames==180);
 for(int i=0;i<50;i++)LegendsAchievementPopupUpdate();
 locked=1;LegendsAchievementPopupUpdate();assert(!windows&&next==0);locked=0;
 LegendsAchievementPopupUpdate();assert(windows&&sNoticeFrames==180);
 for(int id=0;id<3;id++){
  for(int i=0;i<179;i++)LegendsAchievementPopupUpdate();assert(windows&&next==id);
  LegendsAchievementPopupUpdate();assert(!windows&&next==id+1);
  for(int i=0;i<20;i++)LegendsAchievementPopupUpdate();assert(!windows);
  LegendsAchievementPopupUpdate();assert(windows==(id<2));
 }
 assert(dismissed==3&&cleared==4);
 LegendsAchievementPopupHide();LegendsAchievementPopupHide();assert(!windows);
 puts("Field notices: deferred gates, allocation retry, interruption/resume, queued lifetimes and cleanup passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'popup.c').write_text(stubs+source+main)
 subprocess.run(['cc','-std=gnu11','-Wall','-Wextra','-Wno-unused-parameter','-Wno-misleading-indentation','-Werror',str(p/'popup.c'),'-o',str(p/'popup')],check=True)
 subprocess.run([str(p/'popup')],check=True)
