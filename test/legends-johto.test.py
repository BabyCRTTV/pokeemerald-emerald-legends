"""Regression coverage for the first Johto chapter and its existing-save identifiers."""
import json
import re
import struct
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_json(path):
    return json.loads((ROOT / path).read_text())


def map_data(name):
    return read_json(f"data/maps/{name}/map.json")


# Map group 77 follows the previously published maps. The first 25 entries were
# also used by the New Bark to Violet preview and can appear in existing saves.
EXPECTED_ORDER = """
Route22 IndigoGate Route26 Route27East TohjoFalls Route27West NewBarkTown
Route29 CherrygroveCity Route30 Route31 VioletCity ElmsLab WindkeepersHouse
GardenHouse GuidesHouse HarborHouse Academy KilnHouse SproutTower
CherrygroveCenter VioletCenter CherrygroveMart VioletMart VioletGym Route32
UnionCave Route33 AzaleaTown SlowpokeWell AzaleaGym ApricornWorkshop
AzaleaCenter AzaleaMart Route32Center SproutTowerBelfry
""".split()

# Each list starts at an entrance and includes the connected exit or landmark.
STOPS = {
    "IlexForest": [(43, 30), (43, 31), (9, 26), (18, 0), (19, 0)],
    "Route34": [(18, 39), (19, 39), (24, 14), (12, 0), (13, 0), (14, 0)],
    "GoldenrodCity": [(12, 29), (14, 29), (9, 13), (25, 8), (30, 10), (5, 19)],
    "Route22": [(47, 7), (8, 6)],
    "IndigoGate": [(7, 9), (7, 2)],
    "Route26": [(16, 9), (16, 28)],
    "Route27East": [(16, 0), (8, 11)],
    "TohjoFalls": [(29, 18), (16, 9), (5, 18)],
    "Route27West": [(23, 11), (0, 14)],
    "NewBarkTown": [(32, 14), (11, 10), (24, 12), (8, 21), (0, 14)],
    "Route29": [(37, 14), (0, 14), (18, 10)],
    "CherrygroveCity": [(37, 14), (10, 18), (8, 21), (14, 20), (30, 20), (23, 9), (30, 9), (16, 0)],
    "Route30": [(14, 31), (17, 0)],
    "Route31": [(17, 22), (0, 12)],
    "VioletCity": [(41, 15), (20, 10), (16, 7), (7, 14), (9, 24), (29, 25), (27, 13), (35, 24), (20, 32)],
    "Route32": [(14, 0), (21, 24), (22, 47), (14, 50)],
    "UnionCave": [(24, 5), (8, 21), (23, 32)],
    "Route33": [(19, 10), (0, 14)],
    "AzaleaTown": [(42, 14), (34, 9), (10, 10), (24, 13), (29, 9), (15, 22)],
    "SlowpokeWell": [(6, 5), (15, 14)],
    "ElmsLab": [(6, 12), (6, 5)],
    "SproutTower": [(6, 11), (8, 8), (12, 4)],
    "SproutTowerBelfry": [(12, 8), (7, 7)],
    "VioletGym": [(4, 9), (2, 7), (4, 4)],
    "AzaleaGym": [(5, 19), (8, 13), (5, 4)],
}


def reachable_tiles(area, layout, start):
    width, height = layout["width"], layout["height"]
    data = (ROOT / layout["blockdata_filepath"]).read_bytes()
    blocks = struct.unpack(f"<{width * height}H", data)
    objects = {(o["x"], o["y"]) for o in area["object_events"]}
    queue = deque([start])
    visited = {start}
    while queue:
        x, y = queue.popleft()
        for neighbor in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            nx, ny = neighbor
            if neighbor in visited or neighbor in objects or not (0 <= nx < width and 0 <= ny < height):
                continue
            block = blocks[ny * width + nx]
            if block & 0xC00 or block >> 12 not in (0, 3, 4):
                continue
            visited.add(neighbor)
            queue.append(neighbor)
    return visited


