"""Exercise the actual notebook renderer/navigation and native font bounds."""
from pathlib import Path
import subprocess,tempfile,json,re
R=Path(__file__).resolve().parents[1]
ns={'__file__':str(R/'test/legends-adventure.test.py')}
exec((R/'test/legends-adventure.test.py').read_text().split('with tempfile.TemporaryDirectory()')[0],ns)
backend=ns['preamble']+ns['source']
ui='\n'.join(l for l in (R/'src/legends_adventure_ui.c').read_text().splitlines() if not l.startswith('#include'))
charmap={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)};charmap["'"]=0xB4
fonts=(R/'src/fonts.c').read_text();widths=[]
for f in ('Small','Normal'):
 w=list(map(int,re.findall(r'\d+',fonts.split('gFont'+f+'LatinGlyphWidths[] = {')[1].split('};')[0])))
 widths.append([w[charmap[chr(i)]] if chr(i) in charmap else 0 for i in range(128)])
stubs=r'''
#define COMPOUND_STRING(x) ((const u8 *)(x))
#define FONT_SMALL 0
#define FONT_NORMAL 1
#define TEXT_SKIP_DRAW 0
#define COPYWIN_FULL 3
#define EOS 0
#define CHAR_NEWLINE '\n'
#define STR_CONV_MODE_LEADING_ZEROS 1
#define STR_CONV_MODE_LEFT_ALIGN 0
#define PIXEL_FILL(x) ((x)|((x)<<4))
#define RGB(r,g,b) ((r)|((g)<<5)|((b)<<10))
#define RGB_BLACK 0
#define PALETTES_ALL 0xFFFFFFFF
#define BG_COORD_SET 0
#define DISPCNT_MODE_0 0
#define DISPCNT_BG0_ON 256
#define SE_SELECT 1
#define min(a,b) ((a)<(b)?(a):(b))
#define A_BUTTON 1
#define B_BUTTON 2
#define SELECT_BUTTON 4
#define START_BUTTON 8
#define DPAD_RIGHT 16
#define DPAD_LEFT 32
#define DPAD_UP 64
#define DPAD_DOWN 128
#define R_BUTTON 256
#define L_BUTTON 512
#define JOY_NEW(keys) (gMain.newKeys & (keys))
struct BgTemplate {int bg,charBaseIndex,mapBaseIndex,priority;};
struct WindowTemplate {int bg,tilemapLeft,tilemapTop,width,height,paletteNum,baseBlock;};
#define DUMMY_WIN_TEMPLATE {0}
struct {u8 state;u16 newKeys;} gMain;
struct {bool8 active;} gPaletteFade;
struct Task {void (*func)(u8);} gTasks[1];
static void (*currentCallback)(void);
static int freed,failedInit;
static u8 paper[160][240];
struct Op {u8 font,x,y;char text[256];};
static struct Op ops[32];static int opCount;
void SetMainCallback2(void (*cb)(void)){currentCallback=cb;gMain.state=0;}
void SetVBlankCallback(void (*cb)(void)){}
void CB2_ReturnToFieldWithOpenMenu(void){}
void LoadOam(void){} void ProcessSpriteCopyRequests(void){} void TransferPlttBuffer(void){}
void RunTasks(void){} void UpdatePaletteFade(void){}
void SetGpuReg(int reg,int value){} void ResetBgsAndClearDma3BusyFlags(int value){}
void InitBgsFromTemplates(int a,const struct BgTemplate *t,int count){}
void ChangeBgX(int a,int b,int c){} void ChangeBgY(int a,int b,int c){}
void ResetTasks(void){} void ResetSpriteData(void){} void ResetPaletteFade(void){} void ScanlineEffect_Stop(void){}
bool32 InitWindowsUnchecked(const struct WindowTemplate *t){assert(t->width*8==240&&t->height*8==160);assert(t->baseBlock+t->width*t->height<1024);return !failedInit;}
void DeactivateAllTextPrinters(void){} void LoadPalette(const u16 *p,int offset,int bytes){assert(offset==240&&bytes==32);}
void PutWindowTilemap(int window){} void ShowBg(int bg){} void CopyWindowToVram(int w,int flags){}
void BeginNormalPaletteFade(u32 a,int b,int c,int d,int e){}
u8 CreateTask(void (*func)(u8),int priority){gTasks[0].func=func;return 0;}
void DestroyTask(u8 id){} void FreeAllWindowBuffers(void){freed++;} void PlaySE(int se){}
u8 *StringCopy(u8 *dst,const u8 *src){return (u8*)strcpy((char*)dst,(const char*)src);}
u8 *StringAppend(u8 *dst,const u8 *src){return (u8*)strcat((char*)dst,(const char*)src);}
u16 StringLength(const u8 *s){return strlen((const char*)s);}
u8 *ConvertIntToDecimalStringN(u8 *dst,u32 value,int mode,int digits){if(mode)sprintf((char*)dst,"%0*u",digits,value);else sprintf((char*)dst,"%u",value);return dst;}
u8 *GetMapName(u8 *dst,u16 map,int pad){return StringCopy(dst,(const u8*)"VERMILION CITY");}
const u8 *GetSpeciesName(u16 species){return (const u8*)"EEVEE";}
int GetStringWidth(int font,const u8 *text,int spacing){int line=0,maxw=0;for(;*text;text++){if(*text=='\n'){if(line>maxw)maxw=line;line=0;}else line+=fontWidths[font][*text];}return line>maxw?line:maxw;}
void FillWindowPixelBuffer(int w,u8 color){memset(paper,color&15,sizeof(paper));opCount=0;}
void FillWindowPixelRect(int w,u8 color,int x,int y,int width,int height){assert(x>=0&&y>=0&&x+width<=240&&y+height<=160);for(int j=y;j<y+height;j++)for(int i=x;i<x+width;i++)paper[j][i]=color&15;}
void AddTextPrinterParameterized3(int w,int font,int x,int y,const u8 *color,int speed,const u8 *text){
 assert(x+GetStringWidth(font,text,0)<=240);int lines=1;for(const u8 *c=text;*c;c++)if(*c=='\n')lines++;
 assert(y+((lines-1)*16)+(font==FONT_SMALL?12:16)<=160);
 assert(opCount<32);ops[opCount]=(struct Op){font,x,y,{0}};strcpy(ops[opCount++].text,(const char*)text);
}
'''
registers='\n'.join('#define '+name+' '+str(i) for i,name in enumerate(sorted(set(re.findall(r'REG_OFFSET_\w+',ui)))))
fontdef='static const int fontWidths[2][128]='+json.dumps(widths).replace('[','{').replace(']','}')+';\n'
main=r'''
static void key(u16 keys){gMain.newKeys=keys;Task_Read(0);gMain.newKeys=0;}
static void reset(void){memset(&block3,0,sizeof(block3));date=100;clockInfo=(struct SiiRtcInfo){0x26,0x10,0x10};invalid=linked=0;LegendsAdventureInit(TRUE);}
int main(int argc,char **argv){
reset();LegendsAdventureFlagSet(FLAG_SYS_POKEDEX_GET);LegendsAdventureCatch(25,7);
date=101;clockInfo.day=0x11;block2.playTimeHours=7;LegendsAdventureUpdateDay();LegendsAdventureCatch(133,18);LegendsAdventureFlagSet(FLAG_LEGENDS_KANTO_SURGE_WON);
CB2_OpenAdventureLog();assert(gTasks[0].func==Task_Read&&sPage==0&&sFilter==ADV_FILTER_ALL);
// Dump commands and paper for native-font visual QA before navigation changes.
FILE *f=fopen(argv[1],"wb");fwrite(paper,1,sizeof(paper),f);fclose(f);
printf("[");for(int i=0;i<opCount;i++){if(i)printf(",");printf("[%d,%d,%d,\"",ops[i].font,ops[i].x,ops[i].y);for(char *c=ops[i].text;*c;c++){if(*c=='\n')printf("\\n");else if(*c=='\"')printf("\\\"");else putchar(*c);}printf("\"]");}printf("]\n");
gPaletteFade.active=1;key(DPAD_LEFT);assert(sPage==0);gPaletteFade.active=0;
key(DPAD_LEFT);assert(sPage==1);key(DPAD_RIGHT);assert(sPage==0);
key(DPAD_UP);assert(sFilter==ADV_FILTER_DAY&&sDay==1&&sPage==0);key(DPAD_DOWN);assert(sDay==2);
key(SELECT_BUTTON);assert(sFilter==ADV_FILTER_STORY);key(SELECT_BUTTON);assert(sFilter==ADV_FILTER_ALL);
for(int i=0;i<50;i++){key(L_BUTTON);}
assert(sPage==LegendsAdventureCount(ADV_FILTER_ALL,0)-1);
for(int i=0;i<50;i++){key(R_BUTTON);}
assert(sPage==0);
key(L_BUTTON);key(A_BUTTON);assert(sPage==0);
key(B_BUTTON);assert(gTasks[0].func==Task_Close);gPaletteFade.active=1;Task_Close(0);assert(freed==0);gPaletteFade.active=0;Task_Close(0);assert(freed==1&&currentCallback==CB2_ReturnToFieldWithOpenMenu);
// Empty day/story filters and allocation failure always return safely.
reset();sFilter=ADV_FILTER_STORY;sPage=0;DrawPage();assert(strstr(ops[2].text,"No notes"));
failedInit=1;gMain.state=0;CB2_OpenAdventureLog();assert(freed==2&&currentCallback==CB2_ReturnToFieldWithOpenMenu);
return 0;
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'ui.c').write_text(backend+fontdef+registers+'\n'+stubs+ui+main)
 subprocess.run(['cc','-std=gnu99','-Wall','-Wextra','-Wno-unused-parameter','-Wno-unused-function','-Werror','-iquote',str(R/'include'),str(p/'ui.c'),'-o',str(p/'ui')],check=True)
 result=subprocess.run([str(p/'ui'),str(p/'paper.raw')],check=True,capture_output=True,text=True)
 # Optional local-only native font preview; the tests themselves need no Pillow.
 import os
 if os.environ.get('LEGENDS_ADVENTURE_PREVIEW'):
  from PIL import Image
  colors=[]
  for r,g,b in [(18,15,21),(31,29,24),(8,7,10),(26,23,21),(28,25,23),(24,18,18),(23,20,28),(30,27,30),(15,12,18),(31,30,27)]:colors.append(tuple(round(v*255/31) for v in (r,g,b)))
  canvas=Image.new('RGB',(240,160));raw=(p/'paper.raw').read_bytes()
  for y in range(160):
   for x in range(240):canvas.putpixel((x,y),colors[raw[y*240+x]])
  sheets=[Image.open(R/'graphics/fonts/latin_small.png'),Image.open(R/'graphics/fonts/latin_normal.png')]
  for font,x,y,text in json.loads(result.stdout):
   xx=x;yy=y
   for c in text:
    if c=='\n':xx=x;yy+=16;continue
    code=charmap[c];glyph=sheets[font].crop(((code%16)*16,(code//16)*16,(code%16+1)*16,(code//16+1)*16))
    for gy in range(16):
     for gx in range(widths[font][ord(c)]):
      pixel=glyph.getpixel((gx,gy))
      if pixel in (1,2) and yy+gy<160:canvas.putpixel((xx+gx,yy+gy),colors[2 if pixel==1 else 3])
    xx+=widths[font][ord(c)]
  canvas.resize((720,480),Image.Resampling.NEAREST).save(os.environ['LEGENDS_ADVENTURE_PREVIEW'])
print('Notebook input, lifecycle, empty filters, native font and pixel bounds passed.')
