"""Render real field C buffers with the actual outfit/accessory banks and palettes.

The optional previews are native-resolution runtime art, not emulator captures.
"""
import ctypes, hashlib, json, re, struct, subprocess, sys, tempfile, zipfile
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

root = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools/legends'))
import import_generated_world as art
atlas_assets=[root/'graphics/legends/male_overworld/heads.png',root/'tools/legends/male_overworld_sheets.json']
before=[p.read_bytes() for p in atlas_assets];art.build();assert before==[p.read_bytes() for p in atlas_assets],'head import is not reproducible'
preserved=json.loads((root/'docs/qa/appearance-preservation.json').read_text())['tables_sha256']
header=(root/'src/data/legends/style_layers.h').read_text();blob=(root/'graphics/legends/styles/edits.bin').read_bytes()
for name,expected in preserved.items():
    block=re.search(r'const struct StyleEdits '+name+r'[^=]*=\s*(.*?);',header,re.S)[1]
    data=b''.join(struct.pack('<I',int(n))+blob[int(o)*2:(int(o)+int(n))*2] for o,n in re.findall(r'\{(\d+),(\d+)\}',block))
    assert hashlib.sha256(data).hexdigest()==expected,('approved artwork changed',name)
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
wrappers = r'''
int Render(u8 h,u8 col,u8 tone,u8 o,u8 c,u8 s,u8 shoe,u8 state,u8 pose,u8 gender,u8 *pixels,u16 *palette){
 hair=h;color=col;skin=tone;outfit=o;coat=c;selectedScarf=s;shoes=shoe;
 LegendsUpdateAppearancePalettes();
 const struct SpriteFrameImage *src=nativeWorld[gender][state];
 if(LegendsGetAccessoryStyle()&&state!=4)src=sLegendsAccessoryImages[LegendsGetAccessoryStyle()-1][gender][o][state];
 else if(o)src=sLegendsOutfitImages[gender][o-1][state];
 const struct SpriteFrameImage *result=LegendsFootwearImages(src,gender,state);
 assert(pose<sFootwearFrameCount[gender][state]);
 memcpy(pixels,result[pose].data,result[pose].size);
 memcpy(palette,state==4?gLegendsUnderwaterPalettes[gender]:gLegendsOverworldPalettes[gender],32);
 // Repeated consumers must receive the same cached frame and bytes.
 assert(result==LegendsFootwearImages(src,gender,state));
 return result[pose].size;
}
int Count(u8 gender,u8 state){return sFootwearFrameCount[gender][state];}
'''

