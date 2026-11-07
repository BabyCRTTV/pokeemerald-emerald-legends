#include "global.h"
#include "berry.h"
#include "bg.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "item.h"
#include "main.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "pokeblock.h"
#include "scanline_effect.h"
#include "script.h"
#include "sound.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"

#define STAGE_FRAMES 360
#define BAKE_FRAMES (STAGE_FRAMES * 3)

static const u32 sKitchen[] = INCGFX_U32("graphics/poffin/kitchen.png", ".4bpp");
static const u16 sKitchenPal[] = INCGFX_U16("graphics/poffin/kitchen.png", ".gbapal");
static const u32 sStir[] = INCGFX_U32("graphics/poffin/stir.png", ".4bpp");
static const u32 sBun[] = INCGFX_U32("graphics/poffin/bun0.png", ".4bpp");
static const u16 sCrust[][2] = {
    {RGB(26,10,11), RGB(31,18,16)}, {RGB(12,15,23), RGB(18,22,27)},
    {RGB(27,15,20), RGB(31,22,25)}, {RGB(13,21,14), RGB(20,26,18)},
    {RGB(28,23,10), RGB(31,28,18)}
};
static const u8 *const sNames[] = {
    COMPOUND_STRING("Spicy"), COMPOUND_STRING("Dry"), COMPOUND_STRING("Sweet"),
    COMPOUND_STRING("Bitter"), COMPOUND_STRING("Sour")
};
static const struct BgTemplate sBg = {.bg = 0, .mapBaseIndex = 31};
static const struct WindowTemplate sWindows[] = {
    {.width = 30, .height = 20, .baseBlock = 1}, DUMMY_WIN_TEMPLATE
};
enum Cue { STEADY, SPILL, BURN, REVERSE };
struct Batch
{
    u16 berries[2], frame, lastStep, steps, mistakes, cueUntil;
    u8 pose, cue, flavor, level;
    s8 lastDir;
    bool8 finished, exiting;
};
static EWRAM_DATA struct Batch sBatch = {0};

static void Print(const u8 *text, u8 x, u8 y, u8 ink, u8 shadow)
{
    const u8 colors[] = {0, ink, shadow};
    AddTextPrinterParameterized3(0, FONT_NORMAL, x, y, colors, TEXT_SKIP_DRAW, text);
}

// Frames and window coordinates are tile-aligned. Copy whole tile rows so that
// stirring costs no per-pixel bitmap conversion between controller samples.
static void DrawStir(void)
{
    const u8 *src = (const u8 *)sStir + sBatch.pose * 104 * 80 / 2;
    for (u8 row = 0; row < 10; row++)
        CopyToWindowPixelBuffer(0, src + row * 13 * 32, 13 * 32, (4 + row) * 30 + 4);
}

