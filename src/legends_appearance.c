#include "global.h"
#include "legends_appearance.h"
#include "event_data.h"
#include "constants/event_objects.h"
#include "constants/vars.h"
#include "constants/rgb.h"

struct AppearanceSelection
{
    bool8 valid;
    u8 skin;
    u8 outfit;
    u8 scarf;
    u8 costume;
    u8 shoes;
    u8 cardColor;
    u8 hair;
    u8 jacket;
    bool8 legacySkin;
    u8 hairColor;
    u8 leggings;
};

EWRAM_DATA static struct AppearanceSelection sSelection = {0};
EWRAM_DATA static u32 sPaletteStamp = 0;
EWRAM_DATA u16 gLegendsOverworldPalettes[2][16] = {0};
EWRAM_DATA u16 gLegendsTrainerPalettes[2][16] = {0};
EWRAM_DATA u16 gLegendsUnderwaterPalettes[2][16] = {0};

#include "data/legends/appearance_palettes.h"
#include "data/legends/costume_palettes.h"



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

void LegendsCopySkinRamp(u16 *dest)
{
    u32 i;
    u8 skin = LegendsGetSkinTone();
    for (i = 0; i < 3; i++)
        dest[i] = sSkinPalettes[skin][i];
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
    sSelection.leggings = 0;
    sSelection.outfit = 0;
    sSelection.scarf = 0;
    sSelection.costume = 0;
    sSelection.shoes = 0;
    sSelection.cardColor = 0;
    sSelection.hair = 0;
    sSelection.hairColor = 0;
    sSelection.jacket = 0;
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
    VarSet(VAR_LEGENDS_COSTUME, 0);
    VarSet(VAR_LEGENDS_SHOES, 0);
    VarSet(VAR_LEGENDS_CARD_COLOR, 0);
    VarSet(VAR_LEGENDS_HAIR, sSelection.valid ? sSelection.hair + LEGENDS_HAIR_COUNT * sSelection.hairColor : 0);
    VarSet(VAR_LEGENDS_LEGGINGS, 0);
    LegendsClearAppearanceSelection();
}

u8 LegendsGetCostume(void)
{
    u16 costume = sSelection.valid ? sSelection.costume : VarGet(VAR_LEGENDS_COSTUME);
    return costume < LEGENDS_COSTUME_COUNT ? costume : 0;
}

void LegendsSetCostumeSelection(u8 costume)
{
    sSelection.costume = costume < LEGENDS_COSTUME_COUNT ? costume : 0;
    sPaletteStamp = 0;
}

static u8 GetAccessoryCode(void)
{
    u16 code = sSelection.valid ? sSelection.scarf + LEGENDS_SCARF_COUNT * sSelection.jacket
                              : VarGet(VAR_LEGENDS_ACCESSORIES);
    return code < LEGENDS_JACKET_COUNT * LEGENDS_SCARF_COUNT ? code : 0;
}

u8 LegendsGetScarf(void) { return GetAccessoryCode() % LEGENDS_SCARF_COUNT; }
u8 LegendsGetJacketStyle(void) { return GetAccessoryCode() / LEGENDS_SCARF_COUNT; }
bool8 LegendsGetJacket(void) { return LegendsGetJacketStyle() != 0; }
u8 LegendsGetAccessoryStyle(void) { return (LegendsGetScarf() != 0) | (LegendsGetJacket() << 1); }

void LegendsBeginWardrobeSelection(void)
{
    u8 skin = LegendsGetSkinTone(), outfit = LegendsGetOutfit();
    u8 scarf = LegendsGetScarf(), costume = LegendsGetCostume();
    u8 shoes = LegendsGetShoes(), card = LegendsGetCardColor();
    u8 jacket = LegendsGetJacketStyle(), hair = LegendsGetHair(), hairColor = LegendsGetHairColor();
    sSelection.legacySkin = GetAppearanceCode() == 0 || GetAppearanceCode() > 25;
    sSelection.skin = skin;
    sSelection.outfit = outfit;
    sSelection.scarf = scarf;
    sSelection.costume = costume;
    sSelection.shoes = shoes;
    sSelection.cardColor = card;
    sSelection.hair = hair;
    sSelection.hairColor = hairColor;
    sSelection.leggings = LegendsGetLeggings();
    sSelection.jacket = jacket;
    sSelection.valid = TRUE;
    sPaletteStamp = 0;
}

