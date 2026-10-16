// Private controlled fixtures; never linked into a distributed ROM.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "save.h"
#include "script.h"
#include "task.h"
#include "item.h"
#include "pokemon.h"
#include "pokedex.h"
#include "legends_storage.h"
#include "legends_field_requests.h"
#include "legends_journal.h"
#include "legends_appearance.h"
#include "legends_seasons.h"
#include "legends_settings.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/species.h"
#include "constants/moves.h"
#include "constants/items.h"
#include "constants/pokedex.h"
#include "constants/script_menu.h"
#include "constants/characters.h"
#include "config/overworld.h"
extern const u8 LittlerootTown_ProfessorBirchsLab_EventScript_GivePokedex[];
static void lab(bool32 intro)
{
    CleanupOverworldWindowsAndTilemaps(); ResetTasks();
    FlagClear(FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_BIRCH);
    FlagClear(FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_UNKNOWN_0x380);
    if (intro) FlagClear(FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_RIVAL);
    else FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_BIRCHS_LAB_RIVAL);
    SetWarpDestination(MAP_GROUP(MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB), MAP_NUM(MAP_LITTLEROOT_TOWN_PROFESSOR_BIRCHS_LAB), -1, 6, 5);
    WarpIntoMap(); SetMainCallback2(CB2_LoadMap);
}
void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    s16 x, y;
    u16 id;
    u8 task;
    switch (box[0])
    {
    case 0: case 8:
        NewGameInitData();
        gSaveBlock2Ptr->playerName[0] = 0xBB; gSaveBlock2Ptr->playerName[1] = EOS;
        gSaveBlock2Ptr->optionsTextSpeed = 2;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        FlagSet(FLAG_RESCUED_BIRCH); FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
        if (!box[0]) {FlagSet(FLAG_SYS_POKEDEX_GET); FlagSet(FLAG_SYS_NATIONAL_DEX);}
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 4);
        VarSet(VAR_BIRCH_LAB_STATE, 5); VarSet(VAR_LITTLEROOT_HOUSES_STATE_BRENDAN, 4);
        LegendsSetAppearanceSelection(3, 3); LegendsApplyAppearanceToNewGame();
        LegendsBeginWardrobeSelection(); LegendsSetHairSelection(2); LegendsSetHairColorSelection(3);
        LegendsSetShoeSelection(4); LegendsApplyWardrobeSelection();
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME); LegendsSetPlaytimeSeason(LEGENDS_WINTER);
        VarSet(VAR_LEGENDS_BEDROOM_COLORS, 0xB423); VarSet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR, 0xCA03);
        VarSet(VAR_LEGENDS_HOMECOMING_MEMORY, 0xD666);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 8, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        // Format-identical pre-feature fixture: unused vars contain legacy garbage.
        VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, 0xFFFF);
        VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, 0xFFFF);
        VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0xFFFF);
        LegendsJournalInit(TRUE);
        AddBagItem(ITEM_ORAN_BERRY, 3);
        lab(box[0] == 8); box[30] = 1; return;
    case 1:
        box[1] = LegendsFieldRequestActive(); box[2] = VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE);
        box[3] = VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE); box[4] = VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES);
        box[5] = LegendsQuestTracked(); box[6] = ScriptContext_IsEnabled(); box[7] = 0;
        task = FindTaskIdByFunc((TaskFunc)box[29]);
        if (task != TASK_NONE)
        {
            u16 choice = gTasks[task].data[7];
            if (choice == MULTI_LEGENDS_BIRCH_MAIN) box[7] = 1;
            else if (choice == MULTI_LEGENDS_BIRCH_REQUESTS) box[7] = 2;
            else if (choice == MULTI_LEGENDS_BIRCH_ACTIVE) box[7] = 3;
            else box[7] = 9;
        }
        box[8] = FuncIsActiveTask((TaskFunc)box[28]);
        box[9] = VarGet(VAR_LEGENDS_APPEARANCE); box[10] = LegendsGetSkinTone();
        box[11] = LegendsGetHair(); box[12] = LegendsGetHairColor(); box[13] = LegendsGetSeasonMode(); box[14] = LegendsGetSeason();
        PlayerGetDestCoords(&x, &y); box[17] = x - MAP_OFFSET; box[18] = y - MAP_OFFSET;
        box[19] = MapGridGetCollisionAt(x, y); box[20] = OW_FLAG_NO_COLLISION && FlagGet(OW_FLAG_NO_COLLISION);
        box[21] = CheckBagHasItem(ITEM_ORAN_BERRY, 3); box[22] = FlagGet(FLAG_SYS_POKEDEX_GET);
        box[23] = CheckPCHasItem(ITEM_SUPER_POTION, 2);
        box[24] = (u8 *)&gSaveBlock1Ptr->vars - (u8 *)gSaveBlock1Ptr;
        box[25] = (u8 *)&gSaveBlock3Ptr->journal - (u8 *)gSaveBlock3Ptr;
        break;
    case 2:
        box[15] = TrySavingData(SAVE_NORMAL);
        VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, 0); VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, 0); VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
        VarSet(VAR_LEGENDS_BEDROOM_COLORS, 0); VarSet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR, 0);
        box[16] = LoadGameSave(SAVE_NORMAL); LegendsJournalInit(FALSE); break;
    case 3:
        LegendsFieldRequestAbandon();
        VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, 0); VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, 0); VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
        LegendsJournalRefresh(); break;
    case 4:
        id = box[26]; box[27] = LegendsFieldRequestAccept(id);
        if (id == FIELD_REQUEST_FOREST || id == FIELD_REQUEST_COAST)
        {
            CreateMon(&gParties[B_TRAINER_PLAYER][0], id == FIELD_REQUEST_FOREST ? SPECIES_WURMPLE : SPECIES_WINGULL, 8, 32, OTID_STRUCT_PLAYER_ID);
            gPartiesCount[B_TRAINER_PLAYER] = 1;
            CleanupOverworldWindowsAndTilemaps(); ResetTasks();
            u16 map = id == FIELD_REQUEST_FOREST ? MAP_PETALBURG_WOODS : MAP_ROUTE104;
            SetWarpDestination(MAP_GROUP(map), MAP_NUM(map), 0, 0, 0); WarpIntoMap();
            SetMainCallback2(CB2_LoadMap); box[30] = 1; return;
        }
        break;
    case 5:
        lab(FALSE); box[30] = 1; return;
    case 6:
    {
        struct ItemSlot *pc = LegendsStoragePCItems();
        u16 item = 1;
        for (id = 0; id < PC_ITEMS_COUNT; id++)
        {
            if (item == ITEM_SUPER_POTION) item++;
            pc[id].itemId = item++; pc[id].quantity = 1;
        }
        break;
    }
    case 7:
        memset(LegendsStoragePCItems(), 0, sizeof(struct ItemSlot) * PC_ITEMS_COUNT); break;
    case 9:
        ScriptContext_SetupScript(LittlerootTown_ProfessorBirchsLab_EventScript_GivePokedex); break;
    }
    SetMainCallback2((MainCallback)box[31]); box[30] = 1;
}
