#ifndef GUARD_LEGENDS_SEASONS_H
#define GUARD_LEGENDS_SEASONS_H

enum LegendsSeason
{
    LEGENDS_SPRING,
    LEGENDS_SUMMER,
    LEGENDS_AUTUMN,
    LEGENDS_WINTER,
    LEGENDS_SEASON_COUNT,
};

enum LegendsSeasonMode
{
    LEGENDS_SEASONS_RTC,
    LEGENDS_SEASONS_PLAYTIME,
    LEGENDS_SEASON_MODE_COUNT,
};

#define LEGENDS_SEASON_SECONDS (28 * 60 * 60)
#define LEGENDS_SEASON_CYCLE_SECONDS (LEGENDS_SEASON_SECONDS * LEGENDS_SEASON_COUNT)

u8 LegendsGetSeasonMode(void);
void LegendsSetSeasonMode(u8 mode);
u8 LegendsGetSeason(void);
u8 LegendsGetSeasonForMode(u8 mode);
const u8 *LegendsGetSeasonName(u8 season);
void LegendsSeasonTick(void);
bool32 LegendsMapHasSeasons(void);
void LegendsApplySeasonPalette(u16 offset, u16 count);
u8 LegendsSeasonWeather(u8 weather);
void LegendsRefreshSeasons(void);
void LegendsRestoreSeasonWeather(void);

#endif
