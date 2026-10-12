"""Exercise northern survey persistence, native encounter levels and imported geometry."""
import importlib.util,itertools,json,struct,unittest,re
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('challenge',R/'test/legends-kanto-challenge.test.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
class Events(c.Events):
 def __init__(self):super().__init__();self.outcome='B_OUTCOME_WON';self.removed=False
 def run(self,label,answers=()):
  self.answers=list(answers);pc=c.labels[label];stack=[]
  for _ in range(200):
   line=c.commands[pc];pc+=1;op,_,rest=line.partition(' ');a=[s.strip() for s in rest.split(',')]
   if op=='end':return self
   if op=='return':
    if not stack:return self
    pc=stack.pop()
   elif op=='goto':pc=c.labels[a[0]]
   elif op in ('goto_if_set','goto_if_unset'):
    if (a[0] in self.flags)==(op=='goto_if_set'):pc=c.labels[a[1]]
   elif op in ('goto_if_eq','goto_if_ne'):
    if (self.value(a[0])==self.value(a[1]))==(op=='goto_if_eq'):
     if a[2]=='Common_EventScript_NopReturn':
      if not stack:return self
      pc=stack.pop()
     else:pc=c.labels[a[2]]
   elif op=='call_if_set':
    if a[0] in self.flags:stack.append(pc);pc=c.labels[a[1]]
   elif op=='setflag':self.flags.add(a[0])
   elif op=='clearflag':self.flags.discard(a[0])
   elif op=='setvar':self.vars[a[0]]=int(a[1])
   elif op=='msgbox':
    self.messages.append(a[0])
    if a[1]=='MSGBOX_YESNO':self.vars['VAR_RESULT']=self.answers.pop(0)
   elif op=='setwildbattle':self.battles.append(a);assert a==['SPECIES_ZAPDOS','50']
   elif op=='specialvar':assert a[1]=='GetBattleOutcome';self.vars[a[0]]=self.outcome
   elif op=='special':
    assert a==['BattleSetup_StartLegendaryBattle']
    if self.lose:return self
   elif op=='removeobject':self.removed=True
   elif op not in ('lockall','releaseall','faceplayer','playmoncry','waitmoncry','delay','closemessage','waitse'):raise AssertionError(op)
  raise AssertionError('unterminated script')
PREFIX='FLAG_LEGENDS_KANTO_'
class Chapter3(unittest.TestCase):
 def ready(self):e=Events();e.flags.add(PREFIX+'SURVEY_FIELD_REPORT');return e
 def test_no_sequence_breaks(self):
  for label in ('Journal','WestRelay','EastRelay','Zapdos','PlantGuide'):
   e=Events().run('LegendsKanto_Chapter3_'+label);self.assertEqual(e.flags,set());self.assertEqual(e.battles,[])
  for west,east in itertools.product((0,1),repeat=2):
   if west and east:continue
   e=self.ready()
   for v,f in ((west,'WEST_RELAY'),(east,'EAST_RELAY')):
    if v:e.flags.add(PREFIX+f)
   e.run('LegendsKanto_Chapter3_Zapdos');self.assertNotIn(PREFIX+'ZAPDOS_SEEN',e.flags)
 def test_either_order_observation_without_battle_report_once(self):
  for order in itertools.permutations(('West','East')):
   e=self.ready()
   for side in order:
    label='LegendsKanto_Chapter3_'+side+'Relay';e.run(label,[0]);self.assertNotIn(PREFIX+side.upper()+'_RELAY',e.flags)
    e.run(label,[1]);before=e.flags.copy();e.run(label);self.assertEqual(e.flags,before)
   e.run('LegendsKanto_Chapter3_Journal');self.assertNotIn(PREFIX+'SURVEY_POWER_REPORT',e.flags)
   e.run('LegendsKanto_Chapter3_Zapdos',[0]);self.assertIn(PREFIX+'ZAPDOS_SEEN',e.flags);self.assertFalse(e.removed);self.assertEqual(e.battles,[])
   e.run('LegendsKanto_Chapter3_Journal');self.assertIn(PREFIX+'SURVEY_POWER_REPORT',e.flags)
   e.run('LegendsKanto_Chapter3_Journal');self.assertEqual(e.messages.count('LegendsKanto_Chapter3_Text_Report'),1)
 def test_native_legendary_capture_and_retry(self):
  for outcome in ('B_OUTCOME_CAUGHT','B_OUTCOME_WON','B_OUTCOME_RAN','B_OUTCOME_LOST'):
   e=self.ready();e.flags.update({PREFIX+'WEST_RELAY',PREFIX+'EAST_RELAY'});e.outcome=outcome;e.lose=outcome=='B_OUTCOME_LOST'
   e.run('LegendsKanto_Chapter3_Zapdos',[1]);self.assertEqual(PREFIX+'ZAPDOS_CAUGHT' in e.flags,outcome=='B_OUTCOME_CAUGHT')
   if outcome=='B_OUTCOME_CAUGHT':e.run('LegendsKanto_Chapter3_Zapdos');self.assertEqual(len(e.battles),1)
   elif not e.lose:e.run('LegendsKanto_Chapter3_Zapdos',[1]);self.assertEqual(len(e.battles),2)
   callback=self.ready();callback.flags.add('FLAG_SYS_CTRL_OBJ_DELETE');callback.outcome=outcome;callback.run('LegendsKanto_Chapter3_OnResume');self.assertEqual(PREFIX+'ZAPDOS_CAUGHT' in callback.flags,outcome=='B_OUTCOME_CAUGHT')
 def test_native_levels_all_populated_kanto_maps(self):
  wild=json.loads((R/'src/data/wild_encounters.json').read_text())['wild_encounter_groups'][0]['encounters'];by={e['map']:e for e in wild if e['base_label'].endswith('_FireRed')};count=0
  for e in wild:
   if not e['map'].startswith('MAP_LEGENDS_KANTO_'):continue
   native=by[e['map'].replace('MAP_LEGENDS_KANTO_','MAP_')];count+=1
   for field in ('land_mons','water_mons','fishing_mons','rock_smash_mons'):
    if field not in e:continue
    self.assertEqual([(m['min_level'],m['max_level']) for m in e[field]['mons']],[(m['min_level'],m['max_level']) for m in native[field]['mons']],(e['map'],field))
  self.assertGreaterEqual(count,16)
 def test_native_dialogue_width(self):
  chars={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)};chars["'"]=0xb4
  widths=list(map(int,re.findall(r'\d+',(R/'src/fonts.c').read_text().split('gFontNormalLatinGlyphWidths[] = {')[1].split('};')[0])))
  for line in re.findall(r'\.string "(.*?)"',(R/'data/scripts/legends_kanto_chapter3.inc').read_text()):
   text=re.sub(r'\\[npl]|\$','',line);self.assertLessEqual(sum(widths[chars[c]] for c in text),208,text)
 def test_geometry_and_warp_indices(self):
  maps={d['id']:d for p in (R/'data/maps').glob('*/map.json') if (d:=json.loads(p.read_text()))};layouts={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
  for item in json.loads((R/'data/legends_kanto_chapter3.json').read_text())['maps']:
   d=maps[item['id']];l=layouts[d['layout']];buf=(R/l['blockdata_filepath']).read_bytes()
   def block(x,y):return struct.unpack_from('<H',buf,2*(y*l['width']+x))[0]
   for o in d['object_events']:
    # Nurse stands behind her native counter. All walking guides and Zapdos use floor.
    if o['graphics_id']!='OBJ_EVENT_GFX_NURSE':self.assertFalse(block(o['x'],o['y'])&0xC00,(item,o))
   for w in d['warp_events']:
    target=maps[w['dest_map']];self.assertLess(int(w['dest_warp_id']),len(target['warp_events']))
   for bg in d['bg_events']:
    if 'Relay' in bg.get('script',''):
     self.assertTrue(block(bg['x'],bg['y'])&0xC00)
     self.assertTrue(any(not block(bg['x']+dx,bg['y']+dy)&0xC00 for dx,dy in ((1,0),(-1,0),(0,1),(0,-1))))
if __name__=='__main__':unittest.main()
