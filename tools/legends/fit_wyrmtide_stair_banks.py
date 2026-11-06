"""Fit native rock end caps around the approved Wyrmtide stair artwork.

Explicit review authoring only. Reject changed baseline maps before any write,
preserving subsequent Porymap work. No stair pixels or movement bits change.
"""
from pathlib import Path
import argparse, hashlib, json, struct

R = Path(__file__).resolve().parents[2]
BASELINE = 'c144f78be5cb8c40be9e2742a54fca9d98de4459'
EXPECTED = {
    'Descent1': '1d7131ab9e66dbde19db4d75aa26943c3bfce0a1',
    'Descent2': '961561388ac368bdee19f436fb5851644c0d09b9',
    'Descent3': 'b9add8edb8761ef87e5d2a15f379fa03af50dbac',
    'Descent4': '4fd63fb375ded29790e99e53ace933e2870eaf69',
}
FLIGHTS = {
    'Descent1': [(12, 9, 2), (5, 15, 2)],
    'Descent2': [(5, 9, 2)],
    'Descent3': [(12, 7, 2), (5, 13, 2)],
    'Descent4': [(8, 7, 3), (8, 13, 3)],
}


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def author(output):
    pending, records = {}, {}
    for key, expected in EXPECTED.items():
        path = R / f'data/layouts/LegendsWyrmtide_{key}/map.bin'
        raw = path.read_bytes()
        assert blob(raw) == expected, f'Preserve changed map and reconcile: {key}'
        cells = list(struct.unpack('<456H', raw))
        before = cells[:]
        affected = []
        for x, y, width in FLIGHTS[key]:
            assert [cells[y * 19 + x + i] & 1023 for i in range(width)] == ([0x3B1, 0x3B2] if width == 2 else [0x3B1, 0x3B5, 0x3B2])
            # Close each independent bank with its native facing end caps.
            # A flat middle-face tile at the cut leaves an exposed floor gap.
            for xx, yy, old, new in [
                (x - 1, y, 0x209, 0x20A),
                (x - 1, y + 1, 0x219, 0x21A),
                (x + width, y, 0x209, 0x208),
                (x + width, y + 1, 0x219, 0x218),
            ]:
                at = yy * 19 + xx
                assert cells[at] & 1023 == old, (key, xx, yy, hex(cells[at]))
                assert cells[at] & 0xC00, 'A bank cheek must remain solid'
                cells[at] = (cells[at] & ~1023) | new
                affected.append([xx, yy, old, new])
        assert all((a & ~1023) == (b & ~1023) for a, b in zip(before, cells)), 'Collision/elevation changed'
        assert all(a == b for a, b in zip(before, cells) if 0x3B1 <= (a & 1023) <= 0x3B8), 'Approved stair cell changed'
        result = struct.pack('<456H', *cells)
        pending[path] = result
        records[key] = {
            'beforeBlob': expected, 'afterBlob': blob(result),
            'changedBankCells': affected, 'stairCellsExact': True,
            'collisionAndElevationExact': True,
        }
    # Validate all four rooms first, then write the bounded edits.
    for path, data in pending.items():
        path.write_bytes(data)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({'baseline': BASELINE, 'rooms': records,
        'sharedArtworkAndStairPixelsChanged': False,
        'scriptsWarpsAndSavedDataChanged': False}, indent=2) + '\n')
    print('Fitted 28 native rock end-cap cells; stairs, collisions and elevations preserved.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--output', type=Path, default=R / 'build/side-joins/authoring.json')
    args = parser.parse_args()
    if not args.apply:
        raise SystemExit('Owner edits protected. --apply explicitly fits this pinned review.')
    author(args.output)
