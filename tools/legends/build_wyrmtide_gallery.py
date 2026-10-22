"""Frame verified native captures; never synthesize or repaint gameplay pixels."""
from pathlib import Path
import argparse,hashlib,json,shutil
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--captures',type=Path,required=True);a=p.parse_args();src=a.captures.resolve();out=R/'docs/designs/wyrmtide/hoenn-review';out.mkdir(parents=True,exist_ok=True)
proof=json.loads((src/'verification.json').read_text());assert proof['passed'] and not proof['scenesOnly'];assert proof['ROM_sha256']==hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest()
rows=[('02-island-landing','THE SHELTERED SHORE'),('23-open-headland-entrance','THE HEADLAND TEMPLE'),('04-stair-descent','THE MAKER’S HALL'),('05-second-landing','THE TIDAL STAIR'),('06-third-landing','THE MEMORIAL SWITCHBACK'),('07-fourth-landing','THE LAST PROCESSION'),('03-ancient-seal','ONLY THE MAKER CAN OPEN IT'),('08-slumbering-regidrago','THE SLEEPING HEART')]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
sheet=Image.new('RGB',(1000,1530),'#14232a');d=ImageDraw.Draw(sheet);d.text((20,14),'WYRMTIDE ISLE  /  HOENN DESIGN REVIEW',font=font,fill='#e1ce94');d.text((20,42),'v0.0.70 + unshipped review | Actual native mGBA frames | 22 October 2026',font=small,fill='#aabec4')
for i,(name,label) in enumerate(rows):
 path=src/(name+'.png');assert hashlib.sha256(path.read_bytes()).hexdigest()==proof['images'][path.name];shutil.copy2(path,out/path.name);x=12+i%2*494;y=84+i//2*350;d.text((x,y),label,font=font,fill='#e1ce94');im=Image.open(path);assert im.size==(240,160);sheet.paste(im.resize((480,320),Image.Resampling.NEAREST),(x,y+27))
d.text((20,1500),'Existing game art. Exact gameplay pixels enlarged 2x. Controlled review fixtures.',font=small,fill='#aabec4');sheet.save(out/'Wyrmtide-Redesign.png');shutil.copy2(src/'verification.json',out/'verification.json')
proof['design']='Dewford shore with a pink-rock Regi facade, two weathered columns, three low inscription ledges, thick native cave walls, four traversable stair landings and an axial dragon sanctuary.'
proof['sourceScope']='Six unshipped Wyrmtide layouts, sibling tilesets and native facade opening cells. Published IDs, save structures and quest state retain their values and behavior.'
proof['nativeArt']='Exact Cave 0x396 stone stairs use the existing palette 7 at 0x39E/39F. Shore retains every used Dewford pixel, all native metatiles and animation cells. Eight appended inscription/column cells copy existing Cave pixels into unused sibling slots; native Cave palette 6 occupies Dewford’s unused palette 6. Original shared artwork and palette files are untouched.'
proof['gallery_sha256']=hashlib.sha256((out/'Wyrmtide-Redesign.png').read_bytes()).hexdigest();proof['releaseBuild']='in progress';proof['patchVerification']='pending candidate CI';(R/'docs/qa/wyrmtide-hoenn-review.json').write_text(json.dumps(proof,indent=2)+'\n')
print(out/'Wyrmtide-Redesign.png')
