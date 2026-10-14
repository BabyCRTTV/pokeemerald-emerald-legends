#include "global.h"
#include "legends_journal.h"
#include "event_data.h"
#include "overworld.h"
#include "pokedex.h"
#include "item.h"
#include "string_util.h"
#include "constants/game_stat.h"
#include "constants/items.h"
#include "data/legends/journal.h"
#define JOURNAL_MAGIC 0x4C514143
#define DATA (&gSaveBlock3Ptr->journal)
// Transient notices never change the serialized journal or claim bits.
EWRAM_DATA static u8 sPending[LEGENDS_ACHIEVEMENT_BYTES] = {0};
EWRAM_DATA static bool8 sNoticesEnabled = FALSE;
static void Earn(u16 id)
{
    DATA->earned[id / 8] |= 1 << (id % 8);
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
void LegendsJournalInit(bool32 newGame)
{
    sNoticesEnabled = FALSE;
    memset(sPending, 0, sizeof(sPending));
    if (newGame || DATA->magic != JOURNAL_MAGIC || DATA->version != 1 || DATA->checksum != Checksum())
    {
        memset(DATA, 0, sizeof(*DATA));
        DATA->magic = JOURNAL_MAGIC;
        DATA->version = 1;
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
    if (!q->side) return FlagGet(q->steps[q->count - 1].flag);
    for (i = 0; i < q->count; i++) if (!FlagGet(q->steps[i].flag)) return FALSE;
    return TRUE;
}
bool32 LegendsQuestVisible(u16 id)
{
    u8 i;
    const struct LegendsQuest *q = LegendsQuestGet(id);
    if (!q) return FALSE;
    if (!q->start || FlagGet(q->start)) return TRUE;
    for (i = 0; i < q->count; i++) if (FlagGet(q->steps[i].flag)) return TRUE;
    return FALSE;
}
bool32 LegendsQuestStepComplete(u16 id, u8 step)
{
    const struct LegendsQuest *q = LegendsQuestGet(id);
    return q && step < q->count && (LegendsQuestComplete(id) || FlagGet(q->steps[step].flag));
}
u16 LegendsAchievementCount(void) { return ARRAY_COUNT(sAchievements); }
const struct LegendsAchievement *LegendsAchievementGet(u16 id) { return id < ARRAY_COUNT(sAchievements) ? &sAchievements[id] : NULL; }
u32 LegendsAchievementProgress(u16 id)
{
    const struct LegendsAchievement *a = LegendsAchievementGet(id);
    if (!a) return 0;
    switch (a->kind)
    {
    case JOURNAL_FLAG: return FlagGet(a->key);
    case JOURNAL_STAT: return GetGameStat(a->key);
    case JOURNAL_DEX: return GetNationalPokedexCount(FLAG_GET_CAUGHT);
    }
    return 0;
}
bool32 LegendsAchievementEarned(u16 id)
{
    return id < ARRAY_COUNT(sAchievements) && DATA->magic == JOURNAL_MAGIC && (DATA->earned[id / 8] & (1 << (id % 8)));
}
bool32 LegendsAchievementClaimed(u16 id)
{
    return id < ARRAY_COUNT(sAchievements) && DATA->magic == JOURNAL_MAGIC && (DATA->claimed[id / 8] & (1 << (id % 8)));
}
void LegendsJournalRefresh(void)
{
    u16 i;
    if (DATA->magic != JOURNAL_MAGIC || IsOverworldLinkActive()) return;
    for (i = 0; i < ARRAY_COUNT(sAchievements); i++)
        if (!LegendsAchievementEarned(i) && LegendsAchievementProgress(i) >= sAchievements[i].target)
            Earn(i);
    DATA->checksum = Checksum();
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
    if (changed) DATA->checksum = Checksum();
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
    if (changed) DATA->checksum = Checksum();
}
bool32 LegendsAchievementClaim(u16 id)
{
    const struct LegendsAchievement *a = LegendsAchievementGet(id);
    LegendsJournalRefresh();
    if (!a || IsOverworldLinkActive() || !LegendsAchievementEarned(id) || LegendsAchievementClaimed(id)) return FALSE;
    // Native AddPCItem is atomic: full storage retains the claim for a retry.
    if (!AddPCItem(a->berry, a->quantity)) return FALSE;
    DATA->claimed[id / 8] |= 1 << (id % 8);
    DATA->checksum = Checksum();
    return TRUE;
}
