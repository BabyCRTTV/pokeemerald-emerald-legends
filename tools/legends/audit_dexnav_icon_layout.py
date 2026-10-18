#!/usr/bin/env python3
"""Run the shipped C icon factory on every native 32x64 icon PNG (host audit)."""
from pathlib import Path
from PIL import Image
import ast,ctypes,hashlib,json,subprocess,tempfile
R=Path(__file__).resolve().parents[2];s=(R/'src/dexnav.c').read_text();a=s.index('#define DEXNAV_ICON_MAX_WIDTH');b=s.index('#define DEXNAV_SILHOUETTE_PAL_TAG',a);code=s[a:b]
# Reuse only the literal host API stub, without executing the regression script.
tree=ast.parse((R/'test/legends-dexnav-layout.test.py').read_text());pre=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='pre' for t in n.targets))
driver=r'''
void inspect(const u8 *input,int *out){
 reset();memcpy(tiles,input,1024);CreateDexNavMonIcon(TEST_SPECIES,0,0);
 int left=99,right=-99,top=99,bottom=-99;
 for(int f=0;f<2;f++)for(int y=-16;y<16;y++)for(int x=-16;x<16;x++)
  if(opaque(f,((x*scale)>>8)+16,((y*scale)>>8)+16)){
   int dx=x+gSprites[0].x2,dy=y+gSprites[0].y2;
   if(dx<left)left=dx;if(dx>right)right=dx;if(dy<top)top=dy;if(dy>bottom)bottom=dy;
  }
 out[0]=right-left+1;out[1]=bottom-top+1;out[2]=left+right;out[3]=top+bottom;out[4]=scale;
 out[5]=!memcmp(tiles,input,1024)&&gSprites[0].images==tiles&&gSprites[0].callback==SpriteCB_MonIcon&&gSprites[0].oam.paletteNum==5;
}
'''
count=scaled=0;largest=[0,0];failures=[];digest=hashlib.sha256()
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'audit.c';p.write_text(pre+code+driver);lib=Path(d)/'audit.so';subprocess.run(['cc','-std=gnu17','-O2','-shared','-fPIC',str(p),'-o',str(lib)],check=True)
 c=ctypes.CDLL(str(lib));c.inspect.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_int)];out=(ctypes.c_int*6)()
 for p in sorted((R/'graphics/pokemon').rglob('icon*.png')):
  im=Image.open(p)
  if im.mode!='P' or im.size!=(32,64):continue
  values=list(im.getdata());assert max(values)<=15,p
  packed=bytearray(1024)
  for y in range(64):
   for x in range(32):
    offset=(y//32)*512+((y%32)//8)*128+(x//8)*32+(y%8)*4+(x%8)//2
    packed[offset]|=values[y*32+x]<<((x&1)*4)
  data=ctypes.create_string_buffer(bytes(packed));c.inspect(data,out);w,h,x,y,scale,intact=out
  count+=1;scaled+=scale>256;largest=[max(largest[0],w),max(largest[1],h)]
  digest.update(str(p.relative_to(R)).encode()+b'\0'+hashlib.sha256(p.read_bytes()).digest())
  if not (0<w<=23 and 0<h<=23 and abs(x)<=2 and abs(y)<=2 and intact):failures.append(dict(path=str(p.relative_to(R)),result=list(out)))
proof=dict(scope='Host execution of the actual shipped C factory on native PNG-derived tiled icons; GBA affine sample model, not emulator coverage of every species',icon_sheets=count,scaled_sheets=scaled,max_raster_bounds=largest,failures=failures,passed=not failures,factory_sha256=hashlib.sha256(code.encode()).hexdigest(),asset_set_sha256=digest.hexdigest())
print(json.dumps(proof,indent=2));assert not failures
