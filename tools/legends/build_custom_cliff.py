"""Author a palette-bound 16x32 recessed cliff overlay in native GBA tiles.

Original graphic pixels, palettes and metatile definitions are preserved. The
custom overlay occupies eight verified-unused tiles in a sibling atlas and two
appended metatiles. Rebuilding is deterministic; no source art is overwritten.
"""
from pathlib import Path
import hashlib,json,re,struct
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/tilesets/legends_grotto'
FIRST=0x375

def build():
    OUT.mkdir(exist_ok=True,parents=True)
    base=ROOT/'data/tilesets/legends_lights/fallarbor_tiles.png'
    atlas=Image.open(base)
    native=ROOT/'data/tilesets/secondary/fallarbor'
    metas=(ROOT/'data/tilesets/legends_lights/fallarbor_metatiles.bin').read_bytes()
    assert len(metas)==(FIRST-0x200)*16
    words=struct.unpack('<%dH'%(len(metas)//2),metas)
    wall=list(struct.unpack_from('<8H',metas,(0x22A-0x200)*16))
    # The native cliff-face quadrants become the backing layer. A separate
    # sparse overlay uses Fallarbor's timber palette, so the gate can keep its
    # wood grain without recoloring the surrounding stone.
    overlay = Image.new('P', (16, 32), 0)
    overlay.putpalette(atlas.getpalette())
    gate = (
        "............ss..",
        ".........ssshhd.",
        "......ssshhwHHd.",
        "...ssshhwHHbbbd.",
        "..shhwHHbbbtnpd.",
        "..sHHbbbtndtnpd.",
        "..dbbtndtndtnpd.",
        "..dntnndtndtbsd.",
        "..dntnndtbsHhbd.",
        "..dntbsHhbbtndd.",
        "..dsHhbbtndtnpd.",
        "..dhbbndtndtnpd.",
        "..dntnndtndtnpd.",
        "..dntnndtndtbd..",
        "..dntnndtbbhbd..",
        "..dntbbbhhbdd...",
        "..dbbhhhbdd.....",
        "..dhhbdd........",
        "..dbdd..........",
    )
    # Sunlit edge, grain, end grain, timber shadows, and two rivets.
    shades = dict(s=6, h=10, w=9, H=11, b=13, d=8, n=7, p=6, t=12)
    for y, row in enumerate(gate, 7):
        for x, mark in enumerate(row):
            if mark != ".":
                overlay.putpixel((x, y), shades[mark])
    # Two iron strap hinges and a latch catch the light on the planked face.
    for x, y in [(3, 14), (4, 14), (5, 13), (3, 20), (4, 20), (5, 19)]:
        overlay.putpixel((x, y), 15)
    for x, y in [(3, 13), (3, 19), (12, 15), (13, 15)]:
        overlay.putpixel((x, y), 14)
    # A broken sill projects toward the grass on the approach side.
    for x, y in [(11, 22), (12, 22), (13, 21), (14, 21), (15, 21)]:
        overlay.putpixel((x, y), 7)
        overlay.putpixel((x, y + 1), 8)
    anim=(ROOT/'src/tileset_anims.c').read_text()
    reserved={v for k in map(int,re.findall(r'NUM_TILES_IN_PRIMARY\s*\+\s*(\d+)',anim)) for v in range(512+k,512+k+16)}
    used={v&1023 for v in words}
    free=[i for i in range(512,1024) if i not in used and i not in reserved][:8]
    assert len(free)==8
    for i,tid in enumerate(free):
        col=i%2;row=i//2
        atlas.paste(overlay.crop((col*8,row*8,col*8+8,row*8+8)),((tid-512)%16*8,(tid-512)//16*8))
    new=[]
    for half in range(2):
        m=wall[:]
        for i in range(4):
            crop_x = i % 2 * 8
            crop_y = (half * 2 + i // 2) * 8
            if overlay.crop((crop_x, crop_y, crop_x + 8, crop_y + 8)).getbbox():
                m[i] = wall[4 + i]
                m[4 + i] = 0x6000 | free[half * 4 + i]
        new.extend(m)
    atlas.save(OUT/'fallarbor_cliff_tiles.png')
    (OUT/'fallarbor_cliff_metatiles.bin').write_bytes(metas+struct.pack('<16H',*new))
    attrs=(native/'metatile_attributes.bin').read_bytes()
    (OUT/'fallarbor_cliff_attributes.bin').write_bytes(attrs+struct.pack('<2H',0x1000,0x1000))
    # Standalone editable source uses the exact palette and transparent index 0.
    colors=[tuple(map(int,l.split())) for l in (native/'palettes/06.pal').read_text().splitlines()[3:19]]
    overlay.putpalette([c for rgb in colors for c in rgb]+[0]*(768-48))
    overlay.save(OUT/'cliff_recess_overlay.png',transparency=0)
    spec={'resolution':[16,32],'palette':6,'metatiles':[FIRST,FIRST+1],'tile_ids':free,
          'base_atlas_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),
          'base_metatiles_sha256':hashlib.sha256(metas).hexdigest(),
          'base_attributes_sha256':hashlib.sha256(attrs).hexdigest(),
          'style':'Weathered slatted timber gate in the east-facing rock cleft',
          'authoring':'Indexed native tile overlay; existing palette and every pixel outside the eight free tile cells are unchanged.'}
    (OUT/'custom_cliff.json').write_text(json.dumps(spec,indent=2)+'\n')
    return spec
if __name__=='__main__':build()
