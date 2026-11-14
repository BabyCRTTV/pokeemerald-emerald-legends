"""Verify rental entry, payment and room interactions with mGBA controller input."""
from ctypes import CDLL, c_char_p, c_uint, c_void_p, string_at
from hashlib import sha256
import json
import os
import re
from pathlib import Path
from subprocess import Popen, check_output, run

from PIL import Image

SOURCE = Path(__file__).resolve().parent
ROOT = SOURCE.parents[2]
OUTPUT = ROOT / "build/apartment-qa"
OUTPUT.mkdir(parents=True, exist_ok=True)
os.chdir(ROOT)

A, B, RIGHT, LEFT, UP, DOWN = 1, 2, 16, 32, 64, 128
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
     f"-Wl,--defsym=gRentalQaScriptContext={sy['sGlobalScriptContext']:#x}",
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
core.battery.argtypes = [c_char_p]
core.wr.restype = core.step.restype = core.reset.restype = None
assert core.init(bytes(private))
private.unlink()
main = sy["gMain"]
recording = None
record_frame = 0


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
        core.step({0: 12, 4: 180}.get(number, 1), 0)
        if read(4):
            return
    raise AssertionError((number, hex(core.rd(main + 4)), [read(i) for i in range(16)]))


def advance(frames, button=0):
    global record_frame
    if recording is None:
        core.step(frames, button)
        return
    for _ in range(frames):
        core.step(1, button)
        record_frame += 1
        if record_frame % 2 == 0:
            recording.stdin.write(string_at(core.screen(), 240 * 160 * 4))


def key(button, wait=45):
    advance(3, button)
    advance(wait)


def capture(name):
    image = Image.frombytes("RGBA", (240, 160), string_at(core.screen(), 240 * 160 * 4))
    image.convert("RGB").resize((720, 480), Image.Resampling.NEAREST).save(OUTPUT / f"{name}.png")


def map_id(symbol):
    constants = Path("include/constants/map_groups.h").read_text()
    match = re.search(rf"^    {symbol} += \((\d+) \| \((\d+) << 8\)\),$", constants, re.M)
    assert match, symbol
    return int(match[1]) | (int(match[2]) << 8)


LILY_FLOOR = map_id("MAP_LILYCOVE_CITY_COVE_LILY_MOTEL_2F")
LILY_ROOM = map_id("MAP_LILYCOVE_CITY_COVE_LILY_MOTEL_APARTMENT")
HILLS_LOBBY = map_id("MAP_MAUVILLE_CITY_MAUVILLE_HILLS_LOBBY")
HILLS_ROOM = map_id("MAP_MAUVILLE_CITY_MAUVILLE_HILLS_APARTMENT")


def load(scene, money=None):
    if money is not None:
        core.reset()
        core.step(500, 0)
        core.wr(main, 0)
        write(2, money)
    write(1, scene)
    command(0 if money is not None else 1)
    core.step(280, 0)
    command(3)
    core.step(12, 0)


def inspect():
    command(2)
    return [read(i) for i in range(5, 16)]


def check(map_number=None, money=None, flags=None, position=None):
    command(2)
    for index, expected in ((5, map_number), (6, money), (7, flags),
                            (8, None if position is None else position[0] | (position[1] << 16))):
        if expected is not None:
            assert read(index) == expected, (index, expected, read(index), inspect())


def message(label):
    command(2)
    assert read(10) == sy[label], (label, hex(read(10)), hex(sy[label]), inspect())


def offer(label, has_intro=False):
    key(A, 80)
    message(label)
    if has_intro:
        key(A, 75)


def step(direction):
    advance(12, direction)
    advance(18)


