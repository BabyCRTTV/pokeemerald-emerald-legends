#include "global.h"
#include "legends_adventure.h"
#include "event_data.h"
#include "rtc.h"
#include "overworld.h"
#include "string_util.h"
#include "constants/species.h"
#include "constants/region_map_sections.h"

#define ADVENTURE_MAGIC 0x4C414456
#define JOURNAL (&gSaveBlock3Ptr->adventure)

EWRAM_DATA static bool8 sReady = FALSE;
EWRAM_DATA static u16 sTickFrames = 0;

static const struct { u16 flag, event; } sMilestones[] =
{
    {FLAG_SYS_POKEDEX_GET, ADV_POKEDEX},
    {FLAG_DELIVERED_STEVEN_LETTER, ADV_STEVEN_LETTER},
    {FLAG_DEFEATED_MAGMA_SPACE_CENTER, ADV_SPACE_CENTER},
    {FLAG_BADGE01_GET, ADV_BADGE1}, {FLAG_BADGE02_GET, ADV_BADGE2},
    {FLAG_BADGE03_GET, ADV_BADGE3}, {FLAG_BADGE04_GET, ADV_BADGE4},
    {FLAG_BADGE05_GET, ADV_BADGE5}, {FLAG_BADGE06_GET, ADV_BADGE6},
    {FLAG_BADGE07_GET, ADV_BADGE7}, {FLAG_BADGE08_GET, ADV_BADGE8},
    {FLAG_SYS_GAME_CLEAR, ADV_CHAMPION},
    {FLAG_LEGENDS_KANTO_WELCOMED, ADV_KANTO_ARRIVAL},
    {FLAG_LEGENDS_KANTO_SURVEY_STARTED, ADV_SURVEY_START},
    {FLAG_LEGENDS_KANTO_SURGE_WON, ADV_SURGE}, {FLAG_LEGENDS_KANTO_KOGA_WON, ADV_KOGA},
    {FLAG_LEGENDS_KANTO_BROCK_WON, ADV_BROCK}, {FLAG_LEGENDS_KANTO_MISTY_WON, ADV_MISTY},
    {FLAG_LEGENDS_KANTO_ERIKA_WON, ADV_ERIKA}, {FLAG_LEGENDS_KANTO_SABRINA_WON, ADV_SABRINA},
    {FLAG_LEGENDS_KANTO_BLAINE_WON, ADV_BLAINE}, {FLAG_LEGENDS_KANTO_VIRIDIAN_WON, ADV_VIRIDIAN},
    {FLAG_LEGENDS_KANTO_SURVEY_REPORT, ADV_SURVEY_REPORT},
};

static u32 Checksum(void)
{
    const u8 *bytes = (const u8 *)JOURNAL;
    u32 i, hash = 2166136261u;
    // magic/checksum are validated separately; padding is zero-initialized.
    for (i = 8; i < sizeof(*JOURNAL); i++)
        hash = (hash ^ bytes[i]) * 16777619u;
    return hash;
}

static bool32 Ready(void)
{
    return sReady && JOURNAL->magic == ADVENTURE_MAGIC;
}

static bool32 GetDate(struct SiiRtcInfo *rtc)
{
    u32 month, day, year;
    if (RtcGetErrorStatus() & (RTC_ERR_FLAG_MASK | RTC_INIT_ERROR))
        return FALSE;
    RtcGetInfo(rtc);
    month = ConvertBcdToBinary(rtc->month);
    day = ConvertBcdToBinary(rtc->day);
    year = ConvertBcdToBinary(rtc->year);
    return year <= 99 && month >= 1 && month <= 12 && day >= 1
        && day <= (u32)sNumDaysInMonths[month - 1] + (month == 2 && IsLeapYear(year));
}

static void Append(u16 event)
{
    struct SiiRtcInfo rtc;
    struct LegendsAdventureEntry *entry;
    // A day's field note refreshes between milestones instead of flooding the book.
    entry = &JOURNAL->entries[(JOURNAL->head + LEGENDS_ADVENTURE_CAPACITY - 1) % LEGENDS_ADVENTURE_CAPACITY];
    if (!JOURNAL->count || entry->day != JOURNAL->daysPlayed
     || event > ADV_CATCH || entry->event > ADV_CATCH || entry->event == ADV_BEGIN)
    {
        entry = &JOURNAL->entries[JOURNAL->head];
        JOURNAL->head = (JOURNAL->head + 1) % LEGENDS_ADVENTURE_CAPACITY;
        if (JOURNAL->count < LEGENDS_ADVENTURE_CAPACITY)
            JOURNAL->count++;
    }
    memset(entry, 0, sizeof(*entry));
    entry->day = JOURNAL->daysPlayed;
    if (GetDate(&rtc))
        entry->date = (ConvertBcdToBinary(rtc.year) << 9) | (ConvertBcdToBinary(rtc.month) << 5) | ConvertBcdToBinary(rtc.day);
    entry->region = event == ADV_BEGIN ? MAPSEC_LITTLEROOT_TOWN : gMapHeader.regionMapSectionId;
    entry->species = JOURNAL->recentSpecies;
    entry->level = JOURNAL->recentLevel;
    entry->event = event;
    entry->context = JOURNAL->lastStory;
    entry->hours = gSaveBlock2Ptr->playTimeHours;
    entry->minute = gSaveBlock2Ptr->playTimeMinutes;
    JOURNAL->checksum = Checksum();
}

