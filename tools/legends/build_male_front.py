"""Author the shared male 64x64 portraits from native anatomy and a generated reference.

The reference supplies hair only. Native faces, hands, props and lower-body
geometry supply the character; saved IDs and all other sprite banks stay intact.
Pixels use material IDs until the runtime packs one independent 16-color palette.
"""
from pathlib import Path
import json, hashlib
import numpy as np
from PIL import Image, ImageDraw
from build_appearance import ROOT, frames
from build_footwear import front_mask

DIRECTORY = ROOT / 'graphics/legends/male_front'
NATIVE = frames(ROOT/'graphics/trainers/front_pics/brendan.png',64,64)[0]
NAMES = ('Crew Cut','Side Part','Spiky','Side Sweep','Tousled','Quiff','Shag','Curls','Man Bun','Undercut')
# 0..15 are native materials; additional IDs are independent wardrobe materials.
HAIR, HAIR_LIGHT, HAIR_DARK = 16,17,18
COAT, COAT_DARK, SCARF, SHOE, SHOE_DARK = 19,20,21,22,23
SHIRT, SHIRT_DARK, SCARF_DARK, CREAM, EYE_BLUE = 24,25,26,27,28

def components(points):
    result=[]; remaining=set(points)
    while remaining:
        q=remaining.pop(); part={q}; queue=[q]
        for x,y in queue:
            for n in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if n in remaining:remaining.remove(n);part.add(n);queue.append(n)
        result.append(part)
    return result

def semantic_native():
    out=[row[:] for row in NATIVE]
    for y,row in enumerate(out):
        for x,v in enumerate(row):
            if v==4:row[x]=3 if any(0<=xx<64 and 0<=yy<64 and NATIVE[yy][xx] in (1,2,3) for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))) else 15
            if 23<=x<=36 and 16<=y<=23 and v==5:row[x]=EYE_BLUE
    return out

def generated_heads():
    im=np.asarray(Image.open(DIRECTORY/'generated-reference.png').convert('RGB'))
    heads=[];records=[]
    for i,name in enumerate(NAMES):
        row,col=divmod(i,5);left=round(col*im.shape[1]/5);right=round((col+1)*im.shape[1]/5)
        cell=im[row*512:row*512+190,left:right].astype(int)
        r,g,b=cell[:,:,0],cell[:,:,1],cell[:,:,2]
        skin=(r>175)&(g>115)&(g<220)&(r-g>25)&(g-b>10)&(r-b<115)
        sy,sx=np.nonzero(skin)
        fl,fr=np.percentile(sx,(15,85));ft,fb=np.percentile(sy,(15,85))
        yy,xx=np.indices(skin.shape)
        white=(cell.min(2)>215)&((cell.max(2)-cell.min(2))<25)&(xx>fl-24)&(xx<fr+24)&(yy>ft)&(yy<fb-5)
        pieces=components(zip(*np.nonzero(white)[::-1]))
        pieces=sorted((p for p in pieces if len(p)>8 and max(y for x,y in p)-min(y for x,y in p)>4),key=len,reverse=True)[:2]
        eyes=sorted((np.mean([x for x,y in p]),np.mean([y for x,y in p])) for p in pieces)
        if len(eyes)==2 and eyes[1][0]-eyes[0][0]>24:
            scale=max(6.5,min(9,(eyes[1][0]-eyes[0][0])/6));cx=(eyes[0][0]+eyes[1][0])/2;cy=(eyes[0][1]+eyes[1][1])/2
        else:scale=8;cx=(fl+fr)/2;cy=ft+(fb-ft)*.5
        # Register to the native eye midpoint. Only the hair region is sampled.
        out=semantic_native()[:24]
        for y in range(8,18):
            for x in range(19,39):
                if NATIVE[y][x] not in (1,2,3):out[y][x]=0
        mask={}
        for y in range(3,21):
            for x in range(17,41):
                px=round(cx+(x-29)*scale);py=round(cy+(y-18.5)*scale)
                if not (0<=px<cell.shape[1] and 0<=py<cell.shape[0]):continue
                rad=max(1,round(scale*.28));patch=cell[max(0,py-rad):py+rad+1,max(0,px-rad):px+rad+1]
                rr,gg,bb=np.median(patch.reshape(-1,3),axis=0)
                v=0
                if rr>gg+10 and gg>bb+3 and 45<rr<205:
                    # Reject skin from the source: native anatomy supplies it.
                    if not (rr>175 and gg>115 and rr-gg>25 and gg-bb>10):
                        v=HAIR_LIGHT if rr>141 else HAIR if rr>95 else HAIR_DARK
                elif max(rr,gg,bb)<90:v=15
                if i==7:
                    # The reference background is lavender, never cap white.
                    if min(rr,gg,bb)>235 and max(rr,gg,bb)-min(rr,gg,bb)<13:v=14
                    elif gg>rr*1.08 and gg>bb*1.15 and gg>65:v=10 if gg>150 else 11
                    elif bb>rr and max(rr,gg,bb)<170:v=8
                if v:mask[x,y]=v
        # Native eyes, ears, mouth and lower face remain the authoritative art.
        protected={(x,y) for y in range(16,24) for x in range(19,40) if (y>=18 and NATIVE[y][x]) or (NATIVE[y][x] in (1,2,3) and (x<=23 or x>=35))}
        for (x,y),v in mask.items():
            if (x,y) not in protected:out[y][x]=v
        # The retired brim can leave gaps above the pupils. Fill only skull
        # interior, never the outer silhouette, arms or clothing.
        for y in range(13,18):
            for x in range(24,35):
                if not out[y][x]:out[y][x]=HAIR_DARK if y<16 else 2
        if i==7:
            # Keep the authoritative native white/green cap as a single panel.
            # Sampling the generated white/gray cap edges introduced holes;
            # only its exposed ringlets come from the generated hair reference.
            native_head=semantic_native()
            for y in range(16):
                for x in range(17,41):out[y][x]=native_head[y][x]
        heads.append(out);records.append({'name':name,'source_eye_midpoint':[round(cx,3),round(cy,3)],'source_pixels_per_native_pixel':round(scale,3)})
    return heads,records

