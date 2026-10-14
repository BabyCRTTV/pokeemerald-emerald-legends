"""Actual bedroom C: old-save defaults, material isolation, map geometry and safe placement."""
from pathlib import Path
import ctypes,hashlib,json,re,struct,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
def compile_api(directory):
    source=(ROOT/'src/legends_bedroom.c').read_text()
    source='\n'.join(l for l in source.splitlines() if not l.startswith('#include'))
    def palette(m):
        colors=[list(map(int,l.split())) for l in (ROOT/m[1]).read_text().splitlines()[3:19]]
        return ','.join(str((r>>3)|((g>>3)<<5)|((b>>3)<<10)) for r,g,b in colors)
    source=re.sub(r'INCGFX_U16\("([^"]+)", "\.gbapal"\)',palette,source)
    # Replace array macros with native C initializers (including nested arrays).
    for name in ['sRoomPalette','sMaleBedPalette','sFemaleBedPalette']:
        source=re.sub(r'('+name+r'\[\] = )([^;]+);',r'\1{\2};',source)
    maps=[]
    for g in ['Brendans','Mays']:
        maps.append(','.join(map(str,struct.unpack('<72H',(ROOT/f'data/layouts/LittlerootTown_{g}House_2F/map.bin').read_bytes()))))
    preamble=r'''
#include <stdint.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
typedef uint8_t u8; typedef int8_t s8; typedef uint16_t u16; typedef int16_t s16; typedef uint32_t u32; typedef int bool32; typedef uint8_t bool8;
#define TRUE 1
#define FALSE 0
#define MALE 0
#define MAP_OFFSET 7
#define MAPGRID_IMPASSABLE 0xc00
#define OBJECT_EVENTS_COUNT 16
#define DECOR_MAX_PLAYERS_HOUSE 12
#define MAP_LITTLEROOT_TOWN_BRENDANS_HOUSE_2F 1
#define MAP_LITTLEROOT_TOWN_MAYS_HOUSE_2F 2
#define MAP_GROUP(n) 1
#define MAP_NUM(n) (n)
#define RGB(r,g,b) ((r)|((g)<<5)|((b)<<10))
#define _(s) ((const u8 *)(s))
#define COMPOUND_STRING(s) ((const u8 *)(s))
#define CpuCopy16(a,b,n) memcpy(b,a,n)
#include "constants/flags.h"
#include "constants/vars.h"
#include "constants/decorations.h"
#include "legends_bedroom.h"
#include "legends_bedroom_tiles.h"
static struct {struct {u8 mapGroup,mapNum;} location;u8 playerRoomDecorations[12],playerRoomDecorationPositions[12];} save1,*gSaveBlock1Ptr=&save1;
static struct {u8 playerGender;} save2,*gSaveBlock2Ptr=&save2;
static struct {u8 objectEventId;} gPlayerAvatar={15};
static struct {const u16 *map;} layout;
static struct {struct {const u16 *map;} *mapLayout;} gMapHeader;
static u16 grid[22][23],variables[65536],gPlttBufferUnfaded[256],gPlttBufferFaded[256],gSpecialVar_Result;
static u8 flags[65536],objects[22][23],gStringVar4[1024];
static unsigned writes;
static u16 VarGet(u16 n){return variables[n];}
static void VarSet(u16 n,u16 v){variables[n]=v;writes++;}
static int FlagGet(u16 n){return flags[n];}
static void LoadPalette(const u16 *p,u16 offset,u16 size){memcpy(gPlttBufferUnfaded+offset,p,size);memcpy(gPlttBufferFaded+offset,p,size);}
static void StringCopy(u8 *p,const u8 *s){strcpy((char*)p,(const char*)s);}
static void DrawWholeMapView(void){}
static void MapGridSetMetatileEntryAt(int x,int y,u16 v){assert(x>=7&&x<16&&y>=7&&y<15);grid[y][x]=v;}
static void MapGridSetMetatileIdAt(int x,int y,u16 v){grid[y][x]=(grid[y][x]&0xf000)|v;}
static int MapGridGetCollisionAt(int x,int y){return !!(grid[y][x]&0xc00);}
static u8 MapGridGetElevationAt(int x,int y){return grid[y][x]>>12;}
static u8 GetObjectEventIdByPosition(int x,int y,int z){return objects[y][x];}
void GetDecorationDimensions(u8 decor,u8 *w,u8 *h){*w=1;*h=decor==100?2:1;}
'''
    helpers=r'''
void TestRoom(u8 gender,u8 stage){
 memset(&save1,0,sizeof(save1));memset(&save2,0,sizeof(save2));memset(variables,0,sizeof(variables));memset(flags,0,sizeof(flags));memset(objects,16,sizeof(objects));memset(grid,0,sizeof(grid));writes=0;
 save2.playerGender=gender;save1.location.mapGroup=1;save1.location.mapNum=gender+1;
 layout.map=native[gender];gMapHeader.mapLayout=(void*)&layout;
 for(int y=0;y<8;y++)for(int x=0;x<9;x++)grid[y+7][x+7]=native[gender][y*9+x];
 if(stage)flags[FLAG_RESCUED_BIRCH]=1;
 if(stage>=1)flags[FLAG_BADGE01_GET]=1;if(stage>=2)flags[FLAG_BADGE05_GET]=1;if(stage>=3)flags[FLAG_SYS_GAME_CLEAR]=1;if(stage>=4)flags[FLAG_LEGENDS_KANTO_SURVEY_REPORT]=1;
 LegendsBedroomApply();LegendsBedroomLoadPalette(0);
}
unsigned Writes(void){return writes;}
u16 Cell(int x,int y){return grid[y+7][x+7];}
u16 Color(int p,int i){return gPlttBufferUnfaded[p*16+i];}
void Rival(void){save2.playerGender^=1;}
void Away(void){save1.location.mapGroup=2;}
void Block(u8 x,u8 y){grid[y+7][x+7]|=0xc00;}
void Profile(u16 v){variables[VAR_LEGENDS_BEDROOM_COLORS]=v;}
void ChairProfile(u16 v){variables[VAR_LEGENDS_BEDROOM_CHAIR_COLOR]=v;}
u16 ChairGet(void){return variables[VAR_LEGENDS_BEDROOM_CHAIR_COLOR];}
u16 ProfileGet(void){return variables[VAR_LEGENDS_BEDROOM_COLORS];}
void AddLargeDoll(u8 x,u8 y){save1.playerRoomDecorations[0]=100;save1.playerRoomDecorationPositions[0]=(x<<4)|y;}
void AddOldDoll(u8 x,u8 y){save1.playerRoomDecorations[0]=77;save1.playerRoomDecorationPositions[0]=(x<<4)|y;}
'''
    path=Path(directory)/'bedroom.c';path.write_text(preamble+'\nstatic const u16 native[2][72]={{'+maps[0]+'},{'+maps[1]+'}};\n'+source+'\n'+helpers)
    lib=Path(directory)/'bedroom.so';subprocess.run(['cc','-shared','-fPIC','-std=c11','-Werror=implicit-function-declaration','-Wno-incompatible-pointer-types','-I'+str(ROOT/'include'),str(path),'-o',str(lib)],check=True)
    api=ctypes.CDLL(str(lib));api.ChairGet.restype=api.Color.restype=api.Cell.restype=api.ProfileGet.restype=ctypes.c_uint16
    api.LegendsBedroomColor.restype=ctypes.c_uint8
    return api

