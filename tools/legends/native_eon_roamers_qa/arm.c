// Private native fixture; production state machine, battle and flash routines.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "pokemon.h"
#include "roamer.h"
#include "battle.h"
#include "battle_setup.h"
#include "script.h"
#include "save.h"
#include "item.h"
#include "pokedex.h"
#include "legends_clock.h"
#include "legends_seasons.h"
#include "constants/moves.h"
static u32 Hash(const void *p,u32 n){const u8 *s=p;u32 h=2166136261u;while(n--)h=(h^*s++)*16777619u;return h;}
void qa(void)
{
 volatile u32 *b=(u32*)0x0203ffc0;
 if(b[0]==0){
  NewGameInitData();gSaveBlock2Ptr->playerName[0]=0xBB;gSaveBlock2Ptr->playerName[1]=0xFF;
  gSaveBlock2Ptr->optionsTextSpeed=2;gSaveBlock2Ptr->optionsBattleSceneOff=TRUE;
  FlagSet(FLAG_SYS_POKEMON_GET);FlagSet(FLAG_SYS_POKEDEX_GET);FlagSet(FLAG_HIDE_MAP_NAME_POPUP);FlagSet(FLAG_RESCUED_BIRCH);FlagSet(FLAG_SET_WALL_CLOCK);FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
  VarSet(VAR_LITTLEROOT_INTRO_STATE,9);VarSet(VAR_LITTLEROOT_RIVAL_STATE,4);VarSet(VAR_BIRCH_LAB_STATE,5);
  CreateMonWithIVs(&gParties[B_TRAINER_PLAYER][0],SPECIES_RAYQUAZA,100,32,OTID_STRUCT_PLAYER_ID,31);
  SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0],MOVE_DRAGON_CLAW,0);
  for(u32 i=1;i<4;i++)SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0],MOVE_NONE,i);
  u16 stone=ITEM_EVERSTONE;SetMonData(&gParties[B_TRAINER_PLAYER][0],MON_DATA_HELD_ITEM,&stone);gPartiesCount[B_TRAINER_PLAYER]=1;
  AddBagItem(ITEM_MASTER_BALL,8);AddBagItem(ITEM_ORAN_BERRY,11);LegendsClockSetManual(12,0);LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);LegendsSetPlaytimeSeason(LEGENDS_AUTUMN);
  FlagSet(FLAG_LATIOS_OR_LATIAS_ROAMING);gSpecialVar_0x8004=b[1];InitRoamer();
  SetWarpDestination(MAP_GROUP(MAP_ROUTE110),MAP_NUM(MAP_ROUTE110),-1,10,10);WarpIntoMap();b[4]=1;SetMainCallback2(CB2_LoadMap);return;
 }
 if(b[0]==2 || b[0]==5){
  struct Roamer first=*GetRoamer(0);struct LegendsEonSave second=gSaveBlock3Ptr->eon;
  u32 prefix=Hash(gSaveBlock3Ptr,992),party=Hash(gParties[B_TRAINER_PLAYER],sizeof(gParties[B_TRAINER_PLAYER]));
  if(b[0]==2)memset(&gSaveBlock3Ptr->eon,0xA5,sizeof(gSaveBlock3Ptr->eon));
  b[5]=TrySavingData(SAVE_NORMAL);prefix=Hash(gSaveBlock3Ptr,992);memset(gSaveBlock3Ptr,0,sizeof(*gSaveBlock3Ptr));b[6]=LoadGameSave(SAVE_NORMAL);LegendsRoamerInit(FALSE);
  b[7]=Hash(&first,sizeof(first))==Hash(GetRoamer(0),sizeof(first));b[8]=prefix==Hash(gSaveBlock3Ptr,992);b[9]=party==Hash(gParties[B_TRAINER_PLAYER],sizeof(gParties[B_TRAINER_PLAYER]));
  b[10]=b[0]==2?!gSaveBlock3Ptr->eon.unlocked:Hash(&second,sizeof(second))==Hash(&gSaveBlock3Ptr->eon,sizeof(second));
  b[11]=CheckBagHasItem(ITEM_ORAN_BERRY,11)&&LegendsGetActiveSeason()==LEGENDS_AUTUMN;
 }
 if(b[0]==3){
  u32 target=b[1],attempt=0;
  do{while(!IsRoamerAt(target,gSaveBlock1Ptr->location.mapGroup,gSaveBlock1Ptr->location.mapNum)&&attempt++<10000)RoamerMoveToOtherLocationSet(target);
   if(attempt>=10000)break;
  }while((!TryStartRoamerEncounter()||gEncounteredRoamerIndex!=target)&&attempt++<10000);
  b[5]=attempt<10000&&gEncounteredRoamerIndex==target;b[4]=1;
  if(b[5]){gMain.callback2=(MainCallback)b[3];BattleSetup_StartRoamerBattle();return;}
 }
 if(b[0]==7){
  b[5]=offsetof(struct SaveBlock1,roamer);b[6]=Hash(GetRoamer(0),sizeof(struct Roamer));b[7]=gSaveBlock3Ptr->eon.checksum;b[8]=GetRoamer(0)->active;b[9]=GetRoamer(1)->active;b[10]=gSaveBlock3Ptr->eon.unlocked;b[11]=gPartiesCount[B_TRAINER_PLAYER];
 }
 if(b[0]==4){
  b[5]=GetRoamer(0)->active;b[6]=GetRoamer(1)->active;b[7]=gSaveBlock3Ptr->eon.unlocked;b[8]=gBattleOutcome;b[9]=gMain.inBattle;b[10]=ScriptContext_IsEnabled();b[11]=gPartiesCount[B_TRAINER_PLAYER];b[12]=GetRoamer(0)->species;b[13]=GetRoamer(1)->species;b[14]=Hash(GetRoamer(1),sizeof(struct Roamer));
 }
 b[4]=1;gMain.callback2=(MainCallback)b[3];
}
