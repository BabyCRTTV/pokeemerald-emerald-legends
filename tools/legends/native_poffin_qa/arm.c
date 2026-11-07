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

#include "pokeblock.h"
void qa(void)
{
    volatile u32 *b = (u32 *)0x0203ffc0;
    if (b[0] == 0)
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
        SetWarpDestination(MAP_GROUP(MAP_OLDALE_TOWN_POKEMON_CENTER_1F),MAP_NUM(MAP_OLDALE_TOWN_POKEMON_CENTER_1F),-1,9,5);
        WarpIntoMap();
        b[4]=1;
        SetMainCallback2(CB2_LoadMap);
        return;
    }
    if (b[0] == 2)
    {
        b[10] = TrySavingData(SAVE_NORMAL);
        gSaveBlock1Ptr->pokeblocks[0].color = 0;
        b[11] = LoadGameSave(SAVE_NORMAL);
    }
    b[12] = GetMonData(&gParties[B_TRAINER_PLAYER][0],MON_DATA_COOL);
    b[13] = GetMonData(&gParties[B_TRAINER_PLAYER][0],MON_DATA_BEAUTY);
    b[5] = CountTotalItemQuantityInBag(ITEM_CHERI_BERRY);
    b[6] = CountTotalItemQuantityInBag(ITEM_CHESTO_BERRY);
    b[7] = gSaveBlock1Ptr->pokeblocks[0].color;
    b[8] = gSaveBlock1Ptr->pokeblocks[0].spicy;
    b[9] = gSaveBlock1Ptr->pokeblocks[0].dry;
    b[4]=1;
    SetMainCallback2((MainCallback)b[3]);
}
