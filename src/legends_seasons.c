#include "global.h"
#include "legends_seasons.h"
#include "event_data.h"
#include "field_weather.h"
#include "overworld.h"
#include "palette.h"
#include "rtc.h"
#include "constants/map_types.h"
#include "constants/region_map_sections.h"
#include "constants/weather.h"
#include "constants/rgb.h"

// All state lives in unused permanent vars: saves retain their existing layout.
static u32 GetCycleSeconds(void)
{
    u32 seconds;
    if (VarGet(VAR_LEGENDS_SEASON_CLOCK_INIT) != 1)
    {
        seconds = (gSaveBlock2Ptr->playTimeHours * 3600u
                 + gSaveBlock2Ptr->playTimeMinutes * 60u
                 + gSaveBlock2Ptr->playTimeSeconds) % LEGENDS_SEASON_CYCLE_SECONDS;
        VarSet(VAR_LEGENDS_SEASON_SECONDS_LO, seconds);
        VarSet(VAR_LEGENDS_SEASON_SECONDS_HI, seconds >> 16);
        VarSet(VAR_LEGENDS_SEASON_FRAMES, gSaveBlock2Ptr->playTimeVBlanks % 60);
        VarSet(VAR_LEGENDS_SEASON_CLOCK_INIT, 1);
    }
    seconds = VarGet(VAR_LEGENDS_SEASON_SECONDS_LO)
            | ((u32)VarGet(VAR_LEGENDS_SEASON_SECONDS_HI) << 16);
    return seconds % LEGENDS_SEASON_CYCLE_SECONDS;
}

u8 LegendsGetSeasonMode(void)
{
    return VarGet(VAR_LEGENDS_SEASON_MODE) == LEGENDS_SEASONS_PLAYTIME
         ? LEGENDS_SEASONS_PLAYTIME : LEGENDS_SEASONS_RTC;
}

void LegendsSetSeasonMode(u8 mode)
{
    GetCycleSeconds();
    VarSet(VAR_LEGENDS_SEASON_MODE, mode < LEGENDS_SEASON_MODE_COUNT ? mode : LEGENDS_SEASONS_RTC);
}

void LegendsSetPlaytimeSeason(u8 season)
{
    u32 seconds;
    if (LegendsGetSeasonMode() != LEGENDS_SEASONS_PLAYTIME || season >= LEGENDS_SEASON_COUNT)
        return;
    seconds = season * LEGENDS_SEASON_SECONDS;
    VarSet(VAR_LEGENDS_SEASON_SECONDS_LO, seconds);
    VarSet(VAR_LEGENDS_SEASON_SECONDS_HI, seconds >> 16);
    VarSet(VAR_LEGENDS_SEASON_FRAMES, 0);
    VarSet(VAR_LEGENDS_SEASON_CLOCK_INIT, 1);
    // Keep the visible season until the next fully faded map load.
}

u8 LegendsGetSeasonForMode(u8 mode)
{
    struct SiiRtcInfo rtc;
    u32 month;
    if (mode == LEGENDS_SEASONS_PLAYTIME)
        return GetCycleSeconds() / LEGENDS_SEASON_SECONDS;

    // Use the RTC's calendar, not the bedroom clock's local-time offset.
    RtcGetInfo(&rtc);
    month = ConvertBcdToBinary(rtc.month);
    if (RtcGetErrorStatus() & (RTC_ERR_FLAG_MASK | RTC_INIT_ERROR) || month < 1 || month > 12)
        return GetCycleSeconds() / LEGENDS_SEASON_SECONDS;
    if (month >= 3 && month <= 5)
        return LEGENDS_SPRING;
    if (month >= 6 && month <= 8)
        return LEGENDS_SUMMER;
    if (month >= 9 && month <= 11)
        return LEGENDS_AUTUMN;
    return LEGENDS_WINTER;
}

u8 LegendsGetSeason(void)
{
    return LegendsGetSeasonForMode(LegendsGetSeasonMode());
}

