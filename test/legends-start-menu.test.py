"""Compile the actual pause panel under engine mocks; check lifecycle and snapshots."""
import pathlib, subprocess, tempfile
root = pathlib.Path(__file__).resolve().parents[1]
source = (root / "src/legends_start_menu.c").read_text()
source = "\n".join(line for line in source.splitlines() if not line.startswith("#include"))
preamble = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32; typedef int bool8;
#define EWRAM_DATA
#define TRUE 1
#define FALSE 0
#define WINDOW_NONE 255
#define PIXEL_FILL(x) ((x)|((x)<<4))
#define FONT_SMALL 0
#define TEXT_SKIP_DRAW 0
#define COPYWIN_GFX 2
#define COPYWIN_FULL 3
#define COMPOUND_STRING(x) ((const u8 *)(x))
#define RTC_ERR_FLAG_MASK 0xFF0
#define RTC_INIT_ERROR 1
'''
preamble += (root / "include/constants/weather.h").read_text()
preamble += (root / "include/constants/map_types.h").read_text()
preamble += r'''
struct WindowTemplate {u8 bg,tilemapLeft,tilemapTop,width,height,paletteNum;u16 baseBlock;};
struct {u8 mapType;} gMapHeader;
struct {int hours,minutes;} gLocalTime;
static int error,weather,season,adds,removes,copies,rtcReads,pixels,fail;
static const struct WindowTemplate *template;
static char texts[2][32];
static u8 pixelBuffer[32][96];
u16 RtcGetErrorStatus(void){return error;}
void RtcCalcLocalTime(void){rtcReads++;}
u8 GetCurrentWeather(void){return weather;}
u8 LegendsGetActiveSeason(void){return season;}
const u8 *LegendsGetSeasonName(u8 s){return (const u8 *[]){"SPRING","SUMMER","AUTUMN","WINTER"}[s];}
void FormatDecimalTimeWithoutSeconds(u8 *d,int h,int m,int f){sprintf((char*)d,"%02d:%02d %s",h%12?h%12:12,m,h<12?"AM":"PM");}
u32 AddWindow(const struct WindowTemplate *t){adds++;template=t;return fail?255:4;}
void RemoveWindow(u32 w){assert(w==4);removes++;}
void PutWindowTilemap(u32 w){assert(w==4);}
void DrawStdWindowFrame(u8 w,int c){assert(w==4);}
void ClearStdWindowAndFrameToTransparent(u8 w,int c){assert(w==4&&c);}
void CopyWindowToVram(u32 w,u32 m){assert(w==4);copies++;}
void FillWindowPixelBuffer(u32 w,u8 v){pixels=0;memset(pixelBuffer,v&15,sizeof(pixelBuffer));}
void FillWindowPixelRect(u32 w,u8 v,u16 x,u16 y,u16 a,u16 b){assert(x+a<=96&&y+b<=32);for(int j=y;j<y+b;j++)for(int i=x;i<x+a;i++)pixelBuffer[j][i]=v&15;pixels++;}
void AddTextPrinterParameterized(u8 w,u8 f,const u8 *t,u16 x,u16 y,int speed,void *cb){snprintf(texts[y==0?0:1],32,"%s",t);}
'''
main = r'''
int main(void){
gMapHeader.mapType=MAP_TYPE_ROUTE;gLocalTime.hours=0;gLocalTime.minutes=5;
LegendsShowStartMenuPanel();
assert(adds==1&&pixels>0&&!strcmp(texts[0],"12:05 AM")&&!strcmp(texts[1],"SPRING"));
assert(template->tilemapLeft==1&&template->tilemapTop==14);
assert(template->baseBlock+template->width*template->height<=0x107);
int c=copies,r=rtcReads;
for(int i=0;i<60;i++) LegendsUpdateStartMenuPanel();
assert(copies==c+2&&rtcReads==r+1);
gLocalTime.hours=12;gLocalTime.minutes=0;weather=WEATHER_RAIN;season=3;
for(int i=0;i<60;i++) LegendsUpdateStartMenuPanel();
assert(!strcmp(texts[0],"12:00 PM")&&!strcmp(texts[1],"WINTER")&&sLastIcon==ICON_RAIN);
error=1;for(int i=0;i<60;i++) LegendsUpdateStartMenuPanel();assert(!strcmp(texts[0],"--:--"));
assert(GetWeatherIcon()==ICON_RAIN);
gMapHeader.mapType=MAP_TYPE_INDOOR;assert(GetWeatherIcon()==ICON_INDOOR);
gMapHeader.mapType=MAP_TYPE_UNDERWATER;assert(GetWeatherIcon()==ICON_WATER);
gMapHeader.mapType=MAP_TYPE_ROUTE;
weather=WEATHER_VOLCANIC_ASH;assert(GetWeatherIcon()==ICON_ASH);
weather=WEATHER_SANDSTORM;assert(GetWeatherIcon()==ICON_SAND);
weather=WEATHER_SNOW;assert(GetWeatherIcon()==ICON_SNOW);
weather=WEATHER_RAIN_THUNDERSTORM;assert(GetWeatherIcon()==ICON_THUNDER);
weather=WEATHER_FOG_HORIZONTAL;assert(GetWeatherIcon()==ICON_FOG);
LegendsShowStartMenuPanel();assert(adds==1);
LegendsHideStartMenuPanel();LegendsHideStartMenuPanel();assert(removes==1);
c=copies;LegendsUpdateStartMenuPanel();assert(copies==c);
fail=1;LegendsShowStartMenuPanel();assert(!sWindowHandle);
fail=0;error=0;LegendsShowStartMenuPanel();assert(sWindowHandle==5);
LegendsHideStartMenuPanel();assert(removes==2);
// Check every icon and animation phase stays within the icon bounds and
// paints native colors. Clock hands must be an L, not parallel U strokes.
assert(sIcons[ICON_CLOCK][3]==0x841&&sIcons[ICON_CLOCK][6]==0x879);
for(int icon=0;icon<=ICON_INDOOR;icon++){
    u8 frames[2][32][96];
    for(int phase=0;phase<2;phase++){
        sAnimationPhase=phase;
        FillWindowPixelBuffer(4,PIXEL_FILL(1));DrawIcon(4,icon,18);
        for(int y=0;y<32;y++)for(int x=0;x<96;x++)
            if(x<4||x>=16||y<18||y>=30)assert(pixelBuffer[y][x]==1);
        memcpy(frames[phase],pixelBuffer,sizeof(pixelBuffer));
    }
    if(icon!=ICON_CLOCK&&icon!=ICON_CLOUD&&icon!=ICON_INDOOR)
        assert(memcmp(frames[0],frames[1],sizeof(pixelBuffer))!=0);
}
assert(GetIconColor(ICON_SUN,5)==5&&GetIconColor(ICON_RAIN,9)==8);
assert(GetIconColor(ICON_SNOW,4)==9&&GetIconColor(ICON_SAND,4)==5);
puts("Pause panel lifecycle, clock, colored animation and tile/pixel bounds passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
    path = pathlib.Path(d) / "panel.c"
    path.write_text(preamble + source + main)
    subprocess.run(["cc","-std=gnu11","-Werror=implicit-function-declaration",str(path),"-o",d+"/panel"],check=True)
    subprocess.run([d+"/panel"],check=True)
