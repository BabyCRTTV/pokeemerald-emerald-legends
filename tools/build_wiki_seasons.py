#!/usr/bin/env python3
"""Explicitly import pinned seasonal grass tables during an owner-requested review.

An external header is allowed only for an UNPUBLISHED preview, with a recorded hash.
No date/time restrictions are inferred from species lore.
"""
import argparse, hashlib, json, re, subprocess
from collections import defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1]; W=R/'docs/wiki'
SEASONS=['spring','summer','autumn','winter']
parser=argparse.ArgumentParser();parser.add_argument('--preview-header',type=Path);args=parser.parse_args()
p=W/'dex-data.json';data=json.loads(p.read_text());commit=data['sourceCommit']
def read(path):return subprocess.check_output(['git','show',commit+':'+path],cwd=R)
if args.preview_header:
 header=args.preview_header.read_bytes();status='preview'
else:
 path='src/data/legends_seasonal_encounters.h'
 if subprocess.run(['git','cat-file','-e',commit+':'+path],cwd=R,stderr=subprocess.DEVNULL).returncode:raise SystemExit('Pinned game has no seasonal tables; no changes made.')
 header=read(path);status='published'
source=json.loads(read('src/data/wild_encounters.json'))['wild_encounter_groups'][0]
weights=next(f['encounter_rates'] for f in source['fields'] if f['type']=='land_mons')
tables={}
for route,season,body in re.findall(r'static const struct WildPokemon sRoute(10[1-4])(Spring|Summer|Autumn|Winter)Mons.*?=\s*\{(.*?)\};',header.decode(),re.S):
 slots=re.findall(r'\{(\d+),\s*(\d+),\s*SPECIES_(\w+)\}',body);assert len(slots)==len(weights)
 entries={}
 for (lo,hi,species),rate in zip(slots,weights):
  e=entries.setdefault(species,dict(id=species,min=101,max=0,rate=0,time='all-day',seasons=[]))
  e.update(min=min(e['min'],int(lo)),max=max(e['max'],int(hi)),rate=e['rate']+rate)
 assert sum(e['rate'] for e in entries.values())==100
 tables[(route,season.lower())]=list(entries.values())
assert len(tables)==16
forms=[dict(id='SANDSHREW_ALOLA',formOf='SANDSHREW',num=None,name='Alolan Sandshrew',types=['ICE','STEEL'],category='Mouse',stats=[50,75,90,10,35,40],sprite='sandshrew/alola',crySpecies='SANDSHREW'),dict(id='DEERLING_AUTUMN',formOf='DEERLING',num=None,name='Autumn Deerling',types=['NORMAL','GRASS'],category='Season',stats=[60,60,50,40,50,75],sprite='deerling/autumn',crySpecies='DEERLING')]
for form in forms:
 if not any(p['id']==form['id'] for p in data['species']):data['species'].append(form)
known={p['id'] for p in data['species']}
for m in data['maps']:
 route=m['id'].removeprefix('MAP_ROUTE')
 if (route,'spring') not in tables:continue
 land=next(x for x in m['methods'] if x['id']=='land')
 land['seasonalVariants']=[]
 for season in SEASONS:
  entries=tables[(route,season)]
  for e in entries:
   assert e['id'] in known,e['id']
   e['seasons']=[s for s in SEASONS if any(x['id']==e['id'] for x in tables[(route,s)])]
  land['seasonalVariants'].append(dict(season=season,entries=sorted(entries,key=lambda x:-x['rate'])))
data['seasonalStatus']=status
data['seasonalSource']=dict(baseGameVersion=data['gameVersion'],baseCommit=commit,headerSha256=hashlib.sha256(header).hexdigest(),note='Proposed v0.0.63 tables; not in the published v0.0.62 ROM.' if status=='preview' else 'Read from pinned game source.')
data['methodNote']='Percentages are conditional encounter shares for the selected method and season, not chances per step. Native lure/ability modifiers, scripted encounters and gifts are separate.'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'Imported {len(tables)} seasonal tables ({status}); all tables total 100%.')