def check_maps():
    groups = read_json("data/maps/map_groups.json")
    assert groups["group_order"][77] == "gMapGroup_LegendsJohto"
    names = groups["gMapGroup_LegendsJohto"]
    west = ["IlexForest", "Route34", "GoldenrodCity", "Route34DayCare", "GoldenrodCenter",
            "GoldenrodFlorist", "GoldenrodHerbalist", "GoldenrodBikeShop"]
    assert names[len(EXPECTED_ORDER):len(EXPECTED_ORDER) + len(west)] == ["LegendsJohto_" + n for n in west]
    assert names[:len(EXPECTED_ORDER)] == ["LegendsJohto_" + name for name in EXPECTED_ORDER]
    areas = {area["id"]: area for area in map(map_data, names + ["LegendsKanto_ViridianCity"])}
    layouts = {item["id"]: item for item in read_json("data/layouts/layouts.json")["layouts"]}
    for name, stops in STOPS.items():
        area = map_data("LegendsJohto_" + name)
        accessible = reachable_tiles(area, layouts[area["layout"]], stops[0])
        assert set(stops) <= accessible, (name, sorted(set(stops) - accessible))
    opposite = {"left": "right", "right": "left", "up": "down", "down": "up"}
    for name in names:
        area = map_data(name)
        for link in area["connections"]:
            other = areas[link["map"]]
            reverse = {"map": area["id"], "offset": -link["offset"], "direction": opposite[link["direction"]]}
            assert reverse in other["connections"], (name, link)
        for door in area["warp_events"]:
            target = areas[door["dest_map"]]["warp_events"][int(door["dest_warp_id"])]
            assert target["dest_map"] == area["id"], (name, door)


def check_progress():
    trainer_flags = (ROOT / "include/legends_trainer_flags.h").read_text()
    events = (ROOT / "data/scripts/legends_johto.inc").read_text()
    outcomes = {"WREN": "ZEPHYR_BADGE", "RUE": "HIVE_BADGE", **{n: n + "_WON" for n in ("PIP", "LEN", "KIT", "MOSS", "FERN")}}
    for name, flag in outcomes.items():
        assert re.search(rf"case TRAINER_LEGENDS_JOHTO_{name}:\s*return FLAG_JOHTO_{flag};", trainer_flags)
        assert f"trainerbattle_single TRAINER_LEGENDS_JOHTO_{name}," in events
    for checkpoint in ("ELM_SURVEY", "TIDE_READING", "BELL_READING", "SURVEY_RETURNED"):
        assert events.count(f"setflag FLAG_JOHTO_{checkpoint}") == 1
    assert "goto_if_unset FLAG_JOHTO_ZEPHYR_BADGE, Johto_RueGate" in events


