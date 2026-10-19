#!/usr/bin/env python3
"""Compose phone-sized v0.0.65 previews from verified native mGBA captures only."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,hashlib,json,collections
p=argparse.ArgumentParser();p.add_argument('captures',type=Path);a=p.parse_args()
R=Path(__file__).resolve().parents[2];O=R/'docs/qa';proof=json.loads((a.captures/'verification.json').read_text())
assert proof['passed'] and proof['version']=='0.0.65' and len(proof['scenarios'])==102
native={x['map']:x for x in json.loads((R/'src/data/wild_encounters.json').read_text())['wild_encounter_groups'][0]['encounters']}
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',10);bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',11)
colors=['#d6ebce','#f5e4ae','#edceb7','#d7e7ef'];seasons=['Spring','Summer','Autumn','Winter'];records=[]
def frame(index,name,suffix='gui'):
 f=a.captures/f'scene-{index:02d}-{suffix}.png';im=Image.open(f).convert('RGB');assert im.size==(240,160)
 records.append(dict(preview=name,frame=f.name,scene=index,sha256=hashlib.sha256(f.read_bytes()).hexdigest()));return im

def title(im,label):
 d=ImageDraw.Draw(im);d.fontmode='1'
 for y,t,f in [(4,'Emerald: Legends v0.0.65',bold),(21,label,font),(37,'Native mGBA / controlled fixtures',font)]:
  assert d.textbbox((0,0),t,font=f)[2]<=228,t;d.text((6,y),t,font=f,fill='white')
 return d

def panels(name,label,items):
 im=Image.new('RGB',(240,62+214*len(items)),'#182c27');d=title(im,label)
 for n,index in enumerate(items):
  s=proof['scenarios'][index];water=s['area']==1;method='Surf' if water else 'desert' if s['route']==111 else 'grass'
  base=native[f'MAP_ROUTE{s["route"]}']['water_mons' if water else 'land_mons'];residents={x['species'] for x in base['mons']};odds=collections.Counter()
  for species,rate in zip(s['expected'],[60,30,5,4,1] if water else [20,20,10,10,10,10,5,5,4,4,1,1]):odds[species]+=rate
  visitors=sorted(((rate,species.removeprefix('SPECIES_').replace('_',' ').title()) for species,rate in odds.items() if species not in residents),reverse=True)
  assert len(visitors)==2;y=62+214*n;d.rectangle((0,y,239,y+47),fill=colors[s['season']])
  lines=[f'Route {s["route"]} / {seasons[s["season"]]} / {method}']+[f'{rate}% {species}' for rate,species in visitors]
  for j,t in enumerate(lines):
   assert d.textbbox((0,0),t,font=font)[2]<=228,t;d.text((6,y+2+14*j),t,font=font,fill='#182c27')
  capture=frame(index,name);im.paste(capture,(0,y+48));assert im.crop((0,y+48,240,y+208)).tobytes()==capture.tobytes()
 im.resize((480,im.height*2),Image.Resampling.NEAREST).save(O/name)

for route in range(109,113):
 indexes=[i for i,s in enumerate(proof['scenarios']) if s['route']==route and s['mode']==2]
 assert len(indexes)==4;panels(f'route-{route}-seasonal-v0.0.65-preview.png',f'Route {route} / all four seasons',indexes)
panels('seasonal-routes-v0.0.65-preview.png','Next routes / silhouettes and known icons',[68,95])
name='seasonal-routes-v0.0.65-preview.gif';frames=[]
for suffix in ['gui','animated']:
 im=Image.new('RGB',(240,222),'#182c27');title(im,'Route 109 / Spring / native silhouettes');im.paste(frame(68,name,suffix),(0,62));frames.append(im.resize((480,444),Image.Resampling.NEAREST))
frames[0].save(O/name,save_all=True,append_images=frames[1:],duration=500,loop=0,optimize=False)
gif=Image.open(O/name);assert gif.n_frames==2
for i,suffix in enumerate(['gui','animated']):
 gif.seek(i);expected=Image.open(a.captures/f'scene-68-{suffix}.png').convert('RGB').resize((480,320),Image.Resampling.NEAREST)
 assert gif.convert('RGB').crop((0,124,480,444)).tobytes()==expected.tobytes()
(O/'seasonal-routes-v0.0.65-previews.json').write_text(json.dumps(dict(version=proof['version'],ROM_sha256=proof['base_ROM_sha256'],capture_source='Actual compiled Legends Debug ROM in mGBA native core; controlled fixtures',scale='2x nearest-neighbor; exact native pixels with captions outside gameplay',animation='Two native states with illustrative 500ms timing, not a continuous recording',frames=records),indent=2)+'\n')
print('Created four all-season route sheets, narrow summary, native-frame GIF and exact-pixel provenance.')
