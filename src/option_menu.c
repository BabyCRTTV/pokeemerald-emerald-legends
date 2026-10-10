#include "global.h"
#include "option_menu.h"
#include "bg.h"
#include "gpu_regs.h"
#include "international_string_util.h"
#include "legends_settings.h"
#include "legends_starters.h"
#include "legends_seasons.h"
#include "main.h"
#include "menu.h"
#include "palette.h"
#include "scanline_effect.h"
#include "sprite.h"
#include "strings.h"
#include "string_util.h"
#include "constants/characters.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "window.h"
#include "gba/m4a_internal.h"
#include "constants/rgb.h"

#define tMenuSelection data[0]
#define tTextSpeed data[1]
#define tBattleSceneOff data[2]
#define tBattleStyle data[3]
#define tSound data[4]
#define tButtonMode data[5]
#define tWindowFrameType data[6]
#define tExpShare data[7]
#define tMenuPage data[8]
#define tShinyRate data[9]
#define tSeasonMode data[10]
#define tSelectedSeason data[11]
#define tSeasonEdited data[12]
#define tFollowers data[13]
#define tStarterSetting data[14]

enum
{
    MENUITEM_TEXTSPEED,
    MENUITEM_BATTLESCENE,
    MENUITEM_BATTLESTYLE,
    MENUITEM_EXPSHARE,
    MENUITEM_FOLLOWERS,
    MENUITEM_SHINYRATE,
    MENUITEM_SEASONMODE,
    MENUITEM_SEASON,
    MENUITEM_SETSEASON,
    MENUITEM_SOUND,
    MENUITEM_BUTTONMODE,
    MENUITEM_FRAMETYPE,
    MENUITEM_STARTERS,
    MENUITEM_STARTERINFO,
    MENUITEM_NEXTPAGE,
    MENUITEM_COUNT,
};

enum
{
    OPTION_PAGE_GENERAL,
    OPTION_PAGE_LEGENDS,
    OPTION_PAGE_ADVENTURE,
    OPTION_PAGE_COUNT,
};

enum
{
    WIN_HEADER,
    WIN_OPTIONS
};

#define OPTION_ROW_HEIGHT     16
#define OPTION_WINDOW_Y       40
#define OPTION_PAGE_MAX_ITEMS 7

static void Task_OptionMenuFadeIn(u8 taskId);
static void Task_OptionMenuProcessInput(u8 taskId);
static void Task_OptionMenuSave(u8 taskId);
static void Task_OptionMenuFadeOut(u8 taskId);
static void HighlightOptionMenuItem(u8 selection);
static u8 TextSpeed_ProcessInput(u8 selection);
static void TextSpeed_DrawChoices(u8 selection, u8 y);
static u8 BattleScene_ProcessInput(u8 selection);
static void BattleScene_DrawChoices(u8 selection, u8 y);
static u8 BattleStyle_ProcessInput(u8 selection);
static void BattleStyle_DrawChoices(u8 selection, u8 y);
static u8 OnOff_ProcessInput(u8 selection);
static void OnOff_DrawChoices(u8 selection, u8 y);
static u8 ShinyRate_ProcessInput(u8 selection);
static void ShinyRate_DrawChoices(u8 selection, u8 y);
static u8 SeasonMode_ProcessInput(u8 selection);
static void SeasonMode_DrawChoices(u8 selection, u8 y);
static void Season_DrawChoice(u8 y);
static void SetSeason_DrawChoice(u8 mode, u8 season, u8 y);
static u8 SetSeason_ProcessInput(u8 selection);
static u8 Sound_ProcessInput(u8 selection);
static void Sound_DrawChoices(u8 selection, u8 y);
static u8 FrameType_ProcessInput(u8 selection);
static void FrameType_DrawChoices(u8 selection, u8 y);
static u8 ButtonMode_ProcessInput(u8 selection);
static void ButtonMode_DrawChoices(u8 selection, u8 y);
static void DrawHeaderText(u8 page);
static void DrawOptionMenuPage(u8 taskId);
static void ChangeOptionMenuPage(u8 taskId, s8 direction);
static u8 GetOptionMenuItem(u8 taskId);
static void DrawBgWindowFrames(void);
static u8 StarterSetting_ProcessInput(u8 selection);
static void StarterSetting_DrawChoice(u8 selection, u8 y);

EWRAM_DATA static bool8 sArrowPressed = FALSE;

static const u8 gText_PageControls[]       = _("A: NEXT  B: SAVE");
#ifdef RELEASE
static const u8 gText_LegendsVersion[]      = _("LEGENDS v0.0.30");
#else
static const u8 gText_LegendsVersion[]      = _("LEGENDS v0.0.30-D");
#endif
static const u8 gText_TextSpeedSlow[]      = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}SLOW");
static const u8 gText_TextSpeedMid[]       = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}MID");
static const u8 gText_TextSpeedFast[]      = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}FAST");
static const u8 gText_BattleSceneOn[]      = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}ON");
static const u8 gText_BattleSceneOff[]     = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}OFF");
static const u8 gText_BattleStyleShift[]   = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}SHIFT");
static const u8 gText_BattleStyleSet[]     = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}SET");
static const u8 gText_LegendsToggleOn[]          = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}ON");
static const u8 gText_LegendsToggleOff[]         = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}OFF");
static const u8 gText_LegendsShiny8192[]           = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}1/8192");
static const u8 gText_LegendsShiny5680[]           = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}1/5680");
static const u8 gText_LegendsShiny1226[]           = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}1/1226");
static const u8 gText_SoundMono[]          = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}MONO");
static const u8 gText_SoundStereo[]        = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}STEREO");
static const u8 gText_FrameType[]          = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}TYPE");
static const u8 gText_FrameTypeNumber[]    = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}");
static const u8 gText_ButtonTypeNormal[]   = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}NORMAL");
static const u8 gText_ButtonTypeLR[]       = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}LR");
static const u8 gText_ButtonTypeLEqualsA[] = _("{COLOR GREEN}{SHADOW LIGHT_GREEN}L=A");