def check_building_footprints():
    layouts = {entry["id"]: entry for entry in read_json("data/layouts/layouts.json")["layouts"]}
    tileset = ROOT / "data/tilesets/secondary/legends_johto"
    attributes = [value for value, in struct.iter_unpack("<H", (tileset / "metatile_attributes.bin").read_bytes())]
    graphics = [word for word, in struct.iter_unpack("<H", (tileset / "metatiles.bin").read_bytes())]
    # A 1x2 animated door temporarily borrows the last eight graphics tiles.
    assert all((word & 0x3FF) < 0x3F8 for word in graphics)
    # Johto shares the primary storefront lights in palette 12.
    assert all(word >> 12 != 12 for word in graphics)

    labels = (ROOT / "include/constants/metatile_labels.h").read_text()
    doors = (ROOT / "src/field_door.c").read_text()
    # The rear roof is walkable. The wall immediately below it and the front
    # wall on either side of an animated door must stop the player.
    entrances = {
        "ElmsLab": ("ElmsLabDoor", 4, 1),
        "WindkeepersHouse": ("BlueHouseDoor", 3, 1),
        "GardenHouse": ("RedHouseDoor", 3, 1),
        "GuidesHouse": ("PlumHouseDoor", 3, 1),
        "HarborHouse": ("RedHouseDoor", 3, 1),
        "Academy": ("PlumHouseDoor", 3, 1),
        "KilnHouse": ("BlueHouseDoor", 3, 1),
        "ApricornWorkshop": ("WorkshopDoor", 3, 1),
        "SproutTower": ("SproutTowerDoor", 6, 3),
    }
    by_destination = {map_data("LegendsJohto_" + name)["id"]: name for name in entrances}
    checked = set()
    for name in ("NewBarkTown", "CherrygroveCity", "VioletCity", "AzaleaTown"):
        area = map_data("LegendsJohto_" + name)
        layout = layouts[area["layout"]]
        width = layout["width"]
        blocks = struct.unpack(f"<{width * layout['height']}H", (ROOT / layout["blockdata_filepath"]).read_bytes())

        def block(x, y):
            return blocks[y * width + x]

        def walkable_ground(x, y):
            tile = block(x, y)
            return tile >> 12 == 3 and not (tile & 0xC00)

        for warp in area["warp_events"]:
            destination = warp["dest_map"]
            x, y = warp["x"], warp["y"]
            if destination.endswith("_MART"):
                # The cap uses both corner pieces and walkable center pieces.
                assert [block(col, y - 3) for col in range(x - 1, x + 3)] == [0x3028, 0x3029, 0x3029, 0x302B]
            interior = by_destination.get(warp["dest_map"])
            if interior is None:
                continue
            label, depth, roof_rows = entrances[interior]
            symbol = "METATILE_LegendsJohto_" + label
            metatile = int(re.search(rf"#define {symbol}\s+(0x[0-9A-Fa-f]+)", labels).group(1), 16)
            assert block(x, y) & 0x3FF == metatile
            assert attributes[metatile - 0x200] & 0xFF == 0x69  # MB_ANIMATED_DOOR
            assert re.search(rf"\.metatileNum = {symbol},\s+\.tileset = &gTileset_LegendsJohto,", doors)
            assert all(block(col, y) & 0xC00 for col in (x - 1, x, x + 1))
            assert walkable_ground(x, y + 1)
            assert walkable_ground(x, y - depth)
            assert block(x, y - depth + roof_rows) & 0xC00
            if interior == "SproutTower":
                assert walkable_ground(x - 3, y - 2)
                assert block(x - 2, y - 2) & 0xC00
            checked.add(interior)
    assert checked == set(entrances)


def check_coast_and_woodland():
    layouts = {entry["id"]: entry for entry in read_json("data/layouts/layouts.json")["layouts"]}
    coast = {"Route27East": (14, 17), "Route27West": (16, 17),
             "NewBarkTown": (31, 18), "CherrygroveCity": (23, 24)}
    # Exterior and interior use different graphics banks but keep their map
    # block numbers. An unassigned interior block displays an empty square.
    for bank, directory in (("gTileset_LegendsJohto", "legends_johto"),
                            ("gTileset_LegendsJohtoInterior", "legends_johto_interior")):
        metatiles = (ROOT / "data/tilesets/secondary" / directory / "metatiles.bin").read_bytes()
        for layout in layouts.values():
            if layout["secondary_tileset"] != bank:
                continue
            blocks = (ROOT / layout["blockdata_filepath"]).read_bytes()
            for tile in {word & 0x3FF for word, in struct.iter_unpack("<H", blocks)}:
                if tile >= 0x200:
                    offset = (tile - 0x200) * 16
                    assert any(metatiles[offset:offset + 16]), (layout["name"], tile)

    # The ocean is south of these shores. A north-facing sand tile leaves
    # disconnected patches of water on the beach despite identical collision.
    for area, (x, y) in coast.items():
        layout = layouts[map_data("LegendsJohto_" + area)["layout"]]
        blocks = [v for v, in struct.iter_unpack("<H", (ROOT / layout["blockdata_filepath"]).read_bytes())]
        width = layout["width"]
        assert blocks[(y - 1) * width + x] >> 12 == 3, area
        assert blocks[y * width + x] == 0x112C, area
        assert blocks[(y + 1) * width + x] == 0x1170, area

    # Emerald joins the two halves of each trunk horizontally. Dense stands
    # use a different bottom pair where the next row meets the canopy.
    tree_rows = [({0x1D4, 0x1D6}, {0x1D5, 0x1D7}),
                 ({0x1DC}, {0x1DD}), ({0x1E4, 0x1E6}, {0x1E5, 0x1E7})]
    for area in EXPECTED_ORDER:
        layout = layouts[map_data("LegendsJohto_" + area)["layout"]]
        if layout["secondary_tileset"] != "gTileset_LegendsJohto" or layout["primary_tileset"] != "gTileset_General":
            continue
        width = layout["width"]
        blocks = [v for v, in struct.iter_unpack("<H", (ROOT / layout["blockdata_filepath"]).read_bytes())]
        for offset, block in enumerate(blocks):
            x = offset % width
            for left, right in tree_rows:
                if block & 0x3FF in left:
                    assert x + 1 < width and blocks[offset + 1] & 0x3FF in right, (area, offset)
                if block & 0x3FF in right:
                    assert x > 0 and blocks[offset - 1] & 0x3FF in left, (area, offset)


