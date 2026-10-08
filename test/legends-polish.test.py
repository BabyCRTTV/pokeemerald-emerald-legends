"""Actual-module checks for seasonal effects, temporary scuffs and printer colors."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
def function(path,signature):
 s=(root/path).read_text();start=s.index(signature+'\n{');a=s.index('{',start);i=a+1;depth=1
 while depth:
  depth+=(s[i]=='{')-(s[i]=='}');i+=1
 return s[start:i]
colors=function('src/legends_seasons.c','u16 LegendsSeasonVegetationColor(u16 color, u8 season)')+'\n'+function('src/legends_seasons.c','void LegendsApplyGrassPalette(u8 slot, const u16 *source)')
grass='\n'.join(l for l in (root/'src/legends_grass.c').read_text().splitlines() if not l.startswith('#include'))
printer=function('src/text.c','void RunTextPrinters(void)')
clear=function('src/main_menu.c','static void NewGameBirchSpeech_ClearWindow(u8 windowId)')
pre=r'''
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int16_t s16;typedef int32_t s32;typedef int bool32;
#define EWRAM_DATA
#define TRUE 1
#define FALSE 0
#define RGB(r,g,b) ((r)|((g)<<5)|((b)<<10))
enum {LEGENDS_SPRING,LEGENDS_SUMMER,LEGENDS_AUTUMN,LEGENDS_WINTER};
#define MAX_MAP_DATA_SIZE 10240
#define METATILE_General_TallGrass 13
struct Tileset {int n;};static const struct Tileset gTileset_General={1},other={2};
struct Layout {const struct Tileset *primaryTileset;};struct Layout layout={&gTileset_General};
struct {struct Layout *mapLayout;} gMapHeader={&layout};
struct {s32 width,height;} gBackupMapLayout={100,100};
static u8 season=LEGENDS_WINTER;static int seasonal=1,draws=0;static u32 tile=13;
static u16 gPlttBufferUnfaded[512];
bool32 LegendsMapHasSeasons(void){return seasonal;}
u8 LegendsGetActiveSeason(void){return season;}
u32 MapGridGetMetatileIdAt(s16 x,s16 y){return tile;}
void CurrentMapDrawMetatileAt(s16 x,s16 y){draws++;}
enum {RENDER_PRINT,RENDER_UPDATE,RENDER_FINISH,WINDOW_TEXT_PRINTER,SPRITE_TEXT_PRINTER,COPYWIN_GFX};
union TextColor {u32 asU32;};
struct TextPrinterTemplate {int type,windowId;union TextColor color;};
struct TextPrinter {int active,isInUse;struct TextPrinterTemplate printerTemplate;void (*callback)(struct TextPrinterTemplate*,u32);struct TextPrinter *nextPrinter;};
#define FONT_NORMAL 1
#define FONTATTR_COLOR_BACKGROUND 0
#define PIXEL_FILL(n) ((n) | ((n) << 4))
static u8 pixels[216*32];
u8 GetFontAttribute(u8 font,u8 attr){return 1;}
void FillWindowPixelBuffer(u8 window,u8 color){memset(pixels,color,sizeof(pixels));}
static struct TextPrinter *sFirstTextPrinter;static int gDisableTextPrinters,instant;static union TextColor glyph;static int rendered;
bool32 IsPlayerTextSpeedInstant(void){return instant;}
u32 GetPlayerTextSpeedModifier(void){return 1;}
u32 GetNumTextPrinters(void){return 2;}
void GenerateFontHalfRowLookupTable(union TextColor c){glyph=c;}
u32 RenderFont(struct TextPrinter *p){assert(glyph.asU32==p->printerTemplate.color.asU32);rendered++;return RENDER_FINISH;}
void CopyWindowToVram(int w,int mode){}
void FreeFinishedTextPrinters(void){}
'''
main=r'''
int main(void){
    memset(pixels,99,sizeof(pixels));NewGameBirchSpeech_ClearWindow(0);
    for(int i=0;i<sizeof(pixels);i++)assert(pixels[i]==0x11);
    const u16 native[16]={RGB(14,23,29),RGB(22,31,16),RGB(16,24,12),RGB(7,17,6),RGB(9,11,1),RGB(6,8,0),RGB(12,21,29),RGB(12,21,24),RGB(17,25,30),RGB(18,28,31),RGB(18,16,12),RGB(22,21,18),RGB(20,26,24),RGB(14,24,20),RGB(8,22,16),RGB(3,20,13)};
    for(season=0;season<4;season++){
        for(int i=0;i<512;i++)gPlttBufferUnfaded[i]=123;
        memcpy(gPlttBufferUnfaded+320,native,sizeof(native));
        LegendsApplyGrassPalette(4,native);
        assert(gPlttBufferUnfaded[320]==native[0]);
        for(int i=1;i<16;i++)assert(gPlttBufferUnfaded[320+i]==LegendsSeasonVegetationColor(native[i],season));
        LegendsApplyGrassPalette(4,native);
        for(int i=1;i<16;i++)assert(gPlttBufferUnfaded[320+i]==LegendsSeasonVegetationColor(native[i],season));
        for(int i=0;i<320;i++)assert(gPlttBufferUnfaded[i]==123);
        for(int i=336;i<512;i++)assert(gPlttBufferUnfaded[i]==123);
    }
    seasonal=0;LegendsApplyGrassPalette(4,native);assert(!memcmp(gPlttBufferUnfaded+320,native,sizeof(native)));
    LegendsApplyGrassPalette(255,native);seasonal=1;season=LEGENDS_WINTER;
    LegendsResetSnowGrass();assert(!LegendsSnowGrassCleared(7,7));LegendsStepSnowGrass(7,7);assert(LegendsSnowGrassCleared(7,7)&&draws==1&&tile==13);
    LegendsStepSnowGrass(7,7);assert(draws==1);assert(!LegendsSnowGrassCleared(8,7));
    LegendsStepSnowGrass(-1,7);LegendsStepSnowGrass(100,7);LegendsStepSnowGrass(7,100);assert(draws==1);
    season=LEGENDS_SUMMER;LegendsStepSnowGrass(9,9);assert(!LegendsSnowGrassCleared(9,9));season=LEGENDS_WINTER;
    tile=20;assert(!LegendsSnowGrassCleared(7,7));LegendsStepSnowGrass(9,9);tile=13;
    layout.primaryTileset=&other;LegendsStepSnowGrass(9,9);assert(!LegendsSnowGrassCleared(9,9));layout.primaryTileset=&gTileset_General;
    seasonal=0;assert(!LegendsSnowGrassCleared(7,7));seasonal=1;
    LegendsResetSnowGrass();assert(!LegendsSnowGrassCleared(7,7));
    gBackupMapLayout.width=200;gBackupMapLayout.height=200;LegendsStepSnowGrass(199,199);assert(!LegendsSnowGrassCleared(199,199));
    struct TextPrinter second={1,1,{WINDOW_TEXT_PRINTER,2,{22}},0,0};
    struct TextPrinter first={1,1,{WINDOW_TEXT_PRINTER,0,{11}},0,&second};
    sFirstTextPrinter=&first;glyph.asU32=99;RunTextPrinters();assert(rendered==2&&!first.active&&!second.active);
    first.active=second.active=1;instant=1;glyph.asU32=99;RunTextPrinters();assert(rendered==4);
    puts("Seasonal grass isolation, snow scuff/reset/bounds and active-printer glyph colors and full dialogue clearing passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'polish.c';p.write_text(pre+colors+grass+printer+clear+main)
 subprocess.run(['cc','-std=gnu11','-Wall','-Werror=implicit-function-declaration',str(p),'-o',d+'/polish'],check=True)
 subprocess.run([d+'/polish'],check=True)
# The naming screen must route through the appearance-aware object factory.
icon=function('src/naming_screen.c','static void NamingScreen_CreatePlayerIcon(void)')
assert 'LegendsGetPlayerGraphicsId(' in icon and 'GetRivalAvatarGraphicsId' not in icon
