#include "global.h"
#include "legends_settings.h"
#include "event_data.h"
#include "item.h"
#include "battle_pyramid.h"
#include "constants/items.h"
#include "constants/battle_frontier.h"
#include "constants/flags.h"

void LegendsInitNewGameSettings(void)
{
    FlagSet(FLAG_LEGENDS_EXP_SHARE);
    FlagSet(FLAG_LEGENDS_SETTINGS_INITIALIZED);
}

void LegendsEnsureSettingsInitialized(void)
{
    if (!FlagGet(FLAG_LEGENDS_SETTINGS_INITIALIZED))
        LegendsInitNewGameSettings();
}

bool32 LegendsIsExpShareEnabled(void)
{
    LegendsEnsureSettingsInitialized();
    return FlagGet(FLAG_LEGENDS_EXP_SHARE);
}

// The physical Key Item and Options menu both use FLAG_LEGENDS_EXP_SHARE.
void LegendsEnsureExpShareKeyItem(void)
{
    if (!CheckBagHasItem(ITEM_EXP_SHARE, 1))
        AddBagItem(ITEM_EXP_SHARE, 1);
}

void LegendsRestoreUnlocksOnContinue(void)
{
    LegendsEnsureSettingsInitialized();

    // Existing saves that already own a Pokédex should receive DexNav.
    if (FlagGet(FLAG_SYS_POKEDEX_GET))
    {
        FlagSet(FLAG_LEGENDS_DEXNAV_UNLOCKED);
        FlagSet(FLAG_LEGENDS_DEXNAV_DETECTOR_MODE);
    }

    // Do not put a permanent Key Item into the temporary Battle Pyramid Bag.
    // A full Key Items pocket can be retried on a later regular continue.
    if (CurrentBattlePyramidLocation() == PYRAMID_LOCATION_NONE
     && !FlagGet(FLAG_STORING_ITEMS_IN_PYRAMID_BAG))
        LegendsEnsureExpShareKeyItem();
}

void LegendsSetExpShareEnabled(bool32 enabled)
{
    if (enabled)
        FlagSet(FLAG_LEGENDS_EXP_SHARE);
    else
        FlagClear(FLAG_LEGENDS_EXP_SHARE);

    FlagSet(FLAG_LEGENDS_SETTINGS_INITIALIZED);
}
