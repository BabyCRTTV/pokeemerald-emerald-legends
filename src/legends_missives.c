#include "global.h"
#include "event_data.h"
#include "item.h"
#include "legends_journal.h"
#include "overworld.h"
#include "pokemon.h"
#include "string_util.h"
#include "wild_encounter.h"
#include "constants/items.h"
#include "constants/legends_missives.h"
#include "constants/maps.h"
#include "constants/species.h"

struct Missive
{
    u16 item, needed, species, reward, quantity;
    const u8 *notice, *reminder, *thanks;
};

static const struct Missive sJobs[] =
{
    [MISSIVE_TRAIL_KIT] = {
        .item = ITEM_POTION, .needed = 1, .reward = ITEM_POKE_BALL, .quantity = 3,
        .notice = COMPOUND_STRING("My little sister starts Route 101\ntomorrow. Her first-aid tin is empty.\pBring me one POTION at OLDALE MART.\nI'll trade you 3 POKé BALLS.\pSigned, Finn, the boy by the shelf."),
        .reminder = COMPOUND_STRING("Have you got a POTION for the tin?"),
        .thanks = COMPOUND_STRING("A perfect fit! I'll tuck a note from\nher big brother under the lid."),
    },
    [MISSIVE_TRACKS] = {
        .species = SPECIES_ZIGZAGOON, .reward = ITEM_POTION, .quantity = 2,
        .notice = COMPOUND_STRING("The tracks by my house zig AND zag.\nHow many feet does this thing have?\pShow me a ZIGZAGOON in OLDALE.\nI'll give you 2 POTIONS.\pSigned, Nell, the girl outdoors."),
        .reminder = COMPOUND_STRING("I'd like to see a ZIGZAGOON's paws.\nBring one along so I can draw them."),
        .thanks = COMPOUND_STRING("Four paws! It just changes its mind\na lot. That explains my tracks!"),
    },
    [MISSIVE_WOODS] = {
        .item = ITEM_ANTIDOTE, .needed = 2, .reward = ITEM_GREAT_BALL, .quantity = 2,
        .notice = COMPOUND_STRING("Taking two new Trainers through\nPETALBURG WOODS. Both forgot medicine.\pBring 2 ANTIDOTES to PETALBURG MART.\nI've set aside 2 GREAT BALLS.\pSigned, Reed, the man by the shelves."),
        .reminder = COMPOUND_STRING("Two ANTIDOTES should see us through\nthe woods. Have them both?"),
        .thanks = COMPOUND_STRING("One for each pack. I'll make them\ndo the packing next time!"),
    },
    [MISSIVE_POND] = {
        .species = SPECIES_WINGULL, .reward = ITEM_NET_BALL, .quantity = 2,
        .notice = COMPOUND_STRING("A WINGULL flew over the pond. I drew\nits reflection upside down. Help!\pShow me one by the PETALBURG pond.\nThere's a pair of NET BALLS in it.\pSigned, Pip, the boy by the water."),
        .reminder = COMPOUND_STRING("Could you bring a WINGULL here?\nI need a look at its wingtips."),
        .thanks = COMPOUND_STRING("Blue bands on top, water underneath.\nThere! This one's going on my wall."),
    },
    [MISSIVE_ROPE] = {
        .item = ITEM_ESCAPE_ROPE, .needed = 1, .reward = ITEM_DUSK_BALL, .quantity = 3,
        .notice = COMPOUND_STRING("My brother borrowed my last rope.\nHe tied his tent up with it.\pBring an ESCAPE ROPE to RUSTBORO\nMART for 3 DUSK BALLS.\pSigned, Len, the BUG CATCHER."),
        .reminder = COMPOUND_STRING("Have a spare ESCAPE ROPE? My next\ntrip is into RUSTURF TUNNEL."),
        .thanks = COMPOUND_STRING("This rope stays in my pack. My\nbrother can learn to tie knots!"),
    },
    [MISSIVE_ECHO] = {
        .species = SPECIES_WHISMUR, .reward = ITEM_SUPER_POTION, .quantity = 2,
        .notice = COMPOUND_STRING("Does a WHISMUR hear its own echo?\nIt's my turn to speak in class.\pShow me one at the RUSTBORO school.\nReward: 2 SUPER POTIONS.\pSigned, Kit, the boy at the left desk."),
        .reminder = COMPOUND_STRING("Is there a WHISMUR with you? I'll\nkeep my voice down, I promise."),
        .thanks = COMPOUND_STRING("Its ears folded when the bell rang!\nThat's going straight into my talk."),
    },
};

struct MissiveBoard
{
    u16 map, route, firstJob;
    const u8 *routeName;
};

static const struct MissiveBoard sBoards[] =
{
    {MAP_OLDALE_TOWN, MAP_ROUTE102, MISSIVE_TRAIL_KIT, COMPOUND_STRING("ROUTE 102")},
    {MAP_PETALBURG_CITY, MAP_ROUTE104, MISSIVE_WOODS, COMPOUND_STRING("ROUTE 104")},
    {MAP_RUSTBORO_CITY, MAP_ROUTE116, MISSIVE_ROPE, COMPOUND_STRING("ROUTE 116")},
};

