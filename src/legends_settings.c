#include "global.h"
#include "legends_da_bug.h"
#include "legends_settings.h"
#include "legends_starters.h"
#include "legends_seasons.h"
#include "event_data.h"
#include "item.h"
#include "battle_pyramid.h"
#include "constants/items.h"
#include "constants/battle_frontier.h"
#include "constants/flags.h"
#include "constants/vars.h"

// Title-screen choices must survive the new save's flags/vars reset. Keep this
// outside the SaveBlocks, consume it once, and clear it on a fresh title entry.
struct LegendsTitleOptions
{
    bool8 valid;
    bool8 expShareEnabled;
    bool8 followersEnabled;
    u8 shinyRate;
    u8 starterSetting;
    u8 seasonMode;
    u8 playtimeSeason;
};

EWRAM_DATA static struct LegendsTitleOptions sTitleOptions = {0};

void LegendsClearTitleOptions(void)
{
    sTitleOptions.valid = FALSE;
}

void LegendsStageTitleOptions(void)
{
    sTitleOptions.expShareEnabled = LegendsIsExpShareEnabled();
    sTitleOptions.followersEnabled = LegendsAreFollowersEnabled();
    sTitleOptions.starterSetting = LegendsGetStarterSetting();
    sTitleOptions.shinyRate = LegendsGetShinyRateSetting();
    sTitleOptions.seasonMode = LegendsGetSeasonMode();
    sTitleOptions.playtimeSeason = LegendsGetSeasonForMode(LEGENDS_SEASONS_PLAYTIME);
    sTitleOptions.valid = TRUE;
}

void LegendsApplyTitleOptionsToNewGame(void)
{
    if (sTitleOptions.valid)
    {
        LegendsSetExpShareEnabled(sTitleOptions.expShareEnabled);
        LegendsSetFollowersEnabled(sTitleOptions.followersEnabled);
        LegendsSetShinyRateSetting(sTitleOptions.shinyRate);
        LegendsSetStarterSetting(sTitleOptions.starterSetting);
        LegendsSetSeasonMode(sTitleOptions.seasonMode);
        LegendsSetPlaytimeSeason(sTitleOptions.playtimeSeason);
        LegendsClearTitleOptions();
    }
    // Initialize the visible environment before the truck/first outdoor load.
    LegendsCommitSeasonTransition();
}

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
    LegendsEnsureDaBugGift();
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

// Inverted flag gives older and new saves ON without a save migration/reset.
bool32 LegendsAreFollowersEnabled(void)
{
    return !FlagGet(FLAG_LEGENDS_FOLLOWERS_DISABLED);
}

void LegendsSetFollowersEnabled(bool32 enabled)
{
    if (enabled)
        FlagClear(FLAG_LEGENDS_FOLLOWERS_DISABLED);
    else
        FlagSet(FLAG_LEGENDS_FOLLOWERS_DISABLED);
    // The native field reload updates/removes the follower on leaving Options.
}

u8 LegendsGetShinyRateSetting(void)
{
    u16 setting = VarGet(VAR_LEGENDS_SHINY_RATE);

    if (setting >= LEGENDS_SHINY_RATE_COUNT)
        return LEGENDS_SHINY_RATE_8192;

    return setting;
}

void LegendsSetShinyRateSetting(u8 setting)
{
    if (setting >= LEGENDS_SHINY_RATE_COUNT)
        setting = LEGENDS_SHINY_RATE_8192;

    VarSet(VAR_LEGENDS_SHINY_RATE, setting);
}

u16 LegendsGetWildShinyRateDenominator(void)
{
    switch (LegendsGetShinyRateSetting())
    {
    case LEGENDS_SHINY_RATE_5680:
        return 5680;
    case LEGENDS_SHINY_RATE_1226:
        return 1226;
    case LEGENDS_SHINY_RATE_8192:
    default:
        return 8192;
    }
}