static const u8 *const sStarterSettingNames[LEGENDS_STARTERS_COUNT] =
{
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 1"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 2"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 3"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 4"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 5"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 6"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 7"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 8"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}GEN 9"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}SPECIAL"),
    COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}RANDOM"),
};

static const u16 sOptionMenuText_Pal[] = INCGFX_U16("graphics/interface/option_menu_text.pal", ".gbapal");
// note: this is only used in the Japanese release
static const u8 sEqualSignGfx[] = INCGFX_U8("graphics/interface/option_menu_equals_sign.png", ".4bpp");

static const u8 *const sOptionMenuItemsNames[MENUITEM_COUNT] =
{
    [MENUITEM_TEXTSPEED]   = COMPOUND_STRING("TEXT SPEED"),
    [MENUITEM_BATTLESCENE] = COMPOUND_STRING("BATTLE SCENE"),
    [MENUITEM_BATTLESTYLE] = COMPOUND_STRING("BATTLE STYLE"),
    [MENUITEM_EXPSHARE]    = COMPOUND_STRING("EXP SHARE"),
    [MENUITEM_FOLLOWERS]   = COMPOUND_STRING("FOLLOWER"),
    [MENUITEM_SHINYRATE]   = COMPOUND_STRING("SHINY RATE"),
    [MENUITEM_SEASONMODE]  = COMPOUND_STRING("SEASONS"),
    [MENUITEM_SEASON]      = COMPOUND_STRING("CURRENT"),
    [MENUITEM_SETSEASON]  = COMPOUND_STRING("SET SEASON"),
    [MENUITEM_SOUND]       = COMPOUND_STRING("SOUND"),
    [MENUITEM_BUTTONMODE]  = COMPOUND_STRING("BUTTON MODE"),
    [MENUITEM_FRAMETYPE]   = COMPOUND_STRING("FRAME"),
    [MENUITEM_STARTERS]    = COMPOUND_STRING("STARTERS"),
    [MENUITEM_STARTERINFO] = COMPOUND_STRING("APPLIES TO"),
    [MENUITEM_NEXTPAGE]    = COMPOUND_STRING("NEXT PAGE"),
};

static const u8 *const sOptionMenuPageTitles[OPTION_PAGE_COUNT] =
{
    [OPTION_PAGE_GENERAL] = COMPOUND_STRING("GENERAL 1/3"),
    [OPTION_PAGE_LEGENDS] = COMPOUND_STRING("LEGENDS 2/3"),
    [OPTION_PAGE_ADVENTURE] = COMPOUND_STRING("ADVENTURE 3/3"),
};

static const u8 sOptionMenuPageItems[OPTION_PAGE_COUNT][OPTION_PAGE_MAX_ITEMS] =
{
    [OPTION_PAGE_GENERAL] =
    {
        MENUITEM_TEXTSPEED,
        MENUITEM_BATTLESCENE,
        MENUITEM_BATTLESTYLE,
        MENUITEM_SOUND,
        MENUITEM_BUTTONMODE,
        MENUITEM_FRAMETYPE,
        MENUITEM_NEXTPAGE,
    },
    [OPTION_PAGE_LEGENDS] =
    {
        MENUITEM_EXPSHARE,
        MENUITEM_FOLLOWERS,
        MENUITEM_SHINYRATE,
        MENUITEM_SEASONMODE,
        MENUITEM_SEASON,
        MENUITEM_SETSEASON,
        MENUITEM_NEXTPAGE,
    },
    [OPTION_PAGE_ADVENTURE] = {MENUITEM_STARTERS, MENUITEM_STARTERINFO, MENUITEM_NEXTPAGE},
};

static const u8 sOptionMenuPageItemCounts[OPTION_PAGE_COUNT] =
{
    [OPTION_PAGE_GENERAL] = 7,
    [OPTION_PAGE_LEGENDS] = 7,
    [OPTION_PAGE_ADVENTURE] = 3,
};

static const struct WindowTemplate sOptionMenuWinTemplates[] =
{
    [WIN_HEADER] = {
        .bg = 1,
        .tilemapLeft = 2,
        .tilemapTop = 1,
        .width = 26,
        .height = 2,
        .paletteNum = 1,
        .baseBlock = 2
    },
    [WIN_OPTIONS] = {
        .bg = 0,
        .tilemapLeft = 2,
        .tilemapTop = 5,
        .width = 26,
        .height = 14,
        .paletteNum = 1,
        .baseBlock = 0x36
    },
    DUMMY_WIN_TEMPLATE
};

static const struct BgTemplate sOptionMenuBgTemplates[] =
{
    {
        .bg = 1,
        .charBaseIndex = 1,
        .mapBaseIndex = 30,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 0,
        .baseTile = 0
    },
    {
        .bg = 0,
        .charBaseIndex = 1,
        .mapBaseIndex = 31,
        .screenSize = 0,
        .paletteMode = 0,
        .priority = 1,
        .baseTile = 0
    }
};

static const u16 sOptionMenuBg_Pal[] = {RGB(17, 18, 31)};

static void MainCB2(void)
{
    RunTasks();
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
}

