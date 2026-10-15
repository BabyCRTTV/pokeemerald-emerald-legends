#include "global.h"
#include "legends_journal.h"
#include "item.h"
#include "main.h"
#include "menu.h"
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
static const u8 sHeaderInk[] = {7, 8, 3};
static const u8 sAltInk[] = {9, 2, 3};

#define JOURNAL_ROWS 6
#define JOURNAL_ROW_Y 40
#define JOURNAL_ROW_HEIGHT 15
static const u8 sSelectedInk[] = {8, 1, 0};
static const u8 sClaimInk[] = {7, 8, 3};

EWRAM_DATA static bool8 sAchievements = FALSE;
EWRAM_DATA static bool8 sDetail = FALSE;
EWRAM_DATA static u8 sFilter = 0, sMessage = 0;
EWRAM_DATA static u16 sSelected = 0, sTop = 0, sClaimFrames = 0;
static void Print(const u8 *text, u8 x, u8 y)
{
    AddTextPrinterParameterized3(0, FONT_SMALL, x, y, sInk, TEXT_SKIP_DRAW, text);
}
static void Check(u8 x, u8 y, bool32 done)
{
    u8 i;
    FillWindowPixelRect(0, PIXEL_FILL(8), x, y, 8, 8);
    FillWindowPixelRect(0, PIXEL_FILL(1), x + 1, y + 1, 6, 6);
    if (done)
        for (i = 0; i < 5; i++)
            FillWindowPixelRect(0, PIXEL_FILL(2), x + 2 + i, y + (i < 2 ? 3 + i : 6 - i), 1, 2);
}
static void Wrapped(const u8 *text, u8 x, u8 y, u8 maxLines)
{
    u8 line[128];
    u16 begin = 0, end, space, i;
    while (text[begin] != EOS && maxLines--)
    {
        end = begin; space = begin;
        while (text[end] != EOS && end - begin < sizeof(line) - 2)
        {
            line[end - begin] = text[end]; line[end - begin + 1] = EOS;
            if (GetStringWidth(FONT_SMALL, line, 0) > 218 - x) break;
            if (text[end] == CHAR_SPACE) space = end;
            end++;
        }
        if (text[end] != EOS && space > begin) end = space;
        for (i = begin; i < end; i++) line[i - begin] = text[i];
        line[end - begin] = EOS; Print(line, x, y); y += 12;
        begin = end;
        if (text[begin] == CHAR_SPACE) begin++;
        if (begin == i && !StringLength(line)) break;
    }
}
static bool32 Matches(u16 id)
{
    if (sAchievements)
    {
        if (sFilter == 1) return LegendsAchievementEarned(id) && !LegendsAchievementClaimed(id);
        if (sFilter == 2) return LegendsAchievementClaimed(id);
        return TRUE;
    }
    if (!LegendsQuestVisible(id)) return FALSE;
    if (sFilter == 2) return LegendsQuestComplete(id);
    return LegendsQuestGet(id)->side == sFilter;
}
static u16 Count(void)
{
    u16 i, count = 0, total = sAchievements ? LegendsAchievementCount() : LegendsQuestCount();
    for (i = 0; i < total; i++) if (Matches(i)) count++;
    return count;
}
static u16 Entry(u16 position)
{
    u16 i, total = sAchievements ? LegendsAchievementCount() : LegendsQuestCount();
    for (i = 0; i < total; i++) if (Matches(i) && position-- == 0) return i;
    return 0xFFFF;
}
static void JournalTab(const u8 *text, u8 x, u8 width, bool8 selected)
{
    if (selected)
        FillWindowPixelRect(0, PIXEL_FILL(8), x, 24, width, 14);
    else
    {
        FillWindowPixelRect(0, PIXEL_FILL(6), x, 24, width, 1);
        FillWindowPixelRect(0, PIXEL_FILL(6), x, 37, width, 1);
        FillWindowPixelRect(0, PIXEL_FILL(6), x, 24, 1, 14);
        FillWindowPixelRect(0, PIXEL_FILL(6), x + width - 1, 24, 1, 14);
    }
    AddTextPrinterParameterized3(0, FONT_SMALL, x + 4, 24,
        selected ? sSelectedInk : sInk, TEXT_SKIP_DRAW, text);
}

