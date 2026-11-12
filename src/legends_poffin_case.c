#include "global.h"
#include "legends_poffin.h"
#include "bg.h"
#include "event_data.h"
#include "gpu_regs.h"
#include "main.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "pokeblock.h"
#include "pokemon.h"
#include "party_menu.h"
#include "scanline_effect.h"
#include "sound.h"
#include "sprite.h"
#include "string_util.h"
#include "task.h"
#include "text.h"
#include "trainer_pokemon_sprites.h"
#include "window.h"
#include "constants/rgb.h"
#include "constants/songs.h"

#define POFFIN_SAVE_SIGNATURE 0x31464650
#define VISIBLE_TREATS 4
STATIC_ASSERT(LEGENDS_POFFIN_CAPACITY >= POKEBLOCKS_COUNT, PoffinMigrationCapacity);

static const u32 sCaseBackground[] = INCGFX_U32("graphics/poffin/case_bg.png", ".4bpp");
static const u32 sFeedBackground[] = INCGFX_U32("graphics/poffin/feed_bg.png", ".4bpp");
static const u16 sPalette[] = INCGFX_U16("graphics/poffin/kitchen.png", ".gbapal");
static const u32 sServed[] = INCGFX_U32("graphics/poffin/served.png", ".4bpp");
static const u32 sMini[] = INCGFX_U32("graphics/poffin/mini.png", ".4bpp");
static const u16 sFlavorColors[][2] = {
    {RGB(26,10,11), RGB(31,18,16)}, {RGB(12,15,23), RGB(18,22,27)},
    {RGB(27,15,20), RGB(31,22,25)}, {RGB(13,21,14), RGB(20,26,18)},
    {RGB(28,23,10), RGB(31,28,18)}
};
static const u8 *const sFlavors[] = {
    COMPOUND_STRING("Spicy"), COMPOUND_STRING("Dry"), COMPOUND_STRING("Sweet"),
    COMPOUND_STRING("Bitter"), COMPOUND_STRING("Sour")
};
static const u8 *const sAbbreviations[] = {
    COMPOUND_STRING("SP"), COMPOUND_STRING("DR"), COMPOUND_STRING("SW"),
    COMPOUND_STRING("BI"), COMPOUND_STRING("SO")
};
static const struct BgTemplate sBackground = {.bg = 0, .mapBaseIndex = 31};
static const struct WindowTemplate sWindows[] = {
    {.width = 30, .height = 20, .baseBlock = 1}, DUMMY_WIN_TEMPLATE
};
static const union AnimCmd sStill[] = {ANIMCMD_FRAME(0, 1), ANIMCMD_END};
static const union AnimCmd sBiteOne[] = {ANIMCMD_FRAME(1, 1), ANIMCMD_END};
static const union AnimCmd sBiteTwo[] = {ANIMCMD_FRAME(2, 1), ANIMCMD_END};
static const union AnimCmd sFinished[] = {ANIMCMD_FRAME(3, 1), ANIMCMD_END};
static const union AnimCmd *const sServedAnims[] = {sStill, sBiteOne, sBiteTwo, sFinished};
static const struct SpriteFrameImage sServedImages[] = {
    {.data = (const u8 *)sServed, .size = 2048},
    {.data = (const u8 *)sServed + 2048, .size = 2048},
    {.data = (const u8 *)sServed + 4096, .size = 2048},
    {.data = (const u8 *)sServed + 6144, .size = 2048},
};
static const struct SpriteFrameImage sMiniImages[] = {obj_frame_tiles(sMini)};
static const struct OamData sLargeOam = {.size = SPRITE_SIZE(64x64)};
static const struct OamData sSmallOam = {.size = SPRITE_SIZE(32x32)};
static const struct SpriteTemplate sServedTemplate = {
    .tileTag = TAG_NONE, .paletteTag = TAG_NONE, .oam = &sLargeOam,
    .anims = sServedAnims, .images = sServedImages,
    .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
static const struct SpriteTemplate sMiniTemplate = {
    .tileTag = TAG_NONE, .paletteTag = TAG_NONE, .oam = &sSmallOam,
    .anims = sServedAnims, .images = sMiniImages,
    .affineAnims = gDummySpriteAffineAnimTable, .callback = SpriteCallbackDummy,
};
enum ScreenAction { ACTION_NONE, ACTION_EXIT, ACTION_FEED };
static EWRAM_DATA struct
{
    MainCallback returnCallback;
    struct Pokeblock *feeding;
    u8 slots[LEGENDS_POFFIN_CAPACITY];
    u8 count, selected, top, action, hero, thumbnails[VISIBLE_TREATS];
    u16 monSprite, frame;
} sCase = {0};

void LegendsPoffinInit(bool32 newGame)
{
    struct LegendsPoffinSave *save = &gSaveBlock3Ptr->poffins;
    if (newGame || save->signature != POFFIN_SAVE_SIGNATURE)
    {
        memset(save, 0, sizeof(*save));
        if (!newGame)
        {
            // The first preview used native records. Move each once into the
            // independent case, retaining its exact flavors, level and feel.
            u8 slot = 0;
            for (u8 i = 0; i < POKEBLOCKS_COUNT; i++)
            {
                struct Pokeblock *old = &gSaveBlock1Ptr->pokeblocks[i];
                if (old->color >= POFFIN_SPICY && old->color <= POFFIN_SOUR)
                {
                    save->treats[slot++] = *old;
                    memset(old, 0, sizeof(*old));
                }
            }
        }
        save->signature = POFFIN_SAVE_SIGNATURE;
    }
    for (u8 i = 0; i < LEGENDS_POFFIN_CAPACITY; i++)
        if (save->treats[i].color && (save->treats[i].color < POFFIN_SPICY || save->treats[i].color > POFFIN_SOUR))
            memset(&save->treats[i], 0, sizeof(save->treats[i]));
}

s16 LegendsPoffinFreeSlot(void)
{
    LegendsPoffinInit(FALSE);
    for (u8 i = 0; i < LEGENDS_POFFIN_CAPACITY; i++)
        if (!gSaveBlock3Ptr->poffins.treats[i].color)
            return i;
    return -1;
}

bool32 LegendsPoffinStore(const struct Pokeblock *treat)
{
    s16 slot = LegendsPoffinFreeSlot();
    if (slot < 0)
        return FALSE;
    gSaveBlock3Ptr->poffins.treats[slot] = *treat;
    return TRUE;
}

static void Print(const u8 *text, u8 x, u8 y, bool32 small, u8 color)
{
    const u8 colors[] = {0, color, 3};
    AddTextPrinterParameterized3(0, small ? FONT_SMALL : FONT_NORMAL, x, y, colors, TEXT_SKIP_DRAW, text);
}

static void Number(u16 n, u8 x, u8 y, bool32 small)
{
    ConvertIntToDecimalStringN(gStringVar1, n, STR_CONV_MODE_LEFT_ALIGN, 3);
    Print(gStringVar1, x, y, small, 2);
}

static void ColorPoffin(const struct Pokeblock *treat, u8 palette)
{
    u8 primary = treat->color - POFFIN_SPICY;
    u8 secondary = primary;
    u16 colors[16];
    memcpy(colors, sPalette, sizeof(colors));
    for (u8 i = 0; i < FLAVOR_COUNT; i++)
        if (i != primary && GetPokeblockData(treat, i + PBLOCK_SPICY) > 0
            && (secondary == primary || GetPokeblockData(treat, i + PBLOCK_SPICY) > GetPokeblockData(treat, secondary + PBLOCK_SPICY)))
            secondary = i;
    colors[9] = sFlavorColors[primary][0];
    colors[10] = sFlavorColors[primary][1];
    colors[15] = sFlavorColors[secondary][1];
    LoadPalette(colors, OBJ_PLTT_ID(palette), sizeof(colors));
}

static void RemoveDisplaySprites(void)
{
    if (sCase.hero != SPRITE_NONE)
        DestroySprite(&gSprites[sCase.hero]);
    for (u8 i = 0; i < VISIBLE_TREATS; i++)
        if (sCase.thumbnails[i] != SPRITE_NONE)
            DestroySprite(&gSprites[sCase.thumbnails[i]]);
    sCase.hero = SPRITE_NONE;
    memset(sCase.thumbnails, SPRITE_NONE, sizeof(sCase.thumbnails));
}

static void DrawCase(void)
{
    RemoveDisplaySprites();
    CopyToWindowPixelBuffer(0, sCaseBackground, sizeof(sCaseBackground), 0);
    Print(COMPOUND_STRING("TREAT CASE"), 12, 0, FALSE, 14);
    ConvertIntToDecimalStringN(gStringVar1, sCase.count, STR_CONV_MODE_RIGHT_ALIGN, 2);
    StringAppend(gStringVar1, COMPOUND_STRING("/40"));
    Print(gStringVar1, 193, 0, FALSE, 14);
    Print(COMPOUND_STRING("A: Feed    B: Close"), 10, 142, TRUE, 14);
    if (!sCase.count)
    {
        Print(COMPOUND_STRING("Ready for"), 126, 45, FALSE, 2);
        Print(COMPOUND_STRING("fresh POFFINS!"), 121, 62, TRUE, 2);
        Print(COMPOUND_STRING("Cook a batch at"), 122, 90, TRUE, 2);
        Print(COMPOUND_STRING("a POFFIN MAKER."), 122, 104, TRUE, 2);
    }
    else
    {
        struct Pokeblock *selected = &gSaveBlock3Ptr->poffins.treats[sCase.slots[sCase.selected]];
        ColorPoffin(selected, 0);
        sCase.hero = CreateSprite(&sServedTemplate, 58, 56, 0);
        Print(COMPOUND_STRING("Feel"), 14, 94, TRUE, 2);
        Number(selected->feel, 39, 94, TRUE);
        for (u8 i = 0; i < FLAVOR_COUNT; i++)
        {
            Print(sAbbreviations[i], 12 + i * 19, 107, TRUE, 11);
            Number(GetPokeblockData(selected, PBLOCK_SPICY + i), 12 + i * 19, 119, TRUE);
        }
        for (u8 row = 0; row < VISIBLE_TREATS && row + sCase.top < sCase.count; row++)
        {
            u8 index = row + sCase.top;
            struct Pokeblock *treat = &gSaveBlock3Ptr->poffins.treats[sCase.slots[index]];
            u8 y = 28 + row * 24;
            if (index == sCase.selected)
                FillWindowPixelRect(0, 1, 119, y, 112, 24);
            sCase.thumbnails[row] = CreateSprite(&sMiniTemplate, 134, y + 12, 0);
            if (sCase.thumbnails[row] != SPRITE_NONE)
                gSprites[sCase.thumbnails[row]].oam.paletteNum = row + 1;
            ColorPoffin(treat, row + 1);
            Print(sFlavors[treat->color - POFFIN_SPICY], 151, y, TRUE, 2);
            Print(COMPOUND_STRING("Lv."), 151, y + 11, TRUE, 11);
            Number(GetHighestPokeblocksFlavorLevel(treat), 169, y + 11, TRUE);
        }
        if (sCase.top)
            Print(COMPOUND_STRING("{UP_ARROW}"), 222, 23, TRUE, 11);
        if (sCase.top + VISIBLE_TREATS < sCase.count)
            Print(COMPOUND_STRING("{DOWN_ARROW}"), 222, 118, TRUE, 11);
    }
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void VBlank(void)
{
    LoadOam();
    ProcessSpriteCopyRequests();
    TransferPlttBuffer();
}

static bool32 InitDisplay(const u32 *background)
{
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT, 0);
    DmaClearLarge16(3, (void *)VRAM, VRAM_SIZE, 0x1000);
    DmaClear32(3, OAM, OAM_SIZE);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0, &sBackground, 1);
    ChangeBgX(0, 0, BG_COORD_SET);
    ChangeBgY(0, 0, BG_COORD_SET);
    ResetPaletteFade();
    ScanlineEffect_Stop();
    ResetTasks();
    ResetSpriteData();
    FreeAllSpritePalettes();
    if (!InitWindowsUnchecked(sWindows))
        return FALSE;
    DeactivateAllTextPrinters();
    LoadPalette(sPalette, 0, sizeof(sPalette));
    CopyToWindowPixelBuffer(0, background, 240 * 160 / 2, 0);
    PutWindowTilemap(0);
    SetGpuReg(REG_OFFSET_BLDCNT, 0);
    SetGpuReg(REG_OFFSET_BLDY, 0);
    SetGpuReg(REG_OFFSET_DISPCNT, DISPCNT_OBJ_ON | DISPCNT_OBJ_1D_MAP);
    ShowBg(0);
    SetVBlankCallback(VBlank);
    return TRUE;
}

