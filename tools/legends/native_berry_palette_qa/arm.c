// Controlled native fixtures and queries; never shipped in a game ROM.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "legends_clock.h"
#include "pokemon.h"
#include "save.h"
#include "battle.h"
#include "item.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/species.h"
#include "constants/items.h"
#include "constants/vars.h"

#include "berry.h"
#include "sprite.h"
#include "palette.h"
#include "event_object_movement.h"
extern const u16 gObjectEventPal_Npc1[], gObjectEventPal_Npc2[], gObjectEventPal_Npc3[], gObjectEventPal_Npc4[];
#include "legends_seasons.h"
#include "constants/berry.h"
#include "pokeblock.h"
#include "legends_poffin.h"
void qa(void)
{
    volatile u32 *b = (u32 *)0x0203fd00;
    if (b[0] < 4)
    {
        NewGameInitData();
        gSaveBlock2Ptr->optionsTextSpeed = 2;
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        FlagSet(FLAG_LEGENDS_FOLLOWERS_DISABLED);
        FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_SET_WALL_CLOCK);
        FlagSet(FLAG_SYS_POKEMON_GET);
        CreateMonWithIVs(&gParties[B_TRAINER_PLAYER][0],SPECIES_TORCHIC,12,32,OTID_STRUCT_PLAYER_ID,31);
        gPartiesCount[B_TRAINER_PLAYER]=1;
        AddBagItem(ITEM_CHERI_BERRY,3);
        AddBagItem(ITEM_CHESTO_BERRY,2);
        LegendsClockSetManual(12,0);
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
        LegendsSetPlaytimeSeason(b[0]);
        PlantBerryTree(BERRY_TREE_ROUTE_104_ORAN_2, BERRY_ID_ORAN, b[2], TRUE);
        PlantBerryTree(BERRY_TREE_ROUTE_104_SOIL_3, BERRY_ID_CHERI, b[2], TRUE);
        PlantBerryTree(BERRY_TREE_ROUTE_104_PECHA, (b[1] ? BERRY_ID_ASPEAR : BERRY_ID_PECHA), b[2], TRUE);
        SetWarpDestination(MAP_GROUP(MAP_ROUTE104), MAP_NUM(MAP_ROUTE104), -1,23,43);
        WarpIntoMap();
        b[4]=1;
        SetMainCallback2(CB2_LoadMap);
        return;
    }
    if (b[0] == 10)
    {
        const u16 *const palettes[] = {gObjectEventPal_Npc1, gObjectEventPal_Npc2, gObjectEventPal_Npc3, gObjectEventPal_Npc4};
        b[5] = b[6] = 0;
        for (u32 i = 0; i < OBJECT_EVENTS_COUNT; i++)
        {
            struct ObjectEvent *o = &gObjectEvents[i];
            if (!o->active || o->movementType != MOVEMENT_TYPE_BERRY_TREE_GROWTH)
                continue;
            u8 stage = GetStageByBerryTreeId(o->trainerRange_berryTreeId);
            if (!stage) continue;
            u8 berry = GetBerryTypeByBerryTreeId(o->trainerRange_berryTreeId);
            u8 slot = gBerries[berry].berryTreePaletteSlotTable[stage - 1];
            const u16 *expected = palettes[slot - 2];
            u16 offset = (16 + gSprites[o->spriteId].oam.paletteNum) * 16;
            for (u32 j = 1; j < 16; j++)
                if (gPlttBufferUnfaded[offset + j] != expected[j]) b[6]++;
            b[5]++;
        }
    }
    b[4]=1; SetMainCallback2((MainCallback)b[3]);
}
