"""Register generated male hair to native 16x32 eye/ear grids; retain native anatomy.

The atlas contains hair/cap materials only. No generated body or face is used.
West is sampled from the actual west-facing source; east uses native mirroring.
"""
import hashlib,json
import numpy as np
from PIL import Image
from build_appearance import ROOT
from import_male_overworld_sheets import COLORS
from build_male_front import components,NAMES

SOURCE=ROOT/'graphics/legends/male_overworld/generated-reference-draft.png'
TOPS=(50,330,612,898,1178)
# Calibrated pupil centers/top rows in this immutable generated reference.
# Some fringes touch the left pupil; connected-component size alone mistakes
# those forelocks or a temple for an eye and moves the whole head upward.
EYE_ANCHORS=((87,142,410,141),(589.25,140,955,140),
             (86.5,413,411,414),(592,413,961,412),
             (86,692,411,692),(589.5,693,917,692),
             (86.5,973,411,973),(588,974,913,975),
             (84.5,1263,409.5,1264),(589.75,1266,916,1265))

def skin(a):
    r,g,b=a[:,:,0],a[:,:,1],a[:,:,2]
    return (r>215)&(g>160)&(r-g>18)&(g-b>12)

def classify(c,cap=False):
    r,g,b=map(float,c)
    if cap:
        if min(r,g,b)>228 and max(r,g,b)-min(r,g,b)<16:return 14
        if r>180 and g>190 and b>210 and g>r+3:return 14
        if g>r*1.08 and g>b*1.12 and g>65:return 10 if g>150 else 11
        if b>r+5 and max(r,g,b)<170:return 5
    if b>r+12 and b>g+10 and b>135:return 0
    if r>185 and g>130 and r-g>18 and g-b>8:return 0
    if max(r,g,b)<62:return 15
    if r>g+8 and g>b+3:
        brightness=.299*r+.587*g+.114*b
        return 7 if brightness>120 else 4 if brightness>72 else 8
    return 0

def build():
    im=np.asarray(Image.open(SOURCE).convert('RGB')).astype(float)
    assert im.shape[:2]==(1536,1024)
    atlas=Image.new('P',(48,320));atlas.putpalette([v for c in COLORS for v in c]+[0]*(768-48))
    records=[]
    for i,name in enumerate(NAMES):
        row,col=divmod(i,2);top=TOPS[row];shift=col*504
        front_cx,front_eye,west_x,west_eye=EYE_ANCHORS[i]
        pitch=7 # Two native pupil pixels correspond to fourteen source pixels.
        # Back ears are bright skin islands at either edge of the hair. Their
        # upper row, not the bun's top or backpack, determines registration.
        back=im[top+20:top+142,shift+151:shift+253]
        by,bx=np.nonzero(skin(back));valid=(bx<25)|(bx>76)
        rear_y=top+20+float(np.percentile(by[valid],5)) if valid.any() else front_eye
        rear_x=shift+202
        # In profile, one pupil sits in native column five. Source direction
        # is determined by its right-side green backpack, not the text label.
        anchors=((front_cx-7.5*pitch,front_eye,19),(rear_x-7.5*pitch,rear_y,18),(west_x-5*pitch,west_eye,19))
        for view,(zero,anchor_y,target_y) in enumerate(anchors):
            for y in range(8,23):
                for x in range(16):
                    px=round(zero+x*pitch);py=round(anchor_y+(y-target_y+.5)*pitch)
                    if not (2<=px<im.shape[1]-2 and 2<=py<im.shape[0]-2):continue
                    patch=im[max(0,py-2):py+3,max(0,px-2):px+3];rgb=np.median(patch,axis=(0,1))
                    value=classify(rgb,i==7)
                    if y>target_y and view!=1 and 3<=x<=12:value=0 # Native cheeks/chin are authoritative.
                    atlas.putpixel((view*16+x,i*32+y),value)
            # Fill small gaps inside the crown, without extending its silhouette.
            for y in range(10,target_y):
                for x in range(2,14):
                    q=(view*16+x,i*32+y)
                    around=[atlas.getpixel((q[0]+dx,q[1]+dy)) for dx,dy in ((-1,0),(1,0),(0,-1),(0,1))]
                    if not atlas.getpixel(q) and sum(v in (4,7,8,15) for v in around)>=3:atlas.putpixel(q,8)
            # Drop detached label/neck/outline samples. Hair, bun and cap must
            # form one connected crown before the native face is composited.
            points={(x,y) for y in range(8,23) for x in range(16) if atlas.getpixel((view*16+x,i*32+y))}
            parts=components(points)
            if parts:
                main=max(parts,key=len)
                # A pixel-art outline can connect diagonally. Retain crown
                # islands touching that outline, while removing neck artifacts.
                while True:
                    touching={p for p in points-main if any((p[0]+dx,p[1]+dy) in main for dx in (-1,0,1) for dy in (-1,0,1))}
                    if not touching:break
                    main|=touching
                for x,y in points-main:atlas.putpixel((view*16+x,i*32+y),0)
        records.append({'id':i+1,'name':name,'source_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),'grid_step':[pitch,pitch],'anchors':anchors,'source_views':[0,1,3],'east':'native west mirroring','status':'draft awaiting tuning'})
    atlas.save(ROOT/'graphics/legends/male_overworld/heads.png',transparency=0)
    (ROOT/'tools/legends/male_overworld_sheets.json').write_text(json.dumps(records,indent=2,default=float)+'\n')
    print('Generated reference import: ten hair-only native head grids; faces, bodies and native east mirroring retained')

if __name__=='__main__':build()
