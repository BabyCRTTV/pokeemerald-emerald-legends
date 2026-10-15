"""Controlled Debug quest tracking, menu exclusion and flash persistence; private ROM must never be distributed."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[3]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--overflow-demo',action='store_true');a=p.parse_args()
 out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);src=Path(__file__).resolve().parent;prefix=a.prefix.resolve();env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 def run(cmd,name):
  with (out/name).open('w') as f:subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols=pokeemerald.elf',str(src/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
 nm=subprocess.check_output(['arm-none-eabi-nm',str(out/'arm.elf')],text=True);callback=next(int(l.split()[0],16)|1 for l in nm.splitlines() if l.split()[-1]=='qa')
 run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
 rom=bytearray((R/'pokeemerald.gba').read_bytes());arm=(out/'arm.bin').read_bytes();assert len(arm)<65536 and set(rom[0x1f80000:0x1f80000+len(arm)])=={255};rom[0x1f80000:0x1f80000+len(arm)]=arm;(out/'private-quest-tracking.gba').write_bytes(rom)
 nm=subprocess.check_output(['arm-none-eabi-nm',str(R/'pokeemerald.elf')],text=True);mainaddr=next(int(l.split()[0],16) for l in nm.splitlines() if l.split()[-1]=='gMain')
 reminder=next(int(l.split()[0],16) for l in nm.splitlines() if l.split()[-1]=='sReminderHandle')
 extra=[]
 if a.overflow_demo:
  import re
  symbols={parts[2]:int(parts[0],16) for line in nm.splitlines() if len(parts:=line.split())==3}
  chars={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)};chars["'"]=0xB4
  demo='Return the recovered DEVON GOODS to the researcher waiting inside DEVON CORPORATION in RUSTBORO CITY. Speak to the receptionist, take the stairs, and check the delivery details before leaving for your next destination.'
  encoded=bytes([chars[c] for c in demo]+[255]);at=0x1FA0000
  assert set(rom[at:at+len(encoded)])=={255};rom[at:at+len(encoded)]=encoded
  import struct
  # Native LegendsQuest = 40 bytes, step[1].text at offset 16. Private fixture only.
  struct.pack_into('<I',rom,symbols['sQuests']-0x08000000+9*40+16,0x08000000+at)
  (out/'private-quest-tracking.gba').write_bytes(rom)
  extra=[hex(symbols['sReminderScrollOffset']),hex(symbols['sReminderScrollLimit'])]
 run(['cc',str(src/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
 run([str(out/'host'),str(out/'private-quest-tracking.gba'),str(out),hex(mainaddr),hex(callback),hex(reminder),*extra],'emulator.log')
 for raw in out.glob('*.rgba'):Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'))
 baseline=Image.open(out/'pause-off.png');tracked=Image.open(out/'pause-tracked.png')
 assert baseline.crop((136,8,232,152)).tobytes()==tracked.crop((136,8,232,152)).tobytes()
 assert baseline.crop((0,88,112,152)).tobytes()==tracked.crop((0,88,112,152)).tobytes()
 assert tracked.crop((0,0,112,88)).tobytes()!=Image.open(out/'pause-next-step.png').crop((0,0,112,88)).tobytes()
 proof={'version':(R/'VERSION').read_text().strip(),'passed':True,'emulator':'mGBA 0.10.2','variant':'Debug','ROM_sha256':hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),'overflow_demo':a.overflow_demo,'scope':'Controlled Debug fixture with the unchanged v0.0.56-format journal (reserved=0), non-default appearance/bedroom/Winter, and walkable floor position. Actual input tracks a quest through Details and opens the real pause menu on both pages, DexNav help/return and Save dialog. Native flag fixtures advance and complete the quest; Safari layout suppresses the reminder. Real flash save/clear/load verifies pre-feature defaults, tracked selection and completion. Not an authentic historical save, uninterrupted story or Pizza Boy test. Private ROM excluded.','menu_content_and_clock_pixels_unchanged':True,'next_objective_pixels_updated':True,'log':(out/'emulator.log').read_text(),'harness_sha256':{f:hashlib.sha256((src/f).read_bytes()).hexdigest() for f in ['arm.c','host.c','run.py']}}
 (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
if __name__=='__main__':main()