static void InitCase(void);

static void CaseMain(void)
{
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
    if (gPaletteFade.active)
        return;
    if (sCase.action)
    {
        u8 action = sCase.action;
        RemoveDisplaySprites();
        FreeAllWindowBuffers();
        SetVBlankCallback(NULL);
        if (action == ACTION_FEED)
            ChooseMonToGivePokeblock(&gSaveBlock3Ptr->poffins.treats[sCase.slots[sCase.selected]], InitCase);
        else
            SetMainCallback2(sCase.returnCallback);
        return;
    }
    if (JOY_NEW(B_BUTTON))
        sCase.action = ACTION_EXIT;
    else if (sCase.count && JOY_NEW(A_BUTTON))
        sCase.action = ACTION_FEED;
    else if (sCase.count && JOY_REPEAT(DPAD_UP | DPAD_DOWN))
    {
        if (JOY_REPEAT(DPAD_UP))
            sCase.selected = (sCase.selected + sCase.count - 1) % sCase.count;
        else
            sCase.selected = (sCase.selected + 1) % sCase.count;
        if (sCase.selected < sCase.top)
            sCase.top = sCase.selected;
        if (sCase.selected >= sCase.top + VISIBLE_TREATS)
            sCase.top = sCase.selected - VISIBLE_TREATS + 1;
        PlaySE(SE_SELECT);
        DrawCase();
    }
    if (sCase.action)
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
}

