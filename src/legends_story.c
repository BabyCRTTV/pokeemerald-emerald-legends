#include "global.h"
#include "legends_story.h"
#include "event_data.h"
#include "constants/maps.h"
#include "constants/weather.h"

bool32 LegendsIsSeafoamMap(void)
{
#if !IS_FRLG
    const struct WarpData *location = &gSaveBlock1Ptr->location;
    return location->mapGroup == MAP_GROUP(MAP_LEGENDS_KANTO_SEAFOAM_ISLANDS_1F)
        && location->mapNum >= MAP_NUM(MAP_LEGENDS_KANTO_SEAFOAM_ISLANDS_1F)
        && location->mapNum <= MAP_NUM(MAP_LEGENDS_KANTO_SEAFOAM_ISLANDS_B4F);
#else
    return FALSE;
#endif
}

u8 LegendsStoryWeather(u8 weather)
{
#if !IS_FRLG
    const struct WarpData *location = &gSaveBlock1Ptr->location;
    // Only the two outdoor survey routes. Native special story weather, desert
    // sand, indoor maps and the original Groudon/Kyogre sequence stay native.
    if (!FlagGet(FLAG_LEGENDS_STORY_WEATHER_STARTED)
     || FlagGet(FLAG_LEGENDS_STORY_REGIGIGAS_CALMED)
     || !FlagGet(FLAG_SYS_GAME_CLEAR)
     || (weather != WEATHER_SUNNY && weather != WEATHER_SUNNY_CLOUDS
      && weather != WEATHER_RAIN && weather != WEATHER_RAIN_THUNDERSTORM))
        return WEATHER_COUNT;
    if (location->mapGroup == MAP_GROUP(MAP_ROUTE119)
     && location->mapNum == MAP_NUM(MAP_ROUTE119))
        return WEATHER_RAIN_THUNDERSTORM;
    if (location->mapGroup == MAP_GROUP(MAP_ROUTE120)
     && location->mapNum == MAP_NUM(MAP_ROUTE120))
        return WEATHER_FOG_HORIZONTAL;
#endif
    return WEATHER_COUNT;
}
