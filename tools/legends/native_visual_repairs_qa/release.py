"""Unmodified Release boot/Continue from private, Debug-produced current-save fixtures."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--prefix',type=Path,required=True);p.add_argument('--fixtures',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);prefix=a.prefix.resolve();env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 src=Path(__file__).resolve().parent
 nm=subprocess.check_output([str(prefix/'bin/arm-none-eabi-nm'),str(ROOT/'pokeemerald-release.elf')],text=True);symbols={v[2]:int(v[0],16) for line in nm.splitlines() if len(v:=line.split())==3}
 with (out/'host-build.log').open('w') as log:subprocess.run(['cc',str(src/'release.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 rom=ROOT/'pokeemerald-release.gba';before=sha(rom)
 for name in ['male','female','day','night']:
  scene=out/name;scene.mkdir(exist_ok=True);save=scene/'private.sav';save.write_bytes((a.fixtures/('private-'+name+'.sav')).read_bytes())
  with (scene/'emulator.log').open('w') as log:subprocess.run([str(out/'host'),str(rom),str(save),str(scene),hex(symbols['gMain']),hex(symbols['CB2_Overworld']),str(1 if name=='male' else 2 if name=='female' else 0),hex(symbols['sCurrentStartMenuActions']),hex(symbols['sStartMenuCursorPos']),hex(symbols['CB2_TrainerCard']),hex(symbols['gSaveBlock1Ptr'])],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
  for raw in scene.glob('*.rgba'):Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'))
 assert sha(rom)==before
 (out/'verification.json').write_text(json.dumps({'ROM_sha256':before,'ROM_unmodified':True,'input':'Normal Release Continue and controller buttons; no RAM/callback writes','fixtures':'Controlled current Debug saves, not historical owner saves','images':{str(p.relative_to(out)):sha(p) for p in out.rglob('*.png')}},indent=2)+'\n')
 print('Unmodified Release Continue and UI captures completed for both bedrooms and day/night Fallarbor.')
if __name__=='__main__':main()
