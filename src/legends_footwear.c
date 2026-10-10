#include "global.h"
#include "legends_appearance.h"
#include "sprite.h"
#include "decompress.h"
#include "palette.h"
#include "constants/rgb.h"

#include "data/legends/footwear_masks.h"

// One stable bank: only the local player uses custom overworld art, and only
// one movement state is visible at a time. Native/link NPC graphics are separate.
// The generated capacity fits the largest native pose table without heap use.
EWRAM_DATA static u8 sWorldPixels[LEGENDS_FOOTWEAR_CACHE_BYTES] = {0};
EWRAM_DATA static struct SpriteFrameImage sWorldImages[LEGENDS_FOOTWEAR_CACHE_FRAMES] = {0};
EWRAM_DATA static const struct SpriteFrameImage *sWorldSource = NULL;
EWRAM_DATA static u8 sWorldState = 0;
EWRAM_DATA static u8 sWorldBoots = 0;
EWRAM_DATA static u8 sWorldGender = 0;
EWRAM_DATA static u8 sRemap[2][3][2] = {0};
EWRAM_DATA static u32 sFrontPic[2][577] = {0};
EWRAM_DATA static const u32 *sFrontSource[2] = {0};
EWRAM_DATA static u8 sFrontBoots[2] = {0};
EWRAM_DATA static u8 sFrontPixels[2048] = {0};

static const u16 sShoeColors[7][2] = {
    {RGB(29,8,9), RGB(17,3,5)}, {RGB(8,18,29), RGB(3,9,19)},
    {RGB(10,25,14), RGB(4,14,7)}, {RGB(30,30,28), RGB(18,19,21)},
    {RGB(23,15,29), RGB(12,7,20)},
    {RGB(24,17,10), RGB(14,8,4)}, {RGB(9,10,12), RGB(3,4,5)},
};
static const u16 sCardColors[7] = {
    RGB(10,23,14), RGB(9,19,28), RGB(26,10,12), RGB(23,17,29),
    RGB(28,23,10), RGB(28,16,21), RGB(14,17,21),
};

static u32 ColorDistance(u16 a, u16 b)
{
    s32 r = (a & 31) - (b & 31), g = ((a >> 5) & 31) - ((b >> 5) & 31), bl = ((a >> 10) & 31) - ((b >> 10) & 31);
    return r*r + g*g + bl*bl;
}

void LegendsPrepareFootwearPalette(u16 *palette, u8 gender, u8 kind)
{
    static const u8 candidates[] = {4,5,8,9,10,11,15};
    u32 slot, i;
    for (slot = 0; slot < 2; slot++)
    {
        u32 best = 0xFFFFFFFF;
        for (i = 0; i < ARRAY_COUNT(candidates); i++)
        {
            u32 distance = ColorDistance(palette[6 + slot], palette[candidates[i]]);
            if (distance < best)
            {
                best = distance;
                sRemap[gender][kind][slot] = candidates[i];
            }
        }
        // Free two shadow shades, keeping skin, hair highlights, clothing,
        // scarf and red Poké Balls separate from footwear colors.
    }
    palette[6] = sShoeColors[LegendsGetShoes() - 1][0];
    palette[7] = sShoeColors[LegendsGetShoes() - 1][1];
    // Palette reset means pointer-identical art may need a different remap.
    sWorldSource = NULL;
    sFrontSource[gender] = NULL;
}

static void Compose(u8 *dest, const u8 *src, const u8 *mask, u32 size, u8 gender, u8 kind)
{
    u32 i, shift;
    for (i = 0; i < size; i++)
    {
        u8 output = 0;
        for (shift = 0; shift < 8; shift += 4)
        {
            u8 pixel = (src[i] >> shift) & 15;
            u8 overlay = mask == NULL ? 0 : (mask[i] >> shift) & 15;
            if (pixel == 6 || pixel == 7)
                pixel = sRemap[gender][kind][pixel - 6];
            if (overlay)
                pixel = overlay == 3 ? 15 : overlay == 1 ? 6 : 7;
            output |= pixel << shift;
        }
        dest[i] = output;
    }
}

