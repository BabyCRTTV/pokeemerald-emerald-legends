// Controlled fixtures for optimized Release; linked only into a private test copy.
// LTO removes the Debug harness's helper symbols. Seed the same journal view
// directly, then exercise the actual published renderer/input/claim functions.
#include "global.h"
#include "main.h"
#include "legends_journal.h"

void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    const struct LegendsQuest *quests = (const struct LegendsQuest *)QA_QUESTS_ADDRESS;
    volatile u8 *journal = (volatile u8 *)&gSaveBlock3Ptr->journal;
    u16 q, step, i;
    box[3] = 0;
    for (q = 0; q < QA_QUEST_COUNT; q++)
        for (step = 0; step < quests[q].count; step++)
        {
            u16 flag = quests[q].steps[step].flag;
            if (flag >= NUM_FLAG_BYTES * 8)
            {
                box[3] = flag;
                return;
            }
            gSaveBlock1Ptr->flags[flag / 8] |= 1 << (flag % 8);
        }
    for (i = 0; i < sizeof(gSaveBlock3Ptr->journal); i++)
        journal[i] = 0;
    gSaveBlock3Ptr->journal.magic = 0x4C514143;
    gSaveBlock3Ptr->journal.version = 1;
    // One previously claimed entry is a rendering fixture. The second claim
    // is performed with real A-button input by the host, including PC deposit.
    if (box[0])
        gSaveBlock3Ptr->journal.claimed[0] = 1;
    box[1] = box[0] != 0;
    gMain.state = 0;
    gMain.callback2 = box[0] ? CB2_OpenAchievements : CB2_OpenQuestLog;
}
