"""Pinned seasonal imports preserve base tables and remove stale future batches."""
from pathlib import Path
import copy, json, re, subprocess, tempfile
R=Path(__file__).resolve().parents[1]
base=json.loads((R/'docs/wiki/dex-data.json').read_text())
base['sourceCommit']=subprocess.check_output(['git','rev-parse','HEAD'],cwd=R,text=True).strip()
# Start from the protected sixteen-table grass snapshot, even after Surf ships.
for m in base['maps']:
 if m['id'] in [f'MAP_ROUTE{r}' for r in range(105,113)]:
  for method in m['methods']:
   if method['id'] in ['surf','land']:method.pop('seasonalVariants',None)
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'snapshot.json';p.write_text(json.dumps(base))
 def build(header):
  subprocess.run(['python3',str(R/'tools/build_wiki_seasons.py'),'--snapshot',str(p),'--preview-header',str(R/header)],cwd=R,check=True)
  return json.loads(p.read_text())
 new=build('src/data/legends_seasonal_encounters.h')
 assert new['seasonalStatus']=='preview' and new['species']==base['species']
 changed=[]
 for a,b in zip(base['maps'],new['maps']):
  if a!=b:
   assert a['id'] in [f'MAP_ROUTE{r}' for r in range(105,113)]
   for x,y in zip(a['methods'],b['methods']):
    if x!=y:
     assert x['id'] in ['surf','land'] and x['entries']==y['entries'] and len(y['seasonalVariants'])==4
     assert all(sum(e['rate'] for e in v['entries'])==100 for v in y['seasonalVariants'])
   changed.append(a['id'])
 assert len(changed)==8
 # Import the previous thirty-two-table generation after the newer snapshot.
 header=(R/'src/data/legends_seasonal_encounters.h').read_text()
 header=re.sub(r'static const struct WildPokemon sRoute(?:109|110|111|112)(?:Spring|Summer|Autumn|Winter)(?:Water)?Mons.*?=\s*\{.*?\};', '',header,flags=re.S)
 previous=Path(d)/'previous-header.h';previous.write_text(header)
 prior=build(previous)
 expected=copy.deepcopy(base['maps'])
 for m in expected:
  if m['id'] in [f'MAP_ROUTE{r}' for r in range(105,109)]:
   current=next(x for x in new['maps'] if x['id']==m['id'])
   for method in m['methods']:
    if method['id']=='surf':method['seasonalVariants']=next(x for x in current['methods'] if x['id']=='surf')['seasonalVariants']
 assert prior['maps']==expected,'previous headers must remove only the newer route batch'
 old=build('preview-inputs/seasonal-encounters.h')
 assert old['maps']==base['maps'], 'old pinned headers must not retain stale future Surf tables'
print('PASS: pinned land/Surf import, only eight intended methods changed, original data retained, 48/32/16-table imports removed stale future variants')
