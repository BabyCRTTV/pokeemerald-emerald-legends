// Private scene setup and assertions. Never part of the public game binary.
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
#include "pokemon.h"
#include "script.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/species.h"

void qa(void)
{
    volatile u32 *b = (u32 *)0x0203ffc0;
    static const u16 maps[] = {MAP_LEGENDS_GROTTO_LEAFSHADE, MAP_LEGENDS_GROTTO_STILLWATER, MAP_LEGENDS_GROTTO_RAINROOT};
    if (b[0] == 0)
    {
        u16 map = maps[b[1]];
        NewGameInitData();
        gSaveBlock2Ptr->playerName[0] = 0xBB;
        gSaveBlock2Ptr->playerName[1] = 0xFF;
        gSaveBlock2Ptr->optionsTextSpeed = 2;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP); FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 4);
        VarSet(VAR_BIRCH_LAB_STATE, 5);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 25, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        LegendsClockSetManual(12, 0);
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
        LegendsSetPlaytimeSeason(b[2]);
        SetWarpDestination(MAP_GROUP(map), MAP_NUM(map), -1, 11, 11);
        WarpIntoMap(); b[4] = 1; SetMainCallback2(CB2_LoadMap); return;
    }
    if (b[0] == 1)
    {
        s16 x, y;
        u8 object;
        PlayerGetDestCoords(&x, &y);
        b[5] = gSaveBlock1Ptr->location.mapGroup;
        b[6] = gSaveBlock1Ptr->location.mapNum;
        b[7] = LegendsGetActiveSeason();
        b[8] = VarGet(VAR_OBJ_GFX_ID_F);
        b[9] = MapGridGetCollisionAt(x, y);
        b[10] = x - 7; b[11] = y - 7;
        b[12] = ScriptContext_IsEnabled();
        b[13] = 0;
        if (!TryGetObjectEventIdByLocalIdAndMap(1, b[6], b[5], &object))
            b[13] = gObjectEvents[object].graphicsId;
    }
    if (b[0] == 2)
    {
        // Start on the ordinary approach path. The host records real input
        // from here through the root interaction, choice, fade and entry.
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
        LegendsSetPlaytimeSeason(LEGENDS_SPRING);
        VarSet(VAR_REPEL_STEP_COUNT, 200);
        SetWarpDestination(MAP_GROUP(MAP_PETALBURG_WOODS), MAP_NUM(MAP_PETALBURG_WOODS), -1, 13, 35);
        WarpIntoMap(); b[4] = 1; SetMainCallback2(CB2_LoadMap); return;
    }
    b[4] = 1;
    gMain.callback2 = (MainCallback)b[3];
}
