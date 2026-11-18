#include "global.h"
#include "bg.h"
#include "gpu_regs.h"
#include "overworld.h"
#include "scanline_effect.h"
#include "main.h"
#include "constants/rgb.h"
#include "event_data.h"
#include "field_player_avatar.h"
#include "field_specials.h"
#include "fieldmap.h"
#include "legends_seasons.h"
#include "menu.h"
#include "malloc.h"
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
// The print uses 8bpp tiles in character block 2. The paper and lettering
// use a separate 4bpp layer and palette 15, so browsing cannot recolor them.
static const struct BgTemplate sLayers[] = {
    {.bg = 0, .mapBaseIndex = 31},
    {.bg = 1, .charBaseIndex = 2, .mapBaseIndex = 30, .paletteMode = 1, .priority = 1},
};
static const struct WindowTemplate sPaper[] = {
    {.width = 30, .height = 20, .paletteNum = 15, .baseBlock = 1}, DUMMY_WIN_TEMPLATE
};
static const u16 sPaperColors[16] = {
    RGB(5,8,9), RGB(31,30,26), RGB(5,10,11), RGB(15,16,14),
    RGB(10,14,14), RGB(23,23,19), RGB(27,26,22), RGB(18,8,6), RGB(29,28,24),
};
static const u8 sPartnerPosition[][2] = {
    {140,99}, {96,91}, {103,96}, {124,94}, {105,100}, {151,101},
    {153,95}, {79,93}, {109,103}, {137,102}, {143,72}, {129,78},
    {101,105}, {112,105}, {66,98}, {81,85},
};
static EWRAM_DATA u8 sPartner = 0;
static EWRAM_DATA u32 *sPhotoTiles = NULL;
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

enum { PRINT_WIDTH = 28, PRINT_HEIGHT = 14, PRINT_PALETTE = 224, PRINT_BYTES = PRINT_WIDTH * PRINT_HEIGHT * 64 };

static void Text(const u8 *text, u8 font, u8 x, u8 y, u8 ink)
{
    const u8 colors[] = {0, ink, 0};
    AddTextPrinterParameterized3(0, font, x, y, colors, TEXT_SKIP_DRAW, text);
}

