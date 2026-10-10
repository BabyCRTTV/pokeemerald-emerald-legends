#include "global.h"
#include "legends_clock.h"
#include "event_data.h"
#include "rtc.h"
#include "string_util.h"
#include "constants/vars.h"

#define CLOCK_INIT 0xC132
#define CLOCK_DATE_PENDING 0xFFFF
#define SECONDS_PER_DAY 86400

static u32 PlayedSeconds(void)
{
    return VarGet(VAR_LEGENDS_CLOCK_SECONDS_LO) | ((u32)VarGet(VAR_LEGENDS_CLOCK_SECONDS_HI) << 16);
}

static void StoreSeconds(u32 seconds)
{
    VarSet(VAR_LEGENDS_CLOCK_SECONDS_LO, seconds);
    VarSet(VAR_LEGENDS_CLOCK_SECONDS_HI, seconds >> 16);
}

static void EnsureClock(void)
{
    u16 previous = VarGet(VAR_LEGENDS_CLOCK_INIT);
    if (previous == CLOCK_INIT)
        return;
    // Retain the pre-release counter if this save already has it.
    if (previous != 0xC131)
    {
        StoreSeconds((u32)gSaveBlock2Ptr->playTimeHours * 3600
            + gSaveBlock2Ptr->playTimeMinutes * 60 + gSaveBlock2Ptr->playTimeSeconds);
        VarSet(VAR_LEGENDS_CLOCK_FRAMES, gSaveBlock2Ptr->playTimeVBlanks < 60 ? gSaveBlock2Ptr->playTimeVBlanks : 0);
    }
    VarSet(VAR_LEGENDS_CLOCK_DAY_ORIGIN, CLOCK_DATE_PENDING);
    VarSet(VAR_LEGENDS_CLOCK_INIT, CLOCK_INIT);
}

void LegendsClockTick(void)
{
    u16 frames;
    EnsureClock();
    frames = VarGet(VAR_LEGENDS_CLOCK_FRAMES) + 1;
    if (frames >= 60)
    {
        frames = 0;
        StoreSeconds(PlayedSeconds() + 1);
    }
    VarSet(VAR_LEGENDS_CLOCK_FRAMES, frames);
}

static bool8 ReadDeviceClock(struct SiiRtcInfo *rtc)
{
    u32 year, month, day;
    if (RtcGetErrorStatus() & (RTC_ERR_FLAG_MASK | RTC_INIT_ERROR))
        return FALSE;
    RtcGetInfo(rtc);
    year = ConvertBcdToBinary(rtc->year);
    month = ConvertBcdToBinary(rtc->month);
    day = ConvertBcdToBinary(rtc->day);
    return year <= 99 && month >= 1 && month <= 12 && day >= 1
        && day <= sNumDaysInMonths[month - 1] + (month == 2 && IsLeapYear(year))
        && ConvertBcdToBinary(rtc->hour) < 24
        && ConvertBcdToBinary(rtc->minute) < 60 && ConvertBcdToBinary(rtc->second) < 60;
}

static u16 GetDayOrigin(struct SiiRtcInfo *rtc)
{
    u16 origin = VarGet(VAR_LEGENDS_CLOCK_DAY_ORIGIN);
    if (origin == CLOCK_DATE_PENDING)
    {
        struct Time *offset = &gSaveBlock2Ptr->localTimeOffset;
        u16 date = RtcGetDayCount(rtc);
        if (offset->days || offset->hours || offset->minutes || offset->seconds)
        {
            struct Time legacy;
            // Include native hour/day borrowing when migrating an old clock.
            RtcCalcTimeDifference(rtc, &legacy, offset);
            origin = date - legacy.days;
        }
        else
            origin = date - (PlayedSeconds() + 9 * 3600) / SECONDS_PER_DAY;
        VarSet(VAR_LEGENDS_CLOCK_DAY_ORIGIN, origin);
    }
    return origin;
}

void LegendsClockCalcLocalTime(void)
{
    struct SiiRtcInfo rtc;
    struct Time zero = {0};
    u32 seconds;
    EnsureClock();
    if (ReadDeviceClock(&rtc))
    {
        zero.days = GetDayOrigin(&rtc);
        if (VarGet(VAR_LEGENDS_CLOCK_MODE) == 1 && !VarGet(VAR_LEGENDS_MANUAL_RTC_READY))
        {
            u32 manual = (PlayedSeconds() + 9 * 3600 + VarGet(VAR_LEGENDS_MANUAL_OFFSET) * 60) % SECONDS_PER_DAY;
            RtcCalcTimeDifference(&rtc, &gLocalTime, &zero);
            RtcCalcLocalTimeOffset(gLocalTime.days, manual / 3600, manual / 60 % 60, manual % 60);
            VarSet(VAR_LEGENDS_MANUAL_RTC_READY, 1);
        }
        // Real time never inherits the introductory clock's saved offset.
        RtcCalcTimeDifference(&rtc, &gLocalTime,
            VarGet(VAR_LEGENDS_CLOCK_MODE) == 1 ? &gSaveBlock2Ptr->localTimeOffset : &zero);
        return;
    }
    seconds = PlayedSeconds() + 9 * 3600;
    if (VarGet(VAR_LEGENDS_CLOCK_MODE) == 1)
        seconds += VarGet(VAR_LEGENDS_MANUAL_OFFSET) * 60;
    gLocalTime.days = seconds / SECONDS_PER_DAY;
    seconds %= SECONDS_PER_DAY;
    gLocalTime.hours = seconds / 3600;
    gLocalTime.minutes = seconds / 60 % 60;
    gLocalTime.seconds = seconds % 60;
}

void LegendsClockSetManual(u8 hour, u8 minute)
{
    struct SiiRtcInfo rtc;
    u32 current, chosen;
    EnsureClock();
    current = (PlayedSeconds() + 9 * 3600) % SECONDS_PER_DAY;
    chosen = hour * 3600 + minute * 60;
    // Minute offset fits a u16 and advances with played time if RTC is absent.
    VarSet(VAR_LEGENDS_MANUAL_OFFSET, (chosen / 60 + 1440 - current / 60) % 1440);
    if (ReadDeviceClock(&rtc))
    {
        struct Time dayOrigin = {0};
        dayOrigin.days = GetDayOrigin(&rtc);
        RtcCalcTimeDifference(&rtc, &gLocalTime, &dayOrigin);
        RtcCalcLocalTimeOffset(gLocalTime.days, hour, minute, 0);
        VarSet(VAR_LEGENDS_MANUAL_RTC_READY, 1);
    }
    else
        VarSet(VAR_LEGENDS_MANUAL_RTC_READY, 0);
    VarSet(VAR_LEGENDS_CLOCK_MODE, 1);
}

void LegendsClockBufferTime(void)
{
    RtcCalcLocalTime();
    FormatDecimalTimeWithoutSeconds(gStringVar1, gLocalTime.hours, gLocalTime.minutes, FALSE);
}

void LegendsClockUseRealTime(void)
{
    VarSet(VAR_LEGENDS_CLOCK_MODE, 0);
    RtcCalcLocalTime();
}
