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
#include "pokemon.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/decorations.h"
#include "constants/species.h"
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
    case 8:
        ObjectEventSetGraphicsId(&gObjectEvents[gPlayerAvatar.objectEventId], LegendsGetPlayerGraphicsId(box[10],gSaveBlock2Ptr->playerGender));
        SetMainCallback2(CB2_Overworld);break;
    }
}
