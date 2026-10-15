#include "global.h"
#include "legends_adventure.h"
#include "string_util.h"
#include "event_data.h"
#include "field_weather.h"
#include "legends_seasons.h"
#include "legends_start_menu.h"
#include "legends_journal.h"
#include "map_name_popup.h"
#include "menu.h"
#include "malloc.h"
#include "rtc.h"
#include "window.h"
#include "constants/map_types.h"
#include "constants/weather.h"
#include "constants/rtc.h"
#include "constants/characters.h"

// Framed bounds: x=0..111, y=0..87. The menu starts at x=128;
// the existing day/weather panel starts at y=88. BG0 tiles end below 0xE000.
// DexNav help reuses this tile range only after the reminder is removed.
static const struct WindowTemplate sReminderTemplate =
{
    .bg = 0, .tilemapLeft = 1, .tilemapTop = 1,
    .width = 12, .height = 9, .paletteNum = 15, .baseBlock = 0x250,
};
EWRAM_DATA static u8 sReminderHandle = 0;
// This scratch window is RAM-only: never install its tilemap or upload it.
static const struct WindowTemplate sReminderLineTemplate =
{
    .bg = 0, .width = 12, .height = 2, .paletteNum = 15,
};
#define REMINDER_BODY_TOP 12
#define REMINDER_BODY_HEIGHT 60
#define REMINDER_SCROLL_DELAY 120
#define REMINDER_SCROLL_PERIOD 3
EWRAM_DATA static u8 sReminderLineHandle = 0;
EWRAM_DATA static u8 sReminderScrollTick = 0;
EWRAM_DATA static u16 sReminderScrollOffset = 0;
EWRAM_DATA static u16 sReminderScrollLimit = 0;
EWRAM_DATA static u16 sReminderScrollPause = 0;
EWRAM_DATA static bool8 sReminderReturning = FALSE;
EWRAM_DATA static const u8 *sReminderTitle = NULL;
EWRAM_DATA static const u8 *sReminderObjective = NULL;
static const u8 sReminderLabelInk[] = {1, 8, 9};
static const u8 sReminderInk[] = {1, 2, 3};

struct ReminderLine { const u8 *text; u16 length; };
EWRAM_DATA static struct ReminderLine *sReminderLines = NULL;
enum { REMINDER_MEASURE, REMINDER_DRAW, REMINDER_CACHE };

static void ReminderLine(u8 windowId, const u8 *line, u16 lineY)
{
    s32 y = REMINDER_BODY_TOP + lineY - sReminderScrollOffset;
    s32 top, bottom, row, column;
    if (y >= REMINDER_BODY_TOP + REMINDER_BODY_HEIGHT || y + 12 <= REMINDER_BODY_TOP) return;
    if (!sReminderLineHandle)
    {
        AddTextPrinterParameterized3(windowId, FONT_SMALL, 4, y, sReminderInk, TEXT_SKIP_DRAW, line);
        return;
    }
    FillWindowPixelBuffer(sReminderLineHandle - 1, PIXEL_FILL(1));
    AddTextPrinterParameterized3(sReminderLineHandle - 1, FONT_SMALL, 4, 0, sReminderInk, TEXT_SKIP_DRAW, line);
    top = y < REMINDER_BODY_TOP ? REMINDER_BODY_TOP : y;
    bottom = y + 12 > REMINDER_BODY_TOP + REMINDER_BODY_HEIGHT ? REMINDER_BODY_TOP + REMINDER_BODY_HEIGHT : y + 12;
    // Both native 4bpp buffers are twelve tiles wide and word-aligned.
    // Copy complete eight-pixel rows instead of a per-pixel nibble blit.
    const u32 *src = (const u32 *)GetWindowAttribute(sReminderLineHandle - 1, WINDOW_TILE_DATA);
    u32 *dst = (u32 *)GetWindowAttribute(windowId, WINDOW_TILE_DATA);
    for (row = top; row < bottom; row++)
    {
        u32 srcRow = ((row - y) / 8) * 96 + (row - y) % 8;
        u32 dstRow = (row / 8) * 96 + row % 8;
        for (column = 0; column < 12; column++) dst[dstRow + column * 8] = src[srcRow + column * 8];
    }
}

static u16 ReminderText(u8 windowId, const u8 *text, u16 lineY, u8 mode)
{
    u8 line[128];
    u16 length, space, i;
    while (*text != EOS)
    {
        length = space = 0;
        while (text[length] != EOS && text[length] != CHAR_NEWLINE && length < sizeof(line) - 2)
        {
            line[length] = text[length]; line[length + 1] = EOS;
            if (GetStringWidth(FONT_SMALL, line, 0) > 88) break;
            if (text[length] == CHAR_SPACE) space = length;
            length++;
        }
        if (text[length] != EOS && text[length] != CHAR_NEWLINE && space) length = space;
        if (!length && *text != CHAR_NEWLINE) length = 1;
        if (mode == REMINDER_CACHE)
            sReminderLines[lineY / 12] = (struct ReminderLine){text, length};
        if (mode == REMINDER_DRAW)
        {
            for (i = 0; i < length; i++) line[i] = text[i];
            line[length] = EOS;
            ReminderLine(windowId, line, lineY);
        }
        lineY += 12;
        text += length;
        if (*text == CHAR_SPACE || *text == CHAR_NEWLINE) text++;
    }
    return lineY;
}

