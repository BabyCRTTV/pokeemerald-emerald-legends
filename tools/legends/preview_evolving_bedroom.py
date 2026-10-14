"""Static owner-review concepts made exclusively from existing game art.

Not emulator captures or implemented room states. Never modifies ROM inputs.
Run from any directory; output is docs/designs/evolving-bedroom/.
"""
from pathlib import Path
import hashlib,json,struct,textwrap
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/designs/evolving-bedroom'
SOURCES=set()
def read(p):
    SOURCES.add(str(p.relative_to(ROOT)));return p.read_bytes()
def source_hash(p):
    data=p.read_bytes()
    if p.suffix=='.pal':data=data.replace(b'\r\n',b'\n')
    return hashlib.sha256(data).hexdigest()
def png(p):
    read(p);return Image.open(p)
class Tiles:
    def __init__(self,primary,secondary,secret=False):
        self.p=ROOT/'data/tilesets'/primary;self.s=ROOT/'data/tilesets'/secondary
        self.pals=[]
        for n in range(16):
            p=(self.p if secret or n<6 else self.s)/f'palettes/{n:02}.pal'
            self.pals.append([tuple(map(int,t.split())) for t in read(p).decode().splitlines()[3:19]])
        self.atl=[png(self.p/'tiles.png'),png(self.s/('red_cave/tiles.png' if secret else 'tiles.png'))]
        self.metas=[read(p/'metatiles.bin') for p in (self.p,self.s)]
    def tile(self,w):
        t=w&1023;atlas=self.atl[t//512];t%=512
        a=atlas.crop((t%16*8,t//16*8,t%16*8+8,t//16*8+8))
        if w&1024:a=a.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if w&2048:a=a.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        out=Image.new('RGBA',(8,8));pal=self.pals[w>>12]
        out.putdata([(*pal[v%16],255 if v%16 else 0) for v in a.get_flattened_data()]);return out
    def meta(self,n,foreground=False):
        words=struct.unpack_from('<8H',self.metas[n//512],n%512*16)
        out=Image.new('RGBA',(16,16),(0,0,0,0 if foreground else 255))
        for i in range(4 if foreground else 0,8):out.alpha_composite(self.tile(words[i]),(i%2*8,(i//2%2)*8))
        return out
HOUSE=Tiles('primary/building','secondary/brendans_mays_house')
DECOR=Tiles('primary/secret_base','secondary/secret_base',True)
OBJECTS={'flowers':[0x2d4,0x2dc],'silver':[0x2d6,0x2de],'gold':[0x32e,0x336],'glass':[0x282,0x28a]}
def prop(im,name,x,y):
    for k,n in enumerate(OBJECTS[name]):im.alpha_composite(DECOR.meta(n,True),(x*16,(y+k)*16))
def room(stage=0,gender='Brendans',theme='memories'):
    data=struct.unpack('<72H',read(ROOT/f'data/layouts/LittlerootTown_{gender}House_2F/map.bin'))
    out=Image.new('RGBA',(144,128))
    for i,v in enumerate(data):out.paste(HOUSE.meta(v&1023),(i%9*16,i//9*16))
    right=gender=='Brendans';edge=8 if right else 0
    if stage>=1:prop(out,'flowers',edge,6)
    if stage>=2 and theme!='cozy':prop(out,'silver' if stage<3 else 'gold',edge,2)
    # Existing native posters stand for completed research reports, not feathers.
    if stage>=4 and theme!='cozy':
        wallx=[1,2,3] if right else [5,6,7]
        photo_x=2 if right else 6
        if stage>=5:
            out.paste(HOUSE.meta(0x254),(photo_x*16,0))
            out.paste(HOUSE.meta(0x276),(photo_x*16,16))
        for i,n in enumerate([0x331,0x333,0x332]):
            if stage>=5 or i==0:
                x=wallx[i];out.alpha_composite(DECOR.meta(n,True),(x*16,8))
    if stage>=6 and theme=='memories':prop(out,'glass',edge,4)
    if theme=='champion' and stage>=3:
        # Richer alternative: two existing shields; not recommended as default.
        prop(out,'silver',edge,4)
    return out.convert('RGB')
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def sheet(name,title,subtitle,cards):
    w=480;h=108+len(cards)*480+28
    out=Image.new('RGB',(w,h),'#f5f0e7');d=ImageDraw.Draw(out)
    d.text((24,18),title,font=ImageFont.truetype(BOLD,23),fill='#46364b')
    for j,line in enumerate(textwrap.wrap(subtitle,53)):d.text((24,52+j*18),line,font=ImageFont.truetype(FONT,13),fill='#685e62')
    for i,(heading,description,img) in enumerate(cards):
        y=108+i*480
        d.rounded_rectangle((12,y-7,468,y+465),12,fill='#ffffff')
        d.text((24,y+3),heading,font=ImageFont.truetype(BOLD,18),fill='#46364b')
        for j,line in enumerate(textwrap.wrap(description,51)):d.text((24,y+32+j*18),line,font=ImageFont.truetype(FONT,14),fill='#625960')
        out.paste(img.resize((432,384),Image.Resampling.NEAREST),(24,y+78))
    out.save(OUT/name)
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    sheet('bedroom-directions.png','A room that remembers','Design concepts / existing Emerald art only. Static compositions, not gameplay captures.',[
      ('A / Home with memories - recommended','Flowers, small awards and travel displays grow around the familiar bedroom.',room(6)),
      ('B / Cozy home','A gentler look: flowers and the original photo. Most memories live in the notebook.',room(6,theme='cozy')),
      ('C / Champion display','A more formal award corner, with gold and silver shields as the main focus.',room(6,theme='champion'))])
    sheet('bedroom-hoenn-stages.png','Growing through Hoenn','Recommended direction / proposed milestones. The notebook retains earlier memories as displays evolve.',[
      ('1 / First steps','First Gym victory: Mom leaves native flowers. The furniture and wardrobe stay in place.',room(1)),
      ('2 / A proud family','Defeat Norman: a silver display marks how far you have come. Mom has new dialogue.',room(2)),
      ('3 / Home of a Champion','Hall of Fame: the award becomes gold. The notebook retains your earlier milestones.',room(3))])
    sheet('bedroom-kanto-stages.png','Memories beyond Hoenn','Continues through the current Kanto finale. Displays represent reports, never capture requirements.',[
      ('4 / Letters from Kanto','First filed Wing Survey report: a native green poster marks the start of your research.',room(4)),
      ('5 / The Wing Survey','Three filed bird reports replace the small photo display. The notebook keeps every earlier memory.',room(5)),
      ('6 / Beyond the horizon','Final report and Birch epilogue: a native glass ornament celebrates the completed voyage.',room(6))])
    sheet('bedroom-both-layouts.png','Both player bedrooms','Final-stage layout concepts. Native room colors, furniture and wardrobe positions are retained.',[
      ('Brendan-layout home','Keepsakes use the outer right edge. The central rug and staircase remain open.',room(6)),
      ('May-layout home','The display mirrors to the outer left edge. The existing wardrobe stays on the right.',room(6,'Mays'))])
    manifest={'base_commit':'ed88772110e0952c9e9c3887f1345ecabd4429c0','status':'Unapproved static design concepts; no ROM implementation','art':'Existing repository game assets only; foreground layers composed with native palettes; no AI or new pixel art','source_hash_normalization':'Palette text uses LF; binary art is hashed verbatim','sources':{p:source_hash(ROOT/p) for p in sorted(SOURCES)},'outputs':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(OUT.glob('*.png'))}}
    (OUT/'preview-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
if __name__=='__main__':main()
