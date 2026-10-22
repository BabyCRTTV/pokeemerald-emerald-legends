"""Compare archived and repaired native captures without repainting game pixels."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import argparse,json,hashlib,shutil
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--captures',type=Path,required=True);a=p.parse_args();src=a.captures.resolve();out=R/'docs/designs/wyrmtide/edge-review';out.mkdir(parents=True,exist_ok=True)
proof=json.loads((src/'verification.json').read_text());assert proof['passed'] and not proof['scenesOnly']
assert proof['ROM_sha256']==hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest()
before=R/'docs/designs/wyrmtide/hoenn-review';prior=json.loads((before/'verification.json').read_text())
rows=[('03-ancient-seal','COLUMN BASES ON SAND'),('02-island-landing','INSCRIPTION ROCKS ON THE SHORE'),('05-second-landing','MATCHING POOL CORNERS AND FLOOR'),('04-stair-descent','STAIRS IN THE SURROUNDING STONE PALETTE')]
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',19);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',14)
board=Image.new('RGB',(1000,1560),'#14232a');d=ImageDraw.Draw(board)
d.text((16,14),'WYRMTIDE / TERRAIN BORDER REPAIR',font=font,fill='#e1ce94');d.text((16,43),'Actual native mGBA captures | v0.0.70 + unshipped review | 22 October 2026',font=small,fill='#aabec4')
d.text((12,78),'PREVIOUS REVIEW',font=font,fill='#e1ce94');d.text((506,78),'REPAIRED BORDERS',font=font,fill='#e1ce94')
for row,(name,title) in enumerate(rows):
 y=112+row*352;d.text((16,y),title,font=small,fill='#aabec4')
 for col,folder,receipt in [(0,before,prior),(1,src,proof)]:
  path=folder/(name+'.png');assert hashlib.sha256(path.read_bytes()).hexdigest()==receipt['images'][path.name]
  image=Image.open(path);assert image.size==(240,160)
  board.paste(image.resize((480,320),Image.Resampling.NEAREST),(12+col*494,y+26))
  if col:shutil.copy2(path,out/path.name)
d.text((16,1532),'Archived previous review at left; repaired Debug ROM at right. Exact game pixels enlarged 2x.',font=small,fill='#aabec4');board.save(out/'Native-Border-Comparison.png')
shutil.copy2(src/'08-slumbering-regidrago.png',out/'08-slumbering-regidrago.png');shutil.copy2(src/'verification.json',out/'verification.json')
print(out/'Native-Border-Comparison.png')
