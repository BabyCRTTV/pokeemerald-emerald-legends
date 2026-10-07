#include "global.h"
#include "legends_settings.h"
#include "event_data.h"
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

void LegendsSetExpShareEnabled(bool32 enabled)
{
    if (enabled)
        FlagSet(FLAG_LEGENDS_EXP_SHARE);
    else
        FlagClear(FLAG_LEGENDS_EXP_SHARE);

    FlagSet(FLAG_LEGENDS_SETTINGS_INITIALIZED);
}
