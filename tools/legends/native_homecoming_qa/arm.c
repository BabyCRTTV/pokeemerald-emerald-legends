// Controlled native setup only; linked into a private ROM copy, never shipped.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "script.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "config/overworld.h"
#include "task.h"
#include "save.h"
#include "pokemon.h"
#include "legends_appearance.h"
#include "legends_seasons.h"
#include "legends_settings.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/map_event_ids.h"
#include "constants/species.h"
static void room(void)
{
    u16 map = gSaveBlock2Ptr->playerGender ? MAP_NUM(MAP_LITTLEROOT_TOWN_MAYS_HOUSE_1F) : MAP_NUM(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F);
    SetWarpDestination(MAP_GROUP(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F), map, -1,
        gSaveBlock2Ptr->playerGender ? 9 : 1, 7);
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
        gSaveBlock2Ptr->optionsTextSpeed = 2;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP); FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
        FlagSet(FLAG_BADGE01_GET); FlagSet(FLAG_BADGE05_GET); FlagSet(FLAG_SYS_GAME_CLEAR);
        FlagSet(FLAG_LEGENDS_KANTO_WELCOMED); FlagSet(FLAG_LEGENDS_FINAL_HOENN_EPILOGUE);
        FlagSet(FLAG_RECEIVED_SS_TICKET); FlagSet(FLAG_RECEIVED_AMULET_COIN);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_1);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_2);
        FlagSet(FLAG_HIDE_PLAYERS_HOUSE_DAD);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_MOM);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_MOM);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_RIVAL_SIBLING);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_RIVAL_SIBLING);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_BRENDAN);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_MAY);
        FlagClear(gSaveBlock2Ptr->playerGender ? FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_MOM : FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_MOM);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 3);
        VarSet(VAR_LITTLEROOT_HOUSES_STATE_MAY, 4); VarSet(VAR_LITTLEROOT_HOUSES_STATE_BRENDAN, 4);
        LegendsSetAppearanceSelection(3, 3); LegendsApplyAppearanceToNewGame();
        LegendsBeginWardrobeSelection(); LegendsSetHairSelection(2); LegendsSetHairColorSelection(3);
        LegendsSetShoeSelection(4); LegendsApplyWardrobeSelection();
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME); LegendsSetPlaytimeSeason(LEGENDS_WINTER);
        VarSet(VAR_LEGENDS_BEDROOM_COLORS, 0xB423); VarSet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR, 0xCA03);
        // Prepared pre-feature state in the unchanged v0.0.54-format save layout.
        VarSet(VAR_LEGENDS_HOMECOMING_MEMORY, 0xFFFF);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 15, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        room(); break;
    case 2:
    {
        s16 x, y;
        PlayerGetDestCoords(&x, &y);
        box[14] = x - MAP_OFFSET; box[15] = y - MAP_OFFSET;
        box[16] = MapGridGetCollisionAt(x, y);
        box[17] = OW_FLAG_NO_COLLISION && FlagGet(OW_FLAG_NO_COLLISION);
        box[18] = MapGridGetCollisionAt((gSaveBlock2Ptr->playerGender ? 7 : 3) + MAP_OFFSET, 7 + MAP_OFFSET);
        box[1] = VarGet(VAR_LEGENDS_HOMECOMING_MEMORY);
        box[2] = ScriptContext_IsEnabled();
        box[3] = GetObjectEventIdByLocalIdAndMap(LOCALID_PLAYERS_HOUSE_1F_DAD,
            gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
        box[4] = VarGet(VAR_LEGENDS_APPEARANCE);
        box[5] = VarGet(VAR_LEGENDS_BEDROOM_COLORS);
        box[6] = VarGet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR);
        box[7] = LegendsGetSkinTone(); box[8] = LegendsGetHair(); box[9] = LegendsGetHairColor();
        box[10] = LegendsGetSeasonMode(); box[11] = LegendsGetSeason();
        SetMainCallback2(CB2_Overworld); break;
    }
    case 4:
        FlagClear(FLAG_LEGENDS_FINAL_HOENN_EPILOGUE); FlagClear(FLAG_LEGENDS_KANTO_WELCOMED);
        VarSet(VAR_LEGENDS_HOMECOMING_MEMORY, 0);
        SetMainCallback2(CB2_Overworld); break;
    case 5:
        VarSet(VAR_PETALBURG_GYM_STATE, 7); VarSet(VAR_ENIGMA_BERRY_AVAILABLE, 0);
        FlagSet(FLAG_RECEIVED_TM_FACADE); FlagClear(FLAG_HIDE_PETALBURG_GYM_NORMAN);
        CleanupOverworldWindowsAndTilemaps(); ResetTasks();
        SetWarpDestination(MAP_GROUP(MAP_PETALBURG_CITY_GYM), MAP_NUM(MAP_PETALBURG_CITY_GYM), -1, 4, 108);
        WarpIntoMap(); SetMainCallback2(CB2_LoadMap); break;
    case 3:
        box[12] = TrySavingData(SAVE_NORMAL);
        VarSet(VAR_LEGENDS_HOMECOMING_MEMORY, 0);
        VarSet(VAR_LEGENDS_BEDROOM_COLORS, 0);
        VarSet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR, 0);
        box[13] = LoadGameSave(SAVE_NORMAL);
        SetMainCallback2(CB2_Overworld); break;
    }
}