// Commit only while loading a fully faded map (never a seamless route edge).
// Both foliage and ambient weather use this saved snapshot until the next warp.
void LegendsCommitSeasonTransition(void)
{
    struct SiiRtcInfo rtc;
    u32 day = GetCycleSeconds() / LEGENDS_SEASON_SECONDS;
    if (LegendsGetSeasonMode() == LEGENDS_SEASONS_RTC
     && !(RtcGetErrorStatus() & (RTC_ERR_FLAG_MASK | RTC_INIT_ERROR)))
    {
        RtcGetInfo(&rtc);
        if (ConvertBcdToBinary(rtc.month) >= 1 && ConvertBcdToBinary(rtc.month) <= 12)
            day = RtcGetDayCount(&rtc);
    }
    VarSet(VAR_LEGENDS_ACTIVE_SEASON, LegendsGetSeason() + 1);
    VarSet(VAR_LEGENDS_SEASON_WEATHER_DAY, day);
}

u8 LegendsGetActiveSeason(void)
{
    u16 season = VarGet(VAR_LEGENDS_ACTIVE_SEASON);
    if (season < 1 || season > LEGENDS_SEASON_COUNT)
    {
        // New games and pre-0.0.12 saves initialize at their first field load.
        LegendsCommitSeasonTransition();
        season = VarGet(VAR_LEGENDS_ACTIVE_SEASON);
    }
    return season - 1;
}

const u8 *LegendsGetSeasonName(u8 season)
{
    static const u8 *const names[] =
    {
        COMPOUND_STRING("SPRING"), COMPOUND_STRING("SUMMER"),
        COMPOUND_STRING("AUTUMN"), COMPOUND_STRING("WINTER"),
    };
    return names[season < LEGENDS_SEASON_COUNT ? season : LEGENDS_SPRING];
}

void LegendsSeasonTick(void)
{
    u32 seconds = GetCycleSeconds();
    u16 frames = VarGet(VAR_LEGENDS_SEASON_FRAMES) + 1;
    if (frames >= 60)
    {
        frames = 0;
        seconds = (seconds + 1) % LEGENDS_SEASON_CYCLE_SECONDS;
        VarSet(VAR_LEGENDS_SEASON_SECONDS_LO, seconds);
        VarSet(VAR_LEGENDS_SEASON_SECONDS_HI, seconds >> 16);
    }
    VarSet(VAR_LEGENDS_SEASON_FRAMES, frames);
}

bool32 LegendsMapHasSeasons(void)
{
    if (gMapHeader.mapType != MAP_TYPE_TOWN && gMapHeader.mapType != MAP_TYPE_CITY
     && gMapHeader.mapType != MAP_TYPE_ROUTE && gMapHeader.mapType != MAP_TYPE_OCEAN_ROUTE)
        return FALSE;
    // Preserve the volcanic belt, ash fields, hot springs and desert ecosystem.
    switch (gMapHeader.regionMapSectionId)
    {
    case MAPSEC_MT_CHIMNEY:
    case MAPSEC_JAGGED_PASS:
    case MAPSEC_FIERY_PATH:
    case MAPSEC_LAVARIDGE_TOWN:
    case MAPSEC_FALLARBOR_TOWN:
    case MAPSEC_ROUTE_111:
    case MAPSEC_ROUTE_112:
    case MAPSEC_ROUTE_113:
        return FALSE;
    }
    return gMapHeader.weather != WEATHER_VOLCANIC_ASH
        && gMapHeader.weather != WEATHER_SANDSTORM;
}

u16 LegendsSeasonVegetationColor(u16 color, u8 season)
{
    u32 r = color & 31, g = (color >> 5) & 31, b = (color >> 10) & 31;
    if (g < r + 3 || g < b + 2 || g < 7)
        return color;
    switch (season)
    {
    case LEGENDS_SPRING:
        r = (r * 7 + 18) / 8; g = (g * 7 + 31) / 8; b = (b * 7 + 12) / 8;
        break;
    case LEGENDS_SUMMER:
        r = r * 7 / 8; g = g * 15 / 16; b = b * 7 / 8;
        break;
    case LEGENDS_AUTUMN:
        r = (g * 7 + 31) / 8; b = (b + g) / 4; g = g * 3 / 4;
        break;
    case LEGENDS_WINTER:
        r = (g * 3 + 31 * 2) / 5; b = (g * 3 + 31 * 2) / 5; g = (g * 3 + 30 * 2) / 5;
        break;
    }
    return RGB(r, g, b);
}