static void VBlankCB(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

void CB2_InitOptionMenu(void)
{
    switch (gMain.state)
    {
    default:
    case 0:
        SetVBlankCallback(NULL);
        gMain.state++;
        break;
    case 1:
        DmaClearLarge16(3, (void *)(VRAM), VRAM_SIZE, 0x1000);
        DmaClear32(3, OAM, OAM_SIZE);
        DmaClear16(3, PLTT, PLTT_SIZE);
        SetGpuReg(REG_OFFSET_DISPCNT, 0);
        ResetBgsAndClearDma3BusyFlags(0);
        InitBgsFromTemplates(0, sOptionMenuBgTemplates, ARRAY_COUNT(sOptionMenuBgTemplates));
        ChangeBgX(0, 0, BG_COORD_SET);
        ChangeBgY(0, 0, BG_COORD_SET);
        ChangeBgX(1, 0, BG_COORD_SET);
        ChangeBgY(1, 0, BG_COORD_SET);
        ChangeBgX(2, 0, BG_COORD_SET);
        ChangeBgY(2, 0, BG_COORD_SET);
        ChangeBgX(3, 0, BG_COORD_SET);
        ChangeBgY(3, 0, BG_COORD_SET);
        InitWindows(sOptionMenuWinTemplates);
        DeactivateAllTextPrinters();
        SetGpuReg(REG_OFFSET_WIN0H, 0);
        SetGpuReg(REG_OFFSET_WIN0V, 0);
        SetGpuReg(REG_OFFSET_WININ, WININ_WIN0_BG0);
        SetGpuReg(REG_OFFSET_WINOUT, WINOUT_WIN01_BG0 | WINOUT_WIN01_BG1 | WINOUT_WIN01_CLR);
        SetGpuReg(REG_OFFSET_BLDCNT, BLDCNT_TGT1_BG0 | BLDCNT_EFFECT_DARKEN);
        SetGpuReg(REG_OFFSET_BLDALPHA, 0);
        SetGpuReg(REG_OFFSET_BLDY, 4);
        SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_WIN0_ON | DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
        ShowBg(0);
        ShowBg(1);
        gMain.state++;
        break;
    case 2:
        ResetPaletteFade();
        ScanlineEffect_Stop();
        ResetTasks();
        ResetSpriteData();
        gMain.state++;
        break;
    case 3:
        LoadBgTiles(1, GetWindowFrameTilesPal(gSaveBlock2Ptr->optionsWindowFrameType)->tiles, 0x120, 0x1A2);
        gMain.state++;
        break;
    case 4:
        LoadPalette(sOptionMenuBg_Pal, BG_PLTT_ID(0), sizeof(sOptionMenuBg_Pal));
        LoadPalette(GetWindowFrameTilesPal(gSaveBlock2Ptr->optionsWindowFrameType)->pal, BG_PLTT_ID(7), PLTT_SIZE_4BPP);
        gMain.state++;
        break;
    case 5:
        LoadPalette(sOptionMenuText_Pal, BG_PLTT_ID(1), sizeof(sOptionMenuText_Pal));
        gMain.state++;
        break;
    case 6:
        PutWindowTilemap(WIN_HEADER);
        DrawHeaderText(OPTION_PAGE_GENERAL);
        gMain.state++;
        break;
    case 7:
        gMain.state++;
        break;
    case 8:
        PutWindowTilemap(WIN_OPTIONS);
        gMain.state++;
    case 9:
        DrawBgWindowFrames();
        gMain.state++;
        break;
    case 10:
    {
        u8 taskId = CreateTask(Task_OptionMenuFadeIn, 0);

        gTasks[taskId].tMenuSelection = 0;
        gTasks[taskId].tMenuPage = OPTION_PAGE_GENERAL;
        gTasks[taskId].tTextSpeed = gSaveBlock2Ptr->optionsTextSpeed;
        gTasks[taskId].tBattleSceneOff = gSaveBlock2Ptr->optionsBattleSceneOff;
        gTasks[taskId].tBattleStyle = gSaveBlock2Ptr->optionsBattleStyle;
        gTasks[taskId].tSound = gSaveBlock2Ptr->optionsSound;
        gTasks[taskId].tButtonMode = gSaveBlock2Ptr->optionsButtonMode;
        gTasks[taskId].tWindowFrameType = gSaveBlock2Ptr->optionsWindowFrameType;
        gTasks[taskId].tExpShare = LegendsIsExpShareEnabled() ? 0 : 1;
        gTasks[taskId].tFollowers = LegendsAreFollowersEnabled() ? 0 : 1;
        gTasks[taskId].tShinyRate = LegendsGetShinyRateSetting();
        gTasks[taskId].tSeasonMode = LegendsGetSeasonMode();
        gTasks[taskId].tSelectedSeason = LegendsGetSeasonForMode(LEGENDS_SEASONS_PLAYTIME);
        gTasks[taskId].tSeasonEdited = FALSE;
        gTasks[taskId].tStarterSetting = LegendsGetStarterSetting();

        DrawOptionMenuPage(taskId);
        HighlightOptionMenuItem(gTasks[taskId].tMenuSelection);
        gMain.state++;
        break;
    }
    case 11:
        BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
        SetVBlankCallback(VBlankCB);
        SetMainCallback2(MainCB2);
        return;
    }
}

static void Task_OptionMenuFadeIn(u8 taskId)
{
    if (!gPaletteFade.active)
        gTasks[taskId].func = Task_OptionMenuProcessInput;
}

static void Task_OptionMenuProcessInput(u8 taskId)
{
    u8 itemId;
    u8 itemCount;
    u8 y;

    // Handle page navigation before A/B so L still changes pages when Button Mode is L=A.
    if (JOY_NEW(L_BUTTON))
    {
        ChangeOptionMenuPage(taskId, -1);
    }
    else if (JOY_NEW(R_BUTTON))
    {
        ChangeOptionMenuPage(taskId, 1);
    }
    else if (JOY_NEW(A_BUTTON))
    {
        if (GetOptionMenuItem(taskId) == MENUITEM_NEXTPAGE)
            ChangeOptionMenuPage(taskId, 1);
    }
    else if (JOY_NEW(B_BUTTON))
    {
        gTasks[taskId].func = Task_OptionMenuSave;
    }
    else if (JOY_NEW(DPAD_UP))
    {
        itemCount = sOptionMenuPageItemCounts[gTasks[taskId].tMenuPage];
        if (gTasks[taskId].tMenuSelection > 0)
            gTasks[taskId].tMenuSelection--;
        else
            gTasks[taskId].tMenuSelection = itemCount - 1;
        HighlightOptionMenuItem(gTasks[taskId].tMenuSelection);
    }
    else if (JOY_NEW(DPAD_DOWN))
    {
        itemCount = sOptionMenuPageItemCounts[gTasks[taskId].tMenuPage];
        if (gTasks[taskId].tMenuSelection < itemCount - 1)
            gTasks[taskId].tMenuSelection++;
        else
            gTasks[taskId].tMenuSelection = 0;
        HighlightOptionMenuItem(gTasks[taskId].tMenuSelection);
    }
    else
    {
        u8 previousOption;

        itemId = GetOptionMenuItem(taskId);
        y = gTasks[taskId].tMenuSelection * OPTION_ROW_HEIGHT;

        switch (itemId)
        {
        case MENUITEM_STARTERS:
            previousOption = gTasks[taskId].tStarterSetting;
            gTasks[taskId].tStarterSetting = StarterSetting_ProcessInput(previousOption);
            if (previousOption != gTasks[taskId].tStarterSetting)
                StarterSetting_DrawChoice(gTasks[taskId].tStarterSetting, y);
            break;
        case MENUITEM_TEXTSPEED:
            previousOption = gTasks[taskId].tTextSpeed;
            gTasks[taskId].tTextSpeed = TextSpeed_ProcessInput(gTasks[taskId].tTextSpeed);

            if (previousOption != gTasks[taskId].tTextSpeed)
                TextSpeed_DrawChoices(gTasks[taskId].tTextSpeed, y);
            break;
        case MENUITEM_BATTLESCENE:
            previousOption = gTasks[taskId].tBattleSceneOff;
            gTasks[taskId].tBattleSceneOff = BattleScene_ProcessInput(gTasks[taskId].tBattleSceneOff);

            if (previousOption != gTasks[taskId].tBattleSceneOff)
                BattleScene_DrawChoices(gTasks[taskId].tBattleSceneOff, y);
            break;
        case MENUITEM_BATTLESTYLE:
            previousOption = gTasks[taskId].tBattleStyle;
            gTasks[taskId].tBattleStyle = BattleStyle_ProcessInput(gTasks[taskId].tBattleStyle);

            if (previousOption != gTasks[taskId].tBattleStyle)
                BattleStyle_DrawChoices(gTasks[taskId].tBattleStyle, y);
            break;
        case MENUITEM_EXPSHARE:
            previousOption = gTasks[taskId].tExpShare;
            gTasks[taskId].tExpShare = OnOff_ProcessInput(gTasks[taskId].tExpShare);

            if (previousOption != gTasks[taskId].tExpShare)
                OnOff_DrawChoices(gTasks[taskId].tExpShare, y);
            break;
        case MENUITEM_SHINYRATE:
            previousOption = gTasks[taskId].tShinyRate;
            gTasks[taskId].tShinyRate = ShinyRate_ProcessInput(gTasks[taskId].tShinyRate);

            if (previousOption != gTasks[taskId].tShinyRate)
                ShinyRate_DrawChoices(gTasks[taskId].tShinyRate, y);
            break;
        case MENUITEM_FOLLOWERS:
            previousOption = gTasks[taskId].tFollowers;
            gTasks[taskId].tFollowers = OnOff_ProcessInput(previousOption);
            if (previousOption != gTasks[taskId].tFollowers)
                OnOff_DrawChoices(gTasks[taskId].tFollowers, y);
            break;
        case MENUITEM_SEASONMODE:
            previousOption = gTasks[taskId].tSeasonMode;
            gTasks[taskId].tSeasonMode = SeasonMode_ProcessInput(previousOption);
            if (previousOption != gTasks[taskId].tSeasonMode)
            {
                SeasonMode_DrawChoices(gTasks[taskId].tSeasonMode, y);
                SetSeason_DrawChoice(gTasks[taskId].tSeasonMode, gTasks[taskId].tSelectedSeason, y + 2 * OPTION_ROW_HEIGHT);
            }
            break;
        case MENUITEM_SETSEASON:
            if (gTasks[taskId].tSeasonMode == LEGENDS_SEASONS_PLAYTIME)
            {
                previousOption = gTasks[taskId].tSelectedSeason;
                gTasks[taskId].tSelectedSeason = SetSeason_ProcessInput(previousOption);
                if (previousOption != gTasks[taskId].tSelectedSeason)
                {
                    gTasks[taskId].tSeasonEdited = TRUE;
                    SetSeason_DrawChoice(gTasks[taskId].tSeasonMode, gTasks[taskId].tSelectedSeason, y);
                }
            }
            break;
        case MENUITEM_SOUND:
            previousOption = gTasks[taskId].tSound;
            gTasks[taskId].tSound = Sound_ProcessInput(gTasks[taskId].tSound);

            if (previousOption != gTasks[taskId].tSound)
                Sound_DrawChoices(gTasks[taskId].tSound, y);
            break;
        case MENUITEM_BUTTONMODE:
            previousOption = gTasks[taskId].tButtonMode;
            gTasks[taskId].tButtonMode = ButtonMode_ProcessInput(gTasks[taskId].tButtonMode);

            if (previousOption != gTasks[taskId].tButtonMode)
                ButtonMode_DrawChoices(gTasks[taskId].tButtonMode, y);
            break;
        case MENUITEM_FRAMETYPE:
            previousOption = gTasks[taskId].tWindowFrameType;
            gTasks[taskId].tWindowFrameType = FrameType_ProcessInput(gTasks[taskId].tWindowFrameType);

            if (previousOption != gTasks[taskId].tWindowFrameType)
                FrameType_DrawChoices(gTasks[taskId].tWindowFrameType, y);
            break;
        default:
            return;
        }

        if (sArrowPressed)
        {
            sArrowPressed = FALSE;
            CopyWindowToVram(WIN_OPTIONS, COPYWIN_GFX);
        }
    }
}

static void Task_OptionMenuSave(u8 taskId)
{
    gSaveBlock2Ptr->optionsTextSpeed = gTasks[taskId].tTextSpeed;
    gSaveBlock2Ptr->optionsBattleSceneOff = gTasks[taskId].tBattleSceneOff;
    gSaveBlock2Ptr->optionsBattleStyle = gTasks[taskId].tBattleStyle;
    gSaveBlock2Ptr->optionsSound = gTasks[taskId].tSound;
    gSaveBlock2Ptr->optionsButtonMode = gTasks[taskId].tButtonMode;
    gSaveBlock2Ptr->optionsWindowFrameType = gTasks[taskId].tWindowFrameType;
    LegendsSetExpShareEnabled(gTasks[taskId].tExpShare == 0);
    LegendsSetFollowersEnabled(gTasks[taskId].tFollowers == 0);
    LegendsSetShinyRateSetting(gTasks[taskId].tShinyRate);
    LegendsSetStarterSetting(gTasks[taskId].tStarterSetting);
    LegendsSetSeasonMode(gTasks[taskId].tSeasonMode);
    if (gTasks[taskId].tSeasonEdited)
        LegendsSetPlaytimeSeason(gTasks[taskId].tSelectedSeason);

    BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    gTasks[taskId].func = Task_OptionMenuFadeOut;
}

static void Task_OptionMenuFadeOut(u8 taskId)
{
    if (!gPaletteFade.active)
    {
        DestroyTask(taskId);
        FreeAllWindowBuffers();
        SetMainCallback2(gMain.savedCallback);
    }
}

static void HighlightOptionMenuItem(u8 index)
{
    SetGpuReg(REG_OFFSET_WIN0H, WIN_RANGE(16, DISPLAY_WIDTH - 16));
    SetGpuReg(REG_OFFSET_WIN0V, WIN_RANGE(index * OPTION_ROW_HEIGHT + OPTION_WINDOW_Y,
                                          index * OPTION_ROW_HEIGHT + OPTION_WINDOW_Y + OPTION_ROW_HEIGHT));
}

static void DrawOptionMenuChoice(const u8 *text, u8 x, u8 y, u8 style)
{
    u8 dst[16];
    u16 i;

    for (i = 0; *text != EOS && i < ARRAY_COUNT(dst) - 1; i++)
        dst[i] = *(text++);

    // Only recolor the standard COLOR/SHADOW prefix, never ordinary letters.
    if (style != 0 && i >= 6
     && dst[0] == EXT_CTRL_CODE_BEGIN && dst[1] == EXT_CTRL_CODE_COLOR
     && dst[3] == EXT_CTRL_CODE_BEGIN && dst[4] == EXT_CTRL_CODE_SHADOW)
    {
        dst[2] = TEXT_COLOR_RED;
        dst[5] = TEXT_COLOR_LIGHT_RED;
    }

    dst[i] = EOS;
    AddTextPrinterParameterized(WIN_OPTIONS, FONT_NORMAL, dst, x, y + 1, TEXT_SKIP_DRAW, NULL);
}

static u8 StarterSetting_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        selection = (selection + 1) % LEGENDS_STARTERS_COUNT;
        sArrowPressed = TRUE;
    }
    else if (JOY_NEW(DPAD_LEFT))
    {
        selection = (selection + LEGENDS_STARTERS_COUNT - 1) % LEGENDS_STARTERS_COUNT;
        sArrowPressed = TRUE;
    }
    return selection;
}