void LegendsSetAccessorySelection(u8 scarf, u8 jacket)
{
    sSelection.scarf = scarf < LEGENDS_SCARF_COUNT ? scarf : 0;
    sSelection.jacket = jacket < LEGENDS_JACKET_COUNT ? jacket : 0;
    sPaletteStamp = 0;
}

void LegendsApplyWardrobeSelection(void)
{
    VarSet(VAR_LEGENDS_APPEARANCE, GetAppearanceCode());
    VarSet(VAR_LEGENDS_ACCESSORIES, GetAccessoryCode());
    VarSet(VAR_LEGENDS_COSTUME, LegendsGetCostume());
    VarSet(VAR_LEGENDS_SHOES, LegendsGetShoes());
    VarSet(VAR_LEGENDS_CARD_COLOR, LegendsGetCardColor());
    VarSet(VAR_LEGENDS_HAIR, LegendsGetHair() + LEGENDS_HAIR_COUNT * LegendsGetHairColor());
    VarSet(VAR_LEGENDS_LEGGINGS, LegendsGetLeggings());
    LegendsClearAppearanceSelection();
}

void LegendsUpdateAppearancePalettes(void)
{
    u16 code = GetAppearanceCode();
    u32 stamp = code + 1 + 31 * GetAccessoryCode() + 558 * LegendsGetCostume()
              + 1674 * LegendsGetShoes() + 13392 * LegendsGetHair()
              + 147312 * LegendsGetHairColor() + 1178496 * LegendsGetLeggings();
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
            gLegendsOverworldPalettes[gender][i] = LegendsGetCostume() ? sLegendsCostumeOverworldPalettes[LegendsGetCostume()-1][gender][i] : sBaseOverworldPalettes[gender][i];
            gLegendsTrainerPalettes[gender][i] = LegendsGetCostume() ? sLegendsCostumeTrainerPalettes[LegendsGetCostume()-1][gender][i] : sBaseTrainerPalettes[gender][i];
            gLegendsUnderwaterPalettes[gender][i] = sBaseUnderwaterPalette[i];
        }
        if (code != 0 && code <= 25)
            for (i = 0; i < 3; i++)
            {
                gLegendsOverworldPalettes[gender][i + 1] = sSkinPalettes[skin][i];
                gLegendsTrainerPalettes[gender][i + 1] = sSkinPalettes[skin][i];
                gLegendsUnderwaterPalettes[gender][i + 1] = sSkinPalettes[skin][i];
            }
        if (outfit != 0 && !LegendsGetCostume())
            for (i = 0; i < 2; i++)
            {
                // Only the dedicated clothing/accent colors; hair stays intact.
                gLegendsOverworldPalettes[gender][10 + i] = sOutfitPalettes[outfit - 1][i];
                gLegendsTrainerPalettes[gender][10 + i] = sOutfitPalettes[outfit - 1][i];
                gLegendsUnderwaterPalettes[gender][10 + i] = sOutfitPalettes[outfit - 1][i];
            }
        if (LegendsGetHair() && !LegendsGetCostume() && gender == MALE)
        {
            // Custom hair has a warm highlight. The compositor first moves
            // Brendan's native clothing shade 7 to stable field blue slot 8.
            // His eyes use native 5/9/14/15 and keep their exact colors.
            gLegendsOverworldPalettes[gender][7] = 22 | (13 << 5) | (8 << 10);
            gLegendsTrainerPalettes[gender][7] = 22 | (15 << 5) | (10 << 10);
        }
        if (LegendsGetHairColor() && !LegendsGetCostume())
        {
            static const u16 colors[LEGENDS_HAIR_COLOR_COUNT-1][2] = {
                {RGB(6,6,7),RGB(12,12,14)}, {RGB(10,6,5),RGB(17,11,8)},
                {RGB(15,9,6),RGB(23,15,10)}, {RGB(17,6,4),RGB(26,12,7)},
                {RGB(21,13,6),RGB(29,22,11)}, {RGB(26,20,11),RGB(31,28,20)},
                {RGB(18,20,23),RGB(28,29,31)},
            };
            gLegendsOverworldPalettes[gender][4] = gLegendsTrainerPalettes[gender][4] = colors[LegendsGetHairColor()-1][0];
            gLegendsOverworldPalettes[gender][7] = gLegendsTrainerPalettes[gender][7] = colors[LegendsGetHairColor()-1][1];
        }
        if (gender == MALE && LegendsGetHair() && !LegendsGetCostume())
        {
            // Native-scale field hair uses two independent shades and the
            // native outline. Keep both original pupil/body blues (5/8).
            // Curls reserves only red-shadow 13 for its fixed green cap;
            // the compositor keeps small native red details in red 12.
            if (LegendsGetHair() == 8)
                gLegendsOverworldPalettes[gender][13] = sBaseOverworldPalettes[gender][10];
            if (!LegendsGetHairColor())
            {
                gLegendsOverworldPalettes[gender][4] = RGB(17,11,7);
                gLegendsOverworldPalettes[gender][7] = RGB(23,16,10);
            }
        }
        if (LegendsGetJacket() && !LegendsGetCostume())
        {
            u16 coat = LegendsGetJacketStyle() == 2 ? RGB(4,11,7) : RGB(4,7,13);
            gLegendsOverworldPalettes[gender][10] = gLegendsTrainerPalettes[gender][10] = coat;
        }
        if (LegendsGetAccessoryStyle() && !LegendsGetCostume())
        {
            // Templates reserve scarf slot 14 by moving native white to 9.
            // This applies to jacket-only templates too: retain exact eye white.
            gLegendsOverworldPalettes[gender][9] = 0x7FFF;
            gLegendsTrainerPalettes[gender][9] = 0x7FFF;
        }
        if (LegendsGetScarf() && !LegendsGetCostume())
        {
            // Accessories alone reserve highlight 14; Poké Balls keep red 12/13.
            static const u16 colors[] = {0, 0x2118, 0x6EAC, 0x2EAA, 0x7A58, 0x679F};
            gLegendsOverworldPalettes[gender][14] = colors[LegendsGetScarf()];
            gLegendsTrainerPalettes[gender][14] = colors[LegendsGetScarf()];
        }
        if (LegendsGetShoes() && !LegendsGetCostume())
        {
            LegendsPrepareFootwearPalette(gLegendsOverworldPalettes[gender], gender, 0);
            LegendsPrepareFootwearPalette(gLegendsTrainerPalettes[gender], gender, 1);
            // The diving suit has no visible footwear: keep its native colors.
        }
    }
}

