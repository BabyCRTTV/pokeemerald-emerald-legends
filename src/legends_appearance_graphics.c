#include "global.h"
#include "legends_appearance.h"
#include "sprite.h"
#include "constants/event_objects.h"

#include "data/legends/overworld_outfits.h"
#include "data/legends/overworld_accessories.h"
#include "data/legends/overworld_costumes.h"

static const u16 sBaseGraphicsIds[2][LEGENDS_APPEARANCE_STATES] =
{
    {OBJ_EVENT_GFX_BRENDAN_NORMAL, OBJ_EVENT_GFX_BRENDAN_MACH_BIKE,
     OBJ_EVENT_GFX_BRENDAN_ACRO_BIKE, OBJ_EVENT_GFX_BRENDAN_SURFING,
     OBJ_EVENT_GFX_BRENDAN_UNDERWATER, OBJ_EVENT_GFX_BRENDAN_FIELD_MOVE,
     OBJ_EVENT_GFX_BRENDAN_FISHING, OBJ_EVENT_GFX_BRENDAN_WATERING,
     OBJ_EVENT_GFX_BRENDAN_FIELD_MOVE},
    {OBJ_EVENT_GFX_MAY_NORMAL, OBJ_EVENT_GFX_MAY_MACH_BIKE,
     OBJ_EVENT_GFX_MAY_ACRO_BIKE, OBJ_EVENT_GFX_MAY_SURFING,
     OBJ_EVENT_GFX_MAY_UNDERWATER, OBJ_EVENT_GFX_MAY_FIELD_MOVE,
     OBJ_EVENT_GFX_MAY_FISHING, OBJ_EVENT_GFX_MAY_WATERING,
     OBJ_EVENT_GFX_MAY_FIELD_MOVE},
};

EWRAM_DATA static struct ObjectEventGraphicsInfo sGraphicsInfo[2][LEGENDS_APPEARANCE_STATES] = {0};

u16 LegendsGetPlayerGraphicsId(u8 state, enum Gender gender)
{
    if (state >= LEGENDS_APPEARANCE_STATES)
        state = 0;
    return OBJ_EVENT_GFX_LEGENDS_PLAYER_START
         + (gender == FEMALE ? LEGENDS_APPEARANCE_STATES : 0) + state;
}

u16 LegendsGetBasePlayerGraphicsId(u16 graphicsId)
{
    u16 index = graphicsId - OBJ_EVENT_GFX_LEGENDS_PLAYER_START;
    if (index >= 2 * LEGENDS_APPEARANCE_STATES)
        return graphicsId;
    return sBaseGraphicsIds[index / LEGENDS_APPEARANCE_STATES][index % LEGENDS_APPEARANCE_STATES];
}

const struct ObjectEventGraphicsInfo *LegendsGetPlayerGraphicsInfo(u16 graphicsId, const struct ObjectEventGraphicsInfo *base)
{
    u16 index = graphicsId - OBJ_EVENT_GFX_LEGENDS_PLAYER_START;
    u8 gender, state, outfit;
    struct ObjectEventGraphicsInfo *info;
    if (index >= 2 * LEGENDS_APPEARANCE_STATES)
        return base;
    gender = index / LEGENDS_APPEARANCE_STATES;
    state = index % LEGENDS_APPEARANCE_STATES;
    outfit = LegendsGetOutfit();
    LegendsUpdateAppearancePalettes();
    info = &sGraphicsInfo[gender][state];
    *info = *base;
    info->paletteTag = (state == 4 ? OBJ_EVENT_PAL_TAG_LEGENDS_UNDERWATER_MALE : OBJ_EVENT_PAL_TAG_LEGENDS_PLAYER_MALE) + gender;
    if (LegendsGetCostume() && state != 4)
        info->images = sLegendsCostumeImages[LegendsGetCostume()-1][gender][state == 8 ? 5 : state];
    else if (LegendsGetAccessoryStyle() && state != 4)
        info->images = sLegendsAccessoryImages[LegendsGetAccessoryStyle() - 1][gender][outfit][state == 8 ? 5 : state];
    else if (outfit && (!LegendsGetCostume() || state != 4))
        info->images = sLegendsOutfitImages[gender][outfit - 1][state == 8 ? 5 : state];
    info->images = LegendsFootwearImages(info->images, gender, state == 8 ? 5 : state);
    return info;
}
