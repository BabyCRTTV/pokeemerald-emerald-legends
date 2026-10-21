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
 # Reuse General's stone-step geometry with Cave's existing sandstone palette.
 # Original tiles, palettes and every native Cave metatile remain untouched.
 base=R/"data/tilesets/secondary/cave";native=(base/"metatiles.bin").read_bytes();attrs=(base/"metatile_attributes.bin").read_bytes()
 assert len(native)//16==414, "Native Cave allocation changed; review without overwriting owner art"
 general=(R/'data/tilesets/primary/general/metatiles.bin').read_bytes()
 words=struct.unpack_from('<8H',general,0xAF*16)
 tread=struct.pack('<8H',*[(w&0xFFF)|0x6000 if w else 0 for w in words])
 write("data/tilesets/legends_wyrmtide/metatiles.bin",native+tread+tread)
 write("data/tilesets/legends_wyrmtide/metatile_attributes.bin",attrs+struct.pack("<HH",0x61,0))
 groups=json.loads((R/'data/maps/map_groups.json').read_text());layouts=json.loads((R/'data/layouts/layouts.json').read_text())
 for level,key in enumerate(['Isle','Descent1','Descent2','Descent3','Descent4','Heart']):
  name='LegendsWyrmtide_'+key;W,H=(34,29) if level==0 else ((19,24) if level<5 else (23,21))
  a=[0x1170]*(W*H) if level==0 else [0x0423]*(W*H)
  def put(x,y,t,solid=False,elev=3):a[y*W+x]=t|(0x400 if solid else 0)|(elev<<12)
  def fill(x1,y1,x2,y2,t,solid=False):
   for y in range(y1,y2+1):
    for x in range(x1,x2+1):put(x,y,t,solid)
  def stone(x1,y1,x2,y2,inscribed=False):
   # Complete native Sealed Chamber monument, including its shaded foot.
   fill(x1,y1,x2,y2,0x2F1,True)
   for x in range(x1+1,x2):put(x,y1,0x2E9,True);put(x,y2,0x237 if inscribed else 0x2F9,True)
   for y in range(y1+1,y2):put(x1,y,0x2F0,True);put(x2,y,0x2F2,True)
   for x,y,t in [(x1,y1,0x2E8),(x2,y1,0x2EA),(x1,y2,0x2F8),(x2,y2,0x2FA)]:put(x,y,t,True)
  def pillar(x,y):
   for dx,dy,t in [(0,0,0x2E8),(1,0,0x2EA),(0,1,0x2F0),(1,1,0x2F2),(0,2,0x2F8),(1,2,0x2FA)]:put(x+dx,y+dy,t,True)
  def stairs(x1,y1,x2,y2):fill(x1,y1,x2,y2,0x39F)
  def dais(x1,y1,x2,y2,stepx):
   stone(x1,y1,x2,y2)
   fill(x1+1,y1,x2-1,y2-1,0x2F1)
   stairs(stepx-1,y2,stepx+1,y2+1)
  def pool(x1,y1,x2,y2):
   # Native Cave basin: complete bank corners, no cut water edges.
   fill(x1,y1,x2,y2,0x27B,True)
   for x in range(x1+1,x2):put(x,y1,0x251,True);put(x,y2,0x261,True)
   for y in range(y1+1,y2):put(x1,y,0x253,True);put(x2,y,0x255,True)
   for x,y,t in [(x1,y1,0x250),(x2,y1,0x252),(x1,y2,0x260),(x2,y2,0x262)]:put(x,y,t,True)
  def shaft(x1,y1,x2,y2):
   fill(x1,y1,x2,y2,0x023,True)
   for x in range(x1,x2+1):put(x,y1,0x2F9,True);put(x,y2,0x2E9,True)
   for y in range(y1+1,y2):put(x1,y,0x2F2,True);put(x2,y,0x2F0,True)
   for x,y,t in [(x1,y1,0x2FA),(x2,y1,0x2F8),(x1,y2,0x2EA),(x2,y2,0x2E8)]:put(x,y,t,True)
  def room(x1,y1,x2,y2):
   fill(x1,y1,x2,y2,0x201)
   # Native sealed-chamber masonry frames the floor instead of a thin cave box.
   for x in range(x1,x2+1):put(x,y1,0x2F9,True);put(x,y2,0x2E9,True)
   for y in range(y1+1,y2):put(x1,y,0x2F2,True);put(x2,y,0x2F0,True)
   for x,y,t in [(x1,y1,0x2FA),(x2,y1,0x2F8),(x1,y2,0x2EA),(x2,y2,0x2E8)]:put(x,y,t,True)
  def cliff(x1,y1,x2,y2):
   fill(x1,y1,x2,y2,0x071,True)
   for x in range(x1+1,x2):put(x,y1,0x06C,True);put(x,y2,0x07C,True)
   for y in range(y1+1,y2):put(x1,y,0x073,True);put(x2,y,0x075,True)
   for x,y,t in [(x1,y1,0x06B),(x2,y1,0x06D),(x1,y2,0x07B),(x2,y2,0x07D)]:put(x,y,t,True)
  objects=[];warps=[];signs=[]
  if level==0:
   # Native Route 106 sand and complete 3x3 shoreline assemblies.
   shore={3:(13,21),4:(10,24),5:(8,26),6:(7,27),7:(6,28),8:(5,28),9:(5,28),10:(5,28),11:(5,28),12:(5,28),13:(5,28),14:(5,28),15:(6,28),16:(6,28),17:(7,28),18:(7,27),19:(7,27),20:(7,26),21:(9,25),22:(9,24),23:(11,22),24:(13,20)}
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
   # Wind-cut headland: two overlapping heights and rocky coastal shoulders.
   cliff(9,5,24,10);cliff(12,4,21,7)
   cliff(6,8,10,13);cliff(25,8,27,11)
   for dx,t in enumerate([0x22A,0x22B,0x22C]):put(15+dx,9,t,True)
   for dx in range(3):put(15+dx,10,0x235,True)
   # A ruined processional court, approached through a narrow stone stair.
   dais(11,11,21,14,16)
   for x,y in [(12,15),(20,15)]:pillar(x,y)
   # Three complete weathered monuments, rather than isolated plaque squares.
   for x,y,script in [(10,17,'Wyrmtide_ShoreTablet'),(23,14,'Wyrmtide_MakerTablet'),(19,20,'Wyrmtide_SeaTablet')]:
    stone(x-1,y-2,x+1,y,True);signs.append(sign(x,y,script))
   for x,y in [(7,14),(8,19),(25,17),(24,21),(22,6)]:put(x,y,0x202,True)
   for x,y in [(2,9),(29,17),(28,4),(5,21),(22,25)]:
    for dx,dy,t in [(0,0,0x150),(1,0,0x151),(0,1,0x158),(1,1,0x159)]:put(x+dx,y+dy,t,True,1)
   # Small wind-bent groves frame the landing and the eastern tablet trail.
   for x,y in [(7,6),(25,6),(26,12),(26,15),(7,16),(10,20),(24,18)]:
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
   room(2,1,16,22)
   # Each depth has a distinct silhouette and a legible ascending return path.
   if level==1:
    # Hall of the Maker: intact colonnade, then a stair around a fallen plinth.
    for x,y in [(4,3),(13,3),(3,9),(13,14)]:pillar(x,y)
    stone(6,6,10,8,True);stairs(12,6,14,9)
    stone(6,12,10,14);stairs(3,12,5,15)
    stone(3,18,6,20);stairs(9,17,12,19)
   elif level==2:
    # Drowned gallery: a broken ring around a tidal basin; the path hugs its west.
    pool(7,6,13,10);stone(11,12,14,15,True)
    stairs(3,8,5,11);stairs(6,14,8,17)
    for x,y in [(4,4),(14,4),(3,17),(14,18)]:pillar(x,y)
    put(6,12,0x203,True);stairs(9,19,12,19)
   elif level==3:
    # The sealed archive: two offset memorials force a long switchback.
    stone(3,6,10,9,True);stairs(12,6,14,10)
    stone(8,13,15,16,True);stairs(4,13,6,17)
    for x,y in [(4,3),(13,3),(3,19),(14,19)]:pillar(x,y)
    stairs(9,18,12,19)
   else:
    # Last procession: a broad axial stair, dark side basins, paired columns.
    shaft(3,7,6,15);shaft(12,7,15,15)
    for x,y in [(5,3),(12,3),(5,17),(14,17)]:pillar(x,y)
    stairs(8,6,10,9);stairs(8,12,10,15);stairs(9,18,12,19)
    stone(3,20,6,21);stone(13,20,15,21)
   put(8,3,0x39E);put(11,20,0x39E)
   if level in [1,3]:put(13,18,0x235,True);signs.append(sign(13,18,'Wyrmtide_DepthTablet'))
   warps=[warp(8,3,'Isle' if level==1 else 'Descent'+str(level-1),0 if level==1 else 1),warp(11,20,'Heart' if level==4 else 'Descent'+str(level+1),0)]
   scripts=f'{name}_MapScripts::\n\t.byte 0\n'
  else:
   room(2,1,20,19)
   # A sunken sanctuary: twin pools flank the stair and the central resting dais.
   # The tall inscribed headstone anchors the reveal behind the sleeping dragon.
   stone(8,2,14,4,True)
   for x in [10,11,12]:signs.append(sign(x,4,'Wyrmtide_FinalTablet'))
   for x,y in [(5,4),(16,4),(5,14),(16,14)]:pillar(x,y)
   pool(3,8,7,13);pool(15,8,19,13)
   dais(8,5,14,10,11)
   stairs(10,11,12,12)
   stone(3,17,7,18);stone(15,17,19,18)
   # Small flanking memorials echo the creator's three older guardians.
   stone(3,2,5,3);stone(17,2,19,3)
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
  l=dict(id=lid,name=name+'_Layout',width=W,height=H,primary_tileset='gTileset_General',secondary_tileset='gTileset_LegendsWyrmtideCave',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin',layout_version='emerald')
  existing=next((x for x in layouts['layouts'] if x['id']==lid),None)
  if existing:
   assert all(existing[k]==l[k] for k in l if k!='secondary_tileset'),'Never renumber or resize an existing published layout'
   existing.update(l)
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
