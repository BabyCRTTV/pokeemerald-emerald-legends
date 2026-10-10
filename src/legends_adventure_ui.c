#include "global.h"
#include "legends_adventure.h"
#include "main.h"
#include "bg.h"
#include "dma3.h"
#include "gpu_regs.h"
#include "palette.h"
#include "window.h"
#include "text.h"
#include "task.h"
#include "sprite.h"
#include "sound.h"
#include "overworld.h"
#include "string_util.h"
#include "region_map.h"
#include "pokemon.h"
#include "scanline_effect.h"
#include "constants/rgb.h"
#include "constants/characters.h"
#include "constants/songs.h"

static const struct BgTemplate sBg[] =
{
    {.bg = 0, .charBaseIndex = 0, .mapBaseIndex = 31, .priority = 0},
};
static const struct WindowTemplate sWindows[] =
{
    {.bg = 0, .tilemapLeft = 0, .tilemapTop = 0, .width = 30, .height = 20, .paletteNum = 15, .baseBlock = 1},
    DUMMY_WIN_TEMPLATE,
};
static const u16 sPaperPalette[] =
{
    RGB(18,15,21), RGB(31,29,24), RGB(8,7,10), RGB(26,23,21),
    RGB(28,25,23), RGB(24,18,18), RGB(23,20,28), RGB(30,27,30),
    RGB(15,12,18), RGB(31,30,27), RGB(20,18,23), RGB(25,21,22),
    RGB(31,29,24), RGB(31,29,24), RGB(31,29,24), RGB(31,29,24),
};
static const u8 sInk[] = {1, 2, 3};
static const u8 sAccent[] = {1, 8, 3};
static const u8 *const sNotes[ADV_EVENT_COUNT] =
{
    [ADV_BEGIN] = COMPOUND_STRING("A new adventure begins.\nThere's a whole world to meet."),
    [ADV_RESUME] = COMPOUND_STRING("Picking up the adventure.\nYour notebook remembers."),
    [ADV_CHECKPOINT] = COMPOUND_STRING("A quiet moment on the journey.\nA checkpoint to come back to."),
    [ADV_CATCH] = COMPOUND_STRING("Met a new travel companion.\nAnother memory for the notebook."),
    [ADV_POKEDEX] = COMPOUND_STRING("Received the POKEDEX.\nTime to discover HOENN's POKEMON!"),
    [ADV_STEVEN_LETTER] = COMPOUND_STRING("Delivered the letter to STEVEN.\nAn errand worth remembering."),
    [ADV_SPACE_CENTER] = COMPOUND_STRING("Helped STEVEN at the SPACE CENTER.\nTEAM MAGMA's plan was stopped."),
    [ADV_WEATHER_PEACE] = COMPOUND_STRING("RAYQUAZA calmed the weather crisis.\nPeace returned to SOOTOPOLIS."),
    [ADV_BADGE1] = COMPOUND_STRING("Earned the STONE BADGE.\nROXANNE's challenge is complete."),
    [ADV_BADGE2] = COMPOUND_STRING("Earned the KNUCKLE BADGE.\nBRAWLY's challenge is complete."),
    [ADV_BADGE3] = COMPOUND_STRING("Earned the DYNAMO BADGE.\nWATTSON's challenge is complete."),
    [ADV_BADGE4] = COMPOUND_STRING("Earned the HEAT BADGE.\nFLANNERY's challenge is complete."),
    [ADV_BADGE5] = COMPOUND_STRING("Earned the BALANCE BADGE.\nNORMAN's challenge is complete."),
    [ADV_BADGE6] = COMPOUND_STRING("Earned the FEATHER BADGE.\nWINONA's challenge is complete."),
    [ADV_BADGE7] = COMPOUND_STRING("Earned the MIND BADGE.\nTATE and LIZA's challenge is done."),
    [ADV_BADGE8] = COMPOUND_STRING("Earned the RAIN BADGE.\nJUAN's challenge is complete."),
    [ADV_CHAMPION] = COMPOUND_STRING("Became HOENN's CHAMPION.\nA new chapter opens from here."),
    [ADV_KANTO_ARRIVAL] = COMPOUND_STRING("Arrived in VERMILION, KANTO.\nA welcome across the sea."),
    [ADV_SURVEY_START] = COMPOUND_STRING("Began OAK's WING SURVEY.\nListen to the LEADERS' observations."),
    [ADV_SURGE] = COMPOUND_STRING("Completed LT. SURGE's challenge.\nA report from the POWER PLANT."),
    [ADV_KOGA] = COMPOUND_STRING("Completed KOGA's challenge.\nCold winds near SEAFOAM ISLANDS."),
    [ADV_BROCK] = COMPOUND_STRING("Completed BROCK's challenge.\nAnother KANTO record collected."),
    [ADV_MISTY] = COMPOUND_STRING("Completed MISTY's challenge.\nAnother KANTO record collected."),
    [ADV_ERIKA] = COMPOUND_STRING("Completed ERIKA's challenge.\nAnother KANTO record collected."),
    [ADV_SABRINA] = COMPOUND_STRING("Completed SABRINA's challenge.\nAnother KANTO record collected."),
    [ADV_BLAINE] = COMPOUND_STRING("Completed BLAINE's challenge.\nAnother KANTO record collected."),
    [ADV_VIRIDIAN] = COMPOUND_STRING("Completed the VIRIDIAN challenge.\nAnother KANTO record collected."),
    [ADV_SURVEY_REPORT] = COMPOUND_STRING("Filed the first WING SURVEY report.\nThe birds and MEW remain leads."),
};
static const u8 *const sFilters[] =
{
    COMPOUND_STRING("ALL"), COMPOUND_STRING("DAY"), COMPOUND_STRING("STORY"),
};

