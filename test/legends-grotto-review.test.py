"""Review-map reachability, safe route returns and preserved published map IDs."""
import json
import hashlib
from pathlib import Path
import struct
import unittest

R = Path(__file__).resolve().parents[1]

def read(path): return json.loads((R/path).read_text())
def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
BASE = read('docs/qa/hidden-grottos-baseline.json')
def cells(layout):
    return struct.unpack('<%dH' % (layout['width']*layout['height']), (R/layout['blockdata_filepath']).read_bytes())

class Grottos(unittest.TestCase):
    def test_append_only_ids_and_unchanged_routes(self):
        after = read('data/maps/map_groups.json')
        self.assertEqual(list(BASE['groups']),list(after))
        for group, before in BASE['groups'].items():
            self.assertEqual(before['sha256'], digest(after[group][:before['count']]))
        layouts = read('data/layouts/layouts.json')['layouts']
        self.assertEqual(BASE['layouts_sha256'],digest(layouts[:BASE['layout_count']]))
        for route in ['PetalburgWoods','Route114','Route119']:
            p=f'data/maps/{route}/map.json'; current=read(p)
            new=current['bg_events'].pop()
            self.assertTrue(new['script'].startswith('LegendsGrotto_Enter'))
            self.assertEqual(BASE['routes'][route]['map_json_sha256'],digest(current))
            # Exact original metatiles/collisions, scripts and all existing events.
            for f in ['data/layouts/'+route+'/map.bin','data/maps/'+route+'/scripts.inc']:
                self.assertEqual(BASE['routes'][route]['files'][f],hashlib.sha256((R/f).read_bytes()).hexdigest())

    def test_reach_every_interaction_and_exit(self):
        layouts = {l['id']:l for l in read('data/layouts/layouts.json')['layouts']}
        for key in ['Leafshade','Stillwater','Rainroot']:
            m=read(f'data/maps/LegendsGrotto_{key}/map.json');l=layouts[m['layout']];a=cells(l);w=l['width'];h=l['height']
            blocked={(o['x'],o['y']) for o in m['object_events']}
            def walkable(x,y):return 0<=x<w and 0<=y<h and not a[y*w+x]&0xC00 and (x,y) not in blocked
            seen={(11,14)};pending=list(seen)
            while pending:
                x,y=pending.pop()
                for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if v not in seen and walkable(*v):seen.add(v);pending.append(v)
            self.assertIn((11,11),seen)
            for obj in m['object_events']+m['bg_events'][1:]:
                x,y=obj['x'],obj['y'];self.assertTrue(any(p in seen for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]),(key,obj))
            for e in m['coord_events']:self.assertIn((e['x'],e['y']),seen)
            self.assertTrue(m['coord_events'])
            self.assertFalse(m['allow_escaping']);self.assertFalse(m['allow_cycling'])
            self.assertFalse(m['requires_flash'])

    def test_entrances_have_safe_returns_and_no_event_collisions(self):
        layouts = {l['id']:l for l in read('data/layouts/layouts.json')['layouts']}
        for route,approach in [('PetalburgWoods',(13,32)),('Route114',(15,40)),('Route119',(28,105))]:
            m=read(f'data/maps/{route}/map.json');l=layouts[m['layout']];a=cells(l);entry=m['bg_events'][-1]
            self.assertEqual(a[approach[1]*l['width']+approach[0]]&0xC00,0)
            self.assertEqual(abs(entry['x']-approach[0])+abs(entry['y']-approach[1]),1)
            self.assertFalse(any(o['x']==approach[0] and o['y']==approach[1] for o in m['object_events']))
            self.assertFalse(any(e['x']==entry['x'] and e['y']==entry['y'] for e in m['bg_events'][:-1]))

if __name__=='__main__':unittest.main()
