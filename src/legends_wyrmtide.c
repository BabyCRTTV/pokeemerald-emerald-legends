#include "global.h"
#include "legends_wyrmtide.h"
#include "event_data.h"
#include "script.h"
#include "pokemon.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "constants/maps.h"
#include "constants/map_event_ids.h"
#include "constants/species.h"
#include "constants/battle.h"
#include "constants/flags.h"
#include "constants/map_types.h"

extern const u8 Wyrmtide_UnknownCall[];
static EWRAM_DATA u8 sCallSteps;
// Called after higher-priority native step events, only during free movement.
bool32 LegendsWyrmtideTryCall(void)
{
#if !IS_FRLG
    if (FlagGet(FLAG_LEGENDS_WYRMTIDE_CALL))
    {
        LegendsWyrmtideRefreshDewford();
        sCallSteps = 0;
        return FALSE;
    }
    if (!FlagGet(FLAG_RECEIVED_POKENAV)
     || !FlagGet(FLAG_LEGENDS_STORY_WEATHER_REPORT)
     || !FlagGet(FLAG_LEGENDS_STORY_REGIGIGAS_CALMED)
     || FlagGet(FLAG_LEGENDS_WYRMTIDE_CALL)
     || FlagGet(FLAG_SYS_SAFARI_MODE)
     || (gMapHeader.mapType != MAP_TYPE_ROUTE
      && gMapHeader.mapType != MAP_TYPE_TOWN
      && gMapHeader.mapType != MAP_TYPE_CITY))
    {
        sCallSteps = 0;
        return FALSE;
    }
    if (++sCallSteps < 8) return FALSE;
    sCallSteps = 0;
    ScriptContext_SetupScript(Wyrmtide_UnknownCall);
    return TRUE;
#else
    return FALSE;
#endif
}

// Species must be present in the party; a boxed Pokemon or unhatched egg is not
// a companion at the seal. A fainted companion still satisfies the inscription.
bool32 LegendsWyrmtideHasMaker(void)
{
    u32 i;
    for (i = 0; i < CalculatePlayerPartyCount(); i++)
        if (!GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_IS_EGG)
         && GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES) == SPECIES_REGIGIGAS)
            return TRUE;
    return FALSE;
}

static void SpawnExpeditionObject(u8 localId, u16 nativeHideFlag, u16 localHideFlag)
{
    u32 i;
    s16 x, y;
    u8 object;
    PlayerGetDestCoords(&x, &y);
    for (i = 0; i < gMapHeader.events->objectEventCount; i++)
    {
        const struct ObjectEventTemplate *t = &gMapHeader.events->objectEvents[i];
        if (t->localId != localId) continue;
        // Continue may contain the older, shorter Dewford template list. Copy
        // only these appended entries; retain all native NPC permanent moves.
        gSaveBlock1Ptr->objectEventTemplates[i] = *t;
        if (FlagGet(nativeHideFlag) && (x != t->x + 7 || y != t->y + 7))
        {
            FlagClear(localHideFlag);
            if (TryGetObjectEventIdByLocalIdAndMap(localId, MAP_NUM(MAP_DEWFORD_TOWN), MAP_GROUP(MAP_DEWFORD_TOWN), &object))
                TrySpawnObjectEvent(localId, MAP_NUM(MAP_DEWFORD_TOWN), MAP_GROUP(MAP_DEWFORD_TOWN));
        }
        return;
    }
}
void LegendsWyrmtideRefreshDewford(void)
{
#if !IS_FRLG
    if (!FlagGet(FLAG_LEGENDS_WYRMTIDE_CALL)
     || gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_DEWFORD_TOWN)
     || gSaveBlock1Ptr->location.mapNum != MAP_NUM(MAP_DEWFORD_TOWN)) return;
    SpawnExpeditionObject(LOCALID_WYRMTIDE_BRINEY, FLAG_HIDE_MR_BRINEY_DEWFORD_TOWN, FLAG_TEMP_6);
    SpawnExpeditionObject(LOCALID_WYRMTIDE_BOAT, FLAG_HIDE_MR_BRINEY_BOAT_DEWFORD_TOWN, FLAG_TEMP_7);
#endif
}