static void StarterSetting_DrawChoice(u8 selection, u8 y)
{
    FillWindowPixelRect(WIN_OPTIONS, PIXEL_FILL(1), 104, y, 104, OPTION_ROW_HEIGHT);
    DrawOptionMenuChoice(sStarterSettingNames[selection], 104, y, 1);
}

static u8 TextSpeed_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        if (selection <= 1)
            selection++;
        else
            selection = 0;

        sArrowPressed = TRUE;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        if (selection != 0)
            selection--;
        else
            selection = 2;

        sArrowPressed = TRUE;
    }
    return selection;
}

static void TextSpeed_DrawChoices(u8 selection, u8 y)
{
    u8 styles[3];
    s32 widthSlow, widthMid, widthFast, xMid;

    styles[0] = 0;
    styles[1] = 0;
    styles[2] = 0;
    styles[selection] = 1;

    DrawOptionMenuChoice(gText_TextSpeedSlow, 104, y, styles[0]);

    widthSlow = GetStringWidth(FONT_NORMAL, gText_TextSpeedSlow, 0);
    widthMid = GetStringWidth(FONT_NORMAL, gText_TextSpeedMid, 0);
    widthFast = GetStringWidth(FONT_NORMAL, gText_TextSpeedFast, 0);

    widthMid -= 94;
    xMid = (widthSlow - widthMid - widthFast) / 2 + 104;
    DrawOptionMenuChoice(gText_TextSpeedMid, xMid, y, styles[1]);

    DrawOptionMenuChoice(gText_TextSpeedFast, GetStringRightAlignXOffset(FONT_NORMAL, gText_TextSpeedFast, 198), y, styles[2]);
}