EWRAM_DATA static u8 sFilter = 0;
EWRAM_DATA static u8 sPage = 0;
EWRAM_DATA static u16 sDay = 0;

static void Print(const u8 *text, u8 x, u8 y, bool32 small)
{
    AddTextPrinterParameterized3(0, small ? FONT_SMALL : FONT_NORMAL, x, y,
        sInk, TEXT_SKIP_DRAW, text);
}

static void Number(u8 *buffer, u16 number, u8 digits)
{
    ConvertIntToDecimalStringN(buffer, number, STR_CONV_MODE_LEADING_ZEROS, digits);
}

static void DrawPage(void)
{
    const struct LegendsAdventureEntry *entry = LegendsAdventureFiltered(sFilter, sDay, sPage);
    u8 buffer[128], number[16], name[64];
    u8 count = LegendsAdventureCount(sFilter, sDay), row;
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    // Lavender cover, cream paper, rose margin and subtle ruled lines.
    FillWindowPixelRect(0, PIXEL_FILL(6), 0, 0, 8, 160);
    FillWindowPixelRect(0, PIXEL_FILL(7), 8, 0, 232, 20);
    FillWindowPixelRect(0, PIXEL_FILL(5), 17, 37, 1, 99);
    for (row = 40; row <= 136; row += 16)
        FillWindowPixelRect(0, PIXEL_FILL(4), 18, row, 214, 1);
    for (row = 28; row < 140; row += 24)
        FillWindowPixelRect(0, PIXEL_FILL(3), 2, row, 9, 3);
    AddTextPrinterParameterized3(0, FONT_NORMAL, 15, 2, sAccent, TEXT_SKIP_DRAW, COMPOUND_STRING("ADVENTURE LOG"));
    StringCopy(buffer, sFilters[sFilter]);
    StringAppend(buffer, COMPOUND_STRING(" "));
    ConvertIntToDecimalStringN(number, count ? sPage + 1 : 0, STR_CONV_MODE_LEFT_ALIGN, 2);
    StringAppend(buffer, number); StringAppend(buffer, COMPOUND_STRING("/"));
    ConvertIntToDecimalStringN(number, count, STR_CONV_MODE_LEFT_ALIGN, 2);
    StringAppend(buffer, number);
    Print(buffer, 172, 4, TRUE);

    if (entry == NULL)
    {
        Print(COMPOUND_STRING("No notes in this filter yet."), 24, 61, FALSE);
        Print(COMPOUND_STRING("SELECT changes the filter."), 24, 79, FALSE);
    }
    else
    {
        StringCopy(buffer, COMPOUND_STRING("DAY "));
        ConvertIntToDecimalStringN(number, entry->day, STR_CONV_MODE_LEFT_ALIGN, 5);
        StringAppend(buffer, number);
        if (entry->date)
        {
            StringAppend(buffer, COMPOUND_STRING("   "));
            Number(number, (entry->date >> 5) & 15, 2); StringAppend(buffer, number);
            StringAppend(buffer, COMPOUND_STRING("/"));
            Number(number, entry->date & 31, 2); StringAppend(buffer, number);
            StringAppend(buffer, COMPOUND_STRING("/"));
            Number(number, entry->date >> 9, 2); StringAppend(buffer, number);
        }
        else
            StringAppend(buffer, COMPOUND_STRING("   Date unavailable"));
        Print(buffer, 24, 23, TRUE);
        GetMapName(name, entry->region, 0);
        // Variable map names use the smaller native font, with a hard pixel cap.
        while (GetStringWidth(FONT_SMALL, name, 0) > 200)
            name[StringLength(name) - 1] = EOS;
        Print(name, 24, 43, TRUE);
        if (entry->event <= ADV_CHECKPOINT && entry->context >= ADV_POKEDEX && entry->context < ADV_EVENT_COUNT)
        {
            u8 i;
            Print(COMPOUND_STRING("Latest known milestone:"), 24, 60, FALSE);
            StringCopy(buffer, sNotes[entry->context]);
            for (i = 0; buffer[i] != EOS; i++)
                if (buffer[i] == CHAR_NEWLINE)
                {
                    buffer[i] = EOS;
                    break;
                }
            Print(buffer, 24, 76, FALSE);
        }
        else
            Print(sNotes[entry->event < ADV_EVENT_COUNT ? entry->event : ADV_RESUME], 24, 60, FALSE);
        if (entry->species)
        {
            StringCopy(buffer, COMPOUND_STRING("Recent catch: "));
            StringAppend(buffer, GetSpeciesName(entry->species));
            Print(buffer, 24, 96, TRUE);
            StringCopy(buffer, COMPOUND_STRING("Lv. "));
            ConvertIntToDecimalStringN(number, entry->level, STR_CONV_MODE_LEFT_ALIGN, 3);
            StringAppend(buffer, number);
        }
        else
            StringCopy(buffer, COMPOUND_STRING("No recent catch noted."));
        Print(buffer, 24, 108, TRUE);
        StringCopy(buffer, COMPOUND_STRING("Play time: "));
        Number(number, entry->hours, 3); StringAppend(buffer, number);
        StringAppend(buffer, COMPOUND_STRING(":"));
        Number(number, entry->minute, 2); StringAppend(buffer, number);
        Print(buffer, 24, 122, TRUE);
    }
    Print(COMPOUND_STRING("LEFT/RIGHT: Page   UP/DOWN: Day"), 14, 136, TRUE);
    Print(COMPOUND_STRING("SELECT: Filter   A: Newest   B: Close"), 14, 148, TRUE);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void VBlank(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void Main(void)
{
    RunTasks();
    UpdatePaletteFade();
}

static void Task_Close(u8 taskId)
{
    if (!gPaletteFade.active)
    {
        DestroyTask(taskId);
        FreeAllWindowBuffers();
        SetMainCallback2(CB2_ReturnToFieldWithOpenMenu);
    }
}

static void Task_Read(u8 taskId)
{
    u8 count;
    if (gPaletteFade.active)
        return;
    if (JOY_NEW(B_BUTTON | START_BUTTON))
    {
        PlaySE(SE_SELECT);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        gTasks[taskId].func = Task_Close;
        return;
    }
    if (!JOY_NEW(DPAD_LEFT | DPAD_RIGHT | DPAD_UP | DPAD_DOWN | L_BUTTON | R_BUTTON | SELECT_BUTTON | A_BUTTON))
        return;
    if (JOY_NEW(SELECT_BUTTON))
    {
        sFilter = (sFilter + 1) % ADV_FILTER_COUNT;
        sDay = LegendsAdventureDays();
        sPage = 0;
    }
    else if (JOY_NEW(DPAD_UP | DPAD_DOWN))
    {
        const struct LegendsAdventureEntry *entry = LegendsAdventureFiltered(sFilter, sDay, sPage);
        if (sFilter != ADV_FILTER_DAY && entry != NULL)
            sDay = entry->day;
        sFilter = ADV_FILTER_DAY;
        sDay = LegendsAdventureAdjacentDay(sDay, JOY_NEW(DPAD_UP) != 0);
        sPage = 0;
    }
    else if (JOY_NEW(A_BUTTON))
    {
        sDay = LegendsAdventureDays();
        sPage = 0;
    }
    else
    {
        count = LegendsAdventureCount(sFilter, sDay);
        if (JOY_NEW(DPAD_LEFT | L_BUTTON) && sPage + 1 < count)
            sPage++;
        else if (JOY_NEW(DPAD_RIGHT | R_BUTTON) && sPage > 0)
            sPage--;
    }
    PlaySE(SE_SELECT);
    DrawPage();
}

void CB2_OpenAdventureLog(void)
{
    switch (gMain.state)
    {
    case 0:
        SetVBlankCallback(NULL);
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        ResetBgsAndClearDma3BusyFlags(0);
        InitBgsFromTemplates(0, sBg, ARRAY_COUNT(sBg));
        ChangeBgX(0, 0, BG_COORD_SET);
        ChangeBgY(0, 0, BG_COORD_SET);
        SetGpuReg(REG_OFFSET_WIN0H, 0);
        SetGpuReg(REG_OFFSET_WIN0V, 0);
        SetGpuReg(REG_OFFSET_WININ, 0);
        SetGpuReg(REG_OFFSET_WINOUT, 0);
        SetGpuReg(REG_OFFSET_BLDCNT, 0);
        SetGpuReg(REG_OFFSET_BLDY, 0);
        ResetTasks();
        ResetSpriteData();
        ResetPaletteFade();
        ScanlineEffect_Stop();
        if (!InitWindows(sWindows))
        {
            SetMainCallback2(CB2_ReturnToFieldWithOpenMenu);
            return;
        }
        DeactivateAllTextPrinters();
        LoadPalette(sPaperPalette, 240, sizeof(sPaperPalette));
        sFilter = ADV_FILTER_ALL;
        sPage = 0;
        LegendsAdventureUpdateDay();
        sDay = LegendsAdventureDays();
        DrawPage();
        PutWindowTilemap(0);
        ShowBg(0);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_MODE_0 | DISPCNT_BG0_ON);
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        CreateTask(Task_Read, 0);
        SetVBlankCallback(VBlank);
        gMain.state++;
        break;
    default:
        SetMainCallback2(Main);
        break;
    }
}
