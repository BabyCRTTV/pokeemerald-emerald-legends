"""Compile actual effective-clock service: device priority, manual offsets,
invalid RTC, saved fallback ticks, pause-menu polling and the native timer cap.
"""
from pathlib import Path
import subprocess,tempfile,os
root=Path(__file__).resolve().parents[1]
rtc_source=(root/'src/rtc.c').read_text()
start=rtc_source.index('void RtcGetInfo(struct SiiRtcInfo *rtc)')
rtc_get_info=rtc_source[start:rtc_source.index('\n}',start)+2]
def rtc_function(signature):
 start=rtc_source.index(signature);return rtc_source[start:rtc_source.index('\n}',start)+2]
source='\n'.join(l for l in (root/'src/legends_clock.c').read_text().splitlines() if not l.startswith('#include'))
pre=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef int32_t s32;typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int bool8;
#define TRUE 1
#define FALSE 0
#define RTC_ERR_FLAG_MASK 0xFF0
#define RTC_INIT_ERROR 1
#define VAR_LEGENDS_CLOCK_SECONDS_LO 0
#define VAR_LEGENDS_CLOCK_SECONDS_HI 1
#define VAR_LEGENDS_CLOCK_INIT 2
#define VAR_LEGENDS_CLOCK_FRAMES 3
#define VAR_LEGENDS_CLOCK_MODE 4
#define VAR_LEGENDS_MANUAL_OFFSET 5
#define VAR_LEGENDS_MANUAL_RTC_READY 6
#define VAR_LEGENDS_CLOCK_DAY_ORIGIN 7
#define HOURS_PER_DAY 24
#define MINUTES_PER_HOUR 60
#define SECONDS_PER_MINUTE 60
struct Time {int days,hours,minutes,seconds;}gLocalTime;
struct SiiRtcInfo {u8 year,month,day,hour,minute,second;};
struct {u16 playTimeHours;u8 playTimeMinutes,playTimeSeconds,playTimeVBlanks;struct Time localTimeOffset;}save,*gSaveBlock2Ptr=&save;
static u16 vars[8],error;static struct SiiRtcInfo device={26,10,10,13,41,59};
static int polls;
u16 VarGet(int id){return vars[id];}void VarSet(int id,u16 v){vars[id]=v;}
u16 RtcGetErrorStatus(void){return error;}
#define OW_USE_FAKE_RTC 0
#define sErrorStatus error
static const struct SiiRtcInfo sRtcDummy={0,1,1,0,0,0};
void RtcGetRawInfo(struct SiiRtcInfo*r){*r=device;polls++;}
void FakeRtc_GetRawInfo(struct SiiRtcInfo*r){*r=device;}
__RTC_GET_INFO__
u32 ConvertBcdToBinary(u8 v){return v;}
int IsLeapYear(int y){return y%4==0;}
const int sNumDaysInMonths[]={31,28,31,30,31,30,31,31,30,31,30,31};
static struct SiiRtcInfo sRtc;
u16 RtcGetDayCount(struct SiiRtcInfo*r){return 9000+r->day-10;}
void FakeRtc_ManuallySetTime(int d,int h,int m,int s){}
__RTC_DIFFERENCE__
__RTC_OFFSET__
u8 gStringVar1[32];
void RtcCalcLocalTime(void);
void FormatDecimalTimeWithoutSeconds(u8*d,int h,int m,int fmt){sprintf((char*)d,"%02d:%02d",h,m);}
'''
pre=pre.replace('__RTC_GET_INFO__',rtc_get_info).replace('__RTC_DIFFERENCE__',rtc_function('void RtcCalcTimeDifference(')).replace('__RTC_OFFSET__',rtc_function('void RtcCalcLocalTimeOffset('))
post=r'''
void RtcCalcLocalTime(void){LegendsClockCalcLocalTime();}
int main(void){
 struct SiiRtcInfo snapshot;
 error=RTC_INIT_ERROR;RtcGetInfo(&snapshot);assert(!polls&&snapshot.month==1&&snapshot.day==1);
 error=RTC_ERR_FLAG_MASK;RtcGetInfo(&snapshot);assert(!polls&&snapshot.month==1);
 error=0;

 save.localTimeOffset.days=9000;save.localTimeOffset.hours=7;save.localTimeOffset.minutes=12;save.localTimeOffset.seconds=59;
 LegendsClockCalcLocalTime();assert(gLocalTime.hours==13&&gLocalTime.minutes==41&&gLocalTime.seconds==59&&gLocalTime.days==0);
 // Device time advances without any played-frame ticks (as when in a menu).
 device.minute=42;device.second=0;LegendsClockCalcLocalTime();assert(gLocalTime.minutes==42&&polls==2);
 LegendsClockSetManual(18,30);LegendsClockCalcLocalTime();assert(gLocalTime.hours==18&&gLocalTime.minutes==30&&gLocalTime.days==0);assert(save.localTimeOffset.days==8999);
 device.minute=43;LegendsClockCalcLocalTime();assert(gLocalTime.minutes==31);
 LegendsClockUseRealTime();assert(gLocalTime.hours==13&&gLocalTime.minutes==43&&gLocalTime.days==0);
 error=1;LegendsClockCalcLocalTime();assert(gLocalTime.hours==9&&!gLocalTime.minutes);
 for(int i=0;i<60;i++){LegendsClockTick();}LegendsClockCalcLocalTime();assert(gLocalTime.seconds==1);
 StoreSeconds(3600*7);LegendsClockCalcLocalTime();assert(gLocalTime.hours==16);
 LegendsClockSetManual(23,59);LegendsClockCalcLocalTime();assert(gLocalTime.hours==23&&gLocalTime.minutes==59);
 for(int i=0;i<3600;i++){LegendsClockTick();}LegendsClockCalcLocalTime();assert(gLocalTime.hours==0&&!gLocalTime.minutes);
 LegendsClockUseRealTime();assert(gLocalTime.hours==16&&gLocalTime.minutes==1);
 // Invalid calendar/BCD fields cannot index outside the native month table.
 error=0;device.month=0;LegendsClockCalcLocalTime();assert(gLocalTime.hours==16);
 device.month=13;LegendsClockCalcLocalTime();assert(gLocalTime.hours==16);
 device.month=2;device.day=30;LegendsClockCalcLocalTime();assert(gLocalTime.hours==16);
 device.month=10;device.day=10;device.hour=24;LegendsClockCalcLocalTime();assert(gLocalTime.hours==16);
 device.hour=13;LegendsClockCalcLocalTime();assert(gLocalTime.hours==13);
 error=1;LegendsClockSetManual(20,15);error=0;LegendsClockCalcLocalTime();assert(gLocalTime.hours==20&&gLocalTime.minutes==15);
 LegendsClockUseRealTime();assert(gLocalTime.hours==13);

 error=1;save.playTimeHours=999;StoreSeconds(999*3600);for(int i=0;i<3600;i++){LegendsClockTick();}assert(PlayedSeconds()==999*3600+60);
 LegendsClockBufferTime();assert(strlen((char*)gStringVar1)>0);
 // Real/manual switches keep a stable day origin despite hour borrowing.
 device.day=11;device.hour=0;device.minute=0;device.second=0;error=0;
 LegendsClockCalcLocalTime();assert(gLocalTime.days==1);
 LegendsClockSetManual(18,0);LegendsClockUseRealTime();assert(gLocalTime.days==1&&gLocalTime.hours==0);
 // A clock first initialized without RTC anchors to its played-day count.
 memset(vars,0,sizeof(vars));memset(&save,0,sizeof(save));save.playTimeHours=30;error=1;
 LegendsClockCalcLocalTime();assert(gLocalTime.days==1&&gLocalTime.hours==15);
 error=0;LegendsClockCalcLocalTime();assert(gLocalTime.days==1&&gLocalTime.hours==0);
 puts("Device priority, live polling, manual clocks, invalid RTC, persisted fallback and 999-hour cap passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'clock.c';p.write_text(pre+source+post)
 subprocess.run(['cc','-std=gnu17','-Wall','-Werror','-fsanitize=address,undefined',str(p),'-o',d+'/clock'],check=True)
 subprocess.run([d+'/clock'],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
# Intro confirmation no longer resets time; adjustment remains at the bedroom.
scripts=(root/'data/scripts/players_house.inc').read_text()
assert 'special LegendsClockUseRealTime' in scripts and 'special LegendsClockBufferTime' in scripts
assert 'goto_if_eq VAR_RESULT, 0, PlayersHouse_2F_EventScript_ClockCancelled' in scripts
rtc=(root/'src/rtc.c').read_text()
assert 'RtcGetInfo(&sRtc); // Native calendar accessors' in rtc and 'LegendsClockCalcLocalTime();' in rtc
assert 'LegendsClockTick();' in (root/'src/play_time.c').read_text().split('if (sPlayTimeCounterState == MAXED_OUT)')[0]
assert 'LegendsUpdateStartMenuPanel();' in (root/'src/start_menu.c').read_text()

# Execute the actual room-entry branches for both genders and old/new saves.
labels={};current=None
for line in scripts.splitlines():
 line=line.strip()
 if line.endswith('::'):
  current=line[:-2];labels[current]=[]
 elif current and line and not line.startswith('.'):labels[current].append(line)
def room_action(entry,gender,clock_set):
 values={'MALE':0,'FEMALE':1,'VAR_RESULT':gender};label=entry;pc=0
 for _ in range(50):
  line=labels[label][pc];pc+=1;op,_,args=line.partition(' ')
  parts=[v.strip() for v in args.split(',')]
  if op=='checkplayergender':values['VAR_RESULT']=gender
  elif op=='setvar':values[parts[0]]=values[parts[1]]
  elif op=='goto':label=args;pc=0
  elif op=='goto_if_eq' and values[parts[0]]==values[parts[1]]:label=parts[2];pc=0
  elif op=='goto_if_set' and clock_set:label=parts[1];pc=0
  elif op=='call' and args=='PlayersHouse_2F_EventScript_ChooseClockMode':return 'choose'
  elif op=='special' and args=='Special_ViewWallClock':return 'view'
 raise AssertionError('Room clock did not reach a terminal action')
for gender in (0,1):
 for owner,name in enumerate(('Brendans','Mays')):
  for clock_set in (False,True):
   assert room_action(f'LittlerootTown_{name}House_2F_EventScript_WallClock',gender,clock_set)==('choose' if owner==gender else 'view')
