#!/usr/bin/env python3
"""Compose narrow Surf rosters using only verified native Legends frames."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse, hashlib, json
p=argparse.ArgumentParser();p.add_argument('captures',type=Path);a=p.parse_args()
R=Path(__file__).resolve().parents[2];O=R/'docs/qa';proof=json.loads((a.captures/'verification.json').read_text())
assert proof['passed'] and proof['version']=='0.0.64' and len(proof['scenarios'])==68
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10);bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',11)
colors=['#d6ebce','#f5e4ae','#edceb7','#d7e7ef'];seasons=['Spring','Summer','Autumn','Winter'];records=[]
def frame(index,name,suffix='gui'):
 f=a.captures/f'scene-{index:02d}-{suffix}.png';im=Image.open(f).convert('RGB');assert im.size==(240,160)
 records.append(dict(preview=name,frame=f.name,scene=index,sha256=hashlib.sha256(f.read_bytes()).hexdigest()));return im

def title(im,label):
 d=ImageDraw.Draw(im);d.fontmode='1'
 for y,t,f in [(4,'Emerald: Legends v0.0.64',bold),(21,label,font),(37,'Native mGBA / controlled fixtures',font)]:
  assert d.textbbox((0,0),t,font=f)[2]<=228,t;d.text((6,y),t,font=f,fill='white')
 return d

def label(mon):return mon.removeprefix('SPECIES_').replace('_',' ').title()
def panels(name,label_text,items):
 im=Image.new('RGB',(240,62+198*len(items)),'#182c27');d=title(im,label_text)
 for n,index in enumerate(items):
  s=proof['scenarios'][index];y=62+198*n;d.rectangle((0,y,239,y+31),fill=colors[s['season']])
  lines=[f'Route {s["route"]} / {seasons[s["season"]]} / Surf',f'30% {label(s["expected"][1])} / 5% {label(s["expected"][2])}']
  for j,t in enumerate(lines):
   assert d.textbbox((0,0),t,font=font)[2]<=228,t;d.text((6,y+2+14*j),t,font=font,fill='#182c27')
  im.paste(frame(index,name),(0,y+32))
 im.resize((480,im.height*2),Image.Resampling.NEAREST).save(O/name)

for route in range(105,109):
 indexes=[i for i,s in enumerate(proof['scenarios']) if s['route']==route and s['mode']==2]
 assert len(indexes)==4
 panels(f'route-{route}-seasonal-surf-v0.0.64-preview.png',f'Route {route} / seasonal Surf visitors',indexes)
name='seasonal-surf-v0.0.64-preview.png';panels(name,'Native silhouettes and discovered icons',[35,66])
name='seasonal-surf-v0.0.64-preview.gif';frames=[]
for suffix in ['gui','animated']:
 im=Image.new('RGB',(240,222),'#182c27');title(im,'Route 105 / Spring / native silhouettes');im.paste(frame(35,name,suffix),(0,62));frames.append(im.resize((480,444),Image.Resampling.NEAREST))
frames[0].save(O/name,save_all=True,append_images=frames[1:],duration=500,loop=0,optimize=False)
gif=Image.open(O/name);assert gif.n_frames==2
for i,suffix in enumerate(['gui','animated']):
 gif.seek(i);expected=Image.open(a.captures/f'scene-35-{suffix}.png').convert('RGB').resize((480,320),Image.Resampling.NEAREST)
 assert gif.convert('RGB').crop((0,124,480,444)).tobytes()==expected.tobytes()
(O/'seasonal-surf-v0.0.64-previews.json').write_text(json.dumps(dict(version=proof['version'],ROM_sha256=proof['base_ROM_sha256'],capture_source='Actual compiled Legends Debug ROM in mGBA native core; controlled Surf fixtures',scale='2x nearest-neighbor, exact native pixels, captions outside gameplay',animation='Two native states with illustrative 500ms timing; not a continuous recording',frames=records),indent=2)+'\n')
print('Created four all-season route sheets, narrow summary, native-frame GIF and exact-pixel provenance.')
