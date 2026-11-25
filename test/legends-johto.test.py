"""Check map exits, the complete dry footpath, badges and destinations."""
import json
import re
import struct
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def load(path):
    return json.loads((ROOT / path).read_text())
def maps(name):
    return load("data/maps/" + name + "/map.json")
def mid(name):
    return "MAP_LEGENDS_JOHTO_" + re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", name).upper()
def ws(path):
    raw = (ROOT / path).read_bytes()
    return struct.unpack(f"<{len(raw)//2}H", raw)

from collections import deque
g=load('data/maps/map_groups.json')
db={m['id']:m for m in [maps(x)for x in g['gMapGroup_LegendsJohto']+['LegendsKanto_ViridianCity']]}
ls={l['id']:l for l in load('data/layouts/layouts.json')['layouts']}
stations={'Route22':[(47,7),(8,6)],'IndigoGate':[(7,9),(7,2)],'Route26':[(16,9),(16,28)],'Route27East':[(16,0),(8,11)],'TohjoFalls':[(29,18),(16,9),(5,18)],'Route27West':[(23,11),(0,14)],'NewBarkTown':[(32,14),(11,10),(24,12),(8,21),(0,14)],'Route29':[(37,14),(0,14)],'CherrygroveCity':[(37,14),(10,18),(8,21),(14,20),(30,20),(23,9),(30,9),(16,0)],'Route30':[(14,31),(17,0)],'Route31':[(17,22),(0,12)],'VioletCity':[(41,15),(20,10),(7,14),(9,24),(29,25),(27,13),(35,24),(20,32)],'Route32':[(14,0),(22,47),(14,50)],'UnionCave':[(24,5),(23,32)],'Route33':[(19,10),(0,14)],'AzaleaTown':[(42,14),(34,9),(10,10),(24,13),(29,9),(15,22)],'SlowpokeWell':[(6,5),(15,14)],'ElmsLab':[(6,12),(6,5)],'SproutTower':[(6,11),(8,8),(12,4)],'SproutTowerBelfry':[(12,8),(7,7)],'VioletGym':[(4,9),(4,4)],'AzaleaGym':[(5,19),(5,4)]}
def tiles(k):
 m=db[mid(k)];l=ls[m['layout']];words=ws(l['blockdata_filepath']);w=l['width'];return m,[words[y:y+w]for y in range(0,len(words),w)]
def search(k,start,target=None,avoid=set()):
 m,grid=tiles(k);h=len(grid);w=len(grid[0]);blocked={(o['x'],o['y'])for o in m['object_events']};q=deque([start]);seen={start:None}
 while q and target not in seen:
  x,y=q.popleft()
  for d,(dx,dy)in {'U':(0,-1),'D':(0,1),'L':(-1,0),'R':(1,0)}.items():
   p=(x+dx,y+dy)
   if p in seen or p in blocked or ((x,y),p)in avoid or not(0<=p[0]<w and 0<=p[1]<h):continue
   v=grid[p[1]][p[0]]
   if v&0xc00 or v>>12 not in(0,3,4):continue
   seen[p]=((x,y),d);q.append(p)
 return seen
assert g['group_order'][-1] == 'gMapGroup_LegendsJohto'
assert len(g['gMapGroup_LegendsJohto']) == 36
for name, stops in stations.items():
    accessible = search(name, stops[0])
    assert set(stops) <= accessible.keys(), (name, set(stops)-accessible.keys())
opposite = {'left':'right', 'right':'left', 'up':'down', 'down':'up'}
for name in g['gMapGroup_LegendsJohto']:
    area = maps(name)
    for link in area['connections']:
        reverse = {'map':area['id'], 'offset':-link['offset'], 'direction':opposite[link['direction']]}
        assert reverse in db[link['map']]['connections'], (name, link)
    for door in area['warp_events']:
        target = db[door['dest_map']]
        assert target['warp_events'][int(door['dest_warp_id'])]['dest_map'] == area['id'], (name, door)
flags = (ROOT/'include/legends_trainer_flags.h').read_text()
events = (ROOT/'data/scripts/legends_johto.inc').read_text()
for leader, badge in [('WREN','ZEPHYR'),('RUE','HIVE')]:
    assert f'case TRAINER_LEGENDS_JOHTO_{leader}:\n        return FLAG_JOHTO_{badge}_BADGE;' in flags
    assert f'trainerbattle_single TRAINER_LEGENDS_JOHTO_{leader}' in events
for step in ['ELM_SURVEY','TIDE_READING','BELL_READING','SURVEY_RETURNED']:
    assert events.count(f'setflag FLAG_JOHTO_{step}') == 1
assert 'goto_if_unset FLAG_JOHTO_ZEPHYR_BADGE, Johto_RueGate' in events
print('36 Johto maps, dry footpaths, door returns, independent badges and survey checkpoints passed.')
