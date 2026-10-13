#ifndef GUARD_LEGENDS_APPEARANCE_H
#define GUARD_LEGENDS_APPEARANCE_H

#include "global.h"
#include "constants/trainers.h"

struct SpriteFrameImage;

const struct SpriteFrameImage *LegendsBattleBackImage(enum TrainerPicID pic);
const u16 *LegendsBattleBackPalette(enum TrainerPicID pic);
void LegendsCopySkinRamp(u16 *dest);

#define LEGENDS_SKIN_TONE_COUNT 5
#define LEGENDS_OUTFIT_COUNT 5
#define LEGENDS_SCARF_COUNT 6
#define LEGENDS_COSTUME_COUNT 3
#define LEGENDS_APPEARANCE_STATES 9
#define LEGENDS_SHOE_COUNT 8
#define LEGENDS_CARD_COLOR_COUNT 8
#define LEGENDS_JACKET_COUNT 3
#define LEGENDS_HAIR_COUNT 11
#define LEGENDS_HAIR_COLOR_COUNT 8
#define LEGENDS_LEGGINGS_COUNT 3

extern u16 gLegendsOverworldPalettes[2][16];
extern u16 gLegendsTrainerPalettes[2][16];
extern u16 gLegendsUnderwaterPalettes[2][16];

void LegendsBeginAppearanceSelection(void);
void LegendsClearAppearanceSelection(void);
void LegendsSetAppearanceSelection(u8 skin, u8 outfit);
void LegendsApplyAppearanceToNewGame(void);
u8 LegendsGetShoes(void);
u8 LegendsGetLeggings(void);
void LegendsSetLeggingsSelection(u8 leggings);
u8 LegendsGetCardColor(void);
void LegendsSetShoeSelection(u8 shoes);
void LegendsSetCardColorSelection(u8 color);
void LegendsPrepareFootwearPalette(u16 *palette, u8 gender, u8 kind);
const struct SpriteFrameImage *LegendsFootwearImages(const struct SpriteFrameImage *images, u8 gender, u8 state);
const u32 *LegendsFootwearFrontPic(enum TrainerPicID pic, const u32 *data);
const u16 *LegendsMaleFrontPalette(enum TrainerPicID pic);
void LegendsBuildMaleFront(u32 *picture, u8 *tiles);
void LegendsFootwearBackPic(enum TrainerPicID pic, u8 *data, u32 size);
const struct SpriteFrameImage *LegendsFootwearBackImages(enum TrainerPicID pic, const struct SpriteFrameImage *images, u8 frameCount);
void LegendsApplyCardColor(void);
u16 LegendsCardSwatch(void);
void LegendsBeginWardrobeSelection(void);
void LegendsSetAccessorySelection(u8 scarf, u8 jacket);
void LegendsApplyWardrobeSelection(void);
u8 LegendsGetCostume(void);
void LegendsSetCostumeSelection(u8 costume);
u8 LegendsGetScarf(void);
bool8 LegendsGetJacket(void);
u8 LegendsGetJacketStyle(void);
u8 LegendsGetHair(void);
void LegendsSetHairSelection(u8 hair);
u8 LegendsGetHairColor(void);
void LegendsSetHairColorSelection(u8 color);
const u8 *LegendsGetHairName(enum Gender gender, u8 hair);
const u8 *LegendsGetHairColorName(u8 color);
void LegendsPaintStylePose(u8 *data, u8 width, u8 gender, u8 kind, u8 state, u8 pose, u8 hair, u8 coat);
u8 LegendsGetAccessoryStyle(void);
u8 LegendsGetSkinTone(void);
u8 LegendsGetOutfit(void);
void LegendsUpdateAppearancePalettes(void);
u16 LegendsGetPlayerGraphicsId(u8 state, enum Gender gender);
u16 LegendsGetBasePlayerGraphicsId(u16 graphicsId);
const struct ObjectEventGraphicsInfo *LegendsGetPlayerGraphicsInfo(u16 graphicsId, const struct ObjectEventGraphicsInfo *base);
enum TrainerPicID LegendsGetPlayerTrainerPic(enum Gender gender);

#endif
