"""Frame verified native captures; never synthesize or repaint gameplay pixels."""
from pathlib import Path
import argparse,hashlib,json,shutil
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--captures',type=Path,required=True);a=p.parse_args();src=a.captures.resolve();out=R/'docs/designs/wyrmtide/astra-redesign';out.mkdir(parents=True,exist_ok=True)
proof=json.loads((src/'verification.json').read_text());assert proof['passed'] and not proof['scenesOnly'];assert proof['ROM_sha256']==hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest()
rows=[('02-island-landing','THE HIDDEN SHORE'),('03-ancient-seal','THE RUINED COURT'),('04-stair-descent','HALL OF THE MAKER'),('05-second-landing','THE DROWNED GALLERY'),('07-fourth-landing','THE LAST PROCESSION'),('08-slumbering-regidrago','THE SLEEPING HEART')]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',18);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
sheet=Image.new('RGB',(1000,1160),'#14232a');d=ImageDraw.Draw(sheet);d.text((20,14),'WYRMTIDE ISLE  /  ISLAND & TOMB REDESIGN',font=font,fill='#e1ce94');d.text((20,42),'v0.0.70 + unshipped review | Actual native mGBA frames',font=small,fill='#aabec4')
for i,(name,label) in enumerate(rows):
 path=src/(name+'.png');assert hashlib.sha256(path.read_bytes()).hexdigest()==proof['images'][path.name];shutil.copy2(path,out/path.name);x=12+i%2*494;y=84+i//2*350;d.text((x,y),label,font=font,fill='#e1ce94');im=Image.open(path);assert im.size==(240,160);sheet.paste(im.resize((480,320),Image.Resampling.NEAREST),(x,y+27))
d.text((20,1140),'Existing game art. Exact gameplay pixels enlarged 2x. Controlled review fixtures.',font=small,fill='#aabec4');sheet.save(out/'Wyrmtide-Redesign.png');shutil.copy2(src/'verification.json',out/'verification.json')
proof['design']='Stepped headland, ruined entrance court, complete tablet monuments, four distinct stair landings, twin shafts and a raised final dais.'
proof['sourceScope']='Only the six unshipped Wyrmtide maps and sibling tileset; published map IDs, quest state and original artwork unchanged.'
proof['nativeArt']='Exact General 0xAF stone-step pixels/flips use the existing Cave palette 6; appended ordinary and warp treads at 0x39F/0x39E. No pixel or palette files edited.'
proof['gallery_sha256']=hashlib.sha256((out/'Wyrmtide-Redesign.png').read_bytes()).hexdigest();proof['releaseBuild']='in progress';proof['patchVerification']='pending candidate CI';(R/'docs/qa/wyrmtide-redesign.json').write_text(json.dumps(proof,indent=2)+'\n')
print(out/'Wyrmtide-Redesign.png')
