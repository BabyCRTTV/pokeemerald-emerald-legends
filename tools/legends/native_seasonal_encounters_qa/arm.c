// Private diagnostic callback. Never linked into a downloadable game build.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "task.h"
#include "script.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "wild_encounter.h"
#include "pokemon.h"
#include "pokedex.h"
#include "pokemon_icon.h"
#include "sprite.h"
#include "palette.h"
#include "random.h"
#include "dexnav.h"
#include "legends_seasons.h"
#include "legends_journal.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/characters.h"
#include "constants/pokemon_icon.h"
#include "qa_scenarios.h"
static u32 hash(const void *ptr, u32 size)
{
    const u8 *p = ptr; u32 h = 2166136261u;
    while (size--) h = (h ^ *p++) * 16777619u;
    return h;
}
static void check(bool32 passed, u32 error, volatile u32 *b)
{
    if (!passed && !b[29]) b[29] = error;
}
void qa(void)
{
    volatile u32 *b = (u32 *)0x0203fc00;
    const struct QAScenario *s = &scenarios[b[1]];
    if (b[0] == 0)
    {
        NewGameInitData();
        gSaveBlock2Ptr->playerName[0] = 0xBB; gSaveBlock2Ptr->playerName[1] = EOS;
        gSaveBlock2Ptr->optionsTextSpeed = 2;
        FlagSet(FLAG_SYS_POKEMON_GET); FlagSet(FLAG_SYS_POKEDEX_GET); FlagSet(FLAG_HIDE_MAP_NAME_POPUP);
        FlagSet(FLAG_RESCUED_BIRCH); FlagSet(FLAG_SET_WALL_CLOCK); FlagSet(FLAG_RECEIVED_RUNNING_SHOES);
        FlagSet(FLAG_LEGENDS_DEXNAV_UNLOCKED);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 4);
        CreateMon(&gParties[B_TRAINER_PLAYER][0], SPECIES_TREECKO, 5, 32, OTID_STRUCT_PLAYER_ID);
        gPartiesCount[B_TRAINER_PLAYER] = 1;
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME); LegendsSetPlaytimeSeason(s->season);
        LegendsJournalInit(FALSE);
        SetWarpDestination(MAP_GROUP(s->map), MAP_NUM(s->map), -1, s->x, s->y);
        WarpIntoMap(); b[30] = 1; SetMainCallback2(CB2_LoadMap); return;
    }
    if (b[0] == 1)
    {
        u32 header = GetCurrentMapWildMonHeaderId();
        check(header != HEADER_NONE, 1, b);
        const struct WildPokemonInfo *land = GetLandMonsInfo(header, TIME_OF_DAY_DEFAULT);
        check(land && land->encounterRate == 20, 2, b);
        for (u32 i = 0; i < 12; i++)
            check(land->wildPokemon[i].species == s->expected[i], 3, b);
        // Pending season must not affect current field or menu encounter data.
        LegendsSetPlaytimeSeason((s->season + 1) % 4);
        check(GetLandMonsInfo(header, TIME_OF_DAY_DEFAULT) == land, 4, b);
        if (s->mode != 1)
        {
            const struct WildPokemonInfo *base = gWildMonHeaders[header].encounterTypes[TIME_OF_DAY_DEFAULT].landMonsInfo;
            for (u32 i = 0; i < 12; i++)
                GetSetPokedexFlag(SpeciesToNationalPokedexNum(base->wildPokemon[i].species), FLAG_SET_SEEN);
            if (s->mode == 2)
                for (u32 i = 0; i < 12; i++)
                    GetSetPokedexFlag(SpeciesToNationalPokedexNum(land->wildPokemon[i].species), FLAG_SET_SEEN);
        }
        SeedRng(0x1234); u32 found = 0;
        // Actual compiled wild creation, not a sampling model or hand-made party.
        for (u32 n = 0; n < 256; n++)
        {
            check(TryGenerateWildMon(GetLandMonsInfo(header, GetTimeOfDayForEncounters(header, WILD_AREA_LAND)), WILD_AREA_LAND, 0), 5, b);
            enum Species species = GetMonData(&gParties[B_TRAINER_OPPONENT_A][0], MON_DATA_SPECIES);
            u32 level = GetMonData(&gParties[B_TRAINER_OPPONENT_A][0], MON_DATA_LEVEL), match = 0;
            for (u32 i = 0; i < 12; i++)
                if (land->wildPokemon[i].species == species && level >= land->wildPokemon[i].minLevel && level <= land->wildPokemon[i].maxLevel)
                { match = 1; found |= 1u << i; }
            check(match, 6, b);
        }
        for (u32 i = 0; i < 12; i++) check(found & (1u << i), 7, b);
        b[8] = hash(&gSaveBlock2Ptr->pokedex, sizeof(gSaveBlock2Ptr->pokedex));
        b[9] = hash(&gSaveBlock3Ptr->journal, sizeof(gSaveBlock3Ptr->journal));
        b[10] = hash(&gSaveBlock3Ptr->achievementExtra, sizeof(gSaveBlock3Ptr->achievementExtra));
        b[11] = hash(gSaveBlock1Ptr->vars, sizeof(gSaveBlock1Ptr->vars));
        b[12] = LegendsGetActiveSeason(); b[13] = found;
        gSpecialVar_0x8000 = 0;
        CreateTask(Task_OpenDexNavFromStartMenu, 0);
    }
    else if (b[0] == 2)
    {
        struct DexNavGUI *ui = *(struct DexNavGUI **)QA_UI;
        b[3] = FindTaskIdByFunc((TaskFunc)QA_GUI_TASK) != TASK_NONE;
        b[4] = gPaletteFade.active; b[5] = 0; b[6] = 0; b[7] = 0;
        b[14] = hash(&gSaveBlock2Ptr->pokedex, sizeof(gSaveBlock2Ptr->pokedex));
        b[15] = hash(&gSaveBlock3Ptr->journal, sizeof(gSaveBlock3Ptr->journal));
        b[16] = hash(&gSaveBlock3Ptr->achievementExtra, sizeof(gSaveBlock3Ptr->achievementExtra));
        b[17] = hash(gSaveBlock1Ptr->vars, sizeof(gSaveBlock1Ptr->vars));
        b[18] = LegendsGetActiveSeason();
        s16 x, y; PlayerGetDestCoords(&x, &y); b[19] = MapGridGetCollisionAt(x, y);
        if (b[3] && !b[4])
        {
            b[23] = gSpecialVar_0x8000; // actual search request remains unset for unseen A
            for (u32 i = 0; i < 12; i++)
            {
                enum Species species = ui->landSpecies[i];
                if (species == SPECIES_NONE) continue;
                b[5]++; x = ROW_LAND_ICON_X + 24 * (i % COL_LAND_COUNT); y = ROW_LAND_TOP_ICON_Y + (i >= COL_LAND_COUNT ? 28 : 0);
                struct Sprite *icon = NULL;
                for (u32 j = 0; j < MAX_SPRITES; j++)
                    if (gSprites[j].inUse && gSprites[j].x == x && gSprites[j].y == y && gSprites[j].callback == SpriteCB_MonIcon) icon = &gSprites[j];
                check(icon != NULL, 9, b); if (!icon) continue;
                const u8 *tiles = GetMonIconPtr(species, 0xFFFFFFFF);
                check((const u8 *)icon->images == tiles, 10, b);
                bool32 seen = GetSetPokedexFlag(SpeciesToNationalPokedexNum(species), FLAG_GET_SEEN);
                u32 pal = OBJ_PLTT_ID(icon->oam.paletteNum);
                if (!seen)
                {
                    b[6]++;
                    check(icon->oam.paletteNum == IndexOfSpritePaletteTag(0x4011), 11, b);
                    for (u32 n = 0; n < 16; n++) check(gPlttBufferUnfaded[pal + n] == 0, 12, b);
                    if (!b[7])
                    {
                        b[7] = species;
                        const u8 *vram = (const u8 *)(OBJ_VRAM0 + icon->oam.tileNum * TILE_SIZE_4BPP);
                        b[20] = !memcmp(vram, tiles, 512) ? 1 : !memcmp(vram, tiles + 512, 512) ? 2 : 0;
                        b[21] = memcmp(tiles, tiles + 512, 512) != 0;
                        check(b[20] != 0, 13, b);
                    }
                }
                else
                {
                    check(icon->oam.paletteNum != IndexOfSpritePaletteTag(0x4011), 14, b);
                    check(!memcmp(&gPlttBufferUnfaded[pal], GetValidMonIconPalettePtr(species), PLTT_SIZE_4BPP), 15, b);
                }
            }
            u32 expectedCount = 0;
            for (u32 i = 0; i < 12; i++)
            {
                bool32 duplicate = FALSE;
                for (u32 j = 0; j < i; j++) if (s->expected[i] == s->expected[j]) duplicate = TRUE;
                if (!duplicate) expectedCount++;
            }
            check(b[5] == expectedCount, 16, b);
        }
    }
    b[30] = 1; gMain.callback2 = (MainCallback)b[31];
}
