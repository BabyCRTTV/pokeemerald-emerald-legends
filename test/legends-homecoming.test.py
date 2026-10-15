"""Actual homecoming C plus native script routing, save-memory and text-width regressions."""
from pathlib import Path
import ctypes, re, subprocess, tempfile, unittest, json
R=Path(__file__).resolve().parents[1]
M='VAR_LEGENDS_HOMECOMING_MEMORY'

def api_build(out):
 source='\n'.join(l for l in (R/'src/legends_homecoming.c').read_text().splitlines() if not l.startswith('#include')).replace(r'\p',r'\n\n')
 pre=r'''
#include <stdint.h>
#include <string.h>
#include <stddef.h>
typedef uint8_t u8; typedef uint16_t u16; typedef int bool32;
#define MALE 0
#define OBJECT_EVENTS_COUNT 16
#define COMPOUND_STRING(s) ((const u8 *)(s))
#define MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_1F 0x0100
#define MAP_LITTLEROOT_TOWN_MAYS_HOUSE_1F 0x0101
#define MAP_PETALBURG_CITY_GYM 0x0801
#define MAP_GROUP(n) ((n)>>8)
#define MAP_NUM(n) ((n)&255)
#include "constants/flags.h"
#include "constants/vars.h"
struct {struct {u8 mapGroup,mapNum;} location;} save1,*gSaveBlock1Ptr=&save1;
struct {u8 playerGender;} save2,*gSaveBlock2Ptr=&save2;
static u16 variables[65536],gSpecialVar_Result,gSpecialVar_0x8004;
static u8 flags[65536],gStringVar4[1024],spawnFail;
static unsigned writes,spawns;
static u16 VarGet(u16 v){return variables[v];}
static void VarSet(u16 v,u16 n){variables[v]=n;writes++;}
static int FlagGet(u16 f){return flags[f];}
static void StringCopy(u8 *a,const u8 *b){strcpy((char*)a,(const char*)b);}
static u8 TrySpawnObjectEvent(u8 id,u8 n,u8 g){spawns++;return spawnFail?16:5;}
'''
 helpers=r'''
void Reset(int gender){memset(variables,0,sizeof(variables));memset(flags,0,sizeof(flags));writes=spawns=spawnFail=0;save2.playerGender=gender;save1.location.mapGroup=1;save1.location.mapNum=gender;gSpecialVar_0x8004=5;}
void Map(int g,int n){save1.location.mapGroup=g;save1.location.mapNum=n;}
void Flag(int f,int on){flags[f]=on;}
int GetFlag(int f){return flags[f];}
void Var(int v,int n){variables[v]=n;}
int GetVar(int v){return variables[v];}
unsigned Writes(void){return writes;}
unsigned Spawns(void){return spawns;}
int Result(void){return gSpecialVar_Result;}
const char *Text(void){return (const char*)gStringVar4;}
void FailSpawn(int n){spawnFail=n;}
'''
 p=Path(out);(p/'home.c').write_text(pre+source+helpers)
 subprocess.run(['cc','-shared','-fPIC','-std=c11','-Wall','-Werror=implicit-function-declaration','-I'+str(R/'include'),str(p/'home.c'),'-o',str(p/'home.so')],check=True)
 api=ctypes.CDLL(str(p/'home.so'));api.Text.restype=ctypes.c_char_p
 return api

# Resolve numeric native flag/var names using the compiler's actual headers.
def constants():
 text=subprocess.check_output(['cpp','-dM','-I'+str(R/'include'),'-include','constants/vars.h','-include','constants/flags.h','-'],input='',text=True)
 values={k:v for k,v in re.findall(r'^#define (\w+) (.+)$',text,re.M)}
 def number(k):
  v=values.get(k,k)
  if re.fullmatch(r'0x[0-9A-Fa-f]+|[0-9]+',v):return int(v,0)
  if v in values:return number(v)
  def replace(m):
   name=m[0]
   if name not in values:raise ValueError(name)
   n=number(name)
   if n is None:raise ValueError(name)
   return str(n)
  try:
   v=re.sub(r'\b[A-Za-z_]\w*\b',replace,v)
   if not re.fullmatch(r'[0-9a-fA-FxX ()+*/<>&|~^-]+',v):return None
   return int(eval(v,{'__builtins__':{}},{}))
  except (ValueError,NameError,SyntaxError,TypeError,RecursionError):return None
 return {k:n for k in values if (n:=number(k)) is not None}
C=constants()
FILES=['data/scripts/players_house.inc','data/maps/PetalburgCity_Gym/scripts.inc','data/scripts/legends_homecoming.inc']
labels={};commands=[]
for path in FILES:
 for line in (R/path).read_text().splitlines():
  line=line.strip()
  if re.fullmatch(r'\w+::?',line):labels[line.rstrip(':')]=len(commands)
  elif line and not line.startswith(('@','.','#')):commands.append(line)

