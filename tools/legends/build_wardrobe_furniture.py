"""Build a native indexed 16x32 wooden cabinet in unused tiles/metatile slots."""
from pathlib import Path
import struct,json
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]

def cabinet(indices):
    dark,shadow,wood,light=indices
    p=Image.new('P',(16,32),0)
    for y in range(2,31):
        for x in range(1,15):
            v=dark if x in (1,14) or y in (2,30) else shadow if x in (2,13) or y in (3,29) else wood
            if x in (4,11) and 6<=y<=26:v=light
            if x in (7,8):v=dark
            if y in (15,16) and x in (6,9):v=light
            p.putpixel((x,y),v)
    for x in (2,3,12,13):p.putpixel((x,31),dark)
    return p

def build():
    paths=[('primary/secret_base','secondary/secret_base',324,464,3,(12,11,10,9)),('secondary/brendans_mays_house','secondary/brendans_mays_house',196,480,None,None)]
    for art,meta,count,first,pal,indices in paths:
        directory=ROOT/'data/tilesets'/art;target=ROOT/'data/tilesets'/meta
        atlas=Image.open(directory/'tiles.png')
        if pal is None:
            targets=[(49,32,24),(115,73,32),(172,115,57),(222,172,98)]
            best=None
            for n in range(6,13):
                colors=[tuple(map(int,x.split())) for x in (directory/f'palettes/{n:02}.pal').read_text().splitlines()[3:]]
                ramp=[min(range(1,16),key=lambda i:sum((colors[i][k]-c[k])**2 for k in range(3))) for c in targets]
                score=sum(sum((colors[i][k]-c[k])**2 for k in range(3)) for c,i in zip(targets,ramp))
                if best is None or score<best[0]:best=(score,n,ramp)
            _,pal,indices=best
            extended=Image.new('P',(128,248),0);extended.putpalette(atlas.getpalette());extended.paste(atlas.crop((0,0,128,240)),(0,0));atlas=extended
        p=cabinet(indices)
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
        for y,tile in [(6,0x2c4),(7,0x2c5)]:struct.pack_into('<H',data,(y*9+x)*2,0xc00|tile)
        f.write_bytes(data)
        f=ROOT/'data/maps'/name/'map.json';j=json.loads(f.read_text());j['bg_events']=[e for e in j['bg_events'] if e.get('script')!='LegendsWardrobe_EventScript_Home']
        for y in (6,7):j['bg_events'].append({'type':'sign','x':x,'y':y,'elevation':0,'player_facing_dir':'BG_EVENT_PLAYER_FACING_ANY','script':'LegendsWardrobe_EventScript_Home'})
        f.write_text(json.dumps(j,indent=2)+'\n')
if __name__=='__main__':build()
