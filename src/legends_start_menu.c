#include "global.h"
#include "event_data.h"
#include "field_weather.h"
#include "legends_seasons.h"
#include "legends_start_menu.h"
#include "menu.h"
#include "rtc.h"
#include "window.h"
#include "constants/map_types.h"
#include "constants/weather.h"

// This gap sits below the map-name popup and above the save/counter tiles.
static const struct WindowTemplate sPanelTemplate =
{
    .bg = 0, .tilemapLeft = 1, .tilemapTop = 14,
    .width = 12, .height = 4, .paletteNum = 15, .baseBlock = 0xC0,
};

enum PanelIcon
{
    ICON_CLOCK, ICON_SUN, ICON_CLOUD, ICON_RAIN, ICON_THUNDER,
    ICON_SNOW, ICON_FOG, ICON_ASH, ICON_SAND, ICON_WATER, ICON_INDOOR,
};

// Twelve-pixel icons reuse native text colors; no sprite/palette slots.
static const u16 sIcons[][12] =
{
    [ICON_CLOCK]   = {0x1F8,0x306,0x402,0x841,0x841,0x841,0x879,0x801,0x402,0x306,0x1F8,0},
    [ICON_SUN]     = {0x090,0x492,0x000,0x1F8,0x204,0xA05,0x204,0x1F8,0,0x492,0x090,0},
    [ICON_CLOUD]   = {0,0,0x0F0,0x108,0x3CC,0x402,0x801,0x801,0x7FE,0,0,0},
    [ICON_RAIN]    = {0x0F0,0x108,0x3CC,0x402,0x801,0x7FE,0,0x222,0x444,0,0x222,0x444},
    [ICON_THUNDER]= {0x0F0,0x108,0x3CC,0x402,0x801,0x7FE,0x060,0x0C0,0x1E0,0x060,0x0C0,0x180},
    [ICON_SNOW]   = {0x090,0x492,0x294,0x198,0x090,0xFFF,0x090,0x198,0x294,0x492,0x090,0},
    [ICON_FOG]    = {0,0x7FE,0,0x1F8,0,0xFFF,0,0x3FC,0,0x7FE,0,0},
    [ICON_ASH]    = {0x040,0x000,0x208,0,0x092,0,0x400,0x021,0,0x104,0,0x040},
    [ICON_SAND]   = {0,0x3E0,0x010,0xFFF,0,0x002,0x7FE,0,0x070,0x080,0xFFF,0},
    [ICON_WATER]  = {0x060,0x0F0,0x198,0x30C,0x606,0x402,0x801,0x801,0x801,0x402,0x3FC,0},
    [ICON_INDOOR] = {0x060,0x0F0,0x198,0x30C,0x606,0xFFF,0x402,0x462,0x462,0x462,0x7FE,0},
};

// Zero means absent, avoiding a nonzero mutable initializer in the ROM build.
EWRAM_DATA static u8 sWindowHandle = 0;
EWRAM_DATA static u8 sRefreshFrames = 0;
EWRAM_DATA static u8 sAnimationFrames = 0;
EWRAM_DATA static u8 sAnimationPhase = 0;
EWRAM_DATA static u8 sLastHour = 0;
EWRAM_DATA static u8 sLastMinute = 0;
EWRAM_DATA static u8 sLastIcon = 0;
EWRAM_DATA static u8 sLastSeason = 0;
EWRAM_DATA static bool8 sLastClockValid = FALSE;
EWRAM_DATA static bool8 sHasSnapshot = FALSE;

static u8 GetWeatherIcon(void)
{
    if (gMapHeader.mapType == MAP_TYPE_INDOOR || gMapHeader.mapType == MAP_TYPE_SECRET_BASE
     || gMapHeader.mapType == MAP_TYPE_UNDERGROUND)
        return ICON_INDOOR;
    if (gMapHeader.mapType == MAP_TYPE_UNDERWATER)
        return ICON_WATER;

    switch (GetCurrentWeather())
    {
    case WEATHER_SUNNY_CLOUDS:
    case WEATHER_SHADE: return ICON_CLOUD;
    case WEATHER_RAIN:
    case WEATHER_DOWNPOUR: return ICON_RAIN;
    case WEATHER_RAIN_THUNDERSTORM: return ICON_THUNDER;
    case WEATHER_SNOW: return ICON_SNOW;
    case WEATHER_FOG_HORIZONTAL:
    case WEATHER_FOG_DIAGONAL:
    case WEATHER_FOG: return ICON_FOG;
    case WEATHER_VOLCANIC_ASH: return ICON_ASH;
    case WEATHER_SANDSTORM: return ICON_SAND;
    case WEATHER_UNDERWATER:
    case WEATHER_UNDERWATER_BUBBLES: return ICON_WATER;
    case WEATHER_ABNORMAL: return ICON_THUNDER;
    default: return ICON_SUN;
    }
}

// Native palette indices: white 1, dark/light gray 2/3, warm gold 5,
// blue/light blue 8/9. Keep the palette itself intact for other menu windows.
static u8 GetIconColor(u8 icon, u8 row)
{
    switch (icon)
    {
    case ICON_SUN: return 5;
    case ICON_RAIN: return row < 6 ? 3 : 8;
    case ICON_THUNDER: return row < 6 ? 3 : 5;
    case ICON_SNOW: return 9;
    case ICON_FOG: return 3;
    case ICON_SAND: return 5;
    case ICON_WATER: return 8;
    case ICON_CLOUD: return 3;
    default: return 2;
    }
}

