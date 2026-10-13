"""Exercise compiled male portraits, their LZ consumer format and wardrobe palettes.

Preview images decode this exact C output, not the high-resolution reference.
"""
from pathlib import Path
import ctypes, hashlib, re, subprocess, tempfile, sys
from PIL import Image, ImageDraw, ImageFont
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools/legends'))
import build_male_front as art

assets=[root/f'graphics/legends/male_front/{n}' for n in ('heads.bin','bodies.bin','shoes.bin','heads.png','manifest.json')]
before=[p.read_bytes() for p in assets];art.build();assert before==[p.read_bytes() for p in assets]
source='\n'.join(l for l in (root/'src/legends_male_front.c').read_text().splitlines() if not l.startswith('#include'))
header=(root/'src/data/legends/male_front.h').read_text()
for name in ('Heads','Bodies','Shoes'):
    data=(root/f'graphics/legends/male_front/{name.lower()}.bin').read_bytes()
    header=re.sub(r'static const u8 sMaleFront'+name+r'\[\] = INCBIN_U8\([^;]+;', 'static const u8 sMaleFront'+name+'[]={'+','.join(map(str,data))+'};',header)
pre=r'''
#include <stdint.h>
#include <string.h>
typedef uint8_t u8;typedef uint16_t u16;typedef uint32_t u32;typedef int32_t s32;typedef uint8_t bool8;
#define EWRAM_DATA
#define TRUE 1
#define FALSE 0
#define MALE 0
#define RGB(r,g,b) ((r)|((g)<<5)|((b)<<10))
#define ARRAY_COUNT(x) (sizeof(x)/sizeof((x)[0]))
#define LEGENDS_OUTFIT_COUNT 5
enum TrainerPicID {TRAINER_PIC_LEGENDS_BRENDAN_EMERALD=200,TRAINER_PIC_LEGENDS_ACCESSORY_0=210,TRAINER_PIC_LEGENDS_COSTUME_0=240};
u8 outfit,coat,scarf,shoes,hair,color,costume,skin;
u16 gLegendsTrainerPalettes[2][16];
u8 LegendsGetOutfit(void){return outfit;}u8 LegendsGetJacketStyle(void){return coat;}
u8 LegendsGetScarf(void){return scarf;}u8 LegendsGetShoes(void){return shoes;}
u8 LegendsGetHair(void){return hair;}u8 LegendsGetHairColor(void){return color;}
u8 LegendsGetCostume(void){return costume;}
void LegendsUpdateAppearancePalettes(void){
 static const u16 tones[5][3]={{0x679F,0x4EDD,0x3617},{0x575E,0x3E9A,0x29D4},{0x3E9A,0x29F5,0x194F},{0x29D5,0x1950,0x10CB},{0x1D2E,0x10CA,0x0866}};
 for(int i=0;i<3;i++)gLegendsTrainerPalettes[0][i+1]=tones[skin][i];
}
'''

