static const u16 sJohtoPalettes[][16] =
{
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/legends_lights/legends_johto_night.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/legends_lights/legends_johto_day.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/legends_johto/palettes/15.pal", ".gbapal"),
};
static const u32 sJohtoTiles[] = INCGFX_U32("data/tilesets/secondary/legends_johto/tiles.png", ".4bpp.fastSmol");
static const u16 sJohtoMetatiles[] = INCBIN_U16("data/tilesets/secondary/legends_johto/metatiles.bin");
static const u16 sJohtoAttributes[] = INCBIN_U16("data/tilesets/secondary/legends_johto/metatile_attributes.bin");
const struct Tileset gTileset_LegendsJohto =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = sJohtoTiles,
    .palettes = sJohtoPalettes,
    .metatiles = sJohtoMetatiles,
    .metatileAttributes = sJohtoAttributes,
    .swapPalettes = 0x40,
};

// The tower and gyms share their original object IDs and palettes. Loading
// their timber and planting graphics separately frees outdoor VRAM for roofs.
static const u32 sJohtoInteriorTiles[] = INCGFX_U32("data/tilesets/secondary/legends_johto_interior/tiles.png", ".4bpp.fastSmol");
static const u16 sJohtoInteriorMetatiles[] = INCBIN_U16("data/tilesets/secondary/legends_johto_interior/metatiles.bin");
static const u16 sJohtoInteriorAttributes[] = INCBIN_U16("data/tilesets/secondary/legends_johto_interior/metatile_attributes.bin");
const struct Tileset gTileset_LegendsJohtoInterior =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = sJohtoInteriorTiles,
    .palettes = sJohtoPalettes,
    .metatiles = sJohtoInteriorMetatiles,
    .metatileAttributes = sJohtoInteriorAttributes,
    .swapPalettes = 0x40,
};
