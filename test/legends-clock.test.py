"""Compile actual effective-clock service: device priority, manual offsets,
invalid RTC, saved fallback ticks, pause-menu polling and the native timer cap.
"""
from pathlib import Path
import subprocess,tempfile,os
root=Path(__file__).resolve().parents[1]
rtc_source=(root/'src/rtc.c').read_text()
start=rtc_source.index('void RtcGetInfo(struct SiiRtcInfo *rtc)')
rtc_get_info=rtc_source[start:rtc_source.index('\n}',start)+2]
source='\n'.join(l for l in (root/'src/legends_clock.c').read_text().splitlines() if not l.startswith('#include'))
pre=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int bool8;
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
struct Time {int days,hours,minutes,seconds;}gLocalTime;
struct SiiRtcInfo {u8 year,month,day,hour,minute,second;};
struct {u16 playTimeHours;u8 playTimeMinutes,playTimeSeconds;struct Time localTimeOffset;}save,*gSaveBlock2Ptr=&save;
static u16 vars[7],error;static struct SiiRtcInfo device={26,10,10,13,41,59};
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
void RtcCalcTimeDifference(struct SiiRtcInfo*r,struct Time*out,struct Time*offset){
 int seconds=r->hour*3600+r->minute*60+r->second-offset->hours*3600-offset->minutes*60-offset->seconds;
 seconds=(seconds+86400)%86400;out->days=9000-offset->days;out->hours=seconds/3600;out->minutes=seconds/60%60;out->seconds=seconds%60;
}
void RtcCalcLocalTimeOffset(int days,int h,int m,int sec){
 int seconds=device.hour*3600+device.minute*60+device.second-h*3600-m*60-sec;
 save.localTimeOffset.days=9000-days;
 save.localTimeOffset.hours=seconds/3600;save.localTimeOffset.minutes=seconds/60%60;save.localTimeOffset.seconds=seconds%60;
}
u8 gStringVar1[32];
void RtcCalcLocalTime(void);
void FormatDecimalTimeWithoutSeconds(u8*d,int h,int m,int fmt){sprintf((char*)d,"%02d:%02d",h,m);}
'''
pre=pre.replace('__RTC_GET_INFO__',rtc_get_info)
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
 LegendsClockSetManual(18,30);LegendsClockCalcLocalTime();assert(gLocalTime.hours==18&&gLocalTime.minutes==30);
 device.minute=43;LegendsClockCalcLocalTime();assert(gLocalTime.minutes==31);
 LegendsClockUseRealTime();assert(gLocalTime.hours==13&&gLocalTime.minutes==43);
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