class Scripts:
 def __init__(self,api):self.api=api;self.messages=[];self.items={};self.bag_full=False;self.calls=[];self.battles=0;self.removed=[];self.lose=False
 def var(self,k):return self.api.GetVar(C[k]) if k in C else self.vars.get(k,0)
 def setvar(self,k,v):
  if k in C:self.api.Var(C[k],v)
  else:self.vars[k]=v
 def val(self,k):return {'TRUE':1,'FALSE':0}.get(k,int(k) if k.isdigit() else self.var(k))
 def run(self,label):
  self.vars={};pc=labels[label];stack=[]
  for _ in range(600):
   op,_,rest=commands[pc].partition(' ');pc+=1;a=[x.strip() for x in rest.split(',')]
   if op=='end':return
   if op=='return':
    if not stack:return
    pc=stack.pop()
   elif op=='call':
    self.calls.append(a[0])
    if a[0]=='Common_EventScript_OutOfCenterPartyHeal':continue
    stack.append(pc);pc=labels[a[0]]
   elif op=='goto':
    if a[0]=='Common_EventScript_ShowBagIsFull':return
    pc=labels[a[0]]
   elif op in ('goto_if_set','goto_if_unset','call_if_set','call_if_unset'):
    if bool(self.api.GetFlag(C[a[0]]))==op.endswith('_set'):
     if op.startswith('call'):stack.append(pc)
     pc=labels[a[1]]
   elif op in ('goto_if_eq','call_if_eq'):
    if self.val(a[0])==self.val(a[1]):
     if a[2]=='Common_EventScript_ShowBagIsFull':return
     if op.startswith('call'):stack.append(pc)
     pc=labels[a[2]]
   elif op=='switch':switch=self.val(a[0])
   elif op=='case':
    if switch==self.val(a[0]):pc=labels[a[1]]
   elif op=='setvar':self.setvar(a[0],self.val(a[1]))
   elif op=='setflag':self.api.Flag(C[a[0]],1)
   elif op=='special':
    if a[0].startswith('LegendsHomecoming'):
     getattr(self.api,a[0])();self.setvar('VAR_RESULT',self.api.Result())
    elif a[0]=='LegendsBedroomMomMessage':self.setvar('VAR_RESULT',1)
    else:raise AssertionError(a)
   elif op=='specialvar':
    assert a[1]=='IsEnigmaBerryValid';self.setvar(a[0],0)
   elif op=='msgbox':self.messages.append(self.api.Text().decode() if a[0]=='gStringVar4' else a[0])
   elif op in ('checkitem','checkpcitem'):self.setvar('VAR_RESULT',int(a[0] in self.items))
   elif op=='giveitem':
    self.setvar('VAR_RESULT',not self.bag_full)
    if not self.bag_full:self.items[a[0]]=self.items.get(a[0],0)+1
   elif op=='removeobject':self.removed.append(a[0])
   elif op=='trainerbattle_rematch_double':
    self.battles+=1
    if self.lose:return
   elif op not in ('vsseeker_rematchid','lock','release','faceplayer','closemessage','delay','playfanfare','waitfanfare','incrementgamestat','fadescreen','applymovement','waitmovement'):raise AssertionError(op)
  raise AssertionError('script failed to terminate')

