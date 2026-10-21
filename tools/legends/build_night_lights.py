#!/usr/bin/env python3
"""Duplicate only window/sign tile cells into a dedicated emissive palette.

Native source PNGs, metatiles, palette colors and layout coordinates stay intact.
The DNS compositor reads the .pla high bits. Unlit cells retain their original
palette, so roofs, walls, water and paths do not acquire the window glow.
"""
from pathlib import Path
from PIL import Image
import json,re,struct
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'data/tilesets/legends_lights'
SELECTION={
 'general': {0xb:[0,1,2,3],0x13:[0,1],0x21:[0,1],0x42:[1],0x43:[0],0x62:[1],0x63:[0]},
 'general_frlg': {0x60:[5],0x61:[4],0x20:[0,1],0x21:[0],0x4f:[4,5],0x57:[4,5],
  0x19b:[4,5],0x19c:[4,5],0x180:[2,3],0x181:[2,3],0x182:[2,3],0x18b:[2],0x18c:[3]},
}
def words(path):return [e[0] for e in struct.iter_unpack('<H',path.read_bytes())]
def palette(path):return [tuple(map(int,l.split())) for l in path.read_text().splitlines()[3:19]]
def tile(im,t):
 x=t%(im.width//8)*8;y=t//(im.width//8)*8
 return im.crop((x,y,x+8,y+8))

# Source metatiles containing actual windows; water, roofs and walls are excluded.
SECONDARY_WINDOWS = {
 'petalburg': [0x217,0x23a,0x26a,0x27d,0x287,0x28f],
 'rustboro': [0x239,0x242,0x25c,0x260,0x264,0x265,0x278,0x279,0x27a,0x27b],
 'ever_grande': [0x201,0x202,0x227],
 'fallarbor': [0x2a6,0x2ae,0x2ff,0x307],
 'lilycove': [0x20d,0x20f,0x211,0x214,0x215,0x216,0x217,0x224,0x225],
 'fortree': [0x2b8,0x2b9,0x2ba],
}
# FRLG pane variants, including the normal house's four-part window.
SELECTION['general_frlg'].update({0x6:[0,1],0x7:[0],0x43:[0,1,2,3],0x55:[0,1,2,3],0x56:[0,1,2,3],0x150:[0,1],0x154:[0,1]})

def blue_glass(rgb):
 r,g,b=rgb
 return b-r>=48 and b-g>=10 and g>70

def window_color(rgb):return (255,232,152)

def sign_color(rgb):
 r,g,b=rgb
 if max(rgb)-min(rgb)<35:return (255,146,172)
 if r>g+30:return (255,80+(g*56//255),106+(g*48//255))
 return None

def write_pal(name, colors, flags):
 path=OUT/(name+'.pal')
 path.write_text('JASC-PAL\r\n0100\r\n16\r\n'+''.join(' '.join(map(str,c))+'\r\n' for c in colors),newline='')
 path.with_suffix('.pla').write_text('# Authored light colors; slot zero selects self-emission.\n'+''.join(str(i)+'\n' for i in [0]+sorted(flags)))
 return str(path.relative_to(ROOT))

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 previous=json.loads((OUT/'manifest.json').read_text()) if (OUT/'manifest.json').exists() else {}
 originals={}
 for path in sorted((ROOT/'src/data/tilesets').glob('*.h'))+[ROOT/'src/graphics.c']:
  text=path.read_text();relative=str(path.relative_to(ROOT))
  for symbol,body in previous.get('swap_bodies',{}).get(relative,{}).items():
   text=re.sub(r'(const struct Tileset '+symbol+r'\s*=\s*\{).*?(\};)',lambda m:m[1]+body+m[2],text,flags=re.S)
  edits={e['literal']:e['native'] for e in previous.get('header_edits',{}).get(relative,[])}
  index=[0]
  def restore(m):
   i=index[0];index[0]+=1
   return '"'+edits.get(i,m[1])+'"'
  originals[relative]=re.sub(r'"([^\"]+)"',restore,text)
 headers='\n'.join(originals.values())
 layouts={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 pairs=set()
 for path in (ROOT/'data/maps').glob('*/map.json'):
  m=json.loads(path.read_text());l=layouts[m['layout']]
  if m['map_type'] not in ('MAP_TYPE_CITY','MAP_TYPE_TOWN','MAP_TYPE_ROUTE','MAP_TYPE_OCEAN_ROUTE') or 'General' not in l['primary_tileset']:continue
  family='general_frlg' if 'Frlg' in l['primary_tileset'] or 'Legends' in l['primary_tileset'] else 'general'
  symbol=l['secondary_tileset'];body=re.search(r'const struct Tileset '+symbol+r'\s*=\s*\{(.*?)\};',headers,re.S)[1]
  meta=re.search(r'\.metatiles = (\w+)',body)[1];mt=re.search(r'const u16 '+meta+r'\[\] = INCBIN_U16\("([^\"]+)',headers)[1]
  gfx=re.search(r'\.tiles = (\w+)',body)[1];image=re.search(r'const u32 '+gfx+r'\[\] = INCGFX_U32\("([^\"]+)',headers)[1]
  pairs.add((family,symbol,meta,mt,image))
 manifest={'families':{},'secondary':[],'native_metatiles':{meta:mt for f,s,meta,mt,gfx in sorted(pairs)},'glass_palettes':[],'swap_bodies':{}}
 redirects={};swaps={}
 for family,selected in SELECTION.items():
  primary=ROOT/'data/tilesets/primary'/family;im=Image.open(primary/'tiles.png');mt=words(primary/'metatiles.bin')
  used={e&1023 for e in mt}
  for f,s,meta,path,gfx in pairs:
   if f==family:used.update(e&1023 for e in words(ROOT/path))
  limit=640 if family.endswith('frlg') else 512
  free=[i for i in range(limit) if i not in used and not 416<=i<512]
  pals=[palette(primary/'palettes'/f'{i:02}.pal') for i in range(7)]
  slot=7 if family.endswith('frlg') else 12;alt=(slot+9)%16
  keys=[];duplicates={};cells=[]
  def index(rgb,night):
   key=(rgb,night)
   if key not in keys:keys.append(key)
   assert len(keys)<=15,(family,'palette full',keys)
   return keys.index(key)+1
  for mid,entries in selected.items():
   sign=mid in ((0x42,0x43,0x62,0x63) if family=='general' else (0x60,0x61))
   for ei in entries:
    entry=mt[mid*8+ei];tid=entry&1023;pid=entry>>12;native=tile(im,tid)
    def light(v):
     rgb=pals[pid][v]
     if not v:return None
     if sign:return sign_color(rgb)
     if family=='general':return window_color(rgb) if v in ((3,4) if mid in (0xb,0x13) else (9,10)) else None
     return window_color(rgb) if blue_glass(rgb) else None
    if not any(light(v) for v in native.getdata()):continue
    # Preserve original base art. Empty upper cells receive a transparent
    # light overlay; sign source upper cells are replaced without border edits.
    target_ei=ei
    if ei<4 and mt[mid*8+ei+4]&1023==0:target_ei=ei+4
    overlay=target_ei!=ei
    key=(tid,pid,sign,overlay)
    if key not in duplicates:
     target=free[len(duplicates)];duplicates[key]=target;painted=Image.new('P',(8,8),0)
     for y in range(8):
      for x in range(8):
       v=native.getpixel((x,y));night=light(v)
       if v and (night or not overlay):painted.putpixel((x,y),index(pals[pid][v],night))
     im.paste(painted,(target%(im.width//8)*8,target//(im.width//8)*8))
    mt[mid*8+target_ei]=(entry&0xc00)|(slot<<12)|duplicates[key]
    cells.append({'metatile':mid,'source_cell':ei,'cell':target_ei,'source_tile':tid,'source_palette':pid,'tile':duplicates[key],'overlay':overlay,'kind':'sign' if sign else 'window'})
  im.save(OUT/(family+'_tiles.png'));(OUT/(family+'_metatiles.bin')).write_bytes(struct.pack('<'+'H'*len(mt),*mt))
  manifest['families'][family]={'palette':slot,'alternate':alt,'cells':cells,'colors':[{'rgb':rgb,'night':night,'light':night is not None} for rgb,night in keys]}
  redirects[f'data/tilesets/primary/{family}/tiles.png']=f'data/tilesets/legends_lights/{family}_tiles.png'
  redirects[f'data/tilesets/primary/{family}/metatiles.bin']=f'data/tilesets/legends_lights/{family}_metatiles.bin'
  base_keys=keys[:]
  for f,symbol,meta,path,gfx in sorted(pairs):
   if f!=family:continue
   base=ROOT/path;folder=base.parent;name=folder.name;entries=words(base);keys[:]=base_keys
   usedp={e>>12 for e in entries};relocated=None
   if slot in usedp:
    spare=set(range(7 if family.endswith('frlg') else 6,13))-usedp;assert spare,(path,'No safe palette slot')
    relocated=min(spare);entries=[(e&0xfff)|(relocated<<12) if e>>12==slot else e for e in entries]
    redirects[str(folder.relative_to(ROOT)/'palettes'/f'{relocated:02}.pal')]=str(folder.relative_to(ROOT)/'palettes'/f'{slot:02}.pal')
   extra=[];secondary=Image.open(ROOT/gfx);base_tile=limit
   spare=set(range(7 if family.endswith('frlg') else 6,13))-usedp-{slot}
   extra_slot=min(spare) if spare else slot
   extra_alt=(extra_slot+9)%16
   if name in SECONDARY_WINDOWS:
    if extra_slot!=slot:keys.clear()
    usedt={e&1023 for e in entries};native_count=secondary.width*secondary.height//64
    # New cells follow native art when possible. Otherwise reserve unused
    # cells away from every secondary animation DMA destination.
    anim=(ROOT/'src/tileset_anims.c').read_text()
    destinations=[int(v) for v in re.findall(r'NUM_TILES_IN_PRIMARY\s*\+\s*(\d+)',anim)]
    reserved={j for start in destinations for j in range(start,start+16)}
    available=[i for i in range(1024-base_tile) if base_tile+i not in usedt and (i>=native_count or i not in reserved)]
    expanded=Image.new('P',(secondary.width,(1024-base_tile)//(secondary.width//8)*8),0);expanded.putpalette(secondary.getpalette());expanded.paste(secondary,(0,0));cache={}
    for mid in SECONDARY_WINDOWS[name]:
     local=mid-0x200
     for ei in range(8):
      source=words(base)[local*8+ei];tid=source&1023;pid=source>>12
      if tid<base_tile or pid>=13:continue
      pal=palette(folder/'palettes'/f'{pid:02}.pal') if pid>=(7 if family.endswith('frlg') else 6) else pals[pid]
      tile_source=tile(secondary,tid-base_tile)
      if not any(v and blue_glass(pal[v]) for v in tile_source.getdata()):continue
      target_ei=ei
      if ei<4 and entries[local*8+ei+4]&1023==0:target_ei=ei+4
      overlay=target_ei!=ei;key=(tid,pid,overlay)
      if key not in cache:
       target=available[len(cache)];cache[key]=target;painted=Image.new('P',(8,8),0)
       for y in range(8):
        for x in range(8):
         v=tile_source.getpixel((x,y));night=window_color(pal[v]) if v and blue_glass(pal[v]) else None
         if v and (night or not overlay):painted.putpixel((x,y),index(pal[v],night))
       expanded.paste(painted,(target%(secondary.width//8)*8,target//(secondary.width//8)*8))
      entries[local*8+target_ei]=(source&0xc00)|(extra_slot<<12)|(base_tile+cache[key])
      extra.append({'metatile':mid,'source_cell':ei,'cell':target_ei,'source_tile':tid,'source_palette':pid,'tile':base_tile+cache[key],'overlay':overlay})
    dest=f'data/tilesets/legends_lights/{name}_tiles.png';expanded.save(ROOT/dest);redirects[gfx]=dest
   if extra and extra_slot!=slot:
    ec=[(0,0,0)]+[rgb for rgb,night in keys];ec += [(0,0,0)]*(16-len(ec))
    en=[(0,0,0)]+[night or rgb for rgb,night in keys];en += [(0,0,0)]*(16-len(en));ef=[i+1 for i,(rgb,night) in enumerate(keys) if night]
    redirects[str(folder.relative_to(ROOT)/'palettes'/f'{extra_slot:02}.pal')]=write_pal(name+'_windows_day',ec,ef)
    redirects[str(folder.relative_to(ROOT)/'palettes'/f'{extra_alt:02}.pal')]=write_pal(name+'_windows_night',en,ef)
    keys[:]=base_keys
   colors=[(0,0,0)]+[rgb for rgb,night in keys];colors += [(0,0,0)]*(16-len(colors))
   nights=[(0,0,0)]+[night or rgb for rgb,night in keys];nights += [(0,0,0)]*(16-len(nights));flags=[i+1 for i,(rgb,night) in enumerate(keys) if night]
   daypath=write_pal(name+'_day',colors,flags);nightpath=write_pal(name+'_night',nights,flags)
   redirects[str(folder.relative_to(ROOT)/'palettes'/f'{slot:02}.pal')]=daypath
   redirects[str(folder.relative_to(ROOT)/'palettes'/f'{alt:02}.pal')]=nightpath
   swaps[symbol]=1<<(slot-(7 if family.endswith('frlg') else 6))
   if extra:swaps[symbol]|=1<<(extra_slot-(7 if family.endswith('frlg') else 6))
   if extra or relocated is not None:
    dest=f'data/tilesets/legends_lights/{name}_metatiles.bin';(ROOT/dest).write_bytes(struct.pack('<'+'H'*len(entries),*entries));redirects[path]=dest
   manifest['secondary'].append({'family':family,'symbol':symbol,'metatiles':path,'tiles':gfx,'day':daypath,'night':nightpath,'palette':slot,'alternate':alt,'relocated_palette':relocated,'extra_palette':extra_slot,'extra_alternate':extra_alt,'cells':extra})
 # Pallet's separate round lab/house panes already own unique glass colors.
 for slot in (8,9):
  native=f'data/tilesets/secondary/pallet_town_frlg/palettes/{slot:02}.pal';colors=palette(ROOT/native);nights=colors[:]
  for i in (8,9,10):nights[i]=window_color(colors[i])
  day=write_pal(f'pallet_glass_{slot:02}',colors,[8,9,10]);night=write_pal(f'pallet_glass_{slot:02}_night',nights,[8,9,10])
  redirects[native]=day;redirects[f'data/tilesets/secondary/pallet_town_frlg/palettes/{(slot+9)%16:02}.pal']=night
  for symbol in swaps:
   if 'PalletTown' in symbol:swaps[symbol]|=1<<(slot-7)
  manifest['glass_palettes'].append({'native':native,'palette':day,'night':night,'lights':[8,9,10]})
 # The custom cliff is a sibling of the generated Fallarbor atlas: preserve
 # all existing light art, then author only verified-unused cells.
 from build_custom_cliff import build as build_custom_cliff
 build_custom_cliff()
 redirects.update({
  'data/tilesets/secondary/fallarbor/tiles.png':'data/tilesets/legends_grotto/fallarbor_cliff_tiles.png',
  'data/tilesets/secondary/fallarbor/metatiles.bin':'data/tilesets/legends_grotto/fallarbor_cliff_metatiles.bin',
  'data/tilesets/secondary/fallarbor/metatile_attributes.bin':'data/tilesets/legends_grotto/fallarbor_cliff_attributes.bin',
 })
 manifest['redirects']=redirects;manifest['header_edits']={}
 for relative,text in originals.items():
  edits=[];index=[0]
  def replace(m):
   i=index[0];index[0]+=1;new=redirects.get(m[1],m[1])
   if new!=m[1]:edits.append({'literal':i,'native':m[1]})
   return '"'+new+'"'
  text=re.sub(r'"([^\"]+)"',replace,text)
  for symbol,bits in swaps.items():
   pattern=r'(const struct Tileset '+symbol+r'\s*=\s*\{)(.*?)(\};)'
   match=re.search(pattern,text,re.S)
   if not match:continue
   manifest['swap_bodies'].setdefault(relative,{})[symbol]=match[2]
   body=match[2];old=re.search(r'\.swapPalettes\s*=\s*([^,]+),',body)
   assert old is None,(symbol,'Existing alternate palette requires explicit merge')
   text=re.sub(pattern,lambda m:m[1]+m[2]+'    .swapPalettes = '+hex(bits)+',\n'+m[3],text,flags=re.S)
  (ROOT/relative).write_text(text)
  if edits:manifest['header_edits'][relative]=edits
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
 print('Authored night windows/signs:',sum(len(f['cells']) for f in manifest['families'].values()),'primary cells;',sum(len(s['cells']) for s in manifest['secondary']),'town cells')
if __name__=='__main__':main()
