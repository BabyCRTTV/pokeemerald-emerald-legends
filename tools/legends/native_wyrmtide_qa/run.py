"""Capture only real native mGBA frames from the compiled Wyrmtide review ROM."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,struct
from PIL import Image
R=Path(__file__).resolve().parents[3];S=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--prefix',type=Path,default=Path('/usr'));p.add_argument('--scenes-only',action='store_true');p.add_argument('--output',type=Path,default=R/'build/wyrmtide-native');a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);prefix=a.prefix.resolve();env=os.environ.copy();env['PATH']=str(prefix/'bin')+':'+env['PATH'];env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
(out/'verification.json').unlink(missing_ok=True)
captures=[]
def run(cmd,log):
 with (out/log).open('w') as f:subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
def syms(path):return {v[2]:int(v[0],16) for line in subprocess.check_output(['arm-none-eabi-nm',str(path)],env=env,text=True).splitlines() if len(v:=line.split())==3}
elf=R/'pokeemerald.elf';rom=R/'pokeemerald.gba';symbols=syms(elf);source=rom.read_bytes()
run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols='+str(elf),str(S/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log');payload=(out/'arm.bin').read_bytes();assert len(payload)<65536 and set(source[0x1f80000:0x1f80000+len(payload)])=={255};private=out/'PRIVATE-QA.gba';patched=bytearray(source);patched[0x1f80000:0x1f80000+len(payload)]=payload;private.write_bytes(patched)
# Navigation checks use the compiled map collision words and real button steps.
grids=[]
for name in ['Descent1','Descent2','Descent3','Descent4']:
 raw=(R/f'data/layouts/LegendsWyrmtide_{name}/map.bin').read_bytes()
 grids.append('{'+','.join(str(v) for v in struct.unpack('<456H',raw))+'}')
(out/'paths.h').write_text('static const unsigned short grids[4][456]={'+','.join(grids)+'};\n')
run(['cc','-I'+str(out),str(S/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
choices=[hex(int(line.split()[0],16)) for line in subprocess.check_output(['arm-none-eabi-nm',str(elf)],env=env,text=True).splitlines() if line.endswith(' t HandleInputChooseAction')];assert len(choices)==3
try:run([str(out/'host'),str(private),str(out),hex(symbols['gMain']),hex(syms(out/'arm.elf')['qa']),hex(symbols['gBattlerControllerFuncs']),*choices,str(int(a.scenes_only))],'emulator.log')
finally:
 for raw in out.glob('*.rgba'):
  png=raw.with_suffix('.png');Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(png);captures.append(png);raw.unlink()
 private.unlink(missing_ok=True)
assert rom.read_bytes()==source
proof={'version':(R/'VERSION').read_text().strip()+' + unshipped Wyrmtide review','ROM_sha256':hashlib.sha256(source).hexdigest(),'emulator':'mGBA 0.10.2 native core','scenesOnly':a.scenes_only,'passed':True,'setup':'Controlled fresh native fixtures, actual map/script/battle engine and button input; private setup payload never distributed.','limits':'Not an authentic historical owner save, natural full-story playthrough, Release-emulator or Pizza Boy test.','log':(out/'emulator.log').read_text(),'images':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in captures}}
(out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS native Wyrmtide '+('scenes' if a.scenes_only else 'story interactions')+': '+str(out))
