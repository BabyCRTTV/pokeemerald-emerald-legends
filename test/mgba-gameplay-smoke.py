"""Actual mGBA core smoke test of an unmodified Legends Debug ROM."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "build" / "legends-mgba-preview"
OUTPUT.mkdir(parents=True, exist_ok=True)
ROM = ROOT / "pokeemerald.gba"
ELF = ROOT / "pokeemerald.elf"
assert ROM.is_file() and ELF.is_file(), "Build the Debug ROM and ELF first."
assert ROM.stat().st_size >= 8 * 1024 * 1024, "Unexpectedly small Debug ROM."

symbols = {}
for line in subprocess.check_output(["arm-none-eabi-nm", str(ELF)], text=True).splitlines():
    parts = line.split()
    if len(parts) == 3:
        symbols[parts[2]] = int(parts[0], 16)
assert "gMain" in symbols and "CB2_Overworld" in symbols, "Missing native callback symbols."

subprocess.run(["cc", "-O2", "-std=c11", "-Wno-unused-parameter",
                str(ROOT / "tools/legends/mgba_gameplay_smoke.c"),
                "-lmgba", "-o", str(OUTPUT / "gameplay-smoke")], check=True)

env = os.environ.copy()
result = subprocess.run([str(OUTPUT / "gameplay-smoke"), str(ROM), str(OUTPUT),
                         hex(symbols["gMain"]), hex(symbols["CB2_Overworld"])],
                        cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, timeout=120)
(OUTPUT / "emulator.log").write_text(result.stdout)
if result.returncode:
    raise SystemExit(f"mGBA core exited with code {result.returncode}:\n{result.stdout}")

captures = []
for name in ("living-hoenn-gameplay", "living-hoenn-interaction"):
    raw = OUTPUT / (name + ".rgba")
    data = raw.read_bytes()
    assert len(data) == 240 * 160 * 4, f"Wrong frame buffer size: {len(data)}"
    image = Image.frombytes("RGBA", (240, 160), data).convert("RGB")
    # This checks for a rendered, non-uniform frame, not for a completed quest.
    colors = len(image.getcolors(240 * 160) or [])
    assert colors > 12, f"{name} is suspiciously uniform ({colors} colors)"
    image.save(OUTPUT / (name + ".png"))
    captures.append({"name": name, "colors": colors})

report = {
    "model": "GPT-6 (High)",
    "version": (ROOT / "VERSION").read_text().strip(),
    "emulator": "Ubuntu libmGBA 0.10.x, native core",
    "build": "Debug",
    "rom_sha256": hashlib.sha256(ROM.read_bytes()).hexdigest(),
    "ROM_unmodified": True,
    "RAM_writes_by_test": False,
    "test_scope": "Title SELECT Quickstart -> overworld; two live 240x160 frames",
    "not_tested": "Research dialogue/Weather Institute/Champion conversations through normal save progression, Release run, historical saves and full playthrough.",
    "captures": captures,
}
(OUTPUT / "results.json").write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps(report, indent=2))
