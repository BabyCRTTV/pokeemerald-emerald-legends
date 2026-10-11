"""Check native frame hardware limits and actual Options selection/loading."""
from pathlib import Path
import re
import subprocess
import tempfile
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
header = (ROOT / 'include/text_window.h').read_text()
count = int(re.search(r'WINDOW_FRAMES_COUNT (\d+)', header).group(1))
assert count == 25 and count <= 32  # Existing five-bit save field.
source = (ROOT / 'src/text_window.c').read_text()
table = source.split('sWindowFrames[WINDOW_FRAMES_COUNT] =')[1].split('};')[0]
assert len(re.findall(r'Frame\d+_Gfx,', table)) == count
base = Image.open(ROOT / 'graphics/text_window/1.png').getpalette()
for index in range(21, 26):
    with Image.open(ROOT / f'graphics/text_window/{index}.png') as image:
        assert image.mode == 'P' and image.size == (24, 24)
        assert max(image.tobytes()) < 16
        assert set(image.crop((8,8,16,16)).tobytes()) == {14}
        for color in (0,1,14,15):
            assert image.getpalette()[color*3:color*3+3] == base[color*3:color*3+3]
        assert f'graphics/text_window/{index}.png", ".4bpp"' in source
        assert f'graphics/text_window/{index}.png", ".gbapal"' in source
assert len({(ROOT / f'graphics/text_window/{index}.png').read_bytes() for index in range(21,26)}) == 5
options = (ROOT / 'src/option_menu.c').read_text()
start = options.index('static u8 FrameType_ProcessInput(u8 selection)\n{')
function = options[start:options.index('\n}', start)+2]
fixture = r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
typedef uint8_t u8;
#define WINDOW_FRAMES_COUNT 25
#define DPAD_RIGHT 1
#define DPAD_LEFT 2
#define JOY_NEW(keys) (pressed & (keys))
#define BG_PLTT_ID(n) ((n) * 16)
#define PLTT_SIZE_4BPP 32
#define TRUE 1
static u8 pressed, sArrowPressed;
static unsigned loaded, tilesLoaded, palsLoaded;
struct TilesPal { const u8 *tiles; const uint16_t *pal; };
static const u8 tileData[288] = {0};
static const uint16_t palData[16] = {0};
static const struct TilesPal frame = {tileData, palData};
static const struct TilesPal *GetWindowFrameTilesPal(u8 id)
{ assert(id < 25); loaded = id; return &frame; }
static void LoadBgTiles(unsigned bg,const u8 *data,unsigned bytes,unsigned start)
{ assert(bg == 1 && data == tileData && bytes == 288 && start == 0x1A2); tilesLoaded++; }
static void LoadPalette(const uint16_t *data,unsigned start,unsigned bytes)
{ assert(data == palData && start == 112 && bytes == 32); palsLoaded++; }
'''
tests = r'''
int main(void)
{
    u8 selection = 0;
    for (unsigned i=1;i<=25;i++)
    {
        pressed=DPAD_RIGHT; selection=FrameType_ProcessInput(selection);
        assert(selection == i % 25 && loaded == selection && sArrowPressed);
    }
    for (unsigned i=1;i<=25;i++)
    {
        pressed=DPAD_LEFT; selection=FrameType_ProcessInput(selection);
        assert(selection == (25-i) % 25 && loaded == selection);
    }
    assert(tilesLoaded == 50 && palsLoaded == 50);
    puts("25 native frame choices, wrap, palettes and tile bounds passed.");
}
'''
with tempfile.TemporaryDirectory() as directory:
    path=Path(directory)
    (path/'test.c').write_text(fixture+function+tests)
    subprocess.run(['cc','-std=c99','-Wall','-Wextra','-Werror',str(path/'test.c'),'-o',str(path/'check')],check=True)
    subprocess.run([str(path/'check')],check=True)
