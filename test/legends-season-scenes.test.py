"""Actual seasonal battle loads and Kanto time-of-day rebuilds, with native art."""
import json, os, pathlib, re, struct, subprocess, tempfile
R = pathlib.Path(__file__).resolve().parents[1]
def function(file, signature):
    s = (R/file).read_text(); start = s.index(signature + '\n{'); end = s.index('{', start) + 1; depth = 1
    while depth:
        depth += (s[end] == '{') - (s[end] == '}'); end += 1
    return s[start:end]
def stripped(file):
    return '\n'.join(x for x in (R/file).read_text().splitlines() if not x.startswith('#include'))
battle = (R/'include/constants/battle.h').read_text()
constants = re.search(r'enum BattleEnvironments\s*\{.*?\};', battle, re.S)[0]
constants += '\n' + '\n'.join(x for x in battle.splitlines() if x.startswith('#define BATTLE_TYPE_') and not x.endswith('\\'))
sections = json.loads((R/'src/data/region_map/region_map_sections.json').read_text())['map_sections']
constants += '\n' + '\n'.join(f'#define {s["id"]} {i}' for i,s in enumerate(sections))
for file in ['include/constants/map_types.h','include/constants/weather.h','include/constants/rgb.h','include/legends_seasons.h']:
    constants += '\n' + (R/file).read_text()
