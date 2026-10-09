"""Exercise upstream's actual held-item functions with Legends' Gen 9 settings."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
source=(root/'src/battle_util.c').read_text()
source=source[source.index('struct LostItem *GetLostItemState('):source.index('bool32 CanStealItem(')]
pre=r'''
#include <assert.h>
#include <stdio.h>
typedef unsigned int u32;typedef int bool32;
enum Item {ITEM_NONE, ITEM_HYPER_POTION, ITEM_SUPER_POTION, ITEM_BERRY};
enum BattleTrainer {B_TRAINER_PLAYER,B_TRAINER_OPPONENT,B_TRAINER_PARTNER,B_TRAINER_OTHER};
enum BattlerId {PLAYER,OPPONENT,PARTNER,OTHER};
#define PARTY_SIZE 6
#define GEN_9 9
#define TRUE 1
#define FALSE 0
#define MON_DATA_HELD_ITEM 1
#define POCKET_BERRIES 4
#define B_RESTORE_HELD_BATTLE_ITEMS GEN_9
#define B_TRAINERS_KNOCK_OFF_ITEMS TRUE
struct Pokemon {enum Item item;};
struct LostItem {enum Item originalItem;unsigned stolen:1,restoreAfterBattle:1,wildItemPending:1;};
struct BattleStruct {struct {enum Item usedHeldItem;} partyState[4][6];struct LostItem itemLost[4][6];};
static struct BattleStruct state,*gBattleStruct=&state;
static struct Pokemon gParties[4][6];static u32 gBattlersCount=2,gBattlerPartyIndexes[4],bag[4];
static enum Item GetMonData(struct Pokemon *p,int field){return p->item;}
static void SetMonData(struct Pokemon *p,int field,enum Item *item){p->item=*item;}
static int GetItemPocket(enum Item item){return item==ITEM_BERRY?POCKET_BERRIES:1;}
static void AddBagItem(enum Item item,int count){bag[item]+=count;}
static enum BattleTrainer GetBattlerTrainer(enum BattlerId b){return (enum BattleTrainer)b;}
'''
main=r'''
int main(void){
 gParties[PLAYER][0].item=ITEM_SUPER_POTION;SetItemsToRestoreAfterBattle(PLAYER,0);
 gParties[PLAYER][0].item=ITEM_NONE;TryRestoreHeldItems();assert(gParties[PLAYER][0].item==ITEM_SUPER_POTION);
 gParties[PLAYER][1].item=ITEM_BERRY;SetItemsToRestoreAfterBattle(PLAYER,1);
 gParties[PLAYER][1].item=ITEM_NONE;TryRestoreHeldItems();assert(gParties[PLAYER][1].item==ITEM_NONE);
 gParties[OPPONENT][0].item=ITEM_HYPER_POTION;SetItemsToRestoreAfterBattle(OPPONENT,0);
 gParties[OPPONENT][0].item=ITEM_NONE;state.itemLost[OPPONENT][0].wildItemPending=TRUE;
 struct Pokemon caught={ITEM_NONE};RestoreCaughtWildMonHeldItem(&caught,OPPONENT);
 assert(caught.item==ITEM_HYPER_POTION&&!state.itemLost[OPPONENT][0].wildItemPending);
 TryRestoreHeldItems();assert(bag[ITEM_HYPER_POTION]==0);
 SetItemsToRestoreAfterBattle(OPPONENT,0);state.itemLost[OPPONENT][0].wildItemPending=TRUE;
 TryRestoreHeldItems();assert(bag[ITEM_HYPER_POTION]==1);
 state.itemLost[OPPONENT][0].wildItemPending=FALSE;caught.item=ITEM_SUPER_POTION;
 RestoreCaughtWildMonHeldItem(&caught,OPPONENT);assert(caught.item==ITEM_NONE);
 gBattlersCount=4;gParties[PARTNER][0].item=ITEM_SUPER_POTION;
 SetItemsToRestoreAfterBattle(PARTNER,0);gParties[PARTNER][0].item=ITEM_NONE;
 TryRestoreHeldItems();assert(gParties[PARTNER][0].item==ITEM_SUPER_POTION);
 puts("Upstream held-item restoration, berries, captured wild items, bag routing and partner slots passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'items.c').write_text(pre+source+main)
 subprocess.run(['cc','-std=gnu17','-Wall','-Werror','-o',str(p/'items'),str(p/'items.c')],check=True)
 subprocess.run([str(p/'items')],check=True)
assert 'RestoreCaughtWildMonHeldItem(caughtMon, gBattlerTarget);' in (root/'src/battle_script_commands.c').read_text()
