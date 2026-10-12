"""Run finale progression, native encounter outcomes and save-safe import checks."""
import runpy,json,re,unittest,struct,subprocess,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1]
shared=runpy.run_path(str(R/'test/legends-story-expeditions.test.py'))
Events=shared['Events'];labels=shared['labels'];commands=shared['commands']
# Append actual native island entry/sign/resume scripts to the same interpreter.
for file in ('FarawayIsland_Entrance','FarawayIsland_Interior'):
 for line in (R/f'data/maps/{file}/scripts.inc').read_text().splitlines():
  line=line.strip()
  if re.fullmatch(r'\w+::?',line):labels[line.rstrip(':')]=len(commands)
  elif line and not line.startswith(('@','.','#')):commands.append(line)
F='FLAG_LEGENDS_FINAL_';S='FLAG_LEGENDS_STORY_';K='FLAG_LEGENDS_KANTO_'
GYMS=[K+n+'_WON' for n in ('SURGE','KOGA','ERIKA','SABRINA','MISTY','BROCK','BLAINE','VIRIDIAN')]
class Finale(unittest.TestCase):
 def ready(self,*flags):
  e=Events();e.flags.update(GYMS+[S+'EMBER_REPORT']);e.flags.update(F+f for f in flags);return e
 def test_eight_records_each_required(self):
  for missing in GYMS+[S+'EMBER_REPORT']:
   e=self.ready();e.flags.remove(missing);e.run('LegendsFinal_Oak');self.assertNotIn(F+'OAK_ANALYSIS',e.flags);self.assertFalse(e.items)
  e=self.ready();e.run('LegendsFinal_Oak');self.assertIn(F+'EIGHT_RECORDS',e.flags);self.assertIn(F+'VOYAGE_READY',e.flags);self.assertEqual(e.items['ITEM_OLD_SEA_MAP'],1)
 def test_both_blue_modes_decline_loss_and_one_win(self):
  for mode in (0,1):
   e=Events();e.run('LegendsFinal_GymEntry');self.assertNotIn(F+'VIRIDIAN_MODE_SET',e.flags)
   e.flags.add(S+'EMBER_REPORT');e.run('LegendsFinal_GymEntry',[mode]);e.run('LegendsFinal_Blue',[0]);self.assertFalse(e.battles)
   e.lose=True;e.run('LegendsFinal_Blue',[1]);self.assertNotIn(K+'VIRIDIAN_WON',e.flags)
   e.lose=False;e.run('LegendsFinal_Blue',[1]);self.assertIn(K+'VIRIDIAN_WON',e.flags)
   self.assertEqual(e.battles[-1],'TRAINER_LEGENDS_KANTO_BLUE_'+('CHAMPION' if mode else 'STANDARD'))
   count=len(e.battles);e.run('LegendsFinal_Blue');self.assertEqual(len(e.battles),count)
 def test_map_inventory_existing_received_full_and_retry(self):
  e=self.ready();e.bag_full=True;e.run('LegendsFinal_Oak');self.assertIn(F+'OAK_ANALYSIS',e.flags);self.assertNotIn(F+'VOYAGE_READY',e.flags)
  e.bag_full=False;e.run('LegendsFinal_Oak');e.run('LegendsFinal_Oak');self.assertEqual(e.items['ITEM_OLD_SEA_MAP'],1);self.assertEqual(e.messages.count('LegendsFinal_Text_OakAnalysis'),1)
  e=self.ready();e.items['ITEM_OLD_SEA_MAP']=1;e.bag_full=True;e.run('LegendsFinal_Oak');self.assertIn(F+'VOYAGE_READY',e.flags);self.assertEqual(e.items['ITEM_OLD_SEA_MAP'],1)
  e=self.ready();e.flags.add('FLAG_RECEIVED_OLD_SEA_MAP');e.run('LegendsFinal_Oak');self.assertFalse(e.items);self.assertNotIn(F+'VOYAGE_READY',e.flags)
 def test_voyage_native_and_legacy_caught_mew(self):
  e=Events();e.run('LegendsFinal_IslandArrival');self.assertNotIn(F+'ISLAND_VISITED',e.flags)
  e=self.ready('VOYAGE_READY','OAK_ANALYSIS');e.run('FarawayIsland_Entrance_OnTransition');self.assertIn(F+'ISLAND_VISITED',e.flags);self.assertEqual(e.respawn,'HEAL_LOCATION_LILYCOVE_CITY')
  e.flags.update({'FLAG_CAUGHT_MEW','FLAG_DEFEATED_MEW'});e.run('LegendsFinal_MewReentry');self.assertIn('FLAG_DEFEATED_MEW',e.flags)
  e.run('FarawayIsland_Entrance_EventScript_Sign');e.run('FarawayIsland_Entrance_EventScript_Sign');self.assertIn(F+'MEW_OBSERVED',e.flags);self.assertEqual(e.messages.count('LegendsFinal_Text_AlreadyCaught'),1)
  e.run('LegendsFinal_Oak');self.assertIn(F+'REPORT',e.flags)
  native=(R/'data/maps/LilycoveCity_Harbor/scripts.inc').read_text();self.assertIn('FLAG_ENABLE_SHIP_FARAWAY_ISLAND',native);self.assertIn('ITEM_OLD_SEA_MAP',native)
 def test_mew_observation_decline_and_reentry(self):
  e=self.ready('VOYAGE_READY');e.run('LegendsFinal_MewObserve',[0]);self.assertEqual(e.vars['VAR_RESULT'],0);self.assertIn(F+'MEW_OBSERVED',e.flags);self.assertFalse(e.battles)
  e.run('LegendsFinal_MewObserve',[1]);self.assertEqual(e.messages.count('LegendsFinal_Text_MewObserve'),1)
  e.flags.add('FLAG_DEFEATED_MEW');e.run('LegendsFinal_MewReentry');self.assertNotIn('FLAG_DEFEATED_MEW',e.flags)
  e=Events();e.flags.add('FLAG_DEFEATED_MEW');e.run('LegendsFinal_MewReentry');self.assertIn('FLAG_DEFEATED_MEW',e.flags)
  for outcome in ('B_OUTCOME_CAUGHT','B_OUTCOME_WON','B_OUTCOME_RAN'):
   e=Events();e.flags.add('FLAG_SYS_CTRL_OBJ_DELETE');e.outcome=outcome;e.run('FarawayIsland_Interior_EventScript_TryRemoveMew');self.assertEqual('FLAG_CAUGHT_MEW' in e.flags,outcome=='B_OUTCOME_CAUGHT')
 def test_report_and_reward_bag_pc_full_retry_exactly_once(self):
  for bag_full,pc_full in ((False,False),(True,False),(True,True)):
   e=self.ready('OAK_ANALYSIS','VOYAGE_READY','ISLAND_VISITED','MEW_OBSERVED');e.bag_full=bag_full;e.pc_full=pc_full;e.run('LegendsFinal_Oak');self.assertIn(F+'REPORT',e.flags)
   self.assertEqual(F+'REWARD' in e.flags,not(bag_full and pc_full))
   e.bag_full=False;e.pc_full=False;e.run('LegendsFinal_Oak');e.run('LegendsFinal_Oak')
   self.assertEqual(e.messages.count('LegendsFinal_Text_FinalReport'),1);self.assertEqual(e.items.get('ITEM_MASTER_BALL',0)+e.pcitems.get('ITEM_MASTER_BALL',0),1)
  e=self.ready('OAK_ANALYSIS','VOYAGE_READY','MEW_OBSERVED');e.run('LegendsFinal_Oak');self.assertNotIn(F+'REPORT',e.flags)
 def test_native_import_closures_and_reciprocal_connections(self):
  layouts={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
  maps={d['id']:d for p in (R/'data/maps').glob('*/map.json') for d in [json.loads(p.read_text())]}
  for m in json.loads((R/'data/legends_kanto_finale.json').read_text())['maps']:
   d=maps[m['id']];l=layouts[d['layout']];native=maps['MAP_'+m['source'].upper()] if 'MAP_'+m['source'].upper() in maps else json.loads((R/f'data/maps/{m["source"]}/map.json').read_text());nl=layouts[native['layout']]
   if '/LegendsKanto_' in l['blockdata_filepath'] and d['map_type'] in ('MAP_TYPE_TOWN','MAP_TYPE_CITY','MAP_TYPE_ROUTE'):
    a=words(R/l['blockdata_filepath']);b=words(R/nl['blockdata_filepath']);self.assertEqual([v&~0x400 for v in a],[v&~0x400 for v in b])
    for w in d['warp_events']:
     if w['dest_map']==d['id']:self.assertTrue(a[w['y']*l['width']+w['x']]&0x400)
   for c in d['connections']:
    back={'up':'down','down':'up','left':'right','right':'left'}[c['direction']];self.assertTrue(any(x['map']==d['id'] and x['direction']==back and x['offset']==-c['offset'] for x in maps[c['map']]['connections']),m['name'])
  self.assertEqual(len(json.loads((R/'data/maps/FarawayIsland_Interior/map.json').read_text())['object_events']),1)
 def test_actual_mew_reveal_and_grass_cleanup(self):
  native=(R/'src/faraway_island.c').read_text()
  def function(name):
   start=native.index('void '+name+'(');brace=native.index('{',start);end=brace+1;depth=1
   while depth:depth+=(native[end]=='{')-(native[end]=='}');end+=1
   return native[start:end]
  pre="""
#include <stdint.h>
#include <assert.h>
typedef uint8_t u8;
#define TRUE 1
#define FALSE 0
#define MAX_SPRITES 64
#define OBJECT_EVENTS_COUNT 16
#define FLAG_CAUGHT_MEW 458
#define LOCALID_FARAWAY_ISLAND_MEW 1
#define SUBSPRITES_IGNORE_PRIORITY 2
struct ObjectEvent {u8 spriteId,invisible,fixedPriority;} gObjectEvents[16];
struct Sprite {struct {u8 priority;} oam;u8 subpriority,subspriteMode,subspriteTableNum;} gSprites[64];
struct Save {struct {u8 mapNum,mapGroup;} location;} save,*gSaveBlock1Ptr=&save;
static u8 sGrassSpriteId=3,caught,missing,target=2,destroyed;
u8 FlagGet(int flag){return caught;}
u8 TryGetObjectEventIdByLocalIdAndMap(int l,int n,int g,u8 *id){*id=target;return missing;}
void DestroySprite(struct Sprite *s){destroyed++;}
"""
  program=pre+function('LegendsRevealSurveyMew')+function('DestroyMewEmergingGrassSprite')+"""
int main(void){
 gObjectEvents[2]=(struct ObjectEvent){4,1,0};gSprites[4].oam.priority=2;gSprites[4].subspriteTableNum=1;
 caught=1;LegendsRevealSurveyMew();assert(gObjectEvents[2].invisible && gSprites[4].oam.priority==2);
 caught=0;missing=1;LegendsRevealSurveyMew();assert(gObjectEvents[2].invisible);
 missing=0;target=16;LegendsRevealSurveyMew();assert(gObjectEvents[2].invisible);
 target=2;LegendsRevealSurveyMew();assert(!gObjectEvents[2].invisible && gSprites[4].oam.priority==1 && !gSprites[4].subspriteTableNum);
 assert(gSprites[0].oam.priority==0);DestroyMewEmergingGrassSprite();DestroyMewEmergingGrassSprite();assert(destroyed==1);
}
"""
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/'reveal.c').write_text(program);subprocess.run(['cc','-Wall','-Werror',str(p/'reveal.c'),'-o',str(p/'reveal')],check=True);subprocess.run([str(p/'reveal')],check=True)
 def test_native_oak_palette_available_in_emerald(self):
  active=subprocess.check_output(['cpp','-P','-DIS_FRLG=0',str(R/'src/data/object_events/object_event_graphics.h')],text=True)
  self.assertIn('const u16 gObjectEventPal_NpcWhite[]',active)
  self.assertIn('{gObjectEventPal_NpcWhite,              OBJ_EVENT_PAL_TAG_NPC_WHITE}',(R/'src/event_object_movement.c').read_text().split('#if IS_FRLG\n    {gObjectEventPal_PlayerFrlg')[0])
 def test_append_only_flags_and_saved_trainers(self):
  flags=(R/'include/constants/flags.h').read_text();vals=[int(v,16) for v in re.findall(r'#define FLAG_LEGENDS_FINAL_\w+ 0x([0-9A-F]+)',flags)];self.assertEqual(vals,list(range(0x2b0,0x2ba)))
  self.assertIn('#define MAX_TRAINERS_COUNT_EMERALD 864',(R/'include/constants/opponents.h').read_text())
  code=(R/'include/legends_trainer_flags.h').read_text();self.assertIn('case TRAINER_LEGENDS_KANTO_BLUE_STANDARD:',code);self.assertIn('return FLAG_LEGENDS_KANTO_VIRIDIAN_WON;',code)
def words(p):return [v[0] for v in struct.iter_unpack('<H',p.read_bytes())]
if __name__=='__main__':unittest.main()