def check_roads_and_borders():
    layouts = {entry["id"]: entry for entry in read_json("data/layouts/layouts.json")["layouts"]}
    exteriors = {}
    for name in EXPECTED_ORDER:
        area = map_data("LegendsJohto_" + name)
        layout = layouts[area["layout"]]
        if layout["secondary_tileset"] != "gTileset_LegendsJohto":
            continue
        width = layout["width"]
        blocks = [v for v, in struct.iter_unpack("<H", (ROOT / layout["blockdata_filepath"]).read_bytes())]
        rows = [blocks[i:i + width] for i in range(0, len(blocks), width)]
        exteriors[name] = rows
        for sign in area["bg_events"]:
            if sign["type"] == "sign":
                assert rows[sign["y"]][sign["x"]] == 0x0403, (name, sign["script"])

        if name in ("CherrygroveCity", "NewBarkTown", "Route27East", "Route27West", "Route29"):
            # All parts of the surf line, including a little inward hook, use
            # the same elevation as their native counterparts in Slateport.
            for row in rows:
                for block in row:
                    if block & 0x3FF in (0x12B, 0x12C, 0x12D, 0x145, 0x146):
                        assert block >> 12 == 1, (name, hex(block))
            border = [v for v, in struct.iter_unpack("<H", (ROOT / layout["border_filepath"]).read_bytes())]
            bw, bh = layout["border_width"], layout["border_height"]
            assert len(border) == bw * bh
            for x, block in enumerate(rows[-1]):
                if block >> 12 == 1:
                    beyond = border[(len(rows) % bh) * bw + x % bw]
                    assert beyond in (0x170, 0x12B, 0x12C, 0x12D), (name, x)
            assert border[(-2 % bh) * bw] in (0x1D4, 0x1D6), name

    # Both maps draw each marked lane from the same material at the exact
    # join. A straight step out of either map lands on walkable ground.
    gates = [
        ("Route26", "down", "Route27East", (16, 17)),
        ("Route27West", "left", "NewBarkTown", (14, 15)),
        ("NewBarkTown", "left", "Route29", (14, 15)),
        ("CherrygroveCity", "right", "Route29", (14, 15)),
        ("Route30", "down", "CherrygroveCity", (14, 15)),
        ("Route31", "down", "Route30", (17, 18)),
        ("VioletCity", "right", "Route31", (14, 15, 16)),
        ("VioletCity", "down", "Route32", (19, 20, 21)),
        ("AzaleaTown", "right", "Route33", (14, 15)),
    ]
    for source, direction, dest, lanes in gates:
        a, b = exteriors[source], exteriors[dest]
        link = next(c for c in map_data("LegendsJohto_" + source)["connections"] if c["direction"] == direction)
        assert link["map"] == map_data("LegendsJohto_" + dest)["id"]
        for lane in lanes:
            other = lane - link["offset"]
            if direction == "down":
                first, second = a[-1][lane], b[0][other]
            elif direction == "right":
                first, second = a[lane][-1], b[other][0]
            else:
                first, second = a[lane][0], b[other][-1]
            assert first == second and first >> 10 == 12, (source, dest, lane, hex(first), hex(second))

    tower = exteriors["VioletCity"]
    warp = next(w for w in map_data("LegendsJohto_VioletCity")["warp_events"] if w["dest_map"].endswith("_SPROUT_TOWER"))
    x, y = warp["x"], warp["y"]
    landing = tower[y + 1][x - 1:x + 2]
    deck = tower[y + 2][x - 1:x + 2]
    assert all(block >> 10 == 12 for block in landing) and landing != deck
    assert len(set(deck)) == 3 and all(block >> 10 == 12 for block in deck)
    assert all(row[x - 1:x + 2] == deck for row in tower[y + 2:y + 5])
    assert all(tower[y + 3][col] >> 12 == 1 for col in (x - 2, x + 2))

    # Walking can succeed even when an opaque BG1 deck hides the trainer.
    # Probe the board ends, inner paving corners, town gates and their approaches.
    tileset = ROOT / "data/tilesets/secondary/legends_johto"
    attributes = [v for v, in struct.iter_unpack("<H", (tileset / "metatile_attributes.bin").read_bytes())]
    ground = {
        "CherrygroveCity": [(8, 21), (9, 22)],
        "Route32": [(19, 25), (21, 26), (14, 0)],
        "VioletCity": [(x + dx, row) for dx in (-1, 0, 1) for row in range(y + 1, y + 6)]
                      + [(20, 19), (20, 32), (41, 15)],
        "AzaleaTown": [(4, 8)],
    }
    for name, samples in ground.items():
        for col, row in samples:
            block = exteriors[name][row][col]
            tile = block & 0x3FF
            assert block >> 10 == 12 and tile >= 0x200, (name, col, row)
            assert attributes[tile - 0x200] >> 12 == 1, (name, col, row, hex(tile))


