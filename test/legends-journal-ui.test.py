"""Exercise real journal drawing/input with catalogue titles and native font bounds."""
from pathlib import Path
import subprocess,tempfile,json,re
R=Path(__file__).resolve().parents[1]
ns={'__file__':str(R/'test/legends-journal.test.py')}
exec((R/'test/legends-journal.test.py').read_text().split('with tempfile.TemporaryDirectory()')[0],ns)
backend='#define sAchievements sAchievementCatalogue\n'+ns['preamble'].replace('typedef uint8_t u8;', 'typedef uint8_t u8; typedef uint8_t bool8;')+ns['s']+'\n#undef sAchievements\n'
ui='\n'.join(l for l in (R/'src/legends_journal_ui.c').read_text().splitlines() if not l.startswith('#include'))
charmap={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)};charmap["'"]=0xB4
fonts=(R/'src/fonts.c').read_text();widths=[]
for f in ('Small','Normal'):
 w=list(map(int,re.findall(r'\d+',fonts.split('gFont'+f+'LatinGlyphWidths[] = {')[1].split('};')[0])))
 widths.append([w[charmap[chr(i)]] if chr(i) in charmap else 0 for i in range(128)])
stubs=r'''
#define EWRAM_DATA
#define COMPOUND_STRING(x) ((const u8 *)(x))
#define FONT_SMALL 0
#define FONT_NORMAL 1
#define TEXT_SKIP_DRAW 0
#define COPYWIN_FULL 3
#define EOS 0
#define CHAR_SPACE ' '
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
struct Op {u8 font,x,y;char text[256];u8 colors[3];};
static struct Op ops[64];static int opCount;
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
const u8 *GetItemName(u16 item){return (const u8*)"CHERI BERRY";}
const u8 *GetSpeciesName(u16 species){return (const u8*)"EEVEE";}
int GetStringWidth(int font,const u8 *text,int spacing){int line=0,maxw=0;for(;*text;text++){if(*text=='\n'){if(line>maxw)maxw=line;line=0;}else line+=fontWidths[font][*text];}return line>maxw?line:maxw;}
void FillWindowPixelBuffer(int w,u8 color){memset(paper,color&15,sizeof(paper));opCount=0;}
void FillWindowPixelRect(int w,u8 color,int x,int y,int width,int height){assert(x>=0&&y>=0&&x+width<=240&&y+height<=160);for(int j=y;j<y+height;j++)for(int i=x;i<x+width;i++)paper[j][i]=color&15;}
void AddTextPrinterParameterized3(int w,int font,int x,int y,const u8 *color,int speed,const u8 *text){
 assert(x+GetStringWidth(font,text,0)<=240);int lines=1;for(const u8 *c=text;*c;c++)if(*c=='\n')lines++;
 assert(y+((lines-1)*16)+(font==FONT_SMALL?12:16)<=160);
 assert(opCount<64);ops[opCount]=(struct Op){font,x,y,{0},{color[0],color[1],color[2]}};strcpy(ops[opCount++].text,(const char*)text);
}
'''
registers='\n'.join('#define '+name+' '+str(i) for i,name in enumerate(sorted(set(re.findall(r'REG_OFFSET_\w+',ui)))))
fontdef='static const int fontWidths[2][128]='+json.dumps(widths).replace('[','{').replace(']','}')+';\n'
main=r'''
static void key(u16 keys){gMain.newKeys=keys;Task_Read(0);gMain.newKeys=0;}
static void selection(void){
 int titles=0, selected=0;
 for(int row=0;row<6 && sTop+row<Count();row++){
  int y=JOURNAL_ROW_Y+row*JOURNAL_ROW_HEIGHT, active=sTop+row==sSelected;
  int bg=active?8:(row&1?9:1);
  assert(paper[y+1][235]==bg);
  assert(paper[y+4][8]==bg);
  assert(paper[y+5][8]==(active?1:bg));
  // The pointer exists only on the selected row; it cannot look like a check.
  assert(paper[y+8][11]==(active?1:bg));
  assert(paper[y+5][11]==bg);
  assert(paper[y+6][14]==1); // Checkbox interior remains readable.
  for(int j=0;j<opCount;j++)if(ops[j].x==26&&ops[j].y==y){
   u16 id=Entry(sTop+row);
   assert(!strcmp(ops[j].text,(const char*)(sAchievements?LegendsAchievementGet(id)->title:LegendsQuestGet(id)->title)));
   assert(ops[j].colors[0]==bg);
   assert(ops[j].colors[1]==(active?1:2));
   selected+=active;titles++;
  }
 }
 assert(titles==min(6,Count()-sTop));assert(selected==(Count()!=0));
 int tabs=0, activeTabs=0;
 for(int j=0;j<opCount;j++){
  if(ops[j].y==24){tabs++;activeTabs+=ops[j].colors[0]==8;}
  if(ops[j].x==26)assert(ops[j].x+GetStringWidth(ops[j].font,(const u8*)ops[j].text,0)<=220);
 }
 assert(tabs==3&&activeTabs==1);
 assert(paper[132][235]==6);
 // Claimed markers use the same legible colors as their own title.
 for(int j=0;j<opCount;j++)if(ops[j].x==222){
  int row=(ops[j].y-JOURNAL_ROW_Y)/JOURNAL_ROW_HEIGHT;
  assert(sAchievements&&LegendsAchievementClaimed(Entry(sTop+row)));
  assert(ops[j].colors[0]==(sTop+row==sSelected?8:(row&1?9:1)));
 }
}
int main(void){
 LegendsJournalInit(TRUE);
 for(unsigned q=0;q<LegendsQuestCount();q++){
  const struct LegendsQuest *quest=LegendsQuestGet(q);
  for(unsigned i=0;i<quest->count;i++)flags[quest->steps[i].flag]=1;
 }
 CB2_OpenQuestLog();assert(gTasks[0].func==Task_Read);selection();
 assert(Count()>6);u16 count=Count();
 gPaletteFade.active=1;key(DPAD_DOWN);assert(sSelected==0);gPaletteFade.active=0;
 for(unsigned i=0;i<count*2;i++){selection();u16 before=Entry(sSelected);key(A_BUTTON);assert(sDetail&&Entry(sSelected)==before);key(B_BUTTON);assert(!sDetail&&Entry(sSelected)==before);selection();key(DPAD_DOWN);}
 assert(sSelected==0);key(DPAD_UP);assert(sSelected==count-1);selection();
 key(DPAD_DOWN);assert(sSelected==0&&sTop==0);selection();
 key(R_BUTTON);assert(sSelected==6&&sTop==1);selection();
 key(L_BUTTON);assert(sSelected==0&&sTop==0);selection();
 for(int filter=0;filter<3;filter++){key(DPAD_RIGHT);assert(sSelected==0&&sTop==0);selection();}
 key(DPAD_LEFT);assert(sFilter==2);key(SELECT_BUTTON);assert(sFilter==0);
 memset(flags,0,sizeof(flags));sFilter=1;Draw();assert(Count()==0);selection();key(A_BUTTON);assert(!sDetail);
 LegendsJournalInit(TRUE);gMain.state=0;CB2_OpenAchievements();assert(sAchievements&&Count()==95);selection();
 for(int i=0;i<95;i++){selection();key(DPAD_DOWN);}
 key(DPAD_RIGHT);assert(sFilter==1&&Count()==0);selection();
 flags[FLAG_BADGE01_GET]=1;LegendsJournalRefresh();Draw();assert(Count()>0);selection();
 key(A_BUTTON);assert(sDetail);full=1;key(A_BUTTON);assert(sMessage==2&&!LegendsAchievementClaimed(Entry(sSelected)));
 full=0;key(A_BUTTON);assert(sMessage==1&&sClaimFrames==180&&sFilter==0);
 for(int t=0;t<180;t++){key(0);}
 assert(sClaimFrames==0);u16 claimed=Entry(sSelected);assert(LegendsAchievementClaimed(claimed));
 key(B_BUTTON);selection();key(DPAD_RIGHT);key(DPAD_RIGHT);assert(sFilter==2&&Count()==1);selection();
 key(B_BUTTON);assert(gTasks[0].func==Task_Close);gPaletteFade.active=1;Task_Close(0);assert(freed==0);gPaletteFade.active=0;Task_Close(0);assert(freed==1&&currentCallback==CB2_ReturnToFieldWithOpenMenu);
 failedInit=1;gMain.state=0;CB2_OpenQuestLog();assert(freed==2&&currentCallback==CB2_ReturnToFieldWithOpenMenu);
 puts("Journal selection contrast, pointer, catalogue bounds, scrolling, filters, details and claims passed.");
}
'''

with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'ui.c').write_text(backend+fontdef+registers+'\n'+stubs+ui+main)
 subprocess.run(['cc','-std=gnu11','-Wall','-Wextra','-Wno-unused-parameter','-Wno-unused-function','-Wno-sign-compare','-Werror','-iquote',str(R/'include'),'-iquote',str(R),str(p/'ui.c'),'-o',str(p/'ui')],check=True)
 subprocess.run([str(p/'ui')],check=True)
