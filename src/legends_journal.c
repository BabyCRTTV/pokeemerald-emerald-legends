#include "global.h"
#include "legends_journal.h"
#include "legends_field_requests.h"
#include "event_data.h"
#include "overworld.h"
#include "pokedex.h"
#include "item.h"
#include "string_util.h"
#include "constants/game_stat.h"
#include "constants/items.h"
#include "data/legends/journal.h"
STATIC_ASSERT(ARRAY_COUNT(sQuests) < 255, TrackedQuestIdsFitSignedWord);
STATIC_ASSERT(ARRAY_COUNT(sQuests) >= LEGENDS_FIELD_REQUEST_QUEST_BASE + LEGENDS_FIELD_REQUEST_COUNT, BirchRequestQuestIdsPresent);
#define JOURNAL_MAGIC 0x4C514143
#define TRACKED_QUEST_MAGIC 0xA700
#define DATA (&gSaveBlock3Ptr->journal)
#define EXTRA (&gSaveBlock3Ptr->achievementExtra)
#define EXTRA_MAGIC 0x41434832
// Transient notices never change the serialized journal or claim bits.
EWRAM_DATA static u8 sPending[LEGENDS_ACHIEVEMENT_LIMIT / 8] = {0};
EWRAM_DATA static bool8 sNoticesEnabled = FALSE;
static u8 *AchievementBits(u16 id, bool32 claimed)
{
    if (id < LEGENDS_ACHIEVEMENT_LEGACY_LIMIT)
        return claimed ? DATA->claimed : DATA->earned;
    return claimed ? EXTRA->claimed : EXTRA->earned;
}
static u16 AchievementBitId(u16 id)
{
    return id < LEGENDS_ACHIEVEMENT_LEGACY_LIMIT ? id : id - LEGENDS_ACHIEVEMENT_LEGACY_LIMIT;
}
static void Earn(u16 id)
{
    u16 bit = AchievementBitId(id);
    AchievementBits(id, FALSE)[bit / 8] |= 1 << (bit % 8);
    if (sNoticesEnabled) sPending[id / 8] |= 1 << (id % 8);
}
u16 LegendsAchievementNotice(void)
{
    u16 i;
    for (i = 0; i < ARRAY_COUNT(sAchievements); i++)
        if (sPending[i / 8] & (1 << (i % 8))) return i;
    return 0xFFFF;
}
void LegendsAchievementNoticeDismiss(u16 id)
{
    if (id < ARRAY_COUNT(sAchievements)) sPending[id / 8] &= ~(1 << (id % 8));
}
static u32 Checksum(void)
{
    const u8 *p = (const u8 *)DATA;
    u32 i, hash = 2166136261u;
    for (i = 8; i < sizeof(*DATA); i++) hash = (hash ^ p[i]) * 16777619u;
    return hash;
}
static u32 ExtraChecksum(void)
{
    const u8 *p = (const u8 *)EXTRA;
    u32 i, hash = 2166136261u;
    for (i = 8; i < sizeof(*EXTRA); i++) hash = (hash ^ p[i]) * 16777619u;
    return hash;
}
static void UpdateChecksums(void)
{
    DATA->checksum = Checksum();
    EXTRA->checksum = ExtraChecksum();
}
void LegendsJournalInit(bool32 newGame)
{
    bool32 reset = newGame || DATA->magic != JOURNAL_MAGIC || DATA->version != 1 || DATA->checksum != Checksum();
    sNoticesEnabled = FALSE;
    memset(sPending, 0, sizeof(sPending));
    if (reset)
    {
        memset(DATA, 0, sizeof(*DATA));
        DATA->magic = JOURNAL_MAGIC;
        DATA->version = 1;
    }
    if (reset || EXTRA->magic != EXTRA_MAGIC || EXTRA->version != 1 || EXTRA->checksum != ExtraChecksum())
    {
        memset(EXTRA, 0, sizeof(*EXTRA));
        EXTRA->magic = EXTRA_MAGIC;
        EXTRA->version = 1;
        // Bit 95 was unpublished through v0.0.59. Never inherit garbage as a reward claim.
        DATA->earned[11] &= 0x7F;
        DATA->claimed[11] &= 0x7F;
    }
    LegendsJournalRefresh();
    sNoticesEnabled = TRUE;
}
u16 LegendsQuestCount(void) { return ARRAY_COUNT(sQuests); }
const struct LegendsQuest *LegendsQuestGet(u16 id) { return id < ARRAY_COUNT(sQuests) ? &sQuests[id] : NULL; }
bool32 LegendsQuestComplete(u16 id)
{
    u8 i;
    const struct LegendsQuest *q = LegendsQuestGet(id);
    if (!q) return FALSE;
    if (id >= LEGENDS_FIELD_REQUEST_QUEST_BASE && id < LEGENDS_FIELD_REQUEST_QUEST_BASE + LEGENDS_FIELD_REQUEST_COUNT)
        return LegendsFieldRequestComplete(id - LEGENDS_FIELD_REQUEST_QUEST_BASE);
    if (!q->side) return FlagGet(q->steps[q->count - 1].flag);
    for (i = 0; i < q->count; i++) if (!FlagGet(q->steps[i].flag)) return FALSE;
    return TRUE;
}
bool32 LegendsQuestVisible(u16 id)
{
    u8 i;
    const struct LegendsQuest *q = LegendsQuestGet(id);
    if (!q) return FALSE;
    if (id >= LEGENDS_FIELD_REQUEST_QUEST_BASE && id < LEGENDS_FIELD_REQUEST_QUEST_BASE + LEGENDS_FIELD_REQUEST_COUNT)
        return LegendsFieldRequestActive() == id - LEGENDS_FIELD_REQUEST_QUEST_BASE
            || LegendsFieldRequestComplete(id - LEGENDS_FIELD_REQUEST_QUEST_BASE);
    if (!q->start || FlagGet(q->start)) return TRUE;
    for (i = 0; i < q->count; i++) if (FlagGet(q->steps[i].flag)) return TRUE;
    return FALSE;
}
bool32 LegendsQuestStepComplete(u16 id, u8 step)
{
    const struct LegendsQuest *q = LegendsQuestGet(id);
    if (q && id >= LEGENDS_FIELD_REQUEST_QUEST_BASE && id < LEGENDS_FIELD_REQUEST_QUEST_BASE + LEGENDS_FIELD_REQUEST_COUNT)
        return step < q->count && LegendsFieldRequestStepComplete(id - LEGENDS_FIELD_REQUEST_QUEST_BASE, step);
    return q && step < q->count && (LegendsQuestComplete(id) || FlagGet(q->steps[step].flag));
}
u8 LegendsQuestNextStep(u16 id)
{
    u8 step;
    const struct LegendsQuest *q = LegendsQuestGet(id);
    if (q && LegendsQuestVisible(id) && !LegendsQuestComplete(id))
        for (step = 0; step < q->count; step++)
            if (!LegendsQuestStepComplete(id, step)) return step;
    return 0xFF;
}

