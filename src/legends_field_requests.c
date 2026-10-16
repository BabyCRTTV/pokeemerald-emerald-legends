#include "global.h"
#include "legends_field_requests.h"
#include "legends_journal.h"
#include "event_data.h"
#include "item.h"
#include "overworld.h"
#include "pokedex.h"
#include "pokemon.h"
#include "string_util.h"
#include "constants/flags.h"
#include "constants/items.h"
#include "constants/maps.h"
#include "constants/moves.h"
#include "constants/pokedex.h"
#include "constants/species.h"
#include "constants/vars.h"

// Three unused native u16 vars; no serialized structure, sector or journal grows.
// Signed state: 0xB7 + active ID+1 (0 = none). Completion and observation words
// use stable request-ID bits. Six requests ship; this format has room for 16.
#define REQUEST_SIGNATURE 0xB700
#define REQUEST_MASK ((1u << LEGENDS_FIELD_REQUEST_COUNT) - 1)
STATIC_ASSERT(LEGENDS_FIELD_REQUEST_COUNT <= 16, FieldRequestWordsFit);
STATIC_ASSERT(NUMBER_OF_MON_TYPES <= 32, FieldRequestTypeMaskFits);

EWRAM_DATA u8 gLegendsFieldRequestMenuLabels[LEGENDS_FIELD_REQUEST_COUNT][48] = {0};

struct FieldRequest
{
    const u8 *title, *description, *readyText, *rewardText;
    u16 rewardItem, rewardCount;
};

static const struct FieldRequest sRequests[LEGENDS_FIELD_REQUEST_COUNT] =
{
    [FIELD_REQUEST_GRASSLAND] = {
        COMPOUND_STRING("Grassland Neighbors"),
        COMPOUND_STRING("BIRCH: POOCHYENA and ZIGZAGOON\nshare the paths near LITTLEROOT.\pRecord both as caught in your\nPOKéDEX, then bring me your notes.\pTry ROUTES 101 and 102.\nYou keep every POKéMON you catch.\pReward: 5 POKé BALLS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Both neighbors, documented!\nEven familiar paths have stories.\pThose records will help me compare\nhow they live alongside people."),
        COMPOUND_STRING("5 POKé BALLS"), ITEM_POKE_BALL, 5},
    [FIELD_REQUEST_FOREST] = {
        COMPOUND_STRING("Beneath the Canopy"),
        COMPOUND_STRING("BIRCH: A forest looks different\nwith a small partner beside you.\pVisit PETALBURG WOODS with a\nBUG-type POKéMON in your party.\pTake notes during your visit.\nThen come back and tell me about it.\pReward: 3 GREAT BALLS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: A BUG-type in its woodland\nhabitat! That's a useful field note.\pThe smallest POKéMON often notice\nthings the rest of us walk past."),
        COMPOUND_STRING("3 GREAT BALLS"), ITEM_GREAT_BALL, 3},
    [FIELD_REQUEST_BERRIES] = {
        COMPOUND_STRING("Berry Samples"),
        COMPOUND_STRING("BIRCH: I'd like to compare the\nberries growing near our towns.\pBring 3 ORAN BERRIES in your BAG.\nI'll use those three for the study.\pYou can find berry trees on\nROUTE 104. Take time to replant!\pReward: 2 SUPER POTIONS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: These ORAN BERRIES are just\nwhat I needed. Thank you!\pA healthy berry patch helps both\nwild POKéMON and passing TRAINERS."),
        COMPOUND_STRING("2 SUPER POTIONS"), ITEM_SUPER_POTION, 2},
    [FIELD_REQUEST_COAST] = {
        COMPOUND_STRING("Coastal Wings"),
        COMPOUND_STRING("BIRCH: WINGULL is at home where\nthe sea meets the land.\pVisit ROUTE 104 with WINGULL or\nPELIPPER in your party.\pMake a note along the coastline.\nThen bring your notes back to me.\pReward: 2 NET BALLS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Your coastal note is ready!\nA sea breeze tells them so much.\pIt makes me wonder how far they\ntravel along that same coastline."),
        COMPOUND_STRING("2 NET BALLS"), ITEM_NET_BALL, 2},
    [FIELD_REQUEST_RECOVERY] = {
        COMPOUND_STRING("Nature's Recovery"),
        COMPOUND_STRING("BIRCH: Some POKéMON draw energy\nfrom others to restore themselves.\pShow me a party POKéMON that knows\nABSORB, MEGA DRAIN, or GIGA DRAIN.\pLOTAD on ROUTE 102 or SHROOMISH\nin PETALBURG WOODS can help.\pReward: 3 HEAL BALLS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: There it is! Energy taken\nin and put straight back to use.\pI'll add this to my notes on how\nPOKéMON recover in the wild."),
        COMPOUND_STRING("3 HEAL BALLS"), ITEM_HEAL_BALL, 3},
    [FIELD_REQUEST_TEAM] = {
        COMPOUND_STRING("A Balanced Team"),
        COMPOUND_STRING("BIRCH: Different POKéMON reveal\ndifferent sides of the same place.\pShow me a party with at least\n3 different types between them.\pBoth types of a dual-type partner\ncount. Eggs don't count as samples.\pReward: 1 RARE CANDY, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Three types, working\ntogether! That's a fine field team.\pKeep looking beyond the familiar.\nThere's always another way to learn."),
        COMPOUND_STRING("1 RARE CANDY"), ITEM_RARE_CANDY, 1},
};

