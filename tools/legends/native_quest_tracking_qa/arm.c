// Controlled native fixtures only. Never included in a distributed ROM.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "save.h"
#include "pokemon.h"
#include "safari_zone.h"
#include "legends_journal.h"
#include "legends_appearance.h"
#include "legends_seasons.h"
#include "legends_settings.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/species.h"
#include "constants/characters.h"
void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    s16 x, y;
    switch (box[0])
    {
    case 0:
        NewGameInitData();
        gSaveBlock2Ptr->playerName[0] = 0xBB; gSaveBlock2Ptr->playerName[1] = EOS;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_LEGENDS_DEXNAV_UNLOCKED); FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        FlagSet(FLAG_RESCUED_BIRCH); FlagSet(FLAG_SET_WALL_CLOCK);
        FlagSet(FLAG_RECEIVED_RUNNING_SHOES); FlagSet(FLAG_DEVON_GOODS_STOLEN);
        FlagSet(FLAG_RECOVERED_DEVON_GOODS);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_1);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_HOUSE_VIGOROTH_2);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 3);
        VarSet(VAR_LITTLEROOT_HOUSES_STATE_BRENDAN, 4);
        LegendsSetAppearanceSelection(3, 3); LegendsApplyAppearanceToNewGame();
        LegendsBeginWardrobeSelection(); LegendsSetHairSelection(2); LegendsSetHairColorSelection(3);
        LegendsSetShoeSelection(4); LegendsApplyWardrobeSelection();
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME); LegendsSetPlaytimeSeason(LEGENDS_WINTER);
        VarSet(VAR_LEGENDS_BEDROOM_COLORS, 0xB423); VarSet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR, 0xCA03);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 15, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        LegendsJournalInit(TRUE); // Version-1 pre-tracking fixture: reserved word is zero.
        SetWarpDestination(MAP_GROUP(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F), MAP_NUM(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F), -1, 1, 7);
        WarpIntoMap(); SetMainCallback2(CB2_LoadMap); box[30] = 1; return;
    case 2:
        box[1] = LegendsQuestTracked(); box[2] = LegendsQuestNextStep(9);
        box[3] = gSaveBlock3Ptr->journal.reserved; box[4] = LegendsQuestComplete(9);
        box[5] = VarGet(VAR_LEGENDS_APPEARANCE); box[6] = VarGet(VAR_LEGENDS_BEDROOM_COLORS);
        box[7] = VarGet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR);
        box[8] = LegendsGetSkinTone(); box[9] = LegendsGetHair(); box[10] = LegendsGetHairColor();
        box[11] = LegendsGetSeasonMode(); box[12] = LegendsGetSeason();
        PlayerGetDestCoords(&x, &y); box[15] = x - MAP_OFFSET; box[16] = y - MAP_OFFSET;
        box[17] = MapGridGetCollisionAt(x, y); break;
    case 3:
        box[13] = TrySavingData(SAVE_NORMAL);
        gSaveBlock3Ptr->journal.reserved = 0;
        VarSet(VAR_LEGENDS_BEDROOM_COLORS, 0); VarSet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR, 0);
        box[14] = LoadGameSave(SAVE_NORMAL); LegendsJournalInit(FALSE); break;
    case 4:
        FlagSet(FLAG_RETURNED_DEVON_GOODS); LegendsJournalRefresh(); break;
    case 5:
        FlagSet(FLAG_DELIVERED_DEVON_GOODS); LegendsJournalRefresh(); break;
    case 6: SetSafariZoneFlag(); break;
    case 7: FlagClear(FLAG_SYS_SAFARI_MODE); break;
    }
    SetMainCallback2((MainCallback)box[31]);
    box[30] = 1;
}
