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
    {.bg=0,.tilemapLeft=2,.tilemapTop=7,.width=16,.height=11,.paletteNum=15,.baseBlock=79},
    {.bg=0,.tilemapLeft=19,.tilemapTop=7,.width=8,.height=8,.paletteNum=8,.baseBlock=256},
    {.bg=0,.tilemapLeft=19,.tilemapTop=16,.width=8,.height=2,.paletteNum=9,.baseBlock=320},
    DUMMY_WIN_TEMPLATE
};
static const u8 *const sOutfits[] = {COMPOUND_STRING("EMERALD"),COMPOUND_STRING("TRAIL"),COMPOUND_STRING("SPORT"),COMPOUND_STRING("YELLOW"),COMPOUND_STRING("LAVENDER")};
static const u8 *const sScarves[] = {COMPOUND_STRING("NONE"),COMPOUND_STRING("CRIMSON"),COMPOUND_STRING("OCEAN"),COMPOUND_STRING("EMERALD"),COMPOUND_STRING("LAVENDER"),COMPOUND_STRING("CREAM")};
static const u8 *const sCostumes[] = {COMPOUND_STRING("NONE"),COMPOUND_STRING("TEAM MAGMA"),COMPOUND_STRING("TEAM AQUA")};
static const u8 *const sShoes[] = {COMPOUND_STRING("ORIGINAL"),COMPOUND_STRING("RED"),COMPOUND_STRING("BLUE"),COMPOUND_STRING("GREEN"),COMPOUND_STRING("WHITE"),COMPOUND_STRING("PURPLE"),COMPOUND_STRING("BROWN BOOTS"),COMPOUND_STRING("BLACK BOOTS")};
static const u8 *const sCardColors[] = {COMPOUND_STRING("ORIGINAL"),COMPOUND_STRING("EMERALD"),COMPOUND_STRING("OCEAN"),COMPOUND_STRING("CRIMSON"),COMPOUND_STRING("LAVENDER"),COMPOUND_STRING("GOLD"),COMPOUND_STRING("ROSE"),COMPOUND_STRING("SLATE")};
static const u8 *const sLeggings[] = {COMPOUND_STRING("NONE"),COMPOUND_STRING("GREY"),COMPOUND_STRING("BLACK")};
static const u8 *const sCoats[] = {COMPOUND_STRING("NONE"),COMPOUND_STRING("NAVY"),COMPOUND_STRING("WINTER")};
enum {ROW_OUTFIT,ROW_COSTUMES,ROW_HAIR,ROW_HAIR_COLOR,ROW_SCARF,ROW_JACKET,ROW_LEGGINGS,ROW_SHOES,ROW_CARD,ROW_APPLY,ROW_CANCEL,ROW_COUNT};
static const u8 *const sRows[] = {COMPOUND_STRING("OUTFIT"),COMPOUND_STRING("COSTUMES"),COMPOUND_STRING("HAIRSTYLE"),COMPOUND_STRING("HAIR COLOR"),COMPOUND_STRING("SCARF"),COMPOUND_STRING("JACKET"),COMPOUND_STRING("LEGGINGS"),COMPOUND_STRING("SHOES"),COMPOUND_STRING("TRAINER CARD"),COMPOUND_STRING("APPLY"),COMPOUND_STRING("CANCEL")};
#define WARDROBE_VISIBLE 6
static u8 WardrobeDisplayCount(void) { return ROW_COUNT - (gSaveBlock2Ptr->playerGender != FEMALE); }
static u8 WardrobeDisplayRow(u8 index)
{
    return gSaveBlock2Ptr->playerGender != FEMALE && index >= ROW_LEGGINGS ? index + 1 : index;
}
static u8 RowValue(u8 row)
{
    switch(row) {
    case ROW_OUTFIT:return LegendsGetOutfit();
    case ROW_COSTUMES:return LegendsGetCostume();
    case ROW_HAIR:return LegendsGetHair();
    case ROW_HAIR_COLOR:return LegendsGetHairColor();
    case ROW_SCARF:return LegendsGetScarf();
    case ROW_JACKET:return LegendsGetJacketStyle();
    case ROW_LEGGINGS:return LegendsGetLeggings();
    case ROW_SHOES:return LegendsGetShoes();
    case ROW_CARD:return LegendsGetCardColor();
    default:return 0;
    }
}
static u8 RowCount(u8 row)
{
    static const u8 counts[] = {LEGENDS_OUTFIT_COUNT,LEGENDS_COSTUME_COUNT,LEGENDS_HAIR_COUNT,LEGENDS_HAIR_COLOR_COUNT,LEGENDS_SCARF_COUNT,LEGENDS_JACKET_COUNT,LEGENDS_LEGGINGS_COUNT,LEGENDS_SHOE_COUNT,LEGENDS_CARD_COLOR_COUNT};
    if (row == ROW_LEGGINGS && gSaveBlock2Ptr->playerGender != FEMALE) return 0;
    return row<ROW_APPLY?counts[row]:0;
}
static void SetRowValue(u8 row,u8 value)
{
    switch(row) {
    case ROW_OUTFIT:LegendsSetCostumeSelection(0);LegendsSetAppearanceSelection(LegendsGetSkinTone(),value);break;
    case ROW_COSTUMES:LegendsSetCostumeSelection(value);break;
    case ROW_HAIR:LegendsSetHairSelection(value);break;
    case ROW_HAIR_COLOR:LegendsSetHairColorSelection(value);break;
    case ROW_SCARF:LegendsSetAccessorySelection(value,LegendsGetJacketStyle());break;
    case ROW_JACKET:LegendsSetAccessorySelection(LegendsGetScarf(),value);break;
    case ROW_LEGGINGS:LegendsSetLeggingsSelection(value);break;
    case ROW_SHOES:LegendsSetShoeSelection(value);break;
    case ROW_CARD:LegendsSetCardColorSelection(value);break;
    }
}
static const u8 *RowText(u8 row)
{
    if (row>=ROW_HAIR && row<=ROW_SHOES && LegendsGetCostume())return COMPOUND_STRING("FIXED");
    switch(row) {
    case ROW_OUTFIT:return sOutfits[LegendsGetOutfit()];
    case ROW_COSTUMES:return sCostumes[LegendsGetCostume()];
    case ROW_HAIR:return LegendsGetHairName(gSaveBlock2Ptr->playerGender,LegendsGetHair());
    case ROW_HAIR_COLOR:return LegendsGetHairColorName(LegendsGetHairColor());
    case ROW_SCARF:return sScarves[LegendsGetScarf()];
    case ROW_JACKET:return sCoats[LegendsGetJacketStyle()];
    case ROW_LEGGINGS:return sLeggings[LegendsGetLeggings()];
    case ROW_SHOES:return sShoes[LegendsGetShoes()];
    default:return NULL;
    }
}
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
    u8 i, row=WardrobeDisplayRow(gTasks[taskId].data[0]), top=gTasks[taskId].data[1];
    u16 swatch = LegendsCardSwatch();
    FillWindowPixelBuffer(1,PIXEL_FILL(1));
    FillWindowPixelBuffer(0,PIXEL_FILL(1));
    if (gTasks[taskId].data[2])
    {
        u8 value=RowValue(row);
        top=gTasks[taskId].data[3];
        Print(0,row==ROW_HAIR?COMPOUND_STRING("HAIRSTYLE                    A: SELECT"):COMPOUND_STRING("HAIR COLOR                   A: SELECT"),0,0);
        Print(0,COMPOUND_STRING("UP/DOWN: SCROLL  B: BACK"),0,12);
        for (i=0;i<WARDROBE_VISIBLE;i++)
            Print(1,row==ROW_HAIR?LegendsGetHairName(gSaveBlock2Ptr->playerGender,top+i):LegendsGetHairColorName(top+i),12,i*14);
        Print(1,COMPOUND_STRING(">"),0,(value-top)*14);
        if (top) Print(1,COMPOUND_STRING("{UP_ARROW}"),120,0);
        if (top+WARDROBE_VISIBLE<RowCount(row)) Print(1,COMPOUND_STRING("{DOWN_ARROW}"),120,70);
    }
    else
    {
        Print(0,COMPOUND_STRING("WARDROBE                     B: CANCEL"),0,0);
        Print(0,(row==ROW_HAIR||row==ROW_HAIR_COLOR)
            ? (LegendsGetCostume()?COMPOUND_STRING("HAIR FIXED BY COSTUME"):COMPOUND_STRING("A: OPEN LIST  LEFT/RIGHT: OPEN"))
            :COMPOUND_STRING("UP/DOWN: ROW  A/LEFT/RIGHT: CHANGE"),0,12);
        for (i=0;i<WARDROBE_VISIBLE && top+i<WardrobeDisplayCount();i++)
        {
            u8 item=WardrobeDisplayRow(top+i);
            const u8 *value=RowText(item);
            Print(1,sRows[item],12,i*14);
            if(value)Print(1,value,62,i*14);
        }
        Print(1,COMPOUND_STRING(">"),0,(gTasks[taskId].data[0]-top)*14);
        if(top)Print(1,COMPOUND_STRING("{UP_ARROW}"),120,0);
        if(top+WARDROBE_VISIBLE<WardrobeDisplayCount())Print(1,COMPOUND_STRING("{DOWN_ARROW}"),120,70);
    }
    CopyWindowToVram(0,COPYWIN_FULL);
    CopyWindowToVram(1,COPYWIN_FULL);
    // Native Trainer Card drawing owns and frees its temporary graphics buffer.
    FillWindowPixelBuffer(2,PIXEL_FILL(0));
    CreateTrainerCardTrainerPicSprite(LegendsGetPlayerTrainerPic(gSaveBlock2Ptr->playerGender),TRUE,0,0,8,2);
    CopyWindowToVram(2,COPYWIN_FULL);
    // A miniature card swatch updates without hiding the outfit portrait.
    LoadPalette(&swatch,BG_PLTT_ID(9)+10,sizeof(swatch));
    FillWindowPixelBuffer(3,PIXEL_FILL(1));
    FillWindowPixelRect(3,PIXEL_FILL(10),0,0,64,3);
    Print(3,sCardColors[LegendsGetCardColor()],2,4);
    CopyWindowToVram(3,COPYWIN_FULL);
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
    u8 row=WardrobeDisplayRow(gTasks[taskId].data[0]);
    if (gPaletteFade.active) return;
    if (gTasks[taskId].data[2])
    {
        u8 value=RowValue(row), count=RowCount(row);
        if (JOY_NEW(A_BUTTON|B_BUTTON))
        {
            if (JOY_NEW(B_BUTTON)) SetRowValue(row,gTasks[taskId].data[4]);
            gTasks[taskId].data[2]=0;
        }
        else
        {
            if (JOY_REPEAT(DPAD_UP) && value>0)value--;
            else if (JOY_REPEAT(DPAD_DOWN) && value+1<count)value++;
            else return;
            SetRowValue(row,value);
            if(value<gTasks[taskId].data[3])gTasks[taskId].data[3]=value;
            if(value>=gTasks[taskId].data[3]+WARDROBE_VISIBLE)gTasks[taskId].data[3]=value-WARDROBE_VISIBLE+1;
        }
        Draw(taskId);
        return;
    }
    if ((row==ROW_HAIR||row==ROW_HAIR_COLOR) && JOY_NEW(A_BUTTON|DPAD_LEFT|DPAD_RIGHT) && !LegendsGetCostume())
    {
        u8 value=RowValue(row);
        gTasks[taskId].data[2]=1;
        gTasks[taskId].data[3]=value>=WARDROBE_VISIBLE?value-WARDROBE_VISIBLE+1:0;
        gTasks[taskId].data[4]=value;
        Draw(taskId);
        return;
    }
    if (JOY_NEW(B_BUTTON) || (JOY_NEW(A_BUTTON) && row>=ROW_APPLY))
    {
        if (JOY_NEW(A_BUTTON) && row==ROW_APPLY)LegendsApplyWardrobeSelection();
        else LegendsClearAppearanceSelection();
        BeginNormalPaletteFade(PALETTES_ALL,0,0,16,RGB_BLACK);
        gTasks[taskId].func=Task_Return;
        return;
    }
    if (JOY_REPEAT(DPAD_UP))gTasks[taskId].data[0]=(gTasks[taskId].data[0]+WardrobeDisplayCount()-1)%WardrobeDisplayCount();
    else if (JOY_REPEAT(DPAD_DOWN))gTasks[taskId].data[0]=(gTasks[taskId].data[0]+1)%WardrobeDisplayCount();
    else if (row<ROW_APPLY && JOY_NEW(DPAD_LEFT|DPAD_RIGHT|A_BUTTON))
    {
        if (row==ROW_COSTUMES||row==ROW_OUTFIT||row==ROW_CARD||!LegendsGetCostume())
            SetRowValue(row,(RowValue(row)+(JOY_NEW(DPAD_LEFT)?RowCount(row)-1:1))%RowCount(row));
    }
    else return;
    row=gTasks[taskId].data[0];
    if(row<gTasks[taskId].data[1])gTasks[taskId].data[1]=row;
    if(row>=gTasks[taskId].data[1]+WARDROBE_VISIBLE)gTasks[taskId].data[1]=row-WARDROBE_VISIBLE+1;
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
    LoadPalette(gStandardMenuPalette,BG_PLTT_ID(9),PLTT_SIZE_4BPP);
    LoadUserWindowBorderGfx(0,STD_WINDOW_BASE_TILE_NUM,BG_PLTT_ID(STD_WINDOW_PALETTE_NUM));
    SetGpuReg(REG_OFFSET_BLDCNT,0);SetGpuReg(REG_OFFSET_BLDY,0);
    for (i=0;i<4;i++) {FillWindowPixelBuffer(i,PIXEL_FILL(1));PutWindowTilemap(i);DrawStdWindowFrame(i,FALSE);}
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
