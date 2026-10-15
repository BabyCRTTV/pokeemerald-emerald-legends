#include "global.h"
#include "legends_homecoming.h"
#include "event_data.h"
#include "event_object_movement.h"
#include "string_util.h"
#include "constants/flags.h"
#include "constants/maps.h"
#include "constants/vars.h"

// Reuse one previously unreferenced native variable, without changing saves.
// 0xD6 signature; bits 0..2 Mom, 3..5 Norman, bit 6 family scene completed.
// Invalid/legacy values are read as unseen without writing to the save.
#define MEMORY_SIGNATURE 0xD600
#define FAMILY_SEEN 0x40

static u16 ReadMemory(void)
{
    u16 value = VarGet(VAR_LEGENDS_HOMECOMING_MEMORY);
    if ((value & 0xFF80) != MEMORY_SIGNATURE || (value & 7) > 6 || ((value >> 3) & 7) > 4)
        return 0;
    return value & 0x7F;
}

static u8 MomStage(void)
{
    if (FlagGet(FLAG_LEGENDS_FINAL_HOENN_EPILOGUE)) return 6;
    if (FlagGet(FLAG_LEGENDS_KANTO_WELCOMED)) return 5;
    if (FlagGet(FLAG_SYS_GAME_CLEAR)) return 4;
    if (FlagGet(FLAG_BADGE05_GET)) return 3;
    if (FlagGet(FLAG_BADGE01_GET)) return 2;
    if (FlagGet(FLAG_RESCUED_BIRCH)) return 1;
    return 0;
}

static u8 DadStage(void)
{
    if (FlagGet(FLAG_LEGENDS_FINAL_HOENN_EPILOGUE)) return 4;
    if (FlagGet(FLAG_LEGENDS_KANTO_WELCOMED)) return 3;
    if (FlagGet(FLAG_SYS_GAME_CLEAR)) return 2;
    if (FlagGet(FLAG_BADGE05_GET)) return 1;
    return 0;
}

static bool32 OwnHouse(void)
{
    return gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F)
        && gSaveBlock1Ptr->location.mapNum == (gSaveBlock2Ptr->playerGender == MALE
            ? MAP_NUM(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F)
            : MAP_NUM(MAP_LITTLEROOT_TOWN_MAYS_HOUSE_1F));
}

static bool32 DadInGym(void)
{
    return gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_PETALBURG_CITY_GYM)
        && gSaveBlock1Ptr->location.mapNum == MAP_NUM(MAP_PETALBURG_CITY_GYM);
}

void LegendsHomecomingMomMessage(void)
{
    static const u8 *const texts[] = {
        NULL,
        COMPOUND_STRING("MOM: Take your time out there.\nYou don't have to go far today.\pI'll be here when you get back."),
        COMPOUND_STRING("MOM: I still listen for your steps\nat the door around suppertime.\pIt's good to hear them again."),
        COMPOUND_STRING("MOM: Your dad told me about your\nbattle. Every turn of it!\pI think he's told me three times now."),
        COMPOUND_STRING("MOM: Everyone asks what it's like\nto have a CHAMPION in the family.\pI tell them I'm happy you're home."),
        COMPOUND_STRING("MOM: KANTO sounds so far away\nwhen I look at it on the map.\pWill you tell me about the crossing?"),
        COMPOUND_STRING("MOM: You can leave the unpacking\nuntil tomorrow.\pStay a little while, won't you?"),
    };
    u8 stage = MomStage();
    gSpecialVar_Result = OwnHouse() && stage > (ReadMemory() & 7);
    if (gSpecialVar_Result) StringCopy(gStringVar4, texts[stage]);
}

void LegendsHomecomingRememberMom(void)
{
    u16 memory = ReadMemory();
    u8 stage = MomStage();
    if (OwnHouse() && stage > (memory & 7))
        VarSet(VAR_LEGENDS_HOMECOMING_MEMORY, MEMORY_SIGNATURE | (memory & ~7) | stage);
}

void LegendsHomecomingDadMessage(void)
{
    static const u8 *const texts[] = {
        NULL,
        COMPOUND_STRING("DAD: I went over our battle again\nafter the GYM had closed.\pYou made your own decisions.\nThat meant a great deal to me."),
        COMPOUND_STRING("DAD: I knew you could reach the\nLEAGUE. Still, when the news came…\pI had to sit down for a moment.\nYour mother laughed at me."),
        COMPOUND_STRING("DAD: How are the GYMS in KANTO?\nI'd like to hear about them.\pThough your mother says I should\nask about the rest of your trip too."),
        COMPOUND_STRING("DAD: You've seen places I've only\nread about.\pNext time you're home, bring a map.\nYou can show me where you went."),
    };
    u8 stage = DadStage();
    gSpecialVar_Result = DadInGym() && stage > ((ReadMemory() >> 3) & 7);
    if (gSpecialVar_Result) StringCopy(gStringVar4, texts[stage]);
}

void LegendsHomecomingRememberDad(void)
{
    u16 memory = ReadMemory();
    u8 stage = DadStage();
    if (DadInGym() && stage > ((memory >> 3) & 7))
        VarSet(VAR_LEGENDS_HOMECOMING_MEMORY, MEMORY_SIGNATURE | (memory & ~0x38) | (stage << 3));
}

static bool32 FamilyReady(void)
{
    // The ticket and TV sequence must finish first, even on a prepared old save.
    return OwnHouse() && FlagGet(FLAG_LEGENDS_FINAL_HOENN_EPILOGUE)
        && FlagGet(FLAG_RECEIVED_SS_TICKET)
        && VarGet(VAR_LITTLEROOT_HOUSES_STATE_MAY) == 4
        && VarGet(VAR_LITTLEROOT_HOUSES_STATE_BRENDAN) == 4
        && !(ReadMemory() & FAMILY_SEEN);
}

void LegendsHomecomingReady(void)
{
    gSpecialVar_Result = FamilyReady();
}

void LegendsHomecomingShowDad(void)
{
    gSpecialVar_Result = FamilyReady()
        && TrySpawnObjectEvent(gSpecialVar_0x8004, gSaveBlock1Ptr->location.mapNum,
            gSaveBlock1Ptr->location.mapGroup) != OBJECT_EVENTS_COUNT;
}

void LegendsHomecomingFinish(void)
{
    if (FamilyReady())
        VarSet(VAR_LEGENDS_HOMECOMING_MEMORY, MEMORY_SIGNATURE | FAMILY_SEEN | MomStage() | (DadStage() << 3));
}
