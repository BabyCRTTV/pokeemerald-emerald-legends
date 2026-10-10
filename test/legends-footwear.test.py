"""Exercise the actual footwear compositor on native pose art and its masks.
Protect skin/Poké Balls, validate cache lifetimes and compressed front portraits.
Optional --preview writes an authoring contact sheet (not an emulator capture).
"""
import sys,json,re,subprocess,tempfile,os,struct
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools/legends'))
from build_appearance import frames,pack,STATES,FILES
from PIL import Image

def array(name,data):return 'static const u8 '+name+'[]={'+','.join(map(str,data))+'};\n'
source='\n'.join(l for l in (root/'src/legends_footwear.c').read_text().splitlines() if not l.startswith('#include'))
header=(root/'src/data/legends/footwear_masks.h').read_text()
header=re.sub(r'static const u8 ALIGNED\(4\) sFootwearMaskData\[\] = INCBIN_U8\([^;]+;',array('sFootwearMaskData',(root/'graphics/legends/footwear/masks.bin').read_bytes()),header)
pre=r'''
#include <assert.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int32_t s32;
#define EWRAM_DATA
#define ALIGNED(x)
#define ARRAY_COUNT(x) (sizeof(x)/sizeof((x)[0]))
#define RGB(r,g,b) ((r)|((g)<<5)|((b)<<10))
#define LEGENDS_OUTFIT_COUNT 5
struct SpriteFrameImage {const u8 *data;u16 size;};
enum TrainerPicID {TRAINER_PIC_LEGENDS_BRENDAN_EMERALD=200,TRAINER_PIC_LEGENDS_ACCESSORY_0=210,TRAINER_PIC_LEGENDS_COSTUME_0=240};
static u8 shoes,costume,card;
u8 LegendsGetShoes(void){return shoes;}u8 LegendsGetCostume(void){return costume;}u8 LegendsGetCardColor(void){return card;}
void LegendsUpdateAppearancePalettes(void){}
void DecompressDataWithHeaderWram(const u32*s,void*d){memcpy(d,s,2048);}
static u16 cardPal[48];
void LoadPalette(const u16*p,int offset,int size){assert(size==2);cardPal[offset]=*p;}
'''
assets='';mapping=json.loads((root/'tools/legends/appearance_frames.json').read_text());worldTables=[]
for g,name in enumerate(('brendan','may')):
 assets+=array(f'front{g}',pack(frames(root/f'graphics/trainers/front_pics/{name}.png',64,64)[0]))
 tables=[]
 for si,(state,file) in enumerate(zip(STATES,FILES)):
  w=16 if si==0 else 32;src=frames(root/f'graphics/object_events/pics/people/{name}/{file}.png',w,32)
  if si==0:src+=frames(root/f'graphics/object_events/pics/people/{name}/running.png',16,32)
  table=mapping[name.title()][state]['table'];idx=list(range(len(src))) if 'overworld_ascending_frames' in table else [int(v) for v in re.findall(r'overworld_frame\([^,]+,\s*\d+,\s*\d+,\s*(\d+)\)',table)]
  raw=b''.join(pack(src[i]) for i in idx);symbol=f'world{g}{si}';assets+=array(symbol,raw)
  assets+='static const struct SpriteFrameImage '+symbol+'Images[]={'+','.join('{'+symbol+'+'+str(i*w*16)+','+str(w*16)+'}' for i in range(len(idx)))+'};\n';tables.append(symbol+'Images')
 worldTables.append('{'+','.join(tables)+'}')
