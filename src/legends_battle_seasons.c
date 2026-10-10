#include "global.h"
#include "battle.h"
#include "legends_battle_seasons.h"
#include "legends_seasons.h"
#include "palette.h"

void LegendsLoadBattleSeasonPalette(u16 environment, const u16 *source)
{
    u16 colors[3 * 16];
    u32 i;
    u8 season;
    if ((environment != BATTLE_ENVIRONMENT_GRASS
      && environment != BATTLE_ENVIRONMENT_LONG_GRASS
      && environment != BATTLE_ENVIRONMENT_PLAIN)
     || !LegendsMapHasSeasons()
     || (gBattleTypeFlags & (BATTLE_TYPE_LINK | BATTLE_TYPE_RECORDED | BATTLE_TYPE_RECORDED_LINK | BATTLE_TYPE_FRONTIER
                          | BATTLE_TYPE_EREADER_TRAINER | BATTLE_TYPE_TRAINER_HILL | BATTLE_TYPE_LEGENDARY)))
    {
        LoadPalette(source, BG_PLTT_ID(2), sizeof(colors));
        return;
    }
    // Start from the native palette on every load/animation restore. Reuse the
    // visible overworld season; a pending calendar change cannot split the scene.
    memcpy(colors, source, sizeof(colors));
    season = LegendsGetActiveSeason();
    for (i = 0; i < ARRAY_COUNT(colors); i++)
        if ((i & 15) != 0)
            colors[i] = LegendsSeasonVegetationColor(colors[i], season);
    // Native loading updates both unfaded/faded buffers. Pokemon, portraits,
    // healthboxes and battle text use separate palette slots.
    LoadPalette(colors, BG_PLTT_ID(2), sizeof(colors));
}