static bool32 ValidState(void)
{
    u16 state = VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE);
    u16 active = state & 0xFF;
    u16 done = VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE);
    u16 notes = VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES);
    if ((state & 0xFF00) != REQUEST_SIGNATURE || active > LEGENDS_FIELD_REQUEST_COUNT
        || (done & ~REQUEST_MASK))
        return FALSE;
    if (!active) return notes == 0;
    return !(done & (1u << (active - 1))) && !(notes & ~(1u << (active - 1)));
}

u16 LegendsFieldRequestActive(void)
{
    u16 active;
    if (!FlagGet(FLAG_SYS_POKEDEX_GET) || !ValidState()) return FIELD_REQUEST_NONE;
    active = VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE) & 0xFF;
    return active ? active - 1 : FIELD_REQUEST_NONE;
}

bool32 LegendsFieldRequestComplete(u16 id)
{
    return id < LEGENDS_FIELD_REQUEST_COUNT && ValidState()
        && (VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE) & (1u << id));
}

static bool32 SampleMon(u8 slot, u16 *species)
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][slot];
    *species = GetMonData(mon, MON_DATA_SPECIES);
    return *species != SPECIES_NONE && *species < NUM_SPECIES && !GetMonData(mon, MON_DATA_IS_EGG);
}

static bool32 PartyHasType(u8 type)
{
    u8 i;
    u16 species;
    for (i = 0; i < gPartiesCount[B_TRAINER_PLAYER] && i < PARTY_SIZE; i++)
        if (SampleMon(i, &species) && (gSpeciesInfo[species].types[0] == type || gSpeciesInfo[species].types[1] == type))
            return TRUE;
    return FALSE;
}

static bool32 PartyHasSeaBird(void)
{
    u8 i;
    u16 species;
    for (i = 0; i < gPartiesCount[B_TRAINER_PLAYER] && i < PARTY_SIZE; i++)
        if (SampleMon(i, &species) && (species == SPECIES_WINGULL || species == SPECIES_PELIPPER)) return TRUE;
    return FALSE;
}

static bool32 PartyHasDrain(void)
{
    u8 i, move;
    u16 species, id;
    for (i = 0; i < gPartiesCount[B_TRAINER_PLAYER] && i < PARTY_SIZE; i++)
        if (SampleMon(i, &species))
            for (move = 0; move < MAX_MON_MOVES; move++)
            {
                id = GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_MOVE1 + move);
                if (id == MOVE_ABSORB || id == MOVE_MEGA_DRAIN || id == MOVE_GIGA_DRAIN) return TRUE;
            }
    return FALSE;
}

static bool32 PartyHasThreeTypes(void)
{
    u32 types = 0;
    u8 i, t, count = 0;
    u16 species;
    for (i = 0; i < gPartiesCount[B_TRAINER_PLAYER] && i < PARTY_SIZE; i++)
        if (SampleMon(i, &species))
            for (t = 0; t < 2; t++)
            {
                u8 type = gSpeciesInfo[species].types[t];
                if (type > TYPE_NONE && type < NUMBER_OF_MON_TYPES && type != TYPE_MYSTERY)
                    types |= 1u << type;
            }
    while (types) { count += types & 1; types >>= 1; }
    return count >= 3;
}

void LegendsFieldRequestsObserve(void)
{
    u16 id = LegendsFieldRequestActive();
    bool32 here = FALSE;
    if (id == FIELD_REQUEST_NONE || IsOverworldLinkActive()
        || (VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES) & (1u << id))) return;
    if (id == FIELD_REQUEST_FOREST)
        here = gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_PETALBURG_WOODS)
            && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_PETALBURG_WOODS) && PartyHasType(TYPE_BUG);
    else if (id == FIELD_REQUEST_COAST)
        here = gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_ROUTE104)
            && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_ROUTE104) && PartyHasSeaBird();
    if (here) VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 1u << id);
}

bool32 LegendsFieldRequestStepComplete(u16 id, u8 step)
{
    u8 last = id == FIELD_REQUEST_GRASSLAND ? 2 : 1;
    if (id >= LEGENDS_FIELD_REQUEST_COUNT || step > last) return FALSE;
    if (LegendsFieldRequestComplete(id)) return TRUE;
    if (LegendsFieldRequestActive() != id || step == last) return FALSE;
    switch (id)
    {
    case FIELD_REQUEST_GRASSLAND:
        return GetSetPokedexFlag(step ? NATIONAL_DEX_ZIGZAGOON : NATIONAL_DEX_POOCHYENA, FLAG_GET_CAUGHT);
    case FIELD_REQUEST_FOREST:
    case FIELD_REQUEST_COAST:
        return VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES) & (1u << id);
    case FIELD_REQUEST_BERRIES: return CheckBagHasItem(ITEM_ORAN_BERRY, 3);
    case FIELD_REQUEST_RECOVERY: return PartyHasDrain();
    case FIELD_REQUEST_TEAM: return PartyHasThreeTypes();
    }
    return FALSE;
}

