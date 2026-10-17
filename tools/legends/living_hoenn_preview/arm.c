// PRIVATE mGBA QA instrumentation. Never linked into the public Legends ROM.
// Uses the real native maps, event scripts, story flags and text engine.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "script.h"
#include "field_player_avatar.h"
#include "string_util.h"
#include "legends_seasons.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/legends_field_requests.h"

extern const u8 LegendsFieldRequests_Talk[];
extern const u8 RustboroCity_DevonCorp_3F_EventScript_MrStone[];
extern const u8 Route119_WeatherInstitute_1F_EventScript_InstituteWorker2[];
extern const u8 LittlerootTown_EventScript_FatMan[];

void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    u32 scene = box[1];
    if (box[0] == 0)
    {
        NewGameInitData();
        StringCopy(gSaveBlock2Ptr->playerName, COMPOUND_STRING("LEGENDS"));
        gSaveBlock2Ptr->optionsTextSpeed = 2;
        FlagSet(FLAG_SYS_POKEMON_GET);
        FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_SET_WALL_CLOCK);
        FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9);
        VarSet(VAR_BIRCH_LAB_STATE, 5);
        VarSet(VAR_DEVON_CORP_3F_STATE, 1);
        VarSet(VAR_WEATHER_INSTITUTE_STATE, 1);
        VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, 0xB800); // authenticated 30-request layout.
        VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
        if (scene == 0)
        {
            VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, 0x0007); // 3 completed Birch requests
            SetWarpDestination(MAP_GROUP(MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB),
                MAP_NUM(MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB), -1, 6, 7);
        }
        else if (scene == 1)
        {
            VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH, 0x00FC); // first 6 Devon contracts
            FlagSet(FLAG_RECEIVED_EXP_SHARE); // keep native post-gift priority intact
            SetWarpDestination(MAP_GROUP(MAP_RUSTBORO_CITY_DEVON_CORP_3F),
                MAP_NUM(MAP_RUSTBORO_CITY_DEVON_CORP_3F), -1, 17, 7);
        }
        else if (scene == 2)
        {
            LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
            LegendsSetPlaytimeSeason(LEGENDS_WINTER);
            SetWarpDestination(MAP_GROUP(MAP_ROUTE119_WEATHER_INSTITUTE_1F),
                MAP_NUM(MAP_ROUTE119_WEATHER_INSTITUTE_1F), -1, 5, 6);
        }
        else
        {
            FlagSet(FLAG_SYS_GAME_CLEAR);
            ClearTempFieldEventData();
            FlagClear(FLAG_HIDE_LITTLEROOT_TOWN_FAT_MAN);
            SetWarpDestination(MAP_GROUP(MAP_LITTLEROOT_TOWN),
                MAP_NUM(MAP_LITTLEROOT_TOWN), -1, 11, 13);
        }
        WarpIntoMap();
        box[30] = 1;
        SetMainCallback2(CB2_LoadMap);
        return;
    }
    else if (box[0] == 1)
    {
        if (scene == 0) ScriptContext_SetupScript(LegendsFieldRequests_Talk);
        else if (scene == 1) ScriptContext_SetupScript(RustboroCity_DevonCorp_3F_EventScript_MrStone);
        else if (scene == 2) ScriptContext_SetupScript(Route119_WeatherInstitute_1F_EventScript_InstituteWorker2);
        else ScriptContext_SetupScript(LittlerootTown_EventScript_FatMan);
        box[30] = 1;
    }
    gMain.callback2 = (MainCallback)box[31];
}