def unpack(bits):
    return [[(bits[(y//8*8+x//8)*32+y%8*4+x%8//2]>>(x%2*4))&15 for x in range(64)] for y in range(64)]

def rgb(c):return ((c&31)*255//31,((c>>5)&31)*255//31,((c>>10)&31)*255//31)

with tempfile.TemporaryDirectory() as temp:
    c=Path(temp)/'front.c';c.write_text(pre+header+source)
    so=Path(temp)/'front.so';subprocess.run(['cc','-Wall','-Wextra','-Werror','-shared','-fPIC',str(c),'-o',str(so)],check=True)
    api=ctypes.CDLL(str(so));api.LegendsMaleFrontPalette.restype=ctypes.POINTER(ctypes.c_uint16)
    picture=(ctypes.c_uint32*577)();bits=(ctypes.c_uint8*2048)()
    def render(h=1,o=0,c=0,s=0,shoe=0,col=0,tone=0):
        for n,v in zip(('hair','outfit','coat','scarf','shoes','color','skin'),(h,o,c,s,shoe,col,tone)):ctypes.c_uint8.in_dll(api,n).value=v
        api.LegendsBuildMaleFront(picture,bits)
        ptr=api.LegendsMaleFrontPalette(200+o);pal=list(ptr[:16]);raw=bytes(picture)
        assert raw[:4]==b'\x10\x00\x08\x00'
        decoded=b''.join(raw[i+1:i+9] for i in range(4,2308,9))
        assert decoded==bytes(bits)
        # Calling palette first, repeatedly, must neither invalidate the output
        # nor cross-wire a different skin/hair/clothing selection.
        api.LegendsMaleFrontPalette(210+o);api.LegendsBuildMaleFront(picture,bits);assert bytes(picture)==raw
        px=unpack(decoded);im=Image.new('RGB',(64,64),(234,230,242))
        for y,row in enumerate(px):
            for x,v in enumerate(row):
                if v:im.putpixel((x,y),rgb(pal[v]))
        return im,px,pal
    body_signatures=[]
    for o in range(5):
        for c in range(3):
            for s in range(6):
                for shoe in range(8):
                    baseline,px,pal=render(1,o,c,s,shoe)
                    body_signature=baseline.crop((0,24,64,64)).tobytes()
                    for h,col,tone in ((10,7,0),(8,4,0),(3,2,0)):
                        alternate,ap,pp=render(h,o,c,s,shoe,col,tone)
                        assert alternate.crop((0,24,64,64)).tobytes()==body_signature,(o,c,s,shoe,'hair changes outfit')
                        assert [pp[i] for i in (5,8,14,15)]==[pal[i] for i in (5,8,14,15)],'eye RGB changed'
    for h in range(11):
        for col in range(8):
            for tone in range(5):
                im,px,pal=render(h,o=1 if h==0 else 0,col=col,tone=tone)
                # Lower face/eyes preserve native pixel placement; skin follows
                # the saved ramp while all hair/eye colors remain independent.
                for y in range(18,24):
                    for x in range(21,38):
                        native=art.NATIVE[y][x]
                        if native in (1,2,3,8,14,15):assert px[y][x]==native,(h,col,tone,x,y)
    assert len({render(h)[0].tobytes() for h in range(1,11)})==10
    assert not api.LegendsMaleFrontPalette(205), 'female must retain approved art'
    assert not api.LegendsMaleFrontPalette(1), 'NPC must retain native art'
    ctypes.c_uint8.in_dll(api,'costume').value=1
    assert not api.LegendsMaleFrontPalette(200), 'costume must retain fixed art'
    ctypes.c_uint8.in_dll(api,'costume').value=0
    for n in ('hair','outfit','coat','scarf','shoes','color'):ctypes.c_uint8.in_dll(api,n).value=0
    assert not api.LegendsMaleFrontPalette(200), 'unchanged Original must retain native art/palette'
    main=(root/'src/main_menu.c').read_text();assert 'LoadPalette(GetTrainerFrontPicPalette(pic), OBJ_PLTT_ID' in main
    data=(root/'include/data.h').read_text();assert 'LegendsMaleFrontPalette(trainerPic)' in data
    footwear=(root/'src/legends_footwear.c').read_text();assert 'LegendsBuildMaleFront(sFrontPic[MALE], sFrontPixels)' in footwear
    if '--preview' in sys.argv:
        labels=art.NAMES+('Emerald','Trail','Sport','Yellow','Lavender','Navy coat','Winter coat','Red scarf','Brown boots','Winter + scarf', 'Fair / Natural','Light / Black','Medium / Auburn','Brown / Blond','Deep / Silver')
        cases=[dict(h=i+1) for i in range(10)]+[dict(h=2,o=i) for i in range(5)]+[dict(h=6,c=1),dict(h=6,c=2),dict(h=4,s=1),dict(h=9,shoe=6),dict(h=3,c=2,s=2,shoe=7)]+[dict(h=i+1,tone=i,col=(0,1,4,6,7)[i]) for i in range(5)]
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
        titlefont=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',23)
        canvas=Image.new('RGB',(1120,1300),(234,230,242));draw=ImageDraw.Draw(canvas)
        draw.text((30,18),'Emerald: Legends — shared male portrait repair',font=titlefont,fill=(39,33,54))
        draw.text((30,52),'Actual compiled 64×64 sprite output • Draft for visual approval',font=font,fill=(72,61,94))
        headings=('Hairstyles 1–5','Hairstyles 6–10','Five saved outfits','Coats, scarves and footwear','Skin tones and independent hair colors')
        for i,(label,case) in enumerate(zip(labels,cases)):
            row,col=divmod(i,5);x=col*220+25;y=row*240+105
            if col==0:draw.text((30,y-20),headings[row],font=font,fill=(72,61,94))
            im,_,_=render(**case);canvas.paste(im.resize((192,192),Image.Resampling.NEAREST),(x,y))
            box=draw.textbbox((0,0),label,font=font);draw.text((x+(192-box[2])/2,y+197),label,font=font,fill=(39,33,54))
        destination=root/'docs/qa/male-front-repair-preview.png';canvas.save(destination)
        print(destination)
print('Compiled male front: 720 outfit/accessory combinations, 440 hair/color/skin choices, native eyes/anatomy, cache/LZ format and untouched female/NPC/costume routing passed')