def check_western_shores():
    layouts = {entry["id"]: entry for entry in read_json("data/layouts/layouts.json")["layouts"]}
    def words(path):
        return [word for word, in struct.iter_unpack("<H", (ROOT / path).read_bytes())]

    stock = words("data/tilesets/primary/general/metatiles.bin")
    johto = words("data/tilesets/secondary/legends_johto/metatiles.bin")
    for area, y, left, right, bridge in (("IlexForest", 21, 17, 27, {22, 23}),
                                         ("Route34", 25, 3, 9, {7, 8})):
        layout = layouts[map_data("LegendsJohto_" + area)["layout"]]
        blocks = words(layout["blockdata_filepath"])
        for x in range(left, right + 1):
            if x in bridge:
                continue
            block = blocks[y * layout["width"] + x]
            assert block >> 12 == 1
            # Match all eight graphics words to the reflected stock north bank.
            # Repeating the corner in a straight run leaves a notch every 16 pixels.
            north = 0x188 if x == left else 0x18A if x == right else 0x189
            source = stock[north * 8:(north + 1) * 8]
            expected = [source[j ^ 2] ^ 0x800 if source[j ^ 2] else 0 for j in range(8)]
            offset = ((block & 0x3FF) - 0x200) * 8
            assert johto[offset:offset + 8] == expected, (area, x, y)


if __name__ == "__main__":
    check_maps()
    check_progress()
    check_building_footprints()
    check_coast_and_woodland()
    check_roads_and_borders()
    check_western_shores()
    print("Johto map identifiers, paths, borders, signs, coasts, woodland, building collision, doors, trainers and survey checkpoints passed.")
