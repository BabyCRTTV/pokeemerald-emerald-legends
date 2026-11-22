"""Keep each pilgrimage reward unique and each monk on reachable, unobstructed ground."""
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return (ROOT / path).read_text()

def data(path):
    return json.loads(read(path))

scripts = read("data/scripts/legends_plate_monks.inc")
gifts = re.findall(r"^    plate_monk (\w+), ITEM_(\w+)_PLATE, FLAG_MONK_(\w+)_PLATE$", scripts, re.M)
assert len(gifts) == len(set(gifts)) == 19
assert {name.upper() for name, item, flag in gifts if name.upper() == item == flag} == {
    "BLANK", "FLAME", "SPLASH", "ZAP", "MEADOW", "ICICLE", "FIST", "TOXIC", "EARTH",
    "SKY", "MIND", "INSECT", "STONE", "SPOOKY", "DRACO", "DREAD", "IRON", "PIXIE", "LEGEND",
}
flags = read("include/constants/flags.h")
for index, (name, _, _) in enumerate(gifts, 0x8E5):
    assert f"#define FLAG_MONK_{name.upper()}_PLATE FLAG_UNUSED_0x{index:X}" in flags
assert "goto_if_eq VAR_RESULT, FALSE, PlateMonk_NoRoom\n    setflag" in scripts
assert "giveitem ITEM_AZURE_FLUTE\n    goto_if_eq VAR_RESULT, FALSE, PlateMonk_NoRoom\n    setflag FLAG_RECEIVED_AZURE_FLUTE" in scripts
assert scripts.count("Chosen one, I entrust") == 19
assert "wildbattle" not in scripts
layouts = {layout["id"]: layout for layout in data("data/layouts/layouts.json")["layouts"]}
seen = {}
for path in (ROOT / "data/maps").glob("*/map.json"):
    game_map = json.loads(path.read_text())
    for monk in game_map.get("object_events", []):
        script = monk.get("script", "")
        if not script.startswith("PlateMonk_"):
            continue
        name = script.removeprefix("PlateMonk_")
        assert name not in seen and game_map["id"] not in seen.values()
        seen[name] = game_map["id"]
        assert monk["trainer_type"] == "TRAINER_TYPE_NONE"
        assert monk["movement_type"] == "MOVEMENT_TYPE_FACE_DOWN"
        assert monk["flag"] == ("FLAG_HIDE_FLUTE_MONK" if name == "Elder" else "0")
        tile = monk["x"], monk["y"]
        approach = tile[0], tile[1] + 1
        occupied = { (event["x"], event["y"]) for kind in ("object_events", "warp_events", "bg_events", "coord_events")
                     for event in game_map[kind] if event is not monk and "x" in event }
        assert tile not in occupied and approach not in occupied, (path, tile)
        layout = layouts[game_map["layout"]]
        width, height = layout["width"], layout["height"]
        grid = struct.unpack(f"<{width * height}H", (ROOT / layout["blockdata_filepath"]).read_bytes())
        for x, y in (tile, approach):
            block = grid[y * width + x]
            assert block >> 12 == monk["elevation"] and (block >> 10) & 3 == 0, (path, x, y)
assert set(seen) == {name for name, _, _ in gifts} | {"Elder"}
assert seen["Elder"] == "MAP_LITTLEROOT_TOWN"
print("19 distinct plate gifts, 20 separate maps, clear interaction tiles and gated rewards passed.")
