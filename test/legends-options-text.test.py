"""Exercise the actual Options choice renderer with plain and encoded text."""
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
source = (root / 'src/option_menu.c').read_text()
start = source.index('static void DrawOptionMenuChoice(')
end = source.index('\nstatic u8 TextSpeed_ProcessInput', start)
function = source[start:end]
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
    puts("Options plain text and encoded color-prefix regressions passed.");
}
'''
with tempfile.TemporaryDirectory() as directory:
    tmp = Path(directory)
    (tmp / 'test.c').write_text(stub + function + tests)
    subprocess.run(['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', str(tmp / 'test.c'), '-o', str(tmp / 'check')], check=True)
    subprocess.run([str(tmp / 'check')], check=True)
