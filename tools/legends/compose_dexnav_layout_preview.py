#!/usr/bin/env python3
"""Compose phone-friendly previews from two verified native mGBA artifacts."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,json,hashlib
p=argparse.ArgumentParser();p.add_argument('before',type=Path);p.add_argument('after',type=Path);args=p.parse_args()
R=Path(__file__).resolve().parents[2];O=R/'docs/qa';proof=json.loads((args.after/'verification.json').read_text());before=json.loads((args.before/'verification.json').read_text());records=[]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10);head=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',11)
colors=['#d6ebce','#f5e4ae','#edceb7','#d7e7ef'];seasons=['Spring','Summer','Autumn','Winter']
visitors={101:['Scatterbug / Fletchling','Sunkern / Hoppip','Sentret / Tarountula','Skwovet / Rookidee'],102:['Budew / Azurill','Surskit / Tympole','Sewaddle / Smoliv','Wooper / Ducklett'],103:['Pidove / Bunnelby','Buizel / Wattrel','Nidoran F / Nickit','Spheal / Lillipup'],104:['Caterpie / Cutiefly','Fomantis / Ledyba','Autumn Deerling / Shroomish','Snorunt / Alolan Sandshrew']}
def record(name,directory,index,suffix='gui'):
 f=directory/f'scene-{index:02d}-{suffix}.png';im=Image.open(f).convert('RGB');assert im.size==(240,160)
 records.append(dict(preview=name,frame=f.name,artifact='before' if directory==args.before else 'after',sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
 return im

def title(im,text):
 d=ImageDraw.Draw(im);d.fontmode='1'
 for y,line,f in [(4,'Emerald: Legends v0.0.63 preview',head),(21,text,font),(37,'Native mGBA / controlled fixtures',font)]:
  assert d.textbbox((0,0),line,font=f)[2]<=228,line
  d.text((6,y),line,font=f,fill='white')
 return d

def panels(name,text,items):
 im=Image.new('RGB',(240,62+198*len(items)),'#182c27');d=title(im,text)
 for i,(directory,index,line1,line2,color) in enumerate(items):
  y=62+198*i;d.rectangle((0,y,239,y+31),fill=color)
  for j,line in enumerate([line1,line2]):
   assert d.textbbox((0,0),line,font=font)[2]<=228,line
   d.text((6,y+2+14*j),line,font=font,fill='#182c27')
  im.paste(record(name,directory,index),(0,y+32))
 im.resize((480,im.height*2),Image.Resampling.NEAREST).save(O/name)

panels('dexnav-layout-v0.0.63-preview.png','Corrected sizing and centering',[(args.before,17,'Before - Route 104 / Winter','Original native capture',colors[3]),(args.after,17,'After - Route 104 / Winter','Centered art; wide icons fitted',colors[3]),(args.after,16,'After - Route 101 / Spring','Silhouettes use the same placement',colors[0]),(args.after,28,'After - Route 103 / Summer','Small species keep native size',colors[1])])
for route in range(101,105):
 panels(f'route-{route}-seasonal-v0.0.63-centered-preview.png',f'Route {route} - discovered land icons',[(args.after,19+(route-101)*4+s,seasons[s]+' - seasonal visitors',visitors[route][s],colors[s]) for s in range(4)])
name='dexnav-layout-v0.0.63-preview.gif';frames=[]
for suffix in ['gui','animated']:
 im=Image.new('RGB',(240,222),'#182c27');title(im,'Route 104 - Winter / corrected icons');im.paste(record(name,args.after,15,suffix),(0,62));frames.append(im.resize((480,444),Image.Resampling.NEAREST))
frames[0].save(O/name,save_all=True,append_images=frames[1:],duration=500,loop=0,optimize=False)
# Confirm GIF quantization did not change a single native gameplay pixel.
gif=Image.open(O/name);assert gif.n_frames==2
for i,suffix in enumerate(['gui','animated']):
 gif.seek(i);original=Image.open(args.after/f'scene-15-{suffix}.png').convert('RGB').resize((480,320),Image.Resampling.NEAREST)
 assert gif.convert('RGB').crop((0,124,480,444)).tobytes()==original.tobytes()
manifest=dict(version='0.0.63',capture_source='Actual compiled Legends Debug ROM in mGBA native core; controlled diagnostic fixtures',before_ROM_sha256=before['base_ROM_sha256'],after_ROM_sha256=proof['base_ROM_sha256'],scale='2x nearest-neighbor, exact native pixels; captions outside gameplay',animation='Two genuine native states at illustrative 500ms intervals; not a continuous recording',frames=records)
(O/'dexnav-layout-v0.0.63-previews.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Created five narrow PNGs, exact-pixel native-frame GIF and provenance.')