void LegendsApplySeasonPalette(u16 offset, u16 count)
{
    u32 i;
    u8 season;
    if (!LegendsMapHasSeasons())
        return;
    season = LegendsGetActiveSeason();
    for (i = offset; i < offset + count && i < 13 * 16; i++)
        if (i >= 16 && (i & 15) != 0)
            gPlttBufferUnfaded[i] = LegendsSeasonVegetationColor(gPlttBufferUnfaded[i], season);
}

void LegendsApplyGrassPalette(u8 slot, const u16 *source)
{
    u32 i;
    bool32 seasonal = LegendsMapHasSeasons();
    u8 season = seasonal ? LegendsGetActiveSeason() : LEGENDS_SPRING;
    if (slot >= 16)
        return;
    for (i = 1; i < 16; i++)
    {
        u32 offset = (16 + slot) * 16 + i;
        // LoadSpritePalette caches an existing tag. Always start from native art,
        // including connected transitions from a seasonal map to an excluded one.
        gPlttBufferUnfaded[offset] = seasonal ? LegendsSeasonVegetationColor(source[i], season) : source[i];
    }
}

u8 LegendsSeasonWeather(u8 weather)
{
    u8 season;
    u32 day, roll;
    if (!LegendsMapHasSeasons())
        return weather;
    // Only ordinary ambient weather participates. Scripts retain drought,
    // downpours, story conflict, ash, sand, underwater and special effects.
    if (weather != WEATHER_SUNNY && weather != WEATHER_SUNNY_CLOUDS
     && weather != WEATHER_RAIN && weather != WEATHER_RAIN_THUNDERSTORM)
        return weather;
    season = LegendsGetActiveSeason();
    day = VarGet(VAR_LEGENDS_SEASON_WEATHER_DAY);
    // Stable until a faded warp, without consuming battle RNG.
    roll = (day * 37 + gMapHeader.regionMapSectionId * 17) % 10;
    if (gMapHeader.mapType == MAP_TYPE_OCEAN_ROUTE)
        return roll < (season == LEGENDS_SUMMER ? 1 : 3) ? WEATHER_RAIN : WEATHER_SUNNY_CLOUDS;
    // Southern islands remain mild; the mainland gets intermittent winter snow.
    if (season == LEGENDS_WINTER && gMapHeader.regionMapSectionId != MAPSEC_DEWFORD_TOWN
     && gMapHeader.regionMapSectionId != MAPSEC_PACIFIDLOG_TOWN
     && gMapHeader.regionMapSectionId != MAPSEC_SOOTOPOLIS_CITY)
        return roll < 6 ? WEATHER_SNOW : WEATHER_SUNNY_CLOUDS;
    if (season == LEGENDS_AUTUMN && roll < 2)
        return WEATHER_FOG_HORIZONTAL;
    if (season == LEGENDS_SPRING && roll < 4)
        return WEATHER_RAIN;
    if (season == LEGENDS_SUMMER && roll == 0)
        return WEATHER_RAIN_THUNDERSTORM;
    // Rainforest routes keep their characteristic rainfall outside winter.
    return weather;
}

void LegendsRestoreSeasonWeather(void)
{
    u16 original = VarGet(VAR_LEGENDS_BASE_WEATHER);
    u8 weather = original >= 0x100 && original < 0x100 + WEATHER_COUNT
               ? original - 0x100 : gMapHeader.weather;
    // Older saves have no original-weather var; retain active story effects.
    if (original == 0 && (GetSavedWeather() == WEATHER_ABNORMAL
                      || GetSavedWeather() == WEATHER_DROUGHT
                      || GetSavedWeather() == WEATHER_DOWNPOUR))
        weather = GetSavedWeather();
    SetSavedWeather(weather);
}

