"""Author pose-local hair and outerwear edits; runtime only applies checked ROM masks.

Native head/face landmarks are resolved at authoring time. Each animation slot
has its own edit list, so cycling and back throws never guess a head position.
Hair outlines/tufts use native brown/shadow colors, never shoe/scarf slots.
"""
from pathlib import Path
import json,re,struct
from PIL import Image,ImageDraw
from build_appearance import ROOT,STATES,FILES,frames,skin_components,hand_pixels,ball_pixels

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
        return face,(max(0,left-25),max(0,top-22),min(w-1,right+15),min(h-1,bottom)), ((left+right)//2-10,top-14,26,16),2
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
    return face,(max(0,cx-(10 if w==32 else 8)),max(0,min(cy-2,upper) if w==16 else cy-2),min(w-1,cx+(10 if w==32 else 8)),bottom), (cx,cy,hw,ht),direction

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
        protected |= {(x,y) for y in range(ft,fb+1) for x in range(fl,fr+1) if p[y][x] in (1,2,3,4,5,6,7,8,9,12,13,14,15)}
    l,t,r,b=box
    for y in range(t,b+1):
        for x in range(l,r+1):
            if (x,y) not in protected and p[y][x] not in (1,2,3,12,13):
                # Keep the native nape behind the ear in back portraits;
                # removing it would detach the hair from the face/neck.
                if kind=='back' and face and y>=min(yy for xx,yy in face)-4 and p[y][x] in (4,7,8,15):
                    continue
                out[y][x]=0
    from hair_pixels import portrait, overworld
    rows = overworld(style, g) if kind == 'overworld' else portrait(style, g)
    mask = Image.new('L', (len(rows[0]), max(24 if kind=='back' else 20, len(rows))))
    for yy, row in enumerate(rows):
        for xx, char in enumerate(row):
            mask.putpixel((xx, yy), {'.':0, '#':8, '+':4, 'H':7}[char])
    if direction == 2:
        # Back-facing locks use the same outer contour, with a connected
        # shaded crown instead of the front fringe's gaps.
        width=len(rows[0])
        length=(14 if g else 12) if kind=='overworld' else (22 if g else 20)
        if style in (1,2,3,4,5,6):length-=2
        center=(width-1)//2
        for yy in range(3,length):
            radius=width//2-2
            if yy>length//2:
                radius=max(2,radius-(yy-length//2+1)//2)
            left,right=center-radius,center+radius
            for xx in range(left,right+1):
                v=8 if xx in (left,right) or (yy>=length-3 and xx>center+1) else 4
                # A broad curved light cluster breaks into tapered locks,
                # following the supplied back-facing reference lighting.
                offset=1 if yy<length//3 else 2
                if 3<=yy<length-4 and left+offset<=xx<=left+offset+(3 if kind!='overworld' else 2):v=7
                if yy in (length//2,length//2+2) and xx==left+offset:v=4
                mask.putpixel((xx,yy),v)
    elif direction == 1:
        # The side fringe points toward the face. The far-side temple lies
        # behind the ear; native eye and nose pixels remain protected below.
        d=ImageDraw.Draw(mask)
        d.rectangle((0,9,2,19),fill=0)
    if kind == 'front':
        hw=len(rows[0]);cx,cy=(29,7) if g==0 else (28,7)
    elif kind=='overworld':
        hw=len(rows[0])
        if direction!=2:cy-=2
    else:
        # Each back-animation frame has a different face anchor. Scale the
        # larger portrait grid to its own crown, never the tiny field sprite.
        scale=hw/len(rows[0])
        mask=mask.resize((hw,round(mask.height*scale)),Image.Resampling.NEAREST)
    ox=cx-hw//2;oy=cy
    for y in range(mask.height):
        for x in range(mask.width):
            px,py=ox+x,oy+y;v=mask.getpixel((x,y))
            if not v or not (0<=px<w and 0<=py<h) or (px,py) in protected:continue
            if p[py][px] in (1,2,3,12,13):continue
            # Hair stops at the collar unless a long style has side strands.
            if py>b and style not in (7,8,9,10):continue
            if py>b and p[py][px] in (1,2,3,12,13,15):continue
            out[py][px]=v
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
    if kind in ('front','back'):
        # Carry sleeves to the glove/cuff boundary. The old torso-width pass
        # missed outstretched arms, making the winter coat look sleeveless.
        for y in range(top, h if kind == 'back' else 37):
            for x in range(w):
                if (x,y) in protected or p[y][x] not in (1,2,3):
                    continue
                if kind == 'front' and not (x < 24 or x > 35):
                    continue
                out[y][x] = 5 if p[y][x] == 1 else 8
        if kind == 'front':
            # Continuous lower hem plus a lit opening seam; keep the shorter
            # Navy jacket distinct from Winter's longer fitted silhouette.
            hem = 43 if coat == 2 and g else 44 if coat == 2 else 38
            for x in range(22 if g else 24, 36 if g else 38):
                if (x,hem) not in protected and out[hem][x] in (5,8):
                    out[hem][x] = 8
            for y in range(31,hem):
                if out[y][cx-1] == 5:out[y][cx-1] = 9 if y in (32,37,42) else 5
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
