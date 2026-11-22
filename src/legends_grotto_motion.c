#include "global.h"
#include "legends_grotto_review.h"
#include "legends_grottos.h"
#include "field_camera.h"
#include "fieldmap.h"
#include "palette.h"
#include "script.h"
#include "tileset_anims.h"
#include "constants/layouts.h"

struct GrottoMotion
{
    const u16 *graphics;
    const u8 *poses;
    u16 layout, metatile, tileBase;
    u8 x, y, cells, layerOffset, poseCount;
};

// One beat is four field frames. Zero selects the original map art.
static const u8 sVines[] = {1, 2, 2, 1, 0, 3, 3, 4, 0, 1, 0};
static const u8 sPlank[] = {1, 3, 3, 2, 1, 0, 0, 0, 1, 2, 1, 0};
static const u8 sFronds[] = {1, 2, 3, 3, 3, 2, 1, 0};
static const u16 sVineTiles[] = INCBIN_U16("data/tilesets/legends_grotto/leafshade_motion.bin");
static const u16 sPlankTiles[] = INCBIN_U16("data/tilesets/legends_grotto/stillwater_motion.bin");
static const u16 sFrondTiles[] = INCBIN_U16("data/tilesets/legends_grotto/rainroot_motion.bin");
static const struct GrottoMotion sEntrances[LEGENDS_GROTTO_COUNT] =
{
    {sVineTiles, sVines, LAYOUT_PETALBURG_WOODS, 0x036, 632, 12, 31, 2, 0, ARRAY_COUNT(sVines)},
    {sPlankTiles, sPlank, LAYOUT_ROUTE114, 0x379, 632, 7, 46, 1, 4, ARRAY_COUNT(sPlank)},
    {sFrondTiles, sFronds, LAYOUT_ROUTE119, 0x278, 644, 27, 105, 1, 4, ARRAY_COUNT(sFronds)},
};
static EWRAM_DATA const struct GrottoMotion *sEntrance;
static EWRAM_DATA u16 sTimer;
static EWRAM_DATA u8 sPose;

static void RedrawEntrance(void)
{
    for (u32 i = 0; i < sEntrance->cells; i++)
        CurrentMapDrawMetatileAt(sEntrance->x + MAP_OFFSET + i, sEntrance->y + MAP_OFFSET);
}

void LegendsGrottoResetMotion(void)
{
    // A menu can rebuild the same map before its tileset animation initializes.
    if (sPose && sEntrance && sEntrance->layout == gMapHeader.mapLayoutId)
    {
        sPose = 0;
        RedrawEntrance();
    }
    sPose = 0;
    sTimer = 0;
    sEntrance = NULL;
    for (u32 i = 0; i < ARRAY_COUNT(sEntrances); i++)
        if (sEntrances[i].layout == gMapHeader.mapLayoutId)
            sEntrance = &sEntrances[i];
}

void LegendsGrottoTickMotion(void)
{
    if (!sEntrance)
        return;
    u8 pose = 0;
    // Saved camera coordinates are the player's unpadded field position.
    s32 dx = gSaveBlock1Ptr->pos.x - sEntrance->x;
    s32 dy = gSaveBlock1Ptr->pos.y - sEntrance->y;
    if (dx < -7 || dx > 7 || dy < -5 || dy > 5 || gPaletteFade.active
     || ScriptContext_IsEnabled() || !LegendsGrottoVisitorAvailable(sEntrance - sEntrances))
        sTimer = 0;
    else
    {
        if (++sTimer >= 360)
            sTimer = 0;
        if (sTimer >= 60 && (sTimer - 60) / 4 < sEntrance->poseCount)
            pose = sEntrance->poses[(sTimer - 60) / 4];
    }
    if (pose == sPose)
        return;
    bool32 redraw = !sPose || !pose;
    sPose = pose;
    if (pose)
    {
        u32 size = sEntrance->cells * 4 * TILE_SIZE_4BPP;
        const u16 *src = sEntrance->graphics + (pose - 1) * (size / sizeof(u16));
        AppendTilesetAnimToBuffer(src, (u16 *)(BG_VRAM + TILE_OFFSET_4BPP(sEntrance->tileBase)), size);
    }
    if (redraw)
        RedrawEntrance();
}

const u16 *LegendsGrottoMotionTiles(s32 x, s32 y, u16 metatile, const u16 *tiles)
{
    static EWRAM_DATA u16 replacement[NUM_TILES_PER_METATILE];
    if (!sPose || gMapHeader.mapLayoutId != sEntrance->layout || y != sEntrance->y + MAP_OFFSET)
        return tiles;
    s32 cell = x - MAP_OFFSET - sEntrance->x;
    if (cell < 0 || cell >= sEntrance->cells || metatile != sEntrance->metatile + cell)
        return tiles;
    memcpy(replacement, tiles, sizeof(replacement));
    // Poses contain displayed pixels, including native flips. Keep palette and layer priority.
    u16 *layer = replacement + sEntrance->layerOffset;
    for (u32 i = 0; i < 4; i++)
        layer[i] = (layer[i] & 0xF000) | (sEntrance->tileBase + cell * 4 + i);
    return replacement;
}
