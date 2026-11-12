"""Actual controller tests and captures for Poffin cooking and the Treat Case."""
from ctypes import CDLL, c_void_p, c_uint, string_at
from pathlib import Path
from subprocess import check_output, run
from PIL import Image
import hashlib
import json
import os

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[2]
OUTPUT = ROOT / "build/treat-case-native"
OUTPUT.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)


def symbols(path):
    result = {}
    for line in check_output(["arm-none-eabi-nm", str(path)], text=True).splitlines():
        parts = line.split()
        if len(parts) == 3:
            result[parts[2]] = int(parts[0], 16)
    return result


elf = ROOT / "pokeemerald.elf"
rom = ROOT / "pokeemerald.gba"
run(["cc", "-shared", "-fPIC", str(SOURCE / "core.c"), "-lmgba",
     "-o", str(OUTPUT / "core.so")], check=True)
run(["arm-none-eabi-gcc", "-iquote", "include", "-iquote", ".",
     "-DMODERN=1", "-DEMERALD", "-mthumb", "-mcpu=arm7tdmi", "-mabi=apcs-gnu",
     "-Os", "-ffreestanding", "-fno-builtin", "-fno-jump-tables", "-nostdlib",
     "-Wl,-Ttext=0x09f80000", "-Wl,--entry=qa", "-Wl,--just-symbols=" + str(elf),
     str(SOURCE / "arm.c"), "-o", str(OUTPUT / "arm.elf")], check=True)
run(["arm-none-eabi-objcopy", "-O", "binary", str(OUTPUT / "arm.elf"),
     str(OUTPUT / "arm.bin")], check=True)
original = rom.read_bytes()
payload = (OUTPUT / "arm.bin").read_bytes()
assert set(original[0x1f80000:0x1f80000 + len(payload)]) == {255}
private = bytearray(original)
private[0x1f80000:0x1f80000 + len(payload)] = payload
private_path = OUTPUT / "private.gba"
private_path.write_bytes(private)

sy = symbols(elf)
fixture = symbols(OUTPUT / "arm.elf")["qa"] | 1
core = CDLL(str(OUTPUT / "core.so"))
core.screen.restype = c_void_p
core.rd.restype = c_uint
core.step.restype = None
core.wr.restype = None
assert core.init(bytes(private_path))
private_path.unlink()
main = sy["gMain"]
mailbox = 0x0203ffc0


def frames(count, keys=0):
    core.step(count, keys)


def key(keys, wait=90):
    frames(3, keys)
    frames(wait)


def value(index):
    return core.rd(mailbox + index * 4)


def command(number):
    previous = core.rd(main + 4)
    core.wr(mailbox, number)
    core.wr(mailbox + 12, previous)
    core.wr(mailbox + 16, 0)
    core.wr(main + 4, fixture)
    frames(180 if number == 2 else 1)
    for _ in range(10):
        if value(4):
            break
        core.wr(main + 4, fixture)
        frames(180 if number == 2 else 1)
    assert value(4), f"Fixture command {number} did not finish"


def screenshot(name):
    image = Image.frombytes("RGBA", (240, 160), string_at(core.screen(), 240 * 160 * 4)).convert("RGB")
    image = image.resize((720, 480), Image.Resampling.NEAREST)
    image.save(OUTPUT / (name + ".png"))
    return image


def callback(name):
    return core.rd(main + 4) == (sy[name] | 1)


def task_active(name):
    target = sy[name] | 1
    return any(core.rd(sy["gTasks"] + index * 40) == target for index in range(16))


def until_yes():
    for _ in range(24):
        if task_active("Task_HandleYesNoInput"):
            return
        key(1, 130)
    screenshot("failure-dialogue")
    raise AssertionError("Yes/no prompt missing")


def enter_case_from_machine():
    key(1, 170)
    until_yes()
    key(128, 20)
    key(1, 160)
    until_yes()
    key(1, 180)
    assert callback("CaseMain")


# Fresh trainer, party and berries. All subsequent gameplay uses real controls.
frames(500)
core.wr(main, 0)
command(0)
frames(430)
key(64)
key(1, 140)
screenshot("07-First-Visit")
key(1, 140)
screenshot("08-Treat-Case-Gift")
until_yes()
command(1)
assert value(14) == 1

