#!/usr/bin/env python3
"""Export the real C avatar buffers using native walking/running commands."""
import math
import re
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[2]
BG = (178, 167, 236)
INK = (24, 25, 47)


def compile_renderer(directory, shade=True):
    path = ROOT / "test/legends-appearance-colors.test.py"
    fixture = {"__file__": str(path)}
    exec(path.read_text().split("# Artwork preservation:", 1)[0], fixture)
    return fixture["compile_api"](directory, shade=shade)


def animation(name):
    source = (ROOT / "src/data/object_events/object_event_anims.h").read_text()
    body = re.search(r"sAnim_" + name + r"\[\]\s*=\s*\{(.*?)\};", source, re.S)[1]
    assert "ANIMCMD_JUMP(0)" in body
    return [(int(frame), int(ticks), bool(re.search(r"hFlip\s*=\s*TRUE", flags)))
            for frame, ticks, flags in re.findall(r"ANIMCMD_FRAME\((\d+),\s*(\d+)([^)]*)\)", body)]


def mobile(render, poses, title):
    canvas = Image.new("RGB", (360, 1140), BG)
    draw = ImageDraw.Draw(canvas)
    regular = ImageFont.truetype("DejaVuSans.ttf", 14)
    heading = ImageFont.truetype("DejaVuSans.ttf", 23)
    label = ImageFont.truetype("DejaVuSans.ttf", 19)

    def center(text, y, font):
        width = draw.textbbox((0, 0), text, font=font)[2]
        draw.text(((360 - width) // 2, y), text, fill=INK, font=font)

    center(title, 17, heading)
    center("Approved Side Part + repaired ear pixel", 50, regular)
    center("Native C sprite buffers", 73, regular)
    for index, ((pose, flip), name) in enumerate(zip(poses, ("Front", "Back", "Left", "Right"))):
        y = 110 + 255 * index
        center(name, y, label)
        image = render(h=2, kind=0, pose=pose)[0].crop((0, 6, 16, 32))
        if flip:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        image = image.resize((128, 208), Image.Resampling.NEAREST)
        canvas.paste(image, (116, y + 28), image)
    return canvas


def main():
    version = (ROOT / "VERSION").read_text().strip()
    output = ROOT / "docs/qa"
    with tempfile.TemporaryDirectory() as temp:
        api, render = compile_renderer(temp)
        static = mobile(render, [(0, False), (1, False), (2, False), (2, True)], f"Side Part · v{version}")
        static.save(output / f"side-part-v{version}-mobile.png")
        images, durations = [], []
        for motion, repeats, label in (("Go", 3, "Walking"), ("Run", 5, "Running")):
            sequences = [animation(motion + direction) for direction in ("South", "North", "West", "East")]
            assert len({len(sequence) for sequence in sequences}) == 1
            for _ in range(repeats):
                for step in range(len(sequences[0])):
                    poses = [(sequence[step][0], sequence[step][2]) for sequence in sequences]
                    assert len({sequence[step][1] for sequence in sequences}) == 1
                    images.append(mobile(render, poses, f"Side Part · {label}"))
                    durations.append(max(10, round(sequences[0][step][1] * 1000 / 60 / 10) * 10))
        images[0].save(output / f"side-part-v{version}-motion.gif", save_all=True,
                       append_images=images[1:], duration=durations, loop=0, disposal=2)

        names = ("Walking/running", "Mach Bike", "Acro Bike", "Surf", "Dive", "Field move", "Fishing", "Watering")
        cases = [(state, pose) for state in range(8) if state != 4 for pose in range(api.Count(0, state))]
        sheet = Image.new("RGB", (1088, 40 + math.ceil(len(cases) / 8) * 162), BG)
        draw = ImageDraw.Draw(sheet)
        draw.text((12, 10), "Side Part / every native non-diving descriptor / real C buffers", fill=INK)
        for index, (state, pose) in enumerate(cases):
            image = render(h=2, kind=0, state=state, pose=pose)[0]
            x = index % 8 * 136
            y = 40 + index // 8 * 162
            draw.text((x + 3, y), f"{names[state]} {pose}", fill=INK)
            scaled = image.resize((image.width * 4, 128), Image.Resampling.NEAREST)
            sheet.paste(scaled, (x + (136 - scaled.width) // 2, y + 22), scaled)
        sheet.save(output / f"side-part-v{version}-all-poses.png")
    print(f"Wrote mobile PNG, native-command walking/running GIF and {len(cases)}-pose sheet for v{version}")


if __name__ == "__main__":
    main()
