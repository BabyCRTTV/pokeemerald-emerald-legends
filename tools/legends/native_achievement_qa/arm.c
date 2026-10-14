// Private preview harness: actual field scene, real achievement hooks and menu.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "legends_journal.h"
#include "event_data.h"
#include "menu.h"
#include "sprite.h"
#include "task.h"
#include "pokemon.h"
#include "string_util.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/species.h"

void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    switch (box[0])
    {
    case 0:
        NewGameInitData();
        gSaveBlock2Ptr->playerName[0] = 0xBB;
        gSaveBlock2Ptr->playerName[1] = 0xFF;
        FlagSet(FLAG_SYS_POKEMON_GET);
        FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 5, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        LegendsJournalInit(FALSE); // Quietly backfill initial state, as on Continue.
        SetWarpDestination(MAP_GROUP(MAP_OLDALE_TOWN), MAP_NUM(MAP_OLDALE_TOWN), -1, 8, 8);
        WarpIntoMap();
        SetMainCallback2(CB2_LoadMap);
        break;
    case 1:
        FlagSet(FLAG_RECEIVED_BIKE); // Appended achievement 80, through real event hook.
        box[1] = LegendsAchievementEarned(80);
        box[2] = LegendsAchievementClaimed(80);
        box[3] = (u32)&gSaveBlock3Ptr->journal;
        box[4] = (u32)&gSaveBlock1Ptr->pos;
        SetMainCallback2(CB2_Overworld);
        break;
    case 2:
        CleanupOverworldWindowsAndTilemaps();
        SetMainCallback1(NULL);
        SetMainCallback2(CB2_OpenAchievements);
        break;
    case 3:
        box[1] = LegendsAchievementClaimed(80);
        SetMainCallback2(CB2_OpenAchievements);
        break;
    }
}
