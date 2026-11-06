"""Explicit native terrace-lighting review, preserving the accepted geometry."""
from pathlib import Path
import argparse, hashlib, json, struct
from PIL import Image

R = Path(__file__).resolve().parents[2]
S = R / 'data/tilesets/legends_wyrmtide'
C = R / 'data/tilesets/secondary/cave'
FLIGHTS = {'Descent1': [(12, 9, 2), (5, 15, 2)], 'Descent2': [(5, 9, 2)],
           'Descent3': [(12, 7, 2), (5, 13, 2)], 'Descent4': [(8, 7, 3), (8, 13, 3)]}
EXPECTED = {
 'data/tilesets/legends_wyrmtide/tiles.png': '32c886b52c8851c15877e07ab894c5de51e90af9',
 'data/tilesets/legends_wyrmtide/metatiles.bin': 'd8d3fc1f7c4b6ac944e89b9ef35b79e325872781',
 'data/tilesets/legends_wyrmtide/metatile_attributes.bin': 'bde2db393e71e77082653725994e0de8e3ff541a',
 'data/tilesets/legends_wyrmtide/source.json': '0be8af534fbb5c46929acd2b2b89409e0847acbf',
 'src/data/tilesets/legends_wyrmtide.h': '6632ce27955536711896bb59c46e1f3d64c20285',
 'data/layouts/LegendsWyrmtide_Descent1/map.bin': 'fe41a195c9fccee96ecd67c4ee7233a2b2b7cbe6',
 'data/layouts/LegendsWyrmtide_Descent2/map.bin': '50c0b8bbda987ca57dacd6ff3e7b0c175c53e8a4',
 'data/layouts/LegendsWyrmtide_Descent3/map.bin': '5cdce7d6fdfadcdd5af71f913ff662b7119ce5bd',
 'data/layouts/LegendsWyrmtide_Descent4/map.bin': '7219a16a5efedb98d7dec70db54516d44ba23f1d',
}


def blob(b):
 return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def colors(p):
 return [tuple(map(int, l.split())) for l in p.read_text().splitlines()[3:19]]


