"""Run the actual Options input and paging functions against task/UI stubs."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
source = (root / 'src/option_menu.c').read_text()

def function(signature):
    start = source.index(signature + '\n{')
    end = source.index('\n}', start) + 2
    return source[start:end]

macros = source[source.index('#define tMenuSelection'):source.index('enum\n{')]
enums = source[source.index('enum\n{'):source.index('static void Task_OptionMenuFadeIn')]
tables = source[source.index('static const u8 sOptionMenuPageItems'):source.index('static const struct WindowTemplate')]
input_fn = function('static void Task_OptionMenuProcessInput(u8 taskId)')
item_fn = function('static u8 GetOptionMenuItem(u8 taskId)')
page_fn = function('static void ChangeOptionMenuPage(u8 taskId, s8 direction)')
stub = r'''
#include <stdint.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;
typedef int8_t s8;
typedef int16_t s16;
#define FALSE 0
#define TRUE 1
#define L_BUTTON 1
#define R_BUTTON 2
#define A_BUTTON 4
#define B_BUTTON 8
#define DPAD_UP 16
#define DPAD_DOWN 32
#define LEGENDS_SEASONS_PLAYTIME 1
#define COPYWIN_GFX 0
#define JOY_NEW(keys) (pressed & (keys))
static unsigned pressed;
static u8 sArrowPressed;
static unsigned headers, pages, highlights;
struct Task { s16 data[16]; void (*func)(u8); };
static struct Task gTasks[1];
static void Task_OptionMenuSave(u8 id) { (void)id; }
static void DrawHeaderText(u8 page) { (void)page; headers++; }
static void DrawOptionMenuPage(u8 id) { (void)id; pages++; }
static void HighlightOptionMenuItem(u8 row) { (void)row; highlights++; }
static void CopyWindowToVram(u8 w, u8 mode) { (void)w; (void)mode; }
static u8 GetOptionMenuItem(u8 taskId);
static void ChangeOptionMenuPage(u8 taskId, s8 direction);
'''
for name in ['TextSpeed','BattleScene','BattleStyle','OnOff','ShinyRate','SeasonMode','SetSeason','Sound','ButtonMode','FrameType']:
    stub += f'static u8 {name}_ProcessInput(u8 value) {{ return value; }}\n'
for name in ['TextSpeed','BattleScene','BattleStyle','OnOff','ShinyRate','SeasonMode','Sound','ButtonMode','FrameType']:
    stub += f'static void {name}_DrawChoices(u8 value, u8 y) {{ (void)value; (void)y; }}\n'
stub += 'static void SetSeason_DrawChoice(u8 mode, u8 season, u8 y) { (void)mode; (void)season; (void)y; }\n'
tests = r'''
int main(void)
{
    for (unsigned i = 1; i < 14; i++) gTasks[0].data[i] = i;
    gTasks[0].tMenuPage = OPTION_PAGE_GENERAL;
    gTasks[0].tMenuSelection = 6;
    pressed = A_BUTTON;
    Task_OptionMenuProcessInput(0);
    assert(gTasks[0].tMenuPage == OPTION_PAGE_LEGENDS);
    assert(gTasks[0].tMenuSelection == 0 && gTasks[0].func == NULL);
    assert(headers == 1 && pages == 1 && highlights == 1);
    for (unsigned i = 1; i < 14; i++) if (i != 8) assert(gTasks[0].data[i] == (s16)i);
    gTasks[0].tMenuSelection = 6;
    Task_OptionMenuProcessInput(0);
    assert(gTasks[0].tMenuPage == OPTION_PAGE_GENERAL && gTasks[0].tMenuSelection == 0);
    Task_OptionMenuProcessInput(0); // A on a setting does not switch or exit.
    assert(gTasks[0].tMenuPage == OPTION_PAGE_GENERAL && gTasks[0].func == NULL);
    pressed = L_BUTTON | A_BUTTON; // L=A mapping must still navigate.
    Task_OptionMenuProcessInput(0);
    assert(gTasks[0].tMenuPage == OPTION_PAGE_LEGENDS && gTasks[0].func == NULL);
    pressed = R_BUTTON;
    Task_OptionMenuProcessInput(0);
    assert(gTasks[0].tMenuPage == OPTION_PAGE_GENERAL);
    pressed = DPAD_UP;
    Task_OptionMenuProcessInput(0);
    assert(GetOptionMenuItem(0) == MENUITEM_NEXTPAGE);
    pressed = DPAD_DOWN;
    Task_OptionMenuProcessInput(0);
    assert(gTasks[0].tMenuSelection == 0);
    for (unsigned page = 0; page < OPTION_PAGE_COUNT; page++)
    {
        gTasks[0].tMenuPage = page;
        for (unsigned row = 0; row < sOptionMenuPageItemCounts[page]; row++)
        {
            gTasks[0].func = NULL;
            gTasks[0].tMenuSelection = row;
            pressed = B_BUTTON;
            Task_OptionMenuProcessInput(0);
            assert(gTasks[0].func == Task_OptionMenuSave);
        }
    }
    puts("Options A/L/R paging, pending settings, row wrap and B save/exit passed.");
}
'''
with tempfile.TemporaryDirectory() as directory:
    tmp = Path(directory)
    (tmp / 'test.c').write_text(stub + macros + enums + tables + item_fn + page_fn + input_fn + tests)
    subprocess.run(['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', str(tmp / 'test.c'), '-o', str(tmp / 'check')], check=True)
    subprocess.run([str(tmp / 'check')], check=True)
