// Linked only into a private mGBA test copy, never a published game ROM.
#include "global.h"
#include "main.h"
#include "legends_journal.h"
#include "event_data.h"

void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    u16 q, step;
    for (q = 0; q < LegendsQuestCount(); q++)
    {
        const struct LegendsQuest *quest = LegendsQuestGet(q);
        for (step = 0; step < quest->count; step++)
            FlagSet(quest->steps[step].flag);
    }
    LegendsJournalInit(TRUE);
    if (box[0])
    {
        box[1] = LegendsAchievementClaim(0);
        SetMainCallback2(CB2_OpenAchievements);
    }
    else
        SetMainCallback2(CB2_OpenQuestLog);
}
