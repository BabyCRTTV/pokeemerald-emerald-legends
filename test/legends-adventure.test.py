"""Run the real journal/day/filter implementation under host engine stubs."""
from pathlib import Path
import subprocess,tempfile
R=Path(__file__).resolve().parents[1]
source='\n'.join(l for l in (R/'src/legends_adventure.c').read_text().splitlines() if not l.startswith('#include'))
preamble=r'''
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32; typedef int bool32; typedef uint8_t bool8;
#define IS_FRLG 0
#include "constants/opponents.h"
#include "constants/flags.h"
#include "legends_adventure.h"
#define TRUE 1
#define FALSE 0
#define EWRAM_DATA
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define NUM_SPECIES 1600
#define SPECIES_NONE 0
#define MAPSEC_LITTLEROOT_TOWN 0
#define RTC_ERR_FLAG_MASK 0xFF0
#define RTC_INIT_ERROR 1
struct SiiRtcInfo {u8 year,month,day;};
struct {u8 dexNavChain;struct LegendsAdventureSave adventure;} block3,*gSaveBlock3Ptr=&block3;
struct {u16 playTimeHours;u8 playTimeMinutes;} block2,*gSaveBlock2Ptr=&block2;
struct {u16 regionMapSectionId;} gMapHeader;
static int invalid,linked,reads;
static u16 date=100;
static struct SiiRtcInfo clockInfo={0x26,0x10,0x10};
static u8 flags[0x2000];
const int sNumDaysInMonths[]={31,28,31,30,31,30,31,31,30,31,30,31};
u16 RtcGetErrorStatus(void){return invalid;}
void RtcGetInfo(struct SiiRtcInfo *r){*r=clockInfo;reads++;}
u32 ConvertBcdToBinary(u8 x){return (x>>4)*10+(x&15);}
bool32 IsLeapYear(u32 y){return y%4==0;}
u16 RtcGetDayCount(struct SiiRtcInfo *r){return date;}
bool32 FlagGet(u16 f){return (flags[f/8]>>(f%8))&1;}
bool32 IsOverworldLinkActive(void){return linked;}
'''

def function(name):
 text=(R/'src/event_data.c').read_text();start=text.index('u8 '+name+'(');brace=text.index('{',start);depth=1;end=brace+1
 while depth:
  depth+=(text[end]=='{')-(text[end]=='}');end+=1
 return text[start:end]