static void Draw(void)
{
    const u8 *message;
    u8 stage = min(2, sBatch.frame / STAGE_FRAMES);
    CopyToWindowPixelBuffer(0, sKitchen, sizeof(sKitchen), 0);
    Print(COMPOUND_STRING("POFFIN KITCHEN"), 73, 0, 14, 11);
    if (sBatch.finished)
    {
        BlitBitmapToWindow(0, (const u8 *)sBun, 51, 43, 64, 48);
        Print(COMPOUND_STRING("BAKED"), 173, 29, 14, 11);
        Print(sNames[sBatch.flavor], 165, 50, 2, 3);
        Print(COMPOUND_STRING("POFFIN"), 165, 62, 2, 3);
        ConvertIntToDecimalStringN(gStringVar1, sBatch.level, STR_CONV_MODE_LEFT_ALIGN, 3);
        Print(COMPOUND_STRING("Lv."), 165, 85, 2, 3);
        Print(gStringVar1, 185, 85, 2, 3);
        message = COMPOUND_STRING("In the treat case!     A: Finish");
    }
    else
    {
        static const u8 *const stages[] = {COMPOUND_STRING("BLEND"), COMPOUND_STRING("THICKEN"), COMPOUND_STRING("FINISH")};
        DrawStir();
        Print(stages[stage], 165, 29, 14, 11);
        Print(stage == 1 ? COMPOUND_STRING("Turn left") : COMPOUND_STRING("Turn right"), 163, 49, 2, 3);
        Print(stage == 1 ? COMPOUND_STRING("{UP_ARROW} {LEFT_ARROW} {DOWN_ARROW} {RIGHT_ARROW}") : COMPOUND_STRING("{UP_ARROW} {RIGHT_ARROW} {DOWN_ARROW} {LEFT_ARROW}"), 163, 62, 11, 3);
        Print(COMPOUND_STRING("Batter"), 165, 79, 2, 3);
        FillWindowPixelRect(0, 3, 165, 99, 59, 5);
        FillWindowPixelRect(0, 11, 165, 99, 59 * sBatch.frame / BAKE_FRAMES, 5);
        if (sBatch.cueUntil > sBatch.frame && sBatch.cue == SPILL)
            message = COMPOUND_STRING("Oops, a spill! Ease up a little.");
        else if (sBatch.cueUntil > sBatch.frame && sBatch.cue == BURN)
            message = COMPOUND_STRING("It's starting to burn! Keep stirring!");
        else if (sBatch.cueUntil > sBatch.frame && sBatch.cue == REVERSE)
            message = COMPOUND_STRING("Other way! Follow the arrows.");
        else if (stage == 0)
            message = COMPOUND_STRING("Roll the D-pad gently to mix.");
        else if (stage == 1)
            message = COMPOUND_STRING("Switch direction as it thickens!");
        else
            message = COMPOUND_STRING("One last turn! Keep it moving.");
    }
    Print(message, 16, 133, 2, 3);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void Warn(enum Cue cue)
{
    if (sBatch.cueUntil <= sBatch.frame || sBatch.cue != cue || (cue == BURN && sBatch.frame % 90 == 0))
    {
        sBatch.mistakes++;
        PlaySE(SE_FAILURE);
    }
    sBatch.cue = cue;
    sBatch.cueUntil = sBatch.frame + 45;
}

static bool32 HaveIngredients(void)
{
    u16 first = sBatch.berries[0], second = sBatch.berries[1];
    return ItemIdToBerryType(first) && CheckBagHasItem(first, first == second ? 2 : 1)
        && (!second || (ItemIdToBerryType(second) && CheckBagHasItem(second, 1)));
}

static bool32 FinishBatch(void)
{
    struct Pokeblock treat = {0};
    u16 flavors[5] = {0};
    u8 firstBerry[5];
    u16 feel = 0;
    u8 count = sBatch.berries[1] ? 2 : 1;
    if (!HaveIngredients() || GetFirstFreePokeblockSlot() < 0)
        return FALSE;
    for (u8 i = 0; i < count; i++)
    {
        const struct BerryInfo *b = GetBerryInfo(ItemIdToBerryType(sBatch.berries[i]));
        const u8 taste[] = {b->spicy, b->dry, b->sweet, b->bitter, b->sour};
        for (u8 flavor = 0; flavor < ARRAY_COUNT(taste); flavor++)
        {
            flavors[flavor] += taste[flavor];
            if (i == 0)
                firstBerry[flavor] = taste[flavor];
        }
        feel += b->smoothness;
    }
    for (u8 i = 1; i < 5; i++)
        if (flavors[i] > flavors[sBatch.flavor]
            || (flavors[i] == flavors[sBatch.flavor] && firstBerry[i] > firstBerry[sBatch.flavor]))
            sBatch.flavor = i;
    for (u8 i = 0; i < 5; i++)
        if (flavors[i] || i == sBatch.flavor)
            flavors[i] = max(1, (int)flavors[i] + (int)min(15, sBatch.steps / 6) - (int)sBatch.mistakes);
    treat.color = POFFIN_SPICY + sBatch.flavor;
    treat.spicy = flavors[0]; treat.dry = flavors[1]; treat.sweet = flavors[2];
    treat.bitter = flavors[3]; treat.sour = flavors[4]; treat.feel = max(1, feel / count);
    if (!AddPokeblock(&treat))
        return FALSE;
    RemoveBagItem(sBatch.berries[0], 1);
    if (count == 2)
        RemoveBagItem(sBatch.berries[1], 1);
    sBatch.level = GetHighestPokeblocksFlavorLevel(&treat);
    u8 accent = sBatch.flavor;
    for (u8 i = 0; i < 5; i++)
        if (i != sBatch.flavor && flavors[i] && (accent == sBatch.flavor || flavors[i] > flavors[accent]))
            accent = i;
    LoadPalette(sCrust[sBatch.flavor], 9, 4);
    LoadPalette(&sCrust[accent][1], 15, 2);
    return TRUE;
}

static void Leave(void)
{
    SetVBlankCallback(NULL);
    FreeAllWindowBuffers();
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void Main(void)
{
    UpdatePaletteFade();
    if (gPaletteFade.active)
        return;
    if (sBatch.exiting)
    {
        Leave();
        return;
    }
    if (JOY_NEW(B_BUTTON) || (sBatch.finished && JOY_NEW(A_BUTTON)))
    {
        sBatch.exiting = TRUE;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
        return;
    }
    if (sBatch.finished)
        return;
    sBatch.frame++;
    if (sBatch.frame == BAKE_FRAMES)
    {
        if (!FinishBatch())
        {
            gSpecialVar_Result = 0;
            Leave();
            return;
        }
        sBatch.finished = TRUE;
        PlaySE(SE_USE_ITEM);
        Draw();
        return;
    }
    u16 keys = gMain.newKeys & DPAD_ANY;
    s8 dir = keys == DPAD_UP ? 0 : keys == DPAD_RIGHT ? 1 : keys == DPAD_DOWN ? 2 : keys == DPAD_LEFT ? 3 : -1;
    bool32 reverse = sBatch.frame / STAGE_FRAMES == 1;
    u16 previousCueUntil = sBatch.cueUntil;
    bool32 moved = FALSE;
    if (dir >= 0 && sBatch.lastDir != dir)
    {
        if (sBatch.lastDir >= 0)
        {
            int delta = (dir - sBatch.lastDir + 4) % 4;
            if (delta == (reverse ? 3 : 1))
            {
                if (sBatch.frame < STAGE_FRAMES && sBatch.frame - sBatch.lastStep < 5)
                    Warn(SPILL);
                else
                    sBatch.steps++;
                moved = TRUE;
                sBatch.pose = (sBatch.pose + (reverse ? 7 : 1)) % 8;
                sBatch.lastStep = sBatch.frame;
                if (!(sBatch.steps % 4)) PlaySE(SE_M_BUBBLE);
            }
            else if (delta != 2)
                Warn(REVERSE);
        }
        sBatch.lastDir = dir;
    }
    if (sBatch.frame % 30 == 0)
    {
        if (sBatch.frame >= STAGE_FRAMES && sBatch.frame - sBatch.lastStep >= 75)
            Warn(BURN);
    }
    if (sBatch.frame % 30 == 0 || previousCueUntil != sBatch.cueUntil)
        Draw();
    else if (moved)
    {
        DrawStir();
        CopyWindowRectToVram(0, COPYWIN_GFX, 4, 4, 13, 10);
    }
}

static void InitKitchen(void)
{
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, &sBg, 1);
    ChangeBgX(0, 0, BG_COORD_SET);
    ChangeBgY(0, 0, BG_COORD_SET);
    ResetPaletteFade();
    ScanlineEffect_Stop();
    ResetTasks();
    if (!InitWindowsUnchecked(sWindows))
    {
        Leave();
        return;
    }
    DeactivateAllTextPrinters();
    LoadPalette(sKitchenPal, 0, 32);
    PutWindowTilemap(0);
    Draw();
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    ShowBg(0);
    SetVBlankCallback(TransferPlttBuffer);
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetMainCallback2(Main);
}

static void Enter(u8 taskId)
{
    if (gPaletteFade.active)
        return;
    CleanupOverworldWindowsAndTilemaps();
    DestroyTask(taskId);
    SetMainCallback2(InitKitchen);
}

static void ResumeWithoutCooking(u8 taskId)
{
    DestroyTask(taskId);
    ScriptContext_Enable();
}

void LegendsCookPoffin(void)
{
    memset(&sBatch, 0, sizeof(sBatch));
    sBatch.berries[0] = gSpecialVar_0x8004;
    sBatch.berries[1] = gSpecialVar_0x8005;
    sBatch.lastDir = -1;
    gSpecialVar_Result = HaveIngredients() && GetFirstFreePokeblockSlot() >= 0;
    if (!gSpecialVar_Result)
    {
        CreateTask(ResumeWithoutCooking, 0);
        return;
    }
    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    CreateTask(Enter, 0);
}

void LegendsPoffinHasRoom(void)
{
    gSpecialVar_Result = GetFirstFreePokeblockSlot() >= 0;
}

void LegendsOpenTreatCase(void)
{
    CleanupOverworldWindowsAndTilemaps();
    OpenPokeblockCase(PBLOCK_CASE_FIELD, CB2_ReturnToFieldContinueScriptPlayMapMusic);
}
