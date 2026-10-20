"""Run actual badge drawing code; check tile bounds, palettes, and link isolation."""
from pathlib import Path
import re,subprocess,tempfile,unittest
R=Path(__file__).resolve().parents[1];source=(R/'src/trainer_card.c').read_text()
def function(name):
 start=source.index('static void '+name+'(',source.index('static void '+name+'(')+1);body=source.index('{',start);end=body+1;depth=1
 while depth:
  depth += (source[end]=='{')-(source[end]=='}');end+=1
 return source[start:end]
class Badges(unittest.TestCase):
 def test_actual_renderer_for_all_earned_combinations_and_regions(self):
  pre=r'''
#include <stdint.h>
#include <stdbool.h>
#include <assert.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef int16_t s16;
#define NUM_BADGES 8
#define IS_FRLG 0
#define BG_PLTT_ID(x) ((x)*16)
#define PLTT_SIZE_4BPP 32
#define RGB(r,g,b) ((r)|((g)<<5)|((b)<<10))
#define WIN_CARD_TEXT 1
#define FONT_SMALL 0
#define TEXT_SKIP_DRAW 0
#define PIXEL_FILL(x) ((x)|((x)<<4))
#define COMPOUND_STRING(x) ((const u8 *)(x))
struct Data {bool isHoenn,isLink,showKantoBadges;struct {int stars;} trainerCard;u8 badgeCount[8],kantoBadges[8],badgeTiles[1024];u16 frontTilemap[600],backTilemap[600],cardTilemapBuffer[1024];} data,*sData=&data;
static u8 sKantoTrainerCardBadges_Gfx[1024],sHoennTrainerCardBadges_Gfx[1024];
static u16 sKantoTrainerCardBadges_Pal[16],sHoennTrainerCardBadges_Pal[16];static u8 sTrainerCardTextColors[3];
static int writes,filled[8],palettes[8],labelCount,clears;static u16 tilemap[32][32];
void FillBgTilemapBufferRect(int bg,int tile,int x,int y,int w,int h,int pal){
 assert(bg==3 && x>=0 && y>=0 && x+w<=32 && y+h<=32);
 if (y==15 || y==16){int slot=(x-4)/3;assert(slot>=0&&slot<8);assert(tile>=192&&tile<256);filled[slot]++;palettes[slot]=pal;writes++;}
 for(int j=y;j<y+h;j++)for(int i=x;i<x+w;i++)tilemap[j][i]=tile;
}
void FillBgTilemapBufferRect_Palette0(int bg,int tile,int x,int y,int w,int h){assert(x==4&&y==15&&w==24&&h==2);clears++;}
void LoadPalette(const void *p,int offset,int size){assert((offset==48||offset==96)&&size==32);}
void BlendPalette(int offset,int size,int coeff,int color){assert(offset==96&&size==16&&coeff==12);}
void CopyBgTilemapBufferToVram(int bg){assert(bg==3||bg==0);}
void FillWindowPixelRect(int win,int color,int x,int y,int w,int h){assert(win==1&&x>=88&&x+w<=208&&y==100&&y+h<=112);}
void AddTextPrinterParameterized3(int win,int font,int x,int y,const u8*c,int speed,const u8*text){labelCount++;assert(x>=88 && y==100);assert(strstr((const char*)text,sData->showKantoBadges?"KANTO":"HOENN"));}
int GetStringRightAlignXOffset(int font,const u8 *text,int width){return width-60;}
void DecompressDataWithHeaderWram(const void *from,void *to){}
void LoadBgTiles(int bg,const void *data,int size,int offset){assert(bg==3&&size==1024&&offset==0);}
static void PrintLegendsBadgeRegion(void);
'''
  main=r'''
int main(void){
 for(int link=0;link<2;link++)for(int front=0;front<2;front++){
  memset(&data,0,sizeof data);data.isLink=link;
  u16 *ptr=front?data.frontTilemap:data.backTilemap;
  for(int i=0;i<600;i++)ptr[i]=i;
  DrawCardFrontOrBack(ptr);
  for(int y=0;y<20;y++)for(int x=0;x<30;x++)
   assert(data.cardTilemapBuffer[y*32+x]==ptr[y*30+((!link&&front&&y>=15&&y<=16&&x>=4&&x<28)?3:x)]);
 }
 for(int mask=0;mask<256;mask++)for(int region=0;region<2;region++)for(int link=0;link<2;link++){
 memset(&data,0,sizeof data);memset(filled,0,sizeof filled);writes=labelCount=clears=0;
 data.isHoenn=1;data.isLink=link;data.showKantoBadges=region;data.trainerCard.stars=5;
 for(int i=0;i<8;i++)data.badgeCount[i]=data.kantoBadges[i]=(mask>>i)&1;
 DrawStarsAndBadgesOnCard();
 assert(labelCount==!link&&clears==!link);
 for(int i=0;i<8;i++){
 int earned=(mask>>i)&1;assert(filled[i]==(link?0:(region||earned)?4:0));
 if(!link&&(region||earned))assert(palettes[i]==(region&&!earned?6:3));
 }
 }
}
'''
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp);(p/'card.c').write_text(pre+function('DrawStarsAndBadgesOnCard')+'\n'+function('PrintLegendsBadgeRegion')+'\n'+function('DrawCardFrontOrBack')+main);subprocess.run(['gcc','-Wall','-Werror',str(p/'card.c'),'-o',str(p/'card')],check=True);subprocess.run([str(p/'card')],check=True)
 def test_link_layout_and_native_font_fit(self):
  # The public link card layout stays byte-for-byte unchanged.
  old=subprocess.check_output(['git','show','HEAD:include/trainer_card.h'],cwd=R,text=True)
  self.assertEqual((R/'include/trainer_card.h').read_text(),old)
  self.assertIn('!sData->isLink && JOY_NEW(L_BUTTON | R_BUTTON | DPAD_LEFT | DPAD_RIGHT | SELECT_BUTTON)',source)
  chars={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(R/'charmap.txt').read_text(),re.M)}
  widths=list(map(int,re.findall(r'\d+', (R/'src/fonts.c').read_text().split('gFontSmallLatinGlyphWidths[] = {')[1].split('};')[0])))
  for text in ['L/R: HOENN','L/R: KANTO']:
   self.assertLessEqual(sum(widths[chars[c]] for c in text),208)
if __name__=='__main__':unittest.main()
