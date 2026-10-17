// Private controlled mGBA fixtures. Never linked into a published ROM.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "save.h"
#include "pokemon.h"
#include "pokemon_storage_system.h"
#include "constants/characters.h"
#include "item.h"
#include "legends_journal.h"
#include "legends_storage.h"
#include "legends_appearance.h"
#include "legends_seasons.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/species.h"
#include "constants/vars.h"

static bool32 same(const void *a, const void *b, u16 size)
{
    const u8 *x = a, *y = b;
    while (size--) if (*x++ != *y++) return FALSE;
    return TRUE;
}
static u32 legacyChecksum(void)
{
    const u8 *p = (const u8 *)&gSaveBlock3Ptr->journal;
    u32 hash = 2166136261u, i;
    for (i = 8; i < 36; i++) hash = (hash ^ p[i]) * 16777619u;
    return hash;
}
void qa(void)
{
    volatile u32 *b = (u32 *)0x0203fc00;
    u16 i;
    switch (b[0])
    {
    case 0:
        NewGameInitData();
        gSaveBlock2Ptr->playerName[0] = 0xBB; gSaveBlock2Ptr->playerName[1] = EOS;
        gSaveBlock2Ptr->optionsTextSpeed = 2;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET); FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        FlagSet(FLAG_RESCUED_BIRCH); FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_BIRCH_LAB_STATE, 5);
        LegendsSetAppearanceSelection(3, 3); LegendsApplyAppearanceToNewGame();
        LegendsBeginWardrobeSelection(); LegendsSetHairSelection(2); LegendsSetHairColorSelection(3); LegendsSetShoeSelection(4); LegendsApplyWardrobeSelection();
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME); LegendsSetPlaytimeSeason(LEGENDS_WINTER);
        VarSet(VAR_LEGENDS_BEDROOM_COLORS, 0xB423); VarSet(VAR_LEGENDS_BEDROOM_CHAIR_COLOR, 0xCA03);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 8, 32, OTID_STRUCT_PLAYER_ID); gPartiesCount[B_TRAINER_PLAYER] = 1;
        AddBagItem(ITEM_ORAN_BERRY, 11); memset(LegendsStoragePCItems(), 0, PC_ITEMS_COUNT * sizeof(struct ItemSlot)); AddPCItem(ITEM_POTION, 7);
        SetWarpDestination(MAP_GROUP(MAP_OLDALE_TOWN), MAP_NUM(MAP_OLDALE_TOWN), -1, 8, 8);
        WarpIntoMap(); SetMainCallback2(CB2_LoadMap); b[30] = 1; return;
    case 1:
    {
        // Format-identical v0.0.59 journal, with unused tail/bit 95 full of garbage.
        struct LegendsJournalSave *j = &gSaveBlock3Ptr->journal;
        memset(j, 0, sizeof(*j)); j->magic = 0x4C514143; j->version = 1; j->reserved = 0xA702;
        j->earned[0] = j->claimed[0] = 1;
        j->earned[11] = j->claimed[11] = 0xC0; j->checksum = legacyChecksum();
        memset(&gSaveBlock3Ptr->achievementExtra, 0xA5, sizeof(gSaveBlock3Ptr->achievementExtra));
        VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, 0xB800); VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, 0xFFFF); VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH, 0x3FFF); VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
        LegendsJournalInit(FALSE);
        b[1] = LegendsAchievementEarned(0) && LegendsAchievementClaimed(0) && LegendsAchievementEarned(94) && LegendsAchievementClaimed(94);
        b[2] = LegendsQuestTracked() == 1 && LegendsAchievementNotice() == 0xFFFF;
        b[3] = 1;
        for (i = 95; i <= 104; i++) if (!LegendsAchievementEarned(i) || LegendsAchievementClaimed(i)) b[3] = 0;
        for (i = 105; i < 130; i++) if (LegendsAchievementEarned(i) || LegendsAchievementClaimed(i)) b[3] = 0;
        break;
    }
    case 2:
    {
        struct LegendsJournalSave journal = gSaveBlock3Ptr->journal;
        struct LegendsAchievementExtraSave extra = gSaveBlock3Ptr->achievementExtra;
        b[4] = TrySavingData(SAVE_NORMAL);
        memset(gSaveBlock3Ptr, 0, sizeof(*gSaveBlock3Ptr));
        b[5] = LoadGameSave(SAVE_NORMAL); LegendsJournalInit(FALSE);
        b[6] = same(&journal, &gSaveBlock3Ptr->journal, sizeof(journal)) && same(&extra, &gSaveBlock3Ptr->achievementExtra, sizeof(extra));
        b[7] = LegendsGetSkinTone() == 3 && LegendsGetHair() == 2 && LegendsGetHairColor() == 3 && LegendsGetSeason() == LEGENDS_WINTER;
        b[8] = CheckBagHasItem(ITEM_ORAN_BERRY, 11) && CheckPCHasItem(ITEM_POTION, 7) && GetMonData(&gParties[B_TRAINER_PLAYER][0], MON_DATA_SPECIES) == SPECIES_TREECKO;
        b[9] = LegendsQuestTracked() == 1 && VarGet(VAR_LEGENDS_BEDROOM_COLORS) == 0xB423 && VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH) == 0x3FFF;
        break;
    }
    case 3:
        b[10] = LegendsAchievementEarned(129); b[11] = LegendsAchievementClaimed(129);
        b[12] = CheckPCHasItem(ITEM_CHARTI_BERRY, 3); b[13] = CheckPCHasItem(ITEM_CHARTI_BERRY, 6);
        b[14] = (u32)gSaveBlock3Ptr; b[15] = (u8 *)LegendsStoragePCItems() - (u8 *)gPokemonStoragePtr;
        b[16] = (u8 *)gSaveBlock1Ptr->vars - (u8 *)gSaveBlock1Ptr;
        break;
    case 4:
        CleanupOverworldWindowsAndTilemaps(); SetMainCallback1(NULL); SetMainCallback2(CB2_OpenAchievements); b[30] = 1; return;
    case 5:
        FlagSet(FLAG_RECEIVED_REVIVED_FOSSIL_MON); b[10] = LegendsAchievementEarned(129); b[11] = LegendsAchievementClaimed(129); break;
    case 6:
    {
        struct ItemSlot *pc = LegendsStoragePCItems(); u16 item = 1;
        for (i = 0; i < PC_ITEMS_COUNT; i++) { if (item == ITEM_CHARTI_BERRY) item++; pc[i].itemId = item++; pc[i].quantity = 999; }
        break;
    }
    case 7:
        memset(LegendsStoragePCItems(), 0, PC_ITEMS_COUNT * sizeof(struct ItemSlot)); AddPCItem(ITEM_POTION, 7); break;
    }
    b[30] = 1; gMain.callback2 = (MainCallback)b[31];
}