def record_rentals():
    global recording
    load(0, 5300)
    destination = OUTPUT / "Emerald-Legends-Apartment-Rentals.mp4"
    with Popen([
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
        "-f", "rawvideo", "-pix_fmt", "rgba", "-s", "240x160",
        "-r", "30", "-i", "-", "-vf", "scale=720:480:flags=neighbor",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
        str(destination),
    ], stdin=-1) as encoder:
        recording = encoder
        advance(50)
        offer("Rental_Text_LilyOffer", has_intro=True)
        advance(70)
        key(A, 110)
        message("Rental_Text_LilyPaid")
        key(A, 15)
        for direction in (LEFT, LEFT, LEFT, LEFT, UP, UP):
            step(direction)
        advance(65)
        check(LILY_FLOOR)
        for _ in range(4):
            step(RIGHT)
        check(position=(6, 2))
        advance(3, UP)
        advance(12)
        key(A, 110)
        check(LILY_ROOM, 3100, 1)
        step(RIGHT)
        step(RIGHT)
        step(UP)
        advance(95)

        # Cut between cities. The same player's money and lease carry through.
        recording = None
        load(2)
        recording = encoder
        advance(70)
        step(UP)
        advance(70)
        check(HILLS_LOBBY)
        step(UP)
        step(UP)
        check(position=(3, 6))
        offer("Rental_Text_MauvilleOffer", has_intro=True)
        advance(70)
        key(A, 115)
        message("Rental_Text_MauvillePaid")
        key(A, 80)
        key(A, 10)
        for direction in (RIGHT, UP, UP, UP, UP, RIGHT, RIGHT):
            step(direction)
        check(position=(6, 2))
        advance(3, UP)
        advance(12)
        key(A, 110)
        check(HILLS_ROOM, 0, 3)
        for _ in range(3):
            step(UP)
        key(A, 80)
        message("Text_BootUpPC")
        key(A, 100)
        advance(70)
        encoder.stdin.close()
        assert encoder.wait() == 0
    print(f"Recorded {destination}")


if os.environ.get("RECORD_APARTMENT_RENTALS") == "1":
    record_rentals()
    raise SystemExit(0)


