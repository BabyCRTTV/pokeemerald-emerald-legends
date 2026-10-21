#include "global.h"
#include "legends_grottos.h"
#include "legends_seasons.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "field_player_avatar.h"
#include "pokemon.h"
#include "random.h"
#include "script_pokemon_util.h"
#include "string_util.h"
#include "constants/battle.h"
#include "constants/event_objects.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/maps.h"
#include "constants/species.h"
#include "constants/vars.h"

#define DATA (&gSaveBlock3Ptr->grottos)
#define GROTTO_MAGIC 0x3147524C // LRG1
#define GROTTO_VERSION 1
#define VISITOR_LOCAL_ID 1
#define VISITOR_HIDE_FLAG FLAG_TEMP_5
struct GrottoEncounter { u16 species; u8 weight; };
#include "data/legends/grotto_encounters.h"
STATIC_ASSERT(sizeof(struct BoxPokemon) == LEGENDS_GROTTO_BOX_BYTES, GrottoBoxWidth);
STATIC_ASSERT(sizeof(struct LegendsGrottoRoomSave) == 88, GrottoRoomWidth);
STATIC_ASSERT(sizeof(struct LegendsGrottoSave) == 276, GrottoSaveWidth);
static EWRAM_DATA s8 sBattleRoom;

static s32 CurrentRoom(void)
{
    if (gSaveBlock1Ptr->location.mapGroup != MAP_GROUP(MAP_LEGENDS_GROTTO_LEAFSHADE)) return -1;
    switch (gSaveBlock1Ptr->location.mapNum)
    {
    case MAP_NUM(MAP_LEGENDS_GROTTO_LEAFSHADE): return 0;
    case MAP_NUM(MAP_LEGENDS_GROTTO_STILLWATER): return 1;
    case MAP_NUM(MAP_LEGENDS_GROTTO_RAINROOT): return 2;
    default: return -1;
    }
}
static u32 Checksum(void)
{
    const u8 *p = (const u8 *)DATA;
    u32 value = 2166136261u;
    u32 i;
    for (i = 8; i < sizeof(*DATA); i++) value = (value ^ p[i]) * 16777619u;
    return value;
}
static bool32 Valid(void)
{
    u32 i;
    if (DATA->magic != GROTTO_MAGIC || DATA->version != GROTTO_VERSION || DATA->checksum != Checksum()) return FALSE;
    for (i = 0; i < LEGENDS_GROTTO_COUNT; i++)
    {
        const struct LegendsGrottoRoomSave *r = &DATA->rooms[i];
        if (r->state > LEGENDS_GROTTO_COOLDOWN || r->remainingSteps > LEGENDS_GROTTO_REFRESH_STEPS) return FALSE;
        if (r->state == LEGENDS_GROTTO_ACTIVE && (r->season >= 4 || r->species == SPECIES_NONE || r->species >= NUM_SPECIES || r->level < sGrottoLevels[i][0] || r->level > sGrottoLevels[i][1] || r->remainingSteps)) return FALSE;
        if (r->state == LEGENDS_GROTTO_COOLDOWN && !r->remainingSteps) return FALSE;
    }
    return TRUE;
}
static void Sign(void) { DATA->checksum = Checksum(); }
void LegendsGrottoInit(bool32 newGame)
{
    sBattleRoom = -1;
    if (newGame || !Valid())
    {
        memset(DATA, 0, sizeof(*DATA));
        DATA->magic = GROTTO_MAGIC;
        DATA->version = GROTTO_VERSION;
        Sign();
    }
}
static u32 Uniform(u32 max)
{
    u32 roll, limit = (0x10000u / max) * max;
    do { roll = Random(); } while (roll >= limit);
    return roll % max;
}
static void Generate(u8 room)
{
    struct LegendsGrottoRoomSave *r = &DATA->rooms[room];
    u32 season = LegendsGetActiveSeason(), roll = Uniform(100), i;
    if (season >= 4) season = 0;
    memset(r, 0, sizeof(*r));
    r->season = season;
    for (i = 0; i < 5; i++)
    {
        const struct GrottoEncounter *e = &sGrottoEncounters[room][season][i];
        if (roll < e->weight) { r->species = e->species; break; }
        roll -= e->weight;
    }
    r->level = sGrottoLevels[room][0] + Uniform(sGrottoLevels[room][1] - sGrottoLevels[room][0] + 1);
    SetWildShinyGenerationContext(TRUE);
    CreateScriptedWildMon(r->species, r->level, ITEM_NONE);
    SetWildShinyGenerationContext(FALSE);
    memcpy(r->mon, &gParties[B_TRAINER_OPPONENT_A][0].box, sizeof(r->mon));
    r->state = LEGENDS_GROTTO_ACTIVE;
    Sign();
}
void LegendsGrottoPrepareVisitor(void)
{
    s32 room = CurrentRoom();
    struct LegendsGrottoRoomSave *r;
    gSpecialVar_Result = FALSE;
    if (room < 0) return;
    if (!Valid()) LegendsGrottoInit(FALSE);
    r = &DATA->rooms[room];
    if (r->state == LEGENDS_GROTTO_READY) Generate(room);
    if (r->state != LEGENDS_GROTTO_ACTIVE)
    {
        FlagSet(VISITOR_HIDE_FLAG);
        return;
    }
    FlagClear(VISITOR_HIDE_FLAG);
    VarSet(VAR_OBJ_GFX_ID_F, r->species + OBJ_EVENT_MON);
    // Continue restores saved object instances, whose resolved graphics ID may
    // predate the new extension. Resume runs before their sprites are recreated.
    {
        u8 object;
        if (!TryGetObjectEventIdByLocalIdAndMap(VISITOR_LOCAL_ID, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup, &object))
            gObjectEvents[object].graphicsId = r->species + OBJ_EVENT_MON;
    }
    gSpecialVar_0x8004 = r->species;
    StringCopy(gStringVar1, GetSpeciesName(r->species));
    gSpecialVar_Result = TRUE;
}
bool32 LegendsGrottoStartBattle(void)
{
    s32 room = CurrentRoom();
    sBattleRoom = -1;
    gSpecialVar_Result = FALSE;
    if (room < 0 || !Valid() || DATA->rooms[room].state != LEGENDS_GROTTO_ACTIVE) return FALSE;
    ZeroEnemyPartyMons();
    BoxMonToMon((const struct BoxPokemon *)DATA->rooms[room].mon, &gParties[B_TRAINER_OPPONENT_A][0]);
    sBattleRoom = room;
    gSpecialVar_Result = TRUE;
    return TRUE;
}
void LegendsGrottoFinishBattle(u8 outcome)
{
    s32 room = sBattleRoom;
    sBattleRoom = -1;
    if (room < 0 || room != CurrentRoom() || !Valid() || DATA->rooms[room].state != LEGENDS_GROTTO_ACTIVE) return;
    // Only a battle explicitly started by this visitor can consume it. Flee,
    // teleport, forced exit, draw and player defeat preserve its full identity.
    if (outcome != B_OUTCOME_WON && outcome != B_OUTCOME_CAUGHT) return;
    memset(&DATA->rooms[room], 0, sizeof(DATA->rooms[room]));
    DATA->rooms[room].state = LEGENDS_GROTTO_COOLDOWN;
    DATA->rooms[room].remainingSteps = LEGENDS_GROTTO_REFRESH_STEPS;
    Sign();
    FlagSet(VISITOR_HIDE_FLAG);
}
void LegendsGrottoStep(void)
{
    u32 i;
    bool32 changed = FALSE;
    s32 room;
    if (!Valid()) return;
    for (i = 0; i < LEGENDS_GROTTO_COUNT; i++)
    {
        struct LegendsGrottoRoomSave *r = &DATA->rooms[i];
        if (r->state == LEGENDS_GROTTO_COOLDOWN)
        {
            changed = TRUE;
            if (--r->remainingSteps == 0) r->state = LEGENDS_GROTTO_READY;
        }
    }
    if (changed) Sign();
    room = CurrentRoom();
    if (room >= 0 && DATA->rooms[room].state != LEGENDS_GROTTO_COOLDOWN)
    {
        u8 object;
        s16 x, y;
        if (!TryGetObjectEventIdByLocalIdAndMap(VISITOR_LOCAL_ID, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup, &object)) return;
        PlayerGetDestCoords(&x, &y);
        // Avoid creating a solid object on the player's occupied square.
        if (x == 9 + 7 && y == 6 + 7) return;
        LegendsGrottoPrepareVisitor();
        TrySpawnObjectEvent(VISITOR_LOCAL_ID, gSaveBlock1Ptr->location.mapNum, gSaveBlock1Ptr->location.mapGroup);
    }
}
u16 LegendsGrottoRemainingSteps(u8 room)
{
    return room < LEGENDS_GROTTO_COUNT && Valid() ? DATA->rooms[room].remainingSteps : 0;
}