static u8 BattleScene_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        selection ^= 1;
        sArrowPressed = TRUE;
    }

    return selection;
}

static void BattleScene_DrawChoices(u8 selection, u8 y)
{
    u8 styles[2];

    styles[0] = 0;
    styles[1] = 0;
    styles[selection] = 1;

    DrawOptionMenuChoice(gText_BattleSceneOn, 104, y, styles[0]);
    DrawOptionMenuChoice(gText_BattleSceneOff, GetStringRightAlignXOffset(FONT_NORMAL, gText_BattleSceneOff, 198), y, styles[1]);
}

static u8 BattleStyle_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        selection ^= 1;
        sArrowPressed = TRUE;
    }

    return selection;
}

static void BattleStyle_DrawChoices(u8 selection, u8 y)
{
    u8 styles[2];

    styles[0] = 0;
    styles[1] = 0;
    styles[selection] = 1;

    DrawOptionMenuChoice(gText_BattleStyleShift, 104, y, styles[0]);
    DrawOptionMenuChoice(gText_BattleStyleSet, GetStringRightAlignXOffset(FONT_NORMAL, gText_BattleStyleSet, 198), y, styles[1]);
}

static u8 OnOff_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        selection ^= 1;
        sArrowPressed = TRUE;
    }

    return selection;
}

