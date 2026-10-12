#if !IS_FRLG

const u32 gTilesetTiles_LegendsStoryCinnabarIsland[] = INCGFX_U32("data/tilesets/secondary/cinnabar_island_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStoryCinnabarIsland[][16] =
{
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_island_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStoryCinnabarIsland[] = INCBIN_U16("data/tilesets/secondary/cinnabar_island_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStoryCinnabarIsland[] = INCBIN_U16("data/tilesets/secondary/cinnabar_island_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoCinnabarIsland =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStoryCinnabarIsland,
    .palettes = gTilesetPalettes_LegendsStoryCinnabarIsland,
    .metatiles = gMetatiles_LegendsStoryCinnabarIsland,
    .metatileAttributes = gMetatileAttributes_LegendsStoryCinnabarIsland,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStorySeafoamIslands[] = INCGFX_U32("data/tilesets/secondary/seafoam_islands_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStorySeafoamIslands[][16] =
{
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/seafoam_islands_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStorySeafoamIslands[] = INCBIN_U16("data/tilesets/secondary/seafoam_islands_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStorySeafoamIslands[] = INCBIN_U16("data/tilesets/secondary/seafoam_islands_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoSeafoamIslands =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStorySeafoamIslands,
    .palettes = gTilesetPalettes_LegendsStorySeafoamIslands,
    .metatiles = gMetatiles_LegendsStorySeafoamIslands,
    .metatileAttributes = gMetatileAttributes_LegendsStorySeafoamIslands,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStoryCeruleanCity[] = INCGFX_U32("data/tilesets/secondary/cerulean_city_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStoryCeruleanCity[][16] =
{
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_city_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStoryCeruleanCity[] = INCBIN_U16("data/tilesets/secondary/cerulean_city_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStoryCeruleanCity[] = INCBIN_U16("data/tilesets/secondary/cerulean_city_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoCeruleanCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStoryCeruleanCity,
    .palettes = gTilesetPalettes_LegendsStoryCeruleanCity,
    .metatiles = gMetatiles_LegendsStoryCeruleanCity,
    .metatileAttributes = gMetatileAttributes_LegendsStoryCeruleanCity,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStoryCeruleanGym[] = INCGFX_U32("data/tilesets/secondary/cerulean_gym_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStoryCeruleanGym[][16] =
{
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cerulean_gym_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStoryCeruleanGym[] = INCBIN_U16("data/tilesets/secondary/cerulean_gym_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStoryCeruleanGym[] = INCBIN_U16("data/tilesets/secondary/cerulean_gym_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoCeruleanGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStoryCeruleanGym,
    .palettes = gTilesetPalettes_LegendsStoryCeruleanGym,
    .metatiles = gMetatiles_LegendsStoryCeruleanGym,
    .metatileAttributes = gMetatileAttributes_LegendsStoryCeruleanGym,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStoryCave_Frlg[] = INCGFX_U32("data/tilesets/secondary/cave_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStoryCave_Frlg[][16] =
{
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cave_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStoryCave_Frlg[] = INCBIN_U16("data/tilesets/secondary/cave_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStoryCave_Frlg[] = INCBIN_U16("data/tilesets/secondary/cave_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoCave_Frlg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStoryCave_Frlg,
    .palettes = gTilesetPalettes_LegendsStoryCave_Frlg,
    .metatiles = gMetatiles_LegendsStoryCave_Frlg,
    .metatileAttributes = gMetatileAttributes_LegendsStoryCave_Frlg,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStoryPewterCity[] = INCGFX_U32("data/tilesets/secondary/pewter_city_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStoryPewterCity[][16] =
{
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_city_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStoryPewterCity[] = INCBIN_U16("data/tilesets/secondary/pewter_city_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStoryPewterCity[] = INCBIN_U16("data/tilesets/secondary/pewter_city_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoPewterCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStoryPewterCity,
    .palettes = gTilesetPalettes_LegendsStoryPewterCity,
    .metatiles = gMetatiles_LegendsStoryPewterCity,
    .metatileAttributes = gMetatileAttributes_LegendsStoryPewterCity,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStoryPewterGym[] = INCGFX_U32("data/tilesets/secondary/pewter_gym_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStoryPewterGym[][16] =
{
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pewter_gym_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStoryPewterGym[] = INCBIN_U16("data/tilesets/secondary/pewter_gym_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStoryPewterGym[] = INCBIN_U16("data/tilesets/secondary/pewter_gym_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoPewterGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStoryPewterGym,
    .palettes = gTilesetPalettes_LegendsStoryPewterGym,
    .metatiles = gMetatiles_LegendsStoryPewterGym,
    .metatileAttributes = gMetatileAttributes_LegendsStoryPewterGym,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStoryCinnabarGym[] = INCGFX_U32("data/tilesets/secondary/cinnabar_gym_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStoryCinnabarGym[][16] =
{
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/cinnabar_gym_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStoryCinnabarGym[] = INCBIN_U16("data/tilesets/secondary/cinnabar_gym_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStoryCinnabarGym[] = INCBIN_U16("data/tilesets/secondary/cinnabar_gym_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoCinnabarGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStoryCinnabarGym,
    .palettes = gTilesetPalettes_LegendsStoryCinnabarGym,
    .metatiles = gMetatiles_LegendsStoryCinnabarGym,
    .metatileAttributes = gMetatileAttributes_LegendsStoryCinnabarGym,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStorySeviiIslands123[] = INCGFX_U32("data/tilesets/secondary/sevii_islands_123_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStorySeviiIslands123[][16] =
{
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/sevii_islands_123_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStorySeviiIslands123[] = INCBIN_U16("data/tilesets/secondary/sevii_islands_123_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStorySeviiIslands123[] = INCBIN_U16("data/tilesets/secondary/sevii_islands_123_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoSeviiIslands123 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStorySeviiIslands123,
    .palettes = gTilesetPalettes_LegendsStorySeviiIslands123,
    .metatiles = gMetatiles_LegendsStorySeviiIslands123,
    .metatileAttributes = gMetatileAttributes_LegendsStorySeviiIslands123,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsStoryMtEmber[] = INCGFX_U32("data/tilesets/secondary/mt_ember_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsStoryMtEmber[][16] =
{
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mt_ember_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsStoryMtEmber[] = INCBIN_U16("data/tilesets/secondary/mt_ember_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsStoryMtEmber[] = INCBIN_U16("data/tilesets/secondary/mt_ember_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoMtEmber =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsStoryMtEmber,
    .palettes = gTilesetPalettes_LegendsStoryMtEmber,
    .metatiles = gMetatiles_LegendsStoryMtEmber,
    .metatileAttributes = gMetatileAttributes_LegendsStoryMtEmber,
    .callback = NULL,
};

#endif