assets+='static const struct SpriteFrameImage *const nativeWorld[2][8]={'+','.join(worldTables)+'};\nstatic const u8 *const nativeFront[2]={front0,front1};\n'
palettes=(root/'src/data/legends/appearance_palettes.h').read_text()
main=r'''
static void CheckPixels(const u8*result,const u8*original,const u8*mask,int size){
 for(int i=0;i<size;i++)for(int shift=0;shift<8;shift+=4){
  int src=(original[i]>>shift)&15,m=(mask[i]>>shift)&15,out=(result[i]>>shift)&15;
  if(!m&&(src<=3||src==12||src==13))assert(out==src);
  if(m)assert(out==(m==3?15:m==1?6:7));
 }
}
int main(int argc,char**argv){
 assert(sizeof(sWorldPixels)<=16*1024); // Keep within the GBA RAM budget.
 FILE*gallery=argc>1?fopen(argv[1],"wb"):NULL;
 FILE*world=argc>2?fopen(argv[2],"wb"):NULL;
 for(int s=0;s<8;s++){
  shoes=s;
  for(int g=0;g<2;g++){
   u16 pal[3][16];
   memcpy(pal[0],sBaseOverworldPalettes[g],32);memcpy(pal[1],sBaseTrainerPalettes[g],32);memcpy(pal[2],sBaseUnderwaterPalette,32);
   if(s)for(int kind=0;kind<3;kind++)LegendsPrepareFootwearPalette(pal[kind],g,kind);
   for(int st=0;st<8;st++){
    const struct SpriteFrameImage *src=nativeWorld[g][st],*images=LegendsFootwearImages(src,g,st);
    if(world){u8 header[4]={s,g,st,st==0?16:32};fwrite(header,1,4,world);fwrite(images[0].data,1,images[0].size,world);fwrite(pal[st==4?2:0],2,16,world);}
    if(!s){assert(images==src);continue;}
    assert(images==LegendsFootwearImages(src,g,st));
    int offset=0;
    for(int f=0;f<sFootwearFrameCount[g][st];f++){
     CheckPixels(images[f].data,src[f].data,sFootwearMasks[g][st][s>=6]+offset,src[f].size);offset+=src[f].size;
    }
   }
   const u32 *pic=LegendsFootwearFrontPic(200+5*g,(const u32*)nativeFront[g]);
   u8 output[2048];
   if(!s){assert(pic==(const u32*)nativeFront[g]);memcpy(output,nativeFront[g],2048);}
   else{
    assert(pic==LegendsFootwearFrontPic(200+5*g,(const u32*)nativeFront[g]));assert(pic[0]==0x80010);
    const u8 *compressed=(const u8*)pic;int pos=4;
    for(int i=0;i<2048;i+=8){assert(compressed[pos++]==0);memcpy(output+i,compressed+pos,8);pos+=8;}
    CheckPixels(output,nativeFront[g],sFootwearFrontMasks[g][s>=6],2048);
    u8 back[2048];memcpy(back,nativeFront[g],2048);LegendsFootwearBackPic(200+5*g,back,2048);
    for(int i=0;i<2048;i++)for(int shift=0;shift<8;shift+=4){int v=back[i]>>shift&15;assert(v!=6&&v!=7);}
   }
   if(gallery){fwrite(output,1,2048,gallery);fwrite(pal[1],2,16,gallery);}
   costume=1;assert(LegendsFootwearFrontPic(200+5*g,(const u32*)nativeFront[g])==(const u32*)nativeFront[g]);assert(LegendsFootwearImages(nativeWorld[g][0],g,0)==nativeWorld[g][0]);costume=0;
  }
 }
 for(int c=0;c<8;c++){
  card=c;for(int i=0;i<48;i++)cardPal[i]=i;LegendsApplyCardColor();
  for(int i=0;i<48;i++)if(i!=2&&i!=9&&i!=10&&i!=11&&i!=12&&i!=28&&i!=29)assert(cardPal[i]==i);
 }
 if(gallery)fclose(gallery);
 if(world)fclose(world);
 puts("Native footwear poses, color/geometry masks, caches, costume isolation, ball/skin protection and card palette passed");
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d);(p/'footwear.c').write_text(pre+header+assets+palettes+source+main)
 subprocess.run(['cc','-std=gnu17','-Werror=implicit-function-declaration','-fsanitize=address,undefined',str(p/'footwear.c'),'-o',str(p/'footwear')],check=True)
 subprocess.run([str(p/'footwear'),str(p/'gallery.bin'),str(p/'world.bin')],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0'})
 if len(sys.argv)>2 and sys.argv[1]=='--preview':
  data=(p/'gallery.bin').read_bytes();sheet=Image.new('RGB',(8*128,2*128),(175,159,218))
  for s in range(8):
   for g in range(2):
    off=(s*2+g)*2080;raw=data[off:off+2048];pal=struct.unpack_from('<16H',data,off+2048);im=Image.new('RGB',(64,64),(175,159,218))
    i=0
    for ty in range(0,64,8):
     for tx in range(0,64,8):
      for y in range(8):
       for x in range(0,8,2):
        v=raw[i];i+=1
        for dx,c in enumerate((v&15,v>>4)):
         if c:rgb=pal[c];im.putpixel((tx+x+dx,ty+y),((rgb&31)*8,(rgb>>5&31)*8,(rgb>>10&31)*8))
    sheet.paste(im.resize((128,128),Image.Resampling.NEAREST),(s*128,g*128))
  sheet.save(sys.argv[2])

  # First pose of each native movement state, rendered from actual runtime data.
  data=(p/'world.bin').read_bytes();pos=0;world=Image.new('RGB',(8*64,8*64),(175,159,218))
  while pos<len(data):
   shoe,gender,state,width=data[pos:pos+4];pos+=4;size=width*16
   raw=data[pos:pos+size];pos+=size;pal=struct.unpack_from('<16H',data,pos);pos+=32
   if shoe not in (0,1,6,7):continue
   im=Image.new('RGB',(32,32),(175,159,218));i=0
   for ty in range(0,32,8):
    for tx in range(0,width,8):
     for y in range(8):
      for x in range(0,8,2):
       v=raw[i];i+=1
       for dx,c in enumerate((v&15,v>>4)):
        if c:rgb=pal[c];im.putpixel((tx+x+dx+(8 if width==16 else 0),ty+y),((rgb&31)*8,(rgb>>5&31)*8,(rgb>>10&31)*8))
   col=gender*4+(0,1,6,7).index(shoe);world.paste(im.resize((64,64),Image.Resampling.NEAREST),(col*64,state*64))
  world.save(str(Path(sys.argv[2]).with_name('footwear-world-preview.png')))
