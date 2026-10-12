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
#define LEGENDS_HAIR_COLOR_COUNT 8
#define INTRO_HAIR_VISIBLE 5
#define PIXEL_FILL(x) (x)
#define FONT_SMALL 0
#define FONT_NORMAL 1
#define TEXT_SKIP_DRAW 0
#define COPYWIN_FULL 3
#define COMPOUND_STRING(x) ((const u8 *)(x))
#define SE_SELECT 0
struct {u8 playerGender;} save2,*gSaveBlock2Ptr=&save2;
struct Task {void(*func)(u8);}gTasks[1];
static u8 sAppearanceStage=1,sAppearanceLastChoice,sAppearanceHairTop;
static int keys,hair,color,preview,clear,hidden,top,selected,busy;
u8 LegendsGetHair(void){return hair;}
void LegendsSetHairSelection(u8 n){assert(n<11);hair=n;}
void FillWindowPixelBuffer(int w,int c){}
u8 LegendsGetHairColor(void){return color;}
void LegendsSetHairColorSelection(u8 n){assert(n<8);color=n;}
static const u8 labels[11]={0,1,2,3,4,5,6,7,8,9,10};
const u8 *LegendsGetHairName(int gender,u8 h){assert(gender==save2.playerGender&&h<11);return labels+h;}
const u8 *LegendsGetHairColorName(u8 c){assert(c<8);return labels+c;}
void InitMenuInUpperLeftCornerNormal(int w,int count,int cursor){assert(count==5&&cursor>=0&&cursor<5);selected=top+cursor;}
void AddTextPrinterParameterized(int w,int f,const u8*t,int x,int y,int sp,void*c){if(x==8){assert(f==FONT_NORMAL&&y>=1&&y<=65);if(y==1)top=*t;}else assert(x==80&&(y==0||y==64));}
void PutWindowTilemap(int w){}
void CopyWindowToVram(int w,int mode){}
void PlaySE(int id){}
void NewGameBirchSpeech_RefreshAppearance(u8 id){preview++;}
int RunTextPrintersAndIsPrinter0Active(void){return busy;}
int Menu_ProcessInputNoWrap(void){return keys&A_BUTTON?0:keys&B_BUTTON?MENU_B_PRESSED:MENU_NOTHING_CHOSEN;}
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
 // Color has its own bounded viewport and retains its choice on B.
 sAppearanceStage=2;sAppearanceHairTop=0;NewGameBirchSpeech_DrawHairList();assert(selected==0&&top==0);
 keys=DPAD_DOWN;for(int i=1;i<8;i++){Task_NewGameBirchSpeech_ChooseAppearance(0);assert(color==i&&selected==i&&top==(i<5?0:i-4));}
 Task_NewGameBirchSpeech_ChooseAppearance(0);assert(color==7);
 keys=B_BUTTON;Task_NewGameBirchSpeech_ChooseAppearance(0);assert(sAppearanceStage==1&&color==7&&!hidden);
 keys=A_BUTTON;Task_NewGameBirchSpeech_ChooseAppearance(0);assert(sAppearanceStage==2);
 sAppearanceHairTop=0;NewGameBirchSpeech_DrawHairList();assert(selected==7&&top==3);
 Task_NewGameBirchSpeech_ChooseAppearance(0);assert(sAppearanceStage==3);
 keys=B_BUTTON;Task_NewGameBirchSpeech_ChooseAppearance(0);assert(sAppearanceStage==2&&color==7);
 keys=A_BUTTON;Task_NewGameBirchSpeech_ChooseAppearance(0);Task_NewGameBirchSpeech_ChooseAppearance(0);assert(hidden==1&&gTasks[0].func==Task_NewGameBirchSpeech_WhatsYourName);
 for(int g=0;g<2;g++){save2.playerGender=g;sAppearanceStage=1;sAppearanceHairTop=0;NewGameBirchSpeech_DrawHairList();}
 puts("Intro: gender-specific hairstyles, colors, viewport bounds, live previews, A/B and restored choices passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'test.c';p.write_text(pre+function('NewGameBirchSpeech_DrawHairList')+function('Task_NewGameBirchSpeech_ChooseAppearance')+main)
 subprocess.run(['cc','-Wall','-Wno-unused-parameter','-Werror',str(p),'-o',str(p.with_suffix(''))],check=True)
 subprocess.run([str(p.with_suffix(''))],check=True)
