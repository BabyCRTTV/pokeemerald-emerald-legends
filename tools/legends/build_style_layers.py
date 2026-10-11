"""Author pose-local hair and outerwear edits; runtime only applies checked ROM masks.

Native head/face landmarks are resolved at authoring time. Each animation slot
has its own edit list, so cycling and back throws never guess a head position.
Hair outlines/tufts use native brown/shadow colors, never shoe/scarf slots.
"""
from pathlib import Path
import json,re,struct
from PIL import Image,ImageDraw
from build_appearance import ROOT,STATES,FILES,frames,skin_components,hand_pixels,ball_pixels

# Deliberately drawn small silhouettes, with coherent crowns, parting and tufts.
# Geometry is normalized to a 16x14 head, then drawn at each native pose's size.
SHAPES=[
 [(2,5),(3,2),(6,1),(11,1),(14,3),(15,6),(14,9),(2,9)],
 [(1,6),(2,3),(6,1),(12,1),(15,4),(15,8),(11,9),(9,5),(5,8),(1,9)],
 [(1,8),(2,4),(4,5),(5,0),(8,3),(10,0),(12,4),(14,2),(15,8),(13,10),(2,10)],
 [(1,7),(2,3),(6,1),(12,1),(15,4),(14,7),(10,8),(5,10),(1,10)],
 [(1,7),(0,5),(3,4),(3,1),(6,2),(9,0),(11,2),(14,2),(14,5),(16,6),(14,10),(3,10)],
 [(2,7),(3,4),(6,2),(11,2),(14,4),(14,8),(11,9),(8,6),(5,9),(2,9)],
 [(1,11),(1,5),(3,2),(7,1),(11,1),(14,3),(15,6),(15,12),(12,13),(10,9),(4,9),(3,13)],
 [(1,10),(0,7),(1,5),(1,3),(4,2),(6,0),(9,1),(12,0),(14,3),(16,5),(15,8),(16,11),(13,13),(11,10),(4,10),(3,13)],
 [(2,8),(2,4),(5,1),(11,1),(14,3),(15,7),(13,10),(10,8),(5,8),(3,10)],
 [(2,9),(1,5),(4,2),(7,1),(11,1),(14,3),(15,7),(13,10),(10,8),(5,8),(3,10)],
]

