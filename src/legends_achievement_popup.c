#include "global.h"
#include "legends_journal.h"
#include "main.h"
#include "overworld.h"
#include "link.h"
#include "script.h"
#include "palette.h"
#include "menu.h"
#include "window.h"
#include "text.h"
#include "map_name_popup.h"

// Field BG0 starts at VRAM 0x8000. Tiles 0x70-0xB7 fit between native
// counter windows and the day panel, below all map screen blocks (0xE000+).
// No shared BG scroll, palette change, script lock or input consumption.
static const struct WindowTemplate sNoticeWindow =
{
    .bg = 0, .tilemapLeft = 1, .tilemapTop = 1, .width = 18, .height = 4,
    .paletteNum = 15, .baseBlock = 0x70,
};
static const u8 sLabelInk[] = {2, 1, 3};
static const u8 sTitleInk[] = {1, 2, 3};
EWRAM_DATA static u8 sNoticeWindowId = 0;
EWRAM_DATA static u16 sNoticeFrames = 0, sNoticeId = 0;

void LegendsAchievementPopupHide(void)
{
    if (sNoticeWindowId != 0)
    {
        ClearWindowTilemap(sNoticeWindowId - 1);
        CopyWindowToVram(sNoticeWindowId - 1, COPYWIN_MAP);
        RemoveWindow(sNoticeWindowId - 1);
        sNoticeWindowId = 0;
    }
    sNoticeFrames = 0;
}

void LegendsAchievementPopupUpdate(void)
{
    u16 id;
    u8 windowId;
    if (gMain.callback2 != CB2_Overworld || gPaletteFade.active
        || ArePlayerFieldControlsLocked() || ScriptContext_IsEnabled()
        || IsOverworldLinkActive() || InUnionRoom() || IsMapNamePopupActive())
    {
        // Keep the notice queued when a menu, battle, warp or script intervenes.
        LegendsAchievementPopupHide();
        return;
    }
    if (sNoticeFrames)
    {
        if (--sNoticeFrames == 0 && sNoticeWindowId != 0)
        {
            LegendsAchievementNoticeDismiss(sNoticeId);
            LegendsAchievementPopupHide();
            sNoticeFrames = 20; // Short gap between simultaneous unlocks.
        }
        return;
    }
    id = LegendsAchievementNotice();
    if (id == 0xFFFF) return;
    windowId = AddWindow(&sNoticeWindow);
    if (windowId == WINDOW_NONE) return; // Retry without losing the notice.
    sNoticeWindowId = windowId + 1; // Zero is the native EWRAM initializer.
    sNoticeId = id;
    FillWindowPixelBuffer(windowId, PIXEL_FILL(1));
    FillWindowPixelRect(windowId, PIXEL_FILL(2), 0, 0, 144, 15);
    AddTextPrinterParameterized3(windowId, FONT_SMALL, 5, 0, sLabelInk, TEXT_SKIP_DRAW,
        COMPOUND_STRING("ACHIEVEMENT UNLOCKED"));
    AddTextPrinterParameterized3(windowId, FONT_SMALL, 5, 16, sTitleInk, TEXT_SKIP_DRAW,
        LegendsAchievementGet(id)->title);
    FillWindowPixelRect(windowId, PIXEL_FILL(2), 0, 15, 1, 17);
    FillWindowPixelRect(windowId, PIXEL_FILL(2), 143, 15, 1, 17);
    FillWindowPixelRect(windowId, PIXEL_FILL(2), 0, 31, 144, 1);
    PutWindowTilemap(windowId);
    CopyWindowToVram(windowId, COPYWIN_FULL);
    sNoticeFrames = 180;
}
