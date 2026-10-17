"""Native achievement extension UI/flash/save QA. Private ROMs and saves must never be published."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);a=p.parse_args()
 out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);src=Path(__file__).resolve().parent;prefix=a.prefix.resolve();env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 def run(cmd,name):
  with (out/name).open('w') as log:subprocess.run(cmd,cwd=R,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols=pokeemerald.elf',str(src/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
 def symbols(path):
  result={}
  for line in subprocess.check_output(['arm-none-eabi-nm',str(path)],text=True).splitlines():
   values=line.split()
   if len(values)==3:result[values[2]]=int(values[0],16)
  return result
 arm=symbols(out/'arm.elf');native=symbols(R/'pokeemerald.elf')
 run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
 rom=bytearray((R/'pokeemerald.gba').read_bytes());payload=(out/'arm.bin').read_bytes();offset=0x1f80000
 assert len(payload)<65536 and set(rom[offset:offset+len(payload)])=={255}
 rom[offset:offset+len(payload)]=payload;(out/'private-field-requests.gba').write_bytes(rom)
 run(['cc',str(src/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
 run([str(out/'host'),str(out/'private-field-requests.gba'),str(out),hex(native['gMain']),hex(arm['qa']|1),hex(native['sSelected']),hex(native['sDetail'])],'emulator.log')
 for raw in out.glob('*.rgba'):Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'))
 receipt={'version':(R/'VERSION').read_text().strip(),'passed':True,'emulator':'mGBA 0.10.2','variant':'Debug','ROM_sha256':hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),'scope':'Controlled v0.0.59-layout journal with arbitrary unpublished bits/tail, non-default wardrobe and Winter. Tested quiet research backfill, manual high-ID claims/full PC, native UI and actual flash save/clear/load. Not an authentic historical user fixture, full playthrough or Pizza Boy.','log':(out/'emulator.log').read_text(),'harness_sha256':{n:hashlib.sha256((src/n).read_bytes()).hexdigest() for n in ['arm.c','host.c','run.py']}}
 (out/'verification.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
