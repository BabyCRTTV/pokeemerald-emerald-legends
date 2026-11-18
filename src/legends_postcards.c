#include "global.h"
#include "main.h"
#include "constants/rgb.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "field_specials.h"
#include "fieldmap.h"
#include "legends_seasons.h"
#include "menu.h"
#include "palette.h"
#include "pokemon.h"
#include "pokemon_icon.h"
#include "rtc.h"
#include "script.h"
#include "sound.h"
#include "string_util.h"
#include "task.h"
#include "window.h"
#include "constants/maps.h"
#include "constants/songs.h"

static const u8 sPrintOldaleTown[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/OldaleTown.bin");
static const u8 sPrintPetalburgCity[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/PetalburgCity.bin");
static const u8 sPrintRoute104[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/Route104.bin");
static const u8 sPrintDewfordTown[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/DewfordTown.bin");
static const u8 sPrintSlateportCity[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/SlateportCity.bin");
static const u8 sPrintMauvilleCity[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/MauvilleCity.bin");
static const u8 sPrintVerdanturfTown[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/VerdanturfTown.bin");
static const u8 sPrintFallarborTown[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/FallarborTown.bin");
static const u8 sPrintLavaridgeTown[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/LavaridgeTown.bin");
static const u8 sPrintRoute119[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/Route119.bin");
static const u8 sPrintFortreeCity[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/FortreeCity.bin");
static const u8 sPrintRoute120[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/Route120.bin");
static const u8 sPrintLilycoveCity[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/LilycoveCity.bin");
static const u8 sPrintMossdeepCity[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/MossdeepCity.bin");
static const u8 sPrintSootopolisCity[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/SootopolisCity.bin");
static const u8 sPrintPacifidlogTown[] ALIGNED(4) = INCBIN_U8("graphics/legends/postcards/PacifidlogTown.bin");

static const struct PhotoSpot
{
    u8 group, map, x, y;
    const u8 *caption, *print;
} sSpots[] = {
    {MAP_GROUP(MAP_OLDALE_TOWN), MAP_NUM(MAP_OLDALE_TOWN), 11, 9, COMPOUND_STRING("Oldale Crossroads"), sPrintOldaleTown},
    {MAP_GROUP(MAP_PETALBURG_CITY), MAP_NUM(MAP_PETALBURG_CITY), 17, 16, COMPOUND_STRING("Petalburg Gardens"), sPrintPetalburgCity},
    {MAP_GROUP(MAP_ROUTE104), MAP_NUM(MAP_ROUTE104), 7, 20, COMPOUND_STRING("Flower Shop Lane"), sPrintRoute104},
    {MAP_GROUP(MAP_DEWFORD_TOWN), MAP_NUM(MAP_DEWFORD_TOWN), 10, 10, COMPOUND_STRING("Island Village"), sPrintDewfordTown},
    {MAP_GROUP(MAP_SLATEPORT_CITY), MAP_NUM(MAP_SLATEPORT_CITY), 24, 12, COMPOUND_STRING("Slateport Harbor"), sPrintSlateportCity},
    {MAP_GROUP(MAP_MAUVILLE_CITY), MAP_NUM(MAP_MAUVILLE_CITY), 33, 6, COMPOUND_STRING("Cycles of Mauville"), sPrintMauvilleCity},
    {MAP_GROUP(MAP_VERDANTURF_TOWN), MAP_NUM(MAP_VERDANTURF_TOWN), 7, 3, COMPOUND_STRING("Tunnel Mouth"), sPrintVerdanturfTown},
    {MAP_GROUP(MAP_FALLARBOR_TOWN), MAP_NUM(MAP_FALLARBOR_TOWN), 10, 11, COMPOUND_STRING("Ashfall Village"), sPrintFallarborTown},
    {MAP_GROUP(MAP_LAVARIDGE_TOWN), MAP_NUM(MAP_LAVARIDGE_TOWN), 13, 8, COMPOUND_STRING("Hot Spring Hollow"), sPrintLavaridgeTown},
    {MAP_GROUP(MAP_ROUTE119), MAP_NUM(MAP_ROUTE119), 9, 33, COMPOUND_STRING("Rainforest Station"), sPrintRoute119},
    {MAP_GROUP(MAP_FORTREE_CITY), MAP_NUM(MAP_FORTREE_CITY), 6, 9, COMPOUND_STRING("Treetop Walk"), sPrintFortreeCity},
    {MAP_GROUP(MAP_ROUTE120), MAP_NUM(MAP_ROUTE120), 27, 3, COMPOUND_STRING("Eastern Trail"), sPrintRoute120},
    {MAP_GROUP(MAP_LILYCOVE_CITY), MAP_NUM(MAP_LILYCOVE_CITY), 19, 7, COMPOUND_STRING("Museum Terrace"), sPrintLilycoveCity},
    {MAP_GROUP(MAP_MOSSDEEP_CITY), MAP_NUM(MAP_MOSSDEEP_CITY), 66, 16, COMPOUND_STRING("Space Center Hill"), sPrintMossdeepCity},
    {MAP_GROUP(MAP_SOOTOPOLIS_CITY), MAP_NUM(MAP_SOOTOPOLIS_CITY), 41, 37, COMPOUND_STRING("Crater Shores"), sPrintSootopolisCity},
    {MAP_GROUP(MAP_PACIFIDLOG_TOWN), MAP_NUM(MAP_PACIFIDLOG_TOWN), 7, 16, COMPOUND_STRING("Floating Village"), sPrintPacifidlogTown},
};

static const u8 sSignature[] = {'P','C','1','6'};
static const u8 *const sLight[] = {COMPOUND_STRING("Morning"), COMPOUND_STRING("Day"), COMPOUND_STRING("Evening"), COMPOUND_STRING("Night")};
static const struct WindowTemplate sPhoto = {0, 5, 3, 20, 10, 13, 1};
static const struct WindowTemplate sLabel = {0, 5, 13, 20, 5, 15, 201};
static EWRAM_DATA u16 sOldPalette[16] = {};
static EWRAM_DATA u8 sCurrent = 0;

static bool32 HasAlbum(void)
{
    return !memcmp(gSaveBlock1Ptr->postcardMagic, sSignature, sizeof(sSignature));
}

void PostcardFindSite(void)
{
    s16 x, y;
    u32 i;
    GetXYCoordsOneStepInFrontOfPlayer(&x, &y);
    gSpecialVar_Result = FALSE;
    for (i = 0; i < ARRAY_COUNT(sSpots); i++)
    {
        const struct PhotoSpot *spot = &sSpots[i];
        if (gSaveBlock1Ptr->location.mapGroup == spot->group && gSaveBlock1Ptr->location.mapNum == spot->map
         && x == spot->x + MAP_OFFSET && y == spot->y + MAP_OFFSET)
        {
            sCurrent = i;
            gSpecialVar_Result = TRUE;
            return;
        }
    }
}

void PostcardCapture(void)
{
    u8 *record;
    u16 species = GetMonData(&gParties[B_TRAINER_PLAYER][GetLeadMonIndex()], MON_DATA_SPECIES_OR_EGG);
    PostcardFindSite();
    if (!gSpecialVar_Result || species == SPECIES_NONE || species >= NUM_SPECIES)
    {
        gSpecialVar_Result = FALSE;
        return;
    }
    if (!HasAlbum())
    {
        memset(gSaveBlock1Ptr->postcardRecords, 0, sizeof(gSaveBlock1Ptr->postcardRecords));
        memcpy(gSaveBlock1Ptr->postcardMagic, sSignature, sizeof(sSignature));
    }
    record = gSaveBlock1Ptr->postcardRecords[sCurrent];
    record[0] = species;
    record[1] = species >> 8;
    record[2] = LegendsGetActiveSeason() | (GetTimeOfDay() << 2);
}

static u16 PhotoSpecies(u8 slot)
{
    const u8 *record = gSaveBlock1Ptr->postcardRecords[slot];
    u16 species = record[0] | (record[1] << 8);
    return species < NUM_SPECIES ? species : SPECIES_NONE;
}

void PostcardOpen(void)
{
    gSpecialVar_Result = FALSE;
    if (HasAlbum())
        for (sCurrent = 0; sCurrent < ARRAY_COUNT(sSpots); sCurrent++)
            if (PhotoSpecies(sCurrent))
            {
                gSpecialVar_Result = TRUE;
                return;
            }
}

static void RemovePartner(struct Task *task)
{
    if (task->data[2] < MAX_SPRITES)
    {
        FreeAndDestroyMonIconSprite(&gSprites[task->data[2]]);
        SafeFreeMonIconPalette(task->data[3]);
        task->data[2] = MAX_SPRITES;
    }
}

static void DrawPrint(struct Task *task)
{
    const struct PhotoSpot *spot = &sSpots[sCurrent];
    u8 stamp = gSaveBlock1Ptr->postcardRecords[sCurrent][2];
    u8 picture = task->data[0], label = task->data[1];
    u16 species = PhotoSpecies(sCurrent), colors[16];
    u8 i, *end;
    RemovePartner(task);
    memcpy(colors, spot->print, sizeof(colors));
    for (i = 1; i < ARRAY_COUNT(colors); i++)
    {
        u16 color = LegendsSeasonVegetationColor(colors[i], stamp & 3);
        u8 r = color & 31, g = (color >> 5) & 31, b = color >> 10;
        if ((stamp >> 2) == TIME_NIGHT)
            color = RGB(r / 2, g / 2, (b + 8) * 2 / 3);
        else if ((stamp >> 2) == TIME_EVENING)
            color = RGB((r * 3 + 31) / 4, g * 7 / 8, b * 3 / 4);
        colors[i] = color;
    }
    LoadPalette(colors, BG_PLTT_ID(13), sizeof(colors));
    BlitBitmapRectToWindow(picture, spot->print + sizeof(colors), 0, 0, 160, 80, 0, 0, 160, 80);
    FillWindowPixelBuffer(label, PIXEL_FILL(1));
    AddTextPrinterParameterized(label, FONT_NORMAL, spot->caption, 3, 0, TEXT_SKIP_DRAW, NULL);
    end = StringCopy(gStringVar4, LegendsGetSeasonName(stamp & 3));
    end = StringCopy(end, COMPOUND_STRING("  "));
    StringCopy(end, sLight[(stamp >> 2) & 3]);
    AddTextPrinterParameterized(label, FONT_SMALL, gStringVar4, 3, 15, TEXT_SKIP_DRAW, NULL);
    AddTextPrinterParameterized(label, FONT_SMALL, COMPOUND_STRING("{LEFT_ARROW}{RIGHT_ARROW} Browse    B Close"), 3, 27, TEXT_SKIP_DRAW, NULL);
    PutWindowTilemap(picture);
    PutWindowTilemap(label);
    CopyWindowToVram(picture, COPYWIN_FULL);
    CopyWindowToVram(label, COPYWIN_FULL);
    LoadMonIconPalette(species);
    task->data[2] = CreateMonIconNoPersonality(species, SpriteCB_MonIcon, 135, 86, 0);
    task->data[3] = species;
    if (task->data[2] < MAX_SPRITES)
        gSprites[task->data[2]].oam.priority = 0;
}

static void Task_BrowsePrints(u8 taskId)
{
    struct Task *task = &gTasks[taskId];
    if (JOY_NEW(B_BUTTON | A_BUTTON))
    {
        RemovePartner(task);
        LoadPalette(sOldPalette, BG_PLTT_ID(13), sizeof(sOldPalette));
        ClearStdWindowAndFrameToTransparent(task->data[0], TRUE);
        ClearStdWindowAndFrameToTransparent(task->data[1], TRUE);
        RemoveWindow(task->data[0]);
        RemoveWindow(task->data[1]);
        DestroyTask(taskId);
        ScriptContext_Enable();
    }
    else if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        u8 delta = JOY_NEW(DPAD_RIGHT) ? 1 : ARRAY_COUNT(sSpots) - 1;
        do
            sCurrent = (sCurrent + delta) % ARRAY_COUNT(sSpots);
        while (!PhotoSpecies(sCurrent));
        PlaySE(SE_SELECT);
        DrawPrint(task);
    }
}

static void ResumeField(u8 taskId)
{
    DestroyTask(taskId);
    ScriptContext_Enable();
}

void PostcardView(void)
{
    u8 taskId = CreateTask(Task_BrowsePrints, 0x50);
    struct Task *task = &gTasks[taskId];
    task->data[0] = AddWindow(&sPhoto);
    task->data[1] = AddWindow(&sLabel);
    task->data[2] = MAX_SPRITES;
    if (task->data[0] == WINDOW_NONE || task->data[1] == WINDOW_NONE)
    {
        if (task->data[0] != WINDOW_NONE)
            RemoveWindow(task->data[0]);
        if (task->data[1] != WINDOW_NONE)
            RemoveWindow(task->data[1]);
        task->func = ResumeField;
        return;
    }
    memcpy(sOldPalette, &gPlttBufferUnfaded[BG_PLTT_ID(13)], sizeof(sOldPalette));
    DrawStdWindowFrame(task->data[0], FALSE);
    DrawStdWindowFrame(task->data[1], FALSE);
    DrawPrint(task);
}
