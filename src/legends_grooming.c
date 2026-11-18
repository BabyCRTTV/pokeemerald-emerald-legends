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
#include "trig.h"
#include "constants/rgb.h"
#include "constants/songs.h"

enum BathStage { LATHER, RINSE, DRY, CLEAN };
enum BathGraphic { BRUSH, PAIL, TOWEL, SUDS, DROP, GLINT };
enum { TOOL_TAG = 0x4B17, EFFECT_COUNT = 6, BATH_WATERLINE = 80 };

static EWRAM_DATA struct {
    u8 slot, stage, progress, rinseFrames, bounce;
    u16 sprite, clock;
    u8 tool, effects[EFFECT_COUNT];
    u8 name[POKEMON_NAME_LENGTH + 1];
} sBath = {0};

static const u32 sRoom[] = INCGFX_U32("graphics/legends/grooming/bathroom.png", ".8bpp.lz");
static const u16 sRoomPalette[] = INCGFX_U16("graphics/legends/grooming/bathroom.png", ".gbapal");
static const u32 sTools[] = INCGFX_U32("graphics/legends/grooming/tools.png", ".4bpp");
static const u16 sToolPalette[] = INCGFX_U16("graphics/legends/grooming/tools.png", ".gbapal");
static const struct SpriteSheet sToolSheet = {sTools, sizeof(sTools), TOOL_TAG};
static const struct SpritePalette sToolColors = {sToolPalette, TOOL_TAG};
static const struct OamData sObj = {.size = SPRITE_SIZE(32x32)};
static const struct SpriteTemplate sToolTemplate = {
    .tileTag = TOOL_TAG, .paletteTag = TOOL_TAG, .oam = &sObj,
    .anims = gDummySpriteAnimTable, .affineAnims = gDummySpriteAffineAnimTable,
    .callback = SpriteCallbackDummy,
};
static const struct BgTemplate sBg[] = {
    {.bg = 0, .mapBaseIndex = 31},
    {.bg = 1, .charBaseIndex = 1, .mapBaseIndex = 30, .paletteMode = 1, .priority = 2},
};
enum { HEADER, CONTROLS };
static const struct WindowTemplate sWindow[] = {
    {.width = 30, .height = 2, .paletteNum = 15, .baseBlock = 1},
    {.tilemapTop = 15, .width = 30, .height = 5, .paletteNum = 15, .baseBlock = 61},
    DUMMY_WIN_TEMPLATE
};
// Preserve standard keypad glyph indices 1-3 and the system button outlines.
enum { PAPER = 1, INK, SILVER, SEA, FOAM, TRACK, COMPLETED, ACTIVE };
static const u16 sUiColors[16] = {
    0, RGB_WHITE, RGB(6,10,13), RGB(23,25,24), RGB(7,14,15), RGB(29,31,27),
    RGB(24,26,24), RGB(9,19,17), RGB(6,17,17), RGB(20,24,27),
    RGB_WHITE, RGB(25,25,27), RGB(25,25,27), RGB(28,30,31), RGB(25,25,27), RGB(13,14,15)
};
static const u8 *const sStageNames[] = {
    COMPOUND_STRING("Lather"), COMPOUND_STRING("Rinse"), COMPOUND_STRING("Dry")
};

static void Label(u8 window, const u8 *text, u8 font, u8 x, u8 y, u8 color)
{
    const u8 colors[] = {0, color, 0};
    AddTextPrinterParameterized3(window, font, x, y, colors, TEXT_SKIP_DRAW, text);
}

static void DrawHeader(void)
{
    FillWindowPixelBuffer(HEADER, 0);
    Label(HEADER, COMPOUND_STRING("GROOMING KIT"), FONT_SMALL, 23, 1, PAPER);
    Label(HEADER, sBath.name, FONT_SMALL, 230 - GetStringWidth(FONT_SMALL, sBath.name, 0), 1, FOAM);
    PutWindowTilemap(HEADER);
    CopyWindowToVram(HEADER, COPYWIN_FULL);
}

