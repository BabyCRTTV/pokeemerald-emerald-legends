"""Present the custom recess using actual compiled-ROM mGBA captures only."""
from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'build/grotto-review'
OUT=ROOT/'docs/designs/hidden-grottos/custom-cliff'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def text(im,xy,s,size=14,bold=False):
    ImageDraw.Draw(im).text(xy,s,font=ImageFont.truetype(BOLD if bold else FONT,size),fill='#efe9da')
def main():
    p=json.loads((SRC/'verification.json').read_text())
    assert p['seasonal_scenes']==12 and p['cliff_approach_film_frames']>40
    OUT.mkdir(parents=True,exist_ok=True)
    for name in list(p['images'])+list(p['entrance_options'])+['verification.json','emulator.log']:
        shutil.copyfile(SRC/name,OUT/name)
    old=Image.open(SRC/'entrance-option-0.png')
    new=Image.open(SRC/'room-1-season-0-exit.png')
    assert old.size==new.size==(240,160)
    sheet=Image.new('RGB',(512,730),'#282831')
    text(sheet,(14,10),'CUSTOM CLIFF RECESS',22,True)
    text(sheet,(14,40),'v0.0.68 review | actual native mGBA captures',12)
    text(sheet,(12,68),'A · previous cleft',16,True)
    text(sheet,(268,68),'Custom recess',16,True)
    for i,frame in enumerate([old,new]):
        sheet.paste(frame.crop((80,48,144,112)).resize((256,256),Image.Resampling.NEAREST),(i*256,92))
    text(sheet,(16,365),'In the world · landing and access preserved',14,True)
    sheet.paste(new.resize((480,320),Image.Resampling.NEAREST),(16,394))
    sheet.save(OUT/'Emerald-Legends-Custom-Cliff-Preview.png')
    film=[]
    for file in sorted(SRC.glob('cliff-*.png')):
        frame=Image.new('RGB',(480,384),'#282831')
        text(frame,(14,9),'CUSTOM RECESS · REAL WALK-IN',18,True)
        text(frame,(14,36),'v0.0.68 review | native mGBA: approach, inspect, enter',11)
        frame.paste(Image.open(file).resize((480,320),Image.Resampling.NEAREST),(0,64))
        film.append(frame)
    assert len(film)==p['cliff_approach_film_frames']
    atlas=Image.new('RGB',(960,96*((len(film)+7)//8)))
    for i,frame in enumerate(film):atlas.paste(frame.resize((120,96),Image.Resampling.NEAREST),(i%8*120,i//8*96))
    pal=atlas.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    frames=[f.quantize(palette=pal,dither=Image.Dither.NONE) for f in film]
    frames[0].save(OUT/'Emerald-Legends-Custom-Cliff-Walk-In.gif',save_all=True,append_images=frames[1:],duration=100,loop=0,disposal=1,optimize=True)
    print(OUT)
if __name__=='__main__':main()
