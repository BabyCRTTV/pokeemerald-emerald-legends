"""Verify Day Off in Hoenn through the actual follower A-button entry point."""
from ctypes import CDLL, c_uint, c_void_p, string_at
from hashlib import sha256
import json
import os
from pathlib import Path
from subprocess import check_output, run

from PIL import Image

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[2]
OUTPUT = ROOT / "build/day-off-qa"
OUTPUT.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)

A, B, DOWN = 1, 2, 128
MAILBOX = 0x0203FD00
ROOM = 0x1F80000


def symbols(path):
    return {
        fields[2]: int(fields[0], 16)
        for line in check_output(["arm-none-eabi-nm", str(path)], text=True).splitlines()
        if len(fields := line.split()) == 3
    }


elf = Path("pokeemerald.elf")
rom = elf.with_suffix(".gba")
sy = symbols(elf)
run(["cc", "-shared", "-fPIC", str(SOURCE.parent / "native_poffin_qa/core.c"),
     "-lmgba", "-o", str(OUTPUT / "core.so")], check=True)
run(["arm-none-eabi-gcc", "-iquote", "include", "-iquote", ".", "-DMODERN=1",
     "-DEMERALD", "-mthumb", "-mcpu=arm7tdmi", "-mabi=apcs-gnu", "-Os",
     "-ffreestanding", "-fno-builtin", "-fno-jump-tables", "-nostdlib",
     "-Wl,-Ttext=0x09f80000", "-Wl,--entry=qa", "-Wl,--just-symbols=" + str(elf),
     f"-Wl,--defsym=gDayOffQaScriptContext={sy['sGlobalScriptContext']:#x}",
     str(SOURCE / "arm.c"), "-o", str(OUTPUT / "arm.elf")], check=True)
run(["arm-none-eabi-objcopy", "-O", "binary", str(OUTPUT / "arm.elf"),
     str(OUTPUT / "arm.bin")], check=True)
original = rom.read_bytes()
payload = (OUTPUT / "arm.bin").read_bytes()
assert set(original[ROOM:ROOM + len(payload)]) == {255}
private = OUTPUT / "private.gba"
private.write_bytes(original[:ROOM] + payload + original[ROOM + len(payload):])

fixture = symbols(OUTPUT / "arm.elf")["qa"] | 1
core = CDLL(str(OUTPUT / "core.so"))
core.screen.restype = c_void_p
core.rd.restype = c_uint
core.wr.restype = core.step.restype = core.reset.restype = None
assert core.init(bytes(private))
private.unlink()
main = sy["gMain"]


def read(index):
    return core.rd(MAILBOX + 4 * index)


def write(index, value):
    core.wr(MAILBOX + 4 * index, value)


def command(number):
    write(0, number)
    write(3, core.rd(main + 4))
    write(4, 0)
    for _ in range(10):
        core.wr(main + 4, fixture)
        core.step(12 if number == 0 else 1, 0)
        if read(4):
            return
    raise AssertionError((number, hex(core.rd(main + 4)), [read(i) for i in range(12)]))


def key(button, wait=45):
    core.step(3, button)
    core.step(wait, 0)


def capture(name):
    image = Image.frombytes("RGBA", (240, 160), string_at(core.screen(), 240 * 160 * 4))
    image.convert("RGB").resize((720, 480), Image.Resampling.NEAREST).save(OUTPUT / f"{name}.png")


def in_menu():
    target = sy["Task_HandleMultichoiceInput"] | 1
    tasks = range(sy["gTasks"], sy["gTasks"] + 16 * 40, 40)
    return any(core.rd(task) == target and core.rd(task + 4) & 0xff for task in tasks)


def setup(index):
    core.reset()
    core.step(500, 0)
    core.wr(main, 0)
    write(1, index)
    command(0)
    core.step(430, 0)
    command(1)
    core.step(12, 0)
    command(2)
    assert (read(5), read(6), read(10), read(11)) == (1, 0, 3, 1), [read(i) for i in range(12)]


def assert_line(label):
    # The real script message is buffered by loadword into script bank 0.
    command(2)
    text = read(12)
    assert text == sy[label], (label, hex(text), hex(sy[label]))


def finish():
    for _ in range(3):
        key(A, 75)
        command(2)
        if not read(6):
            break
    assert read(5) and not read(6) and not in_menu(), ([read(i) for i in range(12)], in_menu())


def enter(name, spot):
    key(A, 80)
    assert in_menu(), (name, [read(i) for i in range(12)])
    command(2)
    assert read(7) == spot
    capture(name)


checks = []
try:
    for index, name, spot, reaction, intro, result in [
        (0, "Route102", 1, 1, "Pond", "SkipWater"),
        (1, "Dewford", 2, 2, "Shore", "SkipShy"),
        (3, "Route113-Torchic", 4, 3, "Wash", "WashFire"),
        (4, "Route113-Mudkip", 4, 1, "Wash", "WashWater"),
    ]:
        setup(index)
        enter(name + "-Menu", spot)
        key(A, 105)
        assert_line("LegendsDayOff_Text_" + intro)
        capture(name + "-Intro")
        key(A, 22 if spot == 4 else 12)
        capture(name + "-Action")
        core.step(95, 0)
        command(2)
        assert read(8) == reaction
        assert_line("LegendsDayOff_Text_" + result)
        capture(name + "-Reaction")
        finish()
        checks.append(name)

    for action in ["find", "miss", "cancel"]:
        setup(2)
        enter("Woods-Menu", 3)
        key(A, 100)
        assert_line("LegendsDayOff_Text_Hide")
        key(A, 105)
        assert in_menu()
        command(2)
        assert not read(5)
        capture("Woods-Seek")
        if action == "cancel":
            key(B, 120)
            result = "SeekStop"
        else:
            if read(9) ^ (action == "miss"):
                key(DOWN)
            key(A, 120)
            result = "SeekGrass" if action == "find" else "SeekMiss"
        assert_line("LegendsDayOff_Text_" + result)
        capture("Woods-" + action.title())
        finish()
        checks.append("Woods-" + action)

    setup(0)
    enter("Route102-Menu", 1)
    key(B, 100)
    command(2)
    assert read(5) and not read(6) and not in_menu(), ([read(i) for i in range(12)], in_menu())
    enter("Route102-Menu", 1)
    key(DOWN)
    key(A, 230)
    assert not in_menu()
    command(2)
    assert read(6)
    finish()
    checks.extend(["main-menu cancel", "ordinary talk from menu"])

    setup(5)
    key(A, 230)
    assert not in_menu()
    command(2)
    assert read(7) == 0 and read(6)
    finish()
    checks.append("ordinary talk away from a play spot")
except Exception:
    capture("failure")
    raise

(OUTPUT / "verification.json").write_text(json.dumps({
    "version": Path("VERSION").read_text().strip(),
    "romSha256": sha256(original).hexdigest(),
    "emulator": "mGBA native core",
    "captureSize": [720, 480],
    "captureScaling": "3x nearest-neighbor",
    "fixtures": "Private controlled map, position and party setup, then actual controller input",
    "checks": checks,
    "harnessSha256": {name: sha256((SOURCE / name).read_bytes()).hexdigest()
                      for name in ("arm.c", "run.py")},
}, indent=2) + "\n")
print("PASS:", ", ".join(checks))
