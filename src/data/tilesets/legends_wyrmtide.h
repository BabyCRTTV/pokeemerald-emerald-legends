// Contextual variants retain every native Cave pixel and its animation indices.
const u32 gTilesetTiles_LegendsWyrmtideCave[] = INCGFX_U32("data/tilesets/legends_wyrmtide/tiles.png", ".4bpp.fastSmol");
const u16 gMetatiles_LegendsWyrmtideCave[] = INCBIN_U16("data/tilesets/legends_wyrmtide/metatiles.bin");
const u16 gMetatileAttributes_LegendsWyrmtideCave[] = INCBIN_U16("data/tilesets/legends_wyrmtide/metatile_attributes.bin");
const struct Tileset gTileset_LegendsWyrmtideCave = {
    .isCompressed = TRUE, .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsWyrmtideCave, .palettes = gTilesetPalettes_Cave,
    .metatiles = gMetatiles_LegendsWyrmtideCave,
    .metatileAttributes = gMetatileAttributes_LegendsWyrmtideCave,
    .callback = InitTilesetAnim_Cave, .swapPalettes = 0x40,
};

// Dewford shore, with exact native Sealed Chamber inscription cells in free slots.
const u32 gTilesetTiles_LegendsWyrmtideShore[] = INCGFX_U32("data/tilesets/legends_wyrmtide_shore/tiles.png", ".4bpp.fastSmol");
const u16 gMetatiles_LegendsWyrmtideShore[] = INCBIN_U16("data/tilesets/legends_wyrmtide_shore/metatiles.bin");
const u16 gMetatileAttributes_LegendsWyrmtideShore[] = INCBIN_U16("data/tilesets/legends_wyrmtide_shore/metatile_attributes.bin");
const u16 gTilesetPalettes_LegendsWyrmtideShore[][16] = {
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/legends_lights/dewford_night.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/legends_lights/dewford_day.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/dewford/palettes/15.pal", ".gbapal"),
};
const struct Tileset gTileset_LegendsWyrmtideShore = {
    .isCompressed = TRUE, .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsWyrmtideShore, .palettes = gTilesetPalettes_LegendsWyrmtideShore,
    .metatiles = gMetatiles_LegendsWyrmtideShore,
    .metatileAttributes = gMetatileAttributes_LegendsWyrmtideShore,
    .callback = InitTilesetAnim_Dewford, .swapPalettes = 0x40,
};
