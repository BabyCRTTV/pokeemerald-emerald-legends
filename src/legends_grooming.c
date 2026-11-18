#include "global.h"
#include "bg.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "main.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "pokemon.h"
#include "scanline_effect.h"
#include "sound.h"
#include "string_util.h"
#include "task.h"
#include "trainer_pokemon_sprites.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"

enum BathStage { LATHER, RINSE, DRY, CLEAN };
static EWRAM_DATA struct {
    u8 slot;
    u16 sprite;
    u8 stage, progress, rinseFrames, bounce;
    u8 name[POKEMON_NAME_LENGTH + 1];
} sBath = {0};

static const struct BgTemplate sBg[] = {{.bg = 0, .mapBaseIndex = 31}};
static const struct WindowTemplate sWindow[] = {
    {.width = 30, .height = 20, .paletteNum = 15, .baseBlock = 1}, DUMMY_WIN_TEMPLATE
};
enum { INK = 1, TILE, GROUT, WHITE, ICE, WATER, TEAL, NAVY, CREAM, GOLD, CORAL, DEEP, SHADE, MINT, BLUE };
static const u16 sColors[] = {
    RGB(0,0,0), RGB(4,9,12), RGB(23,29,28), RGB(18,25,25), RGB(31,31,29),
    RGB(25,31,31), RGB(11,25,28), RGB(5,17,19), RGB(4,12,15), RGB(31,29,22),
    RGB(29,22,11), RGB(28,15,12), RGB(6,20,24), RGB(14,22,22), RGB(15,27,24), RGB(12,19,25)
};
static const u8 *const sStageNames[] = {
    COMPOUND_STRING("Lather"), COMPOUND_STRING("Rinse"), COMPOUND_STRING("Towel dry"), COMPOUND_STRING("All clean!")
};

static void Rect(u8 color, u8 x, u8 y, u8 w, u8 h)
{
    FillWindowPixelRect(0, color, x, y, w, h);
}

static void Label(const u8 *text, u8 font, u8 x, u8 y, u8 color)
{
    const u8 colors[] = {0, color, 0};
    AddTextPrinterParameterized3(0, font, x, y, colors, TEXT_SKIP_DRAW, text);
}

static void Bubble(u8 x, u8 y)
{
    Rect(TEAL, x+1, y, 4, 6);
    Rect(TEAL, x, y+1, 6, 4);
    Rect(ICE, x+1, y+1, 4, 4);
    Rect(WATER, x+2, y+3, 3, 2);
    Rect(WHITE, x+1, y+1, 2, 1);
}

