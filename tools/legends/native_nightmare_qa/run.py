"""Actual compiled-game captures and controller tests; private fixtures never ship."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,struct,time
from PIL import Image
R=Path(__file__).resolve().parents[3];S=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--prefix',type=Path,default=Path('/usr'));p.add_argument('--output',type=Path,default=R/'build/nightmare-native');a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);prefix=a.prefix.resolve();env=os.environ.copy();env['PATH']=str(prefix/'bin')+':'+env['PATH'];env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','');previous=[*out.glob('*.png'),*out.glob('*.rgba')]+[q for q in [out/'verification.json',out/'emulator.log'] if q.exists()]
if previous:
 archive=out/'history'/str(time.time_ns());archive.mkdir(parents=True)
 for old in previous:old.rename(archive/old.name)
captures=[]
def run(cmd,log):
 with (out/log).open('w') as f:subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
def syms(path):return {v[2]:int(v[0],16) for line in subprocess.check_output(['arm-none-eabi-nm',str(path)],env=env,text=True).splitlines() if len(v:=line.split())==3}
elf=R/'pokeemerald.elf';rom=R/'pokeemerald.gba';symbols=syms(elf);source=rom.read_bytes()
run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols='+str(elf),str(S/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log');payload=(out/'arm.bin').read_bytes();assert len(payload)<65536 and set(source[0x1f80000:0x1f80000+len(payload)])=={255};private=out/'PRIVATE-QA.gba';patched=bytearray(source);patched[0x1f80000:0x1f80000+len(payload)]=payload;private.write_bytes(patched)
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];grids=[];widths=[];sizes=[];warps=[];counts=[];dirs=[]
for name in ['LilycoveCity','LegendsNightmare_Home','MtPyre_1F','LegendsNightmare_Bedroom','LegendsNightmare_Street','LegendsNightmare_Shore']:
 m=json.loads((R/f'data/maps/{name}/map.json').read_text());l=next(x for x in layouts if x['id']==m['layout']);w=l['width'];raw=(R/l['blockdata_filepath']).read_bytes();cells=list(struct.unpack('<%dH'%(len(raw)//2),raw))
 for i,v in enumerate(cells):
  if v>>12==1:cells[i]|=0x400 # Ocean is not a walking path; native stairs change elevation.
 for o in m['object_events']:
  if o['script'] in ['Nightmare_Mira','Nightmare_Darkrai']:continue # Visibility is checked live by the host.
  # Actors remain obstacles even when hidden; chosen paths need no actor tile.
  cells[o['y']*w+o['x']]|=0x400
 grids.append('{'+','.join(map(str,cells))+'}');widths.append(w);sizes.append(len(cells));warps.append('{'+','.join(str(e['y']*w+e['x']) for e in m['warp_events'])+'}');counts.append(len(m['warp_events']));dirs.append('{'+','.join('128' if name.endswith(('Home','Bedroom')) else '64' if name.endswith('Shore') else '0' for e in m['warp_events'])+'}')
(out/'paths.h').write_text('static const unsigned short grids[6][4096]={'+','.join(grids)+'};\nstatic const int widths[]={'+','.join(map(str,widths))+'},sizes[]={'+','.join(map(str,sizes))+'},warp_counts[]={'+','.join(map(str,counts))+'},warps[6]['+str(max(counts))+']={'+','.join(warps)+'},warp_dirs[6]['+str(max(counts))+']={'+','.join(dirs)+'};\n')
run(['cc','-I'+str(out),str(S/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
choices=[hex(int(line.split()[0],16)) for line in subprocess.check_output(['arm-none-eabi-nm',str(elf)],env=env,text=True).splitlines() if line.endswith(' t HandleInputChooseAction')];assert len(choices)==3
try:run([str(out/'host'),str(private),str(out),hex(symbols['gMain']),hex(syms(out/'arm.elf')['qa']),hex(symbols['gBattlerControllerFuncs']),*choices,hex(symbols['Task_HandleYesNoInput']),hex(symbols['CB2_WhiteOut'])],'emulator.log')
finally:
 for raw in out.glob('*.rgba'):
  png=raw.with_suffix('.png');Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(png);captures.append(png);raw.unlink()
 private.unlink(missing_ok=True)
assert rom.read_bytes()==source
proof=dict(version=(R/'VERSION').read_text().strip()+' + unshipped Darkrai review',ROM_sha256=hashlib.sha256(source).hexdigest(),emulator='mGBA0.10.2 native core',ELF_sha256=hashlib.sha256(elf.read_bytes()).hexdigest(),harness_sha256={n:hashlib.sha256((S/n).read_bytes()).hexdigest() for n in ['arm.c','host.c','run.py']},passed=True,setup='Controlled fresh fixtures; actual compiled map/script/battle engine and real controller inputs. Scene cuts only between independent test cases; no synthetic gameplay images.',limits='Not a natural full-story playthrough, authentic historical owner-save matrix, Release emulator or Pizza Boy test.',log=(out/'emulator.log').read_text(),images={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(captures)})
(out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS native Nightmare progression: '+str(out))
