"""Append review-only cliff entrances assembled from unchanged native 8x8 tiles.

No existing tiles, palettes, metatiles or map references are replaced. The native
QA harness stages the three alternatives at Stillwater for owner comparison.
"""
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
BASE_COUNT = 367
FIRST_ID = 0x200 + BASE_COUNT

def build():
    root = ROOT/'data/tilesets/secondary/fallarbor'
    path = root/'metatiles.bin'
    original = path.read_bytes()[:BASE_COUNT * 16]
    def meta(n): return list(struct.unpack_from('<8H', original, (n-0x200)*16))
    wall, top, bottom = meta(0x22A), meta(0x259), meta(0x261)
    def cleft(source):
        out=wall[:]
        for i in [1,3]: out[i]=source[i];out[i+4]=0xB000
        return out
    a_top,a_bottom=cleft(top),cleft(bottom)
    # Keep the whole upper wall above a lower, sheltered slit.
    b_top=wall[:]
    c_bottom=bottom[:]
    # Retain the rock's upper-left corner, opening into a wider lower recess.
    c_bottom[0]=wall[0];c_bottom[4]=wall[4]
    variants=[a_top,a_bottom,b_top,a_bottom,a_top,c_bottom]
    data=original+b''.join(struct.pack('<8H',*m) for m in variants)
    attrs=root/'metatile_attributes.bin'
    attr_data=attrs.read_bytes()[:BASE_COUNT*2]+struct.pack('<6H',*[0]*6)
    # The active tileset points at the existing night-light derivative. Its
    # accepted prefix stays byte-identical; these non-window cells need no
    # lighting transformation and share the same native tile/palette words.
    active=ROOT/'data/tilesets/legends_lights/fallarbor_metatiles.bin'
    active_data=active.read_bytes()[:BASE_COUNT*16]+data[BASE_COUNT*16:]
    for p,data in [(path,data),(attrs,attr_data),(active,active_data)]:
        if p.read_bytes()!=data:p.write_bytes(data)
    return variants

if __name__=='__main__':build()