static void Draw(void)
{
    u8 text[128], number[16], i, j;
    const u8 *rowInk;
    u16 id, count = Count();
    const struct LegendsQuest *q;
    const struct LegendsAchievement *a;
    if (sSelected >= count) sSelected = count ? count - 1 : 0;
    if (sTop > sSelected) sTop = sSelected;
    if (sSelected >= sTop + JOURNAL_ROWS) sTop = sSelected - (JOURNAL_ROWS - 1);
    id = Entry(sSelected);
    FillWindowPixelBuffer(0, PIXEL_FILL(1));
    FillWindowPixelRect(0, PIXEL_FILL(6), 0, 0, 6, 160);
    FillWindowPixelRect(0, PIXEL_FILL(7), 6, 0, 234, 21);
    FillWindowPixelRect(0, PIXEL_FILL(6), 6, 20, 234, 2);
    AddTextPrinterParameterized3(0, FONT_NORMAL, 13, 2, sHeaderInk, TEXT_SKIP_DRAW,
        sAchievements ? COMPOUND_STRING("ACHIEVEMENTS") : COMPOUND_STRING("QUEST LOG"));
        ConvertIntToDecimalStringN(text, count ? sSelected + 1 : 0, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(text, COMPOUND_STRING("/")); ConvertIntToDecimalStringN(number, count, STR_CONV_MODE_LEFT_ALIGN, 3);
        StringAppend(text, number); AddTextPrinterParameterized3(0, FONT_SMALL, 198, 4, sHeaderInk, TEXT_SKIP_DRAW, text);
    if (sDetail && id != 0xFFFF)
    {
        FillWindowPixelRect(0, PIXEL_FILL(6), 8, 23, 228, 113);
        FillWindowPixelRect(0, PIXEL_FILL(1), 9, 24, 226, 111);
        if (!sAchievements)
        {
            q = LegendsQuestGet(id); Print(q->title, 13, 24);
            Print(q->side ? COMPOUND_STRING("SIDE QUEST") : COMPOUND_STRING("MAIN STORY"), 13, 36);
            for (i = 0; i < q->count; i++)
            {
                Check(13, 54 + i * 20, LegendsQuestStepComplete(id, i));
                Wrapped(q->steps[i].text, 26, 50 + i * 20, 2);
            }
            Print(COMPOUND_STRING("Checks update as you play.  B: Back"), 13, 147);
        }
        else
        {
            a = LegendsAchievementGet(id); Print(a->title, 13, 25);
            Wrapped(a->description, 13, 43, 3);
            StringCopy(text, COMPOUND_STRING("Progress: "));
            ConvertIntToDecimalStringN(number, min(LegendsAchievementProgress(id), a->target), STR_CONV_MODE_LEFT_ALIGN, 8);
            StringAppend(text, number); StringAppend(text, COMPOUND_STRING("/"));
            ConvertIntToDecimalStringN(number, a->target, STR_CONV_MODE_LEFT_ALIGN, 8); StringAppend(text, number);
            Print(LegendsAchievementEarned(id) ? COMPOUND_STRING("UNLOCKED") : text, 13, 82);
            StringCopy(text, COMPOUND_STRING("Reward: ")); StringAppend(text, GetItemName(a->berry));
            StringAppend(text, COMPOUND_STRING(" x"));
            ConvertIntToDecimalStringN(number, a->quantity, STR_CONV_MODE_LEFT_ALIGN, 2); StringAppend(text, number); Print(text, 13, 98);
            if (sMessage == 1 && sClaimFrames)
            {
                FillWindowPixelRect(0, PIXEL_FILL(7), 10, 113, 226, 28);
                AddTextPrinterParameterized3(0, FONT_SMALL, 16, 113, sClaimInk, TEXT_SKIP_DRAW, COMPOUND_STRING("REWARD CLAIMED!"));
                AddTextPrinterParameterized3(0, FONT_SMALL, 16, 126, sClaimInk, TEXT_SKIP_DRAW, COMPOUND_STRING("Sent to PC ITEM STORAGE."));
            }
            else
                Print(sMessage == 2 ? COMPOUND_STRING("PC full. Make room, then retry.") :
                    LegendsAchievementClaimed(id) ? COMPOUND_STRING("Reward already claimed.") : COMPOUND_STRING("Claim sends berries to your PC."), 13, 121);
            Print(COMPOUND_STRING("A: Claim reward   B: Back"), 13, 147);
        }
    }
    else
    {
        if (sAchievements)
        {
            JournalTab(COMPOUND_STRING("ALL"), 12, 45, sFilter == 0);
            JournalTab(COMPOUND_STRING("READY"), 61, 57, sFilter == 1);
            JournalTab(COMPOUND_STRING("CLAIMED"), 122, 67, sFilter == 2);
        }
        else
        {
            JournalTab(COMPOUND_STRING("MAIN"), 12, 50, sFilter == 0);
            JournalTab(COMPOUND_STRING("SIDE"), 66, 50, sFilter == 1);
            JournalTab(COMPOUND_STRING("DONE"), 120, 50, sFilter == 2);
        }
        if (!count) Print(COMPOUND_STRING("No entries in this view yet."), 13, 70);
        for (i = 0; i < JOURNAL_ROWS && sTop + i < count; i++)
        {
            id = Entry(sTop + i);
            rowInk = (i & 1) ? sAltInk : sInk;
            if (i & 1)
                FillWindowPixelRect(0, PIXEL_FILL(9), 7, JOURNAL_ROW_Y + i * JOURNAL_ROW_HEIGHT, 229, JOURNAL_ROW_HEIGHT);
            if (sTop + i == sSelected)
            {
                rowInk = sSelectedInk;
                FillWindowPixelRect(0, PIXEL_FILL(8), 7, JOURNAL_ROW_Y + i * JOURNAL_ROW_HEIGHT, 229, JOURNAL_ROW_HEIGHT);
                // Keep the pointer separate from the completion checkbox.
                for (j = 0; j < 4; j++)
                    FillWindowPixelRect(0, PIXEL_FILL(1), 8 + j, JOURNAL_ROW_Y + 5 + i * JOURNAL_ROW_HEIGHT + j, 1, 7 - 2 * j);
            }
            Check(13, JOURNAL_ROW_Y + 5 + i * JOURNAL_ROW_HEIGHT, sAchievements ? LegendsAchievementEarned(id) : LegendsQuestComplete(id));
            AddTextPrinterParameterized3(0, FONT_SMALL, 26, JOURNAL_ROW_Y + i * JOURNAL_ROW_HEIGHT, rowInk, TEXT_SKIP_DRAW,
                sAchievements ? LegendsAchievementGet(id)->title : LegendsQuestGet(id)->title);
            if (sAchievements && LegendsAchievementClaimed(id))
                AddTextPrinterParameterized3(0, FONT_SMALL, 222, JOURNAL_ROW_Y + i * JOURNAL_ROW_HEIGHT, rowInk, TEXT_SKIP_DRAW, COMPOUND_STRING("C"));
        }
        FillWindowPixelRect(0, PIXEL_FILL(6), 7, 132, 229, 1);
        Print(COMPOUND_STRING("A: DETAILS   B: CLOSE   L/R: PAGE"), 12, 134);
        Print(COMPOUND_STRING("LEFT/RIGHT: CHANGE VIEW"), 12, 146);
    }
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
    u16 count, id;
    if (gPaletteFade.active) return;
    if (sClaimFrames && --sClaimFrames == 0) Draw();
    if (JOY_NEW(B_BUTTON | START_BUTTON))
    {
        if (sDetail && !JOY_NEW(START_BUTTON)) { sDetail = FALSE; sMessage = 0; sClaimFrames = 0; Draw(); return; }
        PlaySE(SE_SELECT); BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        gTasks[taskId].func = Task_Close; return;
    }
    if (!JOY_NEW(A_BUTTON | DPAD_UP | DPAD_DOWN | DPAD_LEFT | DPAD_RIGHT | L_BUTTON | R_BUTTON | SELECT_BUTTON)) return;
    count = Count(); id = Entry(sSelected);
    if (sDetail)
    {
        if (sAchievements && JOY_NEW(A_BUTTON) && id != 0xFFFF && !LegendsAchievementClaimed(id) && LegendsAchievementEarned(id))
            {
                sMessage = LegendsAchievementClaim(id) ? 1 : 2;
                sClaimFrames = sMessage == 1 ? 180 : 0;
                if (sMessage == 1 && sFilter == 1)
                {
                    sFilter = 0; sSelected = id; sTop = 0;
                }
            }
    }
    else if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT | SELECT_BUTTON))
    {
        sFilter = (sFilter + (JOY_NEW(DPAD_LEFT) ? 2 : 1)) % 3; sSelected = sTop = 0;
    }
    else if (count && JOY_NEW(A_BUTTON)) sDetail = TRUE;
    else if (count)
    {
        if (JOY_NEW(DPAD_UP)) sSelected = sSelected ? sSelected - 1 : count - 1;
        if (JOY_NEW(DPAD_DOWN)) sSelected = (sSelected + 1) % count;
        if (JOY_NEW(L_BUTTON)) sSelected = sSelected > JOURNAL_ROWS ? sSelected - JOURNAL_ROWS : 0;
        if (JOY_NEW(R_BUTTON)) sSelected = min(sSelected + JOURNAL_ROWS, count - 1);
    }
    PlaySE(SE_SELECT); Draw();
}
static void OpenJournal(void)
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
        if (!InitWindowsUnchecked(sWindows))
        {
            FreeAllWindowBuffers();
            SetMainCallback2(CB2_ReturnToFieldWithOpenMenu);
            return;
        }
        DeactivateAllTextPrinters();
        LoadPalette(sPaperPalette, 240, sizeof(sPaperPalette));
        sFilter = 0; sSelected = 0; sTop = 0; sDetail = FALSE; sMessage = 0; sClaimFrames = 0;
        LegendsJournalRefresh();
        Draw();
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

void CB2_OpenQuestLog(void) { sAchievements = FALSE; OpenJournal(); }
void CB2_OpenAchievements(void) { sAchievements = TRUE; OpenJournal(); }
