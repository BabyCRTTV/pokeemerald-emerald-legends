"""Author append-only Wyrmtide maps from unchanged native Hoenn metatiles.

Only new layouts are regenerated. Existing owner-authored layouts/tilesets are
never rewritten. Native stair warp pairs and collision words are explicit.
"""
import json,struct
from pathlib import Path
R=Path(__file__).resolve().parents[2]
def write(p,data):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True)
 if not isinstance(data,(str,bytes)):data=json.dumps(data,indent=2)+'\n'
 raw=data.encode() if isinstance(data,str) else data
 if not p.exists() or p.read_bytes()!=raw:p.write_bytes(raw)
def obj(gfx,x,y,script='0x0',flag='0',elevation=3):
 return dict(graphics_id=gfx,x=x,y=y,elevation=elevation,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=script,flag=flag)
def sign(x,y,script):return dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=script)
def warp(x,y,dest,index):return dict(x=x,y=y,elevation=3,dest_map='MAP_LEGENDS_WYRMTIDE_'+dest.upper(),dest_warp_id=str(index))
def main(refresh_review=False):
 if any((R/f"data/layouts/LegendsWyrmtide_{k}/map.bin").exists() for k in ["Isle","Descent1","Descent2","Descent3","Descent4","Heart"]) and not refresh_review:
  raise SystemExit("Existing Wyrmtide maps preserved. Use --refresh-review only for explicit review-layout edits.")
 # Append one stair behavior; native art and all prior definitions stay exact.
 base=R/"data/tilesets/secondary/cave";native=(base/"metatiles.bin").read_bytes();attrs=(base/"metatile_attributes.bin").read_bytes()
 assert len(native)//16==414, "Native Cave allocation changed; review without overwriting owner art"
 write("data/tilesets/legends_wyrmtide/metatiles.bin",native+native[64:80])
 write("data/tilesets/legends_wyrmtide/metatile_attributes.bin",attrs+struct.pack("<H",0x61))
 groups=json.loads((R/'data/maps/map_groups.json').read_text());layouts=json.loads((R/'data/layouts/layouts.json').read_text())
 for level,key in enumerate(['Isle','Descent1','Descent2','Descent3','Descent4','Heart']):
  name='LegendsWyrmtide_'+key;W,H=(34,29) if level==0 else ((19,24) if level<5 else (23,21))
  a=[0x1170]*(W*H) if level==0 else [0x0423]*(W*H)
  def put(x,y,t,solid=False,elev=3):a[y*W+x]=t|(0x400 if solid else 0)|(elev<<12)
  def fill(x1,y1,x2,y2,t,solid=False):
   for y in range(y1,y2+1):
    for x in range(x1,x2+1):put(x,y,t,solid)
  def room(x1,y1,x2,y2):
   fill(x1,y1,x2,y2,0x201)
   for x in range(x1,x2+1):put(x,y1,0x219,True);put(x,y2,0x209,True)
   for y in range(y1+1,y2):put(x1,y,0x212,True);put(x2,y,0x210,True)
   put(x1,y1,0x21B,True);put(x2,y1,0x21C,True)
   put(x1,y2,0x247,True);put(x2,y2,0x247,True)
  objects=[];warps=[];signs=[]
  if level==0:
   # Native Route 106 sand and complete 3x3 shoreline assemblies.
   shore={3:(13,19),4:(10,22),5:(8,24),6:(8,24),7:(8,25),8:(6,27),9:(6,27),10:(6,27),11:(6,27),12:(6,27),13:(6,27),14:(7,27),15:(7,27),16:(7,27),17:(7,27),18:(7,27),19:(7,27),20:(7,27),21:(9,25),22:(9,25),23:(11,23),24:(13,21)}
   land={(x,y) for y,(left,right) in shore.items() for x in range(left,right+1)}
   for x,y in land:
    n,e,so,w=[(x+dx,y+dy) in land for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]]
    if not n:t=0x11B if not w else 0x11D if not e else 0x11C
    elif not so:t=0x12B if not w else 0x12D if not e else 0x12C
    elif not w:t=0x123
    elif not e:t=0x125
    elif (x-1,y-1) not in land:t=0x13D
    elif (x+1,y-1) not in land:t=0x13E
    elif (x-1,y+1) not in land:t=0x145
    elif (x+1,y+1) not in land:t=0x146
    else:t=0x124
    put(x,y,t)
   # Native bare-rock cliff, rather than floor art used as an outdoor wall.
   fill(11,6,22,10,0x071,True)
   for x in range(11,23):put(x,6,0x06C,True);put(x,10,0x07C,True)
   for y in range(7,10):put(11,y,0x073,True);put(22,y,0x075,True)
   for x,y,t in [(11,6,0x06B),(22,6,0x06D),(11,10,0x07B),(22,10,0x07D)]:put(x,y,t,True)
   for dx,t in enumerate([0x22A,0x22B,0x22C]):put(15+dx,9,t,True)
   for dx in range(3):put(15+dx,10,0x235,True)
   # Weathered stone tablets, readable from the sand directly below.
   for x,y,script in [(10,17,'Wyrmtide_ShoreTablet'),(23,14,'Wyrmtide_MakerTablet'),(19,20,'Wyrmtide_SeaTablet')]:
    put(x,y,0x235,True);signs.append(sign(x,y,script))
   for x,y in [(8,8),(25,7),(9,12),(24,19),(8,21)]:put(x,y,0x202,True)
   for x,y in [(3,8),(29,17),(27,5)]:
    for dx,dy,t in [(0,0,0x150),(1,0,0x151),(0,1,0x158),(1,1,0x159)]:put(x+dx,y+dy,t,True,1)
   # A palm grove uses complete native General crowns and trunks.
   for x,y in [(23,8),(25,10),(8,14)]:
    for dx,dy,t in [(0,0,0x1D4),(1,0,0x1D5),(0,1,0x1E4),(1,1,0x1E5)]:put(x+dx,y+dy,t,True)
   warps=[warp(16,10,'Descent1',0)]
   objects=[obj('OBJ_EVENT_GFX_EXPERT_M',13,21,'Wyrmtide_ShoreBriney'),obj('OBJ_EVENT_GFX_MR_BRINEYS_BOAT',12,25,elevation=1),obj('OBJ_EVENT_GFX_WINGULL',11,22,'Wyrmtide_Peeko')]
   signs.extend(sign(x,10,'Wyrmtide_Seal') for x in [15,16,17])
   scripts=f'''{name}_MapScripts::
\tmap_script MAP_SCRIPT_ON_TRANSITION, Wyrmtide_Landing
\tmap_script MAP_SCRIPT_ON_LOAD, {name}_OnLoad
\t.byte 0
{name}_OnLoad:
\tcall Wyrmtide_SealOnLoad
\tend
'''
  elif level<5:
   # Four successive landings. Side galleries alternate around a central stair
   # shaft; paths use ordinary floor, while the paired ladders actually warp.
   room(3,2,15,21)
   # Switchback stair flights between visible rock banks. Every tread reuses
   # native Cave art; only the end tread gains a native ladder warp behavior.
   for y,side in [(7,0),(13,1)]:
    left=(level+side)%2
    if left:fill(4,y,11,y+1,0x228,True)
    else:fill(7,y,14,y+1,0x228,True)
    for sy in range(y-1,y+3):
     for sx in (range(12,15) if left else range(4,7)):put(sx,sy,0x204)
   for sy in [18,19]:
    for sx in [10,11,12]:put(sx,sy,0x204)
   put(8,3,0x39E);put(11,20,0x39E)
   for x,y in [(13,4),(5,18)]:put(x,y,0x202,True)
   if level in [1,3]:put(13,18,0x235,True);signs.append(sign(13,18,'Wyrmtide_DepthTablet'))
   warps=[warp(8,3,'Isle' if level==1 else 'Descent'+str(level-1),0 if level==1 else 1),warp(11,20,'Heart' if level==4 else 'Descent'+str(level+1),0)]
   scripts=f'{name}_MapScripts::\n\t.byte 0\n'
  else:
   room(3,2,19,18)
   # Dais, flanking pillars and a quiet, straight final approach.
   for x,y in [(5,5),(17,5),(5,11),(17,11)]:put(x,y,0x202,True)
   for x in [10,11,12]:put(x,4,0x235,True);signs.append(sign(x,4,'Wyrmtide_FinalTablet'))
   put(11,17,0x39E)
   objects=[obj('OBJ_EVENT_GFX_VAR_F',11,7,'Wyrmtide_Regidrago','FLAG_LEGENDS_WYRMTIDE_CAUGHT')]
   warps=[warp(11,17,'Descent4',1)]
   scripts=f'''{name}_MapScripts::
\tmap_script MAP_SCRIPT_ON_TRANSITION, Wyrmtide_ChamberOnTransition
\tmap_script MAP_SCRIPT_ON_RESUME, Wyrmtide_ChamberOnResume
\t.byte 0
'''
  lid='LAYOUT_LEGENDS_WYRMTIDE_'+key.upper();mid='MAP_LEGENDS_WYRMTIDE_'+key.upper()
  write(f'data/layouts/{name}/map.bin',struct.pack('<%dH'%len(a),*a));write(f'data/layouts/{name}/border.bin',struct.pack('<4H',*([0x1170]*4 if level==0 else [0x0023]*4)))
  l=dict(id=lid,name=name+'_Layout',width=W,height=H,primary_tileset='gTileset_General',secondary_tileset='gTileset_Cave' if level==0 else 'gTileset_LegendsWyrmtideCave',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin',layout_version='emerald')
  existing=next((x for x in layouts['layouts'] if x['id']==lid),None)
  if existing:assert existing==l,'Never renumber or resize an existing published layout'
  else:layouts['layouts'].append(l)
  m=dict(id=mid,name=name,layout=lid,music='MUS_DEWFORD' if level==0 else 'MUS_SEALED_CHAMBER',region='REGION_HOENN',region_map_section='MAPSEC_LEGENDS_WYRMTIDE_ISLE',requires_flash=False,weather='WEATHER_SUNNY' if level==0 else 'WEATHER_NONE',map_type='MAP_TYPE_ROUTE' if level==0 else 'MAP_TYPE_UNDERGROUND',allow_cycling=False,allow_escaping=False,allow_running=True,show_map_name=level==0,battle_scene='MAP_BATTLE_SCENE_NORMAL',connections=None,object_events=objects,warp_events=warps,coord_events=[],bg_events=signs)
  write(f'data/maps/{name}/map.json',m);write(f'data/maps/{name}/scripts.inc',scripts)
  if name not in groups['gMapGroup_LegendsHoenn']:groups['gMapGroup_LegendsHoenn'].append(name)
 write('data/maps/map_groups.json',groups);write('data/layouts/layouts.json',layouts)
 # Add local expedition stand-ins only when the native Briney/boat are absent.
 p=R/'data/maps/DewfordTown/map.json';m=json.loads(p.read_text())
 if not any(o.get('script')=='Wyrmtide_ExpeditionBriney' for o in m['object_events']):
  briney=obj('OBJ_EVENT_GFX_EXPERT_M',12,9,'Wyrmtide_ExpeditionBriney','FLAG_TEMP_6');briney['local_id']='LOCALID_WYRMTIDE_BRINEY'
  boat=obj('OBJ_EVENT_GFX_MR_BRINEYS_BOAT',12,8,flag='FLAG_TEMP_7',elevation=1);boat['local_id']='LOCALID_WYRMTIDE_BOAT'
  m['object_events'] += [briney,boat]
  write('data/maps/DewfordTown/map.json',m)
 p=R/'data/event_scripts.s';s=p.read_text();anchor='\t.include "data/scripts/legends_story_common.inc"';extra='\t.include "data/scripts/legends_wyrmtide.inc"\n'+ '\n'.join(f'\t.include "data/maps/LegendsWyrmtide_{key}/scripts.inc"' for key in ['Isle','Descent1','Descent2','Descent3','Descent4','Heart'])
 if 'data/scripts/legends_wyrmtide.inc' not in s:p.write_text(s.replace(anchor,anchor+'\n'+extra,1))
 print('Authored island, four descent landings and the dragon chamber; old layouts untouched.')
if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('--refresh-review',action='store_true');a=p.parse_args();main(a.refresh_review)
