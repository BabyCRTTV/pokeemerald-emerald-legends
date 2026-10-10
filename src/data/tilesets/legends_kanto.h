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

const u32 gTilesetTiles_LegendsKantoBuilding_Frlg[] = INCGFX_U32("data/tilesets/primary/building_frlg/tiles.png", ".4bpp.smol");

const u16 gTilesetPalettes_LegendsKantoBuilding_Frlg[][16] =
{
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/primary/building_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoBuilding_Frlg[] = INCBIN_U16("data/tilesets/primary/building_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoBuilding_Frlg[] = INCBIN_U16("data/tilesets/primary/building_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoBuildingFrlg =
{
    .isCompressed = TRUE,
    .isSecondary = FALSE,
    .tiles = gTilesetTiles_LegendsKantoBuilding_Frlg,
    .palettes = gTilesetPalettes_LegendsKantoBuilding_Frlg,
    .metatiles = gMetatiles_LegendsKantoBuilding_Frlg,
    .metatileAttributes = gMetatileAttributes_LegendsKantoBuilding_Frlg,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoFanClubDaycare[] = INCGFX_U32("data/tilesets/secondary/fan_club_daycare_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoFanClubDaycare[][16] =
{
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fan_club_daycare_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoFanClubDaycare[] = INCBIN_U16("data/tilesets/secondary/fan_club_daycare_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoFanClubDaycare[] = INCBIN_U16("data/tilesets/secondary/fan_club_daycare_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoFanClubDaycare =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoFanClubDaycare,
    .palettes = gTilesetPalettes_LegendsKantoFanClubDaycare,
    .metatiles = gMetatiles_LegendsKantoFanClubDaycare,
    .metatileAttributes = gMetatileAttributes_LegendsKantoFanClubDaycare,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoFuchsiaCity[] = INCGFX_U32("data/tilesets/secondary/fuchsia_city_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoFuchsiaCity[][16] =
{
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_city_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoFuchsiaCity[] = INCBIN_U16("data/tilesets/secondary/fuchsia_city_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoFuchsiaCity[] = INCBIN_U16("data/tilesets/secondary/fuchsia_city_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoFuchsiaCity =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoFuchsiaCity,
    .palettes = gTilesetPalettes_LegendsKantoFuchsiaCity,
    .metatiles = gMetatiles_LegendsKantoFuchsiaCity,
    .metatileAttributes = gMetatileAttributes_LegendsKantoFuchsiaCity,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoFuchsiaGym[] = INCGFX_U32("data/tilesets/secondary/fuchsia_gym_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoFuchsiaGym[][16] =
{
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/fuchsia_gym_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoFuchsiaGym[] = INCBIN_U16("data/tilesets/secondary/fuchsia_gym_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoFuchsiaGym[] = INCBIN_U16("data/tilesets/secondary/fuchsia_gym_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoFuchsiaGym =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoFuchsiaGym,
    .palettes = gTilesetPalettes_LegendsKantoFuchsiaGym,
    .metatiles = gMetatiles_LegendsKantoFuchsiaGym,
    .metatileAttributes = gMetatileAttributes_LegendsKantoFuchsiaGym,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoGenericBuilding1[] = INCGFX_U32("data/tilesets/secondary/generic_building_1_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoGenericBuilding1[][16] =
{
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_1_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoGenericBuilding1[] = INCBIN_U16("data/tilesets/secondary/generic_building_1_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoGenericBuilding1[] = INCBIN_U16("data/tilesets/secondary/generic_building_1_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoGenericBuilding1 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoGenericBuilding1,
    .palettes = gTilesetPalettes_LegendsKantoGenericBuilding1,
    .metatiles = gMetatiles_LegendsKantoGenericBuilding1,
    .metatileAttributes = gMetatileAttributes_LegendsKantoGenericBuilding1,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoGenericBuilding2[] = INCGFX_U32("data/tilesets/secondary/generic_building_2_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoGenericBuilding2[][16] =
{
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building_2_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoGenericBuilding2[] = INCBIN_U16("data/tilesets/secondary/generic_building_2_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoGenericBuilding2[] = INCBIN_U16("data/tilesets/secondary/generic_building_2_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoGenericBuilding2 =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoGenericBuilding2,
    .palettes = gTilesetPalettes_LegendsKantoGenericBuilding2,
    .metatiles = gMetatiles_LegendsKantoGenericBuilding2,
    .metatileAttributes = gMetatileAttributes_LegendsKantoGenericBuilding2,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoLavenderTown[] = INCGFX_U32("data/tilesets/secondary/lavender_town_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoLavenderTown[][16] =
{
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/lavender_town_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoLavenderTown[] = INCBIN_U16("data/tilesets/secondary/lavender_town_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoLavenderTown[] = INCBIN_U16("data/tilesets/secondary/lavender_town_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoLavenderTown =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoLavenderTown,
    .palettes = gTilesetPalettes_LegendsKantoLavenderTown,
    .metatiles = gMetatiles_LegendsKantoLavenderTown,
    .metatileAttributes = gMetatileAttributes_LegendsKantoLavenderTown,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoMart[] = INCGFX_U32("data/tilesets/secondary/mart_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoMart[][16] =
{
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/mart_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoMart[] = INCBIN_U16("data/tilesets/secondary/mart_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoMart[] = INCBIN_U16("data/tilesets/secondary/mart_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoMart =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoMart,
    .palettes = gTilesetPalettes_LegendsKantoMart,
    .metatiles = gMetatiles_LegendsKantoMart,
    .metatileAttributes = gMetatileAttributes_LegendsKantoMart,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoMuseum[] = INCGFX_U32("data/tilesets/secondary/museum_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoMuseum[][16] =
{
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/museum_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoMuseum[] = INCBIN_U16("data/tilesets/secondary/museum_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoMuseum[] = INCBIN_U16("data/tilesets/secondary/museum_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoMuseum =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoMuseum,
    .palettes = gTilesetPalettes_LegendsKantoMuseum,
    .metatiles = gMetatiles_LegendsKantoMuseum,
    .metatileAttributes = gMetatileAttributes_LegendsKantoMuseum,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoPokemonCenter_Frlg[] = INCGFX_U32("data/tilesets/secondary/pokemon_center_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoPokemonCenter_Frlg[][16] =
{
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/pokemon_center_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoPokemonCenter_Frlg[] = INCBIN_U16("data/tilesets/secondary/pokemon_center_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoPokemonCenter_Frlg[] = INCBIN_U16("data/tilesets/secondary/pokemon_center_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoPokemonCenterFrlg =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoPokemonCenter_Frlg,
    .palettes = gTilesetPalettes_LegendsKantoPokemonCenter_Frlg,
    .metatiles = gMetatiles_LegendsKantoPokemonCenter_Frlg,
    .metatileAttributes = gMetatileAttributes_LegendsKantoPokemonCenter_Frlg,
    .callback = NULL,
};

const u32 gTilesetTiles_LegendsKantoSafariZoneBuilding[] = INCGFX_U32("data/tilesets/secondary/safari_zone_building_frlg/tiles.png", ".4bpp.fastSmol");

const u16 gTilesetPalettes_LegendsKantoSafariZoneBuilding[][16] =
{
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/safari_zone_building_frlg/palettes/15.pal", ".gbapal"),
};

const u16 gMetatiles_LegendsKantoSafariZoneBuilding[] = INCBIN_U16("data/tilesets/secondary/safari_zone_building_frlg/metatiles.bin");

const u16 gMetatileAttributes_LegendsKantoSafariZoneBuilding[] = INCBIN_U16("data/tilesets/secondary/safari_zone_building_frlg/metatile_attributes.bin");

const struct Tileset gTileset_LegendsKantoSafariZoneBuilding =
{
    .isCompressed = TRUE,
    .isSecondary = TRUE,
    .tiles = gTilesetTiles_LegendsKantoSafariZoneBuilding,
    .palettes = gTilesetPalettes_LegendsKantoSafariZoneBuilding,
    .metatiles = gMetatiles_LegendsKantoSafariZoneBuilding,
    .metatileAttributes = gMetatileAttributes_LegendsKantoSafariZoneBuilding,
    .callback = NULL,
};

#endif