static void DrawControls(void)
{
    const u8 *hint;
    FillWindowPixelBuffer(CONTROLS, 0);
    for (u8 i = 0; i < CLEAN; i++)
    {
        u8 x = 12 + i * 46;
        bool32 active = i == sBath.stage;
        u8 fill = active ? ACTIVE : TRACK;
        FillWindowPixelRect(CONTROLS, fill, x + 2, 0, 37, 13);
        FillWindowPixelRect(CONTROLS, fill, x, 2, 41, 9);
        Label(CONTROLS, sStageNames[i], FONT_SMALL,
              x + (41 - GetStringWidth(FONT_SMALL, sStageNames[i], 0)) / 2, 0, active ? PAPER : INK);
    }
    for (u8 i = 0; i < 6; i++)
    {
        u8 fill = (i < sBath.progress || sBath.stage == CLEAN) ? COMPLETED : TRACK;
        FillWindowPixelRect(CONTROLS, fill, 168 + 10 * i, 5, 8, 4);
    }
    switch (sBath.stage)
    {
    case LATHER:
        hint = (sBath.progress & 1) ? COMPOUND_STRING("{DPAD_RIGHT} Brush right") : COMPOUND_STRING("{DPAD_LEFT} Brush left");
        break;
    case RINSE: hint = COMPOUND_STRING("Hold {A_BUTTON} to rinse"); break;
    case DRY:   hint = COMPOUND_STRING("Tap {A_BUTTON} to pat dry"); break;
    default:    hint = COMPOUND_STRING("All clean!"); break;
    }
    Label(CONTROLS, hint, FONT_NORMAL, 13, 16, INK);
    Label(CONTROLS, sBath.stage == CLEAN ? COMPOUND_STRING("{A_BUTTON} Done") : COMPOUND_STRING("{B_BUTTON} Leave"),
          FONT_SMALL, 183, 18, SEA);
    PutWindowTilemap(CONTROLS);
    CopyWindowToVram(CONTROLS, COPYWIN_FULL);
}

// All six 32x32 frames share one sheet. The tool and foam sit in front of
// the party sprite, so a brush stroke actually crosses the Pokémon's coat.
static void PlaceGraphic(u8 id, u8 frame, s16 x, s16 y, bool32 visible)
{
    if (id >= MAX_SPRITES)
        return;
    struct Sprite *sprite = &gSprites[id];
    sprite->invisible = !visible;
    sprite->oam.tileNum = sprite->sheetTileStart + frame * 16;
    sprite->x = x;
    sprite->y = y;
}

