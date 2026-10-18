"""Execute shipped DexNav geometry against tiled two-frame icons and GBA sampling."""
from pathlib import Path
import subprocess,tempfile
R=Path(__file__).resolve().parents[1];s=(R/'src/dexnav.c').read_text();a=s.index('#define DEXNAV_ICON_MAX_WIDTH');b=s.index('#define DEXNAV_SILHOUETTE_PAL_TAG',a);code=s[a:b]
pre=r'''
#include <stdint.h>
#include <assert.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
typedef uint8_t u8;typedef uint32_t u32;typedef int16_t s16;typedef int32_t s32;
enum Species {TEST_SPECIES};
#define MAX_SPRITES 64
#define FALSE 0
#define TRUE 1
#define ST_OAM_AFFINE_NORMAL 1
struct Sprite {struct {u8 affineMode,matrixNum,paletteNum;}oam;u8 affineAnimBeginning,affineAnimPaused; s16 x,y,x2,y2;const u8 *images;void(*callback)(struct Sprite*);}gSprites[65];
static u8 tiles[1024],allocated=0,matrix=3;static int scale=256,calls=0;
static void SpriteCB_MonIcon(struct Sprite *s){}
static const u8 *GetMonIconPtr(enum Species species,u32 personality){assert(personality==0xffffffff);return tiles;}
static u8 CreateMonIcon(enum Species species,void(*cb)(struct Sprite*),s16 x,s16 y,u8 p,u32 personality){
 assert(cb==SpriteCB_MonIcon&&personality==0xffffffff);calls++;
 if(allocated!=MAX_SPRITES){gSprites[allocated].x=x;gSprites[allocated].y=y;gSprites[allocated].images=tiles;gSprites[allocated].callback=cb;gSprites[allocated].oam.paletteNum=5;}
 return allocated;
}
static u8 AllocOamMatrix(void){return matrix;}
static void SetOamMatrix(u8 n,u32 a,u32 b,u32 c,u32 d){assert(n==matrix&&a==d&&!b&&!c);scale=a;}
static void pixel(int f,int x,int y){int i=f*512+(y/8)*128+(x/8)*32+(y%8)*4+(x%8)/2;tiles[i]|=1<<((x&1)*4);}
static int opaque(int f,int x,int y){if(x<0||y<0||x>=32||y>=32)return 0;int i=f*512+(y/8)*128+(x/8)*32+(y%8)*4+(x%8)/2;return (tiles[i]>>((x&1)*4))&15;}
static void reset(void){memset(tiles,0,sizeof tiles);memset(gSprites,0,sizeof gSprites);allocated=0;matrix=3;scale=256;}
'''
main=r'''
int main(void){
 unsigned cases=0;
 for(int w=1;w<=32;w++)for(int h=1;h<=32;h++)for(int side=0;side<4;side++){
  reset();int left=(side&1)?32-w:0,top=(side&2)?32-h:0;
  // Only pose 1 has full bounds; pose 0 retains an inset or small corner.
  for(int y=top;y<top+h;y++)for(int x=left;x<left+w;x++)pixel(1,x,y);
  pixel(0,left,top);u8 copy[1024];memcpy(copy,tiles,sizeof copy);
  assert(CreateDexNavMonIcon(TEST_SPECIES,20,72)==0);struct Sprite *p=&gSprites[0];
  assert(p->x==20&&p->y==72&&p->images==tiles&&p->callback==SpriteCB_MonIcon&&p->oam.paletteNum==5);
  assert(!memcmp(copy,tiles,sizeof copy));
  if(w<=22&&h<=24)assert(!p->oam.affineMode&&scale==256);
  else assert(p->oam.affineMode==1&&p->oam.matrixNum==3&&p->affineAnimPaused&&!p->affineAnimBeginning);
  int loX=99,hiX=-99,loY=99,hiY=-99;
  for(int f=0;f<2;f++)for(int dy=-16;dy<16;dy++)for(int dx=-16;dx<16;dx++){
   int sx=((dx*scale)>>8)+16,sy=((dy*scale)>>8)+16;
   if(opaque(f,sx,sy)){
    int x=dx+p->x2,y=dy+p->y2;
    if(x<loX)loX=x;if(x>hiX)hiX=x;if(y<loY)loY=y;if(y>hiY)hiY=y;
   }
  }
  // Hardware rounds samples to pixels; one pixel of raster rounding is allowed.
  assert(hiX-loX+1<=23&&hiY-loY+1<=25);
  assert(abs(loX+hiX)<=2&&abs(loY+hiY)<=2);cases++;
 }
 reset();CreateDexNavMonIcon(TEST_SPECIES,0,0);assert(!gSprites[0].x2&&!gSprites[0].y2&&!gSprites[0].oam.affineMode);
 reset();pixel(0,0,0);pixel(1,31,31);matrix=255;CreateDexNavMonIcon(TEST_SPECIES,0,0);assert(!gSprites[0].oam.affineMode&&scale==256);
 reset();allocated=MAX_SPRITES;memset(&gSprites[MAX_SPRITES],0xa5,sizeof(struct Sprite));struct Sprite guard=gSprites[MAX_SPRITES];assert(CreateDexNavMonIcon(TEST_SPECIES,0,0)==MAX_SPRITES);assert(!memcmp(&guard,&gSprites[MAX_SPRITES],sizeof guard));
 printf("PASS: %u tiled two-pose bounds/GBA raster cases, centering, shrink-only uniform scale, original art/callback/palette and failure guards\n",cases);
}
'''
with tempfile.TemporaryDirectory() as d:
 p=Path(d)/'layout.c';p.write_text(pre+code+main)
 subprocess.run(['cc','-std=gnu17','-O2','-Werror=implicit-function-declaration',str(p),'-o',d+'/layout'],check=True);subprocess.run([d+'/layout'],check=True)
selector=s[s.index('#define DEXNAV_SILHOUETTE_PAL_TAG'):s.index('static void DrawSpeciesIcons(void)\n{')]
assert selector.count('CreateDexNavMonIcon(species, x, y)')==2
free=s[s.index('static void DexNavGuiFreeResources(void)'):s.index('static void CB1_InitDexNavSearch(void)')]
assert 'FreeSpriteOamMatrix' in free and 'SpriteCB_MonIcon' in free
