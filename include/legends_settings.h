#ifndef GUARD_LEGENDS_SETTINGS_H
#define GUARD_LEGENDS_SETTINGS_H

void LegendsInitNewGameSettings(void);
void LegendsEnsureSettingsInitialized(void);
void LegendsEnsureExpShareKeyItem(void);
void LegendsRestoreUnlocksOnContinue(void);
bool32 LegendsIsExpShareEnabled(void);
void LegendsSetExpShareEnabled(bool32 enabled);

// A saved wild encounter base rate. New and existing saves default to 1/8192.
enum
{
    LEGENDS_SHINY_RATE_8192,
    LEGENDS_SHINY_RATE_5680,
    LEGENDS_SHINY_RATE_1226,
    LEGENDS_SHINY_RATE_COUNT
};

u8 LegendsGetShinyRateSetting(void);
void LegendsSetShinyRateSetting(u8 setting);
u16 LegendsGetWildShinyRateDenominator(void);

#endif // GUARD_LEGENDS_SETTINGS_H
