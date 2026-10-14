#include "global.h"
#include "legends_appearance.h"
#include "constants/event_objects.h"

#include "data/legends/family_palettes.h"

// Derived from the player's existing choice. No parent fields or palette RAM cache.
const u16 *LegendsGetFamilyPalette(u16 tag, const u16 *original)
{
    if (tag == OBJ_EVENT_PAL_TAG_LEGENDS_MOM)
        return gLegendsMomPalettes[LegendsGetSkinTone()];
    if (tag == OBJ_EVENT_PAL_TAG_LEGENDS_NORMAN)
        return gLegendsNormanPalettes[LegendsGetSkinTone()];
    return original;
}

const u16 *LegendsGetFamilyTrainerPalette(enum TrainerPicID pic, const u16 *original)
{
    if (pic == TRAINER_PIC_LEADER_NORMAN)
        return gLegendsNormanBattlePalettes[LegendsGetSkinTone()];
    return original;
}
