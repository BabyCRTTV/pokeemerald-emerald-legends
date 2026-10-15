"""Compile the actual pause panel under engine mocks; check lifecycle and snapshots."""
import pathlib, subprocess, tempfile, json, re
root = pathlib.Path(__file__).resolve().parents[1]
source = (root / "src/legends_start_menu.c").read_text()
source = "\n".join(line for line in source.splitlines() if not line.startswith("#include"))
preamble = r'''
#include <assert.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32; typedef int bool8;
typedef int32_t s32;
#define WINDOW_TILE_DATA 7
#define EOS 0
#define CHAR_SPACE ' '
#define CHAR_NEWLINE '\n'
#define EWRAM_DATA
#define TRUE 1
#define FALSE 0
#define WINDOW_NONE 255
#define PIXEL_FILL(x) ((x)|((x)<<4))
#define FONT_SMALL 0
#define TEXT_SKIP_DRAW 0
#define STR_CONV_MODE_LEFT_ALIGN 0
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
enum {TIME_MORNING,TIME_DAY,TIME_EVENING,TIME_NIGHT};
static int timeOfDay=TIME_DAY;
int GetTimeOfDay(void){return timeOfDay;}
static int error,weather,season,adds,removes,copies,rtcReads,pixels,fail;
static const struct WindowTemplate *template;
static char texts[3][32];
static u8 pixelBuffer[48][96];
static u8 cardPixels[72][96];
static u32 cardTiles[12*9*8], scratchTiles[12*2*8];
static unsigned allocations;
void *AllocZeroed(unsigned size){if(fail==3)return NULL;void *p=calloc(1,size);if(p)allocations++;return p;}
void Free(void *p){if(p){assert(allocations);allocations--;free(p);}}
static void setPixel(u32 *tiles,int x,int y,u8 color){unsigned i=(y/8*12+x/8)*8+y%8,shift=x%8*4;tiles[i]=(tiles[i]&~(15u<<shift))|((color&15u)<<shift);}
static void unpackCard(void){for(int y=0;y<72;y++)for(int x=0;x<96;x++)cardPixels[y][x]=(cardTiles[(y/8*12+x/8)*8+y%8]>>(x%8*4))&15;}

static unsigned activeWindows;
static char reminderText[512];
static u16 tracked=0xFFFF;
static int mapPopup,noticeHides;
struct LegendsQuest {const u8 *title;u8 count;struct {const u8 *text;} steps[4];};
static struct LegendsQuest quest;
u16 LegendsQuestTracked(void){return tracked;}
const struct LegendsQuest *LegendsQuestGet(u16 id){return id==0?&quest:NULL;}
u8 LegendsQuestNextStep(u16 id){return 0;}
int IsMapNamePopupActive(void){return mapPopup;}
void LegendsAchievementPopupHide(void){noticeHides++;}
int GetStringWidth(int font,const u8 *text,int spacing){int w=0;for(;*text;text++)w+=fontWidths[*text];return w;}
static u16 playedDays=1;
void LegendsAdventureUpdateDay(void){}
u16 LegendsAdventureDays(void){return playedDays;}
u8 *StringCopy(u8 *d,const u8 *s){strcpy((char*)d,(const char*)s);return d;}
u8 *ConvertIntToDecimalStringN(u8 *d,int n,int mode,int size){sprintf((char*)d,"%d",n);return d;}
u16 RtcGetErrorStatus(void){return error;}
void RtcCalcLocalTime(void){rtcReads++;if(error){gLocalTime.hours=9;gLocalTime.minutes=0;}}
u8 GetCurrentWeather(void){return weather;}
u8 LegendsGetActiveSeason(void){return season;}
const u8 *LegendsGetSeasonName(u8 s){return (const u8 *[]){"SPRING","SUMMER","AUTUMN","WINTER"}[s];}
void FormatDecimalTimeWithoutSeconds(u8 *d,int h,int m,int f){sprintf((char*)d,"%02d:%02d %s",h%12?h%12:12,m,h<12?"AM":"PM");}
u32 AddWindow(const struct WindowTemplate *t){adds++;template=t;if(fail==1||(fail==2&&t->height==2))return 255;unsigned w=t->height==2?6:t->height==9?5:4;assert(!(activeWindows&(1<<w)));activeWindows|=1<<w;return w;}
void RemoveWindow(u32 w){assert(w==4||w==5||w==6);assert(activeWindows&(1<<w));activeWindows&=~(1<<w);removes++;}
void PutWindowTilemap(u32 w){assert(w==4||w==5);}
void DrawStdWindowFrame(u8 w,int c){assert(w==4||w==5);if(w==5)reminderText[0]=0;}
void ClearStdWindowAndFrameToTransparent(u8 w,int c){assert((w==4||w==5)&&c);}
void CopyWindowToVram(u32 w,u32 m){assert(w==4||w==5);copies++;}
void FillWindowPixelBuffer(u32 w,u8 v){if(w==6){memset(scratchTiles,v,sizeof(scratchTiles));return;}pixels=0;memset(pixelBuffer,v&15,sizeof(pixelBuffer));}
void FillWindowPixelRect(u32 w,u8 v,u16 x,u16 y,u16 a,u16 b){if(w==5){assert(x+a<=96&&y+b<=72);for(int j=y;j<y+b;j++)for(int i=x;i<x+a;i++)setPixel(cardTiles,i,j,v);return;}assert(x+a<=96&&y+b<=48);for(int j=y;j<y+b;j++)for(int i=x;i<x+a;i++)pixelBuffer[j][i]=v&15;pixels++;}
void AddTextPrinterParameterized(u8 w,u8 f,const u8 *t,u16 x,u16 y,int speed,void *cb){snprintf(texts[y/16],32,"%s",t);}
void AddTextPrinterParameterized3(u8 w,u8 f,int x,int y,const u8 *ink,int speed,const u8 *t){
 assert((w==5||w==6)&&x+GetStringWidth(f,t,0)<=96&&y+12<=(w==6?16:72));
 int px=x;for(const u8 *p=t;*p;p++){
  for(int col=0;col<fontWidths[*p];col++)for(int row=2;row<10;row++){
   u8 color=(*p+col+row)%12+2;
   setPixel(w==6?scratchTiles:cardTiles,px+col,y+row,color);
  }
  px+=fontWidths[*p];
 }
 if(w==5&&y)for(;*t;t++)if(*t!=' '){unsigned n=strlen(reminderText);reminderText[n]=*t;reminderText[n+1]=0;}
}
uintptr_t GetWindowAttribute(u32 w,u32 a){assert((w==5||w==6)&&a==WINDOW_TILE_DATA);return (uintptr_t)(w==6?scratchTiles:cardTiles);}

'''
helpers = r'''
static void checkReminder(const char *title,const char *step){
 char expected[512];unsigned n=0;quest.title=(const u8*)title;quest.count=1;quest.steps[0].text=(const u8*)step;
 for(const char *p=title;*p;p++)if(*p!=' ')expected[n++]=*p;
 for(const char *p=step;*p;p++)if(*p!=' ')expected[n++]=*p;expected[n]=0;
 LegendsShowTrackedQuestReminder();assert(sReminderHandle==6);assert(!strcmp(expected,reminderText));
 LegendsHideTrackedQuestReminder();assert(!sReminderHandle);
}
'''
main = r'''
int main(void){
gMapHeader.mapType=MAP_TYPE_ROUTE;gLocalTime.hours=0;gLocalTime.minutes=5;
timeOfDay=TIME_NIGHT;
LegendsShowStartMenuPanel();
assert(sLastIcon==ICON_MOON);
assert(adds==1&&pixels>0&&!strcmp(texts[1],"12:05 AM")&&!strcmp(texts[2],"SPRING"));
assert(!strcmp(texts[0],"DAY 1"));
assert(template->tilemapLeft==1&&template->tilemapTop==12);
assert(template->baseBlock+template->width*template->height<=0x107);
int c=copies,r=rtcReads;
for(int i=0;i<60;i++) LegendsUpdateStartMenuPanel();
assert(copies==c+2&&rtcReads==r+1);
playedDays=2;gLocalTime.hours=12;gLocalTime.minutes=0;weather=WEATHER_RAIN;season=3;
for(int i=0;i<60;i++) LegendsUpdateStartMenuPanel();
assert(!strcmp(texts[0],"DAY 2"));
assert(!strcmp(texts[1],"12:00 PM")&&!strcmp(texts[2],"WINTER")&&sLastIcon==ICON_RAIN);
error=1;for(int i=0;i<60;i++) LegendsUpdateStartMenuPanel();assert(!strcmp(texts[1],"09:00 AM"));
assert(GetWeatherIcon()==ICON_RAIN);
weather=WEATHER_SUNNY;timeOfDay=TIME_NIGHT;assert(GetWeatherIcon()==ICON_MOON);
timeOfDay=TIME_DAY;assert(GetWeatherIcon()==ICON_SUN);
weather=WEATHER_SUNNY_CLOUDS;assert(GetWeatherIcon()==ICON_CLOUD);
 weather=WEATHER_DROUGHT;timeOfDay=TIME_NIGHT;assert(GetWeatherIcon()==ICON_SUN);
weather=WEATHER_RAIN;
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
for(int icon=0;icon<=ICON_MOON;icon++){
    u8 frames[2][48][96];
    for(int phase=0;phase<2;phase++){
        sAnimationPhase=phase;
        FillWindowPixelBuffer(4,PIXEL_FILL(1));DrawIcon(4,icon,34);
        for(int y=0;y<48;y++)for(int x=0;x<96;x++)
            if(x<4||x>=16||y<34||y>=46)assert(pixelBuffer[y][x]==1);
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
    charmap={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(root/'charmap.txt').read_text(),re.M)}
    charmap["'"]=0xB4
    widths=list(map(int,re.findall(r'\d+',(root/'src/fonts.c').read_text().split('gFontSmallLatinGlyphWidths[] = {')[1].split('};')[0])))
    table=[widths[charmap[chr(i)]] if chr(i) in charmap else 0 for i in range(128)]
    fontdef='static const int fontWidths[128]='+json.dumps(table).replace('[','{').replace(']','}')+';\n'
    cases='\n'.join('checkReminder(%s,%s);'%(json.dumps(q['title']),json.dumps(step['text'])) for q in json.loads((root/'data/legends/quests.json').read_text()) for step in q['steps'])
    extra=r'''
