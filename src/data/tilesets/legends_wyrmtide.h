// Native stone-step pixels use the existing Cave sandstone palette.
const u16 gMetatiles_LegendsWyrmtideCave[] = INCBIN_U16("data/tilesets/legends_wyrmtide/metatiles.bin");
const u16 gMetatileAttributes_LegendsWyrmtideCave[] = INCBIN_U16("data/tilesets/legends_wyrmtide/metatile_attributes.bin");
const struct Tileset gTileset_LegendsWyrmtideCave = {
    .isCompressed = TRUE, .isSecondary = TRUE,
    .tiles = gTilesetTiles_Cave, .palettes = gTilesetPalettes_Cave,
    .metatiles = gMetatiles_LegendsWyrmtideCave,
    .metatileAttributes = gMetatileAttributes_LegendsWyrmtideCave,
    .callback = InitTilesetAnim_Cave, .swapPalettes = 0x40,
};