static void DrawPaper(void)
{
    FillWindowPixelBuffer(0, PIXEL_FILL(4));
    FillWindowPixelRect(0, 1, 4, 3, 232, 151);
    FillWindowPixelRect(0, 5, 7, 7, 226, 114);
    FillWindowPixelRect(0, 0, 8, 8, 224, 112);
    FillWindowPixelRect(0, 5, 9, 139, 222, 1);
    // Perforated stamp edge around the postcard number.
    FillWindowPixelRect(0, 6, 196, 122, 33, 16);
    for (u8 x = 198; x < 228; x += 4)
    {
        FillWindowPixelRect(0, 1, x, 122, 2, 1);
        FillWindowPixelRect(0, 1, x, 137, 2, 1);
    }
    ConvertIntToDecimalStringN(gStringVar1, sCurrent + 1, STR_CONV_MODE_LEADING_ZEROS, 2);
    StringAppend(gStringVar1, COMPOUND_STRING("/16"));
    Text(gStringVar1, FONT_SMALL, 199, 123, 7);
    Text(sSpots[sCurrent].caption, FONT_NORMAL, 10, 121, 2);
    u8 stamp = gSaveBlock1Ptr->postcardRecords[sCurrent][2];
    u8 *end = StringCopy(gStringVar4, LegendsGetSeasonName(stamp & 3));
    end = StringCopy(end, COMPOUND_STRING(" / "));
    StringCopy(end, sLight[(stamp >> 2) & 3]);
    Text(gStringVar4, FONT_SMALL, 10, 140, 2);
    Text(COMPOUND_STRING("{LEFT_ARROW}{RIGHT_ARROW} Browse    B Close"), FONT_SMALL, 141, 140, 4);
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void DrawPrint(void)
{
    const u8 *print = sSpots[sCurrent].print;
    const u16 *source = (const u16 *)print;
    u8 stamp = gSaveBlock1Ptr->postcardRecords[sCurrent][2];
    u16 colors[PRINT_PALETTE];
    u16 species = PhotoSpecies(sCurrent);
    for (u16 i = 0; i < PRINT_PALETTE; i++)
    {
        u16 color = LegendsSeasonVegetationColor(source[i], stamp & 3);
        u8 r = color & 31, g = (color >> 5) & 31, b = color >> 10;
        if ((stamp >> 2) == TIME_NIGHT)
            color = RGB(r / 2, g / 2, (b + 8) * 2 / 3);
        else if ((stamp >> 2) == TIME_EVENING)
            color = RGB((r * 3 + 31) / 4, g * 7 / 8, b * 3 / 4);
        colors[i] = color;
    }
    LoadPalette(colors, 0, sizeof(colors));
    LZ77UnCompWram((const u32 *)(print + sizeof(colors)), sPhotoTiles);
    LoadBgTiles(1, sPhotoTiles, PRINT_BYTES, 1);
    DrawPaper();
    LoadMonIconPalette(species);
    sPartner = CreateMonIconNoPersonality(species, SpriteCallbackDummy,
        sPartnerPosition[sCurrent][0], sPartnerPosition[sCurrent][1], 0);
    if (sPartner < MAX_SPRITES)
    {
        UpdateMonIconFrame(&gSprites[sPartner]);
        gSprites[sPartner].oam.priority = 0;
    }
}

static void RemovePartner(void)
{
    if (sPartner < MAX_SPRITES)
        FreeAndDestroyMonIconSprite(&gSprites[sPartner]);
    SafeFreeMonIconPalette(PhotoSpecies(sCurrent));
    sPartner = MAX_SPRITES;
}

static void VBlank(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void TurnPage(void)
{
    u8 delta = JOY_NEW(DPAD_RIGHT) ? 1 : ARRAY_COUNT(sSpots) - 1;
    RemovePartner();
    do
        sCurrent = (sCurrent + delta) % ARRAY_COUNT(sSpots);
    while (!PhotoSpecies(sCurrent));
    PlaySE(SE_SELECT);
    DrawPrint();
}

static void CaseMain(void)
{
    if (JOY_NEW(B_BUTTON | A_BUTTON))
    {
        RemovePartner();
        Free(sPhotoTiles);
        sPhotoTiles = NULL;
        SetVBlankCallback(NULL);
        FreeAllWindowBuffers();
        SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
        return;
    }
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
        TurnPage();
    AnimateSprites();
    BuildOamBuffer();
}

static void InitCase(void)
{
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_FORCED_BLANK);
    ScanlineEffect_Stop();
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    DmaClear32(3, OAM, OAM_SIZE);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sLayers, ARRAY_COUNT(sLayers));
    for (u8 bg = 0; bg < 2; bg++)
    {
        ChangeBgX(bg, 0, BG_COORD_SET);
        ChangeBgY(bg, 0, BG_COORD_SET);
    }
    ResetPaletteFade();
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    sPhotoTiles = AllocZeroedUnchecked(PRINT_BYTES);
    if (!InitWindowsUnchecked(sPaper) || sPhotoTiles == NULL)
    {
        if (sPhotoTiles != NULL)
            Free(sPhotoTiles);
        sPhotoTiles = NULL;
        FreeAllWindowBuffers();
        SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
        return;
    }
    DeactivateAllTextPrinters();
    u16 *map = (u16 *)BG_SCREEN_ADDR(30);
    for (u8 y = 0; y < PRINT_HEIGHT; y++)
        for (u8 x = 0; x < PRINT_WIDTH; x++)
            map[(y + 1) * 32 + x + 1] = y * PRINT_WIDTH + x + 1;
    LoadPalette(sPaperColors, BG_PLTT_ID(15), sizeof(sPaperColors));
    DrawPrint();
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    ShowBg(0);
    ShowBg(1);
    SetVBlankCallback(VBlank);
    SetMainCallback2(CaseMain);
}

void PostcardView(void)
{
    CleanupOverworldWindowsAndTilemaps();
    SetMainCallback2(InitCase);
}