static void OnOff_DrawChoices(u8 selection, u8 y)
{
    u8 styles[2];

    styles[0] = 0;
    styles[1] = 0;
    styles[selection] = 1;

    DrawOptionMenuChoice(gText_LegendsToggleOn, 104, y, styles[0]);
    DrawOptionMenuChoice(gText_LegendsToggleOff, GetStringRightAlignXOffset(FONT_NORMAL, gText_LegendsToggleOff, 198), y, styles[1]);
}

static u8 ShinyRate_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        selection = (selection + 1) % LEGENDS_SHINY_RATE_COUNT;
        sArrowPressed = TRUE;
    }
    else if (JOY_NEW(DPAD_LEFT))
    {
        selection = (selection + LEGENDS_SHINY_RATE_COUNT - 1) % LEGENDS_SHINY_RATE_COUNT;
        sArrowPressed = TRUE;
    }

    return selection;
}

static void ShinyRate_DrawChoices(u8 selection, u8 y)
{
    const u8 *text;

    switch (selection)
    {
    case LEGENDS_SHINY_RATE_5680:
        text = gText_LegendsShiny5680;
        break;
    case LEGENDS_SHINY_RATE_1226:
        text = gText_LegendsShiny1226;
        break;
    case LEGENDS_SHINY_RATE_8192:
    default:
        text = gText_LegendsShiny8192;
        break;
    }

    // Render only the selected value; keep the original window dimensions.
    DrawOptionMenuChoice(text, 130, y, 1);
}

static u8 SeasonMode_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        selection ^= 1;
        sArrowPressed = TRUE;
    }
    return selection;
}

static void SeasonMode_DrawChoices(u8 selection, u8 y)
{
    const u8 *text = selection == LEGENDS_SEASONS_PLAYTIME
                  ? COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}7H PLAY")
                  : COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}REAL TIME");
    FillWindowPixelRect(WIN_OPTIONS, PIXEL_FILL(1), 104, y, 96, OPTION_ROW_HEIGHT);
    DrawOptionMenuChoice(text, 120, y, 1);
}

static void DrawSeasonName(u8 season, u8 y, bool32 editable)
{
    u8 text[24];
    StringCopy(text, COMPOUND_STRING("{COLOR GREEN}{SHADOW LIGHT_GREEN}"));
    StringAppend(text, LegendsGetSeasonName(season));
    FillWindowPixelRect(WIN_OPTIONS, PIXEL_FILL(1), 104, y, 96, OPTION_ROW_HEIGHT);
    DrawOptionMenuChoice(text, 130, y, editable);
}

static void Season_DrawChoice(u8 y)
{
    DrawSeasonName(LegendsGetActiveSeason(), y, FALSE);
}

static u8 SetSeason_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        selection = (selection + 1) % LEGENDS_SEASON_COUNT;
        sArrowPressed = TRUE;
    }
    else if (JOY_NEW(DPAD_LEFT))
    {
        selection = (selection + LEGENDS_SEASON_COUNT - 1) % LEGENDS_SEASON_COUNT;
        sArrowPressed = TRUE;
    }
    return selection;
}

