#include "global.h"
#include "legends_weather.h"
#include "legends_seasons.h"
#include "event_data.h"
#include "field_weather.h"
#include "palette.h"
#include "random.h"
#include "rtc.h"
#include "script.h"
#include "util.h"
#include "constants/flags.h"
#include "constants/map_types.h"
#include "constants/region_map_sections.h"
#include "constants/rtc.h"
#include "constants/vars.h"
#include "constants/weather.h"

// Climate is separate from the foliage exclusions. Use explicit Hoenn areas;
// caves, event islands, Frontier facilities and unconfigured regions stay native.
enum Climate { CLIMATE_PROTECTED, CLIMATE_LOWLAND, CLIMATE_COAST, CLIMATE_WET, CLIMATE_UPLAND, CLIMATE_WOODS };

static u8 GetClimate(void)
{
    u16 section = gMapHeader.regionMapSectionId;
    if (gMapHeader.mapType != MAP_TYPE_TOWN && gMapHeader.mapType != MAP_TYPE_CITY
     && gMapHeader.mapType != MAP_TYPE_ROUTE && gMapHeader.mapType != MAP_TYPE_OCEAN_ROUTE)
        return CLIMATE_PROTECTED;
    switch (section)
    {
    case MAPSEC_MT_CHIMNEY: case MAPSEC_JAGGED_PASS: case MAPSEC_FIERY_PATH:
    case MAPSEC_LAVARIDGE_TOWN: case MAPSEC_FALLARBOR_TOWN:
    case MAPSEC_ROUTE_111: case MAPSEC_ROUTE_112: case MAPSEC_ROUTE_113:
        return CLIMATE_PROTECTED;
    case MAPSEC_ROUTE_114: case MAPSEC_ROUTE_115: case MAPSEC_ROUTE_116:
        return CLIMATE_UPLAND;
    case MAPSEC_FORTREE_CITY: case MAPSEC_ROUTE_119: case MAPSEC_ROUTE_120: case MAPSEC_ROUTE_121:
        return CLIMATE_WET;
    case MAPSEC_PETALBURG_WOODS:
        return CLIMATE_WOODS;
    case MAPSEC_DEWFORD_TOWN: case MAPSEC_PACIFIDLOG_TOWN: case MAPSEC_SOOTOPOLIS_CITY:
    case MAPSEC_SLATEPORT_CITY: case MAPSEC_LILYCOVE_CITY: case MAPSEC_MOSSDEEP_CITY:
    case MAPSEC_EVER_GRANDE_CITY:
        return CLIMATE_COAST;
    case MAPSEC_LITTLEROOT_TOWN: case MAPSEC_OLDALE_TOWN: case MAPSEC_PETALBURG_CITY:
    case MAPSEC_RUSTBORO_CITY: case MAPSEC_MAUVILLE_CITY: case MAPSEC_VERDANTURF_TOWN:
        return CLIMATE_LOWLAND;
    default:
        if (section >= MAPSEC_ROUTE_101 && section <= MAPSEC_ROUTE_134)
            return gMapHeader.mapType == MAP_TYPE_OCEAN_ROUTE ? CLIMATE_COAST : CLIMATE_LOWLAND;
        return CLIMATE_PROTECTED;
    }
}

static bool32 IsOrdinaryRequest(u8 weather)
{
    return weather == WEATHER_SUNNY || weather == WEATHER_SUNNY_CLOUDS
        || weather == WEATHER_RAIN || weather == WEATHER_RAIN_THUNDERSTORM;
}

static u16 GetWeatherSeconds(void)
{
    if (!FlagGet(FLAG_LEGENDS_WEATHER_CLOCK_INITIALIZED))
    {
        u32 seconds = gSaveBlock2Ptr->playTimeHours * 3600u
                    + gSaveBlock2Ptr->playTimeMinutes * 60u + gSaveBlock2Ptr->playTimeSeconds;
        VarSet(VAR_LEGENDS_WEATHER_SECONDS, seconds % LEGENDS_WEATHER_CYCLE_SECONDS);
        FlagSet(FLAG_LEGENDS_WEATHER_CLOCK_INITIALIZED);
    }
    return VarGet(VAR_LEGENDS_WEATHER_SECONDS) % LEGENDS_WEATHER_CYCLE_SECONDS;
}

