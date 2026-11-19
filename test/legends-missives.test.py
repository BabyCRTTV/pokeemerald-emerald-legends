"""Verify the board catalogue, NPC wiring and native save-bit reservations."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
def read(path):
    return (root / path).read_text()

header = read("include/constants/legends_missives.h")
flags = re.findall(r"#define (FLAG_MISSIVE_(\w+)_(?:TAKEN|DONE)) FLAG_UNUSED_0x([\dA-F]+)", header)
slots = {int(value, 16) for _, _, value in flags}
assert len(slots) == len(flags) == 12
# Check both games' aliases, including the hidden-item and boss flag ranges.
expected = set(range(0x4A7, 0x4B0)) | {0x4BD, 0x4BE, 0x4BF}
assert slots == expected
for path in ("include/constants/flags.h", "include/constants/flags_frlg.h"):
    for name, value in re.findall(r"^#define\s+(FLAG_\w+)\s+0x([\dA-Fa-f]+)\b", read(path), re.M):
        if int(value, 16) in slots:
            assert re.fullmatch(r"FLAG_(?:UNUSED_)?0x[0-9A-F]+", name), (path, name)

catalogue = read("src/data/legends/journal.h").split("static const struct LegendsAchievement")[0]
entries = re.findall(r'^    \{COMPOUND_STRING.*$', catalogue, re.M)
jobs = read("src/legends_missives.c")
for i, name in enumerate(("TRAIL_KIT", "TRACKS", "WOODS", "POND", "ROPE", "ECHO")):
    assert f"#define MISSIVE_{name} {i}\n" in header
    assert f"[MISSIVE_{name}] =" in jobs
    for suffix in ("TAKEN", "DONE"):
        assert f"FLAG_MISSIVE_{name}_{suffix}" in entries[65+i]
    recipients = []
    for file in (root/"data/maps").glob("*/scripts.inc"):
        if f"setvar VAR_0x8004, MISSIVE_{name}\n" in file.read_text():
            recipients.append(file.parent.name)
            script = file.read_text().split(f"setvar VAR_0x8004, MISSIVE_{name}\n")[0].rsplit("::", 1)[0].splitlines()[-1]
            objects = json.loads((file.parent/"map.json").read_text())["object_events"]
            assert any(obj["script"] == script for obj in objects)
    assert len(recipients) == 1, (name, recipients)
for town in ("OldaleTown", "PetalburgCity", "RustboroCity"):
    events = json.loads(read(f"data/maps/{town}/map.json"))['bg_events']
    assert sum(e.get('script') == 'Missive_Board' for e in events) == 1
print("Six journal IDs, separate save flags, placed recipients and three boards passed.")
