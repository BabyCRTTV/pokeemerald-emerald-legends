"""Authoring contact sheets; these are explicitly not emulator captures."""
from PIL import Image, ImageDraw
from build_style_layers import ROOT, frames, coat_edits, hair_edits, original_hair
BG=(225,218,233)

def render(path,g,kind,pose,hair,coat,state='',color=0):
    w=64 if kind!='overworld' else 16 if state=='walking' else 32
    h=64 if kind!='overworld' else 32
    im=Image.open(path);native=frames(path,w,h)[pose]
    garment=coat_edits(native,g,kind,pose,coat) if coat else native
    hairart,points=hair_edits(native,g,kind,pose,hair,state,True) if hair else (native,original_hair(native,g,kind,pose,state))
    out=[[5 if g==0 and hair and v==7 else v for v in row] for row in garment]
    if hair:
        for y in range(h):
            for x in range(w):
                if hairart[y][x]!=native[y][x] or (x,y) in points:out[y][x]=hairart[y][x]
    pal=im.getpalette()[:]
    if g==0 and hair:pal[21:24]=[181,106 if kind=='overworld' else 123,66 if kind=='overworld' else 82]
    if coat:pal[30:33]=[33,90,57] if coat==2 else [33,57,106]
    a=Image.new('P',(w,h));a.putpalette(pal);a.putdata([v for row in out for v in row]);rgb=a.convert('RGB')
    for y in range(h):
        for x in range(w):
            if out[y][x]==0:rgb.putpixel((x,y),BG)
    return rgb

canvas=Image.new('RGB',(11*180,4*210),BG);d=ImageDraw.Draw(canvas)
for g,n in enumerate(('brendan','may')):
    for row,kind in enumerate(('front','overworld')):
        path=ROOT/(f'graphics/trainers/front_pics/{n}.png' if kind=='front' else f'graphics/object_events/pics/people/{n}/walking.png')
        for hair in range(11):
            rgb=render(path,g,kind,0,hair,2 if hair else 0,'walking')
            scale=2 if kind=='front' else 4
            xx=hair*180+20;yy=(g*2+row)*210+35
            canvas.paste(rgb.resize((rgb.width*scale,rgb.height*scale),Image.Resampling.NEAREST),(xx,yy))
            d.text((xx,yy-20),f'{n} {hair}',fill='black')
canvas.save(ROOT/'docs/qa/wardrobe-v0.0.40.png')

canvas=Image.new('RGB',(1320,900),BG);d=ImageDraw.Draw(canvas)
for g,n in enumerate(('brendan','may')):
    cases=[]
    for kind,file in [('back','back'),('overworld','walking'),('overworld','mach_bike'),('overworld','fishing'),('overworld','field_move')]:
        path=ROOT/(f'graphics/trainers/back_pics/{n}.png' if kind=='back' else f'graphics/object_events/pics/people/{n}/{file}.png')
        for i in range(4 if kind=='back' else 3):cases.append((kind,file,path,i))
    for k,(kind,file,path,i) in enumerate(cases):
        rgb=render(path,g,kind,i,7,2,file)
        xx=(k%8)*165+10;yy=g*440+(k//8)*220+30
        canvas.paste(rgb.resize((rgb.width*3,rgb.height*3),Image.Resampling.NEAREST),(xx,yy))
        d.text((xx,yy-20),f'{n} {file} {i}',fill='black')
canvas.save(ROOT/'docs/qa/wardrobe-actions-v0.0.40.png')
