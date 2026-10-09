#ifndef GUARD_LEGENDS_APPEARANCE_H
#define GUARD_LEGENDS_APPEARANCE_H

#include "global.h"
#include "constants/trainers.h"

#define LEGENDS_SKIN_TONE_COUNT 5
#define LEGENDS_OUTFIT_COUNT 5
#define LEGENDS_SCARF_COUNT 6
#define LEGENDS_COSTUME_COUNT 3
#define LEGENDS_APPEARANCE_STATES 9

extern u16 gLegendsOverworldPalettes[2][16];
extern u16 gLegendsTrainerPalettes[2][16];
extern u16 gLegendsUnderwaterPalettes[2][16];

void LegendsBeginAppearanceSelection(void);
void LegendsClearAppearanceSelection(void);
void LegendsSetAppearanceSelection(u8 skin, u8 outfit);
void LegendsApplyAppearanceToNewGame(void);
void LegendsBeginWardrobeSelection(void);
void LegendsSetAccessorySelection(u8 scarf, bool8 jacket);
void LegendsApplyWardrobeSelection(void);
u8 LegendsGetCostume(void);
void LegendsSetCostumeSelection(u8 costume);
u8 LegendsGetScarf(void);
bool8 LegendsGetJacket(void);
u8 LegendsGetAccessoryStyle(void);
u8 LegendsGetSkinTone(void);
u8 LegendsGetOutfit(void);
void LegendsUpdateAppearancePalettes(void);
u16 LegendsGetPlayerGraphicsId(u8 state, enum Gender gender);
u16 LegendsGetBasePlayerGraphicsId(u16 graphicsId);
const struct ObjectEventGraphicsInfo *LegendsGetPlayerGraphicsInfo(u16 graphicsId, const struct ObjectEventGraphicsInfo *base);
enum TrainerPicID LegendsGetPlayerTrainerPic(enum Gender gender);

#endif