static void InitCase(void)
{
    LegendsPoffinInit(FALSE);
    sCase.count = 0;
    sCase.action = ACTION_NONE;
    sCase.hero = SPRITE_NONE;
    memset(sCase.thumbnails, SPRITE_NONE, sizeof(sCase.thumbnails));
    for (u8 i = 0; i < LEGENDS_POFFIN_CAPACITY; i++)
        if (gSaveBlock3Ptr->poffins.treats[i].color)
            sCase.slots[sCase.count++] = i;
    if (sCase.selected >= sCase.count)
        sCase.selected = 0;
    sCase.top = sCase.selected > VISIBLE_TREATS - 1 ? sCase.selected - VISIBLE_TREATS + 1 : 0;
    if (!InitDisplay(sCaseBackground))
    {
        FreeAllWindowBuffers();
        SetMainCallback2(sCase.returnCallback);
        return;
    }
    DrawCase();
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetMainCallback2(CaseMain);
}

void LegendsShowTreatCase(MainCallback callback)
{
    sCase.returnCallback = callback;
    sCase.selected = 0;
    SetMainCallback2(InitCase);
}

static void DrawFeedMessage(void)
{
    FillWindowPixelRect(0, 14, 10, 132, 218, 20);
    GetMonNickname(&gParties[B_TRAINER_PLAYER][gPokeblockMonId], gStringVar1);
    StringExpandPlaceholders(gStringVar4, sCase.frame < 210
        ? COMPOUND_STRING("A fresh POFFIN for {STR_VAR_1}!")
        : (gPokeblockGain > 0 ? COMPOUND_STRING("{STR_VAR_1} loved that flavor!")
        : gPokeblockGain < 0 ? COMPOUND_STRING("{STR_VAR_1} prefers another flavor.")
        : COMPOUND_STRING("{STR_VAR_1} enjoyed the POFFIN!")));
    Print(gStringVar4, 13, 135, TRUE, 2);
    CopyWindowToVram(0, COPYWIN_FULL);
}

