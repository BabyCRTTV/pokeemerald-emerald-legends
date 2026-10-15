"""Verify native scroll frames and create a lossless, phone-sized GIF."""
from pathlib import Path
import argparse
import collections
import csv
import hashlib
import json
from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--captures', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    offsets = [int(row['offset']) for row in csv.DictReader((args.captures / 'scroll.csv').open())]
    limit = max(offsets)
    assert offsets[0] == offsets[-1] == 0 and limit > 0
    moves = [i for i in range(1, len(offsets)) if offsets[i] != offsets[i - 1]]
    assert len(moves) == 2 * limit
    assert [offsets[i] - offsets[i - 1] for i in moves] == [1] * limit + [-1] * limit
    paths = sorted(path for path in args.captures.glob('scroll-*.rgba') if path.stem[7:].isdigit())
    assert len(paths) == (len(offsets) + 2) // 3
    frames = [Image.frombytes('RGBA', (240, 160), path.read_bytes()).convert('RGB') for path in paths]
    # Exact native pixels outside the moving 96x60 body remain unchanged.
    fixed = [(0, 0, 112, 20), (0, 20, 8, 80), (104, 20, 112, 80),
             (0, 80, 112, 88), (136, 8, 232, 152)]
    for frame in frames:
        for box in fixed:
            assert frame.crop(box).tobytes() == frames[0].crop(box).tobytes(), box
    assert frames[-1].crop((0, 0, 112, 88)).tobytes() == frames[0].crop((0, 0, 112, 88)).tobytes()
    previews = []
    for frame in frames:
        preview = Image.new('RGB', (480, 354), '#201c28')
        draw = ImageDraw.Draw(preview)
        draw.fontmode = '1'
        draw.text((12, 10), 'Long-text test - native game capture', fill='#fff4d9')
        preview.paste(frame.resize((480, 320), Image.Resampling.NEAREST), (0, 34))
        previews.append(preview)
    # A shared exact palette avoids GIF quantization/dither changes.
    colors = sorted(set().union(*(set(frame.getdata()) for frame in previews)))
    assert len(colors) <= 256
    palette = [value for color in colors for value in color] + [0] * (768 - 3 * len(colors))
    reference = Image.new('P', (1, 1)); reference.putpalette(palette)
    encoded = [frame.quantize(palette=reference, dither=Image.Dither.NONE) for frame in previews]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    encoded[0].save(args.output, save_all=True, append_images=encoded[1:], duration=50, loop=0, optimize=False)
    # GIF coalesces identical frames; check the decoded image and full timeline.
    decoded = Image.open(args.output)
    index = 0
    for n in range(decoded.n_frames):
        decoded.seek(n)
        repeat = decoded.info['duration'] // 50
        assert repeat > 0
        for _ in range(repeat):
            assert decoded.convert('RGB').tobytes() == previews[index].tobytes()
            index += 1
    assert index == len(previews)
    proof = {
        'native_frames_checked': len(offsets), 'native_images_checked': len(frames),
        'scroll_limit_pixels': limit, 'one_pixel_moves': len(moves),
        'native_move_interval_frames': dict(collections.Counter(b - a for a, b in zip(moves, moves[1:]))),
        'fixed_header_frame_and_menu_pixels': True, 'returned_to_identical_card': True,
        'GIF_decoded_frames': decoded.n_frames, 'GIF_timeline_frames_verified': index,
        'GIF_SHA256': hashlib.sha256(args.output.read_bytes()).hexdigest(),
        'scale': '2x nearest neighbor, exact native pixels; caption outside game',
        'fixture': 'Synthetic oversized objective in a private controlled Debug ROM; game quest text unchanged.',
    }
    args.output.with_suffix('.verification.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(json.dumps(proof, indent=2))


if __name__ == '__main__':
    main()
