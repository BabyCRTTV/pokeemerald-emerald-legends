// Only the two bed-side floor backgrounds differ from native GenericBuilding.
const u32 gNightmareRoomTiles[] = INCGFX_U32("data/tilesets/legends_nightmare/room/tiles.png", ".4bpp.fastSmol");
const u16 gNightmareRoomMetatiles[] = INCBIN_U16("data/tilesets/legends_nightmare/room/metatiles.bin");
const u16 gNightmareRoomAttributes[] = INCBIN_U16("data/tilesets/legends_nightmare/room/metatile_attributes.bin");
const struct Tileset gTileset_NightmareHomeInterior = {
    .isCompressed = TRUE, .isSecondary = TRUE, .tiles = gNightmareRoomTiles, .palettes = gTilesetPalettes_GenericBuilding,
    .metatiles = gNightmareRoomMetatiles, .metatileAttributes = gNightmareRoomAttributes, .callback = NULL,
};
