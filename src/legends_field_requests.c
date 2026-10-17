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

// v1 B7 words remain readable; v2 B8 initializes one verified-unused completion word.
// No serialized structure, sector, journal field or published request ID changes.
#define REQUEST_LEGACY_SIGNATURE 0xB700
#define REQUEST_SIGNATURE 0xB800
#define REQUEST_MASK ((1u << LEGENDS_FIELD_REQUEST_COUNT) - 1)
#define REQUEST_LEGACY_MASK 0x3Fu
STATIC_ASSERT(LEGENDS_FIELD_REQUEST_COUNT < 32, FieldRequestWordsFit);
STATIC_ASSERT(NUMBER_OF_MON_TYPES <= 32, FieldRequestTypeMaskFits);
enum { PROOF_LEGACY, PROOF_HABITAT_TYPE, PROOF_HABITAT_SPECIES, PROOF_CAUGHT_PAIR, PROOF_MOVE, PROOF_TYPES, PROOF_DEX_COUNT };
EWRAM_DATA u8 gLegendsFieldRequestMenuLabels[LEGENDS_REQUEST_PAGE_SIZE][48] = {0};
static EWRAM_DATA u8 sPatron = 0;
static EWRAM_DATA u8 sGroup = 0;

struct FieldRequest
{
    const u8 *title, *description, *readyText, *rewardText;
    u16 rewardItem, rewardCount;
    u16 gate, proof, arg, map, map2, second;
    const u8 *gateText;
};