try:
    # The blocked door cannot be walked into or opened with A.
    load(1, 5300)
    step(UP)
    check(LILY_FLOOR, 5300, 0, (6, 2))
    key(A, 80)
    message("Rental_Text_LilyLocked")
    capture("Cove-Lily-Locked")
    key(A)

    # A declined offer keeps both leases unset. A short wallet does too.
    load(0)
    offer("Rental_Text_LilyOffer", has_intro=True)
    capture("Cove-Lily-One-Time-Rent")
    key(B)
    check(money=5300, flags=0)
    load(0, 2199)
    offer("Rental_Text_LilyOffer", has_intro=True)
    key(A, 85)
    message("Rental_Text_NotEnoughMoney")
    key(A)
    check(money=2199, flags=0)

    load(0, 5300)
    offer("Rental_Text_LilyOffer", has_intro=True)
    key(A, 85)
    message("Rental_Text_LilyPaid")
    key(A)
    check(money=3100, flags=1)
    key(A, 75)
    message("Rental_Text_LilyPaid")
    key(A)
    check(money=3100, flags=1)

    load(1)
    key(A, 180)
    check(LILY_ROOM, 3100, 1, (3, 6))
    for direction in (LEFT, LEFT, LEFT, UP):
        step(direction)
    check(position=(0, 5))
    core.step(3, UP)
    core.step(15, 0)
    command(5)
    offer("Rental_Text_Rest")
    key(A, 275)
    message("Rental_Text_Rested")
    assert read(14) > 1
    key(A)
    for direction in (RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, RIGHT, UP, UP):
        step(direction)
    check(position=(8, 3))
    offer("Rental_Text_LilyDecor")
    key(A)
    assert inspect()[8] == 1
    for direction in (LEFT, LEFT, DOWN, DOWN, LEFT):
        step(direction)
    assert inspect()[6]
    capture("Cove-Lily-Studio")
    for direction in (LEFT, DOWN, DOWN):
        step(direction)
    core.step(160, 0)
    check(LILY_FLOOR, 3100, 1, (6, 2))
    step(UP)
    key(A, 180)
    check(LILY_ROOM, 3100, 1)
    write(2, 1 + 6 * 16)
    assert inspect()[-1] == 0x291

    load(2)
    capture("Mauville-Hills-Exterior")
    step(UP)
    core.step(100, 0)
    check(HILLS_LOBBY)
    load(4)
    step(UP)
    check(HILLS_LOBBY, 3100, 1, (6, 2))
    key(A, 80)
    message("Rental_Text_MauvilleLocked")
    capture("Mauville-Hills-Locked")
    key(A)
    load(3)
    offer("Rental_Text_MauvilleOffer", has_intro=True)
    capture("Mauville-Hills-One-Time-Rent")
    key(A, 85)
    message("Rental_Text_MauvillePaid")
    key(A, 70)
    key(A, 70)
    check(HILLS_LOBBY, 0, 3)

    load(4)
    key(A, 180)
    check(HILLS_ROOM, 0, 3, (3, 6))
    for _ in range(3):
        step(UP)
    check(position=(3, 3))
    write(2, 3 + 2 * 16)
    assert inspect()[-1] == 0x008
    key(A, 80)
    message("Text_BootUpPC")
    assert inspect()[-1] == 0x009
    capture("Mauville-PC-Boot")
    key(A, 100)
    capture("Mauville-PC-Menu")
    key(DOWN)
    key(DOWN)
    key(A, 85)
    assert inspect()[-1] == 0x008
    capture("Mauville-PC-Closed")
    assert core.rd(main + 4) == sy["CB2_Overworld"] | 1
    for _ in range(4):
        step(RIGHT)
    command(3)
    check(position=(7, 3))
    offer("Rental_Text_MauvilleDecor")
    key(A)
    assert inspect()[8] == 3
    step(DOWN)
    step(DOWN)
    capture("Mauville-Hills-Apartment")
    for direction in (DOWN, LEFT, LEFT, LEFT, DOWN):
        step(direction)
    core.step(160, 0)
    check(HILLS_LOBBY, 0, 3)
    step(UP)
    key(A, 180)
    check(HILLS_ROOM, 0, 3)
    write(2, 8 + 6 * 16)
    assert inspect()[-1] == 0x236
    command(4)
    assert read(12)
    flags_offset, pos_offset = read(16), read(17)
    battery = OUTPUT / "private-apartment.sav"
    assert core.battery(bytes(battery))

    core.init.argtypes = core.load_battery.argtypes = [c_char_p]
    assert core.init(bytes(rom))
    assert core.load_battery(bytes(battery))
    core.reset()
    core.step(500, 0)
    for _ in range(50):
        if core.rd(main + 4) == sy["CB2_Overworld"] | 1:
            break
        key(A, 150)
    assert core.rd(main + 4) == sy["CB2_Overworld"] | 1
    core.step(180, 0)
    saveblock = core.rd(sy["gSaveBlock1Ptr"])
    flags_address = saveblock + flags_offset
    flags_byte = (core.rd(flags_address & ~3) >> (8 * (flags_address & 3))) & 0xff
    assert flags_byte & 0x3c == 0x3c
    assert core.rd(saveblock + pos_offset) == 3 | (6 << 16)
    capture("Mauville-Hills-Continued")
    step(DOWN)
    core.step(160, 0)
    saveblock = core.rd(sy["gSaveBlock1Ptr"])
    assert core.rd(saveblock + pos_offset) == 6 | (2 << 16), hex(core.rd(saveblock + pos_offset))
    step(UP)
    key(A, 220)
    saveblock = core.rd(sy["gSaveBlock1Ptr"])
    assert core.rd(saveblock + pos_offset) == 3 | (6 << 16), hex(core.rd(saveblock + pos_offset))
    battery.unlink()
except Exception:
    capture("failure")
    raise

(OUTPUT / "verification.json").write_text(json.dumps({
    "version": Path("VERSION").read_text().strip(),
    "romSha256": sha256(original).hexdigest(),
    "emulator": "mGBA native core",
    "checks": ["blocked doors and independent tenancy", "cancel and insufficient funds",
               "exact debits, including a zero balance", "repeat access without charge",
               "physical Mauville entrance", "party heal", "storage PC with room-specific on/off art",
               "decor after reentry",
               "normal battery Continue"],
}, indent=2) + "\n")
print("PASS: apartment controller and battery scenarios")
