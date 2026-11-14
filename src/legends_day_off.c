#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_effect.h"
#include "field_effect_helpers.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "legends_day_off.h"
#include "metatile_behavior.h"
#include "overworld.h"
#include "random.h"
#include "pokemon.h"
#include "constants/field_effects.h"
#include "constants/legends_day_off.h"
#include "constants/maps.h"

extern const u8 LegendsDayOff_PondProp[];
extern const u8 LegendsDayOff_ShoreProp[];
extern const u8 LegendsDayOff_WoodsProp[];
extern const u8 LegendsDayOff_WorkshopProp[];

// A Continue on an earlier save already has this map's old object templates.
// Seed only the new prop's empty slot, leaving moved objects and flags intact.
void LegendsDayOffRestoreProp(void)
{
    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    const u8 *script;
    switch (map)
    {
    case MAP_ROUTE102:
        script = LegendsDayOff_PondProp;
        break;
    case MAP_DEWFORD_TOWN:
        script = LegendsDayOff_ShoreProp;
        break;
    case MAP_PETALBURG_WOODS:
        script = LegendsDayOff_WoodsProp;
        break;
    case MAP_ROUTE113:
        script = LegendsDayOff_WorkshopProp;
        break;
    default:
        return;
    }

    for (u32 i = 0; i < gMapHeader.events->objectEventCount; i++)
    {
        const struct ObjectEventTemplate *prop = &gMapHeader.events->objectEvents[i];
        if (prop->script == script && gSaveBlock1Ptr->objectEventTemplates[i].localId == 0)
        {
            gSaveBlock1Ptr->objectEventTemplates[i] = *prop;
            break;
        }
    }
}

u16 LegendsDayOffHasFollower(void)
{
    const struct ObjectEvent *follower = GetFollowerObject();
    return (GetPlayerAvatarFlags() & PLAYER_AVATAR_FLAG_ON_FOOT)
        && follower != NULL && !follower->invisible && GetFirstLiveMon() != NULL;
}

u16 LegendsDayOffGetReaction(void)
{
    struct Pokemon *mon = GetFirstLiveMon();
    if (mon == NULL)
        return DAY_OFF_KEEN;

    u8 nature = GetNature(mon);
    enum Species species = GetMonData(mon, MON_DATA_SPECIES);

    if (nature == NATURE_TIMID || nature == NATURE_BASHFUL)
        return DAY_OFF_SHY;
    if (GetSpeciesType(species, 0) == TYPE_WATER || GetSpeciesType(species, 1) == TYPE_WATER)
        return DAY_OFF_WATER;
    if (GetSpeciesType(species, 0) == TYPE_FIRE || GetSpeciesType(species, 1) == TYPE_FIRE)
        return DAY_OFF_FIRE;
    if (GetSpeciesType(species, 0) == TYPE_GRASS || GetSpeciesType(species, 1) == TYPE_GRASS)
        return DAY_OFF_GRASS;
    return DAY_OFF_KEEN;
}

void LegendsDayOffSkipStone(void)
{
    const struct ObjectEvent *stones = &gObjectEvents[gSelectedObjectEvent];
    enum Direction direction = gSpecialVar_0x8004 == DAY_OFF_POND ? DIR_NORTH : DIR_EAST;
    s16 dx = gDirectionToVectors[direction].x;
    s16 dy = gDirectionToVectors[direction].y;
    s16 x = stones->currentCoords.x + dx;
    s16 y = stones->currentCoords.y + dy;

    if (gSpecialVar_0x8007 != 0
        && MetatileBehavior_IsSurfableWaterOrUnderwater(MapGridGetMetatileBehaviorAt(x + dx, y + dy)))
    {
        x += dx;
        y += dy;
    }
    gFieldEffectArguments[0] = x;
    gFieldEffectArguments[1] = y;
    gFieldEffectArguments[2] = MapGridGetElevationAt(x, y);
    gFieldEffectArguments[3] = 1;
    FieldEffectStart(FLDEFF_JUMP_SMALL_SPLASH);
}

void LegendsDayOffWashEffect(void)
{
    struct ObjectEvent *follower = GetFollowerObject();
    if (follower == NULL)
        return;

    // Lift the native bubbles from the follower's tile.
    gFieldEffectArguments[0] = follower->currentCoords.x;
    gFieldEffectArguments[1] = follower->currentCoords.y;
    FieldEffectStart(FLDEFF_BUBBLES);
}

void LegendsDayOffHeart(void)
{
    struct ObjectEvent *follower = GetFollowerObject();
    if (follower != NULL)
        StartFieldEffectForObjectEvent(FLDEFF_HEART_ICON, follower);
}

u16 LegendsDayOffPickHidingPlace(void)
{
    return Random() & 1;
}

void LegendsDayOffSplashBack(void)
{
    struct ObjectEvent *follower = GetFollowerObject();
    if (follower != NULL)
        StartFieldEffectForObjectEvent(FLDEFF_SPLASH, follower);
}