const struct SpriteFrameImage *LegendsFootwearImages(const struct SpriteFrameImage *images, u8 gender, u8 state)
{
    u32 i, offset = 0;
    u8 boots = LegendsGetShoes() >= 6;
    if (!LegendsGetShoes() || LegendsGetCostume())
        return images;
    if (sWorldSource == images && sWorldGender == gender && sWorldState == state && sWorldBoots == boots)
        return sWorldImages;
    for (i = 0; i < sFootwearFrameCount[gender][state]; i++)
    {
        u32 size = images[i].size;
        // All native player frames are uncompressed, 16x32 or 32x32.
        if (size > 512 || offset + size > sizeof(sWorldPixels))
            return images;
        sWorldImages[i].data = sWorldPixels + offset;
        sWorldImages[i].size = size;
        Compose(sWorldPixels + offset, images[i].data,
            sFootwearMasks[gender][state][boots] + offset, size, gender, state == 4 ? 2 : 0);
        offset += size;
    }
    sWorldSource = images;
    sWorldGender = gender;
    sWorldState = state;
    sWorldBoots = boots;
    return sWorldImages;
}

static u8 PicGender(enum TrainerPicID pic)
{
    if (pic < TRAINER_PIC_LEGENDS_BRENDAN_EMERALD || pic >= TRAINER_PIC_LEGENDS_COSTUME_0)
        return 2;
    if (pic >= TRAINER_PIC_LEGENDS_ACCESSORY_0)
        return ((pic - TRAINER_PIC_LEGENDS_ACCESSORY_0) / LEGENDS_OUTFIT_COUNT) % 2;
    return (pic - TRAINER_PIC_LEGENDS_BRENDAN_EMERALD) / LEGENDS_OUTFIT_COUNT;
}

const u32 *LegendsFootwearFrontPic(enum TrainerPicID pic, const u32 *data)
{
    u8 gender = PicGender(pic), boots = LegendsGetShoes() >= 6;
    u8 *out;
    u32 i, pos;
    if (gender > 1 || !LegendsGetShoes() || LegendsGetCostume())
        return data;
    LegendsUpdateAppearancePalettes();
    if (sFrontSource[gender] == data && sFrontBoots[gender] == boots)
        return sFrontPic[gender];
    DecompressDataWithHeaderWram(data, sFrontPixels);
    Compose(sFrontPixels, sFrontPixels, sFootwearFrontMasks[gender][boots], 2048, gender, 1);
    // Native literal LZ stream: all existing front-pic consumers keep working.
    sFrontPic[gender][0] = 0x00080010;
    out = (u8 *)sFrontPic[gender];
    pos = 4;
    for (i = 0; i < 2048; i += 8)
    {
        u32 j;
        out[pos++] = 0;
        for (j = 0; j < 8; j++) out[pos++] = sFrontPixels[i + j];
    }
    sFrontSource[gender] = data;
    sFrontBoots[gender] = boots;
    return sFrontPic[gender];
}

void LegendsFootwearBackPic(enum TrainerPicID pic, u8 *data, u32 size)
{
    u8 gender = PicGender(pic);
    if (gender > 1 || !LegendsGetShoes() || LegendsGetCostume())
        return;
    LegendsUpdateAppearancePalettes();
    // Feet are outside the native throwing portraits; remap shared shadows only.
    Compose(data, data, NULL, size, gender, 1);
}

static u16 Tint(u16 color, u8 light)
{
    u8 r = color & 31, g = color >> 5 & 31, b = color >> 10 & 31;
    return RGB(r + (31-r)*light/31, g + (31-g)*light/31, b + (31-b)*light/31);
}

u16 LegendsCardSwatch(void)
{
    u8 color = LegendsGetCardColor();
    return color ? sCardColors[color - 1] : RGB(18,29,16);
}

void LegendsApplyCardColor(void)
{
    u8 choice = LegendsGetCardColor();
    u16 color, value;
    u32 i;
    static const u8 slots[] = {2,9,10,11,12,28,29};
    static const u8 light[] = {27,19,13,7,0,13,0};
    if (!choice)
        return;
    color = sCardColors[choice - 1];
    for (i = 0; i < ARRAY_COUNT(slots); i++)
    {
        value = Tint(color, light[i]);
        LoadPalette(&value, slots[i], sizeof(value));
    }
}
