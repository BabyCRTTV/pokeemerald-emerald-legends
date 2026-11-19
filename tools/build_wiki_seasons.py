#!/usr/bin/env python3
"""Explicitly import pinned seasonal encounter tables during an owner-requested review.

An external header is allowed only for an UNPUBLISHED preview, with a recorded hash.
No date/time restrictions are inferred from species lore.
"""
import argparse, hashlib, json, re, subprocess
from collections import defaultdict
from pathlib import Path
R=Path(__file__).resolve().parents[1]; W=R/'docs/wiki'
SEASONS=['spring','summer','autumn','winter']
parser=argparse.ArgumentParser();parser.add_argument('--preview-header',type=Path);parser.add_argument('--snapshot',type=Path,default=W/'dex-data.json');args=parser.parse_args()
p=args.snapshot;data=json.loads(p.read_text());commit=data['sourceCommit']
def read(path):return subprocess.check_output(['git','show',commit+':'+path],cwd=R)
if args.preview_header:
 header=args.preview_header.read_bytes();status='preview'
else:
 path='src/data/legends_seasonal_encounters.h'
 if subprocess.run(['git','cat-file','-e',commit+':'+path],cwd=R,stderr=subprocess.DEVNULL).returncode:raise SystemExit('Pinned game has no seasonal tables; no changes made.')
 header=read(path);status='published'
source=json.loads(read('src/data/wild_encounters.json'))['wild_encounter_groups'][0]
weights={f['type']:f['encounter_rates'] for f in source['fields']}
tables={}
for kanto,route,season,water,body in re.findall(r'static const struct WildPokemon s(Kanto)?Route([0-9]+(?:_NORTH|_SOUTH)?)(Spring|Summer|Autumn|Winter)(Water)?Mons.*?=\s*\{(.*?)\};',header.decode(),re.S):
 method='surf' if water else 'land';native=weights['water_mons' if water else 'land_mons']
 slots=re.findall(r'\{(\d+),\s*(\d+),\s*SPECIES_(\w+)\}',body);assert len(slots)==len(native)
 entries={}
 for (lo,hi,species),rate in zip(slots,native):
  e=entries.setdefault(species,dict(id=species,min=101,max=0,rate=0,time='all-day',seasons=[]))
  e.update(min=min(e['min'],int(lo)),max=max(e['max'],int(hi)),rate=e['rate']+rate)
 assert sum(e['rate'] for e in entries.values())==100
 route=('Kanto' if kanto else '')+route
 tables[(route,method,season.lower())]=list(entries.values())
kanto_initial={(f'Kanto{r}','land') for r in range(1,5)}
kanto_expansion=(
 {(f'Kanto{r}','land') for r in [*range(6,19),'21_NORTH']}
 | {(f'Kanto{r}','surf') for r in [19,20,'21_NORTH','21_SOUTH']}
)
hoenn_surf_expansion={('115','surf'),('118','surf')}
kanto_surf_expansion={('Kanto12','surf'),('Kanto13','surf')}
remaining_hoenn_surf={(str(r),'surf') for r in (102,103,104,110,111,114,117,119,120,121,123)}
remaining_kanto_surf={(f'Kanto{r}','surf') for r in (4,6,10,11)}
kanto={key for key in tables if key[0].startswith('Kanto')}
assert kanto in [set(),*[
 {(route,method,season) for route,method in batch for season in SEASONS}
 for batch in [kanto_initial,kanto_initial|kanto_expansion,kanto_initial|kanto_expansion|kanto_surf_expansion,kanto_initial|kanto_expansion|kanto_surf_expansion|remaining_kanto_surf]
]]
land={key for key in tables if key[1]=='land' and key not in kanto}
assert land in [{(str(r),'land',s) for r in routes for s in SEASONS} for routes in [range(101,105),[*range(101,105),110,111,112],[*range(101,105),*range(110,117)],[*range(101,105),*range(110,122)],[*range(101,105),*range(110,122),123],[*range(101,105),*range(110,122),123,130]]]
water={key for key in tables if key[1]=='surf' and key not in kanto}
assert not water or water in [{(str(r),'surf',s) for r in routes for s in SEASONS} for routes in [range(105,109),range(105,110),[*range(105,110),122,124,125,126],[*range(105,110),122,*range(124,132)],[*range(105,110),122,*range(124,135)],[*range(105,110),115,118,122,*range(124,135)],[102,103,104,*range(105,112),114,115,*range(117,135)]]]
assert (len(land),len(water)) in [(16,0),(16,16),(28,20),(44,20),(64,20),(68,36),(68,56),(68,68),(68,76),(72,120)]
managed=(
 {(str(r),'land') for r in [*range(101,105),*range(110,122),123]}
 | {(str(r),'surf') for r in [*range(105,110),122,*range(124,135)]}
 | remaining_kanto_surf | remaining_hoenn_surf | {('130','land')}
 | kanto_initial | kanto_expansion | hoenn_surf_expansion | kanto_surf_expansion
)
forms=[dict(id='SANDSHREW_ALOLA',formOf='SANDSHREW',num=None,name='Alolan Sandshrew',types=['ICE','STEEL'],category='Mouse',stats=[50,75,90,10,35,40],sprite='sandshrew/alola',crySpecies='SANDSHREW'),dict(id='DEERLING_AUTUMN',formOf='DEERLING',num=None,name='Autumn Deerling',types=['NORMAL','GRASS'],category='Season',stats=[60,60,50,40,50,75],sprite='deerling/autumn',crySpecies='DEERLING')]
for form in forms:
 if not any(p['id']==form['id'] for p in data['species']):data['species'].append(form)
known={p['id'] for p in data['species']}
for m in data['maps']:
 route=m['id'].replace('MAP_LEGENDS_KANTO_ROUTE','Kanto',1) if m['id'].startswith('MAP_LEGENDS_KANTO_ROUTE') else m['id'].removeprefix('MAP_ROUTE')
 for method in m['methods']:
  key=method['id']
  if (route,key,'spring') not in tables:
   if (route,key) in managed:method.pop('seasonalVariants',None)
   continue
  method['seasonalVariants']=[]
  for season in SEASONS:
   entries=tables[(route,key,season)]
   for e in entries:
    assert e['id'] in known,e['id']
    e['seasons']=[s for s in SEASONS if any(x['id']==e['id'] for x in tables[(route,key,s)])]
   method['seasonalVariants'].append(dict(season=season,entries=sorted(entries,key=lambda x:-x['rate'])))
data['seasonalStatus']=status
data['seasonalSource']=dict(baseGameVersion=data['gameVersion'],baseCommit=commit,headerSha256=hashlib.sha256(header).hexdigest(),note='Proposed seasonal tables; not a claim they shipped in the pinned published snapshot.' if status=='preview' else 'Read from pinned game source.')
data['methodNote']='Percentages are conditional encounter shares for the selected method and season, not chances per step. Native lure/ability modifiers, scripted encounters and gifts are separate.'
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(f'Imported {len(tables)} seasonal tables ({status}); all tables total 100%.')
