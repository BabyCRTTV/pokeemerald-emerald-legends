// Private scene setup and assertions. Never part of the public game binary.
#include "global.h"
#include "field_camera.h"
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
#include "constants/items.h"
#include "constants/moves.h"
#include "constants/battle.h"
#include "save.h"
#include "item.h"
#include "legends_grottos.h"
#include "battle.h"
static u32 Hash(const void *ptr, u32 size) { const u8 *p=ptr;u32 v=2166136261u;while(size--)v=(v^*p++)*16777619u;return v; }
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
        gSaveBlock2Ptr->optionsBattleSceneOff = TRUE;
        for (u32 i=FLAG_BADGE01_GET;i<=FLAG_BADGE08_GET;i++) FlagSet(i);
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP); FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 4);
        VarSet(VAR_BIRCH_LAB_STATE, 5);
        CreateMonWithIVs(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 100, 32, OTID_STRUCT_PLAYER_ID, 31);
        SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0], MOVE_AERIAL_ACE, 0);
        for (u32 i=1;i<4;i++) SetMonMoveSlot(&gParties[B_TRAINER_PLAYER][0], MOVE_NONE, i);
        u16 stone=ITEM_EVERSTONE;SetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_HELD_ITEM, &stone);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        AddBagItem(ITEM_MASTER_BALL, 5); AddBagItem(ITEM_ORAN_BERRY, 11);
        LegendsClockSetManual(12, 0);
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
        LegendsSetPlaytimeSeason(b[2]);
        SetWarpDestination(MAP_GROUP(map), MAP_NUM(map), -1, 9, 9);
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
        u32 old; s16 x,y; PlayerGetDestCoords(&x,&y);
        struct BoxPokemon mon = gParties[B_TRAINER_PLAYER][0].box;
        // Synthetic pre-grotto unused tail: real flash transaction and native loader.
        memset(&gSaveBlock3Ptr->grottos, 0xA5, sizeof(gSaveBlock3Ptr->grottos));
        b[5] = TrySavingData(SAVE_NORMAL);
        old = Hash(gSaveBlock3Ptr, 716);
        memset(gSaveBlock3Ptr, 0, sizeof(*gSaveBlock3Ptr));
        b[6] = LoadGameSave(SAVE_NORMAL);
        LegendsGrottoInit(FALSE);
        b[7] = Hash(gSaveBlock3Ptr, 716) == old;
        b[8] = Hash(&mon, sizeof(mon)) == Hash(&gParties[B_TRAINER_PLAYER][0].box, sizeof(mon));
        b[9] = CheckBagHasItem(ITEM_ORAN_BERRY, 11) && LegendsGetSeason() == LEGENDS_SPRING;
        b[10] = gSaveBlock3Ptr->grottos.rooms[0].state == LEGENDS_GROTTO_READY;
        SetWarpDestination(gSaveBlock1Ptr->location.mapGroup,gSaveBlock1Ptr->location.mapNum,-1,x-7,y-7);
        WarpIntoMap();b[4]=1;SetMainCallback2(CB2_LoadMap);return;
    }
    if (b[0] == 3)
    {
        s16 x,y; PlayerGetDestCoords(&x,&y);
        u32 before = Hash(&gSaveBlock3Ptr->grottos, sizeof(gSaveBlock3Ptr->grottos));
        b[5] = TrySavingData(SAVE_NORMAL);
        memset(&gSaveBlock3Ptr->grottos, 0xA5, sizeof(gSaveBlock3Ptr->grottos));
        b[6] = LoadGameSave(SAVE_NORMAL); LegendsGrottoInit(FALSE);
        b[7] = before == Hash(&gSaveBlock3Ptr->grottos, sizeof(gSaveBlock3Ptr->grottos));
        SetWarpDestination(gSaveBlock1Ptr->location.mapGroup,gSaveBlock1Ptr->location.mapNum,-1,x-7,y-7);
        WarpIntoMap();b[4]=1;SetMainCallback2(CB2_LoadMap);return;
    }
    if (b[0] == 4)
    {
        b[5] = gSaveBlock3Ptr->grottos.rooms[0].state;
        b[6] = LegendsGrottoRemainingSteps(0);
        b[7] = Hash(&gSaveBlock3Ptr->grottos.rooms[0].mon, 80);
        b[8] = gBattleOutcome;
        b[9] = gMain.inBattle;
        b[10] = ScriptContext_IsEnabled();
        b[11] = gPartiesCount[B_TRAINER_PLAYER];
        b[12] = FlagGet(FLAG_TEMP_5);
        b[13] = GetMonData(&gParties[B_TRAINER_PLAYER][1], MON_DATA_SPECIES);
        b[14] = GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_PP1);
        b[15] = (u32)gBattleMainFunc;
    }
    if (b[0] == 5)
    {
        for (u32 i=0;i<b[1];i++) LegendsGrottoStep();
        b[5] = gSaveBlock3Ptr->grottos.rooms[0].state;
        b[6] = LegendsGrottoRemainingSteps(0);
    }
    b[4] = 1; gMain.callback2 = (MainCallback)b[3];
}