static void SetSeason_DrawChoice(u8 mode, u8 season, u8 y)
{
    if (mode == LEGENDS_SEASONS_RTC)
    {
        FillWindowPixelRect(WIN_OPTIONS, PIXEL_FILL(1), 104, y, 96, OPTION_ROW_HEIGHT);
        DrawOptionMenuChoice(COMPOUND_STRING("{COLOR LIGHT_GRAY}{SHADOW DARK_GRAY}CALENDAR"), 120, y, 0);
    }
    else
        DrawSeasonName(season, y, TRUE);
}

static u8 Sound_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_LEFT | DPAD_RIGHT))
    {
        selection ^= 1;
        SetPokemonCryStereo(selection);
        sArrowPressed = TRUE;
    }

    return selection;
}

static void Sound_DrawChoices(u8 selection, u8 y)
{
    u8 styles[2];

    styles[0] = 0;
    styles[1] = 0;
    styles[selection] = 1;

    DrawOptionMenuChoice(gText_SoundMono, 104, y, styles[0]);
    DrawOptionMenuChoice(gText_SoundStereo, GetStringRightAlignXOffset(FONT_NORMAL, gText_SoundStereo, 198), y, styles[1]);
}

static u8 FrameType_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        if (selection < WINDOW_FRAMES_COUNT - 1)
            selection++;
        else
            selection = 0;

        LoadBgTiles(1, GetWindowFrameTilesPal(selection)->tiles, 0x120, 0x1A2);
        LoadPalette(GetWindowFrameTilesPal(selection)->pal, BG_PLTT_ID(7), PLTT_SIZE_4BPP);
        sArrowPressed = TRUE;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        if (selection != 0)
            selection--;
        else
            selection = WINDOW_FRAMES_COUNT - 1;

        LoadBgTiles(1, GetWindowFrameTilesPal(selection)->tiles, 0x120, 0x1A2);
        LoadPalette(GetWindowFrameTilesPal(selection)->pal, BG_PLTT_ID(7), PLTT_SIZE_4BPP);
        sArrowPressed = TRUE;
    }
    return selection;
}

static void FrameType_DrawChoices(u8 selection, u8 y)
{
    u8 text[16] = {EOS};
    u8 n = selection + 1;
    u16 i;

    for (i = 0; gText_FrameTypeNumber[i] != EOS && i <= 5; i++)
        text[i] = gText_FrameTypeNumber[i];

    // Convert a number to decimal string
    if (n / 10 != 0)
    {
        text[i] = n / 10 + CHAR_0;
        i++;
        text[i] = n % 10 + CHAR_0;
        i++;
    }
    else
    {
        text[i] = n % 10 + CHAR_0;
        i++;
        text[i] = CHAR_SPACER;
        i++;
    }

    text[i] = EOS;

    DrawOptionMenuChoice(gText_FrameType, 104, y, 0);
    DrawOptionMenuChoice(text, 128, y, 1);
}

static u8 ButtonMode_ProcessInput(u8 selection)
{
    if (JOY_NEW(DPAD_RIGHT))
    {
        if (selection <= 1)
            selection++;
        else
            selection = 0;

        sArrowPressed = TRUE;
    }
    if (JOY_NEW(DPAD_LEFT))
    {
        if (selection != 0)
            selection--;
        else
            selection = 2;

        sArrowPressed = TRUE;
    }
    return selection;
}

static void ButtonMode_DrawChoices(u8 selection, u8 y)
{
    s32 widthNormal, widthLR, widthLA, xLR;
    u8 styles[3];

    styles[0] = 0;
    styles[1] = 0;
    styles[2] = 0;
    styles[selection] = 1;

    DrawOptionMenuChoice(gText_ButtonTypeNormal, 104, y, styles[0]);

    widthNormal = GetStringWidth(FONT_NORMAL, gText_ButtonTypeNormal, 0);
    widthLR = GetStringWidth(FONT_NORMAL, gText_ButtonTypeLR, 0);
    widthLA = GetStringWidth(FONT_NORMAL, gText_ButtonTypeLEqualsA, 0);

    widthLR -= 94;
    xLR = (widthNormal - widthLR - widthLA) / 2 + 104;
    DrawOptionMenuChoice(gText_ButtonTypeLR, xLR, y, styles[1]);

    DrawOptionMenuChoice(gText_ButtonTypeLEqualsA, GetStringRightAlignXOffset(FONT_NORMAL, gText_ButtonTypeLEqualsA, 198), y, styles[2]);
}

static u8 GetOptionMenuItem(u8 taskId)
{
    return sOptionMenuPageItems[gTasks[taskId].tMenuPage][gTasks[taskId].tMenuSelection];
}

static void ChangeOptionMenuPage(u8 taskId, s8 direction)
{
    s16 page = gTasks[taskId].tMenuPage + direction;

    if (page < 0)
        page = OPTION_PAGE_COUNT - 1;
    else if (page >= OPTION_PAGE_COUNT)
        page = 0;

    gTasks[taskId].tMenuPage = page;
    gTasks[taskId].tMenuSelection = 0;

    DrawHeaderText(gTasks[taskId].tMenuPage);
    DrawOptionMenuPage(taskId);
    HighlightOptionMenuItem(gTasks[taskId].tMenuSelection);
}

static void DrawHeaderText(u8 page)
{
    s32 versionStart = GetStringRightAlignXOffset(FONT_NORMAL, gText_LegendsVersion, 200);

    FillWindowPixelBuffer(WIN_HEADER, PIXEL_FILL(1));
    AddTextPrinterParameterized(WIN_HEADER, FONT_NORMAL, sOptionMenuPageTitles[page], 8, 1, TEXT_SKIP_DRAW, NULL);

    AddTextPrinterParameterized(WIN_HEADER, FONT_NORMAL, gText_LegendsVersion,
                                versionStart, 1, TEXT_SKIP_DRAW, NULL);
    CopyWindowToVram(WIN_HEADER, COPYWIN_FULL);
}

