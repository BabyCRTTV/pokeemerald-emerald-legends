// Private fixture. Apartment scripts run through normal field input in mGBA.
#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "main.h"
#include "money.h"
#include "new_game.h"
#include "main_menu.h"
#include "overworld.h"
#include "pokemon.h"
#include "save.h"
#include "script.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/species.h"
#include "legends_clock.h"
#include "legends_seasons.h"

extern struct ScriptContext gRentalQaScriptContext;

struct Scene
{
    u16 map;
    s16 x, y;
};

static const struct Scene sScenes[] =
{
    {MAP_LILYCOVE_CITY_COVE_LILY_MOTEL_1F, 6, 3},
    {MAP_LILYCOVE_CITY_COVE_LILY_MOTEL_2F, 6, 2},
    {MAP_MAUVILLE_CITY, 2, 8},
    {MAP_MAUVILLE_CITY_MAUVILLE_HILLS_LOBBY, 3, 6},
    {MAP_MAUVILLE_CITY_MAUVILLE_HILLS_LOBBY, 6, 2},
};

void qa(void)
{
    volatile u32 *mailbox = (u32 *)0x0203fd00;
    const struct Scene *scene = &sScenes[mailbox[1]];

    if (mailbox[0] == 0)
    {
        NewGameInitData();
        NewGameBirchSpeech_SetDefaultPlayerName(0);
        gSaveBlock2Ptr->optionsTextSpeed = OPTIONS_TEXT_SPEED_INSTANT;
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_SET_WALL_CLOCK);
        FlagSet(FLAG_SYS_POKEMON_GET);
        FlagClear(FLAG_LEGENDS_FOLLOWERS_DISABLED);
        LegendsClockSetManual(12, 0);
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
        LegendsSetPlaytimeSeason(0);
        CreateMonWithIVs(&gParties[B_TRAINER_PLAYER][0], SPECIES_MUDKIP, 12, 0, OTID_STRUCT_PLAYER_ID, 31);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        SetMoney(&gSaveBlock1Ptr->money, mailbox[2]);
    }
    if (mailbox[0] <= 1)
    {
        SetWarpDestination(MAP_GROUP(scene->map), MAP_NUM(scene->map), -1, scene->x, scene->y);
        WarpIntoMap();
        mailbox[4] = 1;
        SetMainCallback2(CB2_LoadMap);
        return;
    }

    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    if (mailbox[0] == 3)
        ObjectEventTurn(player, DIR_NORTH);
    if (mailbox[0] == 4)
    {
        mailbox[12] = TrySavingData(SAVE_NORMAL) == SAVE_STATUS_OK;
        mailbox[16] = offsetof(struct SaveBlock1, flags) + FLAG_RENTAL_COVE_LILY / 8;
        mailbox[17] = offsetof(struct SaveBlock1, pos);
    }
    if (mailbox[0] == 5)
    {
        u16 oneHp = 1;
        SetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_HP, &oneHp);
    }
    mailbox[5] = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    mailbox[6] = GetMoney(&gSaveBlock1Ptr->money);
    mailbox[7] = FlagGet(FLAG_RENTAL_COVE_LILY) | (FlagGet(FLAG_RENTAL_MAUVILLE_HILLS) << 1);
    mailbox[8] = gSaveBlock1Ptr->pos.x | (gSaveBlock1Ptr->pos.y << 16);
    mailbox[9] = ScriptContext_IsEnabled();
    mailbox[10] = gRentalQaScriptContext.data[0];
    mailbox[11] = GetFollowerObject() != NULL && !GetFollowerObject()->invisible;
    mailbox[13] = FlagGet(FLAG_RENTAL_COVE_LILY_DECOR) | (FlagGet(FLAG_RENTAL_MAUVILLE_HILLS_DECOR) << 1);
    mailbox[14] = GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_HP, NULL);
    mailbox[15] = MapGridGetMetatileIdAt(MAP_OFFSET + mailbox[2] % 16, MAP_OFFSET + mailbox[2] / 16 % 16);
    mailbox[4] = 1;
    SetMainCallback2((MainCallback)mailbox[3]);
}
