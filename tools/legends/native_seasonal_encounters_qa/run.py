"""Real compiled DexNav/seasonal encounter previews in a private diagnostic copy."""
from pathlib import Path
import argparse,hashlib,json,subprocess,re,struct,shutil
from workers import worker_count,execute,compare
from PIL import Image
R=Path(__file__).resolve().parents[3];S=Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--jobs',type=int,default=None,help='1–4 isolated native processes, capped by CPU affinity')
parser.add_argument('--compare-serial',action='store_true',help='One-time complete serial/parallel parity benchmark')
parser.add_argument('--output',type=Path,default=R/'build/seasonal-encounters-qa')
options=parser.parse_args();jobs=worker_count(options.jobs);O=options.output.resolve();O.mkdir(parents=True,exist_ok=True)
for old in ['verification.json','serial-parallel-comparison.json','emulator.log']:(O/old).unlink(missing_ok=True)
for folder in ['parallel','serial-reference']:
 if (O/folder).exists():shutil.rmtree(O/folder)
for old in O.glob('scene-*.png'):old.unlink()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,log):
 with (O/log).open('w') as f:subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,check=True)
lines=subprocess.check_output(['arm-none-eabi-nm',str(R/'pokeemerald.elf')],text=True).splitlines();syms={v[2]:int(v[0],16) for line in lines if len(v:=line.split())==3}
source=(R/'src/dexnav.c').read_text();ui=source[source.index('struct DexNavGUI\n{'):source.index('\n};',source.index('struct DexNavGUI\n{'))+3]
data=(R/'src/data/legends_seasonal_encounters.h').read_text();tables={(int(r),s.lower()):re.findall(r'SPECIES_\w+',body) for r,s,method,body in re.findall(r'static const struct WildPokemon sRoute((?:10[1-9]|11[0-9]|12[0-9]|13[0-4]))(Spring|Summer|Autumn|Winter)(Water)?Mons.*?=\s*\{(.*?)\};',data,re.S)}
layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];scenes=[]
def add(route,season,mode=0,south=False):
 water=route in [*range(105,110),122,*range(124,135)];terrain=0x170 if water else 0x251 if route==111 else 0x20a if route==113 else 0x15 if route in (119,120) else 13
 d=json.loads((R/f'data/maps/Route{route}/map.json').read_text());l=next(l for l in layouts if l['id']==d['layout']);raw=(R/l['blockdata_filepath']).read_bytes();blocks=struct.unpack('<'+'H'*(len(raw)//2),raw)
 occupied={(o['x'],o['y']) for o in d['object_events']};coords=[(i%l['width'],i//l['width']) for i,v in enumerate(blocks) if v&0xfff==terrain and 3<i%l['width']<l['width']-3 and 3<i//l['width']<l['height']-3 and (i%l['width'],i//l['width']) not in occupied and (not south or i//l['width']>40)]
 assert coords,(route,'no passable native terrain fixture');x,y=coords[0];name=['spring','summer','autumn','winter'][season];expected=tables[route,name]
 rows=re.findall(r'\{(\d+), (\d+), SPECIES_\w+\}',re.search(r'sRoute'+str(route)+name.title()+('Water' if water else '')+r'Mons.*?=\s*\{(.*?)\};',data,re.S)[1]);minimum=min(int(a) for a,b in rows);maximum=max(int(b) for a,b in rows)
 scenes.append(dict(name=f'route{route}-{name}'+('-all-unseen' if mode==1 else '-all-seen' if mode==2 else '-south' if south else ''),route=route,season=season,mode=mode,area=1 if water else 0,x=x,y=y,min=minimum,max=maximum,rate=10 if route==111 else 4 if water else 15 if route==119 else 20,expected=expected))
for route in range(101,105):
 for season in range(4):add(route,season)
add(101,0,1);add(104,3,2);add(104,3,south=True)
for route in range(101,105):
 for season in range(4):add(route,season,2)
for route in range(105,109):
 for season in range(4):add(route,season)
for route in range(105,109):
 for season in range(4):add(route,season,2)
add(105,0,1)
for mode in [0,2]:
 for route in range(109,113):
  for season in range(4):add(route,season,mode)
add(109,0,1);add(111,3,1)
for mode in [0,2]:
 for route in range(113,117):
  for season in range(4):add(route,season,mode)
add(113,0,1);add(116,3,1)
for mode in [0,2]:
 for route in range(117,122):
  for season in range(4):add(route,season,mode)
add(117,0,1);add(119,3,1)
for mode in [0,2]:
 for route in range(122,127):
  for season in range(4):add(route,season,mode)
add(122,0,1);add(123,3,1)
for mode in [0,2]:
 for route in range(127,132):
  for season in range(4):add(route,season,mode)
add(129,0,1);add(131,3,1)
for mode in [0,2]:
 for route in range(132,135):
  for season in range(4):add(route,season,mode)
add(132,0,1);add(134,3,1)
assert len(scenes)==288
header=[ui,'struct QAScenario {u16 map; s16 x,y; u8 season,mode,area,min,max,rate; enum Species expected[12];};','static const struct QAScenario scenarios[] = {']
for s in scenes:header.append('{MAP_ROUTE%d,%d,%d,%d,%d,%d,%d,%d,%d,{%s}},'%(s['route'],s['x'],s['y'],s['season'],s['mode'],s['area'],s['min'],s['max'],s['rate'],','.join(s['expected'])))
header.append('};');(O/'qa_scenarios.h').write_text('\n'.join(header)+'\n')
args=['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-I'+str(O),'-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib']
for define,symbol in [('QA_GUI_TASK','Task_DexNavMain'),('QA_UI','sDexNavUiDataPtr')]:args+=['-D'+define+'='+hex(syms[symbol]|(0 if define=='QA_UI' else 1))]
run(args+['-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols=pokeemerald.elf',str(S/'arm.c'),'-o',str(O/'qa.elf')],'arm-build.log')
run(['arm-none-eabi-objcopy','-O','binary',str(O/'qa.elf'),str(O/'qa.bin')],'objcopy.log')
a=subprocess.check_output(['arm-none-eabi-nm',str(O/'qa.elf')],text=True).splitlines();extra={v[2]:int(v[0],16) for line in a if len(v:=line.split())==3}
rom=R/'pokeemerald.gba';before=sha(rom);image=bytearray(rom.read_bytes());payload=(O/'qa.bin').read_bytes();assert len(payload)<65536 and set(image[0x1f80000:0x1f80000+len(payload)])=={255};image[0x1f80000:0x1f80000+len(payload)]=payload;private=O/'PRIVATE-QA.gba';private.write_bytes(image)
run(['cc','-std=gnu11',str(S/'host.c'),'-lmgba','-o',str(O/'host')],'host-build.log')
execution={};parity=None
addresses=[hex(syms['gMain']),hex(extra['qa']),hex(syms['CB2_Overworld'])]
try:
 execution=execute([str(O/'host')],private,addresses,len(scenes),jobs,O/'parallel')
 if options.compare_serial:
  serial=execute([str(O/'host')],private,addresses,len(scenes),1,O/'serial-reference')
  parity=compare(O/'serial-reference',O/'parallel')
  parity.update(serial_seconds=serial['seconds'],parallel_seconds=execution['seconds'],speedup=round(serial['seconds']/execution['seconds'],3))
  (O/'serial-parallel-comparison.json').write_text(json.dumps(parity,indent=2)+'\n')
finally:
 for mode in ['parallel','serial-reference']:
  for p in sorted((O/mode).glob('worker-*/*.rgba')):
   target=O/p.with_suffix('.png').name if mode=='parallel' else O/mode/p.with_suffix('.png').name
   Image.frombytes('RGBA',(240,160),p.read_bytes()).convert('RGB').save(target);p.unlink()
 if (O/'parallel/emulator.log').exists():shutil.copyfile(O/'parallel/emulator.log',O/'emulator.log')
 private.unlink(missing_ok=True)
assert sha(rom)==before
proof={'version':(R/'VERSION').read_text().strip(),'base_ROM_sha256':before,'emulator':'mGBA native core 0.10.2','private_instrumentation':True,'public_ROM_unchanged':True,'scenarios':scenes,'wild_creations_per_scenario':256,'passed':True,'scope':'Actual compiled land and Surf tables, wild creation and DexNav GUI; hardware-sampled two-pose bounds/centering and uniform shrink-only scale for every grid icon; controlled route/season/seen state, original icons and VRAM frames, isolated palettes, unseen selection lock, closure and protected state. Both Route104 halves, native Surf fixtures on Routes105-109/122/124-134 and Route111 desert, Route113 native ash-grass and Routes114-118/121/123 grass and Routes119-120 native long-grass fixtures (Route119 rate15) checked. Not a natural progression playthrough, historical-save migration, full DexNav hunt or Pizza Boy test.','harness_sha256':{n:sha(S/n) for n in ['arm.c','host.c','run.py','workers.py']}}
proof['execution']=execution
if parity is not None:proof['serial_parallel_comparison']=parity
(O/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print('PASS: 288 targeted native seasonal/DexNav scenarios and 73728 real generated Pokémon; grass and Surf, original/seen/unseen states.')
