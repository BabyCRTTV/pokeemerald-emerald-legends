"""Execute shipped event branches and audit the new habitats/save contracts."""
import itertools,json,re,struct,subprocess,tempfile,unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
FILES=['legends_kanto_challenge.inc','legends_kanto_chapter2.inc','legends_kanto_chapter3.inc',
       'legends_story_common.inc','legends_seafoam.inc','legends_kanto_chapter4.inc',
       'legends_hoenn_intermission.inc','legends_kanto_chapter5.inc',
       'legends_kanto_new_gyms.inc','legends_kanto_chapter6.inc']
source='\n'.join((R/'data/scripts'/f).read_text() for f in FILES)
source+='\n'+'\n'.join((R/'data/maps'/('LegendsKanto_SeafoamIslands_'+f)/'scripts.inc').read_text() for f in ['1F','B1F','B2F','B3F','B4F'])
labels={};commands=[]
for line in source.splitlines():
 line=line.strip()
 if re.fullmatch(r'\w+::?',line):
  name=line.rstrip(':');assert name not in labels,name;labels[name]=len(commands)
 elif line and not line.startswith(('@','.','#')):commands.append(line)
F='FLAG_LEGENDS_STORY_'
class Events:
 def __init__(self):self.flags=set();self.vars={};self.messages=[];self.battles=[];self.warps=[];self.outcome='B_OUTCOME_CAUGHT';self.lose=False;self.removed=[]
 def val(self,x):return {'YES':1,'NO':0,'TRUE':1,'FALSE':0}.get(x,self.vars.get(x,int(x) if x.isdigit() else x))
 def run(self,label,answers=()):
  answers=list(answers);pc=labels[label];stack=[]
  for _ in range(500):
   line=commands[pc];pc+=1;op,_,rest=line.partition(' ');a=[x.strip() for x in rest.split(',')]
   if op=='end':return self
   if op=='return':
    if not stack:return self
    pc=stack.pop()
   elif op=='goto':pc=labels[a[0]]
   elif op in ['goto_if_set','goto_if_unset','call_if_set','call_if_unset']:
    if (a[0] in self.flags)==op.endswith('_set'):
     if op.startswith('call'):stack.append(pc)
     pc=labels[a[1]]
   elif op in ['goto_if_eq','goto_if_ne','goto_if_lt','call_if_eq','call_if_lt','call_if_ge']:
    x,y=self.val(a[0]),self.val(a[1]);take=(x==y if op.endswith('_eq') else x!=y if op.endswith('_ne') else x<y if op.endswith('_lt') else x>=y)
    if take:
     if a[2]=='Common_EventScript_NopReturn':
      if not stack:return self
      pc=stack.pop()
     else:
      if op.startswith('call'):stack.append(pc)
      pc=labels[a[2]]
   elif op=='call':stack.append(pc);pc=labels[a[0]]
   elif op=='setflag':self.flags.add(a[0])
   elif op=='clearflag':self.flags.discard(a[0])
   elif op=='setvar':self.vars[a[0]]=self.val(a[1])
   elif op=='addvar':self.vars[a[0]]=self.val(a[0])+self.val(a[1])
   elif op=='msgbox':
    self.messages.append(a[0])
    if a[1]=='MSGBOX_YESNO':self.vars['VAR_RESULT']=answers.pop(0)
   elif op=='setwildbattle':self.battles.append(tuple(a))
   elif op=='trainerbattle_single':
    self.battles.append(a[0])
    if self.lose:return self
   elif op=='specialvar':assert a[1]=='GetBattleOutcome';self.vars[a[0]]=self.outcome
   elif op=='special':
    if a[0] in ['StartRegiBattle','BattleSetup_StartLegendaryBattle'] and self.lose:return self
    assert a[0] in ['StartRegiBattle','BattleSetup_StartLegendaryBattle','ShakeScreen','DrawWholeMapView','ForcePlayerToStartSurfing','SeafoamIslandsB4F_CurrentDumpsPlayerOnLand'],a
   elif op=='warp':self.warps.append(a)
   elif op=='removeobject':self.removed.append(a[0])
   elif op not in ['lockall','releaseall','faceplayer','playmoncry','waitmoncry','closemessage','waitse','playse','delay','fadescreen','waitstate','setmetatile','playfanfare','waitfanfare','setrespawn','setmaplayoutindex','turnobject','applymovement','waitmovement']:
    raise AssertionError(op)
  raise AssertionError('Script did not terminate: '+label)
