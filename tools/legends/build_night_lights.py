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
 'general': {0x13:[0,1],0x21:[0,1],0x42:[1],0x43:[0],0x62:[1],0x63:[0]},
 'general_frlg': {0x60:[5],0x61:[4],0x20:[0,1],0x21:[0],0x4f:[4,5],0x57:[4,5],
  0x19b:[4,5],0x19c:[4,5],0x180:[2,3],0x181:[2,3],0x182:[2,3],0x18b:[2],0x18c:[3]},
}
def words(path):return [e[0] for e in struct.iter_unpack('<H',path.read_bytes())]
def palette(path):return [tuple(map(int,l.split())) for l in path.read_text().splitlines()[3:19]]
def tile(im,t):
 x=t%(im.width//8)*8;y=t//(im.width//8)*8
 return im.crop((x,y,x+8,y+8))
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 previous=json.loads((OUT/'manifest.json').read_text()) if (OUT/'manifest.json').exists() else None
 originals={}
 for path in list((ROOT/'src/data/tilesets').glob('*.h'))+[ROOT/'src/graphics.c']:
  text=path.read_text();relative=str(path.relative_to(ROOT))
  edits={e['literal']:e['native'] for e in previous.get('header_edits',{}).get(relative,[])} if previous else {}
  index=[0]
  def restore(m):
   i=index[0];index[0]+=1
   return '"'+edits.get(i,m[1])+'"'
  originals[relative]=re.sub(r'"([^"]+)"',restore,text)
 headers='\n'.join(originals.values())
 layouts={l['id']:l for l in json.loads((ROOT/'data/layouts/layouts.json').read_text())['layouts']}
 pairs=set()
 for p in (ROOT/'data/maps').glob('*/map.json'):
  m=json.loads(p.read_text());l=layouts[m['layout']]
  if m['map_type'] in ('MAP_TYPE_CITY','MAP_TYPE_TOWN','MAP_TYPE_ROUTE','MAP_TYPE_OCEAN_ROUTE') and 'General' in l['primary_tileset']:
   family='general_frlg' if 'Frlg' in l['primary_tileset'] or 'Legends' in l['primary_tileset'] else 'general'
   body=re.search(r'const struct Tileset '+l['secondary_tileset']+r'\s*=\s*\{(.*?)\};',headers,re.S)[1]
   symbol=re.search(r'\.metatiles = (\w+)',body)[1]
   # Always resolve the native path, even after generated headers are installed.
   mt=re.search(r'const u16 '+symbol+r'\[\] = INCBIN_U16\("([^"]+)',headers)[1]
   if '/legends_lights/' in mt:mt=json.loads((OUT/'manifest.json').read_text())['native_metatiles'][symbol]
   pairs.add((family,symbol,mt))
 manifest={'families':{},'native_metatiles':{s:p for f,s,p in sorted(pairs)},'secondary':[]}
 redirects={}
 for family,selected in SELECTION.items():
  primary=ROOT/'data/tilesets/primary'/family;im=Image.open(primary/'tiles.png');mt=words(primary/'metatiles.bin')
  used={e&1023 for e in mt}
  for f,s,p in pairs:
   if f==family:used.update(e&1023 for e in words(ROOT/p))
  slots=[i for i in range(640 if family.endswith('frlg') else 512) if i not in used and not 416<=i<512]
  pals=[palette(primary/'palettes'/f'{i:02}.pal') for i in range(7)]
  pal_slot=7 if family.endswith('frlg') else 12
  color_keys=[];duplicates={};cells=[]
  for mid,entries in selected.items():
   for ei in entries:
    entry=mt[mid*8+ei];tid=entry&1023;pid=entry>>12
    def emissive(v):
     if family=='general':return v in ((3,4) if mid==0x13 else (9,10) if mid==0x21 else (11,14))
     return v in ((11,12,13,14) if pid==2 else (10,12))
    key=(tid,pid,tuple(i for i in range(16) if emissive(i)))
    if key not in duplicates:
     target=slots[len(duplicates)];duplicates[key]=target;native=tile(im,tid);painted=native.copy()
     for y in range(8):
      for x in range(8):
       v=native.getpixel((x,y))
       if not v:continue
       ck=(pals[pid][v],emissive(v))
       if ck not in color_keys:color_keys.append(ck)
       assert len(color_keys)<=15,(family,color_keys)
       painted.putpixel((x,y),color_keys.index(ck)+1)
     im.paste(painted,(target%(im.width//8)*8,target//(im.width//8)*8))
    mt[mid*8+ei]=(entry&0xc00)|(pal_slot<<12)|duplicates[key]
    cells.append({'metatile':mid,'cell':ei,'source_tile':tid,'source_palette':pid,'tile':duplicates[key]})
  im.save(OUT/(family+'_tiles.png'))
  (OUT/(family+'_metatiles.bin')).write_bytes(struct.pack('<'+'H'*len(mt),*mt))
  colors=[(0,0,0)]+[rgb for rgb,light in color_keys];colors += [(0,0,0)]*(16-len(colors))
  (OUT/(family+'.pal')).write_text('JASC-PAL\n0100\n16\n'+''.join(' '.join(map(str,c))+'\n' for c in colors))
  (OUT/(family+'.pla')).write_text('# Window panes and illuminated sign strokes only.\n'+''.join(str(i+1)+'\n' for i,(rgb,light) in enumerate(color_keys) if light))
  manifest['families'][family]={'palette':pal_slot,'cells':cells,'colors':[{'rgb':rgb,'light':light} for rgb,light in color_keys]}
  redirects[f'data/tilesets/primary/{family}/tiles.png']=f'data/tilesets/legends_lights/{family}_tiles.png'
  redirects[f'data/tilesets/primary/{family}/metatiles.bin']=f'data/tilesets/legends_lights/{family}_metatiles.bin'
  for f,s,p in sorted(pairs):
   if f!=family:continue
   base=ROOT/p;entries=words(base);usedp={e>>12 for e in entries};relocated=None
   if pal_slot in usedp:
    free=set(range(7 if family.endswith('frlg') else 6,13))-usedp;assert free,(p,'No safe palette slot')
    relocated=min(free);entries=[(e&0xfff)|(relocated<<12) if e>>12==pal_slot else e for e in entries]
    dest=f'data/tilesets/legends_lights/{base.parent.name}_metatiles.bin';(ROOT/dest).write_bytes(struct.pack('<'+'H'*len(entries),*entries));redirects[p]=dest
    redirects[str(base.parent.relative_to(ROOT)/'palettes'/f'{relocated:02}.pal')]=str(base.parent.relative_to(ROOT)/'palettes'/f'{pal_slot:02}.pal')
   redirects[str(base.parent.relative_to(ROOT)/'palettes'/f'{pal_slot:02}.pal')]=f'data/tilesets/legends_lights/{family}.pal'
   manifest['secondary'].append({'family':family,'metatiles':p,'relocated_palette':relocated})
 # Pallet's native bespoke houses/lab have blue panes isolated from their
 # red/yellow roof colors. Mark those glass colors without changing tile art.
 manifest['glass_palettes']=[]
 for slot in (8,9):
  native=f'data/tilesets/secondary/pallet_town_frlg/palettes/{slot:02}.pal'
  dest=f'data/tilesets/legends_lights/pallet_glass_{slot:02}.pal'
  (ROOT/dest).write_bytes((ROOT/native).read_bytes())
  (ROOT/dest.replace('.pal','.pla')).write_text('# Pallet house/lab window panes; roofs use other colors.\n8\n9\n10\n')
  redirects[native]=dest
  manifest['glass_palettes'].append({'native':native,'palette':dest,'lights':[8,9,10]})
 manifest['redirects']=redirects
 # Replacements are simultaneous so a relocated original palette is retained.
 manifest['header_edits']={}
 for relative,text in originals.items():
  edits=[];index=[0]
  def replace(m):
   i=index[0];index[0]+=1;new=redirects.get(m[1],m[1])
   if new!=m[1]:edits.append({'literal':i,'native':m[1]})
   return '"'+new+'"'
  (ROOT/relative).write_text(re.sub(r'"([^"]+)"',replace,text))
  if edits:manifest['header_edits'][relative]=edits
 (OUT/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print('Night lighting:',sum(len(f['cells']) for f in manifest['families'].values()),'window/sign cells;',len(manifest['secondary']),'native/imported tilesets')
if __name__=='__main__':main()