enum TrainerPicID LegendsGetPlayerTrainerPic(enum Gender gender)
{
    LegendsUpdateAppearancePalettes();
    if (LegendsGetCostume())
        return TRAINER_PIC_LEGENDS_COSTUME_0 + (LegendsGetCostume()-1)*2 + (gender == FEMALE);
    if (LegendsGetAccessoryStyle())
        return TRAINER_PIC_LEGENDS_ACCESSORY_0
             + ((LegendsGetAccessoryStyle() - 1) * 2 + (gender == FEMALE)) * LEGENDS_OUTFIT_COUNT + LegendsGetOutfit();
    return TRAINER_PIC_LEGENDS_BRENDAN_EMERALD
         + (gender == FEMALE ? LEGENDS_OUTFIT_COUNT : 0) + LegendsGetOutfit();
}

u8 LegendsGetShoes(void)
{
    u16 value = sSelection.valid ? sSelection.shoes : VarGet(VAR_LEGENDS_SHOES);
    return value < LEGENDS_SHOE_COUNT ? value : 0;
}

u8 LegendsGetLeggings(void)
{
    u16 value = sSelection.valid ? sSelection.leggings : VarGet(VAR_LEGENDS_LEGGINGS);
    return value < LEGENDS_LEGGINGS_COUNT ? value : 0;
}