static void DrawReminderBody(void)
{
    u8 windowId = sReminderHandle - 1;
    u16 y;
    if (sReminderLines)
    {
        u8 text[128];
        u16 row, i;
        // Every viewport row is covered, including blank lines/background.
        for (row = sReminderScrollOffset / 12; row <= (sReminderScrollOffset + REMINDER_BODY_HEIGHT - 1) / 12; row++)
        {
            const struct ReminderLine *line = &sReminderLines[row];
            for (i = 0; i < line->length; i++) text[i] = line->text[i];
            text[line->length] = EOS;
            ReminderLine(windowId, text, row * 12);
        }
        return;
    }
    FillWindowPixelRect(windowId, PIXEL_FILL(1), 0, REMINDER_BODY_TOP, 96, REMINDER_BODY_HEIGHT);
    y = ReminderText(windowId, sReminderTitle, 0, REMINDER_DRAW);
    ReminderText(windowId, sReminderObjective, y, REMINDER_DRAW);
}

void LegendsUpdateTrackedQuestReminder(void)
{
    if (!sReminderHandle || !sReminderScrollLimit) return;
    if (sReminderScrollPause)
    {
        sReminderScrollPause--;
        return;
    }
    if (++sReminderScrollTick < REMINDER_SCROLL_PERIOD) return;
    sReminderScrollTick = 0;
    if (sReminderReturning)
        sReminderScrollOffset--;
    else
        sReminderScrollOffset++;
    if (!sReminderScrollOffset || sReminderScrollOffset == sReminderScrollLimit)
    {
        sReminderReturning = !sReminderReturning;
        sReminderScrollPause = REMINDER_SCROLL_DELAY;
    }
    DrawReminderBody();
    CopyWindowToVram(sReminderHandle - 1, COPYWIN_GFX);
}

void LegendsShowTrackedQuestReminder(void)
{
    u16 id;
    u8 windowId, step;
    u16 height;
    const struct LegendsQuest *quest;
    if (sReminderHandle || IsMapNamePopupActive()) return;
    id = LegendsQuestTracked();
    if (id == 0xFFFF) return;
    quest = LegendsQuestGet(id);
    step = LegendsQuestNextStep(id);
    if (!quest || step >= quest->count) return;
    sReminderTitle = quest->title;
    sReminderObjective = quest->steps[step].text;
    sReminderScrollOffset = sReminderScrollTick = 0;
    sReminderReturning = FALSE;
    sReminderScrollPause = REMINDER_SCROLL_DELAY;
    height = ReminderText(0, sReminderTitle, 0, REMINDER_MEASURE);
    height = ReminderText(0, sReminderObjective, height, REMINDER_MEASURE);
    sReminderScrollLimit = height > REMINDER_BODY_HEIGHT ? height - REMINDER_BODY_HEIGHT : 0;
    if (sReminderScrollLimit)
    {
        sReminderLines = AllocZeroed((height / 12) * sizeof(*sReminderLines));
        if (!sReminderLines) return;
        height = ReminderText(0, sReminderTitle, 0, REMINDER_CACHE);
        ReminderText(0, sReminderObjective, height, REMINDER_CACHE);
    }
    LegendsAchievementPopupHide();
    windowId = AddWindow(&sReminderTemplate);
    if (windowId == WINDOW_NONE)
    {
        Free(sReminderLines); sReminderLines = NULL;
        return;
    }
    sReminderHandle = windowId + 1;
    if (sReminderScrollLimit)
    {
        windowId = AddWindow(&sReminderLineTemplate);
        if (windowId == WINDOW_NONE)
        {
            RemoveWindow(sReminderHandle - 1);
            sReminderHandle = 0;
            Free(sReminderLines); sReminderLines = NULL;
            return;
        }
        sReminderLineHandle = windowId + 1;
    }
    windowId = sReminderHandle - 1;
    DrawStdWindowFrame(windowId, FALSE);
    AddTextPrinterParameterized3(windowId, FONT_SMALL, 4, 0, sReminderLabelInk, TEXT_SKIP_DRAW, COMPOUND_STRING("TRACKED QUEST"));
    FillWindowPixelRect(windowId, PIXEL_FILL(3), 4, 11, 88, 1);
    DrawReminderBody();
    CopyWindowToVram(windowId, COPYWIN_FULL);
}

