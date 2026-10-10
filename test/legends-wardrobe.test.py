"""Actual wardrobe UI input/lifecycle under native service mocks; furniture bounds."""
from pathlib import Path
import json,struct,subprocess,tempfile
root=Path(__file__).resolve().parents[1]
source='\n'.join(x for x in (root/'src/legends_wardrobe.c').read_text().splitlines() if not x.startswith('#include'))
pre=r'''
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;typedef int bool8;
#define ARRAY_COUNT(x) (sizeof(x)/sizeof((x)[0]))
#define TRUE 1
#define FALSE 0
#define COMPOUND_STRING(x) ((const u8 *)(x))
#define DUMMY_WIN_TEMPLATE {.bg=255}
#define FONT_SMALL 0
#define TEXT_SKIP_DRAW 0
#define COPYWIN_FULL 3
#define PIXEL_FILL(x) (x)
#define BG_COORD_SET 0
#define BG_PLTT_ID(x) ((x)*16)
#define PLTT_SIZE_4BPP 32
#define STD_WINDOW_BASE_TILE_NUM 0x214
#define STD_WINDOW_PALETTE_NUM 14
#define RGB(r,g,b) ((r)|((g)<<5)|((b)<<10))
#define RGB_BLACK 0
#define PALETTES_ALL 0xffffffff
#define REG_OFFSET_DISPCNT 0
#define REG_OFFSET_BLDCNT 1
#define REG_OFFSET_BLDY 2
#define DISPCNT_OBJ_ON 1
#define DISPCNT_OBJ_1D_MAP 2
#define VRAM 0
#define VRAM_SIZE 1
#define OAM 0
#define OAM_SIZE 1
#define DmaClearLarge16(a,b,c,d) ((void)0)
#define DmaClear32(a,b,c) ((void)0)
#define MAP_GROUP(x) ((x)>>8)
#define MAP_NUM(x) ((x)&255)
#define MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F 0x101
#define MAP_LITTLEROOT_TOWN_MAYS_HOUSE_2F 0x102
#define FEMALE 1
#define VAR_CURRENT_SECRET_BASE 0
#define METATILE_SecretBase_LegendsWardrobe_Top 0x344
#define METATILE_SecretBase_LegendsWardrobe_Bottom 0x345
#define LEGENDS_OUTFIT_COUNT 5
#define LEGENDS_SCARF_COUNT 6
#define LEGENDS_COSTUME_COUNT 3
#define LEGENDS_SHOE_COUNT 8
#define LEGENDS_CARD_COLOR_COUNT 8
#define A_BUTTON 1
#define B_BUTTON 2
#define DPAD_LEFT 4
#define DPAD_RIGHT 8
#define DPAD_UP 16
#define DPAD_DOWN 32
#define JOY_NEW(x) (keys&(x))
struct BgTemplate {u8 bg,charBaseIndex,mapBaseIndex,priority;};
struct WindowTemplate {u8 bg,tilemapLeft,tilemapTop,width,height,paletteNum;u16 baseBlock;};
struct Task{void(*func)(u8);int data[16];}gTasks[16];
struct {u8 active;}gPaletteFade;
struct {struct {u8 mapGroup,mapNum;}location;}save1,*gSaveBlock1Ptr=&save1;
struct {u8 playerGender;}save2,*gSaveBlock2Ptr=&save2;
const u16 gStandardMenuPalette[16]={0};
static int keys,base,baseIndex,outfit,scarf,jacket,costume,shoes,card,pending,applies,cancels,freed,returns,resumes,pics,initFail,fieldCleanup;
u16 VarGet(int v){return baseIndex;}
int CurMapIsSecretBase(void){return base;}
void LegendsBeginWardrobeSelection(void){pending=1;}
void LegendsClearAppearanceSelection(void){cancels++;pending=0;}
void LegendsApplyWardrobeSelection(void){applies++;pending=0;}
u8 LegendsGetSkinTone(void){return 2;}
u8 LegendsGetOutfit(void){return outfit;}
u8 LegendsGetCostume(void){return costume;}
void LegendsSetCostumeSelection(u8 c){costume=c;}
u8 LegendsGetShoes(void){return shoes;}
u8 LegendsGetCardColor(void){return card;}
u16 LegendsCardSwatch(void){return card;}
void LegendsSetShoeSelection(u8 s){shoes=s;}
void LegendsSetCardColorSelection(u8 c){card=c;}
u8 LegendsGetScarf(void){return scarf;}
bool8 LegendsGetJacket(void){return jacket;}
void LegendsSetAppearanceSelection(u8 s,u8 o){assert(s==2);outfit=o;}
void LegendsSetAccessorySelection(u8 s,bool8 j){scarf=s;jacket=j;}
u16 LegendsGetPlayerTrainerPic(int g){return 200+g;}
void AddTextPrinterParameterized(int w,int f,const u8*t,int x,int y,int speed,void*cb){assert(x>=0&&y>=0);}
void FillWindowPixelBuffer(int w,int f){}
void FillWindowPixelRect(int w,int f,int x,int y,int width,int height){assert(w==3&&width==64);}
void CopyWindowToVram(int w,int m){}
int CreateTrainerCardTrainerPicSprite(int pic,int front,int x,int y,int pal,int win){assert(win==2&&pal==8);pics++;return 0;}
void RunTasks(void){}void AnimateSprites(void){}void BuildOamBuffer(void){}void UpdatePaletteFade(void){}
void LoadOam(void){}void ProcessSpriteCopyRequests(void){}void TransferPlttBuffer(void){}
void SetVBlankCallback(void(*f)(void)){}
void FreeAllWindowBuffers(void){freed++;}
void CleanupOverworldWindowsAndTilemaps(void){fieldCleanup++;}
void DestroyTask(int t){}
void CB2_ReturnToFieldContinueScriptPlayMapMusic(void){returns++;}
void SetMainCallback2(void(*cb)(void)){if(cb==CB2_ReturnToFieldContinueScriptPlayMapMusic)returns++;}
void BeginNormalPaletteFade(unsigned mask,int delay,int start,int end,int color){}
void SetGpuReg(int a,int b){}void ResetBgsAndClearDma3BusyFlags(int b){}
void InitBgsFromTemplates(int a,const struct BgTemplate*t,int n){assert(n==1);}
void ChangeBgX(int a,int b,int c){}void ChangeBgY(int a,int b,int c){}
void ResetPaletteFade(void){}void ScanlineEffect_Stop(void){}
void ResetTasks(void){memset(gTasks,0,sizeof(gTasks));}void ResetSpriteData(void){}
int InitWindowsUnchecked(const struct WindowTemplate *w){assert(w[4].bg==255);return !initFail;}
void DeactivateAllTextPrinters(void){}void LoadPalette(const u16*p,int off,int n){}
void LoadUserWindowBorderGfx(int win,int tile,int pal){assert(tile==STD_WINDOW_BASE_TILE_NUM&&pal==14*16);}
void PutWindowTilemap(int w){}void DrawStdWindowFrame(int w,int v){}void ShowBg(int b){}
u8 CreateTask(void(*f)(u8),int prio){gTasks[0].func=f;return 0;}
void ScriptContext_Enable(void){resumes++;}
'''
main=r'''
int main(void){
 save1.location.mapGroup=1;save1.location.mapNum=1;assert(LegendsCanUseWardrobe());
 save2.playerGender=1;assert(!LegendsCanUseWardrobe());save1.location.mapNum=2;assert(LegendsCanUseWardrobe());
 save1.location.mapGroup=3;assert(!LegendsCanUseWardrobe());
 base=1;baseIndex=0;assert(LegendsCanUseWardrobe());baseIndex=1;assert(!LegendsCanUseWardrobe());
 assert(LegendsIsWardrobeMetatile(0x344)&&LegendsIsWardrobeMetatile(0x345)&&!LegendsIsWardrobeMetatile(0x2f4));
 LegendsOpenWardrobe();assert(resumes==1&&!pending);baseIndex=0;
 LegendsOpenWardrobe();assert(pending&&gTasks[0].func==Task_Enter);Task_Enter(0);CB2_InitWardrobe();
 assert(pics==1&&fieldCleanup==1&&gTasks[0].func==Task_Input);
 keys=DPAD_LEFT;Task_Input(0);assert(outfit==4);keys=DPAD_RIGHT;Task_Input(0);assert(outfit==0);
 keys=DPAD_DOWN;Task_Input(0);keys=DPAD_LEFT;Task_Input(0);assert(costume==2);
 keys=DPAD_DOWN;Task_Input(0);keys=DPAD_LEFT;Task_Input(0);assert(scarf==0);
 keys=DPAD_UP;Task_Input(0);keys=DPAD_RIGHT;Task_Input(0);assert(costume==0);
 keys=DPAD_DOWN;Task_Input(0);keys=DPAD_LEFT;Task_Input(0);assert(scarf==5);
 keys=DPAD_DOWN;Task_Input(0);keys=A_BUTTON;Task_Input(0);assert(jacket==1);
 keys=DPAD_DOWN;Task_Input(0);keys=DPAD_LEFT;Task_Input(0);assert(shoes==7);
 keys=DPAD_DOWN;Task_Input(0);keys=DPAD_LEFT;Task_Input(0);assert(card==7);
 keys=DPAD_DOWN;Task_Input(0);assert(gTasks[0].data[0]==6&&gTasks[0].data[1]==1);
 keys=DPAD_DOWN;Task_Input(0);assert(gTasks[0].data[0]==7&&gTasks[0].data[1]==2);
 keys=DPAD_DOWN;Task_Input(0);assert(!gTasks[0].data[0]&&!gTasks[0].data[1]);
 keys=DPAD_UP;Task_Input(0);assert(gTasks[0].data[0]==7&&gTasks[0].data[1]==2);
 keys=DPAD_UP;Task_Input(0);keys=A_BUTTON;Task_Input(0);assert(applies==1&&!pending&&gTasks[0].func==Task_Return);
 gPaletteFade.active=1;Task_Return(0);assert(!freed);gPaletteFade.active=0;Task_Return(0);assert(freed==1&&returns==1);
 LegendsOpenWardrobe();CB2_InitWardrobe();keys=B_BUTTON;Task_Input(0);assert(applies==1&&cancels==1&&!pending);
 LegendsOpenWardrobe();initFail=1;CB2_InitWardrobe();assert(cancels==2&&returns==2);
 puts("Wardrobe location guards, preview navigation, apply/cancel, frame bounds and return lifecycle passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'wardrobe.c').write_text(pre+source+main)
 subprocess.run(['cc','-std=gnu17','-Wall','-Werror','-o',str(p/'wardrobe'),str(p/'wardrobe.c')],check=True)
 subprocess.run([str(p/'wardrobe')],check=True)
# Native category, shop availability and pair placement without layout/ID changes.
for house,x in [('Brendans',1),('Mays',7)]:
 name='LittlerootTown_'+house+'House_2F';data=(root/'data/layouts'/name/'map.bin').read_bytes();assert len(data)==9*8*2
 for y,t in [(6,0x2c4)]:assert struct.unpack_from('<H',data,(y*9+x)*2)[0]==t|0xc00
 events=json.loads((root/'data/maps'/name/'map.json').read_text())['bg_events']
 assert sum(e['script']=='LegendsWardrobe_EventScript_Home' for e in events)==1
assert '.2byte DECOR_LEGENDS_WARDROBE' in (root/'data/maps/Route104_PrettyPetalFlowerShop/scripts.inc').read_text()

assert 'LegendsWardrobe_Text_Home' not in (root/'data/maps/LittlerootTown_BrendansHouse_2F/scripts.inc').read_text()

# Scroll indicators must use native encoded glyphs; ASCII caret is unsupported.
assert 'COMPOUND_STRING("{UP_ARROW}")' in source and 'COMPOUND_STRING("{DOWN_ARROW}")' in source
assert 'COMPOUND_STRING("^")' not in source
