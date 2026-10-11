#include "global.h"
#include "legends_appearance.h"
#include "data/legends/style_layers.h"

// Art is authored against each original pose, then stored as sparse pixel
// edits in ROM. No face detection or geometric drawing occurs on the GBA.
static void ApplyEdits(u8 *bits, u8 width, const struct StyleEdits *layer, bool8 coat)
{
    u32 i;
    for (i = 0; i < layer->count; i++)
    {
        u16 edit = sStylePixels[layer->offset + i];
        u32 pixel = edit >> 4, x = pixel % width, y = pixel / width;
        u32 index = ((y >> 3) * (width >> 3) + (x >> 3)) * 32 + (y & 7) * 4 + (x & 7) / 2;
        u8 shift = (x & 1) * 4;
        // A scarf is always in front of the coat, including its loose end.
        if (coat && LegendsGetScarf() && ((bits[index] >> shift) & 15) == 14)
            continue;
        bits[index] = (bits[index] & ~(15 << shift)) | ((edit & 15) << shift);
    }
}

void LegendsPaintStylePose(u8 *bits, u8 width, u8 gender, u8 kind, u8 state, u8 pose, u8 hair, u8 coat)
{
    const struct StyleEdits *layers;
    if (gender > 1 || hair >= LEGENDS_HAIR_COUNT || coat >= LEGENDS_JACKET_COUNT)
        return;
    if (kind == 0)
    {
        if (state >= 8 || state == 4 || pose >= sStyleFrameCount[gender][state])
            return; // Native underwater suit stays intact.
        layers = sStyleWorld[gender][state][pose];
    }
    else if (kind == 1)
        layers = sStyleFront[gender];
    else if (kind == 2 && pose < 4)
        layers = sStyleBack[gender][pose];
    else
        return;
    if (coat)
        ApplyEdits(bits, width, &layers[9 + coat], TRUE);
    if (hair)
        ApplyEdits(bits, width, &layers[hair - 1], FALSE);
}