void LegendsSetLeggingsSelection(u8 leggings)
{
    sSelection.leggings = leggings < LEGENDS_LEGGINGS_COUNT ? leggings : 0;
}
u8 LegendsGetCardColor(void)
{
    u16 value = sSelection.valid ? sSelection.cardColor : VarGet(VAR_LEGENDS_CARD_COLOR);
    return value < LEGENDS_CARD_COLOR_COUNT ? value : 0;
}
void LegendsSetShoeSelection(u8 value)
{
    sSelection.shoes = value < LEGENDS_SHOE_COUNT ? value : 0;
    sPaletteStamp = 0;
}
void LegendsSetCardColorSelection(u8 value)
{
    sSelection.cardColor = value < LEGENDS_CARD_COLOR_COUNT ? value : 0;
}

// Zero is the unmodified Emerald hat; the remaining ten values are custom
// hair silhouettes. Saved in an otherwise unused native state variable.
static u16 GetHairCode(void)
{
    u16 value = VarGet(VAR_LEGENDS_HAIR);
    return value < LEGENDS_HAIR_COUNT * LEGENDS_HAIR_COLOR_COUNT ? value : 0;
}

u8 LegendsGetHair(void)
{
    return sSelection.valid ? sSelection.hair : GetHairCode() % LEGENDS_HAIR_COUNT;
}
u8 LegendsGetHairColor(void)
{
    return sSelection.valid ? sSelection.hairColor : GetHairCode() / LEGENDS_HAIR_COUNT;
}
void LegendsSetHairSelection(u8 hair)
{
    sSelection.hair = hair < LEGENDS_HAIR_COUNT ? hair : 0;
    sPaletteStamp = 0;
}
void LegendsSetHairColorSelection(u8 color)
{
    sSelection.hairColor = color < LEGENDS_HAIR_COLOR_COUNT ? color : 0;
    sPaletteStamp = 0;
}

const u8 *LegendsGetHairName(enum Gender gender, u8 hair)
{
    static const u8 *const names[2][LEGENDS_HAIR_COUNT] = {
        {COMPOUND_STRING("ORIGINAL"),COMPOUND_STRING("CREW CUT"),COMPOUND_STRING("SIDE PART"),COMPOUND_STRING("SPIKY"),COMPOUND_STRING("SIDE SWEEP"),COMPOUND_STRING("TOUSLED"),COMPOUND_STRING("QUIFF"),COMPOUND_STRING("SHAG"),COMPOUND_STRING("CURLS"),COMPOUND_STRING("MAN BUN"),COMPOUND_STRING("UNDERCUT")},
        {COMPOUND_STRING("ORIGINAL"),COMPOUND_STRING("PIXIE"),COMPOUND_STRING("SIDE PART"),COMPOUND_STRING("SOFT LAYERS"),COMPOUND_STRING("SIDE SWEEP"),COMPOUND_STRING("WAVY BOB"),COMPOUND_STRING("SHORT BOB"),COMPOUND_STRING("LONG BOB"),COMPOUND_STRING("CURLS"),COMPOUND_STRING("PONYTAIL"),COMPOUND_STRING("TWIN BRAIDS")},
    };
    return names[gender == FEMALE][hair < LEGENDS_HAIR_COUNT ? hair : 0];
}
const u8 *LegendsGetHairColorName(u8 color)
{
    static const u8 *const names[LEGENDS_HAIR_COLOR_COUNT] = {COMPOUND_STRING("NATURAL"),COMPOUND_STRING("BLACK"),COMPOUND_STRING("DARK BROWN"),COMPOUND_STRING("CHESTNUT"),COMPOUND_STRING("AUBURN"),COMPOUND_STRING("HONEY"),COMPOUND_STRING("BLOND"),COMPOUND_STRING("SILVER")};
    return names[color < LEGENDS_HAIR_COLOR_COUNT ? color : 0];
}
