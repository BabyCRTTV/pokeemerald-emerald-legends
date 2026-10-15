"""Capture the actual OPTION card using a locally built ROM and mGBA 0.10.2."""
from pathlib import Path
import argparse,subprocess,os,json,hashlib
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--release',action='store_true');args=p.parse_args()
 out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);prefix=args.prefix.resolve();env=os.environ.copy();env['PATH']=str(prefix/'bin')+':'+env['PATH'];env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 stem='pokeemerald-release' if args.release else 'pokeemerald';variant='Release' if args.release else 'Debug'
 nm=subprocess.check_output(['arm-none-eabi-nm',stem+'.elf'],cwd=ROOT,env=env,text=True)
 symbols={ps[2]:int(ps[0],16) for line in nm.splitlines() if len(ps:=line.split())==3}
 src=Path(__file__).resolve().parent
 with (out/'compile.log').open('w') as f:subprocess.run(['cc',str(src/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 names=['gMain','CB2_InitMainMenu','gTasks','Task_DisplayMainMenu','gSaveBlock2Ptr','gSaveFileStatus','Task_HandleMainMenuInput']
 with (out/'emulator.log').open('w') as f:subprocess.run([str(out/'host'),str(ROOT/(stem+'.gba')),str(out),*[hex(symbols[n]) for n in names]],env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 for raw in out.glob('*.rgba'):Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(out/(raw.stem+'.png'))
 # Exact ink bounds verify matching native font baselines in all layouts.
 bounds={}
 for layout,top in enumerate([40,104,136,136]):
  selected=Image.open(out/('layout-%d-selected.png'%layout));pixels=selected.load()
  ink=lambda x,y:pixels[x,y]==(99,99,99)
  left=[(x,y) for y in range(top,top+16) for x in range(16,100) if ink(x,y)]
  right=[(x,y) for y in range(top,top+16) for x in range(110,224) if ink(x,y)]
  assert left and right
  a=[min(y for x,y in left),max(y for x,y in left)]
  b=[min(y for x,y in right),max(y for x,y in right)]
  assert a==b and max(x for x,y in right)<224
  bounds[str(layout)]={'OPTION':a,'version':b,'version_rightmost_pixel':max(x for x,y in right)}
  if layout<2:assert selected.tobytes()==Image.open(out/('layout-%d-options-return.png'%layout)).tobytes()
 font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
 sheet=Image.new('RGB',(480,708),(34,29,40));draw=ImageDraw.Draw(sheet)
 for i,state in enumerate(['unselected','selected']):
  draw.text((12,i*354+8),variant+' — OPTION '+state,font=font,fill='white')
  sheet.paste(Image.open(out/('layout-0-'+state+'.png')).resize((480,320),Image.Resampling.NEAREST),(0,i*354+30))
 sheet.save(out/('option-card-'+variant.lower()+'.png'))
 receipt={'state':'Unpublished preview; owner review required','base_version':(ROOT/'VERSION').read_text().strip(),'variant':variant,'ROM_sha256':hashlib.sha256((ROOT/(stem+'.gba')).read_bytes()).hexdigest(),'emulator':'mGBA 0.10.2','controlled_setup':'Native main-menu initialization; RAM selects the four original layout states. No ROM injection or saved layout changes. Empty/saved native input enters Options and returns. Mystery layouts are controlled rendering cases, not full event progression.','layout_pixel_bounds':bounds,'options_return_matches_selected_scene':True,'log':(out/'emulator.log').read_text(),'images':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(out.glob('*.png'))}}
 (out/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
