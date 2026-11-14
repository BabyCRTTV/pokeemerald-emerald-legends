"""Check normal Release Continue with an earlier object-template list."""
from ctypes import CDLL, c_char_p, c_uint, c_void_p, string_at
from hashlib import sha256
import json
from pathlib import Path
from subprocess import check_output

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "build/day-off-qa"
ROM = ROOT / "pokeemerald-release.gba"
symbols = {
    fields[2]: int(fields[0], 16)
    for line in check_output(["arm-none-eabi-nm", str(ROM.with_suffix(".elf"))], text=True).splitlines()
    if len(fields := line.split()) == 3
}

core = CDLL(str(OUTPUT / "core.so"))
core.rd.restype = c_uint
core.init.argtypes = core.load_battery.argtypes = [c_char_p]
core.screen.restype = c_void_p
assert core.init(bytes(ROM))
battery = OUTPUT / "private-old-route102.sav"
assert core.load_battery(bytes(battery))
core.reset()
core.step(500, 0)
for _ in range(50):
    if core.rd(symbols["gMain"] + 4) == symbols["CB2_Overworld"] | 1:
        break
    core.step(3, 1)
    core.step(150, 0)
assert core.rd(symbols["gMain"] + 4) == symbols["CB2_Overworld"] | 1
core.step(230, 0)

fixture = json.loads((OUTPUT / "verification.json").read_text())
route = json.loads((ROOT / "data/maps/Route102/map.json").read_text())
templates = core.rd(symbols["gSaveBlock1Ptr"]) + fixture["templateOffset"]
assert core.rd(templates + 4) & 0xffff == route["object_events"][0]["x"] + 1
prop_index = len(route["object_events"]) - 1
prop = templates + prop_index * 24
assert core.rd(prop) & 0xff == prop_index + 1
assert core.rd(prop + 4) == 41 | (7 << 16)
assert core.rd(prop + 16) == symbols["LegendsDayOff_PondProp"]

# The trainer was saved facing the new prop. Use the field input normally.
# The special variables are halfwords and may not be word-aligned.
spot = symbols["gSpecialVar_0x8004"]
shift = 8 * (spot & 3)
core.step(3, 1)
core.step(90, 0)
assert (core.rd(spot & ~3) >> shift) & 0xffff == 1

image = Image.frombytes("RGBA", (240, 160), string_at(core.screen(), 240 * 160 * 4))
image.convert("RGB").resize((720, 480), Image.Resampling.NEAREST).save(OUTPUT / "Release-Continue-Prop.png")
(OUTPUT / "release-verification.json").write_text(json.dumps({
    "romSha256": sha256(ROM.read_bytes()).hexdigest(),
    "checks": ["Normal Release Continue", "Route 102 prop restored onto an earlier map object list",
               "Existing NPC position retained", "A-button interaction with restored stone pile"],
}, indent=2) + "\n")
battery.unlink()
print("PASS: Release Continue restored the prop and retained an existing NPC position.")
