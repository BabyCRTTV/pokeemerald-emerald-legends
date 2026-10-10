#ifndef GUARD_LEGENDS_APPEARANCE_H
#define GUARD_LEGENDS_APPEARANCE_H

#include "global.h"
#include "constants/trainers.h"

struct SpriteFrameImage;

#define LEGENDS_SKIN_TONE_COUNT 5
#define LEGENDS_OUTFIT_COUNT 5
#define LEGENDS_SCARF_COUNT 6
#define LEGENDS_COSTUME_COUNT 3
#define LEGENDS_APPEARANCE_STATES 9
#define LEGENDS_SHOE_COUNT 8
#define LEGENDS_CARD_COLOR_COUNT 8

extern u16 gLegendsOverworldPalettes[2][16];
extern u16 gLegendsTrainerPalettes[2][16];
extern u16 gLegendsUnderwaterPalettes[2][16];

void LegendsBeginAppearanceSelection(void);
void LegendsClearAppearanceSelection(void);
void LegendsSetAppearanceSelection(u8 skin, u8 outfit);
void LegendsApplyAppearanceToNewGame(void);
u8 LegendsGetShoes(void);
u8 LegendsGetCardColor(void);
void LegendsSetShoeSelection(u8 shoes);
void LegendsSetCardColorSelection(u8 color);
void LegendsPrepareFootwearPalette(u16 *palette, u8 gender, u8 kind);
const struct SpriteFrameImage *LegendsFootwearImages(const struct SpriteFrameImage *images, u8 gender, u8 state);
const u32 *LegendsFootwearFrontPic(enum TrainerPicID pic, const u32 *data);
void LegendsFootwearBackPic(enum TrainerPicID pic, u8 *data, u32 size);
void LegendsApplyCardColor(void);
u16 LegendsCardSwatch(void);
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
