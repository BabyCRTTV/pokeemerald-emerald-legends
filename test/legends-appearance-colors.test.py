"""Real v0.0.46 avatar compositor: preserve artwork and isolate smile/body colors."""
import ctypes,hashlib,json,re,struct,subprocess,sys,tempfile
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1]
BASE=json.loads((root/'test/legends-appearance-color-baseline.json').read_text())
# Share the existing native pose/mask fixture, without executing its test main.
fixture = {'__file__': str(root/'test/legends-footwear.test.py')}
exec((root/'test/legends-footwear.test.py').read_text().split("main=r'''", 1)[0], fixture)
pre = fixture['pre'].replace('void LegendsUpdateAppearancePalettes(void){}', 'void LegendsUpdateAppearancePalettes(void);')
pre = pre.replace('u8 LegendsGetScarf(void){return 0;}', 'u8 selectedScarf, skin, outfit;\nu8 LegendsGetScarf(void){return selectedScarf;}')
pre += r'''
#define LEGENDS_HAIR_COLOR_COUNT 8
static u32 sPaletteStamp;
u16 gLegendsOverworldPalettes[2][16],gLegendsTrainerPalettes[2][16],gLegendsUnderwaterPalettes[2][16];
u8 LegendsGetSkinTone(void){return skin;}
u8 LegendsGetOutfit(void){return outfit;}
u16 GetAppearanceCode(void){return 1+skin+5*outfit;}
u8 GetAccessoryCode(void){return selectedScarf+6*coat;}
u8 LegendsGetJacket(void){return coat!=0;}
u8 LegendsGetAccessoryStyle(void){return (selectedScarf!=0)|((coat!=0)<<1);}
void LegendsPrepareFootwearPalette(u16 *palette,u8 gender,u8 kind);
'''
appearance = (root/'src/legends_appearance.c').read_text()
start = appearance.index('void LegendsUpdateAppearancePalettes(void)')
brace = appearance.index('{', start); depth = 1; end = brace+1
while depth:
    depth += (appearance[end]=='{')-(appearance[end]=='}'); end += 1
palette_source = appearance[start:end]
outfits = (root/'src/data/legends/overworld_outfits.h').read_text()
accessories = (root/'src/data/legends/overworld_accessories.h').read_text()
accessories = re.sub(r'const u8 ALIGNED\(4\) sLegendsAccessoryOverworldData\[\d+\] = INCBIN_U8\([^;]+;', fixture['array']('sLegendsAccessoryOverworldData', (root/'graphics/legends/accessories/overworld.bin').read_bytes()), accessories)
def unpack_lz(data):
    size=int.from_bytes(data[1:4],'little');out=bytearray();i=4
    while len(out)<size:
        flags=data[i];i+=1
        for bit in range(7,-1,-1):
            if len(out)>=size:break
            if flags>>bit&1:
                a,b=data[i:i+2];i+=2;distance=((a&15)<<8|b)+1
                for _ in range((a>>4)+3):out.append(out[-distance])
            else:out.append(data[i]);i+=1
    return bytes(out)

front_header=(root/'src/data/legends/trainer_outfits.h').read_text()
fronts='';tables=[]
accessory_fronts=(root/'graphics/legends/accessories/trainers.bin').read_bytes()
for g,name in enumerate(('Brendan','May')):
    row=[f'front{g}']
    for o,label in enumerate(('Trail','Sport','Yellow','Lavender'),1):
        words=re.search(r'const u32 gLegends'+name+label+r'Front\[\] = \{(.*?)\};',front_header,re.S)[1]
        compressed=b''.join(struct.pack('<I',int(w,16)) for w in re.findall(r'0x([0-9A-Fa-f]+)',words))
        symbol=f'outfitFront{g}{o}';fronts+=fixture['array'](symbol,unpack_lz(compressed));row.append(symbol)
    tables.append('{'+','.join(row)+'}')
fronts+='static const u8 *const frontOutfits[2][5]={'+','.join(tables)+'};\n'
rows=[]
for style in range(3):
    genders=[]
    for g in range(2):
        row=[]
        for o in range(5):
            off=(style*10+g*5+o)*10500
            symbol=f'accessoryFront{style}{g}{o}';fronts+=fixture['array'](symbol,unpack_lz(accessory_fronts[off:off+2308]));row.append(symbol)
        genders.append('{'+','.join(row)+'}')
    rows.append('{'+','.join(genders)+'}')
fronts+='static const u8 *const frontAccessories[3][2][5]={'+','.join(rows)+'};\n'

