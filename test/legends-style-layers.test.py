"""Compile the real runtime hair/coat compositor and check face isolation."""
from pathlib import Path
import subprocess,tempfile
root=Path(__file__).resolve().parents[1]
source='\n'.join(x for x in (root/'src/legends_style_layers.c').read_text().splitlines() if not x.startswith('#include'))
fixture=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int bool8;
#define TRUE 1
#define FALSE 0
u8 LegendsGetScarf(void){return 0;}
''' + source + r'''
static void Setup(u8 *p,u8 w,u8 h)
{
 int x,y,face=h==64?20:12;
 memset(p,0,w*h/2);
 for(y=face-8;y<face;y++)for(x=w/2-(h==64?10:5);x<=w/2+(h==64?10:5);x++)Put(p,w,x,y,4);
 for(y=face;y<face+6;y++)for(x=w/2-3;x<=w/2+3;x++)Put(p,w,x,y,1);
 Put(p,w,w/2-2,face+2,7);Put(p,w,w/2+2,face+2,7);
 for(y=face+(h==64?14:7);y<(h==64?49:h-5);y++)
  for(x=w/2-(h==64?8:3);x<=w/2+(h==64?8:3);x++)Put(p,w,x,y,10);
}
int main(void)
{
 int w,h,gender,style,x,y;
 // Independent rolled-cuff and heel finishing uses only shoe color indices.
 u8 boots[2048]={0};
 for(y=47;y<63;y++)for(x=20;x<=27;x++)Put(boots,64,x,y,6);
 Put(boots,64,23,42,1); // forehead/skin outside the footwear region.
 LegendsPolishBoots(boots,64,64);
 assert(Pixel(boots,64,22,47)==15 && Pixel(boots,64,22,48)==6);
 assert(Pixel(boots,64,22,62)==15 && Pixel(boots,64,23,42)==1);
 for(w=16;w<=64;w*=2) {
  h=w==64?64:32;
  if(w==32)continue; // 32x32 is exercised by the field pose assets.
  for(gender=0;gender<2;gender++){
   u8 originals[2048],tmp[2048];
   u32 signatures[11]={0};
   Setup(originals,w,h);
   for(style=0;style<=10;style++){
    memcpy(tmp,originals,w*h/2);
    LegendsPaintStyle(tmp,w,h,gender,FALSE,style,0);
    for(y=0;y<h;y++)for(x=0;x<w;x++){
     u8 before=Pixel(originals,w,x,y),after=Pixel(tmp,w,x,y);
     if(before==1||before==2||before==3)assert(after==before);
     if(y==(h==64?22:14)&&before==7)assert(after==before);
     signatures[style]=signatures[style]*16777619u+(after+1)*(x+1)+(y+1);
    }
    if(!style)assert(!memcmp(tmp,originals,w*h/2));
   }
   for(style=0;style<=10;style++)for(int other=style+1;other<=10;other++)
    assert(signatures[style]!=signatures[other] && "each hairstyle needs its own silhouette");
   for(style=0;style<=2;style++){
    memcpy(tmp,originals,w*h/2);
    LegendsPaintStyle(tmp,w,h,gender,FALSE,0,style);
    if(style!=2)assert(!memcmp(tmp,originals,w*h/2));
    else {
     assert(memcmp(tmp,originals,w*h/2));
     for(y=0;y<h;y++)for(x=0;x<w;x++){
       u8 before=Pixel(originals,w,x,y),after=Pixel(tmp,w,x,y);
       if(before<=3||before==12||before==13||before==15)
         assert(after==before && "coat cannot alter face, ball or outlines");
     }
    }
   }
  }
 }
 puts("Eleven hair silhouettes, eight face/eye protections, native default, protected winter coats passed");
}
''';
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'style.c';p.write_text(fixture)
 subprocess.run(['cc','-std=gnu17','-Wall','-Wextra','-Werror','-fsanitize=address,undefined',str(p),'-o',str(Path(d)/'style')],check=True)
 subprocess.run([str(Path(d)/'style')],check=True)
 # Render the actual 16x32/32x32 native field motions and all trainer
 # front/back poses through the same compiled C routine, not a Python rewrite.
 import ctypes,sys
 sys.path.insert(0,str(root/'tools/legends'))
 from build_appearance import frames,pack,STATES,FILES
 lib=Path(d)/'style.so'
 subprocess.run(['cc','-std=gnu17','-O2','-fPIC','-shared',str(p),'-o',str(lib)],check=True)
 painter=ctypes.CDLL(str(lib)).LegendsPaintStyle
 painter.argtypes=[ctypes.POINTER(ctypes.c_ubyte),ctypes.c_ubyte,ctypes.c_ubyte,ctypes.c_ubyte,ctypes.c_int,ctypes.c_ubyte,ctypes.c_ubyte]
 poses=0
 for gender,name in enumerate(('brendan','may')):
  cases=[(root/f'graphics/object_events/pics/people/{name}/{f}.png',16 if i==0 else 32,32,0) for i,f in enumerate(FILES)]
  cases += [(root/f'graphics/object_events/pics/people/{name}/running.png',16,32,0)]
  cases += [(root/f'graphics/trainers/{kind}_pics/{name}.png',64,64,int(kind=='back')) for kind in ('front','back')]
  for asset,w,h,back in cases:
   for frame in frames(asset,w,h):
    native=pack(frame);distinct=set()
    for hair in range(11):
     buf=(ctypes.c_ubyte*len(native)).from_buffer_copy(native)
     painter(buf,w,h,gender,back,hair,0)
     result=bytes(buf);distinct.add(result)
     if hair==0:assert result==native,(asset,'original appearance')
     for a,b in zip(native,result):
      for shift in (0,4):
       v=(a>>shift)&15
       if v in (1,2,3,12,13):assert (b>>shift)&15==v,(asset,hair,'skin/ball damage')
    assert len(distinct)>=5,(asset,'hairstyles not visually distinct',len(distinct))
    for coat in (0,2):
     buf=(ctypes.c_ubyte*len(native)).from_buffer_copy(native)
     painter(buf,w,h,gender,back,0,coat)
     for a,b in zip(native,bytes(buf)):
      for shift in (0,4):
       v=(a>>shift)&15
       if v in (1,2,3,12,13,15):assert (b>>shift)&15==v,(asset,'coat touches protected index')
    poses+=1
 print(f'{poses} native player poses: 11 hairstyle shapes, winter coats, protected skin/balls and 4bpp dimensions passed')
