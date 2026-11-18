"""Actual item-history bits and append-only full sector copies across both slots."""
from pathlib import Path
import subprocess,tempfile
R=Path(__file__).resolve().parents[1]
def function(path,signature):
 s=(R/path).read_text();start=s.index(signature+'\n{');return s[start:s.index('\n}',start)+2]
g=(R/'include/global.h').read_text();a=g.index('struct SaveBlock3\n{');block=g[a:g.index('};',a)+2]
legacy=block.replace('struct SaveBlock3','struct LegacySaveBlock3').replace('    struct LegendsJournalSave journal;\n','')
legacy=legacy.replace('    struct LegendsAchievementExtraSave achievementExtra;\n','')
legacy=legacy.replace('    struct LegendsPoffinSave poffins;\n','').replace('    struct LegendsMealSave meals;\n','').replace('    u8 extraItemFlags[LEGENDS_ITEM_FLAGS_EXTRA_COUNT];\n','')
legacy=legacy.replace('    struct LegendsGrottoSave grottos;\n','').replace('    struct LegendsEonSave eon;\n','')
legacy=legacy.replace('    u32 pinnedRecipe;\n','')
legacy=legacy.replace('#if OW_SHOW_ITEM_DESCRIPTIONS == OW_ITEM_DESCRIPTIONS_FIRST_TIME\n    u8 itemFlags[ITEM_FLAGS_COUNT];\n#endif\n','')
flags=(R/'include/overworld.h').read_text().split('enum ItemObtainFlags')[1].split('};')[0]
pre=r'''
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int32_t s32;typedef int bool32;typedef uint8_t bool8;
#define TRUE 1
#define FALSE 0
#define OW_ITEM_DESCRIPTIONS_FIRST_TIME 1
#define OW_SHOW_ITEM_DESCRIPTIONS 1
#define OW_USE_FAKE_RTC 0
#define FNPC_ENABLE_NPC_FOLLOWERS 0
#define USE_DEXNAV_SEARCH_LEVELS 0
#define APRICORN_TREE_COUNT 0
#define min(a,b) ((a)<(b)?(a):(b))
#define max(a,b) ((a)>(b)?(a):(b))
#define GUARD_MAIN_H
typedef void (*MainCallback)(void);
#include "constants/items.h"
#include "legends_adventure.h"
#include "legends_journal.h"
#include "legends_grottos.h"
#include "constants/species.h"
#include "legends_roamers.h"
#include "save.h"
#define ITEM_FLAGS_COUNT 110
#define LEGENDS_MEAL_SLOTS 3
#define LEGENDS_ITEM_FLAGS_EXTRA_COUNT 9
'''
# Match the ARM APCS structure-size boundary (native Pokeblock stride is 8).
pre+=g[g.index('struct Pokeblock\n{'):g.index('struct SaveBlock3\n{')].replace('struct Pokeblock\n{', 'struct __attribute__((aligned(4))) Pokeblock\n{')
pre+='enum ItemObtainFlags'+flags+'};\n'+legacy+'\n'+block+r'''
static struct SaveBlock3 gSaveblock3,*gSaveBlock3Ptr=&gSaveblock3;
static struct SaveSector flash[28],buffer,*gReadWriteSector=&buffer;
static struct SaveSectorLocation locations[14];
static u8 payload[14][SECTOR_DATA_SIZE];
u16 gLastWrittenSector;u32 gSaveCounter;
static u32 fail,writes;
static void CopyFromSaveBlock3(u32,struct SaveSector*);
static u16 CalculateChecksum(void*,u16);
static u8 TryWriteSector(u8 sector,u8 *data){writes++;if(fail)return SAVE_STATUS_ERROR;memcpy(&flash[sector],data,sizeof(struct SaveSector));return SAVE_STATUS_OK;}
u32 LegendsStorageLegacyBytes(void){return 34144;}
'''
code='\n'.join(function('src/save.c',x) for x in [
 'static u16 CalculateChecksum(void *data, u16 size)',
 'static u32 SaveBlock3Size(u32 sectorId)',
 'static void CopyToSaveBlock3(u32 sectorId, struct SaveSector *sector)',
 'static void CopyFromSaveBlock3(u32 sectorId, struct SaveSector *sector)',
 'static u8 HandleWriteSector(u16 sectorId, const struct SaveSectorLocation *locations)',
 'static bool32 StoredSectorValid(const struct SaveSector *sector, const struct SaveSectorLocation *locations)'])
