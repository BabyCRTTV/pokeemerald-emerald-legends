// Private native scene setup and state assertions. Never shipped in a game ROM.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "event_object_movement.h"
#include "legends_clock.h"
#include "legends_seasons.h"
#include "legends_wyrmtide.h"
#include "legends_journal.h"
#include "pokemon.h"
#include "script.h"
#include "save.h"
#include "battle.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/species.h"
#include "constants/moves.h"
#include "constants/items.h"
#include "item.h"
static const u16 flags[]={FLAG_LEGENDS_WYRMTIDE_CALL,FLAG_LEGENDS_WYRMTIDE_LANDED,FLAG_LEGENDS_WYRMTIDE_SEAL_OPEN,FLAG_LEGENDS_WYRMTIDE_AWAKENED,FLAG_LEGENDS_WYRMTIDE_CALMED,FLAG_LEGENDS_WYRMTIDE_CAUGHT,FLAG_LEGENDS_WYRMTIDE_REPORT};
void qa(void)
{
 volatile u32 *b=(u32 *)0x0203ffc0;
 if(b[0]==0){
  static const u16 maps[]={MAP_DEWFORD_TOWN,MAP_LEGENDS_WYRMTIDE_ISLE,MAP_LEGENDS_WYRMTIDE_ISLE,MAP_LEGENDS_WYRMTIDE_DESCENT1,MAP_LEGENDS_WYRMTIDE_DESCENT2,MAP_LEGENDS_WYRMTIDE_DESCENT3,MAP_LEGENDS_WYRMTIDE_DESCENT4,MAP_LEGENDS_WYRMTIDE_HEART,MAP_DEWFORD_TOWN};
  static const u8 xs[]={11,14,16,13,9,9,9,11,8},ys[]={9,21,11,9,11,11,11,8,11};
  u16 map=maps[b[1]];NewGameInitData();gSaveBlock2Ptr->playerName[0]=0xBB;gSaveBlock2Ptr->playerName[1]=0xFF;
  gSaveBlock2Ptr->optionsTextSpeed=2;gSaveBlock2Ptr->optionsBattleSceneOff=TRUE;
  for(u32 i=FLAG_BADGE01_GET;i<=FLAG_BADGE08_GET;i++)FlagSet(i);
  FlagSet(FLAG_SYS_GAME_CLEAR);FlagSet(FLAG_SYS_POKEMON_GET);FlagSet(FLAG_SYS_POKEDEX_GET);FlagSet(FLAG_RECEIVED_POKENAV);
  FlagSet(FLAG_LEGENDS_STORY_REGIGIGAS_CALMED);FlagSet(FLAG_LEGENDS_STORY_WEATHER_REPORT);
  FlagSet(FLAG_HIDE_MAP_NAME_POPUP);FlagSet(FLAG_RESCUED_BIRCH);FlagSet(FLAG_SET_WALL_CLOCK);FlagSet(FLAG_RECEIVED_RUNNING_SHOES);FlagSet(FLAG_LEGENDS_FOLLOWERS_DISABLED);
  FlagSet(FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN);FlagSet(FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN);
  VarSet(VAR_LITTLEROOT_INTRO_STATE,9);VarSet(VAR_LITTLEROOT_RIVAL_STATE,4);VarSet(VAR_BIRCH_LAB_STATE,5);
  for(u32 i=0;i<7;i++)if(b[2]&(1<<i))FlagSet(flags[i]);
  CreateMonWithIVs(&gParties[B_TRAINER_PLAYER][0],SPECIES_TREECKO,100,32,OTID_STRUCT_PLAYER_ID,31);
  SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0],MOVE_AERIAL_ACE,0);for(u32 i=1;i<4;i++)SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0],MOVE_NONE,i);
  u16 stone=ITEM_EVERSTONE;SetMonData(&gParties[B_TRAINER_PLAYER][0],MON_DATA_HELD_ITEM,&stone);gPartiesCount[B_TRAINER_PLAYER]=1;
  AddBagItem(ITEM_MASTER_BALL,4);AddBagItem(ITEM_ORAN_BERRY,11);
  LegendsClockSetManual(12,0);LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);LegendsSetPlaytimeSeason(LEGENDS_SPRING);
  LegendsJournalInit(FALSE);
  SetWarpDestination(MAP_GROUP(map),MAP_NUM(map),-1,xs[b[1]],ys[b[1]]);WarpIntoMap();b[4]=1;SetMainCallback2(CB2_LoadMap);return;
 }
 if(b[0]==1){s16 x,y;PlayerGetDestCoords(&x,&y);b[5]=gSaveBlock1Ptr->location.mapGroup;b[6]=gSaveBlock1Ptr->location.mapNum;b[7]=0;for(u32 i=0;i<7;i++)if(FlagGet(flags[i]))b[7]|=1<<i;b[8]=LegendsWyrmtideHasMaker();b[9]=gMain.inBattle;b[10]=x-7;b[11]=y-7;b[12]=ScriptContext_IsEnabled();b[13]=VarGet(VAR_OBJ_GFX_ID_F);b[14]=gPartiesCount[B_TRAINER_PLAYER];b[15]=gBattleOutcome;}
 if(b[0]==2){
  if(!b[1]){ZeroMonData(&gParties[B_TRAINER_PLAYER][1]);gPartiesCount[B_TRAINER_PLAYER]=1;}
  else{CreateMon(&gParties[B_TRAINER_PLAYER][1],SPECIES_REGIGIGAS,70,32,OTID_STRUCT_PLAYER_ID);gPartiesCount[B_TRAINER_PLAYER]=2;u8 egg=b[1]==2;SetMonData(&gParties[B_TRAINER_PLAYER][1],MON_DATA_IS_EGG,&egg);if(b[1]==3){u16 hp=0;SetMonData(&gParties[B_TRAINER_PLAYER][1],MON_DATA_HP,&hp);}}
  b[5]=LegendsWyrmtideHasMaker();
 }
 if(b[0]==3){
  u32 before=0;for(u32 i=0;i<7;i++)if(FlagGet(flags[i]))before|=1<<i;
  b[5]=TrySavingData(SAVE_NORMAL);for(u32 i=0;i<7;i++)FlagClear(flags[i]);b[6]=LoadGameSave(SAVE_NORMAL);u32 after=0;for(u32 i=0;i<7;i++)if(FlagGet(flags[i]))after|=1<<i;b[7]=before==after;b[8]=after;
 }
 b[4]=1;SetMainCallback2((MainCallback)b[3]);
}
