"""Private bedroom extension: native art only, no changes to shared source assets."""
from pathlib import Path
import struct,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/tilesets/legends_bedroom'
def build():
    src=ROOT/'data/tilesets/secondary/brendans_mays_house'
    decor=ROOT/'data/tilesets/secondary/secret_base'
    art=ROOT/'data/tilesets/primary/secret_base'
    OUT.mkdir(parents=True,exist_ok=True)
    atlas=Image.open(src/'tiles.png');extended=Image.new('P',(128,256),0);extended.putpalette(atlas.getpalette());extended.paste(atlas,(0,0))
    data=bytearray((src/'metatiles.bin').read_bytes());attrs=bytearray((src/'metatile_attributes.bin').read_bytes())
    used={w&1023 for w in struct.unpack('<'+'H'*(len(data)//2),data)}
    free=iter(n for n in range(512,1024) if n not in used)
    source_atlas=Image.open(art/'tiles.png');cache={}
    def imported(w):
        tile=w&1023;assert tile<512
        if tile not in cache:
            new=next(free);part=source_atlas.crop((tile%16*8,tile//16*8,tile%16*8+8,tile//16*8+8));extended.paste(part,((new-512)%16*8,(new-512)//16*8));cache[tile]=new
        # Four private native decoration palettes; 1/2 remain rug/bed.
        pal={0:5,1:11,2:4,3:3,4:5,5:12}[w>>12]
        return cache[tile]|(w&0xc00)|(pal<<12)
    # Isolate rug and blanket palette references without changing artwork.
    for n in list(range(0x298,0x2ae)):
        words=list(struct.unpack_from('<8H',data,(n-512)*16))
        words=[(w&0xfff)|0x1000 if w>>12==6 else w for w in words]
        struct.pack_into('<8H',data,(n-512)*16,*words)
    for ns,pal in [([0x283,0x284,0x285,0x28b,0x28c,0x28d],7),([0x288,0x289,0x28a,0x290,0x291,0x292],10)]:
        for n in ns:
            words=list(struct.unpack_from('<8H',data,(n-512)*16));words=[(w&0xfff)|0x2000 if w>>12==pal else w for w in words];struct.pack_into('<8H',data,(n-512)*16,*words)
    objects={};native=(decor/'metatiles.bin').read_bytes()
    for name,ns in {'FLOWERS':[0x2d4,0x2dc],'SILVER':[0x2d6,0x2de],'GOLD':[0x32e,0x336]}.items():
        objects[name]=len(data)//16+512
        for n in ns:
            base=struct.unpack_from('<8H',data,(0x201-512)*16)
            fg=struct.unpack_from('<8H',native,(n-512)*16)[4:]
            data.extend(struct.pack('<8H',*base[:4],*[imported(w) for w in fg]));attrs.extend(struct.pack('<H',0x1000))
    # Keep the console beneath each poster, including its original lower tiles.
    poster=[imported(w) for w in struct.unpack_from('<8H',native,(0x330-512)*16)[4:]]
    for name,console in [('POSTER_MALE',0x265),('POSTER_FEMALE',0x257)]:
        objects[name]=len(data)//16+512
        for baseid,half in [(0x254,0),(console,1)]:
            base=list(struct.unpack_from('<8H',data,(baseid-512)*16))
            if half==0:base[6:8]=poster[:2]
            else:base[4:6]=poster[2:]
            data.extend(struct.pack('<8H',*base));attrs.extend((src/'metatile_attributes.bin').read_bytes()[(baseid-512)*2:(baseid-511)*2])
    # Compose the existing desk legs into a private background; chair artwork
    # remains a native foreground. The original PC's support is not discarded.
    original=bytearray((src/'metatiles.bin').read_bytes())
    room_palettes=[[tuple(map(int,line.split())) for line in (src/f'palettes/{n:02}.pal').read_text().splitlines()[3:19]] for n in range(16)]
    def native_layer(n,front):
        result=Image.new('RGBA',(16,16),(0,0,0,0 if front else 255))
        words=struct.unpack_from('<8H',original,(n-512)*16)
        for i in range(4 if front else 0,8 if front else 4):
            w=words[i];tile=w&1023;assert tile>=512
            t=atlas.crop(((tile-512)%16*8,(tile-512)//16*8,(tile-512)%16*8+8,(tile-512)//16*8+8))
            if w&1024:t=t.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            if w&2048:t=t.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
            out=Image.new('RGBA',(8,8));pal=room_palettes[w>>12]
            out.putdata([(*pal[v],255 if v else 0) for v in t.get_flattened_data()]);result.alpha_composite(out,(i%2*8,(i//2%2)*8))
        return result
    backgrounds=[];colors=[]
    for n,strip in [(0x262,(0,0,3,16)),(0x261,(13,0,16,16))]:
        bg=native_layer(n,False);fg=native_layer(n,True)
        bg.alpha_composite(fg.crop(strip),strip[:2]);bg=bg.convert('RGB');backgrounds.append(bg)
        for color in bg.get_flattened_data():
            if color not in colors:colors.append(color)
    assert len(colors)<=8
    display=[tuple(map(int,l.split())) for l in (art/'palettes/01.pal').read_text().splitlines()[3:19]]
    display[4:12]=colors+[(0,0,0)]*(8-len(colors))
    colors=display
    (OUT/'chair_backdrop.pal').write_text('JASC-PAL\n0100\n16\n'+''.join('%d %d %d\n'%c for c in colors))
    chair_sources=[0x2b8,0x2b9,0x2ba,0x2c0,0x2c1,0x2c2,0x2c8,0x2c9,0x2ca]
    for name,bg,baseid in zip(['CHAIRS_MALE','CHAIRS_FEMALE'],backgrounds,[0x262,0x261]):
        objects[name]=len(data)//16+512
        bg_words=[]
        indexed=Image.new('P',(16,16));indexed.putpalette([v for c in colors for v in c]+[0]*720)
        indexed.putdata([colors.index(c) for c in bg.get_flattened_data()])
        for i in range(4):
            tile=next(free);part=indexed.crop((i%2*8,i//2*8,i%2*8+8,i//2*8+8));extended.paste(part,((tile-512)%16*8,(tile-512)//16*8));bg_words.append(tile|0xb000)
        for mid in chair_sources:
            fg=struct.unpack_from('<8H',native,(mid-512)*16)[4:]
            data.extend(struct.pack('<8H',*bg_words,*[imported(w) for w in fg]));attrs.extend((src/'metatile_attributes.bin').read_bytes()[(baseid-512)*2:(baseid-511)*2])
    extended.save(OUT/'tiles.png',bits=4);(OUT/'metatiles.bin').write_bytes(data);(OUT/'metatile_attributes.bin').write_bytes(attrs)
    lines=['// Generated by tools/legends/build_bedroom.py; private bedroom assets.','const u32 gLegendsBedroomTiles[] = INCGFX_U32("data/tilesets/legends_bedroom/tiles.png", ".4bpp.fastSmol");','const u16 gLegendsBedroomMetatiles[] = INCBIN_U16("data/tilesets/legends_bedroom/metatiles.bin");','const u16 gLegendsBedroomAttributes[] = INCBIN_U16("data/tilesets/legends_bedroom/metatile_attributes.bin");','const struct Tileset gTileset_LegendsBedroom = { .isCompressed = TRUE, .isSecondary = TRUE, .tiles = gLegendsBedroomTiles, .palettes = gTilesetPalettes_BrendansMaysHouse, .metatiles = gLegendsBedroomMetatiles, .metatileAttributes = gLegendsBedroomAttributes };']
    (ROOT/'src/data/tilesets/legends_bedroom.h').write_text('\n'.join(lines)+'\n')
    (ROOT/'include/legends_bedroom_tiles.h').write_text('// Generated native-asset metatile IDs.\n'+''.join(f'#define BEDROOM_{name} 0x{mid:03X}\n' for name,mid in objects.items()))
    (OUT/'sources.json').write_text(json.dumps({'source':'Native bedroom and Secret Base art','objects':objects,'imported_tiles':len(cache),'private_palette_slots':[1,2,3,4,5,11,12],'original_art_unchanged':True},indent=2)+'\n')
if __name__=='__main__':build()
