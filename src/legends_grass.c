#include "global.h"
#include "legends_grass.h"
#include "legends_seasons.h"
#include "fieldmap.h"
#include "field_camera.h"
#include "tilesets.h"
#include "constants/metatile_labels.h"

EWRAM_DATA static u8 sCleared[(MAX_MAP_DATA_SIZE + 7) / 8] = {0};

void LegendsResetSnowGrass(void)
{
    memset(sCleared, 0, sizeof(sCleared));
}

static s32 SnowGrassIndex(s16 x, s16 y)
{
    s32 index;
    if (x < 0 || y < 0 || x >= gBackupMapLayout.width || y >= gBackupMapLayout.height)
        return -1;
    index = y * gBackupMapLayout.width + x;
    if (index >= MAX_MAP_DATA_SIZE || !LegendsMapHasSeasons()
     || LegendsGetActiveSeason() != LEGENDS_WINTER
     || gMapHeader.mapLayout->primaryTileset != &gTileset_General
     || MapGridGetMetatileIdAt(x, y) != METATILE_General_TallGrass)
        return -1;
    return index;
}

void LegendsStepSnowGrass(s16 x, s16 y)
{
    s32 index = SnowGrassIndex(x, y);
    if (index >= 0 && !(sCleared[index / 8] & (1 << (index & 7))))
    {
        sCleared[index / 8] |= 1 << (index & 7);
        CurrentMapDrawMetatileAt(x, y);
    }
}

bool32 LegendsSnowGrassCleared(s16 x, s16 y)
{
    s32 index = SnowGrassIndex(x, y);
    return index >= 0 && (sCleared[index / 8] & (1 << (index & 7)));
}
