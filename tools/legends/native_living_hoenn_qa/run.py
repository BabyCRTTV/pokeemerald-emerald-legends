"""Targeted original-game dialogue tests in a private instrumented Debug copy."""
from pathlib import Path
import hashlib,json,subprocess,os
from PIL import Image
R=Path(__file__).resolve().parents[3];S=Path(__file__).resolve().parent;O=R/'build/living-hoenn-qa';O.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,log):
 with (O/log).open('w') as f:subprocess.run(cmd,cwd=R,stdout=f,stderr=subprocess.STDOUT,check=True)
lines=subprocess.check_output(['arm-none-eabi-nm',str(R/'pokeemerald.elf')],text=True).splitlines();syms={v[2]:int(v[0],16) for line in lines if len(v:=line.split())==3}
scenes=[]
def add(name,map,x,y,kind,arg,entry,expected,object_script=None):
 d=json.loads((R/'data/maps'/map/'map.json').read_text());local=next((i+1 for i,o in enumerate(d['object_events']) if o.get('script')==(object_script or entry)),0)
 scenes.append(dict(name=name,map=map,x=x,y=y,kind=kind,arg=arg,entry=entry,expected=expected,localId=local))
for patron,counts in [('Birch',[0,3,9,18]),('Devon',[0,3,6,12])]:
 for tier,n in enumerate(counts):
  if patron=='Birch':add('birch-'+str(n),'LittlerootTown_ProfessorBirchsLab',6,5,0,n,'LegendsFieldRequests_Talk','LegendsFieldRequests_Text_BirchNotes'+['None','Early','Advanced','Final'][tier],'LittlerootTown_ProfessorBirchsLab_EventScript_Birch')
  else:add('devon-'+str(n),'RustboroCity_DevonCorp_3F',14,5,1,n,'LegendsDevonRequests_Talk','LegendsFieldRequests_Text_DevonNotes'+['None','Early','Advanced','Final'][tier],'RustboroCity_DevonCorp_3F_EventScript_MrStone')
W='Route119_WeatherInstitute_1F_'
for arg,suffix in enumerate(['WhatWereAquasUpTo','BulletinOffer','BulletinSpring','BulletinSummer','BulletinAutumn','BulletinWinter']):add('weather-'+suffix,'Route119_WeatherInstitute_1F',5,6,2,arg,W+'EventScript_InstituteWorker2',W+'Text_'+suffix)
for kind,map,x,y,entry,texts in [
 (3,'LittlerootTown',11,13,'FatMan',['CanUsePCToStoreItems','ChampionCameHome']),
 (4,'RustboroCity',13,35,'DevonEmployee2',['YoureNewAroundHere','DevonEmployee2Badge','DevonEmployee2Champion']),
 (5,'FortreeCity',8,11,'OldMan',['EveryoneHealthyAndLively','OldManBadge']),
 (6,'LilycoveCity',28,29,'Man3',['ContestHallInTown','ChampionContest'])]:
 for arg,text in enumerate(texts):add(map+'-'+str(arg),map,x,y,kind,arg,map+'_EventScript_'+entry,map+'_Text_'+text)
assert len(scenes)==23
header=['struct QAScenario {u16 map; s16 x,y; u8 kind,arg,localId; const u8 *entry,*expected;};','static const struct QAScenario scenarios[] = {']
for sc in scenes:header.append('{MAP_%s,%d,%d,%d,%d,%d,(const u8*)0x%x,(const u8*)0x%x},'%(json.loads((R/'data/maps'/sc['map']/'map.json').read_text())['id'][4:],sc['x'],sc['y'],sc['kind'],sc['arg'],sc['localId'],syms[sc['entry']],syms[sc['expected']]))
header.append('};');(O/'qa_scenarios.h').write_text('\n'.join(header)+'\n')
run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-I'+str(O),'-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-DQA_MULTI='+hex(syms['Task_HandleMultichoiceInput']|1),'-DQA_YESNO='+hex(syms['Task_HandleYesNoInput']|1),'-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols=pokeemerald.elf',str(S/'arm.c'),'-o',str(O/'qa.elf')],'arm-build.log')
run(['arm-none-eabi-objcopy','-O','binary',str(O/'qa.elf'),str(O/'qa.bin')],'objcopy.log')
a=subprocess.check_output(['arm-none-eabi-nm',str(O/'qa.elf')],text=True).splitlines();extra={v[2]:int(v[0],16) for line in a if len(v:=line.split())==3}
rom=R/'pokeemerald.gba';before=sha(rom);data=bytearray(rom.read_bytes());payload=(O/'qa.bin').read_bytes();assert len(payload)<65536 and set(data[0x1f80000:0x1f80000+len(payload)])=={255};data[0x1f80000:0x1f80000+len(payload)]=payload;private=O/'PRIVATE-QA.gba';private.write_bytes(data)
run(['cc','-std=gnu11',str(S/'host.c'),'-lmgba','-o',str(O/'host')],'host-build.log')
run([str(O/'host'),str(private),str(O),hex(syms['gMain']),hex(extra['qa']),hex(syms['CB2_Overworld']),'1','2'],'emulator.log');assert sha(rom)==before
for p in O.glob('*.rgba'):Image.frombytes('RGBA',(240,160),p.read_bytes()).convert('RGB').save(p.with_suffix('.png'));p.unlink()
proof={'version':(R/'VERSION').read_text().strip(),'base_ROM_sha256':before,'emulator':'mGBA native core 0.10.2','private_instrumentation':True,'public_ROM_unchanged':True,'scenarios':scenes,'passed':True,'scope':'Original compiled text/scripts executed with controlled flags/vars; research cursor and exact expected text, weather choice/state/active season, all four NPC fallbacks/milestones, termination and protected request/journal/PC state checked. Floor collision checked. Not a natural full playthrough, save migration or Pizza Boy test.','harness_sha256':{n:sha(S/n) for n in ['arm.c','host.c','run.py']}}
(O/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');private.unlink();print('PASS: 23 targeted native Living Hoenn scenarios.')
