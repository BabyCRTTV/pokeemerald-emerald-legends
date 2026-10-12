"""Exercise the actual intro callback: every row, viewport, preview, A/B and re-entry."""
from pathlib import Path
import re, subprocess, tempfile
root=Path(__file__).resolve().parents[1]
s=(root/'src/main_menu.c').read_text()
def function(name):
 m=re.search(r'static void '+name+r'\([^;]*?\)\n\{',s);start=m.start();pos=m.end();depth=1
 while depth:
  if s[pos]=='{':depth+=1
  if s[pos]=='}':depth-=1
  pos+=1
 return s[start:pos]
pre=r'''
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;typedef int8_t s8;
#define TRUE 1
#define DPAD_UP 1
#define DPAD_DOWN 2
#define DPAD_LEFT 4
#define DPAD_RIGHT 8
#define A_BUTTON 16
#define B_BUTTON 32
#define JOY_NEW(x) (keys&(x))
#define JOY_REPEAT(x) (keys&(x))
#define MENU_B_PRESSED -1
#define MENU_NOTHING_CHOSEN -2
#define LEGENDS_HAIR_COUNT 11
#define INTRO_HAIR_VISIBLE 5
#define PIXEL_FILL(x) (x)
#define FONT_SMALL 0
#define TEXT_SKIP_DRAW 0
#define COPYWIN_FULL 3
#define COMPOUND_STRING(x) ((const u8 *)(x))
#define SE_SELECT 0
struct MenuAction {int dummy;}sHairChoices[11];
struct Task {void(*func)(u8);}gTasks[1];
static u8 sAppearanceStage=1,sAppearanceLastChoice,sAppearanceHairTop;
static int keys,hair,preview,clear,hidden,top,selected,busy;
u8 LegendsGetHair(void){return hair;}
void LegendsSetHairSelection(u8 n){assert(n<11);hair=n;}
void FillWindowPixelBuffer(int w,int c){}
void PrintMenuTable(int w,int count,const struct MenuAction *p){assert(count==5);top=p-sHairChoices;assert(top>=0&&top+count<=11);}
void InitMenuInUpperLeftCornerNormal(int w,int count,int cursor){assert(count==5&&cursor>=0&&cursor<5);selected=top+cursor;}
void AddTextPrinterParameterized(int w,int f,const u8*t,int x,int y,int sp,void*c){assert(x==80&&(y==0||y==64));}
void PutWindowTilemap(int w){}
void CopyWindowToVram(int w,int mode){}
void PlaySE(int id){}
void NewGameBirchSpeech_RefreshAppearance(u8 id){preview++;}
int RunTextPrintersAndIsPrinter0Active(void){return busy;}
int Menu_ProcessInputNoWrap(void){return MENU_NOTHING_CHOSEN;}
u8 Menu_GetCursorPos(void){return 0;}
u8 LegendsGetSkinTone(void){return 0;}
u8 LegendsGetOutfit(void){return 0;}
void LegendsSetAppearanceSelection(u8 a,u8 b){}
void NewGameBirchSpeech_ClearGenderWindow(int a,int b){clear++;}
void NewGameBirchSpeech_HideAppearancePreview(u8 id){hidden++;}
static void Task_NewGameBirchSpeech_ShowAppearance(u8 id){}
static void Task_NewGameBirchSpeech_WhatsYourName(u8 id){}
static void Task_NewGameBirchSpeech_BoyOrGirl(u8 id){}
'''
main=r'''
int main(void){
 NewGameBirchSpeech_DrawHairList();assert(selected==0&&top==0);
 keys=DPAD_RIGHT;Task_NewGameBirchSpeech_ChooseAppearance(0);assert(hair==0&&preview==0);
 busy=1;keys=DPAD_DOWN;Task_NewGameBirchSpeech_ChooseAppearance(0);assert(hair==0);busy=0;
 for(int i=1;i<11;i++){Task_NewGameBirchSpeech_ChooseAppearance(0);assert(hair==i&&selected==i&&top==(i<5?0:i-4));}
 assert(preview==10);Task_NewGameBirchSpeech_ChooseAppearance(0);assert(hair==10&&preview==10);
 keys=A_BUTTON;Task_NewGameBirchSpeech_ChooseAppearance(0);assert(sAppearanceStage==2&&clear==1&&!hidden&&gTasks[0].func==Task_NewGameBirchSpeech_ShowAppearance);
 sAppearanceStage=1;sAppearanceHairTop=0;NewGameBirchSpeech_DrawHairList();assert(selected==10&&top==6);
 keys=DPAD_UP;for(int i=9;i>=0;i--){Task_NewGameBirchSpeech_ChooseAppearance(0);assert(hair==i&&selected==i);}
 Task_NewGameBirchSpeech_ChooseAppearance(0);assert(hair==0&&preview==20&&top==0);
 keys=B_BUTTON;Task_NewGameBirchSpeech_ChooseAppearance(0);assert(sAppearanceStage==0&&clear==2&&!hidden);
 puts("Intro hair: all 11 rows, viewport bounds, held keys, live previews, A/B and restored selection passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(pre+function('NewGameBirchSpeech_DrawHairList')+function('Task_NewGameBirchSpeech_ChooseAppearance')+main)
 subprocess.run(['cc','-Wall','-Wno-unused-parameter','-Werror',str(p),'-o',str(p.with_suffix(''))],check=True)
 subprocess.run([str(p.with_suffix(''))],check=True)
