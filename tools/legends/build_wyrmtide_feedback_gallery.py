"""Export verified native game frames at exact nearest-neighbor scale."""
from pathlib import Path
import argparse,hashlib,json,shutil
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();src=a.native.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
proof=json.loads((src/'verification.json').read_text());assert proof['passed'] and not proof['scenesOnly']
exports={'33-recessed-upper-passage':'Upper-Passage','34-south-exit-approach':'Lower-Exit','35-large-regidrago':'Regidrago-Large','36-sanctuary-exit':'Sanctuary-Exit','44-rare-dragon-encounter':'Rare-Bagon','40-tidal-lore':'Tidal-Inscription','42-deep-lore':'Deep-Inscription','38-threshold-lore':'Threshold-Inscription'}
for native,name in exports.items():
 original=src/(native+'.png');assert hashlib.sha256(original.read_bytes()).hexdigest()==proof['images'][original.name]
 im=Image.open(original).convert('RGB');scaled=im.resize((960,640),Image.Resampling.NEAREST);path=out/(name+'.png');scaled.save(path)
 assert Image.open(path).resize((240,160),Image.Resampling.NEAREST).tobytes()==im.tobytes()
for group,names in [('Passages',['Upper-Passage','Lower-Exit']),('Inscriptions',['Threshold-Inscription','Tidal-Inscription','Deep-Inscription'])]:
 sheet=Image.new('RGB',(720*len(names),480),(0,0,0))
 for i,name in enumerate(names):sheet.paste(Image.open(out/(name+'.png')).resize((720,480),Image.Resampling.NEAREST),(i*720,0))
 sheet.save(out/(group+'.png'))
strip=Image.new('RGB',(960,576))
for i,native in enumerate(['38-threshold-lore','40-tidal-lore','42-deep-lore']):
 strip.paste(Image.open(src/(native+'.png')).convert('RGB').crop((0,112,240,160)).resize((960,192),Image.Resampling.NEAREST),(0,i*192))
strip.save(out/'Inscriptions-Text.png')
for name in ['33-recessed-upper-passage','34-south-exit-approach','35-large-regidrago','44-rare-dragon-encounter']:shutil.copyfile(src/(name+'.png'),out/(name+'.png'))
(out/'gallery.json').write_text(json.dumps({'version':proof['version'],'ROM_sha256':proof['ROM_sha256'],'nativeSource':proof['emulator'],'RGBExactScaling':True,'rarePreview':'Production generation from the live 4% Bagon slot with a controlled seed; actual walking encounters independently verified on all four floors.','images':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')}},indent=2)+'\n')
print('PASS native RGB-exact feedback gallery: '+str(out))
