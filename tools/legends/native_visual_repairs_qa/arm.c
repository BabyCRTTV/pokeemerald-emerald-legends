// Controlled QA callback, linked only into a private emulator ROM copy.
#include "global.h"
#include "main.h"
#include "legends_appearance.h"
#include "legends_clock.h"
#include "legends_wardrobe.h"
#include "trainer_card.h"
#include "field_weather.h"
#include "palette.h"
#include "sprite.h"
#include "event_object_movement.h"
#include "constants/rtc.h"
#include "new_game.h"
#include "overworld.h"
#include "fieldmap.h"
#include "event_data.h"
#include "legends_journal.h"
#include "legends_bedroom.h"
#include "decoration.h"
#include "decoration_inventory.h"
#include "task.h"
#include "save.h"
#include "item.h"
#include "item_menu.h"
#include "legends_storage.h"
#include "pokemon_storage_system.h"
#include "pokemon.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/decorations.h"
#include "constants/species.h"
void CB2_BagMenuRun(void); // Existing production callback; private QA only.
static void room(void)
{
    SetWarpDestination(MAP_GROUP(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F),
        gSaveBlock2Ptr->playerGender ? MAP_NUM(MAP_LITTLEROOT_TOWN_MAYS_HOUSE_2F) : MAP_NUM(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F), -1, 4, 4);
    WarpIntoMap(); SetMainCallback2(CB2_LoadMap);
}
void qa(void)
{
    volatile u32 *box = (u32 *)0x0203fc00;
    switch (box[0])
    {
    case 0: case 1:
        NewGameInitData(); gSaveBlock2Ptr->playerGender = box[0];
        gSaveBlock2Ptr->playerName[0] = 0xBB; gSaveBlock2Ptr->playerName[1] = 0xFF;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET);
        FlagSet(FLAG_HIDE_MAP_NAME_POPUP); FlagSet(FLAG_RESCUED_BIRCH);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_SWABLU_DOLL);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F_POKE_BALL);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_POKE_BALL);
        FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_MAYS_HOUSE_2F_PICHU_DOLL);
        FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_HIDE_LITTLEROOT_TOWN_PLAYERS_BEDROOM_MOM);
        FlagSet(FLAG_BADGE01_GET); FlagSet(FLAG_BADGE05_GET); FlagSet(FLAG_SYS_GAME_CLEAR);
        FlagSet(FLAG_LEGENDS_KANTO_SURVEY_REPORT); FlagSet(FLAG_LEGENDS_FINAL_HOENN_EPILOGUE);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 3);
        VarSet(VAR_BIRCH_LAB_STATE, 2);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 5, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        DecorationAdd(DECOR_PIKACHU_DOLL);
        LegendsJournalInit(FALSE); LegendsClockSetManual(12,0);
        LegendsBeginWardrobeSelection();
        LegendsSetAppearanceSelection(0,3);
        LegendsSetHairSelection(5); LegendsSetHairColorSelection(6);
        LegendsSetShoeSelection(1); LegendsApplyWardrobeSelection();
        room(); break;
    case 2:
        ShowPlayerTrainerCard(CB2_ReturnToFieldContinueScriptPlayMapMusic); break;
    case 3:
        LegendsOpenWardrobe(); SetMainCallback2(CB2_Overworld); break;
    case 4:
        CleanupOverworldWindowsAndTilemaps(); ResetTasks(); room(); break;
    case 5: case 6:
        LegendsClockSetManual(box[0]==5 ? 12 : 22,0);
        CleanupOverworldWindowsAndTilemaps(); ResetTasks();
        SetWarpDestination(MAP_GROUP(MAP_FALLARBOR_TOWN), MAP_NUM(MAP_FALLARBOR_TOWN), -1, 17, 6);
        WarpIntoMap(); SetMainCallback2(CB2_LoadMap); break;
    case 7:
        {
            u32 i, errors=0;
            u8 slot=gSprites[gPlayerAvatar.spriteId].oam.paletteNum;
            const u16 *pal=box[10] == 4 ? gLegendsUnderwaterPalettes[gSaveBlock2Ptr->playerGender] : gLegendsOverworldPalettes[gSaveBlock2Ptr->playerGender];
            for (i=1;i<16;i++) if (gPlttBufferUnfaded[OBJ_PLTT_ID(slot)+i]!=pal[i]) errors++;
            box[2]=errors;box[3]=slot;box[4]=GetSpritePaletteTagByPaletteNum(slot);
        }
        SetMainCallback2(CB2_Overworld); break;
    case 9:
        {
            static const u16 ids[]={VAR_LEGENDS_APPEARANCE,VAR_LEGENDS_ACCESSORIES,VAR_LEGENDS_COSTUME,VAR_LEGENDS_SHOES,VAR_LEGENDS_CARD_COLOR,VAR_LEGENDS_HAIR,VAR_LEGENDS_LEGGINGS,VAR_LEGENDS_BEDROOM_COLORS,VAR_LEGENDS_BEDROOM_CHAIR_COLOR};
            u16 values[ARRAY_COUNT(ids)]; u32 i;
            for(i=0;i<ARRAY_COUNT(ids);i++)values[i]=VarGet(ids[i]);
            box[5]=TrySavingData(SAVE_NORMAL);
            box[6]=VarGet(VAR_LEGENDS_APPEARANCE);
            for(i=0;i<ARRAY_COUNT(ids);i++)VarSet(ids[i],0);
            box[7]=LoadGameSave(SAVE_NORMAL);
            box[8]=VarGet(VAR_LEGENDS_APPEARANCE);box[9]=0;
            for(i=0;i<ARRAY_COUNT(ids);i++)if(VarGet(ids[i])!=values[i])box[9]++;
        }
        SetMainCallback2(CB2_Overworld);break;
    case 10: case 13:
        {
            u32 i, p, legacy = box[0] == 13, errors = 0;
            static const u16 items[] = {ITEM_POTION, ITEM_POKE_BALL, ITEM_TM_FOCUS_PUNCH, ITEM_ORAN_BERRY, ITEM_LUNAR_WING};
            static const u16 counts[] = {150,32,128,80,60};
            ClearBag();
            for (p = 0; p < POCKETS_COUNT; p++)
                for (i = 0; i < (legacy ? counts[p] : p == 0 ? 600 : 1); i++)
                    BagPocket_SetSlotData(&gBagPockets[p], i, (struct ItemSlot){items[p], p == 4 ? 1 : 77});
            BagPocket_SetSlotData(&gBagPockets[0], legacy ? 149 : 599, (struct ItemSlot){ITEM_ETHER,77});
            BagPocket_SetSlotData(&gBagPockets[4], 0, (struct ItemSlot){ITEM_EXP_SHARE,1});
            if (!legacy) AddBagItem(ITEM_LUNAR_WING,1);
            LegendsStoragePCItems()[149] = (struct ItemSlot){ITEM_MASTER_BALL,1};
            box[11] = TrySavingData(SAVE_NORMAL);
            ClearBag();
            box[12] = LoadGameSave(SAVE_NORMAL);
            for (p = 0; p < POCKETS_COUNT; p++)
            {
                u32 expected = legacy ? counts[p] : p == 0 ? 600 : p == 4 ? 2 : 1;
                if (LegendsStorageBag()->pocketSizes[p] != expected) errors++;
            }
            if (GetBagItemId(0,legacy ? 149 : 599) != ITEM_ETHER || GetBagItemQuantity(0,legacy ? 149 : 599) != 77) errors++;
            if (LegendsStoragePCItems()[149].itemId != ITEM_MASTER_BALL) errors++;
            box[13] = errors;
            box[14] = offsetof(struct PokemonStorage,inventory);
            box[15] = sizeof(struct Bag);
            box[16] = offsetof(struct BagPosition,cursorPosition);
            box[17] = offsetof(struct BagPosition,scrollPosition);
            box[18] = ITEM_ETHER;
            box[21] = offsetof(struct SaveBlock2,encryptionKey);
        }
        SetMainCallback2(CB2_Overworld);break;
    case 11:
        gBagPosition.scrollPosition[POCKET_ITEMS] = 592;
        gBagPosition.cursorPosition[POCKET_ITEMS] = 7;
        GoToBagMenu(ITEMMENULOCATION_FIELD,POCKET_ITEMS,CB2_ReturnToField);break;
    case 12:
        box[19] = GetItemListPosition(POCKET_ITEMS);
        box[20] = gSpecialVar_ItemId;
        SetMainCallback2(CB2_BagMenuRun);break;
    case 8:
        ObjectEventSetGraphicsId(&gObjectEvents[gPlayerAvatar.objectEventId], LegendsGetPlayerGraphicsId(box[10],gSaveBlock2Ptr->playerGender));
        SetMainCallback2(CB2_Overworld);break;
    }
}
