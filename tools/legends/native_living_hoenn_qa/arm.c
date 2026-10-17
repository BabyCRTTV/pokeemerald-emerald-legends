// PRIVATE diagnostic callback; never linked into a public ROM or save.
#include "global.h"
#include "main.h"
#include "new_game.h"
#include "overworld.h"
#include "event_data.h"
#include "script.h"
#include "task.h"
#include "menu.h"
#include "string_util.h"
#include "fieldmap.h"
#include "field_player_avatar.h"
#include "pokemon_storage_system.h"
#include "legends_storage.h"
#include "legends_journal.h"
#include "legends_seasons.h"
#include "constants/maps.h"
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/characters.h"
#include "constants/script_menu.h"
#include "constants/legends_field_requests.h"
#include "qa_scenarios.h"
static u32 hash(const void *ptr, u32 size)
{
    const u8 *p = ptr; u32 h = 2166136261u;
    while (size--) h = (h ^ *p++) * 16777619u;
    return h;
}
static bool32 equal(const u8 *a, const u8 *b)
{
    while (*a == *b) { if (*a == EOS) return TRUE; a++; b++; }
    return FALSE;
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
        FlagSet(FLAG_RECEIVED_EXP_SHARE); FlagSet(FLAG_RECEIVED_POKENAV);
        FlagSet(FLAG_HIDE_ROUTE_119_TEAM_AQUA);
        FlagClear(FLAG_HIDE_WEATHER_INSTITUTE_1F_WORKERS); FlagClear(FLAG_HIDE_LITTLEROOT_TOWN_FAT_MAN);
        VarSet(VAR_LITTLEROOT_INTRO_STATE, 9); VarSet(VAR_LITTLEROOT_RIVAL_STATE, 4);
        VarSet(VAR_BIRCH_LAB_STATE, 5); VarSet(VAR_DEVON_CORP_3F_STATE, 1);
        VarSet(VAR_LITTLEROOT_HOUSES_STATE_BRENDAN, 4); VarSet(VAR_DEX_UPGRADE_JOHTO_STARTER_STATE, 3);
        VarSet(VAR_WEATHER_INSTITUTE_STATE, s->kind == 2 && s->arg == 0 ? 0 : 1);
        VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, 0xB800); VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
        u32 done = s->kind < 2 && s->arg ? ((1u << s->arg) - 1) : 0;
        if (s->kind == 1) done <<= 18;
        VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, done); VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH, done >> 16);
        if ((s->kind == 3 || s->kind == 6) && s->arg) FlagSet(FLAG_SYS_GAME_CLEAR);
        if (s->kind == 4 && s->arg) FlagSet(FLAG_BADGE01_GET);
        if (s->kind == 4 && s->arg == 2) FlagSet(FLAG_SYS_GAME_CLEAR);
        if (s->kind == 5 && s->arg) FlagSet(FLAG_BADGE06_GET);
        LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
        LegendsSetPlaytimeSeason(s->kind == 2 && s->arg >= 2 ? s->arg - 2 : LEGENDS_SPRING);
        LegendsJournalInit(FALSE);
        SetWarpDestination(MAP_GROUP(s->map), MAP_NUM(s->map), -1, s->x, s->y);
        WarpIntoMap(); b[30] = 1; SetMainCallback2(CB2_LoadMap); return;
    }
    if (b[0] == 1)
    {
        // Deliberately pending next season: bulletin must read the committed visible one.
        if (s->kind == 2 && s->arg >= 2) LegendsSetPlaytimeSeason((s->arg - 1) % 4);
        VarSet(VAR_LAST_TALKED, s->localId);
        ScriptContext_SetupScript(s->entry);
    }
    else if (b[0] == 2)
    {
        u8 task = FindTaskIdByFunc((TaskFunc)QA_MULTI);
        b[3] = ScriptContext_IsEnabled(); b[4] = 0;
        if (task != TASK_NONE) b[4] = gTasks[task].data[7] == MULTI_LEGENDS_BIRCH_MAIN ? 1 : gTasks[task].data[7] == MULTI_LEGENDS_DEVON_MAIN ? 2 : 9;
        b[5] = FindTaskIdByFunc((TaskFunc)QA_YESNO) != TASK_NONE;
        b[6] = equal(gStringVar4, s->expected);
        b[7] = Menu_GetCursorPos();
        b[8] = hash(&gSaveBlock3Ptr->journal, sizeof(gSaveBlock3Ptr->journal));
        b[9] = hash(&gSaveBlock3Ptr->achievementExtra, sizeof(gSaveBlock3Ptr->achievementExtra));
        b[10] = hash(LegendsStoragePCItems(), PC_ITEMS_COUNT * sizeof(struct ItemSlot));
        b[11] = VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE); b[12] = VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE);
        b[13] = VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH); b[14] = VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES);
        b[15] = VarGet(VAR_LEGENDS_ACTIVE_SEASON);
        s16 x, y; PlayerGetDestCoords(&x, &y); b[16] = MapGridGetCollisionAt(x, y);
    }
    b[30] = 1; gMain.callback2 = (MainCallback)b[31];
}
