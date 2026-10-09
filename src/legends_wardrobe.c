#include "global.h"
#include "legends_wardrobe.h"
#include "legends_appearance.h"
#include "bg.h"
#include "gpu_regs.h"
#include "event_data.h"
#include "main.h"
#include "menu.h"
#include "overworld.h"
#include "palette.h"
#include "scanline_effect.h"
#include "script.h"
#include "secret_base.h"
#include "sprite.h"
#include "task.h"
#include "text.h"
#include "text_window.h"
#include "trainer_pokemon_sprites.h"
#include "window.h"
#include "constants/maps.h"
#include "constants/metatile_labels.h"
#include "constants/rgb.h"
#include "constants/vars.h"

static const struct BgTemplate sBackground = {.bg=0, .charBaseIndex=0, .mapBaseIndex=31, .priority=0};
static const struct WindowTemplate sWindows[] = {
    {.bg=0,.tilemapLeft=2,.tilemapTop=2,.width=26,.height=3,.paletteNum=15,.baseBlock=1},
    {.bg=0,.tilemapLeft=2,.tilemapTop=7,.width=15,.height=11,.paletteNum=15,.baseBlock=79},
    {.bg=0,.tilemapLeft=19,.tilemapTop=7,.width=8,.height=8,.paletteNum=8,.baseBlock=244},
    DUMMY_WIN_TEMPLATE
};
static const u8 *const sOutfits[] = {COMPOUND_STRING("EMERALD"),COMPOUND_STRING("TRAIL"),COMPOUND_STRING("SPORT"),COMPOUND_STRING("YELLOW"),COMPOUND_STRING("LAVENDER")};
static const u8 *const sScarves[] = {COMPOUND_STRING("NONE"),COMPOUND_STRING("CRIMSON"),COMPOUND_STRING("OCEAN"),COMPOUND_STRING("EMERALD"),COMPOUND_STRING("LAVENDER"),COMPOUND_STRING("CREAM")};
static const u8 *const sRows[] = {COMPOUND_STRING("OUTFIT"),COMPOUND_STRING("SCARF"),COMPOUND_STRING("JACKET"),COMPOUND_STRING("APPLY"),COMPOUND_STRING("CANCEL")};
static void Task_Input(u8 taskId);
static void CB2_InitWardrobe(void);

bool8 LegendsCanUseWardrobe(void)
{
    if (CurMapIsSecretBase())
        return VarGet(VAR_CURRENT_SECRET_BASE) == 0;
    return gSaveBlock1Ptr->location.mapGroup == MAP_GROUP(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F)
        && gSaveBlock1Ptr->location.mapNum == (gSaveBlock2Ptr->playerGender == FEMALE
            ? MAP_NUM(MAP_LITTLEROOT_TOWN_MAYS_HOUSE_2F) : MAP_NUM(MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F));
}

bool8 LegendsIsWardrobeMetatile(u16 metatile)
{
    return metatile == METATILE_SecretBase_LegendsWardrobe_Top || metatile == METATILE_SecretBase_LegendsWardrobe_Bottom;
}

static void Print(u8 w,const u8 *text,u8 x,u8 y)
{
    AddTextPrinterParameterized(w,FONT_SMALL,text,x,y,TEXT_SKIP_DRAW,NULL);
}

static void Draw(u8 taskId)
{
    u8 i, row=gTasks[taskId].data[0];
    FillWindowPixelBuffer(1,PIXEL_FILL(1));
    for (i=0;i<5;i++)
    {
        Print(1,sRows[i],12,i*16);
        if (i==0) Print(1,sOutfits[LegendsGetOutfit()],58,i*16);
        if (i==1) Print(1,sScarves[LegendsGetScarf()],58,i*16);
        if (i==2) Print(1,LegendsGetJacket()?COMPOUND_STRING("NAVY"):COMPOUND_STRING("NONE"),58,i*16);
    }
    Print(1,COMPOUND_STRING(">"),0,row*16);
    CopyWindowToVram(1,COPYWIN_FULL);
    // Native Trainer Card drawing owns and frees its temporary graphics buffer.
    FillWindowPixelBuffer(2,PIXEL_FILL(0));
    CreateTrainerCardTrainerPicSprite(LegendsGetPlayerTrainerPic(gSaveBlock2Ptr->playerGender),TRUE,0,0,8,2);
    CopyWindowToVram(2,COPYWIN_FULL);
}

static void Main(void) { RunTasks(); AnimateSprites(); BuildOamBuffer(); UpdatePaletteFade(); }
static void VBlank(void) { LoadOam(); ProcessSpriteCopyRequests(); TransferPlttBuffer(); }
static void Task_Return(u8 taskId)
{
    if (gPaletteFade.active) return;
    SetVBlankCallback(NULL);
    FreeAllWindowBuffers();
    DestroyTask(taskId);
    SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
}

