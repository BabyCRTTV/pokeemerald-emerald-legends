"""Exercise actual challenge event branches, persistence and playable geometry."""
import json,re,struct,unittest,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
source=(R/'data/scripts/legends_kanto_challenge.inc').read_text();labels={};commands=[]
for line in source.splitlines():
 line=line.strip()
 if re.fullmatch(r'\w+::?',line):labels[line.rstrip(':')]=len(commands)
 elif line and not line.startswith(('@','.')):commands.append(line)
class Events:
 def __init__(self):self.flags=set();self.vars={};self.answers=[];self.battles=[];self.messages=[];self.lose=False
 def value(self,x):return {'YES':1,'NO':0,'TRUE':1}.get(x,self.vars.get(x,int(x) if x.isdigit() else x))
 def run(self,label,answers=()):
  self.answers=list(answers);pc=labels[label]
  for _ in range(150):
   line=commands[pc];pc+=1;op,_,rest=line.partition(' ');a=[s.strip() for s in rest.split(',')]
   if op=='end':return self
   if op=='goto':pc=labels[a[0]]
   elif op in ('goto_if_set','goto_if_unset'):
    if (a[0] in self.flags)==(op=='goto_if_set'):pc=labels[a[1]]
   elif op=='goto_if_eq':
    if self.value(a[0])==self.value(a[1]):pc=labels[a[2]]
   elif op=='setvar':self.vars[a[0]]=int(a[1])
   elif op=='setflag':self.flags.add(a[0])
   elif op=='msgbox':
    self.messages.append(a[0])
    if a[1]=='MSGBOX_YESNO':self.vars['VAR_RESULT']=self.answers.pop(0)
   elif op=='trainerbattle_single':
    self.battles.append(a[0])
    if self.lose:return self # Engine blackouts abort this script on defeat.
   elif op not in ('lockall','releaseall','faceplayer'):raise AssertionError(op)
  raise AssertionError('Script did not terminate')
class ChallengeTests(unittest.TestCase):
 def test_both_modes_share_one_permanent_victory(self):
  for gym in ('Surge','Koga'):
   for champion in (0,1):
    e=Events();pre='LegendsKanto_'+gym;flag='FLAG_LEGENDS_KANTO_'+gym.upper()+'_WON'
    e.run(pre+'_Entry',[champion]);self.assertIn('LegendsKanto_Text_OneWin',e.messages)
    e.run(pre+'_Leader',[1]);self.assertIn(flag,e.flags);self.assertEqual(len(e.battles),1)
    self.assertTrue(e.battles[0].endswith('CHAMPION' if champion else 'STANDARD'))
    e.run(pre+'_Entry',[1-champion]);e.run(pre+'_Leader',[1]);self.assertEqual(len(e.battles),1)
    self.assertFalse(any('BADGE' in f or f.startswith('FLAG_DEFEATED') for f in e.flags))
 def test_loss_and_decline_allow_reselection(self):
  for gym in ('Surge','Koga'):
   e=Events();pre='LegendsKanto_'+gym;e.run(pre+'_Entry',[1]);e.run(pre+'_Leader',[0]);self.assertEqual(e.battles,[])
   e.lose=True;e.run(pre+'_Leader',[1]);self.assertEqual(e.flags,set())
   e.lose=False;e.run(pre+'_Entry',[0]);e.run(pre+'_Leader',[1]);self.assertTrue(e.battles[-1].endswith('STANDARD'))
 def test_report_in_either_order_and_only_once(self):
  for order in [('Surge','Koga'),('Koga','Surge')]:
   e=Events();e.run('LegendsKanto_Survey_Aide');self.assertIn('FLAG_LEGENDS_KANTO_SURVEY_STARTED',e.flags)
   for gym in order:
    e.run('LegendsKanto_'+gym+'_Entry',[0]);e.run('LegendsKanto_'+gym+'_Leader',[1]);e.run('LegendsKanto_Survey_Aide')
   self.assertIn('FLAG_LEGENDS_KANTO_SURVEY_REPORT',e.flags)
   e.run('LegendsKanto_Survey_Aide');self.assertEqual(e.messages.count('LegendsKanto_Text_SurveyReport'),1)
 def test_gym_entrance_coverage_and_npc_positions(self):
  layouts={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
  for name,gym in [('VermilionCity_Gym','Surge'),('FuchsiaCity_Gym','Koga')]:
   d=json.loads((R/f'data/maps/LegendsKanto_{name}/map.json').read_text());l=layouts[d['layout']];b=(R/l['blockdata_filepath']).read_bytes()
   def block(x,y):return struct.unpack_from('<H',b,2*(y*l['width']+x))[0]
   self.assertEqual({c['x'] for c in d['coord_events']},{w['x'] for w in d['warp_events']})
   for c in d['coord_events']:self.assertFalse(block(c['x'],c['y'])&0xC00)
   self.assertEqual(d['object_events'][0]['graphics_id'],'OBJ_EVENT_GFX_LT_SURGE' if gym=='Surge' else 'OBJ_EVENT_GFX_KOGA')
   for o in d['object_events']:self.assertFalse(block(o['x'],o['y'])&0xC00,(name,o))
 def test_gym_raw_graphics_visible_to_emerald(self):
  active=subprocess.check_output(['cpp','-P','-DIS_FRLG=0',str(R/'src/data/object_events/object_event_graphics.h')],text=True)
  for name in ('LtSurge','Koga','GymGuy'):self.assertIn('const u16 gObjectEventPic_'+name+'[]',active)
 def test_unique_layouts_and_emerald_script_includes(self):
  layouts=json.loads((R/'data/layouts/layouts.json').read_text())['layouts'];self.assertEqual(len(layouts),len({l['id'] for l in layouts}))
  includes=(R/'data/event_scripts.s').read_text()
  for entry in json.loads((R/'data/legends_kanto_chapter1.json').read_text())['maps']:
   self.assertIn('data/maps/'+entry['name']+'/scripts.inc',includes)
 def test_encounters_and_teams(self):
  groups=json.loads((R/'src/data/wild_encounters.json').read_text())['wild_encounter_groups'];entries=[e for g in groups for e in g['encounters'] if e.get('map','').startswith('MAP_LEGENDS_KANTO_ROUTE')]
  self.assertEqual(len(entries),12)
  for e in entries:
   for field in ('land_mons','water_mons','fishing_mons'):
    for m in e.get(field,{}).get('mons',[]):self.assertTrue(46<=m['min_level']<=m['max_level']<=54)
  parties=(R/'src/data/trainers.party').read_text()
  for gym in ('SURGE','KOGA'):
   for mode,count in [('STANDARD',4),('CHAMPION',6)]:
    section=parties.split('=== TRAINER_LEGENDS_KANTO_'+gym+'_'+mode+' ===')[1].split('===')[0]
    levels=list(map(int,re.findall(r'^Level: (\d+)',section,re.M)));self.assertEqual(len(levels),count)
    self.assertTrue(all(52<=l<=60 if mode=='STANDARD' else 72<=l<=80 for l in levels))
if __name__=='__main__':unittest.main()