def main():
 with tempfile.TemporaryDirectory() as d:
    api=compile_api(d)
    for gender in [0,1]:
        api.TestRoom(gender,0);before=[api.Cell(x,y) for y in range(8) for x in range(9)]
        api.LegendsBedroomApply();assert before==[api.Cell(x,y) for y in range(8) for x in range(9)]
        for bad in [0,1,0xffff,0xb477,0xb488,0x8400]:
            api.Profile(bad);assert api.LegendsBedroomColor(0)==api.LegendsBedroomColor(1)==0;assert api.ProfileGet()==bad
        api.Profile(0);api.LegendsBedroomSetColor(0,2);assert api.LegendsBedroomColor(0)==2 and api.LegendsBedroomColor(1)==0
        rug=[api.Color(1,i) for i in range(16)];unrelated=[api.Color(6,i) for i in range(16)]
        api.LegendsBedroomSetColor(1,3);assert api.LegendsBedroomColor(0)==2 and api.LegendsBedroomColor(1)==3
        assert rug==[api.Color(1,i) for i in range(16)] and unrelated==[api.Color(6,i) for i in range(16)]
        bed=[api.Color(2,i) for i in range(16)];api.LegendsBedroomSetColor(0,5);assert bed==[api.Color(2,i) for i in range(16)]
        profile=api.ProfileGet();api.LegendsBedroomSetColor(1,255);assert api.ProfileGet()==profile
        api.TestRoom(gender,4)
        cx=0 if gender==0 else 8
        original=api.Cell(cx,2)
        for bad in [0,1,0xffff,0xc909,0xca07,0xcb00]:
            api.ChairProfile(bad);w=api.Writes();assert api.LegendsBedroomColor(2)==0 and api.ChairGet()==bad and api.Writes()==w
        for color in range(7):
            rug=[api.Color(1,i) for i in range(16)];bed=[api.Color(2,i) for i in range(16)]
            api.LegendsBedroomSetColor(2,color)
            assert api.LegendsBedroomColor(2)==color and api.ChairGet()==0xca00|color
            assert api.Cell(cx,2)==original
            assert rug==[api.Color(1,i) for i in range(16)] and bed==[api.Color(2,i) for i in range(16)]
            api.LegendsBedroomApply();assert api.LegendsBedroomColor(2)==color
        profile=api.ChairGet();api.LegendsBedroomSetColor(2,255);api.LegendsBedroomSetColor(3,1);assert api.ChairGet()==profile
        api.Rival();api.LegendsBedroomSetColor(2,1);assert api.ChairGet()==profile;api.Rival()
        api.TestRoom(gender,4)
        xmap=2 if gender==0 else 6
        assert api.Cell(xmap,0)==before[xmap] and api.Cell(xmap,1)==before[9+xmap]
        x=3 if gender==0 else 5
        assert 0x298<=(api.Cell(x,4)&1023)<=0x2ad # rug reaches bed edge
        for x,y in [(0,7),(3,7),(4,7),(5,7),(8,7)]:
            if api.Cell(x,y)&0xc00==0:
                # A 1x1 doll on open bottom floor keeps the room accessible.
                assert api.LegendsBedroomCanPlace(x+7,y+7,1,1),(gender,x,y)
        assert not api.LegendsBedroomCanPlace(xmap+7,7,1,1) # wall map
        wx=1 if gender==0 else 7
        assert not api.LegendsBedroomCanPlace(wx+7,13,1,1) # wardrobe
        assert not api.LegendsBedroomCanPlace(6,14,1,1) # border
        assert not api.LegendsBedroomCanPlace(wx+7,14,1,1) # blocks wardrobe approach
        if gender==0:
            api.Block(2,6)
            assert not api.LegendsBedroomCanPlace(9,14,1,1) # would isolate wardrobe route
            api.TestRoom(gender,4)
        api.AddLargeDoll(3,7)
        assert not api.LegendsBedroomCanPlace(10,13,1,1) # cannot overlap its upper half
        api.TestRoom(gender,4)
        # Previously placed doll suppresses a new fixed keepsake, keeps its record.
        api.AddOldDoll(8 if gender==0 else 0,7);api.LegendsBedroomApply()
        assert (api.Cell(8 if gender==0 else 0,7)&1023)==(before[7*9+(8 if gender==0 else 0)]&1023)
        assert not api.LegendsBedroomCanPlace((8 if gender==0 else 0)+7,14,1,1) # saved doll
        api.LegendsBedroomApply();api.LegendsBedroomLoadPalette(1) # repeat setup is stable
        profile=api.ProfileGet();api.Rival();assert not api.LegendsBedroomIsHome()
        api.LegendsBedroomSetColor(1,4);assert api.ProfileGet()==profile
        api.Away();before=[api.Color(p,i) for p in range(16) for i in range(16)]
        api.LegendsBedroomLoadPalette(0);assert before==[api.Color(p,i) for p in range(16) for i in range(16)]
    print('Bedroom C rules passed: signed legacy defaults, independent colors, seven independent original-chair colors, map preservation, wider rugs, floor placement, protected access and old decorations.')
 # Generator determinism protects all shared source art.
 paths=['data/tilesets/legends_bedroom/'+s for s in ['tiles.png','metatiles.bin','metatile_attributes.bin','sources.json']]+['include/legends_bedroom_tiles.h']
 def asset_digest(path):
  if path.endswith('.png'):
   from PIL import Image
   with Image.open(ROOT/path) as image:
    # Pillow/zlib versions may encode identical indexed art differently.
    # Preserve exact pixel indices, palette colors, dimensions and mode.
    return (image.mode,image.size,image.tobytes(),tuple(image.getpalette()))
  return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
 hashes=[asset_digest(p) for p in paths]
 subprocess.run(['python3',str(ROOT/'tools/legends/build_bedroom.py')],check=True)
 assert hashes==[asset_digest(p) for p in paths]
 # Poster overlays preserve the original console tiles below the wall.
 native=struct.unpack('<%dH'%((ROOT/'data/tilesets/secondary/brendans_mays_house/metatiles.bin').stat().st_size//2),(ROOT/'data/tilesets/secondary/brendans_mays_house/metatiles.bin').read_bytes())
 built=struct.unpack('<%dH'%((ROOT/'data/tilesets/legends_bedroom/metatiles.bin').stat().st_size//2),(ROOT/'data/tilesets/legends_bedroom/metatiles.bin').read_bytes())
 for poster,original in [(0x2cd,0x265),(0x2cf,0x257)]:
  a=built[(poster-0x200)*8:(poster-0x200+1)*8];b=native[(original-0x200)*8:(original-0x200+1)*8]
  assert a[:4]==b[:4] and a[6:]==b[6:]
 # Default is pixel-identical to each original native chair and desk support.
 from PIL import Image
 def pal(path):return [tuple(map(int,l.split())) for l in path.read_text().splitlines()[3:19]]
 room=ROOT/'data/tilesets/secondary/brendans_mays_house'
 old_atlas=Image.open(room/'tiles.png');new_atlas=Image.open(ROOT/'data/tilesets/legends_bedroom/tiles.png')
 palettes=[pal(room/f'palettes/{i:02}.pal') for i in range(16)]
 def render(words,atlas,pals):
  image=Image.new('RGB',(16,16))
  for i,w in enumerate(words):
   tile=(w&1023)-512;part=atlas.crop((tile%16*8,tile//16*8,tile%16*8+8,tile//16*8+8))
   if w&1024:part=part.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
   if w&2048:part=part.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
   for y in range(8):
    for x in range(8):
     v=part.getpixel((x,y))
     if i<4 or v:image.putpixel((i%2*8+x,(i//2%2)*8+y),pals[w>>12][v])
  return image.tobytes()
 for new,old,colorpal in [(0x2d0,0x262,7),(0x2d1,0x261,10)]:
  ps=[p[:] for p in palettes];ps[12]=ps[colorpal][:];ps[12][4]=ps[colorpal][10];ps[12][5]=ps[colorpal][8];ps[12][6]=ps[colorpal][11]
  assert render(built[(new-512)*8:(new-511)*8],new_atlas,ps)==render(native[(old-512)*8:(old-511)*8],old_atlas,palettes)
 # Measure actual native glyph widths for all new notebook/family dialogue.
 chars={c:int(v,16) for c,v in re.findall(r"^'(.)'\s*=\s*([0-9A-F]{2})\s*$",(ROOT/'charmap.txt').read_text(),re.M)};chars["'"]=0xb4
 widths=list(map(int,re.findall(r'\d+',(ROOT/'src/fonts.c').read_text().split('gFontNormalLatinGlyphWidths[] = {')[1].split('};')[0])))
 for p in ['data/scripts/legends_bedroom.inc','src/legends_bedroom.c']:
  s=(ROOT/p).read_text();lines=re.findall(r'\.string "(.*?)"',s) if p.endswith('.inc') else re.findall(r'COMPOUND_STRING\("(.*?)"\)',s)
  for text in lines:
   for line in re.split(r'\\[npl]',text.replace('$','')):assert sum(widths[chars[c]] for c in line)<=208,line
 assert 'LegendsBedroomSavedPosition' in (ROOT/'src/secret_base.c').read_text()
 assert 'VAR_LEGENDS_BEDROOM_COLORS 0x405C' in (ROOT/'include/constants/vars.h').read_text()
if __name__=='__main__':main()
