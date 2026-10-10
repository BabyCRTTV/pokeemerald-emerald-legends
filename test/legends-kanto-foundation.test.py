"""Validate the empty native-map foundation, graph, water gates and progression."""
import importlib.util,json,struct,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('arrival',R/'test/legends-kanto.test.py');arrival=importlib.util.module_from_spec(spec);spec.loader.exec_module(arrival)
MAPS={d['id']:d for p in (R/'data/maps').glob('*/map.json') if (d:=json.loads(p.read_text()))}
LAYOUTS={d['id']:d for d in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
MANIFEST=json.loads((R/'data/legends_kanto_foundation.json').read_text())['maps']
class FoundationTests(unittest.TestCase):
 def test_population_and_native_fidelity(self):
  self.assertEqual(len(MANIFEST),30)
  encounters='\n'.join(p.read_text() for p in (R/'src/data').glob('*wild*json'))
  for item in MANIFEST:
   d=MAPS[item['id']];l=LAYOUTS[d['layout']];s=json.loads((R/('data/maps/'+item['source']+'/map.json')).read_text());sl=LAYOUTS[s['layout']]
   self.assertEqual(d['object_events'],[]);self.assertNotIn(item['id'],encounters)
   self.assertEqual((l['width'],l['height']),(sl['width'],sl['height']))
   self.assertEqual((R/l['border_filepath']).read_bytes(),(R/sl['border_filepath']).read_bytes())
   a=(R/l['blockdata_filepath']).read_bytes();b=(R/sl['blockdata_filepath']).read_bytes();self.assertEqual(len(a),len(b))
   for i in range(len(a)//2):
    new,old=struct.unpack_from('<H',a,i*2)[0],struct.unpack_from('<H',b,i*2)[0]
    if new!=old:self.assertTrue(new in (0x34F4,0x15D9) or new==old|0xC00)
   self.assertNotIn('EventScript_', (R/('data/maps/'+item['name']+'/scripts.inc')).read_text())
 def test_reciprocal_graph_and_append_only_ids(self):
  group=json.loads((R/'data/maps/map_groups.json').read_text())['gMapGroup_LegendsKanto'];self.assertEqual(group[:2],['LegendsKanto_VermilionCity','LegendsKanto_Harbor'])
  opposite={'left':'right','right':'left','up':'down','down':'up'}
  allowed={i['id'] for i in MANIFEST}|{'MAP_LEGENDS_KANTO_VERMILION_CITY'}
  visited=set();queue=['MAP_LEGENDS_KANTO_VERMILION_CITY']
  while queue:
   id=queue.pop()
   if id in visited:continue
   visited.add(id);d=MAPS[id]
   for c in d['connections'] or []:
    self.assertIn(c['map'],allowed)
    self.assertIn({'map':id,'offset':-c['offset'],'direction':opposite[c['direction']]},MAPS[c['map']]['connections'])
    queue.append(c['map'])
   queue += [w['dest_map'] for w in d['warp_events'] if w['dest_map'] in allowed]
  self.assertTrue(allowed<=visited,allowed-visited)
 def test_surf_progression_and_no_return_trap(self):
  for champion in (False,True):
   for ticket in (False,True):
    e=arrival.Events(champion,ticket).run('SurfOutbound');self.assertEqual(bool(e.warp),champion and ticket)
  self.assertIsNone(arrival.Events(True,True,answer=False).run('SurfOutbound').warp)
  e=arrival.Events().run('SurfReturn');self.assertEqual(e.warp,['MAP_ROUTE124','20','4']);self.assertEqual(e.respawn,'HEAL_LOCATION_LILYCOVE_CITY')
  e=arrival.Events(True,True).run('SurfOutbound');self.assertEqual(e.warp,['MAP_LEGENDS_KANTO_ROUTE19','12','53']);self.assertIn('ITEM_INVITE_TICKET',e.items)
 def test_surf_tiles_and_non_looping_arrivals(self):
  for id,x,y,mid in [('MAP_ROUTE124',20,4,0x170),('MAP_LEGENDS_KANTO_ROUTE19',12,53,0x12B)]:
   d=MAPS[id];l=LAYOUTS[d['layout']];data=(R/l['blockdata_filepath']).read_bytes();block=struct.unpack_from('<H',data,2*(y*l['width']+x))[0]
   self.assertEqual(block&1023,mid);self.assertEqual(block&0xC00,0);self.assertNotIn((x,y),[(c['x'],c['y']) for c in d['coord_events']])
   for c in d['coord_events']:
    b=struct.unpack_from('<H',data,2*(c['y']*l['width']+c['x']))[0];self.assertEqual(b&1023,mid);self.assertEqual(b&0xC00,0);self.assertEqual(c['var'],'VAR_TEMP_F')
if __name__=='__main__':unittest.main()
