#ifndef GUARD_LEGENDS_JOURNAL_H
#define GUARD_LEGENDS_JOURNAL_H
#define LEGENDS_ACHIEVEMENT_LEGACY_LIMIT 96
#define LEGENDS_ACHIEVEMENT_BYTES (LEGENDS_ACHIEVEMENT_LEGACY_LIMIT / 8)
#define LEGENDS_ACHIEVEMENT_LIMIT 160
#define LEGENDS_ACHIEVEMENT_EXTRA_BYTES ((LEGENDS_ACHIEVEMENT_LIMIT - LEGENDS_ACHIEVEMENT_LEGACY_LIMIT) / 8)
struct LegendsJournalSave
{
    u32 magic, checksum;
    u16 version, reserved; // Signed tracked-quest selection; version-1 layout unchanged.
    u8 earned[LEGENDS_ACHIEVEMENT_BYTES], claimed[LEGENDS_ACHIEVEMENT_BYTES];
};
// Separate append-only tail: never enlarge or move the published v1 journal.
struct LegendsAchievementExtraSave
{
    u32 magic, checksum;
    u16 version, reserved;
    u8 earned[LEGENDS_ACHIEVEMENT_EXTRA_BYTES], claimed[LEGENDS_ACHIEVEMENT_EXTRA_BYTES];
};
struct LegendsQuestStep { const u8 *text; u16 flag; };
struct LegendsQuest { const u8 *title; u16 start; u8 side, count; struct LegendsQuestStep steps[4]; };
enum LegendsJournalCondition { JOURNAL_FLAG, JOURNAL_STAT, JOURNAL_DEX, JOURNAL_RESEARCH };
struct LegendsAchievement { const u8 *title, *description; u8 kind; u16 key; u32 target; u16 berry; u8 quantity; };
void LegendsJournalInit(bool32 newGame);
void LegendsJournalRefresh(void);
void LegendsJournalFlagSet(u16 flag);
u16 LegendsAchievementNotice(void);
void LegendsAchievementNoticeDismiss(u16 id);
void LegendsAchievementPopupUpdate(void);
void LegendsAchievementPopupHide(void);
void LegendsJournalStatSet(u8 stat, u32 value);
u16 LegendsQuestCount(void);
const struct LegendsQuest *LegendsQuestGet(u16 id);
bool32 LegendsQuestVisible(u16 id);
bool32 LegendsQuestComplete(u16 id);
bool32 LegendsQuestStepComplete(u16 id, u8 step);
u16 LegendsQuestTracked(void); // 0xFFFF means no active reminder.
u8 LegendsQuestNextStep(u16 id);
bool32 LegendsQuestTrack(u16 id); // 0xFFFF explicitly stops tracking.
u16 LegendsAchievementCount(void);
const struct LegendsAchievement *LegendsAchievementGet(u16 id);
bool32 LegendsAchievementEarned(u16 id);
bool32 LegendsAchievementClaimed(u16 id);
u32 LegendsAchievementProgress(u16 id);
bool32 LegendsAchievementClaim(u16 id);
void CB2_OpenQuestLog(void);
void CB2_OpenAchievements(void);
#endif