code+='\n'+function('src/overworld.c','bool8 GetSetItemObtained(enum Item item, enum ItemObtainFlags caseId)')
meals=(R/'src/legends_meals.c').read_text()
code+=r'''
#include "legends_meals.h"
#define ARRAY_COUNT(a) (sizeof(a) / sizeof((a)[0]))
#define COMPOUND_STRING(text) ((const u8 *)(text))
static u8 ingredientStock[ITEMS_COUNT];
static bool32 CheckBagHasItem(enum Item item, u16 quantity)
{
    return ingredientStock[item] >= quantity;
}
'''
code+='\n'+next(line for line in meals.splitlines() if line.startswith('#define PINNED_RECIPE_TAG'))
code+='\n'+meals[meals.index('struct MealRecipe\n{'):meals.index('static bool32 MealSaveValid(void)')]
main=r'''
int main(void)
{
 assert(sizeof(struct LegacySaveBlock3)==0x21C);
 assert(offsetof(struct SaveBlock3,itemFlags)==0x21C);
 assert(offsetof(struct SaveBlock3,journal)==652);
 assert(offsetof(struct SaveBlock3,achievementExtra)==688 && offsetof(struct SaveBlock3,grottos)==716 && offsetof(struct SaveBlock3,eon)==992 && offsetof(struct SaveBlock3,poffins)==1032 && sizeof(struct Pokeblock)==8 && offsetof(struct SaveBlock3,meals)==1356 && offsetof(struct SaveBlock3,extraItemFlags)==1372);
 assert(offsetof(struct SaveBlock3,pinnedRecipe)==1384 && sizeof(struct SaveBlock3)==1388);
 enum Item missing[LEGENDS_RECIPE_INGREDIENTS];
 gSaveblock3.pinnedRecipe=PINNED_RECIPE_TAG | ITEM_ORAN_BERRY;
 assert(LegendsGetPinnedRecipe()==ITEM_NONE);
 LegendsTogglePinnedRecipe(ITEM_ORAN_BERRY);
 assert(gSaveblock3.pinnedRecipe==(PINNED_RECIPE_TAG | ITEM_ORAN_BERRY));
 for(unsigned i=0;i<ARRAY_COUNT(sRecipes);i++){
  const struct MealRecipe *recipe=&sRecipes[i];
  LegendsTogglePinnedRecipe(recipe->meal);
  assert(LegendsGetPinnedRecipe()==recipe->meal);
  memset(ingredientStock,0,sizeof(ingredientStock));
  unsigned total=LegendsGetMissingRecipeIngredients(recipe->meal,missing);
  assert(total>=2 && total<=LEGENDS_RECIPE_INGREDIENTS);
  for(unsigned bought=0;bought<total;bought++){
   assert(LegendsGetMissingRecipeIngredients(recipe->meal,missing)==total-bought);
   assert(missing[0]==recipe->supplies[bought]);
   ingredientStock[missing[0]]++;
  }
  assert(LegendsGetMissingRecipeIngredients(recipe->meal,missing)==0);
 }
 LegendsTogglePinnedRecipe(sRecipes[ARRAY_COUNT(sRecipes)-1].meal);
 assert(LegendsGetPinnedRecipe()==ITEM_NONE && gSaveblock3.pinnedRecipe==0);
 for(unsigned item=1;item<ITEMS_COUNT;item++){
  memset(&gSaveblock3,0,sizeof(gSaveblock3));assert(!GetSetItemObtained(item,FLAG_GET_ITEM_OBTAINED));
  assert(GetSetItemObtained(item,FLAG_SET_ITEM_OBTAINED));assert(GetSetItemObtained(item,FLAG_GET_ITEM_OBTAINED));
  for(unsigned other=1;other<ITEMS_COUNT;other++)assert(!!GetSetItemObtained(other,FLAG_GET_ITEM_OBTAINED)==(other==item));
 }
 // Older writers zero-filled the sector buffer and copied only the first eight extra bytes.
 const unsigned legacyEnd=1372+8;
 const unsigned sectorId=legacyEnd/SAVE_BLOCK_3_CHUNK_SIZE;
 struct SaveSector v087={0};
 memset(v087.saveBlock3Chunk,0xFF,legacyEnd%SAVE_BLOCK_3_CHUNK_SIZE);
 memset(&gSaveblock3,0xFF,sizeof(gSaveblock3));
 CopyToSaveBlock3(sectorId,&v087);
 assert(GetSetItemObtained(ITEM_VANILLA_LATTE,FLAG_GET_ITEM_OBTAINED));
 assert(!GetSetItemObtained(ITEM_ICED_PEACH_TEA,FLAG_GET_ITEM_OBTAINED));
 assert(!GetSetItemObtained(ITEM_GINGER_TEA,FLAG_GET_ITEM_OBTAINED));
 assert(LegendsGetPinnedRecipe()==ITEM_NONE);
 assert(!GetSetItemObtained(ITEM_NONE,FLAG_SET_ITEM_OBTAINED));assert(!GetSetItemObtained(ITEMS_COUNT,FLAG_SET_ITEM_OBTAINED));
 for(unsigned slot=0;slot<2;slot++)for(unsigned rotation=0;rotation<14;rotation++){
  gSaveCounter=slot;gLastWrittenSector=rotation;memset(&gSaveblock3,0x45,sizeof(gSaveblock3));
  struct SaveBlock3 expected=gSaveblock3;
  for(unsigned id=0;id<14;id++){memset(payload[id],id+3,sizeof(payload[id]));locations[id].data=payload[id];locations[id].size=SECTOR_DATA_SIZE;assert(HandleWriteSector(id,locations)==SAVE_STATUS_OK);}
  memset(&gSaveblock3,0,sizeof(gSaveblock3));
  for(unsigned id=0;id<14;id++){
   struct SaveSector *s=&flash[(id+rotation)%14+slot*14];assert(s->id==id&&s->counter==slot&&StoredSectorValid(s,locations));
   assert(!memcmp(s->data,payload[id],SECTOR_DATA_SIZE));CopyToSaveBlock3(id,s);
   s->checksum++;assert(!StoredSectorValid(s,locations));s->checksum--;
  }
  assert(!memcmp(&expected,&gSaveblock3,sizeof(expected)));
  struct SaveSector old={0};old.id=13;old.signature=SECTOR_SIGNATURE;
  memset(old.data,0xAB,sizeof(old.data));old.checksum=CalculateChecksum(old.data,2400);assert(StoredSectorValid(&old,locations));
  old.id=14;assert(!StoredSectorValid(&old,locations));
  struct SaveSector before=flash[(rotation)%14+slot*14];fail=1;assert(HandleWriteSector(0,locations)==SAVE_STATUS_ERROR);assert(!memcmp(&before,&flash[(rotation)%14+slot*14],sizeof(before)));fail=0;
 }
 puts("Every item flag; append-only fields; all 28 save slot/rotation layouts; full payloads, legacy checksums, corrupt IDs and failed writes passed.");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'sector.c').write_text(pre+code+main)
 subprocess.run(['cc','-std=gnu11','-Wall','-Wextra','-Werror','-iquote',str(R/'include'),str(p/'sector.c'),'-o',str(p/'check')],check=True)
 subprocess.run([str(p/'check')],check=True)
# Link and Frontier transactions now include the expanded inventory/PC payload.
s=(R/'src/save.c').read_text()
assert 'LegendsStoragePrepare()' in function('src/save.c','u8 HandleSavingData(u8 saveType)')
assert 'LinkFullSave_WriteSector()' in function('src/save.c','bool8 WriteSaveBlock1Sector(void)')
assert 'WriteSaveSectorOrSlot(FULL_SAVE_SLOT' in s.split('    case SAVE_LINK:')[1].split('    case SAVE_OVERWRITE_DIFFERENT_FILE:')[0]