static const struct MissiveBoard *CurrentBoard(void)
{
    for (u32 i = 0; i < ARRAY_COUNT(sBoards); i++)
        if (MAP_GROUP(sBoards[i].map) == gSaveBlock1Ptr->location.mapGroup
         && MAP_NUM(sBoards[i].map) == gSaveBlock1Ptr->location.mapNum)
            return &sBoards[i];
    return NULL;
}

static const struct LegendsQuest *Entry(u16 job)
{
    return job < ARRAY_COUNT(sJobs) ? LegendsQuestGet(MISSIVE_QUEST_BASE + job) : NULL;
}

static bool32 Outstanding(const struct LegendsQuest *q)
{
    return q && FlagGet(q->start) && !FlagGet(q->steps[0].flag);
}

void MissiveList(void)
{
    const struct MissiveBoard *board = CurrentBoard();
    gSpecialVar_Result = board != NULL;
    if (!board)
        return;
    for (u32 i = 0; i < 2; i++)
    {
        const struct LegendsQuest *q = Entry(board->firstJob + i);
        u8 *label = i == 0 ? gStringVar1 : gStringVar2;
        StringCopy(label, q->title);
        if (FlagGet(q->steps[0].flag))
            StringAppend(label, COMPOUND_STRING(" (Done)"));
        else if (FlagGet(q->start))
            StringAppend(label, COMPOUND_STRING(" (Taken)"));
    }
}

void MissiveRead(void)
{
    const struct MissiveBoard *board = CurrentBoard();
    u16 row = gSpecialVar_0x8004;
    gSpecialVar_Result = 2;
    if (!board || row >= 2)
        return;
    u16 job = board->firstJob + row;
    const struct LegendsQuest *q = Entry(job);
    gSpecialVar_0x8004 = job;
    StringCopy(gStringVar4, sJobs[job].notice);
    if (!FlagGet(q->steps[0].flag))
        gSpecialVar_Result = FlagGet(q->start);
}

void MissiveAccept(void)
{
    const struct LegendsQuest *q = Entry(gSpecialVar_0x8004);
    if (q && !FlagGet(q->steps[0].flag))
        FlagSet(q->start);
}

void MissiveReturn(void)
{
    const struct LegendsQuest *q = Entry(gSpecialVar_0x8004);
    if (!Outstanding(q))
        return;
    if (LegendsQuestTracked() == MISSIVE_QUEST_BASE + gSpecialVar_0x8004)
        LegendsQuestTrack(0xFFFF);
    FlagClear(q->start);
}

static bool32 CanDeliver(u16 id)
{
    const struct Missive *job = &sJobs[id];
    if (job->item)
        return CheckBagHasItem(job->item, job->needed);
    for (u32 i = 0; i < gPartiesCount[B_TRAINER_PLAYER]; i++)
        if (GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_SPECIES_OR_EGG) == job->species)
            return TRUE;
    return FALSE;
}

void MissivePrepareDelivery(void)
{
    u16 id = gSpecialVar_0x8004;
    gSpecialVar_Result = FALSE;
    if (!Outstanding(Entry(id)))
        return;
    StringCopy(gStringVar4, sJobs[id].reminder);
    gSpecialVar_Result = CanDeliver(id);
}

void MissiveSettle(void)
{
    u16 id = gSpecialVar_0x8004;
    const struct LegendsQuest *q = Entry(id);
    gSpecialVar_Result = FALSE;
    if (!Outstanding(q) || !CanDeliver(id))
        return;
    const struct Missive *job = &sJobs[id];
    // PC and Bag are independent. A full PC leaves the delivery intact.
    if (!AddPCItem(job->reward, job->quantity))
        return;
    if (job->item)
        RemoveBagItem(job->item, job->needed);
    FlagSet(q->steps[0].flag);
    StringCopy(gStringVar4, job->thanks);
    ConvertIntToDecimalStringN(gStringVar1, job->quantity, STR_CONV_MODE_LEFT_ALIGN, 3);
    CopyItemNameHandlePlural(job->reward, gStringVar2, job->quantity);
    gSpecialVar_Result = TRUE;
}

void MissiveRumor(void)
{
    const struct MissiveBoard *board = CurrentBoard();
    StringCopy(gStringVar4, COMPOUND_STRING("Rain has smudged this field note."));
    if (!board)
        return;
    for (u32 i = 0; gWildMonHeaders[i].mapGroup != MAP_GROUP(MAP_UNDEFINED); i++)
    {
        if (gWildMonHeaders[i].mapGroup != MAP_GROUP(board->route)
         || gWildMonHeaders[i].mapNum != MAP_NUM(board->route))
            continue;
        enum TimeOfDay time = GetTimeOfDayForEncounters(i, WILD_AREA_LAND);
        const struct WildPokemonInfo *land = GetLandMonsInfo(i, time);
        if (land && land->encounterRate)
        {
            u32 slot = NUM_LAND_MONS_ENCOUNTER_SLOTS - 1 - GetTimeOfDay();
            StringCopy(gStringVar1, GetSpeciesCategory(land->wildPokemon[slot].species));
            StringCopy(gStringVar2, board->routeName);
            StringExpandPlaceholders(gStringVar4, COMPOUND_STRING("In the grass on {STR_VAR_2}!\nMy DEX called it the {STR_VAR_1}\lPOKéMON before it slipped away.\pI swear I saw it.\n- A passing Bug Catcher"));
        }
        return;
    }
}
