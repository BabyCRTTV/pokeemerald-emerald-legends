#include "global.h"
#include "legends_appearance.h"

// Pixel-level accessory overlays use the native 4bpp tiled layout.
// All shades come from the unchanged palette; skin/eyes are never repainted.
// These masks are pose-local rather than whole-palette substitutions.
static u8 Pixel(const u8 *bits, u8 width, int x, int y)
{
    u32 i = ((y >> 3) * (width >> 3) + (x >> 3)) * 32 + (y & 7) * 4 + (x & 7) / 2;
    return (bits[i] >> ((x & 1) * 4)) & 15;
}
static void Put(u8 *bits, u8 width, int x, int y, u8 value)
{
    u32 i = ((y >> 3) * (width >> 3) + (x >> 3)) * 32 + (y & 7) * 4 + (x & 7) / 2;
    u8 shift = (x & 1) * 4;
    bits[i] = (bits[i] & ~(15 << shift)) | (value << shift);
}
static int Magnitude(int a) { return a < 0 ? -a : a; }

// Ten different head silhouettes (plus untouched original). The hair occupies
// the hat/crown region above the first native facial pixels. Eye, face,
// eyebrow, skin and held-object pixels below that boundary remain untouched.
// Additional strands below the crown only occupy transparent side pixels.
static bool8 HairAt(u8 style, int dx, int dy, int radius, int height)
{
    int adx = Magnitude(dx), edge;
    if (dy < 0 || dy >= height) return FALSE;
    // Rounded crown: 7px at the apex, widening into the temples.
    edge = 3 + dy * 2;
    if (edge > radius) edge = radius;
    if (dy >= height - 3) edge -= (dy - (height - 3)) / 2;
    switch (style)
    {
    case 1: return adx <= edge && dy >= adx / 4; // crop
    case 2: return dx >= -edge - 1 && dx <= edge && dy >= (dx < -1 ? 3 : 0)
                && !(dx == -2 && dy < 4); // side part
    case 3: return (adx <= edge && dy >= 2)
                || (dy <= 3 && adx <= radius && dx % 5 >= 0 && dx % 5 <= 1); // spikes
    case 4: return dx >= -edge - 2 && dx <= (edge > 2 ? edge - 2 : 1)
                && dy >= (dx > 3 ? 3 : 0); // side sweep
    case 5: return adx <= edge && dy >= ((dx + radius) % 5 <= 1 ? 0 : 2); // tousled
    case 6: return adx <= (edge > 2 ? edge - 2 : 1) && dy >= adx / 3; // pixie
    case 7: return adx <= edge && dy >= adx / 5; // bob
    case 8: return adx <= edge && (dy >= 3 || (adx % 4 <= 1 && dy >= 1)); // curls
    case 9: return dx >= -edge && dx <= edge && dy >= (dx < 0 ? 1 : 3); // pony
    case 10:return adx <= edge && dy >= adx / 5; // twin tails
    default:return FALSE;
    }
}
void LegendsPaintStyle(u8 *bits, u8 width, u8 height, u8 gender, bool8 isBack, u8 hairstyle, u8 coat)
{
    int x, y, top = height, center = width / 2, sum = 0, count = 0;
    int headTop, headHeight, radius, collar, bottom, torsoRadius;
    if (!hairstyle && coat != 2) return;
    if (isBack)
    {
        top = height == 64 ? 21 : 11;
    }
    else
    {
        // The upper skin island identifies the face without relying on frame
        // number: biking, fishing and overworld action sprites shift position.
        for (y = 0; y < (height == 64 ? 35 : 21); y++)
            for (x = width / 5; x < width - width / 5; x++)
            {
                u8 v = Pixel(bits, width, x, y);
                if (v >= 1 && v <= 3 && y < top)
                    top = y;
            }
        if (top == height)
            top = height == 64 ? 21 : 11;
        for (y = top; y < top + 4 && y < height; y++)
            for (x = width / 5; x < width - width / 5; x++)
            {
                u8 v = Pixel(bits, width, x, y);
                if (v >= 1 && v <= 3) { sum += x; count++; }
            }
        if (count >= 2) center = sum / count;
    }
    if (hairstyle)
    {
        headHeight = height == 64 ? 12 : 6;
        radius = width == 16 ? 6 : width == 32 ? 7 : 13;
        headTop = top - headHeight;
        for (y = headTop - 2; y < top; y++)
        {
            int dy = y - headTop;
            if (y < 0 || y >= height) continue;
            for (x = center - radius - 2; x <= center + radius + 2; x++)
            {
                u8 old, color;
                int dx = x - center;
                if (x < 0 || x >= width) continue;
                old = Pixel(bits, width, x, y);
                if (old >= 1 && old <= 3) continue;
                // Avoid erasing arm / thrown ball pixels outside the head.
                if (old == 12 || old == 13) continue;
                if (HairAt(hairstyle, dx, dy, radius, headHeight))
                {
                    // 4 and 8 are stable dark hair shades; 5 adds fine highlights.
                    color = (dy == 5 && dx % 8 == 0) ? 5
                          : (Magnitude(dx) >= radius - 2 || dy <= 1 ? 8 : 4);
                    Put(bits, width, x, y, color);
                }
                else if (Magnitude(dx) <= radius && y >= headTop - 1)
                    Put(bits, width, x, y, 0); // remove original hat pixels
            }
        }
        // Long, bobbed, ponytail and twin-tail styles have distinct outer
        // lengths; never touch the face itself or its colored eye pixels.
        if (hairstyle == 7 || hairstyle == 9 || hairstyle == 10 || hairstyle == 8)
        {
            int length = height == 64 ? (hairstyle == 7 ? 12 : 15) : (hairstyle == 7 ? 4 : 6);
            for (y = top; y < top + length && y < height; y++)
            {
                int dy = y - top;
                for (x = center - radius - 4; x <= center + radius + 4; x++)
                {
                    int dx = x - center, adx = Magnitude(dx);
                    bool8 outside = hairstyle == 7 ? (adx == radius || adx == radius - 1)
                                  : hairstyle == 8 ? adx == radius + (dy % 3 == 0)
                                  : hairstyle == 9 ? (dx >= radius && dx <= radius + 2 + (dy / 4))
                                  : (adx >= radius && adx <= radius + 1 + (dy / 4));
                    if (outside && x >= 0 && x < width && Pixel(bits,width,x,y) == 0)
                        Put(bits,width,x,y,dy % 3 == 0 ? 8 : 4);
                }
            }
        }
    }
    if (coat == 2)
    {
        // Overlapping cloth panels, long hem and a separate cream shearling
        // collar; female coat tapers at the waist rather than copying the male.
        collar = top + (height == 64 ? 14 : 7);
        bottom = height == 64 ? 49 : height - 5;
        torsoRadius = width == 64 ? (gender ? 10 : 12) : (gender ? 3 : 4);
        for (y = collar; y < bottom && y < height; y++)
        {
            int length = y - collar;
            int extent = torsoRadius + (length > (height == 64 ? 12 : 4) ? 1 : 0);
            if (gender && length > (height == 64 ? 7 : 3) && length < (height == 64 ? 16 : 6))
                extent--;
            for (x = center - extent; x <= center + extent; x++)
            {
                u8 old;
                int dx = x-center;
                if (x < 0 || x >= width) continue;
                old = Pixel(bits,width,x,y);
                if (old == 0 && Magnitude(dx) > torsoRadius) continue;
                if (old == 0 || old == 1 || old == 2 || old == 3 || old == 12 || old == 13 || old == 15)
                    continue;
                // Native light highlights may be recolored into shearling, but
                // an explicitly selected scarf retains its own reserved slot.
                if (old == 14 && LegendsGetScarf()) continue;
                if (length < (height == 64 ? 6 : 3) && Magnitude(dx) < extent - 1
                    && (Magnitude(dx) > 2 || length < 2))
                    Put(bits,width,x,y,9);
                else if (dx == 0 && length % 5 == 0)
                    Put(bits,width,x,y,9); // bright coat buttons
                else
                    Put(bits,width,x,y,(Magnitude(dx) >= extent - 1 || dx > 0) ? 8 : 4);
            }
        }
    }
}
