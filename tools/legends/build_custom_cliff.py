"""Fit Stillwater's natural cave mouth into the two native Route 114 cliff columns."""
from pathlib import Path
import hashlib
import json
import re
import struct

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'data/tilesets/legends_grotto'
FIRST = 0x375
# Right-hand IDs are referenced by existing maps. Left-hand IDs follow them.
BLOCKS = [(16, 0, 0x22A), (16, 16, 0x22A), (0, 0, 0x241), (0, 16, 0x241)]
DEEP = 16


def carve(rock):
    """Cut back the cliff under two offset shelves; the east sill meets the grass."""
    d = ImageDraw.Draw(rock)
    # The high point is back in the hill. The ledge on the right hangs lower.
    d.polygon([(3,16),(6,11),(10,9),(13,6),(19,5),(23,6),(26,8),(28,9),
               (29,13),(28,18),(29,21),(31,22),(31,27),(23,27),(18,26),
               (12,26),(8,24),(5,23),(3,20)], fill=14)
    d.polygon([(4,17),(8,13),(11,12),(13,9),(18,8),(22,9),(23,12),
               (27,12),(27,16),(26,19),(28,21),(31,22),(31,25),
               (22,25),(17,24),(10,24),(6,22),(4,20)], fill=8)
    d.polygon([(5,17),(8,14),(12,13),(14,10),(18,9),(21,10),(22,13),
               (24,14),(23,17),(21,18),(21,20),(15,20),(12,21),
               (8,21),(6,20)], fill=DEEP)
    # Native light direction; isolated fractures cross the lip instead of
    # tracing its outline. The broken lower slab partly hides the far wall.
    d.polygon([(3,14),(6,10),(10,8),(12,5),(16,4),(21,4),(23,5),
               (22,7),(18,6),(14,7),(11,10),(7,11)], fill=11)
    d.line([(4,13),(7,10),(10,9)],fill=2)
    d.line([(12,6),(15,4),(19,4)],fill=2)
    d.polygon([(19,6),(23,6),(26,8),(28,9),(28,12),(25,11),(23,11),(22,9)],fill=13)
    d.line([(23,6),(25,7),(26,8)],fill=11)
    d.line([(4,17),(5,14),(7,13)],fill=13)
    d.line([(25,14),(25,17),(24,19)],fill=7)
    # Uneven, gently sloping bedrock leads out toward the eastern clearing.
    d.polygon([(6,21),(12,22),(16,21),(20,21),(23,19),(27,20),(31,20),
               (31,26),(26,26),(23,27),(18,26),(15,25),(10,25),(7,23)],fill=13)
    d.polygon([(9,22),(13,23),(17,22),(20,22),(24,20),(27,21),(31,20),
               (31,22),(26,23),(22,23),(18,24),(14,24)],fill=7)
    d.line([(15,23),(18,22),(20,22)],fill=6)
    d.line([(23,22),(26,21),(29,21)],fill=5)
    d.polygon([(17,25),(22,24),(26,24),(28,23),(31,23),(31,25),
               (26,25),(23,26),(19,26)],fill=12)
    d.line([(24,24),(27,23),(29,23)],fill=11)
    d.line([(7,22),(9,23),(12,23)],fill=14)
    # A chipped roof slab projects over the far wall. A low rock at the
    # nearer corner breaks up the threshold and leaves the east path clear.
    d.polygon([(19,7),(23,7),(26,9),(26,11),(24,11),(22,10),(20,10)],fill=14)
    d.polygon([(19,6),(22,6),(25,8),(24,9),(21,8)],fill=11)
    d.line([(22,9),(24,10),(25,10)],fill=13)
    d.polygon([(3,20),(5,18),(7,18),(10,21),(9,23),(6,24),(3,22)],fill=14)
    d.polygon([(3,20),(5,18),(7,18),(8,19),(6,21),(4,21)],fill=11)
    d.line([(4,19),(5,18),(6,18)],fill=2)
    d.line([(7,20),(8,20),(9,21)],fill=13)
    d.point([(11,24),(27,25)],fill=11)


