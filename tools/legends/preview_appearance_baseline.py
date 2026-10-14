#!/usr/bin/env python3
"""Render the released appearance compositor without modifying sprite assets."""
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools/legends"))
fixture_path = ROOT / "test/legends-appearance-colors.test.py"
fixture = {"__file__": str(fixture_path)}
# Load the existing real-C renderer and artwork checks, without the test main.
exec(fixture_path.read_text().split("with tempfile.TemporaryDirectory() as temp:", 1)[0], fixture)

version = (ROOT / "VERSION").read_text().strip()
output = ROOT / f"docs/qa/v{version}-sprite-sheet.png"
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans"
regular = ImageFont.truetype(font_path + ".ttf", 16)
small = ImageFont.truetype(font_path + ".ttf", 14)
bold = ImageFont.truetype(font_path + "-Bold.ttf", 22)
sheet = Image.new("RGB", (940, 862), (240, 243, 247))
draw = ImageDraw.Draw(sheet)
ink, muted = (30, 42, 55), (78, 90, 103)
draw.text((28, 22), f"EMERALD: LEGENDS  /  v{version}", font=bold, fill=ink)
draw.text((28, 57), "Existing sprites • Approved smile and body-color repair", font=regular, fill=muted)
for x, label in ((348, "WARDROBE"), (526, "FRONT"), (672, "REAR"), (816, "SIDE")):
    draw.text((x, 96), label, font=small, fill=muted, anchor="mm")

cases = [
    ("Crew Cut", ["Natural hair", "Emerald outfit", "Red shoes"], dict(h=1, col=0, o=0, shoe=1)),
    ("Crew Cut", ["Blond hair", "Emerald outfit", "Red shoes"], dict(h=1, col=6, o=0, shoe=1)),
    ("Tousled", ["Silver hair / deep skin", "Trail / navy coat", "Ocean scarf / black boots"],
     dict(h=5, col=7, tone=3, o=1, coat=1, scarf=2, shoe=7)),
]
with tempfile.TemporaryDirectory() as temp:
    _, render = fixture["compile_api"](temp)
    for index, (title, labels, args) in enumerate(cases):
        y = 122 + index * 232
        draw.rounded_rectangle((20, y, 920, y + 216), radius=8, fill="white", outline=(211, 219, 227))
        draw.text((38, y + 38), title, font=bold, fill=ink)
        for line, label in enumerate(labels):
            draw.text((38, y + 77 + line * 24), label, font=small, fill=muted)
        portrait = render(**args, kind=1)[0].resize((192, 192), Image.Resampling.NEAREST)
        sheet.paste(portrait, (252, y + 12), portrait)
        for pose, center in enumerate((526, 672, 816)):
            world = render(**args, kind=0, state=0, pose=pose)[0]
            world = world.resize((96, 192), Image.Resampling.NEAREST)
            sheet.paste(world, (center - 48, y + 12), world)
draw.text((28, 830), "Actual compiled-C sprite buffers • Wardrobe 3× / overworld 6× • No smoothing or new artwork", font=small, fill=muted)
sheet.save(output)
print(output)