static void DrawOptionMenuPage(u8 taskId)
{
    u8 row;
    u8 itemId;
    u8 page = gTasks[taskId].tMenuPage;
    u8 itemCount = sOptionMenuPageItemCounts[page];

    FillWindowPixelBuffer(WIN_OPTIONS, PIXEL_FILL(1));

    for (row = 0; row < itemCount; row++)
    {
        itemId = sOptionMenuPageItems[page][row];
        AddTextPrinterParameterized(WIN_OPTIONS, FONT_NORMAL, sOptionMenuItemsNames[itemId],
                                    8, (row * OPTION_ROW_HEIGHT) + 1, TEXT_SKIP_DRAW, NULL);

        switch (itemId)
        {
        case MENUITEM_STARTERS:
            StarterSetting_DrawChoice(gTasks[taskId].tStarterSetting, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_STARTERINFO:
            DrawOptionMenuChoice(COMPOUND_STRING("NEW GAME"), 104, row * OPTION_ROW_HEIGHT, 0);
            break;
        case MENUITEM_NEXTPAGE:
            AddTextPrinterParameterized(WIN_OPTIONS, FONT_SMALL, gText_PageControls,
                                        104, row * OPTION_ROW_HEIGHT + 2, TEXT_SKIP_DRAW, NULL);
            break;
        case MENUITEM_TEXTSPEED:
            TextSpeed_DrawChoices(gTasks[taskId].tTextSpeed, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_BATTLESCENE:
            BattleScene_DrawChoices(gTasks[taskId].tBattleSceneOff, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_BATTLESTYLE:
            BattleStyle_DrawChoices(gTasks[taskId].tBattleStyle, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_EXPSHARE:
            OnOff_DrawChoices(gTasks[taskId].tExpShare, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_FOLLOWERS:
            OnOff_DrawChoices(gTasks[taskId].tFollowers, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_SHINYRATE:
            ShinyRate_DrawChoices(gTasks[taskId].tShinyRate, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_SEASONMODE:
            SeasonMode_DrawChoices(gTasks[taskId].tSeasonMode, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_SEASON:
            Season_DrawChoice(row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_SETSEASON:
            SetSeason_DrawChoice(gTasks[taskId].tSeasonMode, gTasks[taskId].tSelectedSeason, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_SOUND:
            Sound_DrawChoices(gTasks[taskId].tSound, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_BUTTONMODE:
            ButtonMode_DrawChoices(gTasks[taskId].tButtonMode, row * OPTION_ROW_HEIGHT);
            break;
        case MENUITEM_FRAMETYPE:
            FrameType_DrawChoices(gTasks[taskId].tWindowFrameType, row * OPTION_ROW_HEIGHT);
            break;
        }
    }

    CopyWindowToVram(WIN_OPTIONS, COPYWIN_FULL);
}

#define TILE_TOP_CORNER_L 0x1A2
#define TILE_TOP_EDGE     0x1A3
#define TILE_TOP_CORNER_R 0x1A4
#define TILE_LEFT_EDGE    0x1A5
#define TILE_RIGHT_EDGE   0x1A7
#define TILE_BOT_CORNER_L 0x1A8
#define TILE_BOT_EDGE     0x1A9
#define TILE_BOT_CORNER_R 0x1AA

static void DrawBgWindowFrames(void)
{
    //                     bg, tile,              x, y, width, height, palNum
    // Draw title window frame
    FillBgTilemapBufferRect(1, TILE_TOP_CORNER_L,  1,  0,  1,  1,  7);
    FillBgTilemapBufferRect(1, TILE_TOP_EDGE,      2,  0, 27,  1,  7);
    FillBgTilemapBufferRect(1, TILE_TOP_CORNER_R, 28,  0,  1,  1,  7);
    FillBgTilemapBufferRect(1, TILE_LEFT_EDGE,     1,  1,  1,  2,  7);
    FillBgTilemapBufferRect(1, TILE_RIGHT_EDGE,   28,  1,  1,  2,  7);
    FillBgTilemapBufferRect(1, TILE_BOT_CORNER_L,  1,  3,  1,  1,  7);
    FillBgTilemapBufferRect(1, TILE_BOT_EDGE,      2,  3, 27,  1,  7);
    FillBgTilemapBufferRect(1, TILE_BOT_CORNER_R, 28,  3,  1,  1,  7);

    // Draw options list window frame
    FillBgTilemapBufferRect(1, TILE_TOP_CORNER_L,  1,  4,  1,  1,  7);
    FillBgTilemapBufferRect(1, TILE_TOP_EDGE,      2,  4, 26,  1,  7);
    FillBgTilemapBufferRect(1, TILE_TOP_CORNER_R, 28,  4,  1,  1,  7);
    FillBgTilemapBufferRect(1, TILE_LEFT_EDGE,     1,  5,  1, 14,  7);
    FillBgTilemapBufferRect(1, TILE_RIGHT_EDGE,   28,  5,  1, 14,  7);
    FillBgTilemapBufferRect(1, TILE_BOT_CORNER_L,  1, 19,  1,  1,  7);
    FillBgTilemapBufferRect(1, TILE_BOT_EDGE,      2, 19, 26,  1,  7);
    FillBgTilemapBufferRect(1, TILE_BOT_CORNER_R, 28, 19,  1,  1,  7);

    CopyBgTilemapBufferToVram(1);
}
