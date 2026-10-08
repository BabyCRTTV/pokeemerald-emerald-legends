#ifndef GUARD_LEGENDS_STARTERS_H
#define GUARD_LEGENDS_STARTERS_H

#include "global.h"

struct Trainer;
struct TrainerMon;

// Saved as setting + 1; legacy zero defaults to the Emerald trio.
enum
{
    LEGENDS_STARTERS_GEN_1,
    LEGENDS_STARTERS_GEN_2,
    LEGENDS_STARTERS_GEN_3,
    LEGENDS_STARTERS_GEN_4,
    LEGENDS_STARTERS_GEN_5,
    LEGENDS_STARTERS_GEN_6,
    LEGENDS_STARTERS_GEN_7,
    LEGENDS_STARTERS_GEN_8,
    LEGENDS_STARTERS_GEN_9,
    LEGENDS_STARTERS_SPECIAL,
    LEGENDS_STARTERS_RANDOM,
    LEGENDS_STARTERS_COUNT
};

u8 LegendsGetStarterSetting(void);
void LegendsSetStarterSetting(u8 setting);
void LegendsPrepareStarters(void);
u16 LegendsGetStarterPokemon(u16 slot);
void LegendsCustomizeRivalMon(const struct Trainer *trainer, struct TrainerMon *mon);

#endif
