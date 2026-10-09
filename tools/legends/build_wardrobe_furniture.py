"""Reuse Emerald’s closed storage box in the wardrobe’s reserved tiles."""
from pathlib import Path
import struct,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def native_box():
    """Read Emerald's closed moving box, including native tile flips/palette."""
    directory=ROOT/'data/tilesets/secondary/brendans_mays_house'
    words=struct.unpack_from('<8H',(directory/'metatiles.bin').read_bytes(),(0x268-512)*16)
    result=Image.new('P',(16,16),0)
    palettes={}
    for i,word in enumerate(words[4:]):
        tile=word&1023;pal=word>>12
        atlas=Image.open((ROOT/'data/tilesets/primary/building' if tile<512 else directory)/'tiles.png')
        tile%=512
        part=atlas.crop(((tile%16)*8,(tile//16)*8,(tile%16+1)*8,(tile//16+1)*8))
        if word&1024:part=part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if word&2048:part=part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        result.paste(part,((i%2)*8,(i//2)*8))
        palettes[pal]=[tuple(map(int,line.split())) for line in (directory/f'palettes/{pal:02}.pal').read_text().splitlines()[3:]]
    assert len(palettes)==1
    return result,next(iter(palettes.values())),words

def build():
    paths=[('primary/secret_base','secondary/secret_base',324,464,3,(12,11,10,9)),('secondary/brendans_mays_house','secondary/brendans_mays_house',196,480,None,None)]
    for art,meta,count,first,pal,indices in paths:
        directory=ROOT/'data/tilesets'/art;target=ROOT/'data/tilesets'/meta
        atlas=Image.open(directory/'tiles.png')
        box,colors,words=native_box()
        p=Image.new('P',(16,32),0)
        if pal is None:
            pal=words[4]>>12
            extended=Image.new('P',(128,248),0);extended.putpalette(atlas.getpalette());extended.paste(atlas.crop((0,0,128,240)),(0,0));atlas=extended
            p.paste(box,(0,0))
        else:
            target_colors=[tuple(map(int,line.split())) for line in (directory/f'palettes/{pal:02}.pal').read_text().splitlines()[3:]]
            remap={0:0,**{i:min(range(1,16),key=lambda n:sum((target_colors[n][k]-colors[i][k])**2 for k in range(3))) for i in range(1,16)}}
            for y in range(16):
                for x in range(16):p.putpixel((x,y),remap[box.getpixel((x,y))])
        for i in range(8):
            tile=p.crop(((i%2)*8,(i//2)*8,(i%2+1)*8,(i//2+1)*8))
            atlas.paste(tile,(((first+i)%16)*8,((first+i)//16)*8))
        atlas.save(directory/'tiles.png',bits=4)
        data=(target/'metatiles.bin').read_bytes()[:count*16]
        attrs=(target/'metatile_attributes.bin').read_bytes()[:count*2]
        if 'secret_base' in meta:
            floor=struct.unpack_from('<4H',data,(0x2f4-512)*16)
        else:floor=struct.unpack_from('<4H',data,(0x201-512)*16)
        for half in range(2):
            cells=[(pal<<12)+first+half*4+i+(512 if 'brendans' in art else 0) for i in range(4)]
            data+=struct.pack('<8H',*floor,*cells);attrs+=struct.pack('<H',0x1000)
        (target/'metatiles.bin').write_bytes(data);(target/'metatile_attributes.bin').write_bytes(attrs)
    labels=ROOT/'include/constants/metatile_labels.h';s=labels.read_text()
    if 'METATILE_SecretBase_LegendsWardrobe_Top' not in s:
        s=s.replace('\n#endif // GUARD_METATILE_LABELS_H','\n#define METATILE_SecretBase_LegendsWardrobe_Top 0x344\n#define METATILE_SecretBase_LegendsWardrobe_Bottom 0x345\n#define METATILE_BrendansMaysHouse_LegendsWardrobe_Top 0x2C4\n#define METATILE_BrendansMaysHouse_LegendsWardrobe_Bottom 0x2C5\n\n#endif // GUARD_METATILE_LABELS_H')
    labels.write_text(s)
    for gender,x in [('Brendans',1),('Mays',7)]:
        name='LittlerootTown_'+gender+'House_2F'
        f=ROOT/'data/layouts'/name/'map.bin';data=bytearray(f.read_bytes())
        for y,tile in [(6,0xc00|0x2c4),(7,0x201)]:struct.pack_into('<H',data,(y*9+x)*2,tile)
        f.write_bytes(data)
        f=ROOT/'data/maps'/name/'map.json';j=json.loads(f.read_text());j['bg_events']=[e for e in j['bg_events'] if e.get('script')!='LegendsWardrobe_EventScript_Home']
        for y in (6,):j['bg_events'].append({'type':'sign','x':x,'y':y,'elevation':0,'player_facing_dir':'BG_EVENT_PLAYER_FACING_ANY','script':'LegendsWardrobe_EventScript_Home'})
        f.write_text(json.dumps(j,indent=2)+'\n')
if __name__=='__main__':build()