static void DrawIcon(u8 windowId, u8 icon, u8 y)
{
    u32 row, column, sourceRow;
    u16 bits;
    u8 color;
    for (row = 0; row < 12; row++)
    {
        sourceRow = row;
        // Rain/ash descend, fog/sand drift, and the sun's rays shimmer.
        if (sAnimationPhase && icon == ICON_RAIN && row >= 7)
            sourceRow = row == 7 ? 11 : row - 1;
        if (sAnimationPhase && icon == ICON_ASH)
            sourceRow = row == 0 ? 11 : row - 1;
        bits = sIcons[icon][sourceRow];
        if (sAnimationPhase && (icon == ICON_FOG || icon == ICON_SAND || icon == ICON_SNOW))
            bits = ((bits << 1) | (bits >> 11)) & 0xFFF;
        if (sAnimationPhase && icon == ICON_SUN && (row < 3 || row > 8))
            bits = ((bits << 1) | (bits >> 11)) & 0xFFF;
        color = GetIconColor(icon, row);
        if (sAnimationPhase && icon == ICON_THUNDER && row >= 6)
            color = 3; // Dim the bolt rather than flashing the whole panel.
        if (sAnimationPhase && (icon == ICON_SNOW || icon == ICON_WATER))
            color = 9;
        if (icon == ICON_SUN && row >= 4 && row <= 6)
            bits |= 0x1F8; // Filled sun, with a soft native gold tone.
        for (column = 0; column < 12; column++)
            if (bits & (1 << (11 - column)))
                FillWindowPixelRect(windowId, PIXEL_FILL(color), 4 + column, y + row, 1, 1);
    }
}

static void AnimateWeatherIcon(void)
{
    u8 windowId;
    if (!sHasSnapshot)
        return;
    if (++sAnimationFrames < 30)
        return;
    sAnimationFrames = 0;
    sAnimationPhase ^= 1;
    // Sheltered locations have a static icon. No RTC reads for animation.
    if (sLastIcon == ICON_INDOOR || sLastIcon == ICON_CLOUD)
        return;
    windowId = sWindowHandle - 1;
    FillWindowPixelRect(windowId, PIXEL_FILL(1), 4, 18, 12, 12);
    DrawIcon(windowId, sLastIcon, 18);
    CopyWindowToVram(windowId, COPYWIN_GFX);
}

void LegendsUpdateStartMenuPanel(void)
{
    u8 timeText[24];
    u8 hour, minute, icon, season, windowId;
    bool8 clockValid;

    if (sWindowHandle == 0)
        return;
    AnimateWeatherIcon();
    if (sRefreshFrames != 0)
    {
        sRefreshFrames--;
        return;
    }
    sRefreshFrames = 59;
    clockValid = !(RtcGetErrorStatus() & (RTC_ERR_FLAG_MASK | RTC_INIT_ERROR));
    hour = minute = 0;
    if (clockValid)
    {
        RtcCalcLocalTime();
        hour = gLocalTime.hours;
        minute = gLocalTime.minutes;
        clockValid = hour < 24 && minute < 60;
    }
    icon = GetWeatherIcon();
    // Observe the displayed environment; opening the menu must not commit a season.
    season = LegendsGetActiveSeason();
    if (sHasSnapshot && hour == sLastHour && minute == sLastMinute
     && icon == sLastIcon && season == sLastSeason && clockValid == sLastClockValid)
        return;
    sLastHour = hour;
    sLastMinute = minute;
    sLastIcon = icon;
    sLastSeason = season;
    sLastClockValid = clockValid;
    sHasSnapshot = TRUE;

    windowId = sWindowHandle - 1;
    FillWindowPixelBuffer(windowId, PIXEL_FILL(1));
    DrawIcon(windowId, ICON_CLOCK, 2);
    DrawIcon(windowId, icon, 18);
    if (clockValid)
        FormatDecimalTimeWithoutSeconds(timeText, hour, minute, FALSE);
    AddTextPrinterParameterized(windowId, FONT_SMALL,
        clockValid ? timeText : COMPOUND_STRING("--:--"), 23, 0, TEXT_SKIP_DRAW, NULL);
    AddTextPrinterParameterized(windowId, FONT_SMALL,
        LegendsGetSeasonName(season), 23, 16, TEXT_SKIP_DRAW, NULL);
    CopyWindowToVram(windowId, COPYWIN_GFX);
}

void LegendsShowStartMenuPanel(void)
{
    u32 windowId;
    if (sWindowHandle != 0)
        return;
    windowId = AddWindow(&sPanelTemplate);
    if (windowId == WINDOW_NONE)
        return;
    sWindowHandle = windowId + 1;
    sRefreshFrames = 0;
    sHasSnapshot = FALSE;
    sAnimationFrames = 0;
    sAnimationPhase = 0;
    PutWindowTilemap(windowId);
    DrawStdWindowFrame(windowId, FALSE);
    LegendsUpdateStartMenuPanel();
    CopyWindowToVram(windowId, COPYWIN_FULL);
}

void LegendsHideStartMenuPanel(void)
{
    if (sWindowHandle == 0)
        return;
    ClearStdWindowAndFrameToTransparent(sWindowHandle - 1, TRUE);
    RemoveWindow(sWindowHandle - 1);
    sWindowHandle = 0;
}
