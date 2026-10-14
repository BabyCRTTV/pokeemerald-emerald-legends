"""Exercise actual family palette C against every pixel of the approved study."""
import ctypes, hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools/legends'))
from build_appearance import frames,pack
from preview_family_skin import SOURCES,skin_mask,packed
record=json.loads((ROOT/'tools/legends/family_skin_approval.json').read_text())
for name,path in SOURCES.items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==record['source_sha256'][path]
family='\n'.join(line for line in (ROOT/'src/legends_family.c').read_text().splitlines() if not line.startswith('#include'))
get_skin=re.search(r'u8 LegendsGetSkinTone\(void\)\n\{.*?\n\}',(ROOT/'src/legends_appearance.c').read_text(),re.S)[0]
pre='''#include <stdint.h>
typedef uint8_t u8; typedef uint16_t u16;
#define LEGENDS_SKIN_TONE_COUNT 5
#define OBJ_EVENT_PAL_TAG_LEGENDS_MOM 0x1174
#define OBJ_EVENT_PAL_TAG_LEGENDS_NORMAN 0x1175
enum TrainerPicID { TRAINER_PIC_LEADER_NORMAN = 99 };
u16 code; u16 GetAppearanceCode(void){return code;}
void SetCode(u16 value){code=value;}
'''
with tempfile.TemporaryDirectory() as temp:
    path=Path(temp);source=path/'family.c'
    source.write_text(pre+get_skin+'\n'+(ROOT/'src/data/legends/family_palettes.h').read_text()+'\n'+family)
    subprocess.run(['cc','-shared','-fPIC','-Wall','-Wextra','-Werror',str(source),'-o',str(path/'family.so')],check=True)
    api=ctypes.CDLL(str(path/'family.so'));pointer=ctypes.POINTER(ctypes.c_uint16)
    for func in [api.LegendsGetFamilyPalette,api.LegendsGetFamilyTrainerPalette]:
        func.argtypes=[ctypes.c_int,pointer];func.restype=pointer
    native_data=(ROOT/'graphics/legends/family/mom.4bpp').read_bytes();cases=0
    for tone in range(5):
        api.SetCode(tone+1)
        for name,tag in [('mom',0x1174),('norman',0x1175),('battle',99)]:
            image=Image.open(ROOT/SOURCES[name]);pal=image.getpalette()
            colors=[packed(pal[i*3:i*3+3]) for i in range(16)]
            fallback=(ctypes.c_uint16*16)(*colors)
            getter=api.LegendsGetFamilyTrainerPalette if name=='battle' else api.LegendsGetFamilyPalette
            actual=list(getter(tag,fallback)[:16]);ramp=record['skin_ramps_RGB555'][tone]
            for pose,pixels in enumerate(frames(ROOT/SOURCES[name],64 if name=='battle' else 16,64 if name=='battle' else 32)):
                mask=skin_mask(name,pixels);runtime=[list(row) for row in pixels]
                if name=='mom':
                    for y,row in enumerate(runtime):
                        for x,v in enumerate(row):
                            if v in (1,2,3) and (x,y) not in mask:row[x]=12
                    assert pack(runtime)==native_data[pose*256:(pose+1)*256]
                for y,row in enumerate(pixels):
                    for x,v in enumerate(row):
                        expected=colors[v]
                        if (x,y) in mask:
                            if v==4:
                                channels=lambda c:(c&31,c>>5&31,c>>10&31)
                                a,b,d=map(channels,(colors[4],colors[3],ramp[2]))
                                c=[round(value*edge/base) for value,edge,base in zip(d,a,b)]
                                expected=c[0]|c[1]<<5|c[2]<<10
                            else:expected=ramp[v-1]
                        assert actual[runtime[y][x]]==expected,(name,tone,pose,x,y)
                        assert (runtime[y][x]==0)==(v==0)
                cases+=1
        for outfit in range(5):
            api.SetCode(tone+1+5*outfit)
            assert api.LegendsGetFamilyPalette(0x1174,fallback)[1]==ramp[0]
    for code in [0,26,27,28,29,30,31,65535]:
        api.SetCode(code)
        assert api.LegendsGetFamilyPalette(0x1174,fallback)[1]==record['skin_ramps_RGB555'][0][0]
    address=ctypes.addressof(fallback)
    for tag in [0,0x1100,0x1103,0x1170,0xffff]:
        assert ctypes.addressof(api.LegendsGetFamilyPalette(tag,fallback).contents)==address
    for pic in [-1,0,1,98,100,65535]:
        assert ctypes.addressof(api.LegendsGetFamilyTrainerPalette(pic,fallback).contents)==address
paths=['src/data/legends/family_palettes.h','graphics/legends/family/mom.4bpp']
before=[(ROOT/p).read_bytes() for p in paths]
subprocess.run([sys.executable,str(ROOT/'tools/legends/build_family_skin.py')],check=True)
assert before==[(ROOT/p).read_bytes() for p in paths]
movement=(ROOT/'src/event_object_movement.c').read_text()
assert movement.index('{gLegendsMomPalettes[0]')>movement.index('{gObjectEventPaletteNeonLight')
assert movement.count('selectedPalette.data = LegendsGetFamilyPalette')==2
assert 'LegendsGetFamilyPalette(originalTag' in movement
assert 'LegendsGetFamilyPalette(paletteTag' in movement
assert 'return LegendsGetFamilyTrainerPalette(trainerPic,' in (ROOT/'include/data.h').read_text()
print(f'Family skin: {cases} approved pixel/alpha cases; saved-code, isolation and deterministic ROM data checks passed.')
