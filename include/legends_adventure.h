#ifndef GUARD_LEGENDS_ADVENTURE_H
#define GUARD_LEGENDS_ADVENTURE_H

#define LEGENDS_ADVENTURE_CAPACITY 32
#define LEGENDS_ADVENTURE_VERSION 1

enum LegendsAdventureEvent
{
    ADV_BEGIN, ADV_RESUME, ADV_CHECKPOINT, ADV_CATCH,
    ADV_POKEDEX, ADV_STEVEN_LETTER, ADV_SPACE_CENTER, ADV_WEATHER_PEACE,
    ADV_BADGE1, ADV_BADGE2, ADV_BADGE3, ADV_BADGE4,
    ADV_BADGE5, ADV_BADGE6, ADV_BADGE7, ADV_BADGE8, ADV_CHAMPION,
    ADV_KANTO_ARRIVAL, ADV_SURVEY_START, ADV_SURGE, ADV_KOGA,
    ADV_BROCK, ADV_MISTY, ADV_ERIKA, ADV_SABRINA, ADV_BLAINE,
    ADV_VIRIDIAN, ADV_SURVEY_REPORT, ADV_EVENT_COUNT,
};

enum LegendsAdventureFilter { ADV_FILTER_ALL, ADV_FILTER_DAY, ADV_FILTER_STORY, ADV_FILTER_COUNT };

// Appended only to SaveBlock3's reserved sector chunks. Existing fields do not move.
struct LegendsAdventureEntry
{
    u16 day, date, region, species, event, context, hours;
    u8 minute, level;
};

struct LegendsAdventureSave
{
    u32 magic, checksum;
    u16 version, daysPlayed, lastRtcDay, lastStory, recentSpecies;
    u8 recentLevel, head, count, reserved;
    struct LegendsAdventureEntry entries[LEGENDS_ADVENTURE_CAPACITY];
};

void LegendsAdventureInit(bool32 newGame);
void LegendsAdventureTick(void);
void LegendsAdventureUpdateDay(void);
void LegendsAdventureRecord(u16 event);
void LegendsAdventureFlagSet(u16 flag);
void LegendsAdventureFlagClear(u16 flag);
void LegendsAdventureCatch(u16 species, u8 level);
u16 LegendsAdventureDays(void);
const struct LegendsAdventureEntry *LegendsAdventureGet(u8 newestIndex);
u8 LegendsAdventureCount(u8 filter, u16 day);
const struct LegendsAdventureEntry *LegendsAdventureFiltered(u8 filter, u16 day, u8 index);
u16 LegendsAdventureAdjacentDay(u16 day, bool32 older);
void CB2_OpenAdventureLog(void);

#endif
