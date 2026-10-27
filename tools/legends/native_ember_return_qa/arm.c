// Private fixture and observations only; production events/movement stay unaltered.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "pokemon.h"
#include "script.h"
#include "task.h"
#include "save.h"
#include "config/overworld.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/species.h"
void qa(void)
{
    volatile u32 *b = (u32 *)0x0203ffc0;
    if (b[0] == 0)
    {
        NewGameInitData();
        gSaveBlock2Ptr->playerName[0] = 0xBB;
        gSaveBlock2Ptr->playerName[1] = 0xFF;
        gSaveBlock2Ptr->optionsTextSpeed = 2;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP); FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
        FlagSet(FLAG_SYS_GAME_CLEAR);
        if (b[1]) { FlagSet(FLAG_LEGENDS_STORY_NORTH_REPORT); FlagSet(FLAG_LEGENDS_KANTO_BLAINE_WON); }
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 4);
        VarSet(VAR_BIRCH_LAB_STATE, 5);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 25, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        SetWarpDestination(MAP_GROUP(MAP_LEGENDS_KANTO_MT_EMBER_EXTERIOR), MAP_NUM(MAP_LEGENDS_KANTO_MT_EMBER_EXTERIOR), -1, 28, 47);
        WarpIntoMap(); b[4] = 1; SetMainCallback2(CB2_LoadMap); return;
    }
    if (b[0] == 2)
    {
        b[5] = TrySavingData(SAVE_NORMAL);
        b[6] = offsetof(struct SaveBlock1, flags);
        b[7] = FLAG_LEGENDS_STORY_NORTH_REPORT;
        b[8] = FLAG_LEGENDS_KANTO_BLAINE_WON;
        b[9] = FLAG_LEGENDS_STORY_EMBER_REPORT;
    }
    if (b[0] == 1)
    {
        s16 x,y; PlayerGetDestCoords(&x,&y);
        b[5] = gSaveBlock1Ptr->location.mapGroup;
        b[6] = gSaveBlock1Ptr->location.mapNum;
        b[7] = MAP_GROUP(MAP_LEGENDS_KANTO_CINNABAR_ISLAND);
        b[8] = MAP_NUM(MAP_LEGENDS_KANTO_CINNABAR_ISLAND);
        b[9] = MapGridGetCollisionAt(x,y);
        b[10] = x-7; b[11] = y-7;
        b[12] = ScriptContext_IsEnabled() || (MainCallback)b[3] != CB2_Overworld;
        b[13] = FindTaskIdByFunc((TaskFunc)QA_YESNO) != TASK_NONE;
        b[12] |= b[13]; b[1] = gSpecialVar_Result;
        b[14] = (FlagGet(FLAG_LEGENDS_STORY_NORTH_REPORT) ? 1 : 0) | (FlagGet(FLAG_LEGENDS_KANTO_BLAINE_WON) ? 2 : 0) | (FlagGet(FLAG_LEGENDS_STORY_EMBER_REPORT) ? 4 : 0);
        b[15] = OW_FLAG_NO_COLLISION && FlagGet(OW_FLAG_NO_COLLISION);
    }
    b[4] = 1; gMain.callback2 = (MainCallback)b[3];
}
