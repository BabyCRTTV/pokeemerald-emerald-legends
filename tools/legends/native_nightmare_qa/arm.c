// Controlled native fixtures and queries; never shipped in a game ROM.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "event_object_movement.h"
#include "legends_clock.h"
#include "legends_seasons.h"
#include "legends_journal.h"
#include "legends_nightmare.h"
#include "pokemon.h"
#include "script.h"
#include "save.h"
#include "battle.h"
#include "item.h"
#include "task.h"
#include "constants/maps.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/species.h"
#include "constants/moves.h"
#include "constants/items.h"
#include "constants/heal_locations.h"
static const u16 flags[]={FLAG_LEGENDS_NIGHTMARE_CALL,FLAG_LEGENDS_NIGHTMARE_VISITED,FLAG_LEGENDS_NIGHTMARE_WING,FLAG_LEGENDS_NIGHTMARE_ENTERED,FLAG_LEGENDS_NIGHTMARE_VOICE,FLAG_LEGENDS_NIGHTMARE_RESOLVED,FLAG_LEGENDS_NIGHTMARE_CAUGHT,FLAG_LEGENDS_NIGHTMARE_REPORTED};
void qa(void)
{
 volatile u32 *b=(u32*)0x0203ffc0;
 if(b[0]==0){
  static const u16 maps[]={MAP_LILYCOVE_CITY,MAP_LEGENDS_NIGHTMARE_HOME,MAP_MT_PYRE_1F,MAP_LEGENDS_NIGHTMARE_BEDROOM,MAP_LEGENDS_NIGHTMARE_STREET,MAP_LEGENDS_NIGHTMARE_SHORE,MAP_DEWFORD_TOWN};
  static const u8 xs[]={50,6,21,6,50,14,8},ys[]={16,5,3,6,16,22,11};
  u16 map=maps[b[1]];u32 mask=b[2];NewGameInitData();gSaveBlock2Ptr->playerName[0]=0xbb;gSaveBlock2Ptr->playerName[1]=0xcd;gSaveBlock2Ptr->playerName[2]=0xc2;gSaveBlock2Ptr->playerName[3]=0xff;
  gSaveBlock2Ptr->optionsTextSpeed=2;gSaveBlock2Ptr->optionsBattleSceneOff=TRUE;
  for(u32 i=FLAG_BADGE01_GET;i<=FLAG_BADGE08_GET;i++)FlagSet(i);
  FlagSet(FLAG_SYS_GAME_CLEAR);FlagSet(FLAG_SYS_POKEMON_GET);FlagSet(FLAG_SYS_POKEDEX_GET);FlagSet(FLAG_RECEIVED_POKENAV);
  FlagSet(FLAG_LEGENDS_WYRMTIDE_CALL);if(mask&(1<<16))FlagSet(FLAG_LEGENDS_WYRMTIDE_CALMED);
  FlagSet(FLAG_HIDE_MAP_NAME_POPUP);FlagSet(FLAG_RESCUED_BIRCH);FlagSet(FLAG_SET_WALL_CLOCK);FlagSet(FLAG_RECEIVED_RUNNING_SHOES);FlagSet(FLAG_LEGENDS_FOLLOWERS_DISABLED);
  VarSet(VAR_REPEL_STEP_COUNT,30000);VarSet(VAR_LITTLEROOT_INTRO_STATE,9);VarSet(VAR_LITTLEROOT_RIVAL_STATE,4);VarSet(VAR_BIRCH_LAB_STATE,5);
  for(u32 i=0;i<8;i++)if(mask&(1<<i))FlagSet(flags[i]);
  CreateMonWithIVs(&gParties[B_TRAINER_PLAYER][0],SPECIES_RAYQUAZA,100,32,OTID_STRUCT_PLAYER_ID,31);SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0],MOVE_DRAGON_CLAW,0);
  for(u32 i=1;i<4;i++)SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0],MOVE_NONE,i);
  u16 stone=ITEM_EVERSTONE;SetMonData(&gParties[B_TRAINER_PLAYER][0],MON_DATA_HELD_ITEM,&stone);gPartiesCount[B_TRAINER_PLAYER]=1;
  AddBagItem(ITEM_MASTER_BALL,4);AddBagItem(ITEM_ORAN_BERRY,11);if(mask&4)AddBagItem(ITEM_LUNAR_WING,1);
  SetLastHealLocationWarp(HEAL_LOCATION_LILYCOVE_CITY);
  LegendsClockSetManual(12,0);LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);LegendsSetPlaytimeSeason(LEGENDS_SPRING);LegendsJournalInit(FALSE);
  SetWarpDestination(MAP_GROUP(map),MAP_NUM(map),-1,xs[b[1]],ys[b[1]]);WarpIntoMap();b[4]=1;SetMainCallback2(CB2_LoadMap);return;
 }
 if(b[0]==1){
  s16 x,y;PlayerGetDestCoords(&x,&y);b[5]=gSaveBlock1Ptr->location.mapGroup;b[6]=gSaveBlock1Ptr->location.mapNum;b[7]=0;for(u32 i=0;i<8;i++)if(FlagGet(flags[i]))b[7]|=1<<i;
  b[8]=CheckBagHasItem(ITEM_LUNAR_WING,1);b[9]=gMain.inBattle;b[10]=x-7;b[11]=y-7;b[12]=ScriptContext_IsEnabled()||ArePlayerFieldControlsLocked();b[13]=FuncIsActiveTask((TaskFunc)b[2]);b[14]=gPartiesCount[B_TRAINER_PLAYER];b[15]=gBattleOutcome;
 }
 if(b[0]==2){
  // A legal weak party for the actual loss/blackout case, not a forced outcome.
  ZeroMonData(&gParties[B_TRAINER_PLAYER][0]);CreateMon(&gParties[B_TRAINER_PLAYER][0],SPECIES_MAGIKARP,1,32,OTID_STRUCT_PLAYER_ID);SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0],MOVE_SPLASH,0);for(u32 i=1;i<4;i++)SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0],MOVE_NONE,i);gPartiesCount[B_TRAINER_PLAYER]=1;
 }
 if(b[0]==3){
  u32 before=0;for(u32 i=0;i<8;i++)if(FlagGet(flags[i]))before|=1<<i;
  b[5]=TrySavingData(SAVE_NORMAL);for(u32 i=0;i<8;i++)FlagClear(flags[i]);b[6]=LoadGameSave(SAVE_NORMAL);u32 after=0;for(u32 i=0;i<8;i++)if(FlagGet(flags[i]))after|=1<<i;b[7]=before==after;b[8]=CheckBagHasItem(ITEM_LUNAR_WING,1);b[9]=CheckBagHasItem(ITEM_CLEANSE_TAG,1);
 }
 if(b[0]==5){
  // Format-identical pre-house saved actor cache, on a newly solid wall tile.
  memcpy(gSaveBlock1Ptr->objectEvents,gObjectEvents,sizeof(gObjectEvents));
  gSaveBlock1Ptr->pos.x=50;gSaveBlock1Ptr->pos.y=14;
  for(u32 i=0;i<OBJECT_EVENTS_COUNT;i++)if(gSaveBlock1Ptr->objectEvents[i].isPlayer){
   struct ObjectEvent*o=&gSaveBlock1Ptr->objectEvents[i];o->initialCoords.x=o->currentCoords.x=o->previousCoords.x=57;o->initialCoords.y=o->currentCoords.y=o->previousCoords.y=21;
  }
  b[5]=TrySavingData(SAVE_NORMAL);b[6]=LoadGameSave(SAVE_NORMAL);
  // Use the actual production Continue path, which invokes the repair.
  b[4]=1;SetMainCallback2(CB2_ContinueSavedGame);return;
 }
 b[4]=1;SetMainCallback2((MainCallback)b[3]);
}