static void AnimateBath(void)
{
    u8 phase = sBath.clock++;
    s16 bodyY = gSprites[sBath.sprite].y;
    s16 side = (sBath.progress & 1) ? -1 : 1;
    s16 glide = 20 - (sBath.bounce * 5 / 2);
    u8 visible = sBath.progress;
    u8 effect = SUDS;
    if (sBath.stage == LATHER)
        PlaceGraphic(sBath.tool, BRUSH, 120 + side * glide, bodyY + 4 + Sin((u8)(phase * 3), 1), TRUE);
    else if (sBath.stage == RINSE)
    {
        PlaceGraphic(sBath.tool, PAIL, 144, bodyY - 16 + Sin((u8)(phase * 2), 1), TRUE);
        effect = DROP;
        visible = JOY_HELD(A_BUTTON) ? EFFECT_COUNT : 0;
    }
    else if (sBath.stage == DRY)
    {
        PlaceGraphic(sBath.tool, TOWEL, 120 + side * glide, bodyY - 7 + sBath.bounce / 3, TRUE);
        effect = GLINT;
    }
    else
    {
        PlaceGraphic(sBath.tool, TOWEL, 0, 0, FALSE);
        effect = GLINT;
        visible = EFFECT_COUNT;
    }
    for (u8 i = 0; i < EFFECT_COUNT; i++)
    {
        u8 cycle = (phase + i * 9) & 31;
        s16 x, y;
        if (effect == DROP)
        {
            x = 133 - cycle / 3 + (i & 1) * 4;
            y = bodyY - 11 + cycle * 2 / 3;
        }
        else
        {
            x = 120 + (i & 1 ? 1 : -1) * (16 + i * 2) + Sin((u8)(phase * 2 + i * 38), 2);
            y = bodyY + 7 - (i / 2) * 9 - cycle / 4;
        }
        PlaceGraphic(sBath.effects[i], effect, x, y, i < visible && (effect == DROP || cycle < 25));
    }
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
    for (u8 i = 0; i < EFFECT_COUNT; i++)
        if (sBath.effects[i] < MAX_SPRITES)
            DestroySprite(&gSprites[sBath.effects[i]]);
    if (sBath.tool < MAX_SPRITES)
        DestroySprite(&gSprites[sBath.tool]);
    FreeSpriteTilesByTag(TOOL_TAG);
    FreeSpritePaletteByTag(TOOL_TAG);
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
        sBath.bounce = 16;
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
        DrawControls();
    }
    if (sBath.bounce)
        sBath.bounce--;
    gSprites[sBath.sprite].y2 = -(sBath.bounce / 6);
    AnimateBath();
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
    ChangeBgX(1, 0, BG_COORD_SET);
    ChangeBgY(1, 0, BG_COORD_SET);
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
    LZ77UnCompVram(sRoom, (void *)BG_CHAR_ADDR(1));
    u16 *map = (u16 *)BG_SCREEN_ADDR(30);
    for (u8 y = 0; y < 20; y++)
        for (u8 x = 0; x < 30; x++)
            map[y * 32 + x] = y * 30 + x;
    LoadPalette(sRoomPalette, 0, min(sizeof(sRoomPalette), BG_PLTT_ID(15) * sizeof(u16)));
    LoadPalette(sUiColors, BG_PLTT_ID(15), sizeof(sUiColors));
    enum Species species = GetMonData(mon, MON_DATA_SPECIES);
    sBath.sprite = CreateMonPicSprite(species, IsMonShiny(mon),
        GetMonData(mon, MON_DATA_PERSONALITY), TRUE, 120, BATH_WATERLINE - 28 + gSpeciesInfo[species].frontPicYOffset, 6, TAG_NONE);
    if (sBath.sprite >= MAX_SPRITES)
    {
        ExitBath();
        return;
    }
    gSprites[sBath.sprite].oam.priority = 1;
    if (LoadSpriteSheet(&sToolSheet) == TAG_NONE || LoadSpritePalette(&sToolColors) == 0xFF)
    {
        ExitBath();
        return;
    }
    sBath.tool = CreateSprite(&sToolTemplate, 0, 0, 0);
    for (u8 i = 0; i < EFFECT_COUNT; i++)
        sBath.effects[i] = CreateSprite(&sToolTemplate, 0, 0, 1);
    AnimateBath();
    DrawHeader();
    DrawControls();
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP | DISPCNT_WIN0_ON);
    SetGpuReg(REG_OFFSET_WIN0H, 240);
    SetGpuReg(REG_OFFSET_WIN0V, BATH_WATERLINE);
    SetGpuReg(REG_OFFSET_WININ, WININ_WIN0_ALL);
    SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG_ALL);
    ShowBg(0);
    ShowBg(1);
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
    sBath.tool = MAX_SPRITES;
    memset(sBath.effects, MAX_SPRITES, sizeof(sBath.effects));
    GetMonData(&gParties[B_TRAINER_PLAYER][sBath.slot], MON_DATA_NICKNAME, sBath.name);
    StringGet_Nickname(sBath.name);
    CleanupOverworldWindowsAndTilemaps();
    SetMainCallback2(InitBath);
}