static void DrawBath(void)
{
    u8 i;
    FillWindowPixelBuffer(0, PIXEL_FILL(TILE));
    for (i = 0; i < 5; i++)
    {
        u16 x;
        u8 y = 19 + i * 18;
        Rect(GROUT, 0, y, 240, 1);
        for (x = (i & 1) * 16; x < 232; x += 32)
            Rect(GROUT, x, y+1, 1, 17);
    }
    Rect(NAVY, 0, 0, 240, 19);
    Label(COMPOUND_STRING("GROOMING KIT"), FONT_SMALL, 8, 2, ICE);
    Label(sBath.name, FONT_SMALL, 157, 2, WHITE);

    // Enamel basin, rolled rim, water reflections and two brass feet.
    Rect(SHADE, 43, 106, 151, 3);
    Rect(GOLD, 58, 101, 10, 7);
    Rect(GOLD, 171, 101, 10, 7);
    Rect(TEAL, 42, 81, 156, 8);
    Rect(TEAL, 44, 89, 152, 5);
    Rect(TEAL, 47, 94, 146, 4);
    Rect(TEAL, 50, 98, 140, 5);
    Rect(WHITE, 44, 82, 152, 7);
    Rect(WHITE, 46, 89, 148, 5);
    Rect(ICE, 49, 94, 142, 3);
    Rect(ICE, 50, 95, 140, 4);
    Rect(MINT, 53, 99, 134, 2);
    Rect(TEAL, 37, 76, 166, 6);
    Rect(TEAL, 39, 82, 162, 2);
    Rect(WHITE, 39, 75, 162, 6);
    Rect(WATER, 43, 76, 154, 3);
    Rect(ICE, 51, 77, 15, 1);
    Rect(ICE, 167, 77, 20, 1);
    // Faucet and folded towels on the two sides of the bath.
    Rect(TEAL, 182, 49, 7, 26);
    Rect(TEAL, 169, 46, 17, 6);
    Rect(TEAL, 167, 49, 6, 7);
    Rect(ICE, 171, 47, 13, 2);
    Rect(ICE, 183, 51, 2, 21);
    Rect(CORAL, 181, 43, 10, 3);
    Rect(TEAL, 14, 86, 27, 4);
    Rect(GOLD, 16, 81, 23, 5);
    Rect(CREAM, 18, 81, 20, 3);
    Rect(CORAL, 19, 76, 19, 5);
    Rect(CREAM, 22, 77, 2, 3);

    for (i = 0; i < (sBath.stage == LATHER ? sBath.progress : sBath.stage == RINSE ? 6 - sBath.progress : 0); i++)
        Bubble(i & 1 ? 150 + i : 79 - i, 74 - i * 5);
    if (sBath.stage == LATHER)
    {
        u8 x = sBath.progress & 1 ? 140 : 86;
        Rect(GOLD, x, 58, 14, 7);
        Rect(GOLD, x+2, 56, 11, 11);
        Rect(CREAM, x+1, 58, 12, 6);
        Rect(GOLD, x+3, 61, 2, 2);
        Rect(GOLD, x+8, 59, 2, 2);
        if (sBath.progress)
            Bubble(x+9, 53);
    }
    if (sBath.stage == DRY)
    {
        u8 x = sBath.progress & 1 ? 137 : 88;
        Rect(TEAL, x, 50, 17, 15);
        Rect(CORAL, x+1, 49, 15, 14);
        Rect(CREAM, x+3, 50, 2, 13);
        Rect(WHITE, x+1, 61, 15, 1);
    }
    if (sBath.stage == RINSE)
        for (i = 0; i < 4; i++)
            Rect(WATER, 167 - i * 3, 57 + i * 4 + (sBath.progress & 1), 2, 3);
    if (sBath.stage == CLEAN || sBath.stage == DRY)
        for (i = 0; i < (sBath.stage == CLEAN ? 6 : sBath.progress); i++)
        {
            u8 x = i & 1 ? 146+i*2 : 92-i*3;
            u8 y = 66-i*6;
            Rect(GOLD, x, y+2, 5, 1);
            Rect(WHITE, x+2, y, 1, 5);
        }
    Rect(NAVY, 0, 111, 240, 49);
    Rect(TEAL, 0, 111, 240, 2);
    Label(sStageNames[sBath.stage], FONT_NORMAL, 9, 115, WHITE);
    for (i = 0; i < 6; i++)
        Rect(i < sBath.progress || sBath.stage == CLEAN ? MINT : TEAL, 153 + 13*i, 123, 10, 4);
    const u8 *hint = COMPOUND_STRING("A  Finish");
    if (sBath.stage == LATHER)
        hint = sBath.progress & 1 ? COMPOUND_STRING("{RIGHT_ARROW} Scrub right") : COMPOUND_STRING("{LEFT_ARROW} Scrub left");
    else if (sBath.stage == RINSE)
        hint = COMPOUND_STRING("Hold A to rinse");
    else if (sBath.stage == DRY)
        hint = COMPOUND_STRING("Tap A to pat dry");
    Label(hint, FONT_SMALL, 9, 140, CREAM);
    if (sBath.stage != CLEAN)
        Label(COMPOUND_STRING("B  Leave"), FONT_SMALL, 183, 140, ICE);
    PutWindowTilemap(0);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void BathVBlank(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static void ExitBath(void)
{
    SetVBlankCallback(NULL);
    if (sBath.sprite < MAX_SPRITES)
        FreeAndDestroyMonPicSprite(sBath.sprite);
    FreeAllWindowBuffers();
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void BathMain(void)
{
    bool32 stroke = FALSE;
    if (JOY_NEW(B_BUTTON) || (sBath.stage == CLEAN && JOY_NEW(A_BUTTON)))
    {
        ExitBath();
        return;
    }
    switch (sBath.stage)
    {
    case LATHER:
        stroke = JOY_NEW((sBath.progress & 1) ? DPAD_RIGHT : DPAD_LEFT);
        break;
    case RINSE:
        if (JOY_HELD(A_BUTTON) && ++sBath.rinseFrames == 12)
        {
            sBath.rinseFrames = 0;
            stroke = TRUE;
        }
        break;
    case DRY:
        stroke = JOY_NEW(A_BUTTON);
        break;
    }
    if (stroke)
    {
        PlaySE(sBath.stage == DRY ? SE_SELECT : SE_M_BUBBLE);
        sBath.bounce = 7;
        if (++sBath.progress == 6)
        {
            sBath.progress = 0;
            if (++sBath.stage == CLEAN)
            {
                struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][sBath.slot];
                u8 friendship = GetMonData(mon, MON_DATA_FRIENDSHIP);
                if (friendship < MAX_FRIENDSHIP)
                {
                    friendship++;
                    SetMonData(mon, MON_DATA_FRIENDSHIP, &friendship);
                }
                PlayCry_Normal(GetMonData(mon, MON_DATA_SPECIES), 0);
            }
        }
        DrawBath();
    }
    if (sBath.bounce)
        sBath.bounce--;
    gSprites[sBath.sprite].y2 = -(sBath.bounce / 2);
    AnimateSprites();
    BuildOamBuffer();
}

static void InitBath(void)
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][sBath.slot];
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_FORCED_BLANK);
    ScanlineEffect_Stop();
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    DmaClear32(3, OAM, OAM_SIZE);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, sBg, ARRAY_COUNT(sBg));
    ChangeBgX(0, 0, BG_COORD_SET);
    ChangeBgY(0, 0, BG_COORD_SET);
    ResetPaletteFade();
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    if (!InitWindowsUnchecked(sWindow))
    {
        ExitBath();
        return;
    }
    DeactivateAllTextPrinters();
    LoadPalette(sColors, BG_PLTT_ID(15), sizeof(sColors));
    sBath.sprite = CreateMonPicSprite(GetMonData(mon, MON_DATA_SPECIES), IsMonShiny(mon),
        GetMonData(mon, MON_DATA_PERSONALITY), TRUE, 119, 56, 6, TAG_NONE);
    if (sBath.sprite >= MAX_SPRITES)
    {
        ExitBath();
        return;
    }
    DrawBath();
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    ShowBg(0);
    SetVBlankCallback(BathVBlank);
    SetMainCallback2(BathMain);
}

void GroomingValidateMon(void)
{
    gSpecialVar_Result = gSpecialVar_0x8004 < PARTY_SIZE
        && !GetMonData(&gParties[B_TRAINER_PLAYER][gSpecialVar_0x8004], MON_DATA_IS_EGG);
}

void GroomingStart(void)
{
    memset(&sBath, 0, sizeof(sBath));
    sBath.slot = gSpecialVar_0x8004;
    sBath.sprite = MAX_SPRITES;
    GetMonData(&gParties[B_TRAINER_PLAYER][sBath.slot], MON_DATA_NICKNAME, sBath.name);
    StringGet_Nickname(sBath.name);
    CleanupOverworldWindowsAndTilemaps();
    SetMainCallback2(InitBath);
}