static const struct FieldRequest sRequests[LEGENDS_FIELD_REQUEST_COUNT] =
{
    [FIELD_REQUEST_GRASSLAND] = {
        COMPOUND_STRING("Grassland Neighbors"),
        COMPOUND_STRING("BIRCH: POOCHYENA and ZIGZAGOON\nshare the paths near LITTLEROOT.\pRecord both as caught in your\nPOKéDEX, then bring me your notes.\pTry ROUTES 101 and 102.\nYou keep every POKéMON you catch.\pReward: 5 POKé BALLS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Both neighbors, documented!\nEven familiar paths have stories.\pThose records will help me compare\nhow they live alongside people."),
        COMPOUND_STRING("5 POKé BALLS"), ITEM_POKE_BALL, 5, 0, 0, 0, 0, 0, 0, NULL},
    [FIELD_REQUEST_FOREST] = {
        COMPOUND_STRING("Beneath the Canopy"),
        COMPOUND_STRING("BIRCH: A forest looks different\nwith a small partner beside you.\pVisit PETALBURG WOODS with a\nBUG-type POKéMON in your party.\pTake notes during your visit.\nThen come back and tell me about it.\pReward: 3 GREAT BALLS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: A BUG-type in its woodland\nhabitat! That's a useful field note.\pThe smallest POKéMON often notice\nthings the rest of us walk past."),
        COMPOUND_STRING("3 GREAT BALLS"), ITEM_GREAT_BALL, 3, 0, 0, 0, 0, 0, 0, NULL},
    [FIELD_REQUEST_BERRIES] = {
        COMPOUND_STRING("Berry Samples"),
        COMPOUND_STRING("BIRCH: I'd like to compare the\nberries growing near our towns.\pBring 3 ORAN BERRIES in your BAG.\nI'll use those three for the study.\pYou can find berry trees on\nROUTE 104. Take time to replant!\pReward: 2 SUPER POTIONS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: These ORAN BERRIES are just\nwhat I needed. Thank you!\pA healthy berry patch helps both\nwild POKéMON and passing TRAINERS."),
        COMPOUND_STRING("2 SUPER POTIONS"), ITEM_SUPER_POTION, 2, 0, 0, 0, 0, 0, 0, NULL},
    [FIELD_REQUEST_COAST] = {
        COMPOUND_STRING("Coastal Wings"),
        COMPOUND_STRING("BIRCH: WINGULL is at home where\nthe sea meets the land.\pVisit ROUTE 104 with WINGULL or\nPELIPPER in your party.\pMake a note along the coastline.\nThen bring your notes back to me.\pReward: 2 NET BALLS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Your coastal note is ready!\nA sea breeze tells them so much.\pIt makes me wonder how far they\ntravel along that same coastline."),
        COMPOUND_STRING("2 NET BALLS"), ITEM_NET_BALL, 2, 0, 0, 0, 0, 0, 0, NULL},
    [FIELD_REQUEST_RECOVERY] = {
        COMPOUND_STRING("Nature's Recovery"),
        COMPOUND_STRING("BIRCH: Some POKéMON draw energy\nfrom others to restore themselves.\pShow me a party POKéMON that knows\nABSORB, MEGA DRAIN, or GIGA DRAIN.\pLOTAD on ROUTE 102 or SHROOMISH\nin PETALBURG WOODS can help.\pReward: 3 HEAL BALLS, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: There it is! Energy taken\nin and put straight back to use.\pI'll add this to my notes on how\nPOKéMON recover in the wild."),
        COMPOUND_STRING("3 HEAL BALLS"), ITEM_HEAL_BALL, 3, 0, 0, 0, 0, 0, 0, NULL},
    [FIELD_REQUEST_TEAM] = {
        COMPOUND_STRING("A Balanced Team"),
        COMPOUND_STRING("BIRCH: Different POKéMON reveal\ndifferent sides of the same place.\pShow me a party with at least\n3 different types between them.\pBoth types of a dual-type partner\ncount. Eggs don't count as samples.\pReward: 1 RARE CANDY, sent to\nITEM STORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Three types, working\ntogether! That's a fine field team.\pKeep looking beyond the familiar.\nThere's always another way to learn."),
        COMPOUND_STRING("1 RARE CANDY"), ITEM_RARE_CANDY, 1, 0, 0, 0, 0, 0, 0, NULL},
    [FIELD_REQUEST_GRANITE] = {
        COMPOUND_STRING("Granite Cave Life"),
        COMPOUND_STRING("BIRCH: Rocky caves shelter some hardy\nneighbors.\pVisit GRANITE CAVE with a ROCK-type\npartner in your party.\pGEODUDE can be found in the cave.\pReward: 3 GREAT BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 GREAT BALLS"), ITEM_GREAT_BALL, 3,
        FLAG_BADGE01_GET, PROOF_HABITAT_TYPE, TYPE_ROCK, MAP_GRANITE_CAVE_1F, 0, 0,
        COMPOUND_STRING("Earn the STONE BADGE.")},
    [FIELD_REQUEST_TIDAL] = {
        COMPOUND_STRING("Tidal Pool Records"),
        COMPOUND_STRING("BIRCH: Our island waters support very\ndifferent swimmers.\pRecord TENTACOOL and MAGIKARP as\ncaught in your POKéDEX.\pTry the OLD ROD around DEWFORD.\nEarlier catches count.\pReward: 3 DIVE BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 DIVE BALLS"), ITEM_DIVE_BALL, 3,
        FLAG_BADGE02_GET, PROOF_CAUGHT_PAIR, NATIONAL_DEX_TENTACOOL, 0, 0, NATIONAL_DEX_MAGIKARP,
        COMPOUND_STRING("Earn the KNUCKLE BADGE.")},
    [FIELD_REQUEST_SPARKS] = {
        COMPOUND_STRING("Meadow Sparks"),
        COMPOUND_STRING("BIRCH: The meadows near MAUVILLE\ncrackle with life.\pVisit ROUTE 110 with an ELECTRIC-type\npartner in your party.\pELECTRIKE makes a fine guide to its\nhome.\pReward: 3 QUICK BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 QUICK BALLS"), ITEM_QUICK_BALL, 3,
        FLAG_BADGE03_GET, PROOF_HABITAT_TYPE, TYPE_ELECTRIC, MAP_ROUTE110, 0, 0,
        COMPOUND_STRING("Earn the DYNAMO BADGE.")},
    [FIELD_REQUEST_DRYLAND] = {
        COMPOUND_STRING("Dryland Partners"),
        COMPOUND_STRING("BIRCH: Dry country asks a lot of its\ninhabitants.\pVisit ROUTE 111 with a GROUND-type\npartner in your party.\pNUMEL or SANDSHREW can help with this\nsurvey.\pReward: 3 NEST BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 NEST BALLS"), ITEM_NEST_BALL, 3,
        FLAG_BADGE04_GET, PROOF_HABITAT_TYPE, TYPE_GROUND, MAP_ROUTE111, 0, 0,
        COMPOUND_STRING("Earn the HEAT BADGE.")},
    [FIELD_REQUEST_RIVERBANK] = {
        COMPOUND_STRING("Riverbank Survey"),
        COMPOUND_STRING("BIRCH: Riverbanks link the forest to\nthe water.\pVisit ROUTE 119 with a GRASS-type\npartner in your party.\pA partner from an earlier route is\nwelcome too.\pReward: 3 NET BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 NET BALLS"), ITEM_NET_BALL, 3,
        FLAG_BADGE05_GET, PROOF_HABITAT_TYPE, TYPE_GRASS, MAP_ROUTE119, 0, 0,
        COMPOUND_STRING("Earn the BALANCE BADGE.")},
    [FIELD_REQUEST_WEATHER] = {
        COMPOUND_STRING("Weather Partners"),
        COMPOUND_STRING("BIRCH: The WEATHER INSTITUTE studies\na remarkable partner.\pVisit ROUTE 119 with CASTFORM in your\nparty.\pAny of CASTFORM's weather forms can\nhelp.\pReward: 1 DAMP ROCK, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("1 DAMP ROCK"), ITEM_DAMP_ROCK, 1,
        FLAG_RECEIVED_CASTFORM, PROOF_HABITAT_SPECIES, SPECIES_CASTFORM, MAP_ROUTE119, 0, 0,
        COMPOUND_STRING("Help the WEATHER INSTITUTE and\nreceive CASTFORM.")},
    [FIELD_REQUEST_CANOPY] = {
        COMPOUND_STRING("Canopy Travelers"),
        COMPOUND_STRING("BIRCH: The canopy has paths we cannot\nwalk.\pVisit ROUTE 120 with a FLYING-type\npartner in your party.\pYou need only observe your partner; no\nmove is required.\pReward: 3 REPEAT BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 REPEAT BALLS"), ITEM_REPEAT_BALL, 3,
        FLAG_BADGE06_GET, PROOF_HABITAT_TYPE, TYPE_FLYING, MAP_ROUTE120, 0, 0,
        COMPOUND_STRING("Earn the FEATHER BADGE.")},
    [FIELD_REQUEST_MOUNTAIN] = {
        COMPOUND_STRING("Quiet Mountain"),
        COMPOUND_STRING("BIRCH: MT. PYRE deserves a quiet and\nrespectful visit.\pVisit the exterior of MT. PYRE with a\nGHOST-type partner.\pSHUPPET and DUSKULL live in the\nmountain.\pReward: 1 CLEANSE TAG, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("1 CLEANSE TAG"), ITEM_CLEANSE_TAG, 1,
        FLAG_VISITED_LILYCOVE_CITY, PROOF_HABITAT_TYPE, TYPE_GHOST, MAP_MT_PYRE_EXTERIOR, 0, 0,
        COMPOUND_STRING("Reach LILYCOVE CITY.")},
    [FIELD_REQUEST_OFFSHORE] = {
        COMPOUND_STRING("Offshore Partners"),
        COMPOUND_STRING("BIRCH: The open sea is another part of\nour field atlas.\pVisit ROUTE 124 with a WATER-type\npartner in your party.\pSURF along the route; diving is not\nrequired.\pReward: 3 DIVE BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 DIVE BALLS"), ITEM_DIVE_BALL, 3,
        FLAG_BADGE07_GET, PROOF_HABITAT_TYPE, TYPE_WATER, MAP_ROUTE124, 0, 0,
        COMPOUND_STRING("Earn the MIND BADGE.")},
    [FIELD_REQUEST_SHOAL] = {
        COMPOUND_STRING("Shoal Cave Voices"),
        COMPOUND_STRING("BIRCH: Tides change the rooms in SHOAL\nCAVE.\pVisit the cave entrance with an\nICE-type partner.\pEither tide is fine. SPHEAL is a local\nresident.\pReward: 3 HEAL BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 HEAL BALLS"), ITEM_HEAL_BALL, 3,
        FLAG_DEFEATED_MAGMA_SPACE_CENTER, PROOF_HABITAT_TYPE, TYPE_ICE, MAP_SHOAL_CAVE_LOW_TIDE_ENTRANCE_ROOM, MAP_SHOAL_CAVE_HIGH_TIDE_ENTRANCE_ROOM, 0,
        COMPOUND_STRING("Help STEVEN at the SPACE CENTER.")},
    [FIELD_REQUEST_PEACE] = {
        COMPOUND_STRING("Peaceful Waters"),
        COMPOUND_STRING("BIRCH: With the skies calm again, we\ncan observe gently.\pVisit SOOTOPOLIS CITY with a\nWATER-type partner.\pThe city's lake is part of its everyday\nlife too.\pReward: 3 LUXURY BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 LUXURY BALLS"), ITEM_LUXURY_BALL, 3,
        FLAG_SOOTOPOLIS_ARCHIE_MAXIE_LEAVE, PROOF_HABITAT_TYPE, TYPE_WATER, MAP_SOOTOPOLIS_CITY, 0, 0,
        COMPOUND_STRING("Resolve the crisis in SOOTOPOLIS.")},
    [FIELD_REQUEST_ATLAS] = {
        COMPOUND_STRING("Hoenn Field Atlas"),
        COMPOUND_STRING("BIRCH: Your earlier reports can become\na regional atlas.\pRecord at least 60 HOENN species as\ncaught, then report to me.\pEarlier catches count. Keep every\nPOKéMON.\pReward: 3 RARE CANDIES, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("BIRCH: Thank you for your careful\nwork!\pYour report will help us understand\nHOENN."),
        COMPOUND_STRING("3 RARE CANDIES"), ITEM_RARE_CANDY, 3,
        FLAG_IS_CHAMPION, PROOF_DEX_COUNT, 60, 0, 0, 0,
        COMPOUND_STRING("Become CHAMPION and finish the other\n17 BIRCH requests.")},
    [FIELD_REQUEST_TUNNEL] = {
        COMPOUND_STRING("Tunnel Acoustics"),
        COMPOUND_STRING("MR. STONE: Your help in the tunnel gave\nour staff an idea.\pVisit RUSTURF TUNNEL with WHISMUR in\nyour party.\pWe need a field note, not a POKéMON\nhandover.\pReward: 3 GREAT BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("3 GREAT BALLS"), ITEM_GREAT_BALL, 3,
        FLAG_RECEIVED_POKENAV, PROOF_HABITAT_SPECIES, SPECIES_WHISMUR, MAP_RUSTURF_TUNNEL, 0, 0,
        COMPOUND_STRING("Meet MR. STONE and receive the\nPOKéNAV.")},
    [FIELD_REQUEST_STEEL] = {
        COMPOUND_STRING("Steel Under Stone"),
        COMPOUND_STRING("MR. STONE: STEVEN's cave studies\ninspire our materials team.\pVisit GRANITE CAVE with a STEEL-type\npartner.\pARON lives in the cave. Keep your\npartner afterward.\pReward: 1 METAL COAT, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("1 METAL COAT"), ITEM_METAL_COAT, 1,
        FLAG_DELIVERED_STEVEN_LETTER, PROOF_HABITAT_TYPE, TYPE_STEEL, MAP_GRANITE_CAVE_1F, 0, 0,
        COMPOUND_STRING("Deliver the LETTER to STEVEN.")},
    [FIELD_REQUEST_HARBOR] = {
        COMPOUND_STRING("Harbor Field Test"),
        COMPOUND_STRING("MR. STONE: CAPT. STERN needs equipment\nsuited to coastal work.\pVisit ROUTE 109 with a WATER-type\npartner.\pObserve the partner on the beach; no\nsamples are taken.\pReward: 3 NET BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("3 NET BALLS"), ITEM_NET_BALL, 3,
        FLAG_DELIVERED_DEVON_GOODS, PROOF_HABITAT_TYPE, TYPE_WATER, MAP_ROUTE109, 0, 0,
        COMPOUND_STRING("Deliver the DEVON GOODS to CAPT.\nSTERN.")},
    [FIELD_REQUEST_CURRENT] = {
        COMPOUND_STRING("Current Conductors"),
        COMPOUND_STRING("MR. STONE: A controlled current can\nteach our engineers a lot.\pShow me a party POKéMON that knows\nTHUNDER WAVE.\pDo not use it on anyone. A\ndemonstration record will do.\pReward: 1 MAGNET, sent to ITEM STORAGE\non the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("1 MAGNET"), ITEM_MAGNET, 1,
        FLAG_BADGE03_GET, PROOF_MOVE, MOVE_THUNDER_WAVE, 0, 0, 0,
        COMPOUND_STRING("Earn the DYNAMO BADGE.")},
    [FIELD_REQUEST_HEAT] = {
        COMPOUND_STRING("Heatproof Materials"),
        COMPOUND_STRING("MR. STONE: We test materials for use\naround volcanic heat.\pVisit FIERY PATH with a FIRE-type\npartner.\pNUMEL and SLUGMA are useful guides to\nthe area.\pReward: 1 CHARCOAL, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("1 CHARCOAL"), ITEM_CHARCOAL, 1,
        FLAG_BADGE04_GET, PROOF_HABITAT_TYPE, TYPE_FIRE, MAP_FIERY_PATH, 0, 0,
        COMPOUND_STRING("Earn the HEAT BADGE.")},
    [FIELD_REQUEST_WATERWAYS] = {
        COMPOUND_STRING("Working Waterways"),
        COMPOUND_STRING("MR. STONE: Reliable river equipment\nstarts with fieldwork.\pVisit ROUTE 118 with a WATER-type\npartner.\pTravel at your own pace; there is no\ndelivery timer.\pReward: 3 DIVE BALLS, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("3 DIVE BALLS"), ITEM_DIVE_BALL, 3,
        FLAG_BADGE05_GET, PROOF_HABITAT_TYPE, TYPE_WATER, MAP_ROUTE118, 0, 0,
        COMPOUND_STRING("Earn the BALANCE BADGE.")},
    [FIELD_REQUEST_RAIN] = {
        COMPOUND_STRING("Rain Instruments"),
        COMPOUND_STRING("MR. STONE: The WEATHER INSTITUTE can\nhelp calibrate our tools.\pVisit ROUTE 119 with CASTFORM in your\nparty.\pOur instruments need a partner, not a\nparticular forecast.\pReward: 1 SMOOTH ROCK, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("1 SMOOTH ROCK"), ITEM_SMOOTH_ROCK, 1,
        FLAG_RECEIVED_CASTFORM, PROOF_HABITAT_SPECIES, SPECIES_CASTFORM, MAP_ROUTE119, 0, 0,
        COMPOUND_STRING("Help the WEATHER INSTITUTE and\nreceive CASTFORM.")},
    [FIELD_REQUEST_FLIGHT] = {
        COMPOUND_STRING("Flight Recorder"),
        COMPOUND_STRING("MR. STONE: We are designing a recorder\nfor aerial journeys.\pShow me a party POKéMON that knows\nFLY.\pThe move can stay on your partner;\nnothing is taken.\pReward: 1 SHARP BEAK, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("1 SHARP BEAK"), ITEM_SHARP_BEAK, 1,
        FLAG_BADGE06_GET, PROOF_MOVE, MOVE_FLY, 0, 0, 0,
        COMPOUND_STRING("Earn the FEATHER BADGE.")},
    [FIELD_REQUEST_POWER] = {
        COMPOUND_STRING("Power Components"),
        COMPOUND_STRING("MR. STONE: Our power systems need a\nbroader research base.\pRecord MAGNEMITE and VOLTORB as\ncaught in your POKéDEX.\pNEW MAUVILLE is home to both. Earlier\ncatches count.\pReward: 1 THUNDER STONE, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("1 THUNDER STONE"), ITEM_THUNDER_STONE, 1,
        FLAG_BADGE06_GET, PROOF_CAUGHT_PAIR, NATIONAL_DEX_MAGNEMITE, 0, 0, NATIONAL_DEX_VOLTORB,
        COMPOUND_STRING("Earn the FEATHER BADGE.")},
    [FIELD_REQUEST_ORBIT] = {
        COMPOUND_STRING("Orbital Telemetry"),
        COMPOUND_STRING("MR. STONE: The SPACE CENTER can resume\nits peaceful work.\pVisit MOSSDEEP CITY with a\nPSYCHIC-type partner.\pYour observations will help our\ndistant-signal study.\pReward: 1 PP UP, sent to ITEM STORAGE\non the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("1 PP UP"), ITEM_PP_UP, 1,
        FLAG_DEFEATED_MAGMA_SPACE_CENTER, PROOF_HABITAT_TYPE, TYPE_PSYCHIC, MAP_MOSSDEEP_CITY, 0, 0,
        COMPOUND_STRING("Help STEVEN at the SPACE CENTER.")},
    [FIELD_REQUEST_PRESSURE] = {
        COMPOUND_STRING("Pressure Recorder"),
        COMPOUND_STRING("MR. STONE: Our new pressure recorder\nneeds an undersea reading.\pVisit UNDERWATER on ROUTE 124 with a\nWATER-type partner.\pUse DIVE where the sea is dark. Return\nsafely.\pReward: 1 PP MAX, sent to ITEM STORAGE\non the PC."),
        COMPOUND_STRING("MR. STONE: Thank you for your careful\nwork!\pYour report will help us build better\ntools for people and POKéMON."),
        COMPOUND_STRING("1 PP MAX"), ITEM_PP_MAX, 1,
        FLAG_RECEIVED_HM_DIVE, PROOF_HABITAT_TYPE, TYPE_WATER, MAP_UNDERWATER_ROUTE124, 0, 0,
        COMPOUND_STRING("Receive DIVE from STEVEN.")},
    [FIELD_REQUEST_MASTER] = {
        COMPOUND_STRING("Devon Master Project"),
        COMPOUND_STRING("MR. STONE: Your eleven reports have\nshaped a final research project.\pShow me at least 6 different types\nacross your party.\pBoth types of dual-type partners\ncount. Eggs do not count.\pReward: 1 MASTER BALL, sent to ITEM\nSTORAGE on the PC."),
        COMPOUND_STRING("MR. STONE: All twelve contracts,\ncomplete!\pYou've earned this MASTER BALL.\nUse it with care!"),
        COMPOUND_STRING("1 MASTER BALL"), ITEM_MASTER_BALL, 1,
        FLAG_IS_CHAMPION, PROOF_TYPES, 6, 0, 0, 0,
        COMPOUND_STRING("Become CHAMPION and finish the other\n11 DEVON contracts.")},

};

static bool32 LegacyState(void)
{
    return (VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE) & 0xFF00) == REQUEST_LEGACY_SIGNATURE;
}
static u32 DoneBits(void)
{
    return VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE) | (LegacyState() ? 0 : (u32)VarGet(VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH) << 16);
}
static u32 NoteBits(void)
{
    u16 raw = VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES);
    u16 active = VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE) & 0xFF;
    if (LegacyState()) return raw;
    // Only one request can be active, so v2 needs one saved observation boolean.
    return raw == 1 && active && active <= LEGENDS_FIELD_REQUEST_COUNT ? 1u << (active - 1) : 0;
}
static bool32 ValidState(void)
{
    u16 state = VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE), active = state & 0xFF;
    bool32 legacy = LegacyState();
    u32 done = DoneBits(), notes = NoteBits(), mask = legacy ? REQUEST_LEGACY_MASK : REQUEST_MASK;
    if ((!legacy && (state & 0xFF00) != REQUEST_SIGNATURE)
        || active > (legacy ? 6 : LEGENDS_FIELD_REQUEST_COUNT) || (done & ~mask)) return FALSE;
    if (!legacy && VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES) > 1) return FALSE;
    if (!active) return VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES) == 0;
    return !(done & (1u << (active - 1))) && !(notes & ~(1u << (active - 1)));
}
// Upgrade only at a write operation, preserving every v0.0.58 low-word bit.
static void EnsureCurrentState(void)
{
    bool32 valid = ValidState();
    u16 active = valid ? VarGet(VAR_LEGENDS_FIELD_REQUEST_STATE) & 0xFF : 0;
    if (!valid)
    {
        VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, 0);
        VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, 0);
    }
    if (!valid || LegacyState())
    {
        VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH, 0);
        VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, valid && VarGet(VAR_LEGENDS_FIELD_REQUEST_NOTES) != 0);
        VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, REQUEST_SIGNATURE | active);
    }
}
static void SetNotes(u32 bits)
{
    VarSet(VAR_LEGENDS_FIELD_REQUEST_NOTES, bits != 0);
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
    return id < LEGENDS_FIELD_REQUEST_COUNT && ValidState() && (DoneBits() & (1u << id));
}
u8 LegendsFieldRequestOwner(u16 id)
{
    return id < LEGENDS_BIRCH_REQUEST_COUNT ? FIELD_PATRON_BIRCH : FIELD_PATRON_DEVON;
}
bool32 LegendsFieldRequestUnlocked(u16 id)
{
    u16 i;
    if (id >= LEGENDS_FIELD_REQUEST_COUNT || !FlagGet(FLAG_SYS_POKEDEX_GET)) return FALSE;
    if (LegendsFieldRequestOwner(id) == FIELD_PATRON_DEVON && !FlagGet(FLAG_RECEIVED_POKENAV)) return FALSE;
    if (sRequests[id].gate && !FlagGet(sRequests[id].gate)) return FALSE;
    if (id == FIELD_REQUEST_ATLAS || id == FIELD_REQUEST_MASTER)
        for (i = id == FIELD_REQUEST_ATLAS ? 0 : LEGENDS_BIRCH_REQUEST_COUNT; i < id; i++)
            if (!LegendsFieldRequestComplete(i)) return FALSE;
    return TRUE;
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

static bool32 PartyHasTypes(u8 minimum)
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
    return count >= minimum;
}

static bool32 OnMap(u16 map)
{
    return gSaveBlock1Ptr->location.mapGroup == (map >> 8) && gSaveBlock1Ptr->location.mapNum == (map & 0xFF);
}
static bool32 PartyHasSpecies(u16 sample)
{
    u8 i;
    u16 species;
    for (i = 0; i < gPartiesCount[B_TRAINER_PLAYER] && i < PARTY_SIZE; i++)
        if (SampleMon(i, &species) && (species == sample || (sample == SPECIES_CASTFORM
            && (species == SPECIES_CASTFORM_SUNNY || species == SPECIES_CASTFORM_RAINY || species == SPECIES_CASTFORM_SNOWY)))) return TRUE;
    return FALSE;
}
static bool32 PartyKnows(u16 move)
{
    u8 i, j;
    u16 species;
    for (i = 0; i < gPartiesCount[B_TRAINER_PLAYER] && i < PARTY_SIZE; i++)
        if (SampleMon(i, &species))
            for (j = 0; j < MAX_MON_MOVES; j++)
                if (GetMonData(&gParties[B_TRAINER_PLAYER][i], MON_DATA_MOVE1 + j) == move) return TRUE;
    return FALSE;
}
void LegendsFieldRequestsObserve(void)
{
    u16 id = LegendsFieldRequestActive();
    bool32 here = FALSE;
    const struct FieldRequest *r;
    if (id == FIELD_REQUEST_NONE || IsOverworldLinkActive() || (NoteBits() & (1u << id))) return;
    if (id == FIELD_REQUEST_FOREST) here = OnMap(MAP_PETALBURG_WOODS) && PartyHasType(TYPE_BUG);
    else if (id == FIELD_REQUEST_COAST) here = OnMap(MAP_ROUTE104) && PartyHasSeaBird();
    else
    {
        r = &sRequests[id];
        if (OnMap(r->map) || (r->map2 && OnMap(r->map2)))
        {
            if (r->proof == PROOF_HABITAT_TYPE) here = PartyHasType(r->arg);
            else if (r->proof == PROOF_HABITAT_SPECIES) here = PartyHasSpecies(r->arg);
        }
    }
    if (here) { EnsureCurrentState(); SetNotes(1u << id); }
}

bool32 LegendsFieldRequestStepComplete(u16 id, u8 step)
{
    u8 last = id == FIELD_REQUEST_GRASSLAND || (id < LEGENDS_FIELD_REQUEST_COUNT && sRequests[id].proof == PROOF_CAUGHT_PAIR) ? 2 : 1;
    if (id >= LEGENDS_FIELD_REQUEST_COUNT || step > last) return FALSE;
    if (LegendsFieldRequestComplete(id)) return TRUE;
    if (LegendsFieldRequestActive() != id || step == last) return FALSE;
    switch (id)
    {
    case FIELD_REQUEST_GRASSLAND:
        return GetSetPokedexFlag(step ? NATIONAL_DEX_ZIGZAGOON : NATIONAL_DEX_POOCHYENA, FLAG_GET_CAUGHT);
    case FIELD_REQUEST_FOREST:
    case FIELD_REQUEST_COAST:
        return NoteBits() & (1u << id);
    case FIELD_REQUEST_BERRIES: return CheckBagHasItem(ITEM_ORAN_BERRY, 3);
    case FIELD_REQUEST_RECOVERY: return PartyHasDrain();
    case FIELD_REQUEST_TEAM: return PartyHasTypes(3);
    }
    switch (sRequests[id].proof)
    {
    case PROOF_HABITAT_TYPE: case PROOF_HABITAT_SPECIES: return NoteBits() & (1u << id);
    case PROOF_CAUGHT_PAIR: return GetSetPokedexFlag(step ? sRequests[id].second : sRequests[id].arg, FLAG_GET_CAUGHT);
    case PROOF_MOVE: return PartyKnows(sRequests[id].arg);
    case PROOF_TYPES: return PartyHasTypes(sRequests[id].arg);
    case PROOF_DEX_COUNT: return GetHoennPokedexCount(FLAG_GET_CAUGHT) >= sRequests[id].arg;
    }
    return FALSE;
}

static bool32 Ready(u16 id)
{
    return id < LEGENDS_FIELD_REQUEST_COUNT && LegendsFieldRequestStepComplete(id, 0)
        && ((id != FIELD_REQUEST_GRASSLAND && sRequests[id].proof != PROOF_CAUGHT_PAIR) || LegendsFieldRequestStepComplete(id, 1));
}

u8 LegendsFieldRequestAccept(u16 id)
{
    if (id >= LEGENDS_FIELD_REQUEST_COUNT || !FlagGet(FLAG_SYS_POKEDEX_GET) || IsOverworldLinkActive()) return FIELD_REQUEST_INVALID;
    if (LegendsFieldRequestActive() != FIELD_REQUEST_NONE) return FIELD_REQUEST_BUSY;
    if (LegendsFieldRequestComplete(id)) return FIELD_REQUEST_FINISHED;
    if (!LegendsFieldRequestUnlocked(id)) return FIELD_REQUEST_LOCKED;
    EnsureCurrentState();
    SetNotes(0);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, REQUEST_SIGNATURE | (id + 1));
    // Respect a previously pinned main/side quest; otherwise pin this request.
    if (LegendsQuestTracked() == 0xFFFF) LegendsQuestTrack(LEGENDS_FIELD_REQUEST_QUEST_BASE + id);
    return FIELD_REQUEST_OK;
}

