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
    atlas=Image.open(base);original=atlas.copy()
    native=ROOT/'data/tilesets/secondary/fallarbor'
    metas=(ROOT/'data/tilesets/legends_lights/fallarbor_metatiles.bin').read_bytes()
    assert len(metas)==(FIRST-0x200)*16
    words=struct.unpack('<%dH'%(len(metas)//2),metas)
    wall=list(struct.unpack_from('<8H',metas,(0x22A-0x200)*16))
    overlay=Image.new('P',(16,32),0);overlay.putpalette(atlas.getpalette())
    primary=Image.open(ROOT/'data/tilesets/legends_lights/general_tiles.png')
    def tile(t):
        source=primary if t<512 else atlas
        if t>=512:t-=512
        return source.crop((t%16*8,t//16*8,t%16*8+8,t//16*8+8))
    # Start with the exact two native cliff-face overlays, preserving the
    # original surface texture outside the new aperture.
    for row in range(4):
        for col in range(2):overlay.paste(tile(wall[4+(row%2)*2+col]&1023),(col*8,row*8))
    p=overlay.load()
    # Oblique aperture: its near edge is hidden behind an irregular projecting
    # rock cheek. The upper lip is offset, rather than a symmetrical front arch.
    edges={9:(12,14),10:(11,14),11:(11,15),12:(10,15),13:(10,15),
           14:(9,15),15:(9,15),16:(9,15),17:(8,15),18:(8,15),
           19:(8,15),20:(8,15),21:(8,15),22:(8,15),23:(9,15),
           24:(9,15),25:(10,15),26:(10,14),27:(11,14)}
    for y,(left,right) in edges.items():
        for x in range(left,right+1):p[x,y]=8  # native deep cave shade
        p[left-1,y]=14                       # near rock's occluding edge
        if y in [10,12,14,17,23,25]:p[left-2,y]=13
        # A dim angled inner face on the far side, fading into the cavity.
        if 12<=y<=25:p[right,y]=13 if y<19 else 7
        if 16<=y<=23:p[right-1,y]=7
    # A short rock cap and broken highlight support the overhang's volume.
    for x,y,v in [(11,8,13),(12,8,14),(13,8,14),(14,8,13),
                  (10,10,12),(9,12,13),(8,14,12),(7,17,13),
                  (8,24,13),(9,26,14),(10,27,13)]:p[x,y]=v
    # A small receding threshold: narrow at the rear, opening toward the landing.
    for x,y,v in [(11,28,14),(12,28,13),(13,28,7),(14,28,13),(15,28,13),
                  (12,29,13),(13,29,12),(14,29,12),(15,29,13),
                  (14,30,13),(15,30,14)]:p[x,y]=v
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
        for i in range(4):m[4+i]=0xB000|free[half*4+i]
        new.extend(m)
    atlas.save(OUT/'fallarbor_cliff_tiles.png')
    (OUT/'fallarbor_cliff_metatiles.bin').write_bytes(metas+struct.pack('<16H',*new))
    attrs=(native/'metatile_attributes.bin').read_bytes()
    (OUT/'fallarbor_cliff_attributes.bin').write_bytes(attrs+struct.pack('<2H',0x1000,0x1000))
    # Standalone editable source uses the exact palette and transparent index 0.
    colors=[tuple(map(int,l.split())) for l in (native/'palettes/11.pal').read_text().splitlines()[3:19]]
    overlay.putpalette([c for rgb in colors for c in rgb]+[0]*(768-48))
    overlay.save(OUT/'cliff_recess_overlay.png',transparency=0)
    spec={'resolution':[16,32],'palette':11,'metatiles':[FIRST,FIRST+1],'tile_ids':free,
          'base_atlas_sha256':hashlib.sha256(base.read_bytes()).hexdigest(),
          'base_metatiles_sha256':hashlib.sha256(metas).hexdigest(),
          'base_attributes_sha256':hashlib.sha256(attrs).hexdigest(),
          'style':'Asymmetric rock lip, near occlusion, shadowed cavity, dim far inner wall, diagonal threshold',
          'authoring':'Indexed native tile overlay; existing palette and every pixel outside the eight free tile cells are unchanged.'}
    (OUT/'custom_cliff.json').write_text(json.dumps(spec,indent=2)+'\n')
    return spec
if __name__=='__main__':build()
