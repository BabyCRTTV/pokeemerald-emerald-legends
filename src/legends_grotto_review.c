// Keep scripted grotto entrances out of the borrowed native Secret Base warp path.
#include "global.h"
#include "legends_grotto_review.h"
#include "constants/maps.h"

bool32 LegendsGrottoIsEntrance(s16 x, s16 y)
{
    u16 map = gSaveBlock1Ptr->location.mapNum | (gSaveBlock1Ptr->location.mapGroup << 8);
    // Borrowed native entrance art retains its Secret Base behavior. The four
    // explicitly scripted grotto cells must not enter a stale native base.
    switch (map)
    {
    case MAP_PETALBURG_WOODS: return y == 31 && (x == 12 || x == 13);
    case MAP_ROUTE114: return x == 13 && y == 40;
    case MAP_ROUTE119: return x == 27 && y == 105;
    default: return FALSE;
    }
}