art = []
for name in ['tall_grass','long_grass','plain']:
    values = [tuple(map(int,x.split())) for x in (R/f'graphics/battle_environment/{name}/palette.pal').read_text().splitlines()[3:]]
    art.append([r//8 | (g//8)<<5 | (b//8)<<10 for r,g,b in values])
kanto = []
for slot in range(7):
    values = [tuple(map(int,x.split())) for x in (R/f'data/tilesets/primary/general_frlg/palettes/{slot:02d}.pal').read_text().splitlines()[3:]]
    kanto.append([r//8 | (g//8)<<5 | (b//8)<<10 for r,g,b in values])
carray = lambda rows: '{' + ','.join('{' + ','.join(map(str,row)) + '}' for row in rows) + '}'
preamble = r'''
#include <assert.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int bool32;
#define TRUE 1
#define FALSE 0
#define OW_ENABLE_DNS 1
#define ARRAY_COUNT(x) (sizeof(x)/sizeof((x)[0]))
#define BG_PLTT_ID(x) ((x)*16)
#define PLTT_SIZE_4BPP 32
#define NUM_PALS_TOTAL 13
#define PALETTES_MAP 0x1FFF
'''
preamble += constants + r'''
struct Tileset {const u16 (*palettes)[16];u8 swapPalettes;};
struct MapLayout {const struct Tileset *primaryTileset,*secondaryTileset;};
struct {u8 mapType,weather;u16 regionMapSectionId;const struct MapLayout *mapLayout;} gMapHeader;
u16 gPlttBufferUnfaded[512],gPlttBufferFaded[512];u32 gBattleTypeFlags;
static u8 season;
struct {u8 altWeight;} gTimeBlend;
u8 LegendsGetActiveSeason(void){return season;}
u32 GetNumPalsInPrimary(const struct MapLayout *l){return 7;}
void CpuCopy16(const void *s,void *d,u32 n){memcpy(d,s,n);}
void AvgPaletteWeighted(u16 *a,u16 *b,u16 *out,u8 weight){memcpy(out,a,32);}
'''
preamble += f'const u16 native[3][48] = {carray(art)};\nstatic const u16 kanto[7][16] = {carray(kanto)};\n'
preamble += r'''
const struct Tileset gTileset_LegendsKantoGeneral_Frlg={kanto,0};
static const struct Tileset other={kanto,0};
static const struct MapLayout kantoLayout={&gTileset_LegendsKantoGeneral_Frlg,&other};
'''
preamble += '#define gBattleEnvironmentPalette_TallGrass native[0]\n'
source = function('src/palette.c','void LoadPalette(const void *src, u32 offset, u32 size)')
for sig in ['bool32 LegendsMapHasSeasons(void)','bool32 LegendsMapHasSeasonalPaletteZero(void)','u16 LegendsSeasonVegetationColor(u16 color, u8 season)','void LegendsApplySeasonPalette(u16 offset, u16 count)']:
    source += '\n'+function('src/legends_seasons.c',sig)
source += '\n'+stripped('src/legends_battle_seasons.c')
source += '\n'+function('src/overworld.c','bool32 MapHasNaturalLight(enum MapType mapType)')
source += '\n'+function('src/overworld.c','void UpdateAltBgPalettes(u16 palettes)')
main = r'''
static void fresh(void){for(int i=0;i<512;i++)gPlttBufferUnfaded[i]=gPlttBufferFaded[i]=0x4210;}
static void unchanged(u16 environment){fresh();LegendsLoadBattleSeasonPalette(environment,native[0]);assert(!memcmp(gPlttBufferUnfaded+32,native[0],96));}
int main(int argc,char **argv){
 const int eligible[]={BATTLE_ENVIRONMENT_GRASS,BATTLE_ENVIRONMENT_LONG_GRASS,BATTLE_ENVIRONMENT_PLAIN};
 FILE *preview=argc>1?fopen(argv[1],"wb"):NULL;
 gMapHeader.mapType=MAP_TYPE_ROUTE;gMapHeader.weather=WEATHER_SUNNY;gMapHeader.regionMapSectionId=MAPSEC_ROUTE_101;
 for(int e=0;e<3;e++)for(season=0;season<4;season++){
  fresh();LegendsLoadBattleSeasonPalette(eligible[e],native[e]);int changed=0;
  for(int i=0;i<48;i++){
   u16 base=native[e][i];
   if(e==2 && i<32 && (i%16==1 || i%16>=11))base=native[0][i];
   u16 expected=i%16?LegendsSeasonVegetationColor(base,season):base;
   assert(gPlttBufferUnfaded[32+i]==expected&&gPlttBufferFaded[32+i]==expected);changed+=expected!=native[e][i];
  }
  assert(changed>0);for(int i=0;i<512;i++)if(i<32||i>=80)assert(gPlttBufferUnfaded[i]==0x4210&&gPlttBufferFaded[i]==0x4210);
  u16 before[48];memcpy(before,gPlttBufferUnfaded+32,96);
  LegendsLoadBattleSeasonPalette(eligible[e],native[e]);assert(!memcmp(before,gPlttBufferUnfaded+32,96));
  if(preview)fwrite(before,2,48,preview);
 }
 if(preview)fclose(preview);
 // Ordinary wild, scripted first battle and trainers get the same line/sky ramp
 // for each active season and every native map weather. Sand/ash stay native.
 for(int weather=0;weather<WEATHER_COUNT;weather++)for(season=0;season<4;season++){
  gMapHeader.weather=weather;
  for(int type=0;type<3;type++){
   gBattleTypeFlags=type==0?0:type==1?BATTLE_TYPE_FIRST_BATTLE:BATTLE_TYPE_TRAINER;
   fresh();LegendsLoadBattleSeasonPalette(BATTLE_ENVIRONMENT_PLAIN,native[2]);
   u16 plain[48];memcpy(plain,gPlttBufferUnfaded+32,96);
   LegendsLoadBattleSeasonPalette(BATTLE_ENVIRONMENT_GRASS,native[0]);
   for(int i=0;i<32;i++)if(i%16==1||i%16>=11){
    if(weather==WEATHER_SANDSTORM||weather==WEATHER_VOLCANIC_ASH)assert(plain[i]==native[2][i]);
    else assert(plain[i]==gPlttBufferUnfaded[32+i]);
   }
  }
 }
 gMapHeader.weather=WEATHER_SUNNY;gBattleTypeFlags=0;
 // The eligible background list is intentionally narrow; all special art stays native.
 for(int e=0;e<BATTLE_ENVIRONMENT_COUNT;e++)if(e!=eligible[0]&&e!=eligible[1]&&e!=eligible[2])unchanged(e);
 const u32 flags[]={BATTLE_TYPE_LINK,BATTLE_TYPE_RECORDED,BATTLE_TYPE_RECORDED_LINK,BATTLE_TYPE_FRONTIER,BATTLE_TYPE_EREADER_TRAINER,BATTLE_TYPE_TRAINER_HILL,BATTLE_TYPE_LEGENDARY};
 for(unsigned f=0;f<ARRAY_COUNT(flags);f++){gBattleTypeFlags=flags[f];unchanged(BATTLE_ENVIRONMENT_GRASS);}gBattleTypeFlags=0;
 const int maps[]={MAP_TYPE_INDOOR,MAP_TYPE_UNDERGROUND,MAP_TYPE_UNDERWATER,MAP_TYPE_SECRET_BASE};
 for(unsigned m=0;m<ARRAY_COUNT(maps);m++){gMapHeader.mapType=maps[m];unchanged(BATTLE_ENVIRONMENT_GRASS);}gMapHeader.mapType=MAP_TYPE_ROUTE;
 gMapHeader.regionMapSectionId=MAPSEC_ROUTE_111;unchanged(BATTLE_ENVIRONMENT_GRASS);
 // Kanto loads the very same active season treatment as Hoenn, including ordinary trainers.
 gMapHeader.regionMapSectionId=MAPSEC_ROUTE_6;gMapHeader.mapLayout=&kantoLayout;gBattleTypeFlags=BATTLE_TYPE_TRAINER;
 for(season=0;season<4;season++){
  fresh();LegendsLoadBattleSeasonPalette(BATTLE_ENVIRONMENT_GRASS,native[0]);assert(memcmp(gPlttBufferUnfaded+32,native[0],96));
  UpdateAltBgPalettes(1);u16 first[16];memcpy(first,gPlttBufferUnfaded,32);
  assert(first[0]==kanto[0][0]);for(int i=1;i<16;i++)assert(first[i]==LegendsSeasonVegetationColor(kanto[0][i],season));
  assert(first[1]!=kanto[0][1]&&first[13]!=kanto[0][13]); // Tree/ground foliage actually changes.
  UpdateAltBgPalettes(1);assert(!memcmp(first,gPlttBufferUnfaded,32));
  UpdateAltBgPalettes(1<<4);assert(!memcmp(kanto[4],gPlttBufferUnfaded+64,32)); // Blue water remains native.
 }
 gMapHeader.mapLayout=NULL;fresh();assert(!LegendsMapHasSeasonalPaletteZero());
 // Original palettes are const and remain unchanged after all seasonal/reload passes.
 puts("Seasonal battle palettes, all special exclusions, native reloads, Kanto slot-zero/day-night foliage and blue water passed");
}
'''
with tempfile.TemporaryDirectory() as d:
    p=pathlib.Path(d);(p/'scene.c').write_text(preamble+source+main)
    subprocess.run(['cc','-std=c99','-Wall','-Werror','-o',str(p/'scene'),str(p/'scene.c')],check=True)
    subprocess.run([str(p/'scene'),str(p/'palettes.bin')],check=True)
    if os.environ.get('LEGENDS_SEASON_PREVIEW'):
        from PIL import Image,ImageDraw
        data=struct.unpack('<576H',(p/'palettes.bin').read_bytes());canvas=Image.new('RGB',(960,384),'#f5eee1');draw=ImageDraw.Draw(canvas)
        for e,name in enumerate(['tall_grass','long_grass','plain']):
            asset='building' if name=='plain' else name
            tiles=Image.open(R/f'graphics/battle_environment/{asset}/tiles.png');raw=(R/f'graphics/battle_environment/{asset}/map.bin').read_bytes();entries=struct.unpack('<'+'H'*(len(raw)//2),raw)
            for season,label in enumerate(['Spring','Summer','Autumn','Winter']):
                pal=data[(e*4+season)*48:(e*4+season+1)*48];im=Image.new('RGB',(240,112))
                for y in range(112):
                    for x in range(240):
                        word=entries[y//8*32+x//8];t=word&1023;tx=x%8;ty=y%8
                        if word&1024:tx=7-tx
                        if word&2048:ty=7-ty
                        ci=tiles.getpixel((t%(tiles.width//8)*8+tx,t//(tiles.width//8)*8+ty))
                        c=pal[((word>>12)-2)*16+ci];im.putpixel((x,y),tuple(v*255//31 for v in [c&31,(c>>5)&31,(c>>10)&31]))
                draw.text((season*240+4,e*128+2),name.replace('_',' ')+' / '+label,fill='#332d40');canvas.paste(im,(season*240,e*128+16))
        canvas.save(os.environ['LEGENDS_SEASON_PREVIEW'])
bg=(R/'src/battle_bg.c').read_text();assert bg.count('LegendsLoadBattleSeasonPalette(')==2
assert 'LoadPalette(gBattleEnvironmentInfo[' not in bg
