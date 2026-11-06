"""Explicit Wyrmtide stair authoring; preserve later owner edits and all shared art.

Use only native Cave 0x204 tread/edge pixels and Cave 0x201 floor pixels.
One flight has outer edges, four risers and floor landings; it is not a row of
repeated complete narrow stairs. No routine generator invokes this review edit.
"""
from pathlib import Path
import argparse,base64,hashlib,json,struct
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parents[2]
S=R/'data/tilesets/legends_wyrmtide';C=R/'data/tilesets/secondary/cave'
EXPECTED={
  "data/tilesets/legends_wyrmtide/tiles.png": "974fdd13c0df76cf32c1a0216781c64bb02e5e0c",
  "data/tilesets/legends_wyrmtide/metatiles.bin": "cabf042f9e0257ca9a4b2071da77fb1008725506",
  "data/tilesets/legends_wyrmtide/metatile_attributes.bin": "b75fe92328b3ca153f5f27ed7ea46bff7bdb51a1",
  "data/layouts/LegendsWyrmtide_Descent1/map.bin": "70b1544cacbd9c5228c827552ab6506c13d13507",
  "data/layouts/LegendsWyrmtide_Descent2/map.bin": "a9232435ae93c63f78e37529ddcb679c26219714",
  "data/layouts/LegendsWyrmtide_Descent3/map.bin": "43bc7204ab7b9404499bd8dd7a4cbc930e51ce9a",
  "data/layouts/LegendsWyrmtide_Descent4/map.bin": "ae598d86b5b7538ab845e34ad3f8126a102a341c",
  "data/tilesets/secondary/cave/tiles.png": "cd9a8370190b695bfdef79ab3cc7b8acfc3a6a5a",
  "data/tilesets/secondary/cave/metatiles.bin": "cc8b117e20f6477dfdeb92612730fb3136372523",
  "data/layouts/LegendsWyrmtide_Heart/map.bin": "0a28989e98a1fe5aced3323344f9b4fbc222c523",
  "data/layouts/LegendsWyrmtide_Isle/map.bin": "b6694bccdf7bf80cb60d1305d13ffb8451d6566a",
  "data/tilesets/legends_wyrmtide/source.json": "9b4f52027f94f3672d72d0960e8b588d0e434411"
}
FLIGHTS={'Descent1':[(12,9,2),(5,15,2)],'Descent2':[(5,9,2)],'Descent3':[(12,7,2),(5,13,2)],'Descent4':[(8,7,3),(8,13,3)]}
OUTPUTS=['data/tilesets/legends_wyrmtide/'+n for n in ['tiles.png','metatiles.bin','metatile_attributes.bin','source.json']]+['data/layouts/LegendsWyrmtide_'+k+'/map.bin' for k in FLIGHTS]
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def digest(p):return blob((R/p).read_bytes())
def tile(image,n):
 n-=512
 return image.crop((n%16*8,n//16*8,n%16*8+8,n//16*8+8))
def cell(image,meta,n):
 out=Image.new('P',(16,16),0)
 words=struct.unpack_from('<8H',meta,(n-512)*16)
 assert not any(words[4:]),'Review native foreground'
 for i,w in enumerate(words[:4]):
  assert w>>12==6
  t=tile(image,w&1023)
  if w&1024:t=t.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if w&2048:t=t.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  out.paste(t,(i%2*8,i//2*8))
 return out
def author(output):
 for p,h in EXPECTED.items():assert digest(p)==h,'Preserve changed source and reconcile: '+p
 meta=(S/'metatiles.bin').read_bytes();attrs=(S/'metatile_attributes.bin').read_bytes()
 assert len(meta)==433*16 and len(attrs)==433*2
 native=Image.open(C/'tiles.png');native_meta=(C/'metatiles.bin').read_bytes()
 floor=cell(native,native_meta,0x201);steps=cell(native,native_meta,0x204)
 # Keep all material colors in the existing cave bank. Avoid the original
 # bright yellow highlight and black-looking narrow stair edge.
 tone={1:2,2:3,7:6}
 def flight(width):
  im=Image.new('P',(width,32),0)
  for y in range(32):
   for x in range(width):
    v=floor.getpixel((x%16,y%16))%16
    if 8<=y<24:
     sx=x if x<2 else x-width+16 if x>=width-2 else 2+(x-2)%12
     v=steps.getpixel((sx,y-8))%16;v=tone.get(v,v)
    im.putpixel((x,y),v)
  return im
 wide=flight(32);center=flight(48);single=flight(16)
 # Left/right modules make one 32px flight. A middle module extends it to48px.
 parts=[wide.crop((0,0,16,16)),wide.crop((16,0,32,16)),
        wide.crop((0,16,16,32)),wide.crop((16,16,32,32)),
        center.crop((16,0,32,16)),center.crop((16,16,32,32)),
        single.crop((0,0,16,16)),single.crop((0,16,16,32))]
 # Existing references and all animation destinations are excluded.
 used={w[0]&1023 for w in struct.iter_unpack('<H',meta)}
 assert not used&set(range(976,1008)) and 976>931
 image=Image.open(S/'tiles.png').copy();old_pixels=image.tobytes()
 assert image.size==(128,256)
 words=[];n=976
 for part in parts:
  quartet=[]
  for i in range(4):
   image.paste(part.crop((i%2*8,i//2*8,i%2*8+8,i//2*8+8)),((n-512)%16*8,(n-512)//16*8))
   quartet.append(0x6000|n);n+=1
  words.extend(quartet+[0]*4)
 assert n==1008
 # Every pre-existing tile retains its exact indexed pixels.
 for t in range(512,976):
  assert tile(image,t).tobytes()==tile(Image.open(S/'tiles.png'),t).tobytes()
 image.save(S/'tiles.png',bits=4)
 (S/'metatiles.bin').write_bytes(meta+struct.pack('<64H',*words))
 (S/'metatile_attributes.bin').write_bytes(attrs+struct.pack('<8H',0,0,0,0,0,0,0,0x61))
 changed_cells={}
 for k,flights in FLIGHTS.items():
  p=R/('data/layouts/LegendsWyrmtide_'+k+'/map.bin');raw=p.read_bytes();a=list(struct.unpack('<456H',raw));old=a[:]
  def put(x,y,n,expect):
   at=y*19+x;assert a[at]&1023==expect,(k,x,y,hex(a[at]))
   a[at]=(a[at]&~1023)|n
  for x,y,width in flights:
   top=[0x3b1,0x3b2] if width==2 else [0x3b1,0x3b5,0x3b2]
   bottom=[0x3b3,0x3b4] if width==2 else [0x3b3,0x3b6,0x3b4]
   for dy,row in enumerate([top,bottom]):
    for dx,n in enumerate(row):put(x+dx,y+dy,n,0x39f)
  for x,y in [(8,2),(11,19)]:put(x,y,0x3b7,0x39f);put(x,y+1,0x3b8,0x39e)
  assert all((x&~1023)==(y&~1023) for x,y in zip(a,old)),'Collision/elevation changed'
  changed_cells[k]=sum(x!=y for x,y in zip(a,old))
  p.write_bytes(struct.pack('<456H',*a))
 source=json.loads((S/'source.json').read_text())
 source['authoredTileRange']=[944,1007]
 source['stairs']='Native Cave 0x204 tread/edge pixels with Cave 0x201 landings; one continuous four-riser flight, outer edges only'
 source['stairFlights']={'metatiles':[0x3b1,0x3b8],'tileRange':[976,1007],'palette':6,'toneMap':tone,'treadRows':[8,23],'floorLandingRows':[[0,7],[24,31]],'ordinaryAttributes':0,'warpBottomAttribute':0x61,'collisionAndElevationUnchanged':True,'source':'Native Cave 0x204 and 0x201'}
 (S/'source.json').write_text(json.dumps(source,indent=2)+'\n')
 for k in ['Heart','Isle']:
  p='data/layouts/LegendsWyrmtide_'+k+'/map.bin'
  assert digest(p)==EXPECTED[p]
 output.mkdir(parents=True,exist_ok=True)
 colors=[tuple(map(int,l.split())) for l in (C/'palettes/06.pal').read_text().splitlines()[3:19]]
 def rgb(im):
  im=im.copy();im.putpalette([v for color in colors for v in color]+[0]*(768-48));return im.convert('RGB')
 before=Image.new('P',(32,32),0)
 for y in [0,16]:
  for x in [0,16]:before.paste(steps,(x,y))
 sheet=Image.new('RGB',(480,184),(24,24,30));d=ImageDraw.Draw(sheet)
 for x,im,label in [(8,before,'Previous repeated flight'),(160,wide,'Continuous 32px flight'),(304,center,'48px flight')]:
  sheet.paste(rgb(im).resize((im.width*3,96),Image.Resampling.NEAREST),(x,30));d.text((x,8),label,fill='white')
 d.text((8,146),'SOURCE TILE STUDY ONLY - not a gameplay capture',fill='white')
 sheet.save(output/'Source-Stairs.png')
 report={'baseline':'792873f194ceea0d56caed20720538c822ca96a0','inputBlobs':EXPECTED,'changedCells':changed_cells,'outputBlobs':{p:digest(p) for p in OUTPUTS},'outputSHA256':{p:hashlib.sha256((R/p).read_bytes()).hexdigest() for p in OUTPUTS},'protectedMaps':['Heart','Isle'],'collisionAndElevationExact':True}
 (output/'authoring.json').write_text(json.dumps(report,indent=2)+'\n')
 for p in OUTPUTS:print('STAIR_FILE '+p+' '+digest(p)+' '+base64.b64encode((R/p).read_bytes()).decode())
 print('STAIR_IMAGE '+base64.b64encode((output/'Source-Stairs.png').read_bytes()).decode())
 print('STAIR_REPORT '+base64.b64encode((output/'authoring.json').read_bytes()).decode())
def main():
 p=argparse.ArgumentParser();p.add_argument('--apply',action='store_true');p.add_argument('--output',type=Path,default=R/'build/stair-authoring');a=p.parse_args()
 if not a.apply:raise SystemExit('Owner edits protected. --apply explicitly authors this pinned stair review.')
 author(a.output)
if __name__=='__main__':main()