bool32 LegendsFieldRequestAbandon(void)
{
    if (LegendsFieldRequestActive() == FIELD_REQUEST_NONE || IsOverworldLinkActive()) return FALSE;
    EnsureCurrentState();
    SetNotes(0);
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
    EnsureCurrentState();
    u32 done = DoneBits() | (1u << id);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE, done);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_DONE_HIGH, done >> 16);
    SetNotes(0);
    VarSet(VAR_LEGENDS_FIELD_REQUEST_STATE, REQUEST_SIGNATURE);
    LegendsJournalRefresh();
    return FIELD_REQUEST_OK;
}

void LegendsFieldRequestsGetActive(void) { gSpecialVar_Result = LegendsFieldRequestActive(); }
void LegendsFieldRequestsBeginBirch(void) { sPatron = FIELD_PATRON_BIRCH; sGroup = 0; }
void LegendsFieldRequestsBeginDevon(void) { sPatron = FIELD_PATRON_DEVON; sGroup = 0; }
void LegendsFieldRequestsGetPatron(void) { gSpecialVar_Result = sPatron; }
// Presentation only: count the patron's existing, signed completion bits.
void LegendsFieldRequestsResearchNotes(void)
{
    u16 id = sPatron == FIELD_PATRON_DEVON ? LEGENDS_BIRCH_REQUEST_COUNT : 0;
    u16 end = sPatron == FIELD_PATRON_DEVON ? LEGENDS_FIELD_REQUEST_COUNT : LEGENDS_BIRCH_REQUEST_COUNT;
    u8 completed = 0;
    for (; id < end; id++)
        if (LegendsFieldRequestComplete(id))
            completed++;
    if (completed == (sPatron == FIELD_PATRON_DEVON ? 12 : 18))
        gSpecialVar_Result = 3;
    else if (completed >= (sPatron == FIELD_PATRON_DEVON ? 6 : 9))
        gSpecialVar_Result = 2;
    else
        gSpecialVar_Result = completed >= 3 ? 1 : 0;
}
void LegendsFieldRequestsCanReview(void) { u16 id = LegendsFieldRequestActive(); gSpecialVar_Result = id != FIELD_REQUEST_NONE && LegendsFieldRequestOwner(id) == sPatron; }
void LegendsFieldRequestsSelectGroup(void)
{
    gSpecialVar_Result = gSpecialVar_0x8004 < (sPatron == FIELD_PATRON_BIRCH ? 3 : 2);
    if (gSpecialVar_Result) sGroup = gSpecialVar_0x8004;
}
void LegendsFieldRequestsSelectRow(void)
{
    u16 id = (sPatron == FIELD_PATRON_BIRCH ? 0 : LEGENDS_BIRCH_REQUEST_COUNT) + sGroup * LEGENDS_REQUEST_PAGE_SIZE + gSpecialVar_0x8004;
    gSpecialVar_Result = gSpecialVar_0x8004 < LEGENDS_REQUEST_PAGE_SIZE && id < LEGENDS_FIELD_REQUEST_COUNT && LegendsFieldRequestOwner(id) == sPatron;
    gSpecialVar_0x8004 = id;
}
void LegendsFieldRequestsAcceptSpecial(void)
{
    gSpecialVar_Result = LegendsFieldRequestOwner(gSpecialVar_0x8004) == sPatron ? LegendsFieldRequestAccept(gSpecialVar_0x8004) : FIELD_REQUEST_INVALID;
}
void LegendsFieldRequestsSubmitSpecial(void)
{
    gSpecialVar_Result = LegendsFieldRequestOwner(LegendsFieldRequestActive()) == sPatron ? LegendsFieldRequestSubmit() : FIELD_REQUEST_INVALID;
}
void LegendsFieldRequestsAbandonSpecial(void)
{
    gSpecialVar_Result = LegendsFieldRequestOwner(LegendsFieldRequestActive()) == sPatron && LegendsFieldRequestAbandon();
}
void LegendsFieldRequestsGreeting(void)
{
    StringCopy(gStringVar2, sPatron == FIELD_PATRON_BIRCH ? COMPOUND_STRING("BIRCH") : COMPOUND_STRING("MR. STONE"));
    StringCopy(gStringVar4, sPatron == FIELD_PATRON_BIRCH
        ? COMPOUND_STRING("BIRCH: Good to see you!\nWhat would you like to work on?\pNew field requests become available\nas you explore more of HOENN.")
        : COMPOUND_STRING("MR. STONE: Welcome back!\nHow can DEVON help you today?\pOur research contracts open as your\njourney takes you farther afield."));
}
void LegendsFieldRequestsPrepareMenu(void)
{
    u8 i;
    for (i = 0; i < LEGENDS_REQUEST_PAGE_SIZE; i++)
    {
        u16 id = (sPatron == FIELD_PATRON_BIRCH ? 0 : LEGENDS_BIRCH_REQUEST_COUNT) + sGroup * LEGENDS_REQUEST_PAGE_SIZE + i;
        StringCopy(gLegendsFieldRequestMenuLabels[i], LegendsFieldRequestComplete(id) ? COMPOUND_STRING("Done: ")
            : !LegendsFieldRequestUnlocked(id) ? COMPOUND_STRING("Later: ") : COMPOUND_STRING(""));
        StringAppend(gLegendsFieldRequestMenuLabels[i], sRequests[id].title);
    }
}
void LegendsFieldRequestsDescribe(void)
{
    u16 id = gSpecialVar_0x8004;
    gSpecialVar_Result = TRUE;
    if (id >= LEGENDS_FIELD_REQUEST_COUNT) { StringCopy(gStringVar4, COMPOUND_STRING("Let's look at the list again.")); return; }
    if (LegendsFieldRequestComplete(id)) StringCopy(gStringVar4, COMPOUND_STRING("We've already finished that\nrequest. Thank you for your help!"));
    else if (!LegendsFieldRequestUnlocked(id))
    {
        StringCopy(gStringVar4, COMPOUND_STRING("This work will be available later.\p"));
        StringAppend(gStringVar4, sRequests[id].gateText ? sRequests[id].gateText : COMPOUND_STRING("Receive your POKéDEX first."));
    }
    else { gSpecialVar_Result = FALSE; StringCopy(gStringVar4, sRequests[id].description); }
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
