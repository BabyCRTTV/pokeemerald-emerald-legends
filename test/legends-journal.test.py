"""Run the actual journal rules, reward claims and legacy initialization."""
from pathlib import Path
import subprocess, tempfile
R=Path(__file__).resolve().parents[1]
s=(R/'src/legends_journal.c').read_text()
s='\n'.join(l for l in s.splitlines() if not l.startswith('#include'))
preamble=r'''
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32; typedef int bool32;
#define TRUE 1
#define FALSE 0
#define ARRAY_COUNT(x) (sizeof(x)/sizeof((x)[0]))
#define STATIC_ASSERT(x,n) _Static_assert(x,#n)
#define COMPOUND_STRING(x) ((const u8 *)(x))
#define FLAG_GET_CAUGHT 1
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/game_stat.h"
#include "legends_journal.h"
#include "src/data/legends/journal.h"
static struct {struct LegendsJournalSave journal;} data,*gSaveBlock3Ptr=&data;
static u8 flags[4096];static u32 stats[64],dex,pcQuantity,pcItem,full,linked;
bool32 FlagGet(u16 flag){assert(flag<4096);return flags[flag];}
u32 GetGameStat(u8 id){assert(id<64);return stats[id];}
u32 GetNationalPokedexCount(u8 mode){return dex;}
bool32 IsOverworldLinkActive(void){return linked;}
bool32 AddPCItem(u16 item,u16 count){if(full)return FALSE;pcItem=item;pcQuantity+=count;return TRUE;}
'''
# Include the catalogue after condition structs only once.
s=s.replace('#define JOURNAL_MAGIC','#define JOURNAL_MAGIC',1)
main=r'''
int main(void)
{
    memset(&data,0xA5,sizeof(data)); flags[FLAG_BADGE01_GET]=1;
    stats[GAME_STAT_POKEMON_CAPTURES]=100; dex=200;
    LegendsJournalInit(FALSE);
    assert(LegendsAchievementCount()==80 && LegendsQuestCount()==33);
    assert(LegendsAchievementEarned(0));
    assert(!LegendsAchievementEarned(1));
    for(unsigned i=0;i<LegendsAchievementCount();i++)
    {
        const struct LegendsAchievement *a=LegendsAchievementGet(i);
        assert(a->berry>ITEM_NONE && a->berry<ITEMS_COUNT && a->quantity);
        if(LegendsAchievementEarned(i))
        {
            unsigned before=pcQuantity;
            full=1;assert(!LegendsAchievementClaim(i));assert(!LegendsAchievementClaimed(i));assert(pcQuantity==before);
            full=0;assert(LegendsAchievementClaim(i));assert(pcQuantity==before+a->quantity && pcItem==a->berry);
            assert(!LegendsAchievementClaim(i));assert(pcQuantity==before+a->quantity);
        }
    }
    LegendsJournalStatSet(GAME_STAT_BATTLE_TOWER_SINGLES_STREAK, 49);
    LegendsJournalStatSet(GAME_STAT_BATTLE_TOWER_SINGLES_STREAK, 0);
    for (unsigned i=0;i<LegendsAchievementCount();i++)
        if(LegendsAchievementGet(i)->key==GAME_STAT_BATTLE_TOWER_SINGLES_STREAK && LegendsAchievementGet(i)->kind==JOURNAL_STAT)
            assert(LegendsAchievementEarned(i));
    struct LegendsJournalSave before=data.journal;
    LegendsJournalInit(FALSE);assert(!memcmp(&before,&data.journal,sizeof(before)));
    flags[FLAG_BADGE01_GET]=0;stats[GAME_STAT_POKEMON_CAPTURES]=0;dex=0;
    LegendsJournalRefresh();assert(LegendsAchievementEarned(0));
    for(unsigned q=0;q<LegendsQuestCount();q++)
    {
        const struct LegendsQuest *quest=LegendsQuestGet(q);
        memset(flags,0,sizeof(flags));
        for(unsigned k=0;k<quest->count;k++)
        {
            assert(!LegendsQuestStepComplete(q,k));
            flags[quest->steps[k].flag]=1;
            assert(LegendsQuestStepComplete(q,k));assert(LegendsQuestVisible(q));
        }
        assert(LegendsQuestComplete(q));
    }
    assert(!LegendsAchievementClaim(80) && !LegendsAchievementEarned(65535));
    assert(!LegendsQuestVisible(33) && !LegendsQuestStepComplete(33,0));
    linked=1;flags[FLAG_BADGE02_GET]=1;assert(!LegendsAchievementClaim(1));linked=0;
    LegendsJournalInit(TRUE);assert(!LegendsAchievementClaimed(0));
    puts("33 quests; 80 achievements; old saves, permanent unlocks, full-PC retry, claim idempotency and link guards passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'journal.c').write_text(preamble+s+main)
 subprocess.run(['cc','-std=gnu11','-Wall','-Wextra','-Werror','-Wno-unused-parameter','-iquote',str(R/'include'),'-iquote',str(R),str(p/'journal.c'),'-o',str(p/'journal')],check=True)
 subprocess.run([str(p/'journal')],check=True)
