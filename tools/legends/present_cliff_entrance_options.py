"""Present exact native mGBA option frames and nearest-neighbor detail crops."""
from pathlib import Path
import json,shutil
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
SOURCE=R/'build/grotto-review'
OUT=R/'docs/designs/hidden-grottos/cliff-options'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
def text(im,xy,value,size=14,bold=False):
    ImageDraw.Draw(im).text(xy,value,font=ImageFont.truetype(BOLD if bold else FONT,size),fill='#efe9da')
def main():
    proof=json.loads((SOURCE/'verification.json').read_text())
    assert len(proof['entrance_options'])==3
    OUT.mkdir(exist_ok=True,parents=True)
    for name in list(proof['entrance_options'])+list(proof['images']):shutil.copyfile(SOURCE/name,OUT/name)
    for name in ['verification.json','emulator.log']:shutil.copyfile(SOURCE/name,OUT/name)
    detail=Image.new('RGB',(576,288),'#282831')
    text(detail,(14,10),'SIDE-FACING CLIFF ENTRANCES',20,True)
    text(detail,(14,37),'v0.0.68 review | native mGBA crops, 3× pixels',12)
    world=Image.new('RGB',(480,1208),'#282831')
    text(world,(16,12),'STILLWATER: ENTRANCE OPTIONS',20,True)
    text(world,(16,45),'v0.0.68 review | actual native mGBA frames',12)
    text(world,(16,66),'Same landing and interaction; current map unchanged',12)
    for i,label in enumerate(['A · Narrow cleft','B · Low opening','C · Angled recess']):
        frame=Image.open(SOURCE/f'entrance-option-{i}.png');assert frame.size==(240,160)
        text(detail,(i*192+8,66),label,14,True)
        # Capture is centered on player (14,40); include both mouth cells,
        # the landing and adjacent cliff. No pixel painting or synthetic scene.
        detail.paste(frame.crop((80,48,144,112)).resize((192,192),Image.Resampling.NEAREST),(i*192,92))
        y=100+i*368
        text(world,(16,y),label,19,True)
        text(world,(16,y+25),'Walk to the landing and examine the mouth',12)
        world.paste(frame.resize((480,320),Image.Resampling.NEAREST),(0,y+44))
    detail.save(OUT/'Emerald-Legends-Cliff-Options.png')
    world.save(OUT/'Emerald-Legends-Cliff-Options-World.png')
    print(OUT)
if __name__=='__main__':main()
