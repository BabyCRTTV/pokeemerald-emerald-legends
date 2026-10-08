#include "global.h"
#include "legends_appearance.h"
#include "event_data.h"
#include "constants/event_objects.h"
#include "constants/vars.h"

struct AppearanceSelection
{
    bool8 valid;
    u8 skin;
    u8 outfit;
};

EWRAM_DATA static struct AppearanceSelection sSelection = {0};
EWRAM_DATA static u16 sPaletteStamp = 0;
EWRAM_DATA u16 gLegendsOverworldPalettes[2][16] = {0};
EWRAM_DATA u16 gLegendsTrainerPalettes[2][16] = {0};
EWRAM_DATA u16 gLegendsUnderwaterPalettes[2][16] = {0};

#include "data/legends/appearance_palettes.h"

static u16 GetAppearanceCode(void)
{
    u16 code;
    if (sSelection.valid)
        return 1 + sSelection.skin + LEGENDS_SKIN_TONE_COUNT * sSelection.outfit;
    code = VarGet(VAR_LEGENDS_APPEARANCE);
    return code <= LEGENDS_SKIN_TONE_COUNT * LEGENDS_OUTFIT_COUNT ? code : 0;
}

u8 LegendsGetSkinTone(void)
{
    u16 code = GetAppearanceCode();
    return code ? (code - 1) % LEGENDS_SKIN_TONE_COUNT : 0;
}

u8 LegendsGetOutfit(void)
{
    u16 code = GetAppearanceCode();
    return code ? (code - 1) / LEGENDS_SKIN_TONE_COUNT : 0;
}

void LegendsClearAppearanceSelection(void)
{
    sSelection.valid = FALSE;
    sPaletteStamp = 0;
}

void LegendsBeginAppearanceSelection(void)
{
    sSelection.valid = TRUE;
    sSelection.skin = 0;
    sSelection.outfit = 0;
    sPaletteStamp = 0;
}

void LegendsSetAppearanceSelection(u8 skin, u8 outfit)
{
    sSelection.valid = TRUE;
    sSelection.skin = skin < LEGENDS_SKIN_TONE_COUNT ? skin : 0;
    sSelection.outfit = outfit < LEGENDS_OUTFIT_COUNT ? outfit : 0;
}

void LegendsApplyAppearanceToNewGame(void)
{
    // Called after InitEventData: staged choices survive the vars reset once.
    u16 code = sSelection.valid ? GetAppearanceCode() : 0;
    VarSet(VAR_LEGENDS_APPEARANCE, code);
    LegendsClearAppearanceSelection();
}

void LegendsUpdateAppearancePalettes(void)
{
    u16 code = GetAppearanceCode();
    u32 gender, i;
    u8 skin = LegendsGetSkinTone();
    u8 outfit = LegendsGetOutfit();
    if (sPaletteStamp == code + 1)
        return;
    sPaletteStamp = code + 1;
    for (gender = 0; gender < 2; gender++)
    {
        for (i = 0; i < 16; i++)
        {
            gLegendsOverworldPalettes[gender][i] = sBaseOverworldPalettes[gender][i];
            gLegendsTrainerPalettes[gender][i] = sBaseTrainerPalettes[gender][i];
            gLegendsUnderwaterPalettes[gender][i] = sBaseUnderwaterPalette[i];
        }
        if (code != 0)
            for (i = 0; i < 3; i++)
            {
                gLegendsOverworldPalettes[gender][i + 1] = sSkinPalettes[skin][i];
                gLegendsTrainerPalettes[gender][i + 1] = sSkinPalettes[skin][i];
                gLegendsUnderwaterPalettes[gender][i + 1] = sSkinPalettes[skin][i];
            }
        if (outfit != 0)
            for (i = 0; i < 2; i++)
            {
                // Only the dedicated clothing/accent colors; hair stays intact.
                gLegendsOverworldPalettes[gender][10 + i] = sOutfitPalettes[outfit - 1][i];
                gLegendsTrainerPalettes[gender][10 + i] = sOutfitPalettes[outfit - 1][i];
                gLegendsUnderwaterPalettes[gender][10 + i] = sOutfitPalettes[outfit - 1][i];
            }
    }
}

enum TrainerPicID LegendsGetPlayerTrainerPic(enum Gender gender)
{
    LegendsUpdateAppearancePalettes();
    return TRAINER_PIC_LEGENDS_BRENDAN_EMERALD
         + (gender == FEMALE ? LEGENDS_OUTFIT_COUNT : 0) + LegendsGetOutfit();
}