def rgb(c):return ((c&31)*255//31, (c>>5&31)*255//31, (c>>10&31)*255//31)

with tempfile.TemporaryDirectory() as temp:
    c = Path(temp)/'world.c'; so = c.with_suffix('.so')
    c.write_text(pre+fixture['header']+fixture['style_header']+fixture['style_source']+fixture['assets']+fixture['palettes']+(root/'src/data/legends/costume_palettes.h').read_text()+outfits+accessories+fixture['source']+palette_source+wrappers)
    subprocess.run(['cc','-std=gnu17','-Werror=implicit-function-declaration','-shared','-fPIC','-O1',str(c),'-o',str(so)],check=True)
    api = ctypes.CDLL(str(so)); api.Render.argtypes = [ctypes.c_uint8]*10+[ctypes.POINTER(ctypes.c_uint8),ctypes.POINTER(ctypes.c_uint16)]
    def render(h=1,col=0,tone=0,o=0,coat=0,scarf=0,shoe=0,state=0,pose=0,g=0):
        pixels=(ctypes.c_uint8*512)(); palette=(ctypes.c_uint16*16)()
        size=api.Render(h,col,tone,o,coat,scarf,shoe,state,pose,g,pixels,palette)
        w=16 if state==0 else 32
        assert size==w*16
        raw=bytes(pixels[:size]); pal=list(palette)
        px=[[raw[(y//8*(w//8)+x//8)*32+y%8*4+x%8//2]>>(x%2*4)&15 for x in range(w)] for y in range(32)]
        im=Image.new('RGBA',(w,32))
        for y,row in enumerate(px):
            for x,v in enumerate(row):
                if v:im.putpixel((x,y),(*rgb(pal[v]),255))
        return im,px,pal

    if '--preview-only' not in sys.argv:
        from build_style_layers import head
        body_tops={}
        for state,file in enumerate(fixture['FILES']):
            w=16 if state==0 else 32
            path=root/f'graphics/object_events/pics/people/brendan/{file}.png'
            native=fixture['frames'](path,w,32)
            if state==0:native+=fixture['frames'](path.with_name('running.png'),16,32)
            table=fixture['mapping']['Brendan'][fixture['STATES'][state]]['table']
            indexes=list(range(len(native))) if 'overworld_ascending_frames' in table else list(map(int,re.findall(r'overworld_frame\([^,]+,\s*\d+,\s*\d+,\s*(\d+)\)',table)))
            for pose,index in enumerate(indexes):
                face=head(native[index],0,'overworld',index,file)[0]
                body_tops[state,pose]=max(24,max((y for x,y in face),default=22)+2)
        poses=0
        for state in range(8):
            for pose in range(api.Count(0,state)):
                for h in range(1,11):
                    baseline,px,pal=render(h,state=state,pose=pose)
                    # Hair changes must never recolor the clothes below the head.
                    body_top=body_tops[state,pose]
                    body=baseline.crop((0,body_top,baseline.width,32)).tobytes()
                    for col in range(1,8):
                        alt,ap,pp=render(h,col=col,state=state,pose=pose)
                        assert alt.crop((0,body_top,alt.width,32)).tobytes()==body,(state,pose,h,col,'hair tints outfit/hand')
                        if state!=4:assert [pp[i] for i in (5,8)]==[pal[i] for i in (5,8)],'native pupil/body blues changed'
                    poses+=1
        for h in (1,8,10):
            for o in range(5):
                for coat in range(3):
                    for scarf in range(6):
                        for shoe in range(8):
                            im,px,pal=render(h,o=o,coat=coat,scarf=scarf,shoe=shoe)
                            alt,ap,pp=render(h,col=6,o=o,coat=coat,scarf=scarf,shoe=shoe)
                            assert im.crop((0,24,16,32)).tobytes()==alt.crop((0,24,16,32)).tobytes(),(h,o,coat,scarf,shoe,'wardrobe tints body')
                            # Native front pupils stay two pixels tall in fixed columns.
                            assert px[19][6]==px[20][6]==px[19][9]==px[20][9]==8,(h,o,coat,scarf,shoe,'pupil moved')
        for h in range(1,11):
            for col in range(8):
                for tone in range(5):
                    im,px,pal=render(h,col=col,tone=tone)
                    assert all(px[y][x] in (1,2,3,5,8,15) for y in (20,21,22) for x in range(4,12)),(h,col,tone,'hair in lower face')
        assert len({render(h)[0].tobytes() for h in range(1,11)})==10
        assert render(10,col=6,state=4)[0].tobytes()==render(0,state=4)[0].tobytes(),'diving changed'
        print(f'{poses} male native pose/style combinations, all hair colors, 2160 wardrobe combinations, pupil/face protection and diving passed')

    if '--preview' in sys.argv or '--preview-only' in sys.argv:
        dest=root/'docs/qa'; dest.mkdir(exist_ok=True)
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
        bold=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',22)
        names=('Crew Cut','Side Part','Spiky','Side Sweep','Tousled','Quiff','Shag','Curls','Man Bun','Undercut')
        sheet=Image.new('RGB',(1000,1140),(242,243,247)); d=ImageDraw.Draw(sheet)
        d.text((30,20),'EMERALD: LEGENDS  /  OVERWORLD DRAFT',font=bold,fill=(23,38,58))
        d.text((30,53),'Native 16×32 frames • compiled game compositor • 6× pixel zoom',font=font,fill=(71,88,108))
        for i,name in enumerate(names):
            row,col=divmod(i,2); x=24+col*500; y=90+row*204
            d.rounded_rectangle((x,y,x+452,y+190),radius=10,fill='white',outline=(211,218,226))
            d.text((x+14,y+10),f'{i+1:02d}  {name}',font=bold,fill=(23,38,58))
            for j,(pose,label) in enumerate(((0,'Front'),(1,'Back'),(2,'West'),(2,'East'))):
                im=render(i+1)[0] if pose==0 else render(i+1,pose=pose)[0]
                if j==3:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                im=im.crop((0,8,16,32)).resize((96,144),Image.Resampling.NEAREST)
                sheet.paste(im,(x+14+j*110,y+30),im)
                d.text((x+20+j*110,y+167),label,font=font,fill=(71,88,108))
        d.text((30,1110),'Review artwork only • published v0.0.46 is unchanged',font=font,fill=(71,88,108))
        sheet.save(dest/'male-overworld-repair-preview.png')
        # Parse frame IDs, mirroring and timing from the actual native animation tables.
        anims=(root/'src/data/object_events/object_event_anims.h').read_text()
        cycles=[]
        for direction in ('South','North','West','East'):
            body=re.search(r'sAnim_Go'+direction+r'\[\]\s*=\s*\{(.*?)\};',anims,re.S)[1]
            cycles.append([(int(f),int(t), 'TRUE' in flags) for f,t,flags in re.findall(r'ANIMCMD_FRAME\((\d+),\s*(\d+)([^)]*)\)',body)])
        frames=[]
        for step in range(4):
            canvas=Image.new('RGB',(1000,770),(242,243,247)); draw=ImageDraw.Draw(canvas)
            draw.text((30,20),'NATIVE WALK CYCLE  /  OUTFIT CHECK',font=bold,fill=(23,38,58))
            draw.text((30,53),'All ten cuts • four directions • original frame timing and east mirroring',font=font,fill=(71,88,108))
            for i,name in enumerate(names):
                row,col=divmod(i,5); x=24+col*196; y=100+row*270
                draw.text((x,y),name,font=font,fill=(23,38,58))
                for view in range(4):
                    pose,timing,mirror=cycles[view][step]
                    im=render(i+1,pose=pose)[0]
                    if mirror:im=im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
                    im=im.crop((0,8,16,32)).resize((48,72),Image.Resampling.NEAREST)
                    canvas.paste(im,(x+(view%2)*88,y+35+(view//2)*98),im)
            draw.line((24,650,976,650),fill=(211,218,226))
            for i,label in enumerate(('Emerald','Trail','Sport','Yellow','Lavender')):
                draw.text((38+i*196,666),label,font=font,fill=(23,38,58))
                pose=cycles[0][step][0]; im=render(6,col=5,o=i,pose=pose)[0].crop((0,8,16,32)).resize((48,72),Image.Resampling.NEAREST)
                canvas.paste(im,(108+i*196,690),im)
            frames.append(canvas)
        frames[0].save(dest/'male-overworld-walk-preview.gif',save_all=True,append_images=frames[1:],duration=round(1000*cycles[0][0][1]/60),loop=0,disposal=2)
        # Give the owner exact native sheets as well as the enlarged review.
        with zipfile.ZipFile(dest/'male-overworld-native-draft.zip','w',zipfile.ZIP_DEFLATED) as archive:
            for h,name in enumerate(names,1):
                for state,label in enumerate(fixture['STATES']):
                    count=api.Count(0,state);w=16 if state==0 else 32
                    im,px,pal=render(h,state=state)
                    native=Image.new('P',(count*w,32));native.putpalette([v for c in pal for v in rgb(c)]+[0]*(768-48))
                    for pose in range(count):
                        _,px,_=render(h,state=state,pose=pose)
                        for y,row in enumerate(px):
                            for x,v in enumerate(row):native.putpixel((pose*w+x,y),v)
                    path=Path(temp)/'native.png';native.save(path,transparency=0)
                    archive.writestr(f'{h:02d}-{name.lower().replace(" ","_")}/{label}.png',path.read_bytes())
            archive.writestr('README.txt','Pokémon Emerald: Legends — male overworld review draft\n\n80 indexed PNG sheets, actual compiled field output at native resolution.\nNatural hair, first skin tone, Emerald outfit, no accessories.\nWalking sheets contain 18 native walking/running frames in runtime order.\nOther sheets use the native image-table order; east is mirrored by native animations.\nThese PNGs are review/export assets. ROM integration uses heads.png, the\npose-local edits.bin/style_layers.h bank and the existing C compositor.\nArtwork requires owner approval; published VERSION remains 0.0.46.\n')
        print('Wrote two compact previews from real C field buffers')
