"""Controlled native visual repairs QA. Requires built Debug ELF/ROM, ARM tools and mGBA."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--mgba-prefix',type=Path,required=True);p.add_argument('--rom',type=Path,default=ROOT/'pokeemerald.gba');p.add_argument('--elf',type=Path,default=ROOT/'pokeemerald.elf');args=p.parse_args();out=args.output.resolve();out.mkdir(exist_ok=True,parents=True)
 src=Path(__file__).resolve().parent;env=os.environ.copy();prefix=args.mgba_prefix.resolve();env['PATH']=str(prefix/'bin')+':'+env['PATH'];env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 def run(cmd,log):
  with (out/log).open('w') as f:subprocess.run(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols='+str(args.elf.resolve()),str(src/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
 arm_nm=subprocess.check_output(['arm-none-eabi-nm',str(out/'arm.elf')],cwd=ROOT,env=env,text=True)
 callback=next(int(line.split()[0],16)|1 for line in arm_nm.splitlines() if line.split()[-1]=='qa')
 run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
 rom=bytearray(args.rom.read_bytes());arm=(out/'arm.bin').read_bytes();assert len(arm)<65536 and set(rom[0x1f80000:0x1f80000+len(arm)])=={255};rom[0x1f80000:0x1f80000+len(arm)]=arm;(out/'private-visual-repairs.gba').write_bytes(rom)
 nm=subprocess.check_output(['arm-none-eabi-nm',str(args.elf)],cwd=ROOT,env=env,text=True);symbols={p[2]:int(p[0],16) for line in nm.splitlines() if len(p:=line.split())==3}
 run(['cc',str(src/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
 run([str(out/'host'),str(out/'private-visual-repairs.gba'),str(out),hex(symbols['gMain']),hex(callback)],'emulator.log')
 for raw in sorted(out.glob('*.rgba')):Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(out/(raw.stem+'.png'))
 log=(out/'emulator.log').read_text()
 assert log.count(' errors=0')==72 and log.count('Wardrobe Apply/Cancel, Trainer Card returns and real flash roundtrip: passed')==2
 proof={'ROM_sha256':hashlib.sha256(args.rom.read_bytes()).hexdigest(),'ROM_version':(ROOT/'VERSION').read_text().strip(),'state':'Unpublished visual repairs candidate','emulator':'mGBA 0.10.2','controlled_setup':'Private callback prepares both bedrooms and native manual-clock day/night Fallarbor. Production ROM stays unchanged; do not publish private ROM or save fixtures.','movement_palette_cases':72,'wardrobe_apply_cancel_card_cycles':16,'battery_roundtrip_fields_per_gender':9,'outfit_corruption_reproduced':False,'limits':'Controlled current saves and direct state switches; not historical saves or a Pizza Boy device reproduction.','images':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('*.png'))}}
 (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
if __name__=='__main__':main()