def head(p,gender,kind,pose,state=''):
    groups=skin_components(p);h,w=len(p),len(p[0])
    if kind!='overworld':
        candidates=[s for s in groups if len(s)>30]
        face=min(candidates,key=lambda s:min(y for x,y in s))
        # Every native portrait/back frame has a distinct hat/face location.
        left=min(x for x,y in face);right=max(x for x,y in face)
        top=min(y for x,y in face);bottom=max(y for x,y in face)
        if kind=='front':
            return face,(19 if gender==0 else 13,7,38 if gender==0 else 39,27 if gender else 23), (28 if gender==0 else 27,8,20 if gender==0 else 18,11),0
        return face,(max(0,left-25),max(0,top-22),min(w-1,right+15),min(h-1,bottom+5)), ((left+right)//2-9,top-21,28,23),2
    # Native tables: front, back, left, plus the matching motion poses.
    direction=(0 if pose%3==0 else 2 if pose%3==1 else 1) if w==16 else None
    face=max(groups,key=len) if groups else set()
    if not face:return set(),(0,0,0,0),(0,0,0,0),0
    top=min(y for x,y in face);bottom=max(y for x,y in face)
    # Facing-away head has no face island: use the upper hat silhouette.
    occupied=[(x,y) for y in range(h) for x in range(w) if p[y][x]]
    upper=min(y for x,y in occupied)
    if direction==2:
        # Back sprites have an exposed neck, not a forehead.
        cy=upper;cx=round(sum(x for x,y in occupied if y<=upper+5)/sum(1 for x,y in occupied if y<=upper+5))
    else:
        cx=round(sum(x for x,y in face)/len(face));cy=top-5
    if w==32:
        # The face island remains useful in bike/field-action poses; topmost
        # skin at the head, excluding the disconnected lower hands.
        candidates=[s for s in groups if min(y for x,y in s)<24]
        face=max(candidates,key=len) if candidates else face
        # Tiny isolated ear highlights must not become the head anchor.
        # Join shaded face islands around the main component at authoring time.
        fl,fr=min(x for x,y in face),max(x for x,y in face)
        ft,fb=min(y for x,y in face),max(y for x,y in face)
        face=set().union(*(s for s in groups if all(fl-4<=x<=fr+4 and ft-3<=y<=fb+1 for x,y in s)))
        top=min(y for x,y in face);bottom=max(y for x,y in face)
        cx=round(sum(x for x,y in face)/len(face));cy=top-6
        direction=2 if top>=21 and max(x for x,y in face)-min(x for x,y in face)<=4 else 1 if max(x for x,y in face)-min(x for x,y in face)<6 else 0
        if state in ('mach_bike','acro_bike','surfing','watering'):
            direction=0 if pose%3==0 else 2 if pose%3==1 else 1
        if direction==2:cy=upper
    if direction==1:cx+=2
    hw=12
    ht=8 if direction!=2 else 10
    return face,(max(0,cx-(10 if w==32 else 8)),max(0,cy-2),min(w-1,cx+(10 if w==32 else 8)),bottom), (cx,cy,hw,ht),direction

def hair_edits(p,g,kind,pose,style,state=''):
    face,box,anchor,direction=head(p,g,kind,pose,state)
    cx,cy,hw,ht=anchor
    if not hw:return p
    h,w=len(p),len(p[0]);out=[r[:] for r in p]
    protected=set(face)
    if kind!='overworld':protected |= {(x,y) for x,y in hand_pixels(g,kind,pose) if p[y][x] not in (4,7,8)}|ball_pixels(g,kind,pose)
    # Preserve eyes/mouth and face outlines inside the native face envelope.
    if face:
        fl,fr=min(x for x,y in face),max(x for x,y in face)
        ft,fb=min(y for x,y in face),max(y for x,y in face)
        protected |= {(x,y) for y in range(ft,fb+1) for x in range(fl,fr+1) if p[y][x] in (1,2,3,4,5,7,8,9,12,13,14,15)}
    l,t,r,b=box
    for y in range(t,b+1):
        for x in range(l,r+1):
            if (x,y) not in protected and p[y][x] not in (1,2,3,12,13):out[y][x]=0
    mask=Image.new('L',(18,20));d=ImageDraw.Draw(mask)
    shape=SHAPES[style-1]
    d.polygon(shape,fill=4,outline=8)
    # Hand-drawn light cluster follows the crown; a dark curved part grounds
    # it in the native Gen 3 lighting instead of a flat horizontal slab.
    d.line([(3,6),(4,3),(7,2),(11,2)],fill=4,width=2)
    d.line([(5,7),(6,5),(7,4)],fill=8)
    d.line([(11,5),(12,7),(12,9)],fill=8)
    if style in (2,4):d.line([(9,2),(8,4),(7,6)],fill=8)
    if style==8:
        for x,y in ((3,4),(7,2),(12,3),(14,6),(2,8)):d.arc((x-1,y-1,x+2,y+2),20,290,fill=8)
    if style in (9,10):
        sides=(14,) if style==9 else (0,14)
        for x in sides:
            d.polygon([(x,7),(x+2,7),(x+3,10),(x+2,15),(x+1,18),(x-1,17),(x,12)],fill=4,outline=8)
            d.point((x+1,8),fill=9)
    if g:
        d.line([(4,4),(6,3),(10,3)],fill=7,width=1)
    # Back crowns have no fringe; side views expose a tapered temple.
    if direction==2:
        d.polygon([(2,6),(14,6),(15,11),(12,16),(7,17),(3,15),(1,11)],fill=4)
        d.line([(2,6),(1,11),(3,15),(7,17),(12,16),(15,11),(14,6)],fill=8)
        d.line([(4,7),(5,11),(6,14)],fill=8)
        d.line([(11,7),(12,10),(11,14)],fill=8)
        if g:d.line([(4,6),(4,9),(5,11)],fill=7)
    elif direction==1:
        d.polygon([(0,7),(3,7),(3,12),(0,12)],fill=0)
    scale=hw/16
    mh=round(20*ht/12);mw=round(18*scale)
    mask=mask.resize((mw,mh),Image.Resampling.NEAREST)
    ox=cx-hw//2;oy=cy
    for y in range(mask.height):
        for x in range(mask.width):
            px,py=ox+x,oy+y;v=mask.getpixel((x,y))
            if not v or not (0<=px<w and 0<=py<h) or (px,py) in protected:continue
            if p[py][px] in (1,2,3,12,13):continue
            # Hair stops at the collar unless a long style has side strands.
            if py>b and style not in (7,8,9,10):continue
            if py>b and p[py][px]!=0:continue
            out[py][px]=v
    if kind=='front':
        # Tapered sideburns join the crown to the ears without covering eyes.
        fl,fr=min(x for x,y in face),max(x for x,y in face)
        for x in (fl-2,fr+1):
            for y in range(cy+ht-3,min(cy+ht+3,h)):
                if 0<=x<w and (x,y) not in protected and p[y][x] not in (1,2,3,12,13):out[y][x]=8
    return out

def coat_edits(p,g,kind,pose,coat):
    h,w=len(p),len(p[0]);out=[r[:] for r in p]
    groups=skin_components(p)
    if not groups:return out
    face=max(groups,key=len) if kind=='overworld' else min((s for s in groups if len(s)>30),key=lambda s:min(y for x,y in s))
    fb=max(y for x,y in face);cx=round(sum(x for x,y in face)/len(face))
    protected=set(face)
    if kind!='overworld':protected |= hand_pixels(g,kind,pose)|ball_pixels(g,kind,pose)
    top=fb+1 if kind=='overworld' else (25 if kind=='front' else fb+1)
    # Front art: shaped shoulder seams -> fitted waist -> longer winter hem.
    # Back art: preserve the green native backpack over the coat.
    if kind=='front':
        top=25;cx=30 if g==0 else 28
        bottom=45 if coat==2 else 39
    elif kind=='back':bottom=64
    else:bottom=min(h-3,top+((7 if w==16 else 4) if coat==2 else 4))
    for y in range(top,bottom):
        extent=(8 if g else 9) if kind=='front' else (11 if kind=='back' else 4)
        rel=y-top
        if kind=='front':extent=(13 if rel<8 else (7 if g else 9) if rel<14 else (9 if g else 10))
        for x in range(max(0,cx-extent),min(w,cx+extent+1)):
            if (x,y) in protected:continue
            v=p[y][x]
            if v in (0,4,15):continue
            if kind=='back' and v in (10,11):continue # backpack stays visible
            # Keep legs clear; exposed upper arm becomes a real coat sleeve.
            if kind=='overworld' and (v in (1,2,3) or (rel>=2 and v in (5,6,7,8))):continue
            if kind=='front' and y>=43 and v in (1,2,3):continue
            if v==14:continue # selected scarf overlays the collar
            edge=abs(x-cx)>=extent-1
            if coat==2 and rel<4 and abs(x-cx)>1:
                out[y][x]=9 if rel<3 or (x+y)%3 else 5
            elif coat==2 and kind=='front' and rel in (10,11) and g:
                out[y][x]=8 # fitted belt, feminine flared hem
            elif x==cx and kind!='back':out[y][x]=8 # front fastening
            elif kind=='front' and x==cx+1 and rel in (6,11,16):out[y][x]=9
            else:out[y][x]=8 if edge or x>cx+2 else 5
        # Pose-local shoulder and long hem silhouettes, in transparent margins.
        if kind=='front' and 3<=rel<(18 if coat==2 else 10):
            for x in (cx-extent-1,cx+extent+1):
                if 0<=x<w and p[y][x]==0 and (x,y) not in protected:
                    out[y][x]=8
    if kind=='front':
        # Authored sleeve/torso contours follow the native asymmetric stance.
        # A filled garment (rather than repainting shirt pixels) covers the
        # shoulder and upper arm, and gives winter wear an actual lower hem.
        contours=(
            [(23,26),(20,29),(17,33),(20,35),(24,32),(24,39),(23,44),(38,44),(37,35),(40,30),(36,25)],
            [(23,25),(20,28),(17,30),(19,32),(23,30),(23,36),(21,43),(36,43),(34,36),(35,31),(39,35),(41,34),(37,27),(33,25)],
        )
        cloth=Image.new('L',(w,h));ImageDraw.Draw(cloth).polygon(contours[g],fill=5,outline=8)
        for y in range(25,45 if coat==2 else 39):
            for x in range(16,42):
                v=cloth.getpixel((x,y))
                if not v or (x,y) in protected:continue
                if p[y][x]==15:continue
                if v==5 and x>cx+4:v=8
                if g and y==36:v=8
                if x==cx:v=8
                if x==cx+1 and y in (32,37,42):v=9
                out[y][x]=v
    if coat==2:
        # Thick turned shearling lapels and a scalloped neckline. This is
        # authored outside the original shirt boundary so the coat reads as
        # an added garment; it does not borrow the scarf palette slot.
        if kind=='front':
            collar=[(cx-7,24),(cx-5,24),(cx-3,26),(cx,27),(cx+3,26),(cx+5,24),(cx+7,25),(cx+5,29),(cx+3,30),(cx,29),(cx-4,30),(cx-7,27)]
            mask=Image.new('L',(w,h));ImageDraw.Draw(mask).polygon(collar,fill=9,outline=8)
            for y in range(24,31):
                for x in range(max(0,cx-8),min(w,cx+9)):
                    v=mask.getpixel((x,y))
                    if v and (x,y) not in protected and p[y][x] not in (12,13):out[y][x]=v
        elif kind=='overworld':
            for y in range(top,min(top+2,h)):
                for x in range(max(0,cx-3),min(w,cx+4)):
                    if p[y][x] and p[y][x] not in (1,2,3,12,13,15) and (x,y) not in protected:out[y][x]=9
    return out

def build():
    mapping=json.loads((ROOT/'tools/legends/appearance_frames.json').read_text())
    blob=bytearray();headers=['// Generated pose-local hair/coat edits.\n'];pose_count=0
    tables=[];back=[];front=[];counts=[]
    def emit(p,g,kind,i,state=''):
        nonlocal pose_count
        items=[]
        for hair in range(1,11):items.append(hair_edits(p,g,kind,i,hair,state))
        for coat in (1,2):items.append(coat_edits(p,g,kind,i,coat))
        desc=[]
        for edited in items:
            off=len(blob)//2
            edits=[((y*len(p[0])+x)<<4)|v for y,row in enumerate(edited) for x,v in enumerate(row) if v!=p[y][x]]
            blob.extend(struct.pack('<'+'H'*len(edits),*edits));desc.append(f'{{{off},{len(edits)}}}')
        pose_count+=1
        return '{'+','.join(desc)+'}'
    for g,name in enumerate(('Brendan','May')):
        gt=[];gc=[]
        for si,(state,file) in enumerate(zip(STATES,FILES)):
            w=16 if si==0 else 32;path=ROOT/f'graphics/object_events/pics/people/{name.lower()}/{file}.png';src=frames(path,w,32)
            if si==0:src+=frames(path.with_name('running.png'),16,32)
            tab=mapping[name][state]['table'];idx=list(range(len(src))) if 'overworld_ascending_frames' in tab else [int(v) for v in re.findall(r'overworld_frame\([^,]+,\s*\d+,\s*\d+,\s*(\d+)\)',tab)]
            gc.append(len(idx))
            symbol=f'sStyle{g}{si}'
            headers.append(f'static const struct StyleEdits {symbol}[][12] = {{\n'+',\n'.join(emit(src[i],g,'overworld',i,file) for i in idx)+'\n};\n');gt.append(symbol)
        counts.append(gc)
        tables.append('{'+','.join(gt)+'}')
        front.append(emit(frames(ROOT/f'graphics/trainers/front_pics/{name.lower()}.png',64,64)[0],g,'front',0))
        back.append('{'+','.join(emit(p,g,'back',i) for i,p in enumerate(frames(ROOT/f'graphics/trainers/back_pics/{name.lower()}.png',64,64)))+'}')
    headers.insert(1,'struct StyleEdits { u32 offset; u16 count; };\nstatic const u16 sStylePixels[] = INCBIN_U16("graphics/legends/styles/edits.bin");\n')
    headers.append('static const u8 sStyleFrameCount[2][8] = {'+','.join('{'+','.join(map(str,c))+'}' for c in counts)+'};\n')
    headers.append('static const struct StyleEdits (*const sStyleWorld[2][8])[12] = {'+','.join(tables)+'};\n')
    headers.append('static const struct StyleEdits sStyleFront[2][12] = {'+','.join(front)+'};\n')
    headers.append('static const struct StyleEdits sStyleBack[2][4][12] = {'+','.join(back)+'};\n')
    directory=ROOT/'graphics/legends/styles';directory.mkdir(parents=True,exist_ok=True);(directory/'edits.bin').write_bytes(blob)
    (ROOT/'src/data/legends/style_layers.h').write_text(''.join(headers))
    print(f'{pose_count} pose masks, {len(blob)} bytes of sparse edits')
if __name__=='__main__':build()