void LegendsAdventureUpdateDay(void)
{
    struct SiiRtcInfo rtc;
    u16 date;
    if (!Ready() || !GetDate(&rtc))
        return; // Never invent calendar dates when the RTC is unavailable.
    date = RtcGetDayCount(&rtc);
    if (!JOURNAL->lastRtcDay)
    {
        JOURNAL->lastRtcDay = date;
        JOURNAL->checksum = Checksum();
    }
    else if (date > JOURNAL->lastRtcDay)
    {
        // One active date, even after a week away. Rollbacks do not add days.
        JOURNAL->lastRtcDay = date;
        if (JOURNAL->daysPlayed < 65535)
            JOURNAL->daysPlayed++;
        JOURNAL->recentSpecies = SPECIES_NONE;
        JOURNAL->recentLevel = 0;
        Append(ADV_RESUME);
    }
}

void LegendsAdventureInit(bool32 newGame)
{
    u32 i;
    struct SiiRtcInfo rtc;
    sReady = FALSE;
    sTickFrames = 0;
    if (newGame || JOURNAL->magic != ADVENTURE_MAGIC || JOURNAL->version != LEGENDS_ADVENTURE_VERSION
     || JOURNAL->head >= LEGENDS_ADVENTURE_CAPACITY || JOURNAL->count > LEGENDS_ADVENTURE_CAPACITY
     || !JOURNAL->daysPlayed || JOURNAL->recentSpecies >= NUM_SPECIES || JOURNAL->lastStory >= ADV_EVENT_COUNT
     || JOURNAL->checksum != Checksum())
    {
        // Old saves have arbitrary reserved bytes. Reset only this extension.
        memset(JOURNAL, 0, sizeof(*JOURNAL));
        JOURNAL->magic = ADVENTURE_MAGIC;
        JOURNAL->version = LEGENDS_ADVENTURE_VERSION;
        JOURNAL->daysPlayed = 1;
        if (GetDate(&rtc))
            JOURNAL->lastRtcDay = RtcGetDayCount(&rtc);
        if (!newGame)
            for (i = 0; i < ARRAY_COUNT(sMilestones); i++)
                if (FlagGet(sMilestones[i].flag))
                    JOURNAL->lastStory = sMilestones[i].event;
        sReady = TRUE;
        Append(newGame ? ADV_BEGIN : ADV_RESUME);
    }
    else
    {
        sReady = TRUE;
        LegendsAdventureUpdateDay();
    }
}

void LegendsAdventureTick(void)
{
    if (!Ready() || ++sTickFrames < 3600)
        return;
    sTickFrames = 0;
    if (!IsOverworldLinkActive())
        LegendsAdventureUpdateDay();
}

u16 LegendsAdventureDays(void)
{
    return Ready() ? JOURNAL->daysPlayed : 1;
}

void LegendsAdventureRecord(u16 event)
{
    if (!Ready() || event >= ADV_EVENT_COUNT || IsOverworldLinkActive())
        return;
    LegendsAdventureUpdateDay();
    if (event >= ADV_POKEDEX)
        JOURNAL->lastStory = event;
    Append(event);
}

void LegendsAdventureFlagSet(u16 flag)
{
    u32 i;
    if (!Ready())
        return;
    for (i = 0; i < ARRAY_COUNT(sMilestones); i++)
        if (sMilestones[i].flag == flag)
        {
            LegendsAdventureRecord(sMilestones[i].event);
            return;
        }
}

void LegendsAdventureFlagClear(u16 flag)
{
    // Emerald ends the Sootopolis cutscene by clearing this active-crisis flag.
    if (flag == FLAG_SYS_WEATHER_CTRL)
        LegendsAdventureRecord(ADV_WEATHER_PEACE);
}

void LegendsAdventureCatch(u16 species, u8 level)
{
    if (!Ready() || species == SPECIES_NONE || species >= NUM_SPECIES || IsOverworldLinkActive())
        return;
    LegendsAdventureUpdateDay();
    JOURNAL->recentSpecies = species;
    JOURNAL->recentLevel = level;
    Append(ADV_CATCH);
}

const struct LegendsAdventureEntry *LegendsAdventureGet(u8 newestIndex)
{
    if (!Ready() || newestIndex >= JOURNAL->count)
        return NULL;
    return &JOURNAL->entries[(JOURNAL->head + LEGENDS_ADVENTURE_CAPACITY - 1 - newestIndex) % LEGENDS_ADVENTURE_CAPACITY];
}

static bool32 Matches(const struct LegendsAdventureEntry *entry, u8 filter, u16 day)
{
    return (filter != ADV_FILTER_DAY || entry->day == day)
        && (filter != ADV_FILTER_STORY || entry->event >= ADV_POKEDEX);
}

u8 LegendsAdventureCount(u8 filter, u16 day)
{
    u8 i, count = 0;
    const struct LegendsAdventureEntry *entry;
    for (i = 0; (entry = LegendsAdventureGet(i)) != NULL; i++)
        if (Matches(entry, filter, day))
            count++;
    return count;
}

const struct LegendsAdventureEntry *LegendsAdventureFiltered(u8 filter, u16 day, u8 index)
{
    u8 i;
    const struct LegendsAdventureEntry *entry;
    for (i = 0; (entry = LegendsAdventureGet(i)) != NULL; i++)
        if (Matches(entry, filter, day) && index-- == 0)
            return entry;
    return NULL;
}

u16 LegendsAdventureAdjacentDay(u16 day, bool32 older)
{
    u8 i;
    u16 best = day;
    const struct LegendsAdventureEntry *entry;
    for (i = 0; (entry = LegendsAdventureGet(i)) != NULL; i++)
        if ((older && entry->day < day && (best == day || entry->day > best))
         || (!older && entry->day > day && (best == day || entry->day < best)))
            best = entry->day;
    return best;
}