static void FeedMain(void)
{
    AnimateSprites();
    BuildOamBuffer();
    UpdatePaletteFade();
    if (gPaletteFade.active)
        return;
    if (sCase.action == ACTION_EXIT)
    {
        if (sCase.monSprite < MAX_SPRITES)
            FreeAndDestroyMonPicSprite(sCase.monSprite);
        RemoveDisplaySprites();
        SetVBlankCallback(NULL);
        FreeAllWindowBuffers();
        SetMainCallback2(gMain.savedCallback);
        return;
    }
    if (sCase.frame < 210)
    {
        sCase.frame++;
        if (sCase.monSprite < MAX_SPRITES)
        {
            // Small forward nibbles; the plated pastry stays on the table.
            gSprites[sCase.monSprite].x2 = sCase.frame % 60 > 42 ? 4 : 0;
            gSprites[sCase.monSprite].y2 = sCase.frame % 60 > 42 ? 2 : 0;
        }
        if (sCase.frame == 60 || sCase.frame == 120 || sCase.frame == 180)
        {
            if (sCase.hero != SPRITE_NONE)
                StartSpriteAnim(&gSprites[sCase.hero], sCase.frame / 60);
            PlaySE(SE_USE_ITEM);
        }
        if (sCase.frame == 210)
        {
            if (sCase.monSprite < MAX_SPRITES)
            {
                gSprites[sCase.monSprite].x2 = 0;
                gSprites[sCase.monSprite].y2 = 0;
            }
            DrawFeedMessage();
            Print(COMPOUND_STRING("A: Continue"), 170, 0, TRUE, 14);
            CopyWindowToVram(0, COPYWIN_FULL);
        }
    }
    else if (JOY_NEW(A_BUTTON | B_BUTTON))
    {
        sCase.action = ACTION_EXIT;
        BeginNormalPaletteFade(PALETTES_ALL, 0, 0, 16, RGB_BLACK);
    }
}