static bool32 Ready(u16 id)
{
    return id < LEGENDS_FIELD_REQUEST_COUNT && LegendsFieldRequestStepComplete(id, 0)
        && (id != FIELD_REQUEST_GRASSLAND || LegendsFieldRequestStepComplete(id, 1));
}

u8 LegendsFieldRequestAccept(u16 id)
{
    if (id >= LEGENDS_FIELD_REQUEST_COUNT || !FlagGet(FLAG_SYS_POKEDEX_GET) || IsOverworldLinkActive()) return FIELD_REQUEST_INVALID;
    if (LegendsFieldRequestActive() != FIELD_REQUEST_NONE) return FIELD_REQUEST_BUSY;
    if (LegendsFieldRequestComplete(id)) return FIELD_REQUEST_FINISHED;
    if (!ValidState()) VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, 0);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, REQUEST_SIGNATURE | (id + 1));
    // Respect a previously pinned main/side quest; otherwise pin this request.
    if (LegendsQuestTracked() == 0xFFFF) LegendsQuestTrack(LEGENDS_FIELD_REQUEST_QUEST_BASE + id);
    return FIELD_REQUEST_OK;
}

bool32 LegendsFieldRequestAbandon(void)
{
    if (LegendsFieldRequestActive() == FIELD_REQUEST_NONE || IsOverworldLinkActive()) return FALSE;
    VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, REQUEST_SIGNATURE);
    LegendsJournalRefresh();
    return TRUE;
}

u8 LegendsFieldRequestSubmit(void)
{
    u16 id = LegendsFieldRequestActive();
    if (id == FIELD_REQUEST_NONE || IsOverworldLinkActive()) return FIELD_REQUEST_INVALID;
    if (!Ready(id)) return FIELD_REQUEST_NOT_READY;
    // AddPCItem is atomic. No berries/progress are consumed if storage is full.
    if (!AddPCItem(sRequests[id].rewardItem, sRequests[id].rewardCount)) return FIELD_REQUEST_STORAGE_FULL;
    if (id == FIELD_REQUEST_BERRIES) RemoveBagItem(ITEM_ORAN_BERRY, 3);
    StringCopy(gStringVar4, sRequests[id].readyText);
    StringCopy(gStringVar1, sRequests[id].rewardText);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE) | (1u << id));
    VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, REQUEST_SIGNATURE);
    LegendsJournalRefresh();
    return FIELD_REQUEST_OK;
}

void LegendsFieldRequestsGetActive(void) { gSpecialVar_Result = LegendsFieldRequestActive(); }
void LegendsFieldRequestsAcceptSpecial(void) { gSpecialVar_Result = LegendsFieldRequestAccept(gSpecialVar_0x8004); }
void LegendsFieldRequestsSubmitSpecial(void) { gSpecialVar_Result = LegendsFieldRequestSubmit(); }
void LegendsFieldRequestsAbandonSpecial(void) { gSpecialVar_Result = LegendsFieldRequestAbandon(); }

void LegendsFieldRequestsPrepareMenu(void)
{
    u8 i;
    for (i = 0; i < LEGENDS_FIELD_REQUEST_COUNT; i++)
    {
        StringCopy(gLegendsFieldRequestMenuLabels[i], LegendsFieldRequestComplete(i) ? COMPOUND_STRING("Done: ") : COMPOUND_STRING(""));
        StringAppend(gLegendsFieldRequestMenuLabels[i], sRequests[i].title);
    }
}

void LegendsFieldRequestsDescribe(void)
{
    u16 id = gSpecialVar_0x8004;
    if (id >= LEGENDS_FIELD_REQUEST_COUNT)
    {
        StringCopy(gStringVar4, COMPOUND_STRING("BIRCH: Let's look at the list again."));
        gSpecialVar_Result = TRUE;
        return;
    }
    gSpecialVar_Result = LegendsFieldRequestComplete(id);
    StringCopy(gStringVar4, gSpecialVar_Result ? COMPOUND_STRING("BIRCH: We've already finished that\nrequest. Thank you for your help!") : sRequests[id].description);
}

void LegendsFieldRequestsReview(void)
{
    u16 id = LegendsFieldRequestActive();
    if (id == FIELD_REQUEST_NONE) return;
    StringCopy(gStringVar4, sRequests[id].description);
    StringAppend(gStringVar4, Ready(id)
        ? COMPOUND_STRING("\pYour findings are ready.\nI can file your report now!")
        : COMPOUND_STRING("\pThere's still a little work to do.\nYour QUEST LOG lists what remains."));
}