class Story(unittest.TestCase):
 def ready(self,*flags):e=Events();e.flags.update(F+f for f in flags);return e
 def test_capture_optional_bird_observations_and_single_reports(self):
  for bird,gates,report in [('Articuno',['FLAG_LEGENDS_KANTO_SURVEY_POWER_REPORT',F+'SEAFOAM_B3F_CURRENT',F+'SEAFOAM_B4F_CURRENT'],'SEAFOAM'),('Moltres',[F+'NORTH_REPORT','FLAG_LEGENDS_KANTO_BLAINE_WON'],'EMBER')]:
   for mask in range(1<<len(gates)):
    e=Events();e.flags={f for i,f in enumerate(gates) if mask&(1<<i)}
    if mask!=(1<<len(gates))-1:
     e.run('LegendsStory_'+bird);self.assertEqual(e.battles,[]);self.assertNotIn(F+bird.upper()+'_SEEN',e.flags)
    else:
     e.run('LegendsStory_'+bird,[0]);self.assertIn(F+bird.upper()+'_SEEN',e.flags);self.assertEqual(e.battles,[])
     chapter='4' if bird=='Articuno' else '6'
     e.run('LegendsStory_Chapter'+chapter+'_Journal');e.run('LegendsStory_Journal')
     self.assertIn(F+report+'_REPORT',e.flags)
     self.assertEqual(e.messages.count('LegendsStory_Text_'+('SeafoamReport' if bird=='Articuno' else 'EmberReport')),1)
 def test_bird_capture_faint_flee_loss_and_native_resume(self):
  for bird,gates in [('Articuno',['FLAG_LEGENDS_KANTO_SURVEY_POWER_REPORT',F+'SEAFOAM_B3F_CURRENT',F+'SEAFOAM_B4F_CURRENT']),('Moltres',[F+'NORTH_REPORT','FLAG_LEGENDS_KANTO_BLAINE_WON'])]:
   for outcome in ['B_OUTCOME_CAUGHT','B_OUTCOME_WON','B_OUTCOME_RAN','B_OUTCOME_LOST']:
    e=Events();e.flags.update(gates);e.outcome=outcome;e.lose=outcome=='B_OUTCOME_LOST';e.run('LegendsStory_'+bird,[1])
    self.assertEqual(F+bird.upper()+'_CAUGHT' in e.flags,outcome=='B_OUTCOME_CAUGHT')
    self.assertEqual(e.battles,[('SPECIES_'+bird.upper(),'50')])
    e.flags.add('FLAG_SYS_CTRL_OBJ_DELETE');e.run('LegendsStory_'+bird+'_OnResume')
    self.assertEqual(F+bird.upper()+'_CAUGHT' in e.flags,outcome=='B_OUTCOME_CAUGHT')
 def test_hoenn_readings_and_regulators_either_order(self):
  for order in itertools.permutations(['Rain','Heat']):
   e=self.ready('WEATHER_SUMMONED');e.run('LegendsHoenn_Scientist')
   for side in order:
    e.run('LegendsHoenn_'+side+'Reading',[0]);self.assertNotIn(F+'WEATHER_'+side.upper()+'_READING',e.flags)
    e.run('LegendsHoenn_'+side+'Reading',[1])
   e.run('LegendsHoenn_FaultEntrance',[0]);self.assertEqual(e.warps,[])
   e.run('LegendsHoenn_FaultEntrance',[1]);self.assertEqual(e.warps[-1],['MAP_LEGENDS_HOENN_CONTINENTAL_VAULT','8','27'])
   for anchors in itertools.permutations(['Rock','Ice','Steel']):
    a=Events();a.flags=e.flags.copy()
    for element in anchors:a.run('LegendsHoenn_Anchor'+element,[1])
    self.assertEqual(a.messages.count('LegendsHoenn_Text_Door'),1)
    before=a.flags.copy();a.run('LegendsHoenn_Anchor'+anchors[-1]);self.assertEqual(a.flags,before)
 def test_intermission_gates_and_regigigas_outcomes(self):
  for label in ['RainReading','HeatReading','FaultEntrance','Regigigas']:
   e=Events().run('LegendsHoenn_'+label);self.assertFalse(e.battles or e.warps or e.flags)
  for outcome in ['B_OUTCOME_CAUGHT','B_OUTCOME_WON','B_OUTCOME_RAN','B_OUTCOME_LOST']:
   e=self.ready('VAULT_ROCK','VAULT_ICE','VAULT_STEEL');e.outcome=outcome;e.lose=outcome=='B_OUTCOME_LOST'
   before=e.flags.copy();e.run('LegendsHoenn_Regigigas',[0]);self.assertEqual(e.flags,before);self.assertEqual(e.battles,[])
   e.run('LegendsHoenn_Regigigas',[1]);self.assertEqual(e.battles,[('SPECIES_REGIGIGAS','70')])
   self.assertEqual(F+'REGIGIGAS_CALMED' in e.flags,outcome in ['B_OUTCOME_CAUGHT','B_OUTCOME_WON'])
   self.assertEqual(F+'REGIGIGAS_CAUGHT' in e.flags,outcome=='B_OUTCOME_CAUGHT')
   callback=self.ready();callback.outcome=outcome;callback.flags.add('FLAG_SYS_CTRL_OBJ_DELETE');callback.run('LegendsHoenn_Vault_OnResume')
   self.assertEqual(F+'REGIGIGAS_CAUGHT' in callback.flags,outcome=='B_OUTCOME_CAUGHT')
   self.assertEqual(F+'REGIGIGAS_CALMED' in callback.flags,outcome=='B_OUTCOME_CAUGHT')
 def test_report_and_northern_sites_do_not_skip_intermission(self):
  e=self.ready('WEATHER_SUMMONED');e.run('LegendsHoenn_Scientist');self.assertNotIn(F+'WEATHER_REPORT',e.flags)
  e.flags.add(F+'REGIGIGAS_CALMED');e.run('LegendsHoenn_Scientist');e.run('LegendsHoenn_Scientist');self.assertEqual(e.messages.count('LegendsHoenn_Text_Report'),1)
  for leader,site in [('MISTY','NorthWater'),('BROCK','NorthStone')]:
   a=self.ready('WEATHER_REPORT');a.run('LegendsStory_'+site);self.assertNotIn(F+'NORTH_'+('WATER' if leader=='MISTY' else 'STONE'),a.flags)
   a.flags.add('FLAG_LEGENDS_KANTO_'+leader+'_WON');a.run('LegendsStory_'+site,[1]);a.run('LegendsStory_'+site)
   self.assertIn(F+'NORTH_'+('WATER' if leader=='MISTY' else 'STONE'),a.flags)
  for water,stone in itertools.product([False,True],repeat=2):
   a=self.ready('SEAFOAM_REPORT','WEATHER_REPORT')
   for yes,f in [(water,'NORTH_WATER'),(stone,'NORTH_STONE')]:
    if yes:a.flags.add(F+f)
   a.run('LegendsStory_Journal');self.assertEqual(F+'NORTH_REPORT' in a.flags,water and stone)
 def test_new_gyms_modes_decline_loss_and_one_victory(self):
  for gym in ['Brock','Misty','Blaine']:
   for mode in [0,1]:
    e=Events();e.run('LegendsKanto_'+gym+'_Entry',[mode]);e.run('LegendsKanto_'+gym+'_Leader',[0]);self.assertEqual(e.battles,[])
    e.lose=True;e.run('LegendsKanto_'+gym+'_Leader',[1]);self.assertNotIn('FLAG_LEGENDS_KANTO_'+gym.upper()+'_WON',e.flags)
    e.lose=False;e.run('LegendsKanto_'+gym+'_Entry',[mode]);e.run('LegendsKanto_'+gym+'_Leader',[1]);before=len(e.battles)
    self.assertTrue(e.battles[-1].endswith('CHAMPION' if mode else 'STANDARD'))
    e.run('LegendsKanto_'+gym+'_Entry',[1-mode]);e.run('LegendsKanto_'+gym+'_Leader');self.assertEqual(len(e.battles),before)
 def test_seafoam_initialization_is_once_only_and_currents_require_two(self):
  e=Events().run('LegendsSeafoam_Init');self.assertIn(F+'SEAFOAM_INITIALIZED',e.flags)
  for floor in ['B3F','B4F']:
   for first,second in itertools.product([0,1],repeat=2):
    a=Events();a.flags=e.flags.copy()
    for present,num in [(first,1),(second,2)]:
     if present:a.flags.discard(F+f'SEAFOAM_{floor}_BOULDER_{num}')
    a.run('LegendsSeafoam_'+floor+'_OnTransition');self.assertEqual(F+'SEAFOAM_'+floor+'_CURRENT' in a.flags,bool(first and second))
    before=a.flags.copy();a.run('LegendsSeafoam_Init');self.assertEqual(a.flags,before)
 def test_travel_decline_and_return_are_safe(self):
  for flags in [[],['NORTH_REPORT']]:
   e=self.ready(*flags);e.run('LegendsStory_EmberFerry');self.assertEqual(e.warps,[])
  e=self.ready('NORTH_REPORT');e.flags.add('FLAG_LEGENDS_KANTO_BLAINE_WON');e.run('LegendsStory_EmberFerry',[0]);self.assertEqual(e.warps,[])
  e.run('LegendsStory_EmberFerry',[1]);self.assertEqual(e.warps[-1],['MAP_LEGENDS_KANTO_MT_EMBER_EXTERIOR','28','47'])
  e.run('LegendsStory_EmberReturn',[1]);self.assertEqual(e.warps[-1],['MAP_LEGENDS_KANTO_CINNABAR_ISLAND','20','9'])
 def test_maps_native_art_warp_indices_and_npc_floors(self):
  maps={d['id']:d for p in (R/'data/maps').glob('*/map.json') if (d:=json.loads(p.read_text()))}
  layouts={l['id']:l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts']}
  for m in json.loads((R/'data/legends_kanto_chapters4-6.json').read_text())['maps']:
   d=maps[m['id']];native=maps[json.loads((R/'data/maps'/m['source']/'map.json').read_text())['id']];l=layouts[d['layout']];b=(R/l['blockdata_filepath']).read_bytes()
   self.assertEqual(len(b),2*l['width']*l['height'])
   for w in d['warp_events']:self.assertLess(int(w['dest_warp_id']),len(maps[w['dest_map']]['warp_events']))
   for o in d['object_events']:
    self.assertTrue(0<=o['x']<l['width'] and 0<=o['y']<l['height'])
    if o['graphics_id']!='OBJ_EVENT_GFX_NURSE':self.assertFalse(struct.unpack_from('<H',b,2*(o['y']*l['width']+o['x']))[0]&0xC00,(m['name'],o))
   self.assertEqual(len({o.get('local_id',str(i+1)) for i,o in enumerate(d['object_events'])}),len(d['object_events']))
  vault=maps['MAP_LEGENDS_HOENN_CONTINENTAL_VAULT'];self.assertEqual(vault['region_map_section'],'MAPSEC_FIERY_PATH')
  group=json.loads((R/'data/maps/map_groups.json').read_text());self.assertNotIn(vault['name'],group['gMapGroup_LegendsKanto'])
 def test_dialogue_native_font_width(self):
  chars={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)};chars["'"]=0xb4
  widths=list(map(int,re.findall(r'\d+',(R/'src/fonts.c').read_text().split('gFontNormalLatinGlyphWidths[] = {')[1].split('};')[0])))
  for line in re.findall(r'\.string "(.*?)"',source):
   text=re.sub(r'\\[npl]|\$','',line);self.assertLessEqual(sum(widths[chars[c]] for c in text),208,text)
 def test_unused_saved_bits_and_unchanged_native_flag_capacity(self):
  flags=(R/'include/constants/flags.h').read_text();pairs=re.findall(r'#define (FLAG_LEGENDS_STORY_\w+) (0x[0-9A-F]+)',flags)
  self.assertEqual(len(pairs),len({v for _,v in pairs}));self.assertTrue(all(0x284<=int(v,16)<0x2C0 for _,v in pairs))
  for _,v in pairs:self.assertNotRegex(flags,r'#define FLAG_(?!LEGENDS_STORY_|UNUSED_)\w+\s+'+v+r'\b')
  self.assertIn('#define MAX_TRAINERS_COUNT_EMERALD 864',(R/'include/constants/opponents.h').read_text())
  variables=(R/'include/constants/vars.h').read_text()
  self.assertIn('#define VAR_LEGENDS_SEAFOAM_ENTRY VAR_ROUTE124_STATE',variables)
  self.assertEqual(len(re.findall(r'^#define VAR_\w+\s+0x4077\b',variables,re.M)),1)
  self.assertIn('data/tilesets/legends_story.h',(R/'src/tilesets.c').read_text())
 def test_actual_c_story_weather_and_habitat_boundaries(self):
  body='\n'.join(l for l in (R/'src/legends_story.c').read_text().splitlines() if not l.startswith('#include'))
  program='''#include <stdint.h>
#include <assert.h>
typedef uint8_t u8; typedef int bool32;
#define IS_FRLG 0
#define FALSE 0
#define MAP_GROUP(m) ((m)>>8)
#define MAP_NUM(m) ((m)&255)
#define MAP_LEGENDS_KANTO_SEAFOAM_ISLANDS_1F 0x4101
#define MAP_LEGENDS_KANTO_SEAFOAM_ISLANDS_B4F 0x4105
#define MAP_ROUTE119 0x0010
#define MAP_ROUTE120 0x0011
#define FLAG_LEGENDS_STORY_WEATHER_STARTED 1
#define FLAG_LEGENDS_STORY_REGIGIGAS_CALMED 2
#define FLAG_SYS_GAME_CLEAR 3
struct WarpData { u8 mapGroup,mapNum; };
struct {struct WarpData location;} save,*gSaveBlock1Ptr=&save;
static int flags[4]; int FlagGet(int f){return flags[f];}
'''+(R/'include/constants/weather.h').read_text()+body+'''
int main(void) {
 for(int group=0;group<80;group++)for(int map=0;map<150;map++) {
  save.location.mapGroup=group;save.location.mapNum=map;
  assert(LegendsIsSeafoamMap()==(group==0x41&&map>=1&&map<=5));
 }
 for(int started=0;started<2;started++)for(int calm=0;calm<2;calm++)for(int champion=0;champion<2;champion++) {
  flags[1]=started;flags[2]=calm;flags[3]=champion;
  for(int map=0;map<25;map++)for(int w=0;w<WEATHER_COUNT;w++) {
   save.location.mapGroup=0;save.location.mapNum=map;
   int eligible=started&&!calm&&champion&&(w==WEATHER_SUNNY||w==WEATHER_SUNNY_CLOUDS||w==WEATHER_RAIN||w==WEATHER_RAIN_THUNDERSTORM);
   int wanted=eligible&&map==16?WEATHER_RAIN_THUNDERSTORM:eligible&&map==17?WEATHER_FOG_HORIZONTAL:WEATHER_COUNT;
   assert(LegendsStoryWeather(w)==wanted);
  }
 }
}'''
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'story.c').write_text(program)
   subprocess.run(['gcc','-Wall','-Werror',str(p/'story.c'),'-o',str(p/'story')],check=True)
   subprocess.run([str(p/'story')],check=True)
if __name__=='__main__':unittest.main()