tracked=0;mapPopup=1;c=adds;LegendsShowTrackedQuestReminder();assert(adds==c&&!sReminderHandle);
assert(sReminderTemplate.tilemapLeft+sReminderTemplate.width+1<=16);
assert(sReminderTemplate.tilemapTop+sReminderTemplate.height+1<=sPanelTemplate.tilemapTop-1);
assert(sReminderTemplate.baseBlock>=0x214+9);
assert(sReminderTemplate.baseBlock+sReminderTemplate.width*sReminderTemplate.height<=(0xE000-0x8000)/32);
mapPopup=0;fail=1;LegendsShowTrackedQuestReminder();assert(!sReminderHandle);fail=0;
'''+cases+r'''
LegendsShowTrackedQuestReminder();c=adds;LegendsShowTrackedQuestReminder();assert(adds==c);
LegendsHideStartMenuPanel();assert(!sReminderHandle); // Also hides when the clock panel is absent.
// Current short text stays still: no scratch allocation or repeated graphics copies.
checkReminder("SHORT TITLE","A short objective.");LegendsShowTrackedQuestReminder();
assert(!sReminderScrollLimit&&!sReminderLineHandle);c=copies;
for(int f=0;f<900;f++)LegendsUpdateTrackedQuestReminder();assert(copies==c);
LegendsHideTrackedQuestReminder();
quest.title=(const u8*)"A longer title that wraps across several lines";
quest.steps[0].text=(const u8*)"Return the recovered DEVON GOODS to the researcher waiting inside DEVON CORPORATION in RUSTBORO CITY. Speak to the receptionist and check the delivery details before you leave for the next destination.";
LegendsShowTrackedQuestReminder();assert(sReminderScrollLimit>60&&sReminderLineHandle==7);
unsigned limit=sReminderScrollLimit;u8 start[72][96];unpackCard();memcpy(start,cardPixels,sizeof(start));c=copies;
for(int f=0;f<120;f++){LegendsUpdateTrackedQuestReminder();assert(sReminderScrollOffset==0);}
assert(copies==c);
for(unsigned f=0;f<limit*3;f++){
 LegendsUpdateTrackedQuestReminder();assert(sReminderScrollOffset==(f+1)/3);
 unpackCard();assert(!memcmp(start,cardPixels,12*96)); // Fixed label/divider are never scrolled.
}
assert(sReminderReturning&&sReminderScrollOffset==limit);c=copies;
for(int f=0;f<120;f++)LegendsUpdateTrackedQuestReminder();assert(copies==c);
for(unsigned f=0;f<limit*3;f++){
 LegendsUpdateTrackedQuestReminder();assert(sReminderScrollOffset==limit-(f+1)/3);
 unpackCard();assert(!memcmp(start,cardPixels,12*96));
}
assert(!sReminderScrollOffset&&!sReminderReturning&&!memcmp(start,cardPixels,sizeof(start)));
LegendsHideTrackedQuestReminder();c=copies;
for(int f=0;f<300;f++)LegendsUpdateTrackedQuestReminder();assert(copies==c&&!activeWindows&&!allocations);
for(fail=1;fail<=3;fail++){LegendsShowTrackedQuestReminder();assert(!sReminderHandle&&!sReminderLineHandle&&!activeWindows&&!allocations);}fail=0;
LegendsShowTrackedQuestReminder();assert(!sReminderScrollOffset);LegendsHideStartMenuPanel();assert(!activeWindows&&!allocations);
'''
    main=main.replace('puts("Pause panel',extra+'puts("Pause panel')
    path.write_text(fontdef + preamble + source + helpers + main)
    subprocess.run(["cc","-std=gnu11","-Werror=implicit-function-declaration",str(path),"-o",d+"/panel"],check=True)
    subprocess.run([d+"/panel"],check=True)

# Framed screen rectangles and physical VRAM ranges cannot collide.
def disjoint(a,b):
    return a[2]<=b[0] or b[2]<=a[0] or a[3]<=b[1] or b[3]<=a[1]
assert disjoint((0,0,112,88),(128,0,240,160))
assert disjoint((0,0,112,88),(0,88,112,152))
assert 0x250 >= 0x214+9 and 0x250+12*9 <= (0xE000-0x8000)//32
assert 0x139+12*18 <= 0x250 and 0xB8+12*6 <= 0x250
menu=(root/'src/start_menu.c').read_text()
helpbody=menu.split('static void ShowDexNavHelp(void)\n{')[1].split('\nstatic bool8 HandleStartMenuInput')[0]
assert helpbody.index('LegendsHideTrackedQuestReminder();')<helpbody.index('AddWindow(&window)')
guard=menu.split('static void ShowTrackedQuestReminder(void)\n{')[1].split('\n}')[0]
for predicate in ['!GetSafariZoneFlag()', 'PYRAMID_LOCATION_NONE', '!IsOverworldLinkActive()', '!InUnionRoom()', '!InBattlePike()', '!InMultiPartnerRoom()']:
    assert predicate in guard