wrappers=r'''
int Render(u8 h,u8 col,u8 tone,u8 o,u8 c,u8 s,u8 shoe,u8 state,u8 pose,u8 gender,u8 kind,u8 *pixels,u16 *palette){
 hair=h;color=col;skin=tone;outfit=o;coat=c;selectedScarf=s;shoes=shoe;
 LegendsUpdateAppearancePalettes();
 if(kind==1){
  const u8 *src=LegendsGetAccessoryStyle()?frontAccessories[LegendsGetAccessoryStyle()-1][gender][o]:frontOutfits[gender][o];
  int pic=LegendsGetAccessoryStyle()?210+((LegendsGetAccessoryStyle()-1)*2+gender)*5+o:200+gender*5+o;
  const u32 *result=LegendsFootwearFrontPic(pic,(const u32 *)src);
  if((const u8 *)result==src)memcpy(pixels,src,2048);
  else{const u8 *stream=(const u8 *)result;int pos=4;assert(result[0]==0x80010);for(int i=0;i<2048;i+=8){assert(stream[pos++]==0);memcpy(pixels+i,stream+pos,8);pos+=8;}}
  memcpy(palette,gLegendsTrainerPalettes[gender],32);assert(result==LegendsFootwearFrontPic(pic,(const u32 *)src));return 64;
 }
 const struct SpriteFrameImage *src=nativeWorld[gender][state];
 if(LegendsGetAccessoryStyle()&&state!=4)src=sLegendsAccessoryImages[LegendsGetAccessoryStyle()-1][gender][o][state];
 else if(o)src=sLegendsOutfitImages[gender][o-1][state];
 const struct SpriteFrameImage *result=LegendsFootwearImages(src,gender,state);
 assert(pose<sFootwearFrameCount[gender][state]);memcpy(pixels,result[pose].data,result[pose].size);
 memcpy(palette,state==4?gLegendsUnderwaterPalettes[gender]:gLegendsOverworldPalettes[gender],32);
 assert(result==LegendsFootwearImages(src,gender,state));return state==0?16:32;
}
int Count(u8 gender,u8 state){return sFootwearFrameCount[gender][state];}
'''