const u8 *LegendsQuestHint(u16 id)
{
    static const struct LegendsQuestStep hints[] =
    {
        {COMPOUND_STRING("Visit BIRCH at his lab on the west side of LITTLEROOT TOWN."), FLAG_SYS_POKEDEX_GET},
        {COMPOUND_STRING("Enter RUSTBORO GYM and speak to ROXANNE at the back."), FLAG_BADGE01_GET},
        {COMPOUND_STRING("Find BRAWLY at DEWFORD GYM. The lights brighten as you defeat its trainers."), FLAG_BADGE02_GET},
        {COMPOUND_STRING("Head into MAUVILLE GYM and use the floor switches to reach WATTSON."), FLAG_BADGE03_GET},
        {COMPOUND_STRING("Find FLANNERY inside LAVARIDGE GYM. Use the hot spring openings to move between floors."), FLAG_BADGE04_GET},
        {COMPOUND_STRING("Challenge NORMAN in PETALBURG GYM after earning four badges."), FLAG_BADGE05_GET},
        {COMPOUND_STRING("Use the turnstiles inside FORTREE GYM to reach WINONA."), FLAG_BADGE06_GET},
        {COMPOUND_STRING("Bring at least two Pokémon that can fight to MOSSDEEP GYM for TATE and LIZA."), FLAG_BADGE07_GET},
        {COMPOUND_STRING("Enter SOOTOPOLIS GYM and break each ice tile on your way to JUAN."), FLAG_BADGE08_GET},
        {COMPOUND_STRING("Head into RUSTURF TUNNEL from ROUTE 116 to find the thief and PEEKO."), FLAG_RECOVERED_DEVON_GOODS},
        {COMPOUND_STRING("Bring the recovered goods to MR. STONE at DEVON CORP. in RUSTBORO."), FLAG_RETURNED_DEVON_GOODS},
        {COMPOUND_STRING("From DEWFORD, enter GRANITE CAVE on ROUTE 106 and find STEVEN inside."), FLAG_DELIVERED_STEVEN_LETTER},
        {COMPOUND_STRING("Ask for CAPTAIN STERN at the OCEANIC MUSEUM in SLATEPORT."), FLAG_DELIVERED_DEVON_GOODS},
        {COMPOUND_STRING("Take the cable car from ROUTE 112 to MT. CHIMNEY and check the machine at the summit."), FLAG_RECEIVED_METEORITE},
        {COMPOUND_STRING("Cross ROUTE 119 and enter the WEATHER INSTITUTE before reaching FORTREE."), FLAG_RECEIVED_CASTFORM},
        {COMPOUND_STRING("Find STEVEN on the bridge east of FORTREE on ROUTE 120."), FLAG_RECEIVED_DEVON_SCOPE},
        {COMPOUND_STRING("Take JAGGED PASS down from MT. CHIMNEY. Check the MAGMA HIDEOUT along the way."), FLAG_GROUDON_AWAKENED_MAGMA_HIDEOUT},
        {COMPOUND_STRING("Check the harbor in SLATEPORT, then follow TEAM AQUA to its hideout east of LILYCOVE."), FLAG_TEAM_AQUA_ESCAPED_IN_SUBMARINE},
        {COMPOUND_STRING("Talk to STEVEN upstairs in the MOSSDEEP SPACE CENTER."), FLAG_DEFEATED_MAGMA_SPACE_CENTER},
        {COMPOUND_STRING("Take VICTORY ROAD from EVER GRANDE CITY to the POKEMON LEAGUE."), FLAG_SYS_GAME_CLEAR},
        {COMPOUND_STRING("Look for the survey marker on ROUTE 16, just west of CELADON."), FLAG_LEGENDS_KANTO_SURVEY_LEAVES},
        {COMPOUND_STRING("Look for the survey marker on ROUTE 8 between SAFFRON and LAVENDER."), FLAG_LEGENDS_KANTO_SURVEY_ECHO},
        {COMPOUND_STRING("Look for the rain-reading station on ROUTE 119."), FLAG_LEGENDS_STORY_WEATHER_RAIN_READING},
        {COMPOUND_STRING("Look for the heat-reading station in the ROUTE 111 desert."), FLAG_LEGENDS_STORY_WEATHER_HEAT_READING},
        {COMPOUND_STRING("Look for the water survey marker in CERULEAN CITY."), FLAG_LEGENDS_STORY_NORTH_WATER},
        {COMPOUND_STRING("Look for the stone survey marker on ROUTE 4, west of CERULEAN."), FLAG_LEGENDS_STORY_NORTH_STONE},
        {COMPOUND_STRING("Talk to OAK in his PALLET TOWN lab once your visiting records are complete."), FLAG_LEGENDS_FINAL_VOYAGE_READY},
        {COMPOUND_STRING("Visit RYDEL's bike shop in MAUVILLE CITY."), FLAG_RECEIVED_BIKE},
        {COMPOUND_STRING("Talk to the person by the tree on ROUTE 111, north of MAUVILLE."), FLAG_RECEIVED_SECRET_POWER},
        {COMPOUND_STRING("Find CAPTAIN STERN at SLATEPORT HARBOR after recovering the SCANNER."), FLAG_EXCHANGED_SCANNER},
        {COMPOUND_STRING("Dive on ROUTE 134 and explore the SEALED CHAMBER."), FLAG_REGI_DOORS_OPENED},
    };
    u8 step = LegendsQuestNextStep(id);
    if (step == 0xFF)
        return NULL;

    const struct LegendsQuestStep *next = &LegendsQuestGet(id)->steps[step];
    for (u32 i = 0; i < ARRAY_COUNT(hints); i++)
        if (hints[i].flag == next->flag)
            return hints[i].text;
    return next->text;
}
u16 LegendsQuestTracked(void)
{
    u16 word = DATA->reserved;
    u16 id = (word & 0xFF) - 1;
    // Old version-1 reserved bytes are not a selection. Reads never write.
    if (DATA->magic != JOURNAL_MAGIC || DATA->version != 1
        || (word & 0xFF00) != TRACKED_QUEST_MAGIC || !(word & 0xFF)
        || LegendsQuestNextStep(id) == 0xFF)
        return 0xFFFF;
    return id;
}
bool32 LegendsQuestTrack(u16 id)
{
    if (DATA->magic != JOURNAL_MAGIC || DATA->version != 1 || IsOverworldLinkActive()
        || (id != 0xFFFF && (id >= 255 || LegendsQuestNextStep(id) == 0xFF)))
        return FALSE;
    DATA->reserved = TRACKED_QUEST_MAGIC | (id == 0xFFFF ? 0 : id + 1);
    UpdateChecksums();
    return TRUE;
}
u16 LegendsAchievementCount(void) { return ARRAY_COUNT(sAchievements); }
const struct LegendsAchievement *LegendsAchievementGet(u16 id) { return id < ARRAY_COUNT(sAchievements) ? &sAchievements[id] : NULL; }
u32 LegendsAchievementProgress(u16 id)
{
    const struct LegendsAchievement *a = LegendsAchievementGet(id);
    u16 request;
    u32 count = 0;
    if (!a) return 0;
    switch (a->kind)
    {
    case JOURNAL_FLAG: return FlagGet(a->key);
    case JOURNAL_STAT: return GetGameStat(a->key);
    case JOURNAL_DEX: return GetNationalPokedexCount(FLAG_GET_CAUGHT);
    case JOURNAL_RESEARCH:
        for (request = 0; request < LEGENDS_FIELD_REQUEST_COUNT; request++)
            if ((a->key == 2 || LegendsFieldRequestOwner(request) == a->key) && LegendsFieldRequestComplete(request)) count++;
        return count;
    }
    return 0;
}
bool32 LegendsAchievementEarned(u16 id)
{
    u16 bit = AchievementBitId(id);
    return id < ARRAY_COUNT(sAchievements) && DATA->magic == JOURNAL_MAGIC
        && (id < LEGENDS_ACHIEVEMENT_LEGACY_LIMIT || EXTRA->magic == EXTRA_MAGIC)
        && (AchievementBits(id, FALSE)[bit / 8] & (1 << (bit % 8)));
}
bool32 LegendsAchievementClaimed(u16 id)
{
    u16 bit = AchievementBitId(id);
    return id < ARRAY_COUNT(sAchievements) && DATA->magic == JOURNAL_MAGIC
        && (id < LEGENDS_ACHIEVEMENT_LEGACY_LIMIT || EXTRA->magic == EXTRA_MAGIC)
        && (AchievementBits(id, TRUE)[bit / 8] & (1 << (bit % 8)));
}
void LegendsJournalRefresh(void)
{
    u16 i;
    if (DATA->magic != JOURNAL_MAGIC || IsOverworldLinkActive()) return;
    // Completion clears only a recognized selection, never arbitrary legacy bytes.
    if ((DATA->reserved & 0xFF00) == TRACKED_QUEST_MAGIC
        && (DATA->reserved & 0xFF) && LegendsQuestTracked() == 0xFFFF)
        DATA->reserved = TRACKED_QUEST_MAGIC;
    for (i = 0; i < ARRAY_COUNT(sAchievements); i++)
        if (!LegendsAchievementEarned(i) && LegendsAchievementProgress(i) >= sAchievements[i].target)
            Earn(i);
    UpdateChecksums();
}
void LegendsJournalFlagSet(u16 flag)
{
    u16 i;
    bool32 changed = FALSE;
    if (DATA->magic != JOURNAL_MAGIC || IsOverworldLinkActive()) return;
    for (i = 0; i < ARRAY_COUNT(sAchievements); i++)
        if (sAchievements[i].kind == JOURNAL_FLAG && sAchievements[i].key == flag && !LegendsAchievementEarned(i))
        {
            Earn(i);
            changed = TRUE;
        }
    if (changed) UpdateChecksums();
}
void LegendsJournalStatSet(u8 stat, u32 value)
{
    u16 i;
    bool32 changed = FALSE;
    if (DATA->magic != JOURNAL_MAGIC || IsOverworldLinkActive()) return;
    for (i = 0; i < ARRAY_COUNT(sAchievements); i++)
        if (sAchievements[i].kind == JOURNAL_STAT && sAchievements[i].key == stat
            && value >= sAchievements[i].target && !LegendsAchievementEarned(i))
        {
            Earn(i);
            changed = TRUE;
        }
    if (changed) UpdateChecksums();
}
bool32 LegendsAchievementClaim(u16 id)
{
    const struct LegendsAchievement *a = LegendsAchievementGet(id);
    LegendsJournalRefresh();
    if (!a || IsOverworldLinkActive() || !LegendsAchievementEarned(id) || LegendsAchievementClaimed(id)) return FALSE;
    // Native AddPCItem is atomic: full storage retains the claim for a retry.
    if (!AddPCItem(a->berry, a->quantity)) return FALSE;
    u16 bit = AchievementBitId(id);
    AchievementBits(id, TRUE)[bit / 8] |= 1 << (bit % 8);
    UpdateChecksums();
    return TRUE;
}
