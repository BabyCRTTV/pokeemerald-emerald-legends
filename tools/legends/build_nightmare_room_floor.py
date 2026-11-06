"""Match only the bed-side floor to the existing Nightmare room floor."""
from pathlib import Path
import argparse, hashlib, json, struct
from io import BytesIO
from PIL import Image

R = Path(__file__).resolve().parents[2]
P = R / 'data/tilesets/legends_nightmare/room'
PINS = {
    'data/tilesets/secondary/generic_building/tiles.png': '7783d199aaaaa51db286c745ddc6907a576f2930767a2f52862128c39cf15be8',
    'data/tilesets/secondary/generic_building/metatiles.bin': 'c3401446239749a25f6abc1daab0c19cd43eb6333a7ec5335bb7e1580d002b1d',
    'data/tilesets/secondary/generic_building/metatile_attributes.bin': 'eb3e942c013770224ffc7d99c469cdaf9cd31243f71ce3fb05a70b278dc5a509',
}

def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)

def apply():
    for path, digest in PINS.items():
        assert hashlib.sha256((R / path).read_bytes()).hexdigest() == digest, path
    native = R / 'data/tilesets/secondary/generic_building'
    image = Image.open(native / 'tiles.png')
    original = image.copy()
    metas = bytearray((native / 'metatiles.bin').read_bytes())
    used = set()
    for room in ['Home', 'Bedroom']:
        folder = R / f'data/layouts/LegendsNightmare_{room}'
        for name in ['map.bin', 'border.bin']:
            raw = (folder / name).read_bytes()
            used.update(word & 1023 for word in struct.unpack(f'<{len(raw)//2}H', raw))
    occupied = {word & 1023 for m in used if m >= 512
                for word in struct.unpack_from('<8H', metas, (m-512)*16)}
    free = iter(t for t in range(512, 1024) if t not in occupied)
    # These two frame tiles contain dark wall-shadow floor. Replace just their
    # floor pixels with existing 0x223 floor and retain every frame pixel.
    replacements = {}
    for tile, is_floor in [(0x3c2, lambda x: x < 5), (0x3c5, lambda x: x >= 3)]:
        dest = next(free)
        replacements[tile] = dest
        for y in range(8):
            for x in range(8):
                source = 0x230 if is_floor(x) else tile
                n = source - 512
                value = original.getpixel((n % 16 * 8 + x, n // 16 * 8 + y))
                n = dest - 512
                image.putpixel((n % 16 * 8 + x, n // 16 * 8 + y), value)
    for metatile in [0x2d2, 0x2d4]:
        for quadrant in range(4):
            offset = (metatile-512)*16 + quadrant*2
            word = struct.unpack_from('<H', metas, offset)[0]
            tile = word & 1023
            if tile in replacements:
                word = (word & ~1023) | replacements[tile]
            else:
                assert tile == 0x240
                word = (word & ~1023) | (0x230 + quadrant % 2)
            struct.pack_into('<H', metas, offset, word)
    encoded = BytesIO()
    image.save(encoded, format='PNG')
    write(P / 'tiles.png', encoded.getvalue())
    write(P / 'metatiles.bin', bytes(metas))
    write(P / 'metatile_attributes.bin', (native / 'metatile_attributes.bin').read_bytes())
    header = ['// Only the two bed-side floor backgrounds differ from native GenericBuilding.',
        'const u32 gNightmareRoomTiles[] = INCGFX_U32("data/tilesets/legends_nightmare/room/tiles.png", ".4bpp.fastSmol");',
        'const u16 gNightmareRoomMetatiles[] = INCBIN_U16("data/tilesets/legends_nightmare/room/metatiles.bin");',
        'const u16 gNightmareRoomAttributes[] = INCBIN_U16("data/tilesets/legends_nightmare/room/metatile_attributes.bin");',
        'const struct Tileset gTileset_NightmareHomeInterior = {',
        '    .isCompressed = TRUE, .isSecondary = TRUE, .tiles = gNightmareRoomTiles, .palettes = gTilesetPalettes_GenericBuilding,',
        '    .metatiles = gNightmareRoomMetatiles, .metatileAttributes = gNightmareRoomAttributes, .callback = NULL,', '};']
    write(R / 'src/data/tilesets/legends_nightmare_room.h', ('\n'.join(header)+'\n').encode())
    metadata = dict(nativeInputs=PINS, changedMetatiles=[0x2d2, 0x2d4],
        allocatedTiles=list(replacements.values()),
        scope='Only the two bed-side floor backgrounds match existing GenericBuilding 0x223. Original room floor, palettes, furniture, wall, maps, scripts and collisions retained.')
    write(P / 'source.json', (json.dumps(metadata, indent=2)+'\n').encode())
    print('Matched two bed-side floor backgrounds; original room floor and palettes retained.')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    if not parser.parse_args().apply:
        raise SystemExit('Explicit authoring only: --apply required')
    apply()
