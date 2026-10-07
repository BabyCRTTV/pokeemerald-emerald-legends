#ifndef GUARD_LEGENDS_SETTINGS_H
#define GUARD_LEGENDS_SETTINGS_H

void LegendsInitNewGameSettings(void);
void LegendsEnsureSettingsInitialized(void);
void LegendsEnsureExpShareKeyItem(void);
void LegendsRestoreUnlocksOnContinue(void);
bool32 LegendsIsExpShareEnabled(void);
void LegendsSetExpShareEnabled(bool32 enabled);

#endif // GUARD_LEGENDS_SETTINGS_H