def build():
    base = ROOT / 'data/tilesets/legends_lights/fallarbor_tiles.png'
    atlas = Image.open(base)
    primary = Image.open(ROOT / 'data/tilesets/legends_lights/general_tiles.png')
    native = ROOT / 'data/tilesets/secondary/fallarbor'
    metas = (ROOT / 'data/tilesets/legends_lights/fallarbor_metatiles.bin').read_bytes()
    assert len(metas) == (FIRST - 0x200) * 16
    template = []
    rock = Image.new('P', (32, 32), 0)
    for x, y, metatile in BLOCKS:
        words = list(struct.unpack_from('<8H', metas, (metatile - 0x200) * 16))
        template.append(words)
        for quadrant, word in enumerate(words[:4] if x == 0 else words[4:]):
            index = word & 1023
            source = primary if index < 512 else atlas
            tx, ty = index % 16 * 8, index % 512 // 16 * 8
            assert not word & 0xC00 and word >> 12 == 11
            rock.paste(source.crop((tx, ty, tx+8, ty+8)),
                       (x + quadrant % 2 * 8, y + quadrant // 2 * 8))
    # Leave the raised west trail beneath the player's feet intact. Fit only
    # the aperture into the band east of its center line, with a lower roof.
    artwork = Image.new('P', (32, 32), 255)
    carve(artwork)
    fitted = artwork.resize((25, 27), Image.Resampling.NEAREST)
    mask = Image.frombytes('L', fitted.size, bytes(255 if shade != 255 else 0 for shade in fitted.tobytes()))
    rock.paste(fitted, (7, 4), mask)
    used = {word & 1023 for word in struct.unpack('<%dH' % (len(metas)//2), metas)}
    anim = (ROOT / 'src/tileset_anims.c').read_text()
    for offset in re.findall(r'NUM_TILES_IN_PRIMARY\s*\+\s*(\d+)', anim):
        used.update(range(512 + int(offset), 528 + int(offset)))
    available = [i for i in range(512, 1024) if i not in used]
    free = available[:17]  # The previously shipped cliff cells keep their tile IDs.
    plank_tiles = available[17:21]
    assert len(plank_tiles) == 4

    def store(index, pixels):
        atlas.paste(pixels, (index % 16 * 8, index % 512 // 16 * 8))

    # Opaque black in the existing Fallarbor rock palette. Transparent cuts
    # in the overlying slate and rock layer reveal only this deepest shadow.
    store(free[-1], Image.new('P', (8, 8), 7))
    extra = []
    for block, (x, y, _) in enumerate(BLOCKS):
        words = template[block]
        for quadrant in range(4):
            tx, ty = x + quadrant % 2 * 8, y + quadrant // 2 * 8
            pixels = rock.crop((tx, ty, tx+8, ty+8))
            if pixels.getextrema()[1] == DEEP:
                # Preserve any exposed grass pinhole in the native upper face.
                pixels = pixels.point([15 if i == 0 else 0 if i == DEEP else i for i in range(256)])
                words[quadrant] = 0xA000 | free[-1]
            tid = free[block * 4 + quadrant]
            store(tid, pixels)
            words[quadrant + 4] = 0xB000 | tid
        extra.extend(words)
    # Add the crossbar on the upper layer of a copy of the native threshold.
    # Palette six is already loaded on Route 114. Zero is transparent.
    plank = Image.new('P', (16, 16), 0)
    ink = {'.': 0, 'h': 5, 'm': 6, 'b': 7, 'd': 13, 'n': 15}
    rows = ('.hhhmmmmhhhmhmh.', '.mndmmbmmmmmbmm.',
            '.dmmmbbbmmmmbbd.', '..ddddd.ddddddd.')
    for y, row in enumerate(rows, start=6):
        for x, shade in enumerate(row):
            plank.putpixel((x, y), ink[shade])
    threshold = list(struct.unpack_from('<8H', metas, (0x261 - 0x200) * 16))
    for quadrant, tile_id in enumerate(plank_tiles):
        x, y = quadrant % 2 * 8, quadrant // 2 * 8
        store(tile_id, plank.crop((x, y, x + 8, y + 8)))
        threshold[quadrant + 4] = 0x6000 | tile_id
    extra.extend(threshold)
    atlas.save(OUT / 'fallarbor_cliff_tiles.png', bits=4)
    (OUT / 'fallarbor_cliff_metatiles.bin').write_bytes(metas + struct.pack('<40H', *extra))
    attrs = (native / 'metatile_attributes.bin').read_bytes()
    threshold_attr = attrs[(0x261 - 0x200)*2:(0x262 - 0x200)*2]
    (OUT / 'fallarbor_cliff_attributes.bin').write_bytes(attrs + struct.pack('<4H', *([0x1000]*4)) + threshold_attr)
    colors = [int(v) for line in (native / 'palettes/11.pal').read_text().splitlines()[3:19]
              for v in line.split()]
    rock.putpalette(colors + [0, 0, 0])
    rock.save(OUT / 'cliff_recess_overlay.png', transparency=0)
    spec = dict(resolution=[32,32], palette=11, shadow_palette=10,
                metatiles=list(range(FIRST, FIRST+4)), tile_ids=free, crossbar_tile_ids=plank_tiles,
                base_atlas_sha256=hashlib.sha256(base.read_bytes()).hexdigest(),
                base_metatiles_sha256=hashlib.sha256(metas).hexdigest(),
                base_attributes_sha256=hashlib.sha256(attrs).hexdigest(),
                style='Open rock shelter with a broken overhang and sloping stone floor')
    (OUT / 'custom_cliff.json').write_text(json.dumps(spec, indent=2)+'\n')


if __name__ == '__main__':
    build()
