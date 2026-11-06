#include "global.h"
#include "legends_nightmare.h"
#include "event_data.h"
#include "script.h"
#include "field_player_avatar.h"
#include "constants/flags.h"
#include "constants/map_types.h"
#include "constants/layouts.h"
#include "constants/maps.h"

extern const u8 Nightmare_UnknownCall[];
static EWRAM_DATA u8 sNightmareCallSteps;

bool32 LegendsNightmareIsShore(void)
{
    return gMapHeader.mapLayoutId == LAYOUT_LEGENDS_NIGHTMARE_SHORE;
}

// An older battery save may be standing in the formerly empty grass occupied
// by the new house's solid walls. Repair only that impossible position, before
// Continue restores actors; keep every other actor and all saved story state.
void LegendsNightmareRepairLegacyPosition(void)
{
    u32 i;
    if (gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_LILYCOVE_CITY)
     || gSaveBlock1Ptr->location.mapNum != MAP_NUM(MAP_LILYCOVE_CITY)
     || gSaveBlock1Ptr->pos.x < 49 || gSaveBlock1Ptr->pos.x > 52
     || gSaveBlock1Ptr->pos.y < 13 || gSaveBlock1Ptr->pos.y > 15)
        return;
    gSaveBlock1Ptr->pos.x = 50;
    gSaveBlock1Ptr->pos.y = 16;
    for (i = 0; i < OBJECT_EVENTS_COUNT; i++)
    {
        struct ObjectEvent *actor = &gSaveBlock1Ptr->objectEvents[i];
        if (!actor->isPlayer)
            continue;
        actor->initialCoords.x = actor->currentCoords.x = actor->previousCoords.x = 57;
        actor->initialCoords.y = actor->currentCoords.y = actor->previousCoords.y = 23;
        actor->currentElevation = actor->previousElevation = 3;
    }
}

// The shared CALMED flag covers capture or defeat, but never escape/blackout.
// Called only after higher-priority field events and the Wyrmtide call.
bool32 LegendsNightmareTryCall(void)
{
#if !IS_FRLG
    if (FlagGet(FLAG_LEGENDS_NIGHTMARE_CALL)
     || !FlagGet(FLAG_LEGENDS_WYRMTIDE_CALMED)
     || !FlagGet(FLAG_RECEIVED_POKENAV)
     || FlagGet(FLAG_SYS_SAFARI_MODE)
     || (gPlayerAvatar.flags & PLAYER_AVATAR_FLAG_FORCED_MOVE)
     || (gMapHeader.mapType != MAP_TYPE_ROUTE
      && gMapHeader.mapType != MAP_TYPE_TOWN
      && gMapHeader.mapType != MAP_TYPE_CITY))
    {
        sNightmareCallSteps = 0;
        return FALSE;
    }
    if (++sNightmareCallSteps < 8)
        return FALSE;
    sNightmareCallSteps = 0;
    ScriptContext_SetupScript(Nightmare_UnknownCall);
    return TRUE;
#else
    return FALSE;
#endif
}
