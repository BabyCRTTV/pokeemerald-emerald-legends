#include "global.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_effect.h"
#include "field_effect_helpers.h"
#include "field_player_avatar.h"
#include "fieldmap.h"
#include "metatile_behavior.h"
#include "overworld.h"
#include "random.h"
#include "pokemon.h"
#include "constants/field_effects.h"
#include "constants/legends_day_off.h"
#include "constants/maps.h"

static enum Direction FindSkippingWater(s16 *x, s16 *y)
{
    s16 playerX, playerY;
    PlayerGetDestCoords(&playerX, &playerY);

    for (enum Direction dir = DIR_SOUTH; dir <= DIR_EAST; dir++)
    {
        s16 waterX = playerX + gDirectionToVectors[dir].x;
        s16 waterY = playerY + gDirectionToVectors[dir].y;
        if (MetatileBehavior_IsSurfableWaterOrUnderwater(MapGridGetMetatileBehaviorAt(waterX, waterY)))
        {
            *x = waterX;
            *y = waterY;
            return dir;
        }
    }
    return DIR_NONE;
}

u16 LegendsDayOffGetSpot(void)
{
    s16 x, y;
    struct ObjectEvent *follower = GetFollowerObject();
    if (follower == NULL || follower->invisible || GetFirstLiveMon() == NULL
        || !(GetPlayerAvatarFlags() & PLAYER_AVATAR_FLAG_ON_FOOT))
        return DAY_OFF_NONE;

    u16 map = (gSaveBlock1Ptr->location.mapGroup << 8) | gSaveBlock1Ptr->location.mapNum;
    switch (map)
    {
    case MAP_ROUTE102:
    case MAP_DEWFORD_TOWN:
        if (FindSkippingWater(&x, &y) != DIR_NONE)
            return map == MAP_ROUTE102 ? DAY_OFF_POND : DAY_OFF_SHORE;
        break;
    case MAP_PETALBURG_WOODS:
        PlayerGetDestCoords(&x, &y);
        x -= MAP_OFFSET;
        y -= MAP_OFFSET;
        if (x >= 14 && x <= 22 && y >= 32 && y <= 37)
            return DAY_OFF_WOODS;
        break;
    case MAP_ROUTE113:
        PlayerGetDestCoords(&x, &y);
        x -= MAP_OFFSET;
        y -= MAP_OFFSET;
        if (x >= 30 && x <= 35 && y >= 6 && y <= 8)
            return DAY_OFF_WORKSHOP;
        break;
    }
    return DAY_OFF_NONE;
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
    s16 x, y;
    enum Direction direction = FindSkippingWater(&x, &y);
    if (direction == DIR_NONE)
        return;

    // The second skip stays in the first tile if the next tile is dry.
    if (gSpecialVar_0x8007 != 0)
    {
        s16 nextX = x + gDirectionToVectors[direction].x;
        s16 nextY = y + gDirectionToVectors[direction].y;
        if (MetatileBehavior_IsSurfableWaterOrUnderwater(MapGridGetMetatileBehaviorAt(nextX, nextY)))
        {
            x = nextX;
            y = nextY;
        }
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
