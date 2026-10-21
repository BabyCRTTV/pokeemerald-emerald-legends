// Review prototype only. No captures, rewards, claims or cooldown state yet.
#include "global.h"
#include "event_data.h"
#include "legends_seasons.h"
#include "legends_grotto_review.h"
#include "pokemon.h"
#include "string_util.h"
#include "constants/event_objects.h"
#include "constants/maps.h"
#include "constants/species.h"
#include "constants/vars.h"

void LegendsGrottoPrepareVisitor(void)
{
    static const u16 visitors[3][LEGENDS_SEASON_COUNT] =
    {
        {SPECIES_BUNEARY, SPECIES_FOMANTIS, SPECIES_SHROOMISH, SPECIES_MINCCINO},
        {SPECIES_MARILL, SPECIES_BARBOACH, SPECIES_WOOPER, SPECIES_SNORUNT},
        {SPECIES_MORELULL, SPECIES_TROPIUS, SPECIES_GOOMY, SPECIES_SWABLU},
    };
    u8 room, season = LegendsGetActiveSeason();
    u16 species;
    if (gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_LEGENDS_GROTTO_LEAFSHADE))
        return;
    switch (gSaveBlock1Ptr->location.mapNum)
    {
    case MAP_NUM(MAP_LEGENDS_GROTTO_LEAFSHADE): room = 0; break;
    case MAP_NUM(MAP_LEGENDS_GROTTO_STILLWATER): room = 1; break;
    case MAP_NUM(MAP_LEGENDS_GROTTO_RAINROOT): room = 2; break;
    default: return;
    }
    species = visitors[room][season < LEGENDS_SEASON_COUNT ? season : LEGENDS_SPRING];
    VarSet(VAR_OBJ_GFX_ID_F, species + OBJ_EVENT_MON);
    gSpecialVar_0x8004 = species;
    StringCopy(gStringVar1, GetSpeciesName(species));
}

bool32 LegendsGrottoIsEntrance(s16 x, s16 y)
{
    u16 map = gSaveBlock1Ptr->location.mapNum | (gSaveBlock1Ptr->location.mapGroup << 8);
    // Borrowed native entrance art retains its Secret Base behavior. The four
    // explicitly scripted grotto cells must not enter a stale native base.
    switch (map)
    {
    case MAP_PETALBURG_WOODS: return y == 31 && (x == 12 || x == 13);
    case MAP_ROUTE114: return x == 14 && y == 40;
    case MAP_ROUTE119: return x == 27 && y == 105;
    default: return FALSE;
    }
}