void LegendsHideTrackedQuestReminder(void)
{
    Free(sReminderLines);
    sReminderLines = NULL;
    if (sReminderLineHandle)
    {
        RemoveWindow(sReminderLineHandle - 1);
        sReminderLineHandle = 0;
    }
    sReminderScrollOffset = sReminderScrollLimit = sReminderScrollTick = sReminderScrollPause = 0;
    sReminderReturning = FALSE;
    sReminderTitle = sReminderObjective = NULL;
    if (!sReminderHandle) return;
    ClearStdWindowAndFrameToTransparent(sReminderHandle - 1, TRUE);
    RemoveWindow(sReminderHandle - 1);
    sReminderHandle = 0;
}

// This gap sits below the map-name popup and above the save/counter tiles.
static const struct WindowTemplate sPanelTemplate =
{
    .bg = 0, .tilemapLeft = 1, .tilemapTop = 12,
    .width = 12, .height = 6, .paletteNum = 15, .baseBlock = 0xB8,
};

enum PanelIcon
{
    ICON_CLOCK, ICON_SUN, ICON_CLOUD, ICON_RAIN, ICON_THUNDER,
    ICON_SNOW, ICON_FOG, ICON_ASH, ICON_SAND, ICON_WATER, ICON_INDOOR, ICON_MOON,
};

// Twelve-pixel icons reuse native text colors; no sprite/palette slots.
static const u16 sIcons[][12] =
{
    [ICON_MOON]    = {0x0E0,0x1C2,0x380,0x700,0x700,0x700,0x700,0x380,0x1C0,0x0F0,0x07C,0},
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
EWRAM_DATA static u16 sLastDay = 0;
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
    case WEATHER_DROUGHT: return ICON_SUN;
    default: return GetTimeOfDay() == TIME_NIGHT ? ICON_MOON : ICON_SUN;
    }
}

// Native palette indices: white 1, dark/light gray 2/3, warm gold 5,
// blue/light blue 8/9. Keep the palette itself intact for other menu windows.
static u8 GetIconColor(u8 icon, u8 row)
{
    switch (icon)
    {
    case ICON_SUN: return 5;
    case ICON_MOON: return 9;
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
        if (sAnimationPhase && icon == ICON_MOON && row == 1)
            bits ^= 0x005; // A tiny star twinkle beside the crescent.
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
    FillWindowPixelRect(windowId, PIXEL_FILL(1), 4, 34, 12, 12);
    DrawIcon(windowId, sLastIcon, 34);
    CopyWindowToVram(windowId, COPYWIN_GFX);
}

void LegendsUpdateStartMenuPanel(void)
{
    u8 timeText[24];
    u8 dayText[20];
    u16 day;
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
    clockValid = TRUE; // Effective clock includes the final-priority played-time fallback.
    hour = minute = 0;
    if (clockValid)
    {
        RtcCalcLocalTime();
        hour = gLocalTime.hours;
        minute = gLocalTime.minutes;
        clockValid = hour < 24 && minute < 60;
    }
    LegendsAdventureUpdateDay();
    day = LegendsAdventureDays();
    icon = GetWeatherIcon();
    // Observe the displayed environment; opening the menu must not commit a season.
    season = LegendsGetActiveSeason();
    if (sHasSnapshot && hour == sLastHour && minute == sLastMinute
     && icon == sLastIcon && season == sLastSeason && clockValid == sLastClockValid && day == sLastDay)
        return;
    sLastDay = day;
    sLastHour = hour;
    sLastMinute = minute;
    sLastIcon = icon;
    sLastSeason = season;
    sLastClockValid = clockValid;
    sHasSnapshot = TRUE;

    windowId = sWindowHandle - 1;
    FillWindowPixelBuffer(windowId, PIXEL_FILL(1));
    StringCopy(dayText, COMPOUND_STRING("DAY "));
    ConvertIntToDecimalStringN(dayText + 4, day, STR_CONV_MODE_LEFT_ALIGN, 5);
    AddTextPrinterParameterized(windowId, FONT_SMALL, dayText, 4, 0, TEXT_SKIP_DRAW, NULL);
    DrawIcon(windowId, ICON_CLOCK, 18);
    DrawIcon(windowId, icon, 34);
    if (clockValid)
        FormatDecimalTimeWithoutSeconds(timeText, hour, minute, FALSE);
    AddTextPrinterParameterized(windowId, FONT_SMALL,
        clockValid ? timeText : COMPOUND_STRING("--:--"), 23, 16, TEXT_SKIP_DRAW, NULL);
    AddTextPrinterParameterized(windowId, FONT_SMALL,
        LegendsGetSeasonName(season), 23, 32, TEXT_SKIP_DRAW, NULL);
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
    LegendsHideTrackedQuestReminder();
    if (sWindowHandle == 0)
        return;
    ClearStdWindowAndFrameToTransparent(sWindowHandle - 1, TRUE);
    RemoveWindow(sWindowHandle - 1);
    sWindowHandle = 0;
}