# First cooking interaction after the one-time gift.
key(1, 100)
key(1, 180)
key(1, 180)
until_yes()
key(1, 160)
key(128, 20)
key(1, 180)
assert callback("Main") or core.rd(sy["sBatch"]) != 0
batch = sy["sBatch"]
for index in range(260):
    frame = core.rd(batch + 4) & 0xffff
    if frame >= 1080:
        break
    order = [64, 32, 128, 16] if 360 <= frame < 720 else [64, 16, 128, 32]
    frames(8, order[index % 4])
frames(30)
screenshot("09-Cooked")
command(1)
flavors = (value(8), value(9))
assert (value(5), value(6), value(7)) == (2, 1, 15)
assert min(flavors) > 0 and value(15) == 0

key(1, 180)
command(2)
assert (value(10), value(11)) == (1, 1)
assert (value(7), value(8), value(9), value(14)) == (15, *flavors, 1)
enter_case_from_machine()
command(1)
assert value(14) == 1
screenshot("10-Treat-Case")

# Select the Pokémon through its ordinary condition screen.
key(1, 200)
key(1, 160)
screenshot("11-Offer-Poffin")
key(1, 40)
for _ in range(30):
    if callback("FeedMain"):
        break
    frames(3)
assert callback("FeedMain")
animation = []
for _ in range(48):
    frames(6)
    animation.append(Image.frombytes("RGBA", (240, 160),
                     string_at(core.screen(), 240 * 160 * 4)).convert("RGB").resize((720, 480), Image.Resampling.NEAREST))
animation[10].save(OUTPUT / "12-Poffin-Feeding.png")
animation[0].save(OUTPUT / "13-Poffin-Feeding.gif", save_all=True,
                  append_images=animation[1:], duration=100, loop=0)
screenshot("14-Poffin-Reaction")
key(1, 220)
for _ in range(14):
    if callback("CaseMain"):
        break
    key(1, 130)
assert callback("CaseMain")
command(1)
assert value(7) == 0 and value(12) == flavors[0] and value(13) == flavors[1]
screenshot("15-Empty-Case")

# Bag entry and return, including registered SELECT use.
key(2, 180)
key(8, 100)
key(128)
key(128)
key(1, 180)
key(16, 120)
key(128)
screenshot("16-Treat-Case-In-Bag")
key(1, 80)
key(1, 180)
assert callback("CaseMain")
key(2, 180)
key(1, 80)
screenshot("17-Bag-Actions")
# A key item offers USE and REGISTER on a two-column menu.
key(16, 20)
key(1, 120)
key(2, 180)
key(2, 120)
key(4, 180)
assert callback("CaseMain")
key(2, 180)

# Migration is deterministic and repeated initialization does not duplicate it.
command(3)
assert (value(7), value(8), value(9), value(15)) == (16, 8, 21, 1)
command(2)
assert (value(7), value(8), value(9), value(15)) == (16, 8, 21, 1)

# Forty independent records, full-case refusal and scrolling.
command(4)
enter_case_from_machine()
for _ in range(12):
    key(128, 20)
screenshot("18-Full-Treat-Case")
key(2, 180)
key(1, 170)
until_yes()
key(1, 180)
until_yes()
command(1)
assert (value(5), value(6)) == (2, 1)
key(128, 20)
key(1, 180)
command(2)
assert (value(10), value(11), value(14), value(15)) == (1, 1, 1, 1)

assert core.battery(bytes(OUTPUT / "private-full-case.sav"))
assert rom.read_bytes() == original
receipt = {
    "version": (ROOT / "VERSION").read_text().strip(),
    "emulator": "mGBA native core",
    "rom_sha256": hashlib.sha256(original).hexdigest(),
    "passed": True,
    "tests": ["first-use gift", "one case on repeat interaction", "two-berry cooking",
              "separate storage", "battery round trip", "custom feeding and condition gains",
              "exactly one consumed", "Bag open/return", "registered SELECT use",
              "preview record migration and idempotence", "40-record capacity and scroll",
              "full-case refusal without berry loss"],
    "limits": "Controlled fixture, not an authentic historical player save or full story playthrough.",
}
(OUTPUT / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
print(json.dumps(receipt, indent=2))
