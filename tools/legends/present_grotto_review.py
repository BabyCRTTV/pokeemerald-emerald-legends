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
    text(sheet,(16,45),'Compact habitats - unpublished review',14)
    text(sheet,(16,66),'v0.0.68 + prototype | native mGBA captures',12)
    for i,(name,route) in enumerate([('Leafshade Hollow','Petalburg Woods'),('Stillwater Nook','Route 114'),('Rainroot Hollow','Route 119')]):
        y=100+i*368
        text(sheet,(16,y),name,19,True)
        text(sheet,(16,y+25),route,12)
        frame=Image.open(SOURCE/f'room-{i}-season-0-overview.png')
        assert frame.size==(240,160)
        sheet.paste(frame.resize((480,320),Image.Resampling.NEAREST),(0,y+44))
    sheet.save(OUT/'Emerald-Legends-Grottos-Compact-Preview.png')
    entrances=Image.new('RGB',(480,1208),'#282831')
    text(entrances,(16,12),'FINDING THE ENTRANCES',22,True)
    text(entrances,(16,47),'Approach the opening and press A',15)
    text(entrances,(16,71),'v0.0.68 + review | actual mGBA frames',12)
    for i,(name,place) in enumerate([('Vine-framed trunk','Southern Petalburg Woods'),('Rock crevice','Route 114'),('Gap in the undergrowth','Lower Route 119')]):
        y=100+i*368
        text(entrances,(16,y),name,19,True)
        text(entrances,(16,y+25),place,12)
        entrances.paste(Image.open(SOURCE/f'room-{i}-season-0-entrance.png').resize((480,320),Image.Resampling.NEAREST),(0,y+44))
    entrances.save(OUT/'Emerald-Legends-Grotto-Entrances.png')
    frames=[]
    for season,(name,visitor) in enumerate([('Spring','Morelull'),('Summer','Tropius'),('Autumn','Goomy'),('Winter','Swablu')]):
        card=Image.new('RGB',(480,384),'#282831')
        text(card,(14,9),'RAINROOT HOLLOW',18,True)
        text(card,(14,34),f'{name} - {visitor} | unshipped review',14)
        card.paste(Image.open(SOURCE/f'room-2-season-{season}-overview.png').resize((480,320),Image.Resampling.NEAREST),(0,64))
        frames.append(card)
    frames[0].save(OUT/'Emerald-Legends-Rainroot-Grass-Fix.png')
    frames[0].save(OUT/'Emerald-Legends-Grotto-Seasons.gif',save_all=True,append_images=frames[1:],duration=1800,loop=0,disposal=2)
    discovery=[]
    for path in sorted(SOURCE.glob('discovery-*.png')):
        card=Image.new('RGB',(480,384),'#282831')
        text(card,(14,8),'FINDING LEAFSHADE HOLLOW',19,True)
        text(card,(14,35),'Walk up, examine the vines, choose Yes',14)
        card.paste(Image.open(path).resize((480,320),Image.Resampling.NEAREST),(0,64))
        discovery.append(card)
    assert len(discovery)==proof['discovery_film_frames']>40
    # A shared palette permits small delta frames, keeping the real walk clip
    # convenient to open/save on a phone. Source PNGs retain exact native RGB.
    palette_source=Image.new('RGB',(120*8,96*((len(discovery)+7)//8)))
    for i,frame in enumerate(discovery):
        palette_source.paste(frame.resize((120,96),Image.Resampling.NEAREST),(i%8*120,i//8*96))
    palette=palette_source.quantize(colors=256,method=Image.Quantize.MEDIANCUT)
    compact=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in discovery]
    compact[0].save(OUT/'Emerald-Legends-Grotto-Discovery.gif',save_all=True,append_images=compact[1:],duration=100,loop=0,disposal=1,optimize=True)
    print(OUT)

if __name__=='__main__':main()
