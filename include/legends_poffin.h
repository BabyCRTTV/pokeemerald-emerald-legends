#ifndef GUARD_LEGENDS_POFFIN_H
#define GUARD_LEGENDS_POFFIN_H

void LegendsPoffinInit(bool32 newGame);
s16 LegendsPoffinFreeSlot(void);
bool32 LegendsPoffinStore(const struct Pokeblock *treat);
void LegendsShowTreatCase(void (*callback)(void));
void LegendsPreparePoffinFeed(struct Pokeblock *treat);
void ItemUseOutOfBattle_TreatCase(u8 taskId);

#endif
