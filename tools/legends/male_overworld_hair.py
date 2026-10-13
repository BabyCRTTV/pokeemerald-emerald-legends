"""Place the imported head atlas on each native male overworld pose.

All placement is performed at authoring time; the ROM keeps the established
sparse compositor and original pose tables, including native east mirroring.
"""
from functools import lru_cache
from PIL import Image
from build_appearance import ROOT

@lru_cache(maxsize=1)
def atlas():
    image=Image.open(ROOT/'graphics/legends/male_overworld/heads.png')
    assert image.mode=='P' and image.size==(48,320)
    return image

def imported_hair(native,style,face,box,direction,state,pose):
    assert 1<=style<=10 and direction in (0,1,2)
    h,w=len(native),len(native[0]);out=[row[:] for row in native]
    if not face:
        return out,set()
    left,right=min(x for x,y in face),max(x for x,y in face)
    ear_y=min(y for x,y in face)
    # Reference front eye row 19 and rear ears 18 share one calibrated atlas.
    dx=(left+right-15)//2 if direction!=1 else left-3
    dy=ear_y-18
    view={0:0,2:1,1:2}[direction]
    eyes=[]
    if direction!=2:
        for y in range(ear_y,min(h,ear_y+4)):
            for x in range(left,right+1):
                neighbors=sum(0<=xx<w and 0<=yy<h and native[yy][xx] in (1,2,3)
                              for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
                if native[y][x] in (5,8) and neighbors>=3:eyes.append((x,y))
        if eyes:
            eye_y=min(y for x,y in eyes)
            eyes=[x for x,y in eyes if y==eye_y]
            dy=eye_y-19
            if len(eyes)>1:
                dx=(min(eyes)+max(eyes)-15)//2;view=0
            else:dx=eyes[0]-5
            ear_y=eye_y-1
    image=atlas();forced=set()
    protected=set()
    for y,row in enumerate(native):
        for x,v in enumerate(row):
            if v not in (1,2,3):continue
            forehead=direction!=2 and eyes and ear_y-1<=y<=ear_y and min(eyes)-2<=x<=max(eyes)+2
            if not forehead:protected.add((x,y))
    if direction!=2:
        # Protect real pupils and face/ear edges, rather than the entire old
        # navy cap/temple rectangle behind the ear.
        for y in range(ear_y+1,min(h,ear_y+5)):
            for x in range(left,right+1):
                neighbors=sum(0<=xx<w and 0<=yy<h and native[yy][xx] in (1,2,3)
                              for xx,yy in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)))
                if native[y][x] in (4,5,6,7,8,9,12,13,14,15) and neighbors>=2:
                    protected.add((x,y))
    # Keep real ears and their outside rims, never the retired cap between them.
    if direction in (0,2):
        protected|={(x,y) for y in (ear_y,ear_y+1) for x in (left-1,right+1)
                    if 0<=x<w and native[y][x] in (1,2,3)}
        if direction==2:
            protected|={(x,y) for y in (ear_y,ear_y+1) for x in (left,right)
                        if native[y][x] in (1,2,3)}
            protected|={(x,y) for y in (ear_y,ear_y+1) for x in (left-1,right+1)
                        if 0<=x<w and native[y][x]}
    if state=='fishing':
        from build_style_layers import fishing_rod
        protected|=fishing_rod(native,0,pose)
    l,t,r,b=box
    bottom=ear_y+2 if direction==2 else ear_y+3
    for y in range(max(0,t),min(h,bottom+1)):
        for x in range(max(0,l),min(w,r+1)):
            if (x,y) in protected or native[y][x] in (1,2,3,12,13):
                continue
            out[y][x]=0;forced.add((x,y))
    for ay in range(6,22):
        y=ay+dy
        if not 0<=y<h:continue
        for ax in range(16):
            x=ax+dx
            if not 0<=x<w or (x,y) in protected:continue
            value=image.getpixel((view*16+ax,(style-1)*32+ay))
            if not value:continue
            if value==5:value=8 # Reference navy hair-edge pixels use the hair ramp.
            if native[y][x] in (12,13):continue
            out[y][x]=value;forced.add((x,y))
    if direction!=2:
        center=(min(eyes)+max(eyes))//2 if eyes else (left+right)//2
        # Skin under a fringe must remain solid even where the enlarged
        # reference leaves tiny background gaps between separate locks.
        for y in range(ear_y-3,ear_y+2):
            for x in range(center-2,center+3):
                if 0<=x<w and 0<=y<h and not out[y][x] and (x,y) not in protected:
                    out[y][x]=1;forced.add((x,y))
    # The reference neck begins where the original cap rim ended. Restore
    # skin there if a short rear cut leaves that formerly covered row exposed.
    if direction==2:
        for y in (ear_y,ear_y+1):
            for x in range(left+1,right):
                if not out[y][x]:out[y][x]=8;forced.add((x,y))
        for x in range(left+3,right-2):
            y=ear_y+2
            if 0<=y<h and not out[y][x]:out[y][x]=3;forced.add((x,y))
    return out,forced
