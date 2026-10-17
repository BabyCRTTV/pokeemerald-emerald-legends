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
#include <stddef.h>
typedef uint8_t u8; typedef uint8_t bool8;
#define EWRAM_DATA
typedef uint16_t u16; typedef uint32_t u32; typedef int bool32;
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
#include "legends_field_requests.h"
#include "src/data/legends/journal.h"
static struct {struct LegendsJournalSave journal;struct LegendsAchievementExtraSave achievementExtra;} data,*gSaveBlock3Ptr=&data;
static u8 flags[4096];static u32 stats[64],dex,pcQuantity,pcItem,full,linked;
bool32 FlagGet(u16 flag){assert(flag<4096);return flags[flag];}
u32 GetGameStat(u8 id){assert(id<64);return stats[id];}
u32 GetNationalPokedexCount(u8 mode){return dex;}
bool32 IsOverworldLinkActive(void){return linked;}
bool32 AddPCItem(u16 item,u16 count){if(full)return FALSE;pcItem=item;pcQuantity+=count;return TRUE;}
#ifndef TEST_REAL_FIELD_REQUESTS
u16 LegendsFieldRequestActive(void){return FIELD_REQUEST_NONE;}
static u32 researchDone;
bool32 LegendsFieldRequestComplete(u16 id){return !!(researchDone & (1u<<id));}
u8 LegendsFieldRequestOwner(u16 id){return id < 18 ? 0 : 1;}
bool32 LegendsFieldRequestStepComplete(u16 id,u8 step){return FALSE;}
#endif
'''
# Include the catalogue after condition structs only once.
s=s.replace('#define JOURNAL_MAGIC','#define JOURNAL_MAGIC',1)
main=r'''
int main(void)
{
    memset(&data,0xA5,sizeof(data)); flags[FLAG_BADGE01_GET]=1;
    stats[GAME_STAT_POKEMON_CAPTURES]=100; dex=200;
    LegendsJournalInit(FALSE);
    assert(LegendsAchievementCount()==130 && LegendsQuestCount()==63);
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
    for(unsigned q=0;q<LEGENDS_FIELD_REQUEST_QUEST_BASE;q++)
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
    assert(!LegendsAchievementClaim(130) && !LegendsAchievementEarned(65535));
    assert(!LegendsQuestVisible(33) && !LegendsQuestStepComplete(33,0));
    linked=1;flags[FLAG_BADGE02_GET]=1;assert(!LegendsAchievementClaim(1));linked=0;
    LegendsJournalInit(TRUE);assert(!LegendsAchievementClaimed(0));
    // Version-1 / 80-achievement saves keep their exact layout and claim bits.
    assert(sizeof(struct LegendsJournalSave)==36);
    assert(offsetof(struct LegendsJournalSave,earned)==12 && offsetof(struct LegendsJournalSave,claimed)==24);
    memset(flags,0,sizeof(flags));memset(stats,0,sizeof(stats));dex=0;
    LegendsJournalInit(TRUE);
    memset(data.journal.earned,0xAA,10);memset(data.journal.claimed,0x22,10);
    data.journal.checksum=Checksum();before=data.journal;
    LegendsJournalInit(FALSE);assert(!memcmp(&before,&data.journal,sizeof(before)));
    assert(LegendsAchievementNotice()==0xFFFF);
    flags[FLAG_RECEIVED_BIKE]=1;unsigned pcBefore=pcQuantity;
    LegendsJournalInit(FALSE);
    assert(!memcmp(before.earned,data.journal.earned,10)&&!memcmp(before.claimed,data.journal.claimed,10));
    assert(LegendsAchievementEarned(80)&&!LegendsAchievementClaimed(80));
    assert(LegendsAchievementNotice()==0xFFFF&&pcQuantity==pcBefore); // Quiet, unrewarded backfill.
    // Each appended ID unlocks at its threshold, queues once and needs a manual claim.
    for(unsigned id=80;id<130;id++){
        memset(flags,0,sizeof(flags));memset(stats,0,sizeof(stats));dex=0;
        researchDone=0;LegendsJournalInit(TRUE);const struct LegendsAchievement *a=LegendsAchievementGet(id);
        if(a->kind==JOURNAL_FLAG){flags[a->key]=1;LegendsJournalFlagSet(a->key);}
        else if(a->kind==JOURNAL_STAT){stats[a->key]=a->target-1;LegendsJournalStatSet(a->key,a->target-1);assert(!LegendsAchievementEarned(id));stats[a->key]=a->target;LegendsJournalStatSet(a->key,a->target);}
        else if(a->kind==JOURNAL_RESEARCH){unsigned start=a->key==1?18:0;for(unsigned n=0;n+1<a->target;n++)researchDone|=1u<<(start+n);LegendsJournalRefresh();assert(!LegendsAchievementEarned(id));researchDone|=1u<<(start+a->target-1);LegendsJournalRefresh();}
        else {dex=a->target-1;LegendsJournalRefresh();assert(!LegendsAchievementEarned(id));dex=a->target;LegendsJournalRefresh();}
        assert(LegendsAchievementEarned(id)&&!LegendsAchievementClaimed(id));
        assert(sPending[id/8]&(1<<(id%8)));
        LegendsAchievementNoticeDismiss(id);LegendsJournalRefresh();assert(!(sPending[id/8]&(1<<(id%8))));
        full=1;assert(!LegendsAchievementClaim(id)&&!LegendsAchievementClaimed(id));
        full=0;unsigned quantity=pcQuantity;assert(LegendsAchievementClaim(id)&&LegendsAchievementClaimed(id));assert(pcQuantity==quantity+a->quantity);assert(!LegendsAchievementClaim(id));
        LegendsJournalInit(FALSE);assert(LegendsAchievementEarned(id)&&LegendsAchievementClaimed(id)&&LegendsAchievementNotice()==0xFFFF);
    }
    // Unchanged v1 reserved bytes: every possible word has a bounded, read-only meaning.
    memset(flags,0,sizeof(flags));LegendsJournalInit(TRUE);
    for(unsigned word=0;word<=65535;word++){
        data.journal.reserved=word;struct LegendsJournalSave snapshot=data.journal;
        unsigned id=(word&255)-1;
        unsigned expected=(word&0xFF00)==0xA700 && (word&255) && id<LegendsQuestCount()
            && LegendsQuestNextStep(id)!=0xFF ? id:0xFFFF;
        assert(LegendsQuestTracked()==expected);
        assert(!memcmp(&snapshot,&data.journal,sizeof(snapshot)));
    }
    data.journal.reserved=0;data.journal.checksum=Checksum();before=data.journal;
    LegendsJournalInit(FALSE);assert(!memcmp(&before,&data.journal,sizeof(before)));
    assert(LegendsQuestTracked()==0xFFFF);
    assert(!LegendsQuestTrack(33)&&!LegendsQuestTrack(2)); // Invalid and undiscovered.
    assert(!memcmp(&before,&data.journal,sizeof(before)));
    assert(LegendsQuestTrack(0)&&LegendsQuestTracked()==0&&LegendsQuestNextStep(0)==0);
    before=data.journal;LegendsJournalInit(FALSE);assert(!memcmp(&before,&data.journal,sizeof(before)));
    flags[FLAG_SYS_POKEMON_GET]=1;assert(LegendsQuestNextStep(0)==1);
    flags[FLAG_SYS_POKEDEX_GET]=1;assert(LegendsQuestTracked()==0xFFFF);
    LegendsJournalRefresh();assert(data.journal.reserved==0xA700);
    assert(!LegendsQuestTrack(0)); // Completed quests cannot be pinned.
    assert(LegendsQuestTrack(1)&&LegendsQuestTracked()==1);
    assert(LegendsQuestTrack(27)&&LegendsQuestTracked()==27); // Switch to bicycle side quest.
    before=data.journal;linked=1;assert(!LegendsQuestTrack(1)&&!LegendsQuestTrack(0xFFFF));
    assert(!memcmp(&before,&data.journal,sizeof(before)));linked=0;
    assert(LegendsQuestTrack(0xFFFF)&&LegendsQuestTracked()==0xFFFF);
    before=data.journal;LegendsJournalInit(FALSE);assert(!memcmp(&before,&data.journal,sizeof(before)));
    assert(sizeof(data.journal)==36&&offsetof(struct LegendsJournalSave,reserved)==10);

    // A valid v0.0.59 journal survives arbitrary unused tail bytes; bit 95 was unpublished.
    memset(flags,0,sizeof(flags));memset(stats,0,sizeof(stats));dex=researchDone=0;
    LegendsJournalInit(TRUE);
    memset(data.journal.earned,0xFF,12);memset(data.journal.claimed,0x55,12);
    data.journal.claimed[11]|=0x80; data.journal.checksum=Checksum();before=data.journal;
    memset(&data.achievementExtra,0xA5,sizeof(data.achievementExtra));
    LegendsJournalInit(FALSE);
    assert(!memcmp(before.earned,data.journal.earned,11)&&!memcmp(before.claimed,data.journal.claimed,11));
    assert(data.journal.earned[11]==0x7F && data.journal.claimed[11]==0x55);
    for(unsigned id=95;id<130;id++)assert(!LegendsAchievementEarned(id)&&!LegendsAchievementClaimed(id));
    assert(ExtraChecksum()==data.achievementExtra.checksum);
    // Every new bit, including 95, 96, 127, 128 and 129, persists independently.
    for(unsigned id=95;id<130;id++){
        Earn(id);u16 bit=AchievementBitId(id);AchievementBits(id,TRUE)[bit/8]|=1<<(bit%8);
    }
    UpdateChecksums();typeof(data) all=data;
    LegendsJournalInit(FALSE);assert(!memcmp(&all,&data,sizeof(data)));
    for(unsigned id=95;id<130;id++)assert(LegendsAchievementEarned(id)&&LegendsAchievementClaimed(id));
    assert(LegendsAchievementNotice()==0xFFFF);
    // Legacy checksum and tracked-quest word remain independent of the appended tail.
    assert(sizeof(data.journal)==36&&sizeof(data.achievementExtra)==28);
    puts("63 quests; 130 achievements; legacy tracking words, progression, persistence, claims and link guards passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'journal.c').write_text(preamble+s+main)
 subprocess.run(['cc','-std=gnu11','-Wall','-Wextra','-Werror','-Wno-unused-parameter','-iquote',str(R/'include'),'-iquote',str(R),str(p/'journal.c'),'-o',str(p/'journal')],check=True)
 subprocess.run([str(p/'journal')],check=True)

# Published IDs 0-79 retain their original definitions; new IDs are append-only.
import re,hashlib
catalogue=(R/'src/data/legends/journal.h').read_text().split('static const struct LegendsAchievement sAchievements[] =')[1]
entries=re.findall(r'\{COMPOUND_STRING[^\n]+',catalogue)
assert len(entries)==130
assert hashlib.sha256(('\n'.join(entries[:80])+'\n').encode()).hexdigest()=="18a8c74c46e5596c5d7a3c8f9f7e5f1f120d13cfbd9b970800e6683b0f264f12"

assert hashlib.sha256(('\n'.join(entries[:95])+'\n').encode()).hexdigest()=="43683155034a7ab8eae45443de9e15a46ff7174794b098fb5b02a41ef90d12dd"

# The editable authoring data and native catalogue must agree on every stable ID.
import json
rows=json.loads((R/'data/legends/achievements.json').read_text())
assert len(rows)==130
for i,row in enumerate(rows):
 assert row['id']==i
 expected='{COMPOUND_STRING("%s"), COMPOUND_STRING("%s"), JOURNAL_%s, %s, %s, ITEM_%s_BERRY, %s},'%(row['title'],row['description'],row['kind'],row['key'],row['target'],row['berry'],row['quantity'])
 assert entries[i].strip()==expected