static void Task_Input(u8 taskId)
{
    u8 row=gTasks[taskId].data[0];
    if (gPaletteFade.active) return;
    if (JOY_NEW(B_BUTTON) || (JOY_NEW(A_BUTTON) && row>=3))
    {
        if (JOY_NEW(A_BUTTON) && row==3) LegendsApplyWardrobeSelection();
        else LegendsClearAppearanceSelection();
        BeginNormalPaletteFade(PALETTES_ALL,0,0,16,RGB_BLACK);
        gTasks[taskId].func=Task_Return;
        return;
    }
    if (JOY_NEW(DPAD_UP)) gTasks[taskId].data[0]=(row+4)%5;
    else if (JOY_NEW(DPAD_DOWN)) gTasks[taskId].data[0]=(row+1)%5;
    else if (row<3 && (JOY_NEW(DPAD_LEFT|DPAD_RIGHT|A_BUTTON)))
    {
        u8 count=row==0?LEGENDS_OUTFIT_COUNT:row==1?LEGENDS_SCARF_COUNT:2;
        u8 value=row==0?LegendsGetOutfit():row==1?LegendsGetScarf():LegendsGetJacket();
        value=(value+(JOY_NEW(DPAD_LEFT)?count-1:1))%count;
        if (row==0) LegendsSetAppearanceSelection(LegendsGetSkinTone(),value);
        else LegendsSetAccessorySelection(row==1?value:LegendsGetScarf(),row==2?value:LegendsGetJacket());
    }
    else return;
    Draw(taskId);
}

static void CB2_InitWardrobe(void)
{
    u8 i, taskId;
    SetVBlankCallback(NULL);
    SetGpuReg(REG_OFFSET_DISPCNT,0);
    DmaClearLarge16(3,(void *)VRAM,VRAM_SIZE,0x1000);
    DmaClear32(3,OAM,OAM_SIZE);
    ResetBgsAndClearDma3BusyFlags(0);
    InitBgsFromTemplates(0,&sBackground,1);
    ChangeBgX(0,0,BG_COORD_SET);ChangeBgY(0,0,BG_COORD_SET);
    ResetPaletteFade();ScanlineEffect_Stop();ResetTasks();ResetSpriteData();
    if (!InitWindowsUnchecked(sWindows))
    {
        FreeAllWindowBuffers();
        LegendsClearAppearanceSelection();
        SetMainCallback2(CB2_ReturnToFieldContinueScriptPlayMapMusic);
        return;
    }
    DeactivateAllTextPrinters();
    { const u16 color=RGB(22,20,29);LoadPalette(&color,0,sizeof(color)); }
    LoadPalette(gStandardMenuPalette,BG_PLTT_ID(15),PLTT_SIZE_4BPP);
    LoadUserWindowBorderGfx(0,STD_WINDOW_BASE_TILE_NUM,BG_PLTT_ID(STD_WINDOW_PALETTE_NUM));
    SetGpuReg(REG_OFFSET_BLDCNT,0);SetGpuReg(REG_OFFSET_BLDY,0);
    for (i=0;i<3;i++) {FillWindowPixelBuffer(i,PIXEL_FILL(1));PutWindowTilemap(i);DrawStdWindowFrame(i,FALSE);}
    Print(0,COMPOUND_STRING("WARDROBE                     B: CANCEL"),0,0);
    Print(0,COMPOUND_STRING("UP/DOWN: SELECT  LEFT/RIGHT: CHANGE"),0,12);
    CopyWindowToVram(0,COPYWIN_FULL);
    taskId=CreateTask(Task_Input,0);Draw(taskId);
    BeginNormalPaletteFade(PALETTES_ALL,0,16,0,RGB_BLACK);
    SetGpuReg(REG_OFFSET_DISPCNT,DISPCNT_OBJ_ON|DISPCNT_OBJ_1D_MAP);
    ShowBg(0);SetVBlankCallback(VBlank);SetMainCallback2(Main);
}

static void Task_Enter(u8 taskId)
{
    if (gPaletteFade.active) return;
    CleanupOverworldWindowsAndTilemaps();
    DestroyTask(taskId);SetMainCallback2(CB2_InitWardrobe);
}

void LegendsOpenWardrobe(void)
{
    if (!LegendsCanUseWardrobe()) {ScriptContext_Enable();return;}
    LegendsBeginWardrobeSelection();
    BeginNormalPaletteFade(PALETTES_ALL,0,0,16,RGB_BLACK);
    CreateTask(Task_Enter,0);
}
