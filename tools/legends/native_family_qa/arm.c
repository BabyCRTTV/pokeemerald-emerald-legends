// Diagnostic callback linked into a PRIVATE ROM copy by run.py, never a game build.
#include "global.h"
#include "main.h"
#include "sprite.h"
#include "palette.h"
#include "event_object_movement.h"
#include "legends_appearance.h"
#include "field_weather.h"
#include "field_effect_helpers.h"
#include "event_data.h"
#include "data.h"
#include "constants/event_objects.h"

void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    u32 step = box[0], tone = step % 5, i;
    struct ObjectEvent parent = {0};
    u8 mom, norman, unrelated;
    const struct ObjectEventGraphicsInfo *info;
    if (step >= 10) return;
    ResetSpriteData();
    FreeAllSpritePalettes();
    gWeatherPtr->palProcessingState = 0;
    gWeatherPtr->colorMapIndex = 0;
    gWeatherPtr->currWeather = 0;
    LegendsBeginAppearanceSelection();
    LegendsSetAppearanceSelection(tone, 0);
    LegendsApplyWardrobeSelection();
    LegendsBeginWardrobeSelection();
    LegendsSetAppearanceSelection((tone + 1) % 5, 0);
    LegendsClearAppearanceSelection();
    box[17] = LegendsGetSkinTone();
    box[18] = VarGet(VAR_LEGENDS_APPEARANCE);
    unrelated = CreateVirtualObject(OBJ_EVENT_GFX_FLANNERY, 1, 2, 2, 3, DIR_SOUTH);
    mom = CreateVirtualObject(OBJ_EVENT_GFX_MOM, 2, 4, 2, 3, DIR_SOUTH);
    norman = CreateVirtualObject(OBJ_EVENT_GFX_NORMAN, 3, 6, 2, 3, DIR_SOUTH);
    box[3] = mom; box[4] = norman; box[5] = unrelated;
    box[6] = gSprites[mom].oam.paletteNum;
    box[7] = gSprites[norman].oam.paletteNum;
    box[8] = gSprites[unrelated].oam.paletteNum;
    info = GetObjectEventGraphicsInfo(OBJ_EVENT_GFX_MOM);
    box[9] = (u32)info->images;
    info = GetObjectEventGraphicsInfo(OBJ_EVENT_GFX_NORMAN);
    box[10] = (u32)info->images;
    box[11] = (u32)GetTrainerFrontPicPalette(TRAINER_PIC_LEADER_NORMAN);
    box[12] = LoadObjectEventPalette(OBJ_EVENT_PAL_TAG_LEGENDS_MOM);
    parent.spriteId = mom;
    SetUpReflection(&parent, &gSprites[mom], step / 5);
    parent.spriteId = norman;
    SetUpReflection(&parent, &gSprites[norman], step / 5);
    box[15] = IndexOfSpritePaletteTag(OBJ_EVENT_PAL_TAG_LEGENDS_MOM + 0x800);
    box[16] = IndexOfSpritePaletteTag(OBJ_EVENT_PAL_TAG_LEGENDS_NORMAN + 0x800);
    for (i = 0; i < 11; i++)
    {
        struct SpritePalette pal = {gLegendsMomPalettes[tone], 0x6000 + i};
        LoadSpritePalette(&pal);
    }
    box[13] = LoadObjectEventPalette(OBJ_EVENT_PAL_TAG_LEGENDS_NORMAN);
    box[14] = IndexOfSpritePaletteTag(TAG_NONE);
    box[0] = step + 1;
}
