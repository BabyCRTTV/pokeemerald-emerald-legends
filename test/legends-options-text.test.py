"""Exercise the actual Options choice renderer with plain and encoded text."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
source = (root / 'src/option_menu.c').read_text()
start = source.index('static void DrawOptionMenuChoice(')
end = source.index('\n}', start) + 2
function = source[start:end]
start = source.index('static void TextSpeed_DrawChoices(u8 selection, u8 y)\n{')
end = source.index('\n}', start) + 2
speed_function = source[start:end]
stub = r'''
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8;
typedef uint16_t u16;
#define EOS 255
#define ARRAY_COUNT(a) (sizeof(a) / sizeof((a)[0]))
#define EXT_CTRL_CODE_BEGIN 252
#define EXT_CTRL_CODE_COLOR 1
#define EXT_CTRL_CODE_SHADOW 3
#define TEXT_COLOR_RED 4
#define TEXT_COLOR_LIGHT_RED 5
#define WIN_OPTIONS 1
#define FONT_NORMAL 1
#define TEXT_SKIP_DRAW 255
u8 captured[32];
void AddTextPrinterParameterized(u8 w, u8 f, const u8 *text, u8 x, u8 y, u8 speed, void *cb)
{
    (void)w; (void)f; (void)x; (void)y; (void)speed; (void)cb;
    unsigned i = 0;
    do {captured[i] = text[i];} while (text[i++] != EOS);
}
'''
stub += r'''
#define OPTIONS_TEXT_SPEED_SLOW 0
#define OPTIONS_TEXT_SPEED_MID 1
#define OPTIONS_TEXT_SPEED_FAST 2
#define OPTIONS_TEXT_SPEED_INSTANT 3
#define OPTION_ROW_HEIGHT 16
#define PIXEL_FILL(x) (x)
static unsigned clears;
static const u8 gText_TextSpeedSlow[] = {252,1,6,252,3,7,'S','L','O','W',EOS};
static const u8 gText_TextSpeedMid[] = {252,1,6,252,3,7,'M','I','D',EOS};
static const u8 gText_TextSpeedFast[] = {252,1,6,252,3,7,'F','A','S','T',EOS};
static const u8 gText_TextSpeedInstant[] = {252,1,6,252,3,7,'I','N','S','T','A','N','T',EOS};
static void FillWindowPixelRect(u8 w,u8 fill,u8 x,u8 y,u8 width,u8 height)
{
    assert(w == WIN_OPTIONS && fill == 1 && x == 104 && y == 0);
    assert(width == 96 && height == OPTION_ROW_HEIGHT);
    clears++;
}
'''
tests = r'''
int main(void)
{
    const u8 plain[] = {'R','E','A','L',' ','T','I','M','E',EOS};
    DrawOptionMenuChoice(plain, 120, 0, 1);
    assert(memcmp(captured, plain, sizeof(plain)) == 0);
    const u8 autumn[] = {'A','U','T','U','M','N',EOS};
    DrawOptionMenuChoice(autumn, 130, 16, 1);
    assert(memcmp(captured, autumn, sizeof(autumn)) == 0);
    const u8 encoded[] = {252,1,6,252,3,7,'R','E','A','L',' ','T','I','M','E',EOS};
    DrawOptionMenuChoice(encoded, 120, 0, 1);
    assert(captured[2] == TEXT_COLOR_RED && captured[5] == TEXT_COLOR_LIGHT_RED);
    assert(memcmp(captured + 6, encoded + 6, sizeof(encoded) - 6) == 0);
    DrawOptionMenuChoice(encoded, 120, 0, 0);
    assert(memcmp(captured, encoded, sizeof(encoded)) == 0);
    const u8 shortText[] = {'O','N',EOS};
    DrawOptionMenuChoice(shortText, 120, 0, 1);
    assert(memcmp(captured, shortText, sizeof(shortText)) == 0);
    const char *labels[] = {"SLOW", "MID", "FAST", "INSTANT"};
    for (u8 speed = 0; speed < 4; speed++)
    {
        TextSpeed_DrawChoices(speed, 0);
        assert(memcmp(captured + 6, labels[speed], strlen(labels[speed])) == 0);
        assert(captured[6 + strlen(labels[speed])] == EOS);
        assert(captured[2] == TEXT_COLOR_RED && captured[5] == TEXT_COLOR_LIGHT_RED);
    }
    TextSpeed_DrawChoices(0, 0); // INSTANT -> SLOW clears trailing letters.
    TextSpeed_DrawChoices(7, 0); // Invalid saved values safely display FAST.
    assert(memcmp(captured + 6, "FAST", 4) == 0);
    assert(clears == 6);
    puts("Options plain text and encoded color-prefix regressions passed.");
}
'''
with tempfile.TemporaryDirectory() as directory:
    tmp = Path(directory)
    (tmp / 'test.c').write_text(stub + function + speed_function + tests)
    subprocess.run(['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', str(tmp / 'test.c'), '-o', str(tmp / 'check')], check=True)
    subprocess.run([str(tmp / 'check')], check=True)