def rgb(c):return (c&31)*255//31,(c>>5&31)*255//31,(c>>10&31)*255//31
def baseline(path):return subprocess.check_output(['git','show',BASE['base']+':'+path],cwd=root)
def compile_api(temp,old=False,ref=None,shade=True):
    def read(path):return subprocess.check_output(['git','show',ref+':'+path],cwd=root) if ref else baseline(path) if old else (root/path).read_bytes()
    h=read('src/data/legends/style_layers.h').decode();b=read('graphics/legends/styles/edits.bin')
    edits=struct.unpack('<'+'H'*(len(b)//2),b)
    h=re.sub(r'static const u16 sStylePixels\[\] = INCBIN_U16\([^;]+;', 'static const u16 sStylePixels[]={'+','.join(map(str,edits))+'};',h)
    def source(path):return '\n'.join(l for l in read(path).decode().splitlines() if not l.startswith('#include'))
    c=Path(temp)/('before.c' if old else 'after.c');so=c.with_suffix('.so')
    footwear=source('src/legends_footwear.c')
    if not shade:
        # Reproduce the pre-shading pipeline for exact before/after QA.
        footwear=footwear.replace('        LegendsPaintFrontFaceShade(sWorldPixels + offset, width, gender, state, i);','')
        footwear=footwear.replace('if (LegendsGetCostume() || state == 4)', 'if (LegendsGetCostume() || state == 4 || (!shoes && !hair && !hairColor && !coat && !leggings))',1)
    c.write_text(pre+fixture['header']+h+source('src/legends_style_layers.c')+fixture['assets']+fixture['palettes']+(root/'src/data/legends/costume_palettes.h').read_text()+outfits+accessories+fronts+footwear+palette_source+wrappers)
    subprocess.run(['cc','-std=gnu17','-Werror=implicit-function-declaration','-shared','-fPIC','-O1',str(c),'-o',str(so)],check=True)
    api=ctypes.CDLL(str(so));api.Render.argtypes=[ctypes.c_uint8]*11+[ctypes.POINTER(ctypes.c_uint8),ctypes.POINTER(ctypes.c_uint16)]
    def render(h=6,col=0,tone=0,o=0,coat=0,scarf=0,shoe=0,state=0,pose=0,g=0,kind=1):
        buf=(ctypes.c_uint8*2048)();pal=(ctypes.c_uint16*16)()
        w=api.Render(h,col,tone,o,coat,scarf,shoe,state,pose,g,kind,buf,pal);height=64 if kind else 32
        raw=bytes(buf[:w*height//2]);px=[[raw[(y//8*(w//8)+x//8)*32+y%8*4+x%8//2]>>(x%2*4)&15 for x in range(w)] for y in range(height)]
        im=Image.new('RGBA',(w,height))
        for y,row in enumerate(px):
            for x,v in enumerate(row):
                if v:im.putpixel((x,y),(*rgb(pal[v]),255))
        return im,px,list(pal)
    return api,render

# Artwork preservation: only the separately approved male Side Part world
# layer may differ. Existing coats, other cuts, portraits and battle art stay frozen.
header=(root/'src/data/legends/style_layers.h').read_text();blob=(root/'graphics/legends/styles/edits.bin').read_bytes()
for name,expected in BASE['unchanged_layers'].items():
    block=re.search(r'const struct StyleEdits '+name+r'[^=]*=\s*(.*?);',header,re.S)[1];pieces=[]
    for i,(off,n) in enumerate(re.findall(r'\{(\d+),(\d+)\}',block)):
        if name.startswith('sStyle0') and name!='sStyle04' and i%16 in (1,13,14,15):continue
        if name=='sStyleFront' and i<16 and i%16 in (13,14,15):continue
        pieces.append(struct.pack('<I',int(n))+blob[int(off)*2:(int(off)+int(n))*2])
    assert hashlib.sha256(b''.join(pieces)).hexdigest()==expected,('v0.0.46 artwork changed',name)
for path,sha in BASE['unchanged_files'].items():assert hashlib.sha256((root/path).read_bytes()).hexdigest()==sha,path

with tempfile.TemporaryDirectory() as temp:
    api,render=compile_api(temp)
    from build_appearance import ball_pixels
    def body_signature(im,kind):
        props=ball_pixels(0,'front',0) if kind else set()
        return bytes(v for y in range(24,im.height) for x in range(im.width) if (x,y) not in props for v in im.getpixel((x,y)))
    for kind in (0,1):
        for h in range(1,11):
            base,px,pal=render(h=h,kind=kind)
            body=body_signature(base,kind)
            for col in range(1,8):
                im,px,pal=render(h=h,col=col,kind=kind)
                assert body_signature(im,kind)==body,(kind,h,col,'hair paints body')
                assert px[22][30 if kind else 5]==3,(kind,h,col,'smile/chin uses hair')
    for h in range(1,11):
        for col in range(8):
            for tone in range(5):
                _,px,pal=render(h=h,col=col,tone=tone)
                assert px[22][30]==3 and rgb(pal[3])!=rgb(pal[4]),'smile color is not isolated'
    for kind in (0,1):
        for o in range(5):
            for coat in range(3):
                for scarf in range(6):
                    for shoe in range(8):
                        im,px,pal=render(kind=kind,o=o,coat=coat,scarf=scarf,shoe=shoe)
                        for col in (1,6,7):
                            alt,_,_=render(kind=kind,col=col,o=o,coat=coat,scarf=scarf,shoe=shoe)
                            assert body_signature(im,kind)==body_signature(alt,kind),(kind,o,coat,scarf,shoe,'wardrobe body tint')
    print('Preserved approved artwork outside the new Side Part; 400 smile/color/skin cases and 1,440 front/field wardrobe combinations isolate body RGB')
    if '--preview' in sys.argv:
        _,before=compile_api(temp,True)
        cases=[('Portrait smile / blond',dict(col=6),True),('Field chin / blond',dict(col=6,kind=0),True),('Field chin / silver',dict(col=7,tone=3,kind=0),True)]
        cases +=[(label+' outfit',dict(o=o,col=6),False) for o,label in enumerate(('Emerald','Trail','Sport','Yellow','Lavender'))]
        cases +=[('Natural / red shoes',dict(shoe=1),False),('Navy coat / blond',dict(col=6,coat=1),False),('Winter / scarf / boots',dict(col=7,coat=2,scarf=2,shoe=7),False),('Field / yellow / blond',dict(col=6,o=3,kind=0),False)]
        sheet=Image.new('RGB',(1200,1270),(238,240,245));d=ImageDraw.Draw(sheet)
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17);bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',21)
        d.text((25,20),'v0.0.46 ARTWORK  /  SMILE AND BODY COLORS ONLY',font=bold,fill=(28,38,55))
        d.text((25,52),'Before / after from the actual C compositor • Existing sprite shapes and hair are retained',font=font,fill=(66,76,98))
        for i,(label,args,closeup) in enumerate(cases):
            row,col=divmod(i,3);x=16+col*400;y=90+row*288
            d.rounded_rectangle((x,y,x+382,y+272),radius=10,fill='white',outline=(207,214,225))
            d.text((x+12,y+10),label,font=bold,fill=(28,38,55))
            for j,r in enumerate((before,render)):
                im=r(**args)[0]
                if closeup:
                    im=im.crop((19,15,39,25) if im.width==64 else (0,16,16,24));scale=8
                else:scale=3 if im.width==64 else 6
                im=im.resize((im.width*scale,im.height*scale),Image.Resampling.NEAREST)
                xx=x+8+j*190+(174-im.width)//2;yy=y+45+(180-im.height)//2
                sheet.paste(im,(xx,yy),im);d.text((x+55+j*190,y+243),'Before' if j==0 else 'After',font=font,fill=(66,76,98))
        d.text((25,1245),'Review repair only • Published v0.0.46 is unchanged',font=font,fill=(66,76,98))
        sheet.save(root/'docs/qa/appearance-color-fix-preview.png')
        print('Wrote one compact before/after preview with the original v0.0.46 artwork')
