#include "global.h"
#include "sprite.h"
#include "graphics.h"
#include "legends_appearance.h"
#include "data/legends/battle_sheets.h"

extern const u8 gTrainerBackPic_Brendan[], gTrainerBackPic_May[];
extern const u16 gTrainerPalette_Brendan[], gTrainerPalette_May[];

// Battle art owns its own palette: wardrobe clothing, scarves, footwear and
// costumes cannot recolor these fixed uniforms. Rebuild from current choices
// on each request so a wardrobe change also takes effect in the next battle.
EWRAM_DATA static u16 sBattlePalettes[2][16] = {0};

static u8 BattlePicGender(enum TrainerPicID pic)
{
    if (pic >= TRAINER_PIC_LEGENDS_BRENDAN_EMERALD && pic < TRAINER_PIC_LEGENDS_ACCESSORY_0)
        return (pic - TRAINER_PIC_LEGENDS_BRENDAN_EMERALD) / LEGENDS_OUTFIT_COUNT;
    if (pic >= TRAINER_PIC_LEGENDS_ACCESSORY_0 && pic < TRAINER_PIC_LEGENDS_COSTUME_0)
        return ((pic - TRAINER_PIC_LEGENDS_ACCESSORY_0) / LEGENDS_OUTFIT_COUNT) % 2;
    if (pic >= TRAINER_PIC_LEGENDS_COSTUME_0 && pic < TRAINER_PIC_LEGENDS_COSTUME_0 + 4)
        return (pic - TRAINER_PIC_LEGENDS_COSTUME_0) % 2;
    return 2;
}

static const struct SpriteFrameImage sDefaultBattleImages[2] = {
    {.data=gTrainerBackPic_Brendan, .size=2048, .relativeFrames=TRUE},
    {.data=gTrainerBackPic_May, .size=2048, .relativeFrames=TRUE},
};

const struct SpriteFrameImage *LegendsBattleBackImage(enum TrainerPicID pic)
{
    u8 gender = BattlePicGender(pic);
    u8 hair = LegendsGetHair();
    if (gender > 1)
        return NULL;
    if (gender == FEMALE && hair > 0 && hair < LEGENDS_HAIR_COUNT)
        return &sMayBattleImages[hair - 1];
    return &sDefaultBattleImages[gender];
}

const u16 *LegendsBattleBackPalette(enum TrainerPicID pic)
{
    u8 gender = BattlePicGender(pic);
    u8 hair = LegendsGetHair(), color = LegendsGetHairColor();
    u32 i;
    const u16 *source;
    if (gender > 1)
        return NULL;
    source = gender == FEMALE && hair > 0 && hair < LEGENDS_HAIR_COUNT
        ? sMayBattleBasePalette : (gender == FEMALE ? gTrainerPalette_May : gTrainerPalette_Brendan);
    for (i = 0; i < 16; i++)
        sBattlePalettes[gender][i] = source[i];
    LegendsCopySkinRamp(sBattlePalettes[gender] + 1);
    if (gender == FEMALE && hair > 0 && hair < LEGENDS_HAIR_COUNT)
    {
        sBattlePalettes[gender][4] = sMayBattleHairRamps[color][0];
        sBattlePalettes[gender][7] = sMayBattleHairRamps[color][1];
        sBattlePalettes[gender][11] = sMayBattleHairRamps[color][2];
    }
    return sBattlePalettes[gender];
}
