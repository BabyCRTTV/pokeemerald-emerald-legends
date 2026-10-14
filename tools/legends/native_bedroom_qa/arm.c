// Controlled QA callback, linked only into a private emulator ROM copy.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "fieldmap.h"
#include "event_data.h"
#include "legends_journal.h"
#include "legends_bedroom.h"
#include "decoration.h"
#include "decoration_inventory.h"
#include "task.h"
#include "save.h"
#include "pokemon.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/decorations.h"
#include "constants/species.h"
static void room(void)
{
    SetWarpDestination(MAP_GROUP(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F),
        gSaveBlock2Ptr->playerGender ? MAP_NUM(MAP_LITTLEROOT_TOWN_MAYS_HOUSE_2F) : MAP_NUM(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F), -1, 4, 5);
    WarpIntoMap(); SetMainCallback2(CB2_LoadMap);
}
void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    switch (box[0])
    {
    case 0: case 1:
        NewGameInitData(); gSaveBlock2Ptr->playerGender = box[0];
        gSaveBlock2Ptr->playerName[0] = 0xBB; gSaveBlock2Ptr->playerName[1] = 0xFF;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP); FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_SWABLU_DOLL);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_POKE_BALL);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_POKE_BALL);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_PICHU_DOLL);
        FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_BEDROOM_MOM);
        FlagSet(FLAG_BADGE01_GET); FlagSet(FLAG_BADGE05_GET); FlagSet(FLAG_SYS_GAME_CLEAR);
        FlagSet(FLAG_LEGENDS_KANTO_SURVEY_REPORT); FlagSet(FLAG_LEGENDS_FINAL_HOENN_EPILOGUE);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 3);
        VarSet(VAR_BIRCH_LAB_STATE, 2);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 5, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        DecorationAdd(DECOR_PIKACHU_DOLL);
        LegendsJournalInit(FALSE); room(); break;
    case 2:
        CreateTask(DoPlayerRoomDecorationMenu, 8);
        SetMainCallback2(CB2_Overworld); break;
    case 3:
        CleanupOverworldWindowsAndTilemaps(); ResetTasks(); room(); break;
    case 4:
        // Real flash write/load round trip; no new save layout or reader.
        box[4] = TrySavingData(SAVE_NORMAL);
        VarSet(VAR_LEGENDS_BEDROOM_COLORS, 0);
        gSaveBlock1Ptr->playerRoomDecorations[0] = 0;
        gSaveBlock1Ptr->playerRoomDecorationPositions[0] = 0;
        box[5] = LoadGameSave(SAVE_NORMAL);
        box[6] = VarGet(VAR_LEGENDS_BEDROOM_COLORS);
        SetMainCallback2(CB2_Overworld); break;
    case 5:
        gSaveBlock1Ptr->playerRoomDecorations[0] = DECOR_PIKACHU_DOLL;
        gSaveBlock1Ptr->playerRoomDecorationPositions[0] = (gSaveBlock2Ptr->playerGender ? 8 << 4 : 0) | 7;
        CleanupOverworldWindowsAndTilemaps(); ResetTasks(); room(); break;
    case 9:
        box[7] = gSaveBlock1Ptr->playerRoomDecorations[0];
        box[8] = gSaveBlock1Ptr->playerRoomDecorationPositions[0];
        box[1] = VarGet(VAR_LEGENDS_BEDROOM_COLORS);
        box[2] = LegendsBedroomCanPlace(MAP_OFFSET + 3, MAP_OFFSET + 7, 1, 1);
        box[3] = LegendsBedroomCanPlace(MAP_OFFSET + (gSaveBlock2Ptr->playerGender ? 7 : 1), MAP_OFFSET + 7, 1, 1);
        SetMainCallback2(CB2_Overworld); break;
    }
}
