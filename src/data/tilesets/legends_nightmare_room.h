// Private room floor; native furniture and all shared tilesets retained.
const u32 gNightmareRoomTiles[] = INCGFX_U32("data/tilesets/legends_nightmare/room/tiles.png", ".4bpp.fastSmol");
const u16 gNightmareRoomMetatiles[] = INCBIN_U16("data/tilesets/legends_nightmare/room/metatiles.bin");
const u16 gNightmareRoomAttributes[] = INCBIN_U16("data/tilesets/legends_nightmare/room/metatile_attributes.bin");
const u16 gNightmareRoomPalettes[][16] = {
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/00.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/01.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/02.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/03.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/04.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/05.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/06.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/07.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/08.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/09.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/10.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/11.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/legends_nightmare/room/12.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/13.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/14.pal", ".gbapal"),
    INCGFX_U16("data/tilesets/secondary/generic_building/palettes/15.pal", ".gbapal"),
};
const struct Tileset gTileset_NightmareHomeInterior = {
    .isCompressed = TRUE, .isSecondary = TRUE, .tiles = gNightmareRoomTiles, .palettes = gNightmareRoomPalettes,
    .metatiles = gNightmareRoomMetatiles, .metatileAttributes = gNightmareRoomAttributes, .callback = NULL,
};
