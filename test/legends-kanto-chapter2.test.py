"""Chapter-two event execution, native warps/geometry, and actual flag resolver."""
import importlib.util,itertools,json,re,struct,subprocess,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('chapter',R/'test/legends-kanto-challenge.test.py');chapter=importlib.util.module_from_spec(spec);spec.loader.exec_module(chapter)
class ChapterTwo(unittest.TestCase):
 def test_chapter_commands_are_native_event_macros(self):
  macros=set()
  for p in (R/'asm/macros').glob('*.inc'):
   macros.update(re.findall(r'\.macro\s+(\w+)',p.read_text()))
  for line in (R/'data/scripts/legends_kanto_chapter2.inc').read_text().splitlines():
   if line.startswith('\t') and not line.lstrip().startswith(('.', '@')):
    self.assertIn(line.split()[0],macros,line)

 def test_fieldwork_gates_decline_revisit_and_either_order(self):
  for site,gym in [('Leaves','ERIKA'),('Echo','SABRINA')]:
   flag='FLAG_LEGENDS_KANTO_SURVEY_'+site.upper()
   for opening,won in itertools.product((False,True),repeat=2):
    e=chapter.Events()
    if opening:e.flags.add('FLAG_LEGENDS_KANTO_SURVEY_REPORT')
    if won:e.flags.add('FLAG_LEGENDS_KANTO_'+gym+'_WON')
    before=e.flags.copy();e.run('LegendsKanto_Chapter2_'+site,[0]);self.assertEqual(before,e.flags)
    e.run('LegendsKanto_Chapter2_'+site,[1]);self.assertEqual(flag in e.flags,opening and won)
    before=e.flags.copy();e.run('LegendsKanto_Chapter2_'+site);self.assertEqual(e.flags,before)
  for order in [('Leaves','Echo'),('Echo','Leaves')]:
   e=chapter.Events();e.flags.update({'FLAG_LEGENDS_KANTO_SURGE_WON','FLAG_LEGENDS_KANTO_KOGA_WON'})
   e.run('LegendsKanto_Survey_Aide',[0])
   for gym in ['Erika','Sabrina']:e.run('LegendsKanto_'+gym+'_Entry',[0]);e.run('LegendsKanto_'+gym+'_Leader',[1])
   for site in order:e.run('LegendsKanto_Chapter2_'+site,[1])
   e.run('LegendsKanto_Survey_Aide',[0]);e.run('LegendsKanto_Survey_Aide',[0])
   self.assertEqual(e.messages.count('LegendsKanto_Text_Chapter2Report'),1)
   self.assertEqual(e.messages.count('LegendsKanto_Text_SurveyReport'),1)
 def test_journal_lists_only_missing_tasks_and_does_not_skip_gates(self):
  for bits in itertools.product((False,True),repeat=4):
   e=chapter.Events();e.flags.add('FLAG_LEGENDS_KANTO_SURVEY_REPORT')
   for bit,flag in zip(bits,['ERIKA_WON','SABRINA_WON','SURVEY_LEAVES','SURVEY_ECHO']):
    if bit:e.flags.add('FLAG_LEGENDS_KANTO_'+flag)
   e.run('LegendsKanto_Chapter2_Journal')
   self.assertEqual('LegendsKanto_Text_NeedErika' in e.messages,not bits[0])
   self.assertEqual('LegendsKanto_Text_NeedSabrina' in e.messages,not bits[1])
   self.assertEqual('LegendsKanto_Text_NeedLeaves' in e.messages,bits[0] and not bits[2])
   self.assertEqual('LegendsKanto_Text_NeedEcho' in e.messages,bits[1] and not bits[3])
   self.assertEqual('FLAG_LEGENDS_KANTO_SURVEY_FIELD_REPORT' in e.flags,all(bits))
 def test_native_rooms_exit_and_teleport_slots(self):
  layouts={x['id']:x for x in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
  for city,leader,idx in [('Celadon','Erika',6),('Saffron','Sabrina',3)]:
   d=json.loads((R/f'data/maps/LegendsKanto_{city}City_Gym/map.json').read_text());native=json.loads((R/f'data/maps/{city}City_Gym_Frlg/map.json').read_text());l=layouts[d['layout']];nl=layouts[native['layout']]
   self.assertEqual((R/l['blockdata_filepath']).read_bytes(),(R/nl['blockdata_filepath']).read_bytes())
   b=(R/l['blockdata_filepath']).read_bytes()
   for o in d['object_events']+d['coord_events']:
    block=struct.unpack_from('<H',b,2*(o['y']*l['width']+o['x']))[0];self.assertEqual(block&0xC00,0,(city,o))
   self.assertEqual({c['x'] for c in d['coord_events']},{w['x'] for w in d['warp_events'][:3]})
   for a,n in zip(d['warp_events'],native['warp_events']):
    self.assertEqual((a['x'],a['y'],a['dest_warp_id']),(n['x'],n['y'],n['dest_warp_id']))
   outdoor=json.loads((R/f'data/maps/LegendsKanto_{city}City/map.json').read_text());self.assertEqual(outdoor['warp_events'][idx]['dest_map'],d['id'])
   self.assertFalse(any(o.get('target_map','').startswith('MAP_ROUTE') for o in outdoor['object_events']))
  # Native warp chain documented by staff: entry, TL, BL, BL reaches Sabrina's room.
  d=json.loads((R/'data/maps/LegendsKanto_SaffronCity_Gym/map.json').read_text())
  self.assertEqual([d['warp_events'][i]['dest_warp_id'] for i in [3,25,22,5]],['32','27','4','20'])
 def test_actual_trainer_flag_mapping_and_partner_separation(self):
  program='''#include <assert.h>
#include <stdint.h>
typedef uint16_t u16;
#define IS_FRLG 0
#include "constants/opponents.h"
#define TRAINER_FLAGS_START 0x500
#define FLAG_LEGENDS_KANTO_ERIKA_WON 0x272
#define FLAG_LEGENDS_KANTO_SABRINA_WON 0x273
#include "legends_trainer_flags.h"
int main(void) {
assert(MAX_TRAINERS_COUNT == 864);
assert(TRAINER_FLAGS_START + MAX_TRAINERS_COUNT == 0x860);
for (int i=0;i<864;i++) assert(LegendsTrainerFlag(i)==0x500+i);
assert(LegendsTrainerFlag(864)==0x272 && LegendsTrainerFlag(865)==0x272);
assert(LegendsTrainerFlag(866)==0x273 && LegendsTrainerFlag(867)==0x273);
assert(TRAINERS_COUNT == 868 && TRAINER_PARTNER(PARTNER_STEVEN)==869);
assert(LegendsTrainerFlag(TRAINER_PARTNER(PARTNER_STEVEN))==0);
assert(LegendsTrainerFlag(65535)==0);
}'''
  debug=(R/'src/debug.c').read_text()
  toggle='static void DebugToggleTrainerFlag'+debug.split('static void DebugToggleTrainerFlag',1)[1].split('\n}\n',1)[0]+'\n}\n'
  stubs="""static int bits[0x900];
static int HasTrainerBeenFought(u16 id) {return bits[LegendsTrainerFlag(id)];}
static void SetTrainerFlag(u16 id) {u16 f=LegendsTrainerFlag(id);if(f)bits[f]=1;}
static void ClearTrainerFlag(u16 id) {u16 f=LegendsTrainerFlag(id);if(f)bits[f]=0;}
"""
  program=program.replace('int main(void) {',stubs+toggle+'int main(void) {')
  program=program.replace('assert(MAX_TRAINERS_COUNT',"""for(int id=0;id<868;id++) {
 DebugToggleTrainerFlag(id);assert(bits[LegendsTrainerFlag(id)]==1);
 for(int f=0x860;f<0x900;f++)assert(bits[f]==0);
 DebugToggleTrainerFlag(id);assert(bits[LegendsTrainerFlag(id)]==0);
}
assert(MAX_TRAINERS_COUNT""")
  self.assertNotRegex(debug,r'TRAINER_FLAGS_START\s*\+')
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'t.c').write_text(program);subprocess.run(['gcc','-I'+str(R/'include'),str(p/'t.c'),'-o',str(p/'t')],check=True);subprocess.run([str(p/'t')],check=True)
  # Every native trainer flag access in battle setup must use the resolver.
  self.assertNotRegex((R/'src/battle_setup.c').read_text(),r'TRAINER_FLAGS_START\s*\+')
 def test_native_emerald_leader_graphics_are_defined(self):
  active=subprocess.check_output(['cpp','-P','-DIS_FRLG=0',str(R/'src/data/object_events/object_event_graphics.h')],text=True)
  for leader in ['Erika','Sabrina','CuttableTreeFrlg']:self.assertIn('const u16 gObjectEventPic_'+leader+'[]',active)
  for file in ['object_event_graphics_info.h','object_event_pic_tables.h','object_event_graphics_info_pointers.h']:
   active=subprocess.check_output(['cpp','-P','-DIS_FRLG=0',str(R/'src/data/object_events'/file)],text=True)
   for leader in ['Erika','Sabrina','CuttableTreeFrlg']:self.assertIn(leader,active)
if __name__=='__main__':unittest.main()
