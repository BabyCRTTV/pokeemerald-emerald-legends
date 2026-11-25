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


if __name__ == "__main__":
    check_maps()
    check_progress()
    print("Johto map identifiers, walkable landmarks, return warps, trainers and survey checkpoints passed.")
