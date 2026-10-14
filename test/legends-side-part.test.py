"""Freeze the owner-approved head and verify its real C animation buffers."""
import hashlib
import json
import sys
import tempfile
from pathlib import Path

from PIL import Image

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / "tools/legends"))
from preview_side_part import animation, compile_renderer

approval = json.loads((root / "tools/legends/side_part_approval.json").read_text())
heads = approval["reference_heads"]
atlas = Image.open(root / "graphics/legends/male_overworld/heads.png")
untouched = bytes(atlas.getpixel((x, y)) for y in range(320) if not 32 <= y < 64 for x in range(48))
assert hashlib.sha256(untouched).hexdigest() == approval["other_heads_sha256"], "another cut changed"
assert atlas.getpixel((4, 32 + 17)) == 8, "reported front hole returned"
for view, edits in approval["atlas_overrides"].items():
    dx = 0 if view == "front" else 32
    for x, y, value in edits:
        assert atlas.getpixel((dx + x, 32 + y)) == value

with tempfile.TemporaryDirectory() as temp:
    api, render = compile_renderer(temp)
    for pose, reference in enumerate(heads):
        _, pixels, _ = render(h=2, kind=0, pose=pose)
        for y, row in enumerate(reference["pixels"], reference["top"]):
            assert pixels[y] == [int(value, 16) for value in row], (reference["view"], y, "approved head")

    # Native running frames retain the original four ear-rim shade changes;
    # crown/fringe shape must match the same approved head at every step.
    directions = (0, 1, 2, 0, 0, 1, 1, 2, 2) * 2
    for pose, direction in enumerate(directions):
        _, pixels, _ = render(h=2, kind=0, pose=pose)
        reference = heads[direction]

        def matches(dx, dy):
            for y, row in enumerate(reference["pixels"], reference["top"]):
                for x, value in enumerate(map(lambda c: int(c, 16), row)):
                    xx, yy = x + dx, y + dy
                    actual = pixels[yy][xx] if 0 <= xx < 16 and 0 <= yy < 32 else 0
                    if actual == value:
                        continue
                    if pose >= 9 and direction == 0 and (x, y) in ((2, 17), (13, 17), (2, 18), (13, 18)) and actual == 3:
                        continue
                    return False
            return True

        assert any(matches(dx, dy) for dy in range(-4, 5) for dx in range(-2, 3)), (pose, "hair changed between steps")

    for motion in ("Go", "Run"):
        for direction, head in (("South", 0), ("North", 1), ("West", 2), ("East", 2)):
            for pose, ticks, flip in animation(motion + direction):
                assert directions[pose] == head and ticks > 0
                assert flip == (direction == "East")

    verified = 0
    for state in range(8):
        for pose in range(api.Count(0, state)):
            if state == 4:
                native = render(h=0, kind=0, state=state, pose=pose)[0]
                assert native.tobytes() == render(h=2, kind=0, state=state, pose=pose)[0].tobytes()
                continue
            image, pixels, _ = render(h=2, kind=0, state=state, pose=pose)
            digest = hashlib.sha256(bytes([image.width, image.height]) + bytes(v for row in pixels for v in row)).hexdigest()
            assert digest == approval["native_pose_sha256"][f"{state}:{pose}"], (state, pose, "native pose changed")
            verified += 1

    for color in range(8):
        for tone in range(5):
            for pose, reference in ((0, heads[0]), (2, heads[2])):
                image, pixels, palette = render(h=2, col=color, tone=tone, kind=0, pose=pose)
                eye_x = 6 if pose == 0 else 5
                assert pixels[19][eye_x] == 5 and palette[5] == (2 | (4 << 5) | (7 << 10)), "pupil recolored"
                box = (0, reference["top"], 16, reference["top"] + len(reference["pixels"]))
                for outfit, coat, scarf, shoes in ((3, 2, 2, 7), (2, 1, 1, 1)):
                    alternate = render(h=2, col=color, tone=tone, kind=0, pose=pose,
                                       o=outfit, coat=coat, scarf=scarf, shoe=shoes)[0]
                    assert image.crop(box).tobytes() == alternate.crop(box).tobytes(), "wardrobe changed head"

print(f"Approved Side Part head + fixed cell; 18 walk/run frames, {verified} field poses, eyes, colors and wardrobes passed")