static void InitFeed(void)
{
    struct Pokemon *mon = &gParties[B_TRAINER_PLAYER][gPokeblockMonId];
    sCase.frame = 0;
    sCase.action = ACTION_NONE;
    sCase.hero = SPRITE_NONE;
    memset(sCase.thumbnails, SPRITE_NONE, sizeof(sCase.thumbnails));
    gPokeblockGain = PokeblockGetGain(GetNature(mon), sCase.feeding);
    if (!InitDisplay(sFeedBackground))
    {
        FreeAllWindowBuffers();
        SetMainCallback2(gMain.savedCallback);
        return;
    }
    sCase.monSprite = CreateMonPicSprite(GetMonData(mon, MON_DATA_SPECIES), IsMonShiny(mon),
        GetMonData(mon, MON_DATA_PERSONALITY), TRUE, 67, 78, 6, TAG_NONE);
    ColorPoffin(sCase.feeding, 0);
    sCase.hero = CreateSprite(&sServedTemplate, 169, 85, 0);
    Print(COMPOUND_STRING("POFFIN TIME"), 12, 0, FALSE, 14);
    Print(sFlavors[sCase.feeding->color - POFFIN_SPICY], 146, 30, FALSE, 2);
    Print(COMPOUND_STRING("Lv."), 155, 45, TRUE, 11);
    Number(GetHighestPokeblocksFlavorLevel(sCase.feeding), 173, 45, TRUE);
    DrawFeedMessage();
    BeginNormalPaletteFade(PALETTES_ALL, 0, 16, 0, RGB_BLACK);
    SetMainCallback2(FeedMain);
}

void LegendsPreparePoffinFeed(struct Pokeblock *treat)
{
    sCase.feeding = treat;
    SetMainCallback2(InitFeed);
}
