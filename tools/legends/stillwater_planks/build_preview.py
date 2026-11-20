"""Build one playable Stillwater art option atop the approved rock terrace.

Run from a clean checkout of the review branch. The native inputs are restored
after make, including on failure. Only the requested preview build is copied out.
"""
import argparse
import re
import shutil
import struct
import subprocess
import tempfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[3]
ART = ROOT / "data/tilesets/legends_grotto"
ATLAS = ART / "fallarbor_cliff_tiles.png"
METAS = ART / "fallarbor_cliff_metatiles.bin"
ATTRS = ART / "fallarbor_cliff_attributes.bin"
ROUTE = ROOT / "data/layouts/Route114/map.bin"
EVENT = ROOT / "data/scripts/legends_grotto_review.inc"

# Tile-local indexed pixels. The worn edge catches light from the northwest.
# Keep the arch above the player's head and the lip below the board visible.
PATTERNS = {
    "A": [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        ".hhhmmmmhhhmhmh.",
        ".mndmmbmmmmmbmm.",
        ".dmmmbbbmmmmbbd.",
        "..ddddd.ddddddd.",
    ],
    "B": [
        "................",
        ".hh.............",
        ".mnhh...........",
        ".bdmmhh.........",
        "..dbbmmhh.......",
        "....dbbmmhh.....",
        "......dbbmmhh...",
        "........dbbmmhh.",
        "..........dbbmmm",
        "............dbbd",
        "..............d.",
    ],
    "C": [
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "hhhmmmmh........",
        "mndmmmmbhh......",
        "dmmmmbbbmmh.....",
        ".ddbbmmm........",
        "...ddddbb.......",
        ".......ddh......",
    ],
}

# The diagonal board hangs alongside the jamb after the player swings it.
SWUNG_ASIDE = [
    ".hh.............", ".hm.............", ".hnb............",
    ".hmb............", ".mbd............", ".hbd............",
    ".hmb............", ".mmb............", ".hmb............",
    ".mbd............", ".hbd............", ".mbd............",
    ".hmb............", ".mbd............", ".db.............",
]


# Use the existing, straw, ochre and dark wood tones from Fallarbor palette six.
INK = {".": 0, "h": 5, "m": 6, "b": 7, "d": 13, "n": 15}
TEXT = {
    "A": ("A faded plank rests in two notches.", "Lift it and enter the grotto?"),
    "B": ("One old nail holds the plank.", "Swing it aside and enter?"),
    "C": ("The end of the plank has split.", "Slip through the gap?"),
}


def fit_plank(option):
    image = Image.open(ATLAS).copy()
    metas = METAS.read_bytes()
    attrs = ATTRS.read_bytes()
    new_id = 0x200 + len(metas) // 16
    assert new_id < 0x400 and len(attrs) * 8 == len(metas)
    original = list(struct.unpack_from("<8H", metas, (0x261 - 0x200) * 16))
    assert original[4:] == [0xB000] * 4
    used = {word & 1023 for (word,) in struct.iter_unpack("<H", metas)}
    anim = (ROOT / "src/tileset_anims.c").read_text()
    for offset in re.findall(r"NUM_TILES_IN_PRIMARY\s*\+\s*(\d+)", anim):
        used.update(range(512 + int(offset), 528 + int(offset)))
    free = iter(i for i in range(512, 1024) if i not in used)
    threshold_attr = attrs[(0x261 - 0x200) * 2:(0x262 - 0x200) * 2]
    tiles = {}
    patterns = [PATTERNS[option]]
    if option == "B":
        patterns.append(SWUNG_ASIDE)
    for pattern in patterns:
        layer = Image.new("P", (16, 16))
        words = original.copy()
        for y, row in enumerate(pattern):
            assert len(row) == 16
            for x, pixel in enumerate(row):
                layer.putpixel((x, y), INK[pixel])
        for i in range(4):
            x, y = i % 2 * 8, i // 2 * 8
            quad = layer.crop((x, y, x + 8, y + 8))
            if not quad.getbbox():
                continue
            pixels = quad.tobytes()
            if pixels not in tiles:
                slot = next(free)
                tiles[pixels] = slot
                image.paste(quad, (slot % 16 * 8, (slot - 512) // 16 * 8))
            words[i + 4] = 0x6000 | tiles[pixels]
        metas += struct.pack("<8H", *words)
        attrs += threshold_attr
    assert new_id == 0x379
    image.save(ATLAS, bits=4)
    METAS.write_bytes(metas)
    ATTRS.write_bytes(attrs)
    route = bytearray(ROUTE.read_bytes())
    cell = (46 * 40 + 7) * 2
    word, = struct.unpack_from("<H", route, cell)
    assert word & 0x3FF == 0x261 and word & 0xC00
    struct.pack_into("<H", route, cell, (word & ~0x3FF) | new_id)
    ROUTE.write_bytes(route)


def fit_interaction(option):
    script = EVENT.read_text()
    start = script.index("LegendsGrotto_EnterStillwater::")
    warp = script.index("\twarp ", start)
    if option in ("A", "B"):
        opened = "0x261" if option == "A" else "0x37A"
        action = (f"\tplayse SE_BRIDGE_WALK\n\tsetmetatile 7, 46, {opened}, 1\n"
                  "\tspecial DrawWholeMapView\n\tdelay 32\n")
    else:
        action = ("\tapplymovement OBJ_EVENT_ID_PLAYER, StillwaterPlank_SlipPast\n"
                  "\twaitmovement 0\n")
        script += "\nStillwaterPlank_SlipPast:\n\twalk_in_place_faster_up\n\tstep_end\n"
    script = script[:warp] + action + script[warp:]
    text = 'LegendsGrotto_Text_StillwaterEntry:\n'
    a = script.index(text) + len(text)
    b = script.index('LegendsGrotto_Text_RainrootEntry:', a)
    first, second = TEXT[option]
    EVENT.write_text(script[:a] + f'\t.string "{first}\\n"\n\t.string "{second}$"\n' + script[b:])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("option", choices=PATTERNS)
    parser.add_argument("output", type=Path)
    parser.add_argument("-j", type=int, default=4)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    files = [ATLAS, METAS, ATTRS, ROUTE, EVENT]
    # Temporary input edits must never clobber another local build or map edit.
    paths = [str(p.relative_to(ROOT)) for p in files]
    if subprocess.run(["git", "diff", "--quiet", "HEAD", "--", *paths], cwd=ROOT).returncode:
        parser.error("The five native inputs must match the checkout before creating a preview.")
    with tempfile.TemporaryDirectory() as tmp:
        for p in files:
            shutil.copy2(p, Path(tmp) / p.name)
        try:
            fit_plank(args.option)
            fit_interaction(args.option)
            for target, stem in [("all", "pokeemerald"), ("release", "pokeemerald-release")]:
                subprocess.run(["make", f"-j{args.j}", target], cwd=ROOT, check=True)
                for ext in ("gba", "elf"):
                    shutil.copyfile(ROOT / f"{stem}.{ext}", args.output / f"{stem}.{ext}")
        finally:
            for p in files:
                shutil.copyfile(Path(tmp) / p.name, p)


if __name__ == "__main__":
    main()
