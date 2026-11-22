"""Rebuild the occupied entrance poses from the approved indexed field art."""
from pathlib import Path
from struct import iter_unpack, unpack_from
from math import floor

from PIL import Image

ROOT = Path(__file__).resolve().parents[2] / 'data/tilesets'
OUT = ROOT / 'legends_grotto'
GENERAL = 'legends_lights/general'


def read_face(atlas, metatile, layer):
    words = unpack_from('<8H', (ROOT / (atlas + '_metatiles.bin')).read_bytes(), metatile * 16)
    sheet = Image.open(ROOT / (atlas + '_tiles.png'))
    image = Image.new('L', (16, 16))
    for i, word in enumerate(words[layer:layer + 4]):
        index = (word & 1023) - (0 if atlas == GENERAL else 512)
        x, y = index % 16 * 8, index // 16 * 8
        tile = sheet.crop((x, y, x + 8, y + 8))
        if word & 1024:
            tile = tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if word & 2048:
            tile = tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        image.paste(Image.frombytes('L', (8, 8), tile.tobytes()), ((i % 2) * 8, (i // 2) * 8))
    return image


def ease(v):
    v = max(0, min(v, 1))
    return v * v * (3 - 2 * v)


def hill(x, center, radius):
    return ease(1 - abs(x - center) / radius)


def leafshade(x, y, a):
    # The long vine has a loose tip. The shorter vine moves less.
    right = a * ease((y + 2) / 16)
    left = -0.48 * a * ease((y + 1) / 12)
    dx = right * hill(x, 22.5 + 0.7 * right, 7.8) + left * hill(x, 8.5 + 0.65 * left, 6.3)
    lift = 0.9 * abs(right / 3.7) * hill(x, 22.5 + 0.7 * right, 5)
    return x - dx, y + lift


def rainroot(x, y, a):
    # The central fronds part while the outer bushes and roots stay planted.
    b = 0.80 * a
    left = hill(x, 4 - 0.45 * a, 10.5) * hill(y, 3.8 - 0.48 * a, 10.2)
    right = hill(x, 12 + 0.38 * b, 9.4) * hill(y, 3.8 - 0.48 * b, 10.4)
    return x + 0.92 * a * left - 0.9 * b * right, y + 0.93 * a * left + 0.8 * b * right


def render(native, transform, amplitude):
    result = native.copy()
    for y in range(native.height):
        for x in range(native.width):
            sx, sy = transform(x, y, amplitude)
            sx = max(0, min(native.width - 1, floor(sx + 0.5)))
            sy = max(0, min(native.height - 1, floor(sy + 0.5)))
            result.putpixel((x, y), native.getpixel((sx, sy)))
    return result


def crossbar(native, height):
    # Keep the iron nail at the left fixed. Zero is transparent on this layer.
    result = Image.new('L', native.size)
    for x in range(16):
        shift = max(0, floor((x - 2) * height / 12 + 0.5))
        for y in range(6, 10):
            result.putpixel((x, y - shift), native.getpixel((x, y)))
    return result


def pack(image):
    packed = bytearray()
    for cell in range(0, image.width, 16):
        for top in (0, 8):
            for left in (cell, cell + 8):
                for y in range(top, top + 8):
                    for x in range(left, left + 8, 2):
                        packed.append(image.getpixel((x, y)) | image.getpixel((x + 1, y)) << 4)
    return bytes(packed)


def main():
    woods = Image.new('L', (32, 16))
    for i in range(2):
        woods.paste(read_face(GENERAL, 0x36 + i, 0), (i * 16, 0))
    plank = read_face('legends_grotto/fallarbor_cliff', 0x179, 4)
    fern = read_face('legends_lights/fortree', 0x78, 4)
    rooms = [
        ('leafshade', 'legends_lights/rustboro', 632, [render(woods, leafshade, a) for a in [-1.5, -3.7, 2.7, 1]]),
        ('stillwater', 'legends_grotto/fallarbor_cliff', 632, [crossbar(plank, a) for a in [1, 2, 3]]),
        ('rainroot', 'legends_lights/fortree', 644, [render(fern, rainroot, a) for a in [1, 2, 3.7]]),
    ]
    for name, atlas, first, frames in rooms:
        # Reserve only blank, unreferenced secondary tiles, below the native door slots.
        slots = set(range(first, first + frames[0].width // 4))
        sheet = Image.open(ROOT / (atlas + '_tiles.png'))
        for slot in slots:
            x, y = (slot - 512) % 16 * 8, (slot - 512) // 16 * 8
            assert sheet.crop((x, y, x + 8, y + 8)).getextrema() == (0, 0)
        for source in (atlas, GENERAL):
            words = iter_unpack('<H', (ROOT / (source + '_metatiles.bin')).read_bytes())
            assert not any((w & 1023) in slots for w, in words)
        (OUT / (name + '_motion.bin')).write_bytes(b''.join(map(pack, frames)))


if __name__ == '__main__':
    main()
