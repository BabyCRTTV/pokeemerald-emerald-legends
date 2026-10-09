// Reuse upstream Kanto assets with native FRLG tile/palette counts and attribute packing.
#if !IS_FRLG

const u32 gTilesetTiles_LegendsKantoGeneral_Frlg[] = INCGFX_U32("data/tilesets/primary/general_frlg/tiles.png", ".4bpp.smol");

const u16 ALIGNED(4) gTilesetPalettes_LegendsKantoGeneral_Frlg[][16] =
{
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/general_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoGeneral_Frlg[] = INCBIN_U16("data/tilesets/primary/general_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoGeneral_Frlg[] = INCBIN_U16("data/tilesets/primary/general_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoGeneral_Frlg =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_LegendsKantoGeneral_Frlg,
    .palettes = gTilesetPalettes_LegendsKantoGeneral_Frlg,
    .metatiles = gMetatiles_LegendsKantoGeneral_Frlg,
    .metatileAttributes = gMetatileAttributes_LegendsKantoGeneral_Frlg,
    .callback = InitTilesetAnim_General_Frlg,
};

const u32 gTilesetTiles_LegendsKantoVermilionCity[] = INCGFX_U32("data/tilesets/secondary/vermilion_city_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoVermilionCity[][16] =
{
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/vermilion_city_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoVermilionCity[] = INCBIN_U16("data/tilesets/secondary/vermilion_city_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoVermilionCity[] = INCBIN_U16("data/tilesets/secondary/vermilion_city_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoVermilionCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoVermilionCity,
    .palettes = gTilesetPalettes_LegendsKantoVermilionCity,
    .metatiles = gMetatiles_LegendsKantoVermilionCity,
    .metatileAttributes = gMetatileAttributes_LegendsKantoVermilionCity,
    .callback = NULL,
};

#endif
