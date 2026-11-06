"""Explicit Nightmare map authoring. Shared art and Wyrmtide are never regenerated."""
from pathlib import Path
import argparse,json,struct
from PIL import Image
R=Path(__file__).resolve().parents[2]
def save(p,d):
 p=R/p;p.parent.mkdir(parents=True,exist_ok=True)
 if not isinstance(d,(str,bytes)):d=json.dumps(d,indent=2)+'\n'
 raw=d.encode() if isinstance(d,str) else d
 if not p.exists() or p.read_bytes()!=raw:p.write_bytes(raw)
def obj(g,x,y,s,f='0'):
 return dict(graphics_id=g,x=x,y=y,elevation=3,movement_type='MOVEMENT_TYPE_FACE_DOWN',movement_range_x=0,movement_range_y=0,trainer_type='TRAINER_TYPE_NONE',trainer_sight_or_berry_tree_id='0',script=s,flag=f)
def warp(x,y,m,i):return dict(x=x,y=y,elevation=0,dest_map=m,dest_warp_id=str(i))
def sign(x,y,s):return dict(type='sign',x=x,y=y,elevation=0,player_facing_dir='BG_EVENT_PLAYER_FACING_ANY',script=s)
def main():
 p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--refresh-review',action='store_true');a=p.parse_args()
 if not a.apply:raise SystemExit('Explicit authoring only: --apply required')
 if (R/'data/maps/LegendsNightmare_Home/map.json').exists() and not a.refresh_review:raise SystemExit('Existing owner maps preserved; --refresh-review required')
 groups=json.loads((R/'data/maps/map_groups.json').read_text());layouts=json.loads((R/'data/layouts/layouts.json').read_text());lily=json.loads((R/'data/maps/LilycoveCity/map.json').read_text());raw=(R/'data/layouts/LilycoveCity/map.bin').read_bytes();cells=list(struct.unpack('<3200H',raw));before={}
 # Complete native house, roof and grass underlay; an open east approach remains.
 source=[[cells[(y+3)*80+x+35] for x in range(4)] for y in range(4)]
 for y in range(4):
  for x in range(4):
   at=(y+12)*80+x+49;before[str(at)]=cells[at];cells[at]=source[y][x]
 exitid=next((i for i,w in enumerate(lily['warp_events']) if w['dest_map']=='MAP_LEGENDS_NIGHTMARE_HOME'),len(lily['warp_events']))
 if exitid==len(lily['warp_events']):lily['warp_events'].append(warp(50,15,'MAP_LEGENDS_NIGHTMARE_HOME',0))
 save('data/maps/LilycoveCity/map.json',lily);save('data/layouts/LilycoveCity/map.bin',struct.pack('<3200H',*cells))
 W,H=12,10;home=[0x3223]*(W*H)
 def put(x,y,t,solid=False,elev=3):home[y*W+x]=t|(0x400 if solid else 0)|(elev<<12)
 # Native House1 wall, shadow/base and complete left bookcase assembly.
 for x in range(W):put(x,0,0x205,True,0);put(x,1,0x20d,True,0);put(x,2,0x224)
 original=(R/'data/layouts/House1/map.bin').read_bytes();native=struct.unpack('<90H',original)
 for y in range(3):
  for x in range(4):home[y*W+x]=native[y*10+x]
 for x in [5,9]:put(x,0,0x207,True,0);put(x,1,0x20f,True,0)
 put(10,3,0x222,True);put(10,4,0x22a,True)
 # Native two-row bed only; the preceding atlas row is wall, not furniture.
 # Side tiles include matching wooden floor, so both bedside approaches remain open.
 for y,row in enumerate([[0x2d2,0x2d3,0x2d4],[0x2da,0x2db,0x2dc]]):
  for x,t in enumerate(row):put(7+x,3+y,t,x==1,4 if (x,y)==(1,0) else 3)
 rug=[[0x235,0x236,0x237],[0x23d,0x23e,0x23f],[0x245,0x246,0x247]]
 for y,row in enumerate(rug):
  for x,t in enumerate(row):put(x+2,y+5,t)
 put(6,3,0x22b,True)
 put(5,9,0x208,False,0);put(6,9,0x209,False,0)
 template=json.loads((R/'data/maps/LilycoveCity_House2/map.json').read_text());shore=(R/'data/layouts/SouthernIsland_Exterior/map.bin').read_bytes()
 cases=[('Home',12,10,'Building','GenericBuilding',home),('Bedroom',12,10,'NightmareBuilding','NightmareInterior',home),('Street',80,40,'NightmareGeneral','NightmareLilycove',cells),('Shore',33,30,'NightmareGeneral','NightmareRustboro',list(struct.unpack('<990H',shore)))]
 for key,w,h,pri,sec,blocks in cases:
  stem='LegendsNightmare_'+key;ident='LAYOUT_LEGENDS_NIGHTMARE_'+key.upper();folder='data/layouts/'+stem
  layout=dict(id=ident,name=stem+'_Layout',width=w,height=h,primary_tileset='gTileset_'+pri,secondary_tileset='gTileset_'+sec,border_filepath=folder+'/border.bin',blockdata_filepath=folder+'/map.bin',layout_version='emerald')
  if not any(x['id']==ident for x in layouts['layouts']):layouts['layouts'].append(layout)
  if stem not in groups['gMapGroup_LegendsHoenn']:groups['gMapGroup_LegendsHoenn'].append(stem)
  save(layout['blockdata_filepath'],struct.pack('<%dH'%len(blocks),*blocks));origin='SouthernIsland_Exterior' if key=='Shore' else 'LilycoveCity' if key=='Street' else 'LilycoveCity_House2';save(layout['border_filepath'],(R/f'data/layouts/{origin}/border.bin').read_bytes())
  m=dict(template,id='MAP_LEGENDS_NIGHTMARE_'+key.upper(),name=stem,layout=ident,music='MUS_LILYCOVE' if key=='Home' else 'MUS_MT_PYRE',weather='WEATHER_NONE',map_type='MAP_TYPE_INDOOR',allow_running=True,connections=None,show_map_name=False,object_events=[],warp_events=[],coord_events=[],bg_events=[])
  load=''
  if key=='Home':
   m['object_events']=[obj('OBJ_EVENT_GFX_MAN_3',6,4,'Nightmare_Father'),obj('OBJ_EVENT_GFX_LEGENDS_MIRA_ASLEEP',8,3,'Nightmare_Bed','FLAG_TEMP_9'),obj('OBJ_EVENT_GFX_LITTLE_GIRL',8,5,'Nightmare_Mira','FLAG_TEMP_8')];m['warp_events']=[warp(x,9,'MAP_LILYCOVE_CITY',exitid) for x in [5,6]];m['bg_events']=[sign(8,4,'Nightmare_Bed'),sign(6,3,'Nightmare_Chair')];load='\tmap_script MAP_SCRIPT_ON_LOAD, Nightmare_HomeLoad\n'
  elif key=='Bedroom':
   m['warp_events']=[warp(x,9,'MAP_LEGENDS_NIGHTMARE_STREET',0) for x in [5,6]];m['bg_events']=[sign(8,4,'Nightmare_DreamBed'),sign(6,3,'Nightmare_DreamChair')];load='\tmap_script MAP_SCRIPT_ON_TRANSITION, Nightmare_EnterDream\n'
  elif key=='Street':
   m['warp_events']=[warp(50,15,'MAP_LEGENDS_NIGHTMARE_BEDROOM',0),warp(55,15,'MAP_LEGENDS_NIGHTMARE_SHORE',0)];m['object_events']=[obj('OBJ_EVENT_GFX_LITTLE_GIRL',53,17,'Nightmare_Echo')];m['bg_events']=[sign(55,15,'Nightmare_WrongDoor')]+[sign(q['x'],q['y'],'Nightmare_ClosedDoor') for q in lily['warp_events'] if (q['x'],q['y']) not in [(50,15),(55,15)]]
  else:
   m['bg_events']=[sign(16,7,'Nightmare_ShoreSign'),sign(13,22,'Nightmare_Darkrai')];m['warp_events']=[warp(x,5,'MAP_LEGENDS_NIGHTMARE_STREET',1) for x in [14,15]];m['object_events']=[obj('OBJ_EVENT_GFX_SPECIES(DARKRAI)',12,22,'Nightmare_Darkrai','FLAG_LEGENDS_NIGHTMARE_CAUGHT')];m['object_events'][0]['movement_type']='MOVEMENT_TYPE_FACE_RIGHT';load='\tmap_script MAP_SCRIPT_ON_LOAD, Nightmare_ShoreLoad\n\tmap_script MAP_SCRIPT_ON_RESUME, Nightmare_ShoreResume\n'
  save(f'data/maps/{stem}/map.json',m);save(f'data/maps/{stem}/scripts.inc',f'{stem}_MapScripts::\n'+load+'\t.byte 0\n')
 save('data/layouts/layouts.json',layouts);save('data/maps/map_groups.json',groups)
 configs=[('General','primary/general','General',False,'InitTilesetAnim_General'),('Lilycove','secondary/lilycove','Lilycove',True,'InitTilesetAnim_Lilycove'),('Rustboro','secondary/rustboro','Rustboro',True,'InitTilesetAnim_Rustboro'),('Building','primary/building','InsideBuilding',False,'InitTilesetAnim_Building'),('Interior','secondary/generic_building','GenericBuilding',True,'NULL')];header=['// Dream-only cold palettes. Native tiles, attributes and animations are reused.']
 for key,folder,symbol,sec,callback in configs:
  header.append(f'const u16 gNightmarePalettes{key}[][16] = {{')
  for i in range(16):
   p=R/f'data/tilesets/{folder}/palettes/{i:02d}.pal'
   if not p.exists():p=R/f'data/tilesets/{folder}/palettes/00.pal'
   colors=[tuple(map(int,x.split())) for x in p.read_text().splitlines()[3:19]];cold=[(round(r*.43+b*.08),round(g*.46+b*.08),min(255,round(b*.63+r*.08))) for r,g,b in colors];path=f'data/tilesets/legends_nightmare/{key.lower()}/{i:02d}.pal';save(path,'JASC-PAL\n0100\n16\n'+'\n'.join(' '.join(map(str,c)) for c in cold)+'\n');header.append(f'    INCGFX_U16("{path}", ".gbapal"),')
  header.extend(['};',f'const struct Tileset gTileset_Nightmare{key} = {{',f'    .isCompressed = TRUE, .isSecondary = {"TRUE" if sec else "FALSE"},',f'    .tiles = gTilesetTiles_{symbol}, .palettes = gNightmarePalettes{key},',f'    .metatiles = gMetatiles_{symbol}, .metatileAttributes = gMetatileAttributes_{symbol},',f'    .callback = {callback},','};'])
 save('src/data/tilesets/legends_nightmare.h','\n'.join(header)+'\n')
 source=Image.open(R/'graphics/object_events/pics/people/little_girl.png');head=Image.new('P',(144,16),0);head.putpalette(source.getpalette())
 for i in range(9):head.paste(source.crop((0,0,16,10)),(i*16,2))
 head.save(R/'graphics/object_events/pics/people/legends_mira_asleep.png')
 path=R/'data/tilesets/legends_nightmare/source.json';old=json.loads(path.read_text()) if path.exists() else {};save('data/tilesets/legends_nightmare/source.json',dict(baseline='2b99c6555954d6284a8d4ebee488e349a8e05a61',exteriorBefore=old.get('exteriorBefore',before),exteriorFootprint=[49,12,52,15],nativeHouseSource=[35,3,38,6],shore='SouthernIsland_Exterior exact block and border bytes',sleepingPortrait='Exact native Little Girl head pixels tucked into native bed',paletteScope='Private primary0..5 and secondary6..12'))
 from build_nightmare_room_floor import apply as fit_room_floor
 fit_room_floor()
 print('Authored four Nightmare maps and a complete native Lilycove house; shared art preserved.')
if __name__=='__main__':main()
