"""Author append-only Wyrmtide maps from unchanged native Hoenn metatiles.

Only new layouts are regenerated. Existing owner-authored layouts/tilesets are
never rewritten. Native stair warp pairs and collision words are explicit.
"""
import json,struct
from PIL import Image
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
def shore_tileset():
 # Keep every used Dewford pixel/metatile and its native palm animation intact.
 # Only unused sibling cells receive exact Cave inscription pixels (palette 6,
 # unused by Dewford). The original shared tilesets are never written.
 dew=R/'data/tilesets/secondary/dewford';cave=R/'data/tilesets/secondary/cave';out=R/'data/tilesets/legends_wyrmtide_shore';out.mkdir(parents=True,exist_ok=True)
 image=Image.open(dew/'tiles.png').copy();source=Image.open(cave/'tiles.png')
 native=(dew/'metatiles.bin').read_bytes();words=struct.unpack('<%dH'%(len(native)//2),native)
 used={w&1023 for w in words};assert not used&set(range(944,1024))
 assert 6 not in {w>>12 for w in words},'Dewford palette 6 is no longer free'
 metas=[];mapping={};ids={}
 for original in [0x208,0x209,0x20A,0x218,0x235,0x21A,0x2BC,0x2C4]:
  block=[]
  for w in struct.unpack_from('<8H',(cave/'metatiles.bin').read_bytes(),(original-512)*16):
   tile=w&1023
   if tile>=512:
    if tile not in mapping:
     target=944+len(mapping);assert target<1024;mapping[tile]=target
     src=tile-512;dst=target-512
     image.paste(source.crop((src%16*8,src//16*8,src%16*8+8,src//16*8+8)),(dst%16*8,dst//16*8))
    w=(w&~1023)|mapping[tile]
   assert w>>12 in (0,3,6)
   block.append(w)
  ids[original]=512+len(native)//16+len(metas);metas.append(struct.pack('<8H',*block))
 image.save(out/'tiles.png')
 write('data/tilesets/legends_wyrmtide_shore/metatiles.bin',native+b''.join(metas))
 write('data/tilesets/legends_wyrmtide_shore/metatile_attributes.bin',(dew/'metatile_attributes.bin').read_bytes()+bytes(16))
 write('data/tilesets/legends_wyrmtide_shore/source.json',{'native':'Dewford','inscriptions':'Cave 0x208/209/20A/218/235/21A/2BC/2C4','source_to_sibling_tiles':mapping,'metatiles':ids,'palette':6,'animationReserved':[682,687]})
 return ids
def main(refresh_review=False):
 if any((R/f"data/layouts/LegendsWyrmtide_{k}/map.bin").exists() for k in ["Isle","Descent1","Descent2","Descent3","Descent4","Heart"]) and not refresh_review:
  raise SystemExit("Existing Wyrmtide maps preserved. Use --refresh-review only for explicit review-layout edits.")
 # Native Cave stair geometry; no pixel or palette files are changed.
 base=R/"data/tilesets/secondary/cave";native=(base/"metatiles.bin").read_bytes();attrs=(base/"metatile_attributes.bin").read_bytes()
 assert len(native)//16==414, "Native Cave allocation changed; review without overwriting owner art"
 tread=native[(0x396-512)*16:(0x397-512)*16]
 write("data/tilesets/legends_wyrmtide/metatiles.bin",native+tread+tread)
 write("data/tilesets/legends_wyrmtide/metatile_attributes.bin",attrs+struct.pack("<HH",0x61,0))
 shore_ids=shore_tileset()
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
   # Intact native Cave column, complete top and foot (two tiles high).
   put(x,y,shore_ids[0x2BC] if level==0 else 0x2BC,True);put(x,y+1,shore_ids[0x2C4] if level==0 else 0x2C4,True)
  def stairs(x1,y1,x2,y2):fill(x1,y1,x2,y2,0x39F)
  def tablet(x1,y1,x2):
   # Low two-row inscription ledge from the original Sealed Chamber.
   def cell(n):return shore_ids[n] if level==0 else n
   for x in range(x1,x2+1):put(x,y1,cell(0x209),True);put(x,y1+1,cell(0x235),True)
   put(x1,y1,cell(0x208),True);put(x2,y1,cell(0x20A),True)
   put(x1,y1+1,cell(0x218),True);put(x2,y1+1,cell(0x21A),True)
  def bank(x1,y1,x2,y2):
   # Native floor-height rock terrace with a coherent cap and shaded foot.
   fill(x1,y1,x2,y2,0x211,True)
   for x in range(x1+1,x2):put(x,y1,0x209,True);put(x,y2,0x219,True)
   for y in range(y1+1,y2):put(x1,y,0x210,True);put(x2,y,0x212,True)
   for x,y,t in [(x1,y1,0x208),(x2,y1,0x20A),(x1,y2,0x218),(x2,y2,0x21A)]:put(x,y,t,True)
  def pool(x1,y1,x2,y2):
   # Native Cave basin: complete bank corners, no cut water edges.
   fill(x1,y1,x2,y2,0x27B,True)
   for x in range(x1+1,x2):put(x,y1,0x251,True);put(x,y2,0x261,True)
   for y in range(y1+1,y2):put(x1,y,0x253,True);put(x2,y,0x255,True)
   for x,y,t in [(x1,y1,0x250),(x2,y1,0x252),(x1,y2,0x260),(x2,y2,0x262)]:put(x,y,t,True)
  def room():
   # Original Sealed Chamber's three-cell-deep wall grammar and bevels.
   # The old draft used outward-facing boulder rims as paper-thin room walls.
   fill(0,0,W-1,H-1,0x201)
   for y in range(H):
    depth=3-y if y<3 else y-(H-4) if y>=H-3 else 0
    if depth:
     top=y<3
     for x in range(W):
      if x<3-depth:t=0x212
      elif x==3-depth:t=0x21B if top else 0x224
      elif x>W-4+depth:t=0x210
      elif x==W-4+depth:t=0x21C if top else 0x223
      else:t=0x219 if top else 0x209
      put(x,y,t,True)
    else:
     for x in range(3):put(x,y,0x212,True);put(W-1-x,y,0x210,True)
  def headland():
   # Complete Route 106 / Regi-island rock faces, including sand-base feet.
   rows={4:(12,21),5:(10,23),6:(8,25),7:(8,25),8:(8,25),9:(9,24)}
   mask={(x,y) for y,(l,r) in rows.items() for x in range(l,r+1)}
   for x,y in sorted(mask,key=lambda p:(p[1],p[0])):
    n=(x,y-1) in mask;so=(x,y+1) in mask;w=(x-1,y) in mask;e=(x+1,y) in mask
    if not n:t=0x06B if not w else 0x06D if not e else 0x06C
    elif not so:t=0x07B if not w else 0x07D if not e else 0x07C
    elif not w:t=0x073
    elif not e:t=0x075
    else:t=0x071
    put(x,y,t,True)
   for x in range(9,25):put(x,10,0x090 if x==9 else 0x092 if x==24 else 0x091,True)
   # Same two-cell closed facade used by the original three Regi islands.
   put(16,9,0x07C,True);put(16,10,0x091,True)
  def palm(x,y):
   put(x,y,0x239,True);put(x,y+1,0x23A,True)
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
   # One headland anchors the island; vegetation frames the sheltered beach.
   headland()
   pillar(14,11);pillar(18,11)
   for x,y in [(6,11),(7,13),(8,11),(26,11),(27,13),(25,16),(26,19),(10,21)]:palm(x,y)
   # Three optional short clue spurs, with clear open approaches below each.
   for x,y,script in [(10,17,'Wyrmtide_ShoreTablet'),(23,14,'Wyrmtide_MakerTablet'),(19,20,'Wyrmtide_SeaTablet')]:
    tablet(x-1,y-1,x+1);signs.append(sign(x,y,script))
   # Native sand boulders loosely frame the approach and weathered clue spurs.
   for x,y in [(13,13),(19,13),(8,16),(8,20),(25,18),(23,21)]:put(x,y,0x0E2,True)
   for x,y in [(2,9),(29,17),(28,4),(5,22),(22,25)]:
    for dx,dy,t in [(0,0,0x150),(1,0,0x151),(0,1,0x158),(1,1,0x159)]:put(x+dx,y+dy,t,True,1)
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
   room()
   # Each landing has a deliberate route and a different relationship to water,
   # inscriptions and the central stair. No repeated giant boulder furniture.
   if level==1:
    # Entrance hall: the maker's inscription and two alternating stair flights.
    tablet(6,6,10)
    for x,y in [(4,4),(14,4)]:pillar(x,y)
    bank(3,9,15,11);stairs(12,8,13,11)
    bank(3,15,15,17);stairs(5,14,6,17)
    put(4,19,0x202,True)
   elif level==2:
    # Sea reaches the tomb: follow the dry western stair around a tidal pool.
    pool(8,6,15,12);bank(3,7,7,11);stairs(5,7,6,11)
    tablet(10,15,14)
    for x,y in [(4,4),(14,3),(4,15)]:pillar(x,y)
    put(7,13,0x203,True);put(14,18,0x202,True)
   elif level==3:
    # Memorial switchback: alternating rock terraces extend the descent.
    bank(3,7,15,9);stairs(12,6,13,9)
    bank(3,13,15,15);stairs(5,12,6,15)
    for x,y in [(4,4),(14,4)]:pillar(x,y)
    put(4,18,0x203,True)
   else:
    # Final procession: slim columns, quiet side water and a central stair.
    pool(3,7,6,14);pool(12,7,15,14)
    for x,y in [(4,3),(14,3),(4,17),(14,17)]:pillar(x,y)
    for y in range(6,15):put(7,y,0x212,True);put(11,y,0x210,True)
    stairs(8,6,10,8);stairs(8,11,10,13)
    put(8,15,0x2D5);put(10,15,0x2D5)
   # Recessed, native-looking stair mouths keep both travel directions obvious.
   put(8,2,0x39F);put(8,3,0x39E)
   stairs(10,18,12,19);put(11,20,0x39E)
   if level in [1,3]:
    tablet(12,17,14);signs.append(sign(13,18,'Wyrmtide_DepthTablet'))
   warps=[warp(8,3,'Isle' if level==1 else 'Descent'+str(level-1),0 if level==1 else 1),warp(11,20,'Heart' if level==4 else 'Descent'+str(level+1),0)]
   scripts=f'{name}_MapScripts::\n\t.byte 0\n'
  else:
   room()
   # A single inscription, seven worn stones and a quiet, axial resting place.
   # The dragon is the focal point; the floor around it stays readable.
   tablet(9,3,13)
   for x in [10,11,12]:signs.append(sign(x,4,'Wyrmtide_FinalTablet'))
   for x,y in [(6,4),(16,4),(6,14),(16,14)]:pillar(x,y)
   pool(3,8,7,12);pool(15,8,19,12)
   for x,y in [(9,6),(13,6),(8,7),(14,7),(9,9),(11,10),(13,9)]:put(x,y,0x2D5)
   bank(8,12,14,14);stairs(10,12,12,14);put(11,16,0x39F);put(11,17,0x39E)
   objects=[obj('OBJ_EVENT_GFX_VAR_F',11,7,'Wyrmtide_Regidrago','FLAG_LEGENDS_WYRMTIDE_CAUGHT')]
   warps=[warp(11,17,'Descent4',1)]
   scripts=f'''{name}_MapScripts::
\tmap_script MAP_SCRIPT_ON_TRANSITION, Wyrmtide_ChamberOnTransition
\tmap_script MAP_SCRIPT_ON_RESUME, Wyrmtide_ChamberOnResume
\t.byte 0
'''
  lid='LAYOUT_LEGENDS_WYRMTIDE_'+key.upper();mid='MAP_LEGENDS_WYRMTIDE_'+key.upper()
  write(f'data/layouts/{name}/map.bin',struct.pack('<%dH'%len(a),*a));write(f'data/layouts/{name}/border.bin',struct.pack('<4H',*([0x1170]*4 if level==0 else [0x0023]*4)))
  l=dict(id=lid,name=name+'_Layout',width=W,height=H,primary_tileset='gTileset_General',secondary_tileset='gTileset_LegendsWyrmtideShore' if level==0 else 'gTileset_LegendsWyrmtideCave',border_filepath=f'data/layouts/{name}/border.bin',blockdata_filepath=f'data/layouts/{name}/map.bin',layout_version='emerald')
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
