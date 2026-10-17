"""Execute affected source-script paths and validate real field-text control geometry."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
paths=['data/scripts/legends_field_requests.inc']+[f'data/maps/{m}/scripts.inc' for m in ['Route119_WeatherInstitute_1F','LittlerootTown','RustboroCity','FortreeCity','LilycoveCity']]
texts={};blocks={};fallthrough={}
for path in paths:
 source=(R/path).read_text()
 labels=list(re.finditer(r'(?m)^([A-Za-z_]\w*):{1,2}\s*\n',source))
 for a,b in zip(labels,labels[1:]):fallthrough[a[1]]=b[1]
 for m in labels:
  after=source[m.end():];next_label=re.search(r'(?m)^[A-Za-z_]\w*:{1,2}\s*$',after)
  body=after[:next_label.start()] if next_label else after
  lines=[x.strip().split('@')[0].strip() for x in body.splitlines()]
  blocks[m[1]]=[x for x in lines if x and not x.startswith('@')]
  values=re.findall(r'\.string "(.*)"',body)
  if values:texts[m[1]]=''.join(values)

def run(entry,flags=(),state=1,season=0,answer=1):
 label=entry;pc=0;result=0;messages=[];locked=False;steps=0
 while steps<100:
  steps+=1;lines=blocks[label]
  if pc==len(lines):label=fallthrough[label];pc=0;lines=blocks[label]
  cmd,*arg=lines[pc].split(None,1);pc+=1;args=arg[0].split(', ') if arg else []
  if cmd in ['lock','lockall']:locked=True
  elif cmd=='faceplayer':pass
  elif cmd=='release':locked=False
  elif cmd=='end':assert not locked,(entry,'lock leaked');return messages
  elif cmd=='goto':label=args[0];pc=0
  elif cmd=='goto_if_set':
   if args[0] in flags:label=args[1];pc=0
  elif cmd=='goto_if_eq':
   value=state if args[0]=='VAR_WEATHER_INSTITUTE_STATE' else result
   target={'NO':0,'YES':1}.get(args[1],int(args[1]) if args[1].isdigit() else -1)
   if value==target:label=args[2];pc=0
  elif cmd=='msgbox':
   messages.append(args[0]);assert args[0] in texts,args[0]
   if args[1]=='MSGBOX_YESNO':result=answer
   if args[1]=='MSGBOX_NPC':return messages # native standard script locks/releases itself.
  elif cmd=='special':assert args[0]=='LegendsSeasonBulletinSpecial';result=season
  else:raise AssertionError((entry,'unexpected command / side effect',cmd,args))
 raise AssertionError(('nonterminating script',entry))

W='Route119_WeatherInstitute_1F_'
for state in [0,1,2]:
 for season in range(4):
  for answer in [0,1]:
   result=run(W+'EventScript_InstituteWorker2',state=state,season=season,answer=answer)
   expected=[W+'Text_WhatWereAquasUpTo']
   if state:
    expected.append(W+'Text_BulletinOffer')
    if answer:expected.append(W+'Text_Bulletin'+['Spring','Summer','Autumn','Winter'][season])
   assert result==expected,(state,season,answer,result)
checks=[('LittlerootTown_EventScript_FatMan',(), 'LittlerootTown_Text_CanUsePCToStoreItems'),('LittlerootTown_EventScript_FatMan',('FLAG_SYS_GAME_CLEAR',),'LittlerootTown_Text_ChampionCameHome'),('RustboroCity_EventScript_DevonEmployee2',(),'RustboroCity_Text_YoureNewAroundHere'),('RustboroCity_EventScript_DevonEmployee2',('FLAG_BADGE01_GET',),'RustboroCity_Text_DevonEmployee2Badge'),('RustboroCity_EventScript_DevonEmployee2',('FLAG_SYS_GAME_CLEAR','FLAG_BADGE01_GET'),'RustboroCity_Text_DevonEmployee2Champion'),('FortreeCity_EventScript_OldMan',(),'FortreeCity_Text_EveryoneHealthyAndLively'),('FortreeCity_EventScript_OldMan',('FLAG_BADGE06_GET',),'FortreeCity_Text_OldManBadge'),('LilycoveCity_EventScript_Man3',(),'LilycoveCity_Text_ContestHallInTown'),('LilycoveCity_EventScript_Man3',('FLAG_SYS_GAME_CLEAR',),'LilycoveCity_Text_ChampionContest')]
for entry,flags,expected in checks:assert run(entry,flags=flags)==[expected]
# Only new dialogue: old text is protected rather than broadly reformatted.
selected=[n for n in texts if re.search(r'(BirchNotes|DevonNotes|Bulletin|OldManBadge|ChampionCameHome|DevonEmployee2Badge|DevonEmployee2Champion|ChampionContest)',n)]
charmap={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)};charmap["'"]=0xb4
widths=list(map(int,re.findall(r'\d+',(R/'src/fonts.c').read_text().split('gFontNormalLatinGlyphWidths[] = {')[1].split('};')[0])))
for name in selected:
 y=0
 for token in re.split(r'(\\[npl])',texts[name]):
  if token==r'\n':y+=1;assert y<=1,(name,'third unscrolled line in a two-line field box')
  elif token==r'\p':y=0
  elif token==r'\l':y=1
  else:
   text=token.replace('$','');assert sum(widths[charmap[c]] for c in text)<=208,(name,text)
print(f'PASS: 24 weather state/choice/season paths, 9 NPC milestone paths, lock release, no reward/write commands, and {len(selected)} new field texts.')