class Homecoming(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.tmp=tempfile.TemporaryDirectory();cls.api=api_build(cls.tmp.name)
 @classmethod
 def tearDownClass(cls):cls.tmp.cleanup()
 def setUp(self):self.api.Reset(0)
 def flag(self,name,on=1):self.api.Flag(C[name],on)
 def put(self,name,value):self.api.Var(C[name],value)
 def full(self,gender=0):
  self.api.Reset(gender)
  for f in ['FLAG_RESCUED_BIRCH','FLAG_BADGE01_GET','FLAG_BADGE05_GET','FLAG_SYS_GAME_CLEAR','FLAG_LEGENDS_KANTO_WELCOMED','FLAG_LEGENDS_FINAL_HOENN_EPILOGUE','FLAG_RECEIVED_SS_TICKET']:self.flag(f)
  for v in ['VAR_LITTLEROOT_HOUSES_STATE_MAY','VAR_LITTLEROOT_HOUSES_STATE_BRENDAN']:self.put(v,4)
 def test_all_legacy_words_are_read_without_mutation(self):
  for value in range(65536):
   self.put(M,value);self.api.LegendsHomecomingMomMessage();self.api.LegendsHomecomingReady()
   self.assertEqual(self.api.GetVar(C[M]),value)
  self.assertEqual(self.api.Writes(),0)
 def test_latest_stage_once_independent_parents_and_no_backward_backlog(self):
  stages=['FLAG_RESCUED_BIRCH','FLAG_BADGE01_GET','FLAG_BADGE05_GET','FLAG_SYS_GAME_CLEAR','FLAG_LEGENDS_KANTO_WELCOMED','FLAG_LEGENDS_FINAL_HOENN_EPILOGUE']
  for gender in [0,1]:
   self.api.Reset(gender)
   for stage,f in enumerate(stages,1):
    self.flag(f);self.api.LegendsHomecomingMomMessage();self.assertEqual(self.api.Result(),1)
    self.api.LegendsHomecomingRememberMom();self.api.LegendsHomecomingMomMessage();self.assertEqual(self.api.Result(),0)
    self.assertEqual(self.api.GetVar(C[M])&7,stage)
   mom=self.api.GetVar(C[M]);self.api.Map(8,1)
   self.api.LegendsHomecomingDadMessage();self.assertEqual(self.api.Result(),1)
   self.api.LegendsHomecomingRememberDad();self.assertEqual(self.api.GetVar(C[M])&7,mom&7)
   self.api.LegendsHomecomingDadMessage();self.assertEqual(self.api.Result(),0)
   self.flag(stages[-1],0);self.api.LegendsHomecomingDadMessage();self.assertEqual(self.api.Result(),0)
 def test_older_postgame_defaults_and_snapshot_reload(self):
  for legacy in [0,1,0xffff,0xd607,0xd638,0xd680,0xb423]:
   self.full();self.put(M,legacy);self.api.LegendsHomecomingMomMessage();self.assertEqual(self.api.Result(),1)
   self.api.LegendsHomecomingRememberMom();saved=self.api.GetVar(C[M]);self.assertEqual(saved,0xd606)
   self.put(M,0);self.put(M,saved);self.api.LegendsHomecomingMomMessage();self.assertEqual(self.api.Result(),0)
 def test_location_guards_both_houses_rival_and_gym(self):
  for gender in [0,1]:
   self.full(gender);self.api.Map(1,1-gender)
   self.api.LegendsHomecomingReady();self.assertEqual(self.api.Result(),0)
   self.api.LegendsHomecomingRememberMom();self.assertEqual(self.api.Writes(),0)
   self.api.Map(1,gender);self.api.LegendsHomecomingDadMessage();self.assertEqual(self.api.Result(),0)
   self.api.LegendsHomecomingRememberDad();self.assertEqual(self.api.Writes(),0)
 def test_family_gates_failure_retry_completion_once(self):
  for missing in ['FLAG_LEGENDS_FINAL_HOENN_EPILOGUE','FLAG_RECEIVED_SS_TICKET']:
   self.full();self.flag(missing,0);self.api.LegendsHomecomingReady();self.assertEqual(self.api.Result(),0)
  for v in ['VAR_LITTLEROOT_HOUSES_STATE_MAY','VAR_LITTLEROOT_HOUSES_STATE_BRENDAN']:
   for state in [0,1,2,3]:
    self.full();self.put(v,state);self.api.LegendsHomecomingReady();self.assertEqual(self.api.Result(),0)
  for gender in [0,1]:
   self.full(gender);self.api.FailSpawn(1);s=Scripts(self.api);s.run('LegendsHomecoming_Mom')
   self.assertNotIn('LegendsHomecoming_Text_MomWelcome',s.messages);self.assertFalse(self.api.GetVar(C[M])&64)
   self.api.FailSpawn(0);s=Scripts(self.api);s.run('LegendsHomecoming_Mom')
   self.assertEqual(s.messages.count('LegendsHomecoming_Text_MomWelcome'),1);self.assertEqual(len(s.messages),5)
   self.assertEqual(s.removed,['LOCALID_PLAYERS_HOUSE_1F_DAD']);self.assertEqual(self.api.GetVar(C[M]),0xd666)
   s.run('LegendsHomecoming_Mom');self.assertEqual(len(s.messages),5)
 def test_mom_native_registration_gift_full_bag_and_healing_priority(self):
  self.flag('FLAG_RESCUED_BIRCH');self.flag('FLAG_HAS_MATCH_CALL');self.flag('FLAG_BADGE05_GET')
  s=Scripts(self.api);s.run('PlayersHouse_1F_EventScript_Mom')
  self.assertIn('PlayersHouse_1F_Text_RegisteredMom',s.messages);self.assertEqual(self.api.Writes(),0)
  self.assertTrue(self.api.GetFlag(C['FLAG_ENABLE_MOM_MATCH_CALL']))
  s.bag_full=True;s.run('PlayersHouse_1F_EventScript_Mom');self.assertEqual(self.api.Writes(),0)
  self.assertFalse(self.api.GetFlag(C['FLAG_RECEIVED_AMULET_COIN']))
  s.bag_full=False;s.run('PlayersHouse_1F_EventScript_Mom');self.assertEqual(s.items.get('ITEM_AMULET_COIN'),1)
  self.assertEqual(self.api.Writes(),0)
  s.run('PlayersHouse_1F_EventScript_Mom');self.assertIn('Common_EventScript_OutOfCenterPartyHeal',s.calls)
  self.assertEqual(s.items.get('ITEM_AMULET_COIN'),1);self.assertEqual(self.api.GetVar(C[M]),0xd603)
 def test_postgame_mom_retains_native_branch_and_gym_retains_rematches(self):
  self.full();s=Scripts(self.api);s.run('PlayersHouse_1F_EventScript_Mom')
  self.assertEqual(s.messages[-1],'PlayersHouse_1F_Text_DontPushYourselfTooHard')
  self.assertNotIn('Common_EventScript_OutOfCenterPartyHeal',s.calls)
  self.api.Map(8,1);self.put('VAR_PETALBURG_GYM_STATE',7)
  s=Scripts(self.api);s.run('PetalburgCity_Gym_EventScript_Norman');self.assertEqual(s.items.get('ITEM_TM_FACADE'),1)
  self.flag('FLAG_RECEIVED_TM_FACADE');self.put(M,0);s.run('PetalburgCity_Gym_EventScript_Norman')
  self.assertIn('PetalburgCity_Gym_Text_DadNoAmountOfTrainingIsEnough',s.messages)
  self.put('VAR_PETALBURG_GYM_STATE',8);s.run('PetalburgCity_Gym_EventScript_Norman');self.assertEqual(s.battles,1)
 def test_norman_milestones_and_lost_rematch_do_not_consume_words(self):
  self.api.Map(8,1)
  for stage,f in enumerate(['FLAG_BADGE05_GET','FLAG_SYS_GAME_CLEAR','FLAG_LEGENDS_KANTO_WELCOMED','FLAG_LEGENDS_FINAL_HOENN_EPILOGUE'],1):
   self.flag(f);self.api.LegendsHomecomingDadMessage();self.assertEqual(self.api.Result(),1)
   self.api.LegendsHomecomingRememberDad();self.assertEqual((self.api.GetVar(C[M])>>3)&7,stage)
   self.api.LegendsHomecomingDadMessage();self.assertEqual(self.api.Result(),0)
  self.put(M,0);self.put('VAR_PETALBURG_GYM_STATE',8)
  s=Scripts(self.api);s.lose=True;s.run('PetalburgCity_Gym_EventScript_Norman')
  self.assertEqual(self.api.GetVar(C[M]),0);self.assertFalse(s.messages)
  s.lose=False;s.run('PetalburgCity_Gym_EventScript_Norman');self.assertEqual(self.api.GetVar(C[M]),0xd620)
 def test_native_font_width_ids_and_assets(self):
  chars={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)};chars["'"]=0xb4
  widths=list(map(int,re.findall(r'\d+',(R/'src/fonts.c').read_text().split('gFontNormalLatinGlyphWidths[] = {')[1].split('};')[0])))
  for path in ['src/legends_homecoming.c','data/scripts/legends_homecoming.inc']:
   s=(R/path).read_text();strings=re.findall(r'COMPOUND_STRING\("(.*?)"\)',s) if path.endswith('.c') else re.findall(r'\.string "(.*?)"',s)
   for text in strings:
    for line in re.split(r'\\[npl]',text.replace('$','')):self.assertLessEqual(sum(widths[chars[c]] for c in line),208,line)
  self.assertEqual(C[M],0x406a)
  # Native aliases are never referenced by active code/scripts; the FRLG var table is separate.
  for base in ['src','data']:
   for p in (R/base).rglob('*'):
    if p.suffix in ['.c','.inc','.s','.json']:self.assertNotIn('VAR_ROUTE111_STATE',p.read_text(errors='ignore'),str(p))
  for house in ['Brendans','Mays']:
   objects=json.loads((R/f'data/maps/LittlerootTown_{house}House_1F/map.json').read_text())['object_events']
   dad=next(o for o in objects if o.get('local_id')=='LOCALID_PLAYERS_HOUSE_1F_DAD')
   self.assertEqual((dad['graphics_id'],dad['x'],dad['y']),('OBJ_EVENT_GFX_NORMAN',5,6))
  self.assertTrue((R/'data/specials.inc').read_text().index('def_special LegendsHomecomingMomMessage')>(R/'data/specials.inc').read_text().index('def_special LegendsBedroomMomMessage'))

if __name__=='__main__':unittest.main()