def body(outfit,coat,scarf):
    p=semantic_native()
    if outfit:
        for y in range(26,40):
            for x in range(22,40):
                if NATIVE[y][x] in (5,6,7,8,12,13):p[y][x]=SHIRT if NATIVE[y][x] in (5,6,12) else SHIRT_DARK
        # Native green diagonal strap/backpack is a separate material, never
        # a shirt color. Ball/cuff outlines and native hand geometry remain.
        for l,t,r,b in ((14,36,20,43),(41,29,49,35)):
            for y in range(t,b+1):
                for x in range(l,r+1):
                    if 45<=x<=50 and 26<=y<=30:continue
                    v=NATIVE[y][x]
                    if v in (5,6,7,8,9,12,13,14):p[y][x]=1 if v in (5,9,14) else 2 if v in (6,12) else 3
        if outfit==1:
            for y in range(30,37):
                for x in range(18,43):
                    if NATIVE[y][x] in (1,2,3) and (x<25 or x>36):p[y][x]=SHIRT if NATIVE[y][x]==1 else SHIRT_DARK
        if outfit==2:
            for y in (31,32):
                for x in range(23,39):
                    if p[y][x] in (SHIRT,SHIRT_DARK):p[y][x]=14
            for y in range(42,47):
                for x in range(16,43):
                    if NATIVE[y][x] in (5,6,7,8):p[y][x]=14 if y in (44,46) else NATIVE[y][x]
            for y in range(48,55):
                for x in range(16,43):
                    if NATIVE[y][x] in (5,6,7,8):p[y][x]=2 if NATIVE[y][x] in (5,6) else 3
        if outfit==4:
            for y in range(26,34):
                for x in range(26,33):
                    if p[y][x] in (SHIRT,SHIRT_DARK) and (y<28 or x in (30,31)):p[y][x]=CREAM
    if coat:
        shape=Image.new('L',(64,64));draw=ImageDraw.Draw(shape)
        draw.polygon(((23,26),(20,29),(18,33),(20,35),(24,32),(24,38),(23,44 if coat==2 else 38),(38,44 if coat==2 else 38),(37,34),(40,31),(37,26)),fill=COAT,outline=15)
        for y in range(26,45 if coat==2 else 39):
            for x in range(18,42):
                v=shape.getpixel((x,y))
                if not v or NATIVE[y][x] in (10,11) or (NATIVE[y][x] in (1,2,3) and y>=37):continue
                p[y][x]=v if v==15 else COAT_DARK if x>32 or x==30 else COAT
        for y in range(30,37):
            for x in range(18,43):
                if NATIVE[y][x] in (1,2,3) and (x<25 or x>36):p[y][x]=COAT if NATIVE[y][x]==1 else COAT_DARK
        if coat==2:
            for y in range(26,30):
                for x in range(24,37):
                    if p[y][x] in (COAT,COAT_DARK) and (x<28 or x>32):p[y][x]=CREAM
    if scarf:
        for y in range(26,35):
            for x in range(25,34):
                if p[y][x] and (y<=27 or x in (30,31)):p[y][x]=SCARF_DARK if x==31 and y>=28 else SCARF
    return p

def build():
    DIRECTORY.mkdir(parents=True,exist_ok=True)
    heads,records=generated_heads()
    atlas=Image.new('P',(640,24));pal=Image.open(ROOT/'graphics/trainers/front_pics/brendan.png').getpalette();pal[48:87]=[139,90,57,189,132,82,65,41,32,33,57,106,24,41,65,180,66,66,90,60,36,49,33,24,100,130,210,66,82,148,107,74,74,239,222,181,98,123,156]
    atlas.putpalette(pal)
    for i,h in enumerate(heads):
        for y,row in enumerate(h):
            for x,v in enumerate(row):atlas.putpixel((i*64+x,y),v)
    atlas.save(DIRECTORY/'heads.png',transparency=0)
    (DIRECTORY/'heads.bin').write_bytes(bytes(v for h in heads for row in h for v in row))
    (DIRECTORY/'bodies.bin').write_bytes(bytes(v for o in range(5) for c in range(3) for s in range(2) for row in body(o,c,s) for v in row))
    (DIRECTORY/'shoes.bin').write_bytes(bytes(v for b in range(2) for row in front_mask(0,b) for v in row))
    record={'reference_sha256':hashlib.sha256((DIRECTORY/'generated-reference.png').read_bytes()).hexdigest(),'native_size':[64,64],'hair_only_import':True,'styles':records}
    (DIRECTORY/'manifest.json').write_text(json.dumps(record,indent=2)+'\n')
    header='// Generated by tools/legends/build_male_front.py. Material IDs are not palette indices.\n'
    for name in ('heads','bodies','shoes'):header+=f'static const u8 sMaleFront{name.title()}[] = INCBIN_U8("graphics/legends/male_front/{name}.bin");\n'
    (ROOT/'src/data/legends/male_front.h').write_text(header)
    print('Male front: ten generated hair references, thirty native outfit/coat/scarf bodies, native shoe/boot masks')

if __name__=='__main__':build()
