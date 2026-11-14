// Private setup and read-only queries. Gameplay is driven by mGBA buttons.
#include "global.h"
#include "battle.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "pokemon.h"
#include "script.h"
#include "save.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/species.h"
#include "legends_clock.h"
#include "legends_seasons.h"

extern struct ScriptContext gDayOffQaScriptContext;

struct Scene
{
    u16 map, species;
    s16 x, y;
    u8 nature, facing;
    bool8 followersOff;
};

static const struct Scene sScenes[] =
{
    {MAP_ROUTE102, SPECIES_MUDKIP, 40, 7, NATURE_JOLLY, DIR_EAST, FALSE},
    {MAP_DEWFORD_TOWN, SPECIES_MUDKIP, 9, 2, NATURE_TIMID, DIR_EAST, FALSE},
    {MAP_PETALBURG_WOODS, SPECIES_SHROOMISH, 18, 32, NATURE_JOLLY, DIR_EAST, FALSE},
    {MAP_ROUTE113, SPECIES_TORCHIC, 31, 6, NATURE_JOLLY, DIR_EAST, FALSE},
    {MAP_ROUTE113, SPECIES_MUDKIP, 31, 6, NATURE_JOLLY, DIR_EAST, FALSE},
    {MAP_ROUTE102, SPECIES_TREECKO, 40, 7, NATURE_JOLLY, DIR_WEST, FALSE},
    {MAP_ROUTE102, SPECIES_MUDKIP, 40, 7, NATURE_JOLLY, DIR_EAST, TRUE},
    {MAP_ROUTE102, SPECIES_MUDKIP, 41, 8, NATURE_JOLLY, DIR_NORTH, FALSE},
};

void qa(void)
{
    volatile u32 *mailbox = (u32 *)0x0203fd00;
    if (mailbox[0] == 0)
    {
        const struct Scene *scene = &sScenes[mailbox[1]];
        NewGameInitData();
        gSaveBlock2Ptr->optionsTextSpeed = OPTIONS_TEXT_SPEED_INSTANT;
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        if (scene->followersOff)
            FlagSet(FLAG_LEGENDS_FOLLOWERS_DISABLED);
        else
            FlagClear(FLAG_LEGENDS_FOLLOWERS_DISABLED);
        FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_SET_WALL_CLOCK);
        FlagSet(FLAG_SYS_POKEMON_GET);
        LegendsClockSetManual(12, 0);
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
        LegendsSetPlaytimeSeason(0);
        SetWarpDestination(MAP_GROUP(scene->map), MAP_NUM(scene->map), -1, scene->x, scene->y);
        WarpIntoMap();
        CreateMonWithIVs(&gParties[B_TRAINER_PLAYER][0], scene->species, 12, (0x12340000 / NUM_NATURES) * NUM_NATURES + scene->nature, OTID_STRUCT_PLAYER_ID, 31);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        mailbox[4] = 1;
        SetMainCallback2(CB2_LoadMap);
        return;
    }

    struct ObjectEvent *player = &gObjectEvents[gPlayerAvatar.objectEventId];
    struct ObjectEvent *follower = GetFollowerObject();
    if (mailbox[0] == 1)
    {
        if (follower != NULL)
        {
            MoveObjectEventToMapCoords(follower, player->currentCoords.x - 1, player->currentCoords.y);
            follower->invisible = FALSE;
            ObjectEventTurn(follower, DIR_EAST);
        }
        ObjectEventTurn(player, sScenes[mailbox[1]].facing);
    }
    if (mailbox[0] == 3)
    {
        // Model an older battery saved on the activity map. Preserve a sentinel
        // edit to a pre-existing NPC to check that Continue only adds the prop.
        struct ObjectEventTemplate *templates = gSaveBlock1Ptr->objectEventTemplates;
        u32 index = gMapHeader.events->objectEventCount - 1;
        struct ObjectEventTemplate original = templates[index];
        s16 originalX = templates[0].x;
        templates[0].x++;
        templates[index] = (struct ObjectEventTemplate){0};
        mailbox[13] = TrySavingData(SAVE_NORMAL) == SAVE_STATUS_OK;
        mailbox[14] = offsetof(struct SaveBlock1, objectEventTemplates);
        templates[index] = original;
        templates[0].x = originalX;
    }
    mailbox[5] = follower != NULL && !follower->invisible;
    mailbox[6] = ScriptContext_IsEnabled();
    mailbox[7] = gSpecialVar_0x8004;
    mailbox[8] = gSpecialVar_0x8005;
    mailbox[9] = gSpecialVar_0x8006;
    mailbox[10] = GetPlayerFacingDirection();
    mailbox[11] = follower != NULL && follower->currentCoords.x == player->currentCoords.x - 1
               && follower->currentCoords.y == player->currentCoords.y;
    mailbox[12] = gDayOffQaScriptContext.data[0];
    mailbox[4] = 1;
    SetMainCallback2((MainCallback)mailbox[3]);
}
