"""Pair approved grotto exteriors/interiors from current native mGBA captures."""
from pathlib import Path
import hashlib,json,shutil
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2]
SRC=ROOT/'build/grotto-review'
OUT=ROOT/'docs/designs/hidden-grottos/approved-overview'
FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
PLACES=[('Leafshade Hollow','Petalburg Woods','Vine-framed trunk beside the southern Trainer Tips sign'),
        ('Stillwater Nook','Route 114','Cliff recess southwest of Lanette’s house'),
        ('Rainroot Hollow','Route 119','Undergrowth northwest of the small southern house')]
def text(im,xy,value,size=16,bold=False):
    ImageDraw.Draw(im).text(xy,value,font=ImageFont.truetype(BOLD if bold else FONT,size),fill='#efe9da')
def main():
    p=json.loads((SRC/'verification.json').read_text())
    assert p['ROM_sha256']==hashlib.sha256((ROOT/'pokeemerald.gba').read_bytes()).hexdigest()
    OUT.mkdir(parents=True,exist_ok=True)
    sheet=Image.new('RGB',(960,1304),'#282831')
    text(sheet,(18,12),'APPROVED HIDDEN GROTTOS',27,True)
    text(sheet,(18,47),'Current prototype · v0.0.68 review ROM · actual native mGBA captures',15)
    text(sheet,(18,77),'EXTERIOR',16,True);text(sheet,(498,77),'INTERIOR · SPRING',16,True)
    evidence={}
    for i,(name,route,landmark) in enumerate(PLACES):
        y=110+i*396
        text(sheet,(18,y),f'{name} · {route}',24,True)
        text(sheet,(18,y+32),landmark,16)
        frames=[]
        for label in ['exit','overview']:
            filename=f'room-{i}-season-0-{label}.png'
            digest=hashlib.sha256((SRC/filename).read_bytes()).hexdigest()
            assert p['images'][filename]==digest
            frame=Image.open(SRC/filename);assert frame.size==(240,160)
            frames.append(frame)
            shutil.copyfile(SRC/filename,OUT/filename);evidence[filename]=digest
        for col,frame in enumerate(frames):sheet.paste(frame.resize((480,320),Image.Resampling.NEAREST),(col*480,y+65))
        pair=Image.new('RGB',(480,786),'#282831')
        text(pair,(14,10),name,23,True)
        text(pair,(14,42),f'{route} | v0.0.68 review | native mGBA',12)
        text(pair,(14,68),'OUTSIDE',15,True);pair.paste(frames[0].resize((480,320),Image.Resampling.NEAREST),(0,94))
        text(pair,(14,432),'INSIDE · SPRING',15,True);pair.paste(frames[1].resize((480,320),Image.Resampling.NEAREST),(0,458))
        pair.save(OUT/f'Emerald-Legends-{name.split()[0]}-Inside-Outside.png')
    sheet.save(OUT/'Emerald-Legends-Grottos-Inside-Outside.png')
    receipt={'approval':'Owner: Excellent work, approved.','date':'2026-10-21','source_commit':'ecd005983f4d8835da6b93b7d430a7331831a870',
             'ROM_sha256':p['ROM_sha256'],'emulator':p['emulator'],'capture_setup':p['setup'],
             'presentation':'Exact current native Spring frames, labels outside gameplay, nearest-neighbor 2× enlargement',
             'images':evidence,'status':'Visuals approved. Exploration prototype remains unshipped; capture/reward/refresh persistence is unfinished.'}
    prior=OUT/'approval-and-capture-receipt.json'
    if prior.exists():
        accepted=json.loads(prior.read_text())
        for key in ['approved_visual_sha256','entrances']:
            if key in accepted:receipt[key]=accepted[key]
        for path,sha in receipt.get('approved_visual_sha256',{}).items():
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==sha, 'Approved art changed: '+path
    (OUT/'approval-and-capture-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(OUT)
if __name__=='__main__':main()