// Called once per recorded second, including menus/battles, from the existing
// saved season frame clock. No RTC, weather effects or global RNG in VBlank.
void LegendsAdvanceWeatherClock(void)
{
    VarSet(VAR_LEGENDS_WEATHER_SECONDS, (GetWeatherSeconds() + 1) % LEGENDS_WEATHER_CYCLE_SECONDS);
}

u8 LegendsChooseAmbientWeather(u8 weather)
{
    u8 climate = GetClimate();
    u8 season, timeOfDay, rain, thunder, fog = 0, snow = 0;
    u32 roll;
    rng_value_t localState;
    if (climate == CLIMATE_PROTECTED || !IsOrdinaryRequest(weather))
        return weather;
    season = LegendsGetActiveSeason();
    // Reuse the expansion's local seeded forecast pattern, not battle RNG.
    const u32 pieces[] = { gSaveBlock1Ptr->dailySeed,
        GetWeatherSeconds() / LEGENDS_WEATHER_PERIOD_SECONDS,
        gMapHeader.regionMapSectionId, season };
    localState = LocalRandomSeed(Crc32B((const u8 *)pieces, sizeof(pieces)));
    roll = LocalRandom32(&localState) % 100;

    // Percent weights, with clear/cloudy as the remainder. Hoenn stays mild:
    // lowlands and tropical coasts never receive random snow.
    rain = season == LEGENDS_SPRING ? 30 : season == LEGENDS_SUMMER ? 18 : 25;
    thunder = season == LEGENDS_SUMMER ? 5 : season == LEGENDS_SPRING ? 2 : 1;
    if (climate == CLIMATE_WET)
    {
        rain += 20;
        fog = season == LEGENDS_AUTUMN ? 12 : 6;
    }
    else if (climate == CLIMATE_UPLAND)
    {
        fog = season == LEGENDS_AUTUMN ? 12 : 6;
        if (season == LEGENDS_WINTER)
        {
            snow = 25;
            rain = 15;
            thunder = 0;
        }
    }
    timeOfDay = GetTimeOfDay();
    if (timeOfDay == TIME_MORNING || timeOfDay == TIME_NIGHT)
    {
        if (climate == CLIMATE_WET || climate == CLIMATE_UPLAND)
            fog += 8;
    }
    if (roll < snow) return WEATHER_SNOW;
    roll -= snow;
    if (roll < fog) return WEATHER_FOG_HORIZONTAL;
    roll -= fog;
    if (roll < thunder) return WEATHER_RAIN_THUNDERSTORM;
    roll -= thunder;
    if (roll < rain) return WEATHER_RAIN;
    // Woods retain canopy shade (their explicit shade request stays native).
    return climate == CLIMATE_WOODS ? WEATHER_SHADE
         : roll - rain < 18 ? WEATHER_SUNNY_CLOUDS : WEATHER_SUNNY;
}

EWRAM_DATA static u8 sPollFrames = 0;

void LegendsWeatherTick(void)
{
    u16 original;
    u8 current;
    if (++sPollFrames < 60)
        return;
    sPollFrames = 0;
    // Native tasks perform the transition; never interrupt dialogue, fades,
    // special story weather or an effect that is still cleaning up.
    if (ScriptContext_IsEnabled() || gPaletteFade.active
     || gWeatherPtr->palProcessingState != WEATHER_PAL_STATE_IDLE
     || gWeatherPtr->currWeather != gWeatherPtr->nextWeather
     || GetClimate() == CLIMATE_PROTECTED)
        return;
    current = GetCurrentWeather();
    if (!IsOrdinaryRequest(current) && current != WEATHER_SNOW && current != WEATHER_FOG_HORIZONTAL)
        return;
    original = VarGet(VAR_LEGENDS_BASE_WEATHER);
    if (original < 0x100 || original >= 0x100 + WEATHER_COUNT)
        return; // Native map/continue initialization establishes the baseline.
    original -= 0x100;
    if (!IsOrdinaryRequest(original) && original != WEATHER_ROUTE119_CYCLE && original != WEATHER_ROUTE123_CYCLE)
        return;
    // Preserves the raw map/script request and native rain statistics. Only
    // request a transition when the forecast actually changes.
    SetSavedWeather(original);
    if (GetSavedWeather() != current)
        SetNextWeather(GetSavedWeather());
}
