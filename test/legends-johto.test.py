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


if __name__ == "__main__":
    check_maps()
    check_progress()
    check_building_footprints()
    check_coast_and_woodland()
    print("Johto map identifiers, walkable landmarks, coasts, woodland, building collision, animated doors, trainers and survey checkpoints passed.")
