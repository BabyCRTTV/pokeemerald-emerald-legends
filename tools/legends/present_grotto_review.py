"""Label and nearest-neighbor enlarge existing mGBA frames for phone review."""
from pathlib import Path
import json
import shutil
from PIL import Image, ImageDraw, ImageFont

R = Path(__file__).resolve().parents[2]
SOURCE = R/'build/grotto-review'
OUT = R/'docs/designs/hidden-grottos'
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

def text(im, xy, value, size=16, bold=False, color='#efe9da'):
    ImageDraw.Draw(im).text(xy,value,font=ImageFont.truetype(BOLD if bold else FONT,size),fill=color)

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    proof = json.loads((SOURCE/'verification.json').read_text())
    assert proof['seasonal_scenes']==12
    for name in proof['images']:
        shutil.copyfile(SOURCE/name, OUT/name)
    shutil.copyfile(SOURCE/'verification.json', OUT/'verification.json')
    shutil.copyfile(SOURCE/'emulator.log', OUT/'emulator.log')
    sheet = Image.new('RGB',(480,1208),'#282831')
    text(sheet,(16,12),'HIDDEN GROTTOS',24,True)
    text(sheet,(16,45),'First playable concept - unpublished review',14)
    text(sheet,(16,66),'v0.0.68 + prototype | native mGBA captures',12)
    for i,(name,route) in enumerate([('Leafshade Hollow','Petalburg Woods'),('Stillwater Nook','Route 114'),('Rainroot Hollow','Route 119')]):
        y=100+i*368
        text(sheet,(16,y),name,19,True)
        text(sheet,(16,y+25),route,12)
        frame=Image.open(SOURCE/f'room-{i}-season-0-overview.png')
        assert frame.size==(240,160)
        sheet.paste(frame.resize((480,320),Image.Resampling.NEAREST),(0,y+44))
    sheet.save(OUT/'Emerald-Legends-Hidden-Grottos-Preview.png')
    frames=[]
    for season,(name,visitor) in enumerate([('Spring','Morelull'),('Summer','Tropius'),('Autumn','Goomy'),('Winter','Swablu')]):
        card=Image.new('RGB',(480,384),'#282831')
        text(card,(14,9),'RAINROOT HOLLOW',18,True)
        text(card,(14,34),f'{name} - {visitor} | unshipped review',14)
        card.paste(Image.open(SOURCE/f'room-2-season-{season}-overview.png').resize((480,320),Image.Resampling.NEAREST),(0,64))
        frames.append(card)
    frames[0].save(OUT/'Emerald-Legends-Grotto-Seasons.gif',save_all=True,append_images=frames[1:],duration=1800,loop=0,disposal=2)
    print(OUT)

if __name__=='__main__':main()