def author(out):
 for path, h in EXPECTED.items():
  assert blob((R / path).read_bytes()) == h, 'Preserve changed source and reconcile: ' + path
 for name in ['ledge_rim.pal', 'ledge_face.pal']:
  assert not (S / name).exists(), 'Preserve existing private palette: ' + name
 protected = {str(p.relative_to(R)): p.read_bytes() for p in [
  R/'data/layouts/LegendsWyrmtide_Heart/map.bin', R/'data/layouts/LegendsWyrmtide_Isle/map.bin', S/'water.pal']}
 meta = (S / 'metatiles.bin').read_bytes(); attrs = (S / 'metatile_attributes.bin').read_bytes()
 assert len(meta) == 441 * 16 and len(attrs) == 441 * 2
 # Banks7/8 are actually loaded and unused by all old room references.
 for key in list(FLIGHTS) + ['Heart']:
  for cell, in struct.iter_unpack('<H', (R/f'data/layouts/LegendsWyrmtide_{key}/map.bin').read_bytes()):
   n = cell & 1023
   if n >= 512:
    assert not {w[0] >> 12 for w in struct.iter_unpack('<H', meta[(n-512)*16:(n-511)*16])} & {7, 8}
 loaded = int(next(l.split()[2] for l in (R/'include/fieldmap.h').read_text().splitlines() if l.startswith('#define NUM_PALS_TOTAL ')))
 assert 8 < loaded
 base = colors(C/'palettes/06.pal'); rim = base[:]; face = base[:]
 rim[3] = base[2]  # Native warm highlight on the existing upper rim pixels.
 face[6] = colors(C/'palettes/07.pal')[7]
 face[7] = colors(R/'data/tilesets/secondary/mt_ember_frlg/palettes/12.pal')[12]
 assert face[6] == (90, 65, 57) and face[7] == (49, 32, 32)
 # Dominant floor colors retain exact native values; no new floor matte.
 assert all(face[i] == base[i] for i in range(6))
 for name, pal in [('ledge_rim.pal', rim), ('ledge_face.pal', face)]:
  (S/name).write_text('JASC-PAL\n0100\n16\n' + '\n'.join(' '.join(map(str,c)) for c in pal) + '\n')
 image = Image.open(S/'tiles.png').copy(); original = image.copy()
 def rect(t):
  t -= 512
  return (t%16*8, t//16*8, t%16*8+8, t//16*8+8)
 def indexed(n):
  im = Image.new('P', (16,16), 0)
  for i,w in enumerate(struct.unpack_from('<8H', meta, (n-512)*16)[:4]):
   tile = original.crop(rect(w&1023))
   if w&1024: tile = tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if w&2048: tile = tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   im.paste(tile, (i%2*8, i//2*8))
  return im
 # Add a single soft native-color contact row below the final riser. Tread
 # pixels8..23 and the remaining floor landing stay exact.
 for n,left,right in [(0x3B3,2,16),(0x3B4,0,14),(0x3B6,0,16),(0x3B8,2,14)]:
  words = struct.unpack_from('<8H',meta,(n-512)*16)
  for x in range(left,right):
   w = words[2+x//8]; t = w&1023; box = rect(t)
   image.putpixel((box[0]+x%8,box[1]),5)
 extra = []; extra_attrs = []; variants = []; bank_ids = {}
 def add(source, words, role):
  mid = 512 + len(meta)//16 + len(extra)
  extra.append(struct.pack('<8H',*words)); extra_attrs.append(struct.unpack_from('<H',attrs,(source-512)*2)[0])
  variants.append({'id':mid,'source':source,'role':role})
  return mid
 for n in [0x208,0x209,0x20A,0x218,0x219,0x21A]:
  bank = 7 if n < 0x218 else 8
  words = struct.unpack_from('<8H',meta,(n-512)*16)
  bank_ids[n] = add(n,[(w&0x0FFF)|(bank<<12) if w else 0 for w in words], 'upper-rim' if bank==7 else 'vertical-face')
 # Reuse the native bank-foot silhouette as a two-row contact shadow. Only
 # four unused8px tiles are allocated, with the floor underlay untouched.
 next_tile = 1008; shadow_ids = {}
 floor = list(struct.unpack_from('<8H',meta,16))
 for source in [0x219,0x21A]:
  foot = indexed(source); shadow = Image.new('P',(16,16),0)
  for x in range(16):
   if foot.getpixel((x,15)) in [6,7]:
    shadow.putpixel((x,0),6); shadow.putpixel((x,1),5)
  fore = []
  for i in range(2):
   image.paste(shadow.crop((i*8,0,i*8+8,8)),rect(next_tile)[:2])
   fore.append(0x6000|next_tile); next_tile += 1
  shadow_ids[source] = add(0x201,floor[:4]+fore+[0,0],'bank-contact-shadow-'+hex(source))
 assert next_tile == 1012
 assert not {w[0]&1023 for w in struct.iter_unpack('<H',meta)} & set(range(1008,1012))
 map_report = {}
 for key,flights in FLIGHTS.items():
  p = R/f'data/layouts/LegendsWyrmtide_{key}/map.bin'; raw=p.read_bytes(); a=list(struct.unpack('<456H',raw)); before=a[:]
  for _,y,_ in flights:
   for yy in [y,y+1]:
    for x in range(3,16):
     at=yy*19+x; n=a[at]&1023
     if n in bank_ids:a[at]=(a[at]&~1023)|bank_ids[n]
   for x in range(3,16):
    above=before[(y+1)*19+x]&1023; at=(y+2)*19+x
    if above in shadow_ids and a[at]&1023==0x201:a[at]=(a[at]&~1023)|shadow_ids[above]
  assert all((x&~1023)==(y&~1023) for x,y in zip(a,before))
  assert all(x==y for x,y in zip(a,before) if 0x3B1<=(x&1023)<=0x3B8)
  p.write_bytes(struct.pack('<456H',*a));map_report[key]={'changedCells':sum(x!=y for x,y in zip(a,before)),'movementBitsExact':True,'stairCellsExact':True}
 image.save(S/'tiles.png',bits=4)
 (S/'metatiles.bin').write_bytes(meta+b''.join(extra));(S/'metatile_attributes.bin').write_bytes(attrs+struct.pack('<8H',*extra_attrs))
 header=R/'src/data/tilesets/legends_wyrmtide.h';text=header.read_text()
 for i,name in [(7,'ledge_rim.pal'),(8,'ledge_face.pal')]:
  text=text.replace(f'data/tilesets/secondary/cave/palettes/{i:02}.pal',f'data/tilesets/legends_wyrmtide/{name}',1)
 header.write_text(text)
 source=json.loads((S/'source.json').read_text());source['authoredTileRange']=[944,1011]
 source['stairFlights']['floorLandingRows']=[[0,7],[25,31]]
 source['stairFlights']['contactShadowRows']=[24,24]
 source['terraceDepth']={'paletteBanks':[7,8],'variants':variants,'contactTiles':[1008,1011],'stairFootRow':24,'treadsAndGeometryUnchanged':True,'rimHighlight':'Cave06 index2','faceShades':['Cave07 index7','MtEmberFRLG12 index12'],'floorMatteUnchanged':True}
 (S/'source.json').write_text(json.dumps(source,indent=2)+'\n')
 for name,b in protected.items():assert (R/name).read_bytes()==b
 for t in range(512,976):assert image.crop(rect(t)).tobytes()==original.crop(rect(t)).tobytes()
 out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps({'baseline':'f707ff4c3271531f2969be487d75c18a3bc399de','inputs':EXPECTED,'maps':map_report,'variants':variants,'paletteBanks':[7,8],'nativeSourcesOnly':True,'protectedHeartIsleWaterExact':True},indent=2)+'\n')
 print('Applied native rim highlights, deeper vertical faces and fitted contact shadows.')


if __name__ == '__main__':
 p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--output',type=Path,default=R/'build/terrace-depth/authoring.json');a=p.parse_args()
 if not a.apply:raise SystemExit('Owner edits protected. --apply explicitly authors this pinned review.')
 author(a.output)