source += '\nu8 *GetFlagPointer(u16 id){return id ? &flags[id/8] : NULL;}\n'+function('FlagSet')+'\n'+function('FlagClear')
tests=r'''
static void reset(void){memset(&block3,0,sizeof(block3));memset(&block2,0,sizeof(block2));memset(flags,0,sizeof(flags));invalid=linked=0;date=100;clockInfo=(struct SiiRtcInfo){0x26,0x10,0x10};gMapHeader.regionMapSectionId=12;LegendsAdventureInit(TRUE);}
int main(void){
assert(sizeof(struct LegendsAdventureEntry)==16);
assert(sizeof(block3)<=580); // Entire extension fits all native partial-save chunks.
reset();assert(LegendsAdventureDays()==1&&LegendsAdventureCount(ADV_FILTER_ALL,0)==1);
assert(LegendsAdventureGet(0)->event==ADV_BEGIN);
block2.playTimeHours=4;LegendsAdventureRecord(ADV_CHECKPOINT);
LegendsAdventureInit(FALSE);assert(LegendsAdventureDays()==1); // Same-date reload.
date=101;clockInfo.day=0x11;block2.playTimeHours=7;LegendsAdventureInit(FALSE);
assert(LegendsAdventureDays()==2&&LegendsAdventureGet(0)->hours==7);
LegendsAdventureUpdateDay();assert(LegendsAdventureDays()==2);
date=108;clockInfo.day=0x18;LegendsAdventureUpdateDay();assert(LegendsAdventureDays()==3); // A week away is one active day.
date=105;LegendsAdventureUpdateDay();assert(LegendsAdventureDays()==3); // Rollback never inflates count.
date=108;LegendsAdventureUpdateDay();assert(LegendsAdventureDays()==3);
invalid=1;date=109;LegendsAdventureUpdateDay();assert(LegendsAdventureDays()==3);
invalid=0;LegendsAdventureUpdateDay();assert(LegendsAdventureDays()==4);
LegendsAdventureCatch(25,6);assert(LegendsAdventureGet(0)->species==25);
u8 n=LegendsAdventureCount(ADV_FILTER_ALL,0);LegendsAdventureCatch(133,8);assert(LegendsAdventureCount(ADV_FILTER_ALL,0)==n&&LegendsAdventureGet(0)->species==133);
LegendsAdventureFlagSet(FLAG_BADGE01_GET);assert(LegendsAdventureGet(0)->event==ADV_BADGE1&&LegendsAdventureGet(0)->species==133);
LegendsAdventureRecord(ADV_CHECKPOINT);assert(LegendsAdventureGet(0)->context==ADV_BADGE1);
n=LegendsAdventureCount(ADV_FILTER_ALL,0);LegendsAdventureRecord(ADV_CHECKPOINT);assert(LegendsAdventureCount(ADV_FILTER_ALL,0)==n);
for(int i=0;i<12;i++){LegendsAdventureCatch(25,9);LegendsAdventureRecord(ADV_CHECKPOINT);}
assert(LegendsAdventureCount(ADV_FILTER_ALL,0)==n); // Alternating catches/saves refresh one field note.
assert(LegendsAdventureCount(ADV_FILTER_STORY,0)==1);
assert(LegendsAdventureFiltered(ADV_FILTER_STORY,0,0)->event==ADV_BADGE1);
assert(LegendsAdventureFiltered(ADV_FILTER_STORY,0,1)==NULL);
assert(LegendsAdventureCount(ADV_FILTER_DAY,4)==3);
assert(LegendsAdventureAdjacentDay(4,TRUE)==3&&LegendsAdventureAdjacentDay(1,FALSE)==2);
date=110;LegendsAdventureUpdateDay();assert(LegendsAdventureGet(0)->species==0);
// Every shipped/future Kanto flag can use the same modular registry.
for(u32 i=0;i<ARRAY_COUNT(sMilestones);i++)LegendsAdventureFlagSet(sMilestones[i].flag);
assert(LegendsAdventureGet(0)->event==ADV_SURVEY_REPORT);
for(int i=0;i<80;i++){block2.playTimeMinutes=i%60;LegendsAdventureRecord(ADV_BADGE1);}
assert(LegendsAdventureCount(ADV_FILTER_ALL,0)==32&&LegendsAdventureGet(32)==NULL);
struct LegendsAdventureSave saved=block3.adventure;
LegendsAdventureInit(FALSE);assert(!memcmp(&saved,&block3.adventure,sizeof(saved))); // Save/reload continuity.
block3.adventure.entries[5].species=999;LegendsAdventureInit(FALSE);assert(block3.adventure.count==1&&LegendsAdventureDays()==1); // Torn/corrupt extension only resets notebook.
reset();FlagSet(FLAG_SYS_GAME_CLEAR);memset(&block3.adventure,0xFF,sizeof(block3.adventure));LegendsAdventureInit(FALSE);
assert(LegendsAdventureGet(0)->event==ADV_RESUME&&LegendsAdventureGet(0)->context==ADV_CHAMPION); // No fabricated historical dates.
reset();clockInfo.month=0;LegendsAdventureUpdateDay();assert(LegendsAdventureDays()==1);
clockInfo.month=0x02;clockInfo.day=0x30;LegendsAdventureUpdateDay();assert(LegendsAdventureDays()==1);
reset();FlagSet(FLAG_BADGE01_GET);n=LegendsAdventureCount(ADV_FILTER_ALL,0);
FlagSet(FLAG_BADGE01_GET);assert(LegendsAdventureCount(ADV_FILTER_ALL,0)==n);
FlagClear(FLAG_SYS_WEATHER_CTRL);assert(LegendsAdventureCount(ADV_FILTER_ALL,0)==n);
FlagSet(FLAG_SYS_WEATHER_CTRL);FlagClear(FLAG_SYS_WEATHER_CTRL);assert(LegendsAdventureGet(0)->event==ADV_WEATHER_PEACE);
n=LegendsAdventureCount(ADV_FILTER_ALL,0);FlagClear(FLAG_SYS_WEATHER_CTRL);assert(LegendsAdventureCount(ADV_FILTER_ALL,0)==n);
reset();linked=1;LegendsAdventureRecord(ADV_BADGE1);assert(LegendsAdventureCount(ADV_FILTER_STORY,0)==0);
linked=0;reads=0;for(int i=0;i<3599;i++)LegendsAdventureTick();assert(reads==0);LegendsAdventureTick();assert(reads==1);
puts("Adventure journal, active dates, retention, filters, catches and migration passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'check.c').write_text(preamble+source+tests)
 subprocess.run(['cc','-std=gnu99','-Wall','-Wextra','-Wno-unused-parameter','-Werror','-iquote',str(R/'include'),str(p/'check.c'),'-o',str(p/'check')],check=True)
 subprocess.run([str(p/'check')],check=True)
