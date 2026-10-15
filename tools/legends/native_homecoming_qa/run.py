"""Controlled Debug native conversations and flash persistence; private ROM must never be distributed."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);a=p.parse_args()
 out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);src=Path(__file__).resolve().parent;prefix=a.prefix.resolve();env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 def run(cmd,name):
  with (out/name).open('w') as f:subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols=pokeemerald.elf',str(src/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
 nm=subprocess.check_output(['arm-none-eabi-nm',str(out/'arm.elf')],text=True);callback=next(int(l.split()[0],16)|1 for l in nm.splitlines() if l.split()[-1]=='qa')
 run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
 rom=bytearray((R/'pokeemerald.gba').read_bytes());arm=(out/'arm.bin').read_bytes();assert len(arm)<65536 and set(rom[0x1f80000:0x1f80000+len(arm)])=={255};rom[0x1f80000:0x1f80000+len(arm)]=arm;(out/'private-homecoming.gba').write_bytes(rom)
 nm=subprocess.check_output(['arm-none-eabi-nm',str(R/'pokeemerald.elf')],text=True);mainaddr=next(int(l.split()[0],16) for l in nm.splitlines() if l.split()[-1]=='gMain')
 run(['cc',str(src/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
 run([str(out/'host'),str(out/'private-homecoming.gba'),str(out),hex(mainaddr),hex(callback)],'emulator.log')
 for raw in out.glob('*.rgba'):Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'))
 proof={'version':(R/'VERSION').read_text().strip(),'passed':True,'emulator':'mGBA 0.10.2','variant':'Debug','ROM_sha256':hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),'scope':'Controlled New Game setup of both home layouts and format-identical pre-feature state (not an authentic historical-release save). Passable floor spawns and real input approach to Mom; native table collision rejected movement with no-clip disabled in both layouts; unchanged walkable player position throughout the scene. Actual Mom interaction, native family script and object cleanup, real flash save/clear/load before and after the welcome, retained non-default wardrobe/bedroom/seasons, and no repeat after reload; actual Champion-stage Mom and Norman Gym conversations. Private callback ROM excluded from distribution. Uninterrupted story and Pizza Boy remain unverified.','log':(out/'emulator.log').read_text(),'harness_sha256':{f:hashlib.sha256((src/f).read_bytes()).hexdigest() for f in ['arm.c','host.c','run.py']}}
 (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
if __name__=='__main__':main()
