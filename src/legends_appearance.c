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
    u8 scarf;
    bool8 jacket;
    bool8 legacySkin;
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
        return sSelection.legacySkin ? 26 + sSelection.outfit : 1 + sSelection.skin + LEGENDS_SKIN_TONE_COUNT * sSelection.outfit;
    code = VarGet(VAR_LEGENDS_APPEARANCE);
    return code <= 30 ? code : 0;
}

u8 LegendsGetSkinTone(void)
{
    u16 code = GetAppearanceCode();
    return code && code <= 25 ? (code - 1) % LEGENDS_SKIN_TONE_COUNT : 0;
}

u8 LegendsGetOutfit(void)
{
    u16 code = GetAppearanceCode();
    return code > 25 ? code - 26 : code ? (code - 1) / LEGENDS_SKIN_TONE_COUNT : 0;
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
    sSelection.scarf = 0;
    sSelection.jacket = FALSE;
    sSelection.legacySkin = FALSE;
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
    VarSet(VAR_LEGENDS_ACCESSORIES, 0);
    LegendsClearAppearanceSelection();
}

static u8 GetAccessoryCode(void)
{
    u16 code = sSelection.valid ? sSelection.scarf + LEGENDS_SCARF_COUNT * sSelection.jacket
                              : VarGet(VAR_LEGENDS_ACCESSORIES);
    return code < 2 * LEGENDS_SCARF_COUNT ? code : 0;
}

u8 LegendsGetScarf(void) { return GetAccessoryCode() % LEGENDS_SCARF_COUNT; }
bool8 LegendsGetJacket(void) { return GetAccessoryCode() >= LEGENDS_SCARF_COUNT; }
u8 LegendsGetAccessoryStyle(void) { return (LegendsGetScarf() != 0) | (LegendsGetJacket() << 1); }

void LegendsBeginWardrobeSelection(void)
{
    u8 skin = LegendsGetSkinTone(), outfit = LegendsGetOutfit();
    u8 scarf = LegendsGetScarf();
    bool8 jacket = LegendsGetJacket();
    sSelection.legacySkin = GetAppearanceCode() == 0 || GetAppearanceCode() > 25;
    sSelection.skin = skin;
    sSelection.outfit = outfit;
    sSelection.scarf = scarf;
    sSelection.jacket = jacket;
    sSelection.valid = TRUE;
    sPaletteStamp = 0;
}

void LegendsSetAccessorySelection(u8 scarf, bool8 jacket)
{
    sSelection.scarf = scarf < LEGENDS_SCARF_COUNT ? scarf : 0;
    sSelection.jacket = !!jacket;
    sPaletteStamp = 0;
}

void LegendsApplyWardrobeSelection(void)
{
    VarSet(VAR_LEGENDS_APPEARANCE, GetAppearanceCode());
    VarSet(VAR_LEGENDS_ACCESSORIES, GetAccessoryCode());
    LegendsClearAppearanceSelection();
}

void LegendsUpdateAppearancePalettes(void)
{
    u16 code = GetAppearanceCode();
    u16 stamp = code + 1 + 31 * GetAccessoryCode();
    u32 gender, i;
    u8 skin = LegendsGetSkinTone();
    u8 outfit = LegendsGetOutfit();
    if (sPaletteStamp == stamp)
        return;
    sPaletteStamp = stamp;
    for (gender = 0; gender < 2; gender++)
    {
        for (i = 0; i < 16; i++)
        {
            gLegendsOverworldPalettes[gender][i] = sBaseOverworldPalettes[gender][i];
            gLegendsTrainerPalettes[gender][i] = sBaseTrainerPalettes[gender][i];
            gLegendsUnderwaterPalettes[gender][i] = sBaseUnderwaterPalette[i];
        }
        if (code != 0 && code <= 25)
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
        if (LegendsGetScarf())
        {
            // Accessories alone reserve highlight 14; Poké Balls keep red 12/13.
            static const u16 colors[] = {0, 0x2118, 0x6EAC, 0x2EAA, 0x7A58, 0x679F};
            gLegendsOverworldPalettes[gender][14] = colors[LegendsGetScarf()];
            gLegendsTrainerPalettes[gender][14] = colors[LegendsGetScarf()];
        }
    }
}

enum TrainerPicID LegendsGetPlayerTrainerPic(enum Gender gender)
{
    LegendsUpdateAppearancePalettes();
    if (LegendsGetAccessoryStyle())
        return TRAINER_PIC_LEGENDS_ACCESSORY_0
             + ((LegendsGetAccessoryStyle() - 1) * 2 + (gender == FEMALE)) * LEGENDS_OUTFIT_COUNT + LegendsGetOutfit();
    return TRAINER_PIC_LEGENDS_BRENDAN_EMERALD
         + (gender == FEMALE ? LEGENDS_OUTFIT_COUNT : 0) + LegendsGetOutfit();
}
