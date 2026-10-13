"""Author pose-local hair and outerwear edits; runtime only applies checked ROM masks.

Native head/face landmarks are resolved at authoring time. Each animation slot
has its own edit list, so cycling and back throws never guess a head position.
Hair outlines/tufts use native brown/shadow colors, never shoe/scarf slots.
"""
from pathlib import Path
import json,re,struct
from PIL import Image,ImageDraw
from build_appearance import ROOT,STATES,FILES,frames,skin_components,hand_pixels,ball_pixels

# In two throw frames the arm touches the cheek. Skin flood-fill alone then
# joins the forearm to the face, incorrectly protecting it from long sleeves.
BACK_FACE_RECTS = (
    ((31,28,44,39),(37,29,50,39),(26,30,44,42),(35,27,49,37)),
    ((28,30,42,42),(34,30,49,43),(22,32,38,49),(29,29,44,42)),
)
# May's original swept lock extends beyond the face/hat envelope. Clear that
# native lock when a custom cut is selected; it is not the connected nape.
BACK_FRONT_LOCK_RECTS = ((42,27,63,46),(49,29,63,43),(38,31,49,48),(44,27,63,45))

# Directions of SOURCE-sheet poses, before native pic-table indirection.
# Walking/running/bikes group the two step frames by facing direction.
# They do not alternate down/up/left on every frame.
WORLD_DIRECTIONS = {
    'walking': (0,2,1,0,0,2,2,1,1) * 2,
    'running': (0,2,1,0,0,2,2,1,1),
    'mach_bike': (0,2,1,0,0,2,2,1,1),
    'acro_bike': (0,2,1,0,0,2,2,1,1,0,0,0,0,2,2,2,2,1,1,1,1,0,0,2,2,1,1),
    'surfing': (0,0,2,2,1,1),
    'watering': (0,0,2,2,1,1),
    'fishing': (1,1,1,1,2,2,2,2,0,0,0,0),
    'field_move': (0,0,1,1,1),
}

FISHING_ROD_RECTS = (
    (23,4,31,14),(25,3,30,12),(4,10,16,24),(3,20,18,25),
    (24,18,24,30),(23,22,24,29),(23,6,24,14),(16,3,16,11),
    (10,1,10,16),(8,8,10,18),(8,19,12,28),(15,21,15,30),
)

def fishing_rod(p,g,pose):
    l,t,r,b=FISHING_ROD_RECTS[pose]
    return {(x,y) for y in range(t,b+1) for x in range(l,r+1)
            if p[y][x] in (12,13,15)}

def head(p,gender,kind,pose,state=''):
    groups=skin_components(p);h,w=len(p),len(p[0])
    if kind!='overworld':
        candidates=[s for s in groups if len(s)>30]
        face=min(candidates,key=lambda s:min(y for x,y in s))
        if kind=='back':
            l,t,r,b=BACK_FACE_RECTS[gender][pose]
            face={(x,y) for y in range(t,b+1) for x in range(l,r+1) if p[y][x] in (1,2,3)}
        # Every native portrait/back frame has a distinct hat/face location.
        left=min(x for x,y in face);right=max(x for x,y in face)
        top=min(y for x,y in face);bottom=max(y for x,y in face)
        if kind=='front':
            return face,(19 if gender==0 else 13,7,38 if gender==0 else 39,27 if gender else 23), (28 if gender==0 else 27,8,20 if gender==0 else 18,11),0
        return face,(max(0,left-25),max(0,top-22),min(w-1,right+15),min(h-1,bottom)), ((left+right)//2-10,top-14,26,16),2
    # Native tables: front, back, left, plus the matching motion poses.
    direction=WORLD_DIRECTIONS[state][pose] if state in WORLD_DIRECTIONS else None
    face=max(groups,key=len) if groups else set()
    if direction==2:
        # Anchor the crown to native hat highlights, not an exposed ear or
        # a fishing rod. One wheelie pose has no skin island at all.
        marker=10 if gender else 14
        points=[(x,y) for y,row in enumerate(p) for x,v in enumerate(row) if v==marker]
        top=min(y for x,y in points)
        crown=[(x,y) for x,y in points if y<top+4]
        cx=round((min(x for x,y in crown)+max(x for x,y in crown))/2)
        cy=top-(2 if gender or w==16 else 1)
        bottom=cy+(11 if gender else 9)
        face={(x,y) for y in range(cy,min(h,bottom+1)) for x in range(max(0,cx-8),min(w,cx+9)) if p[y][x] in (1,2,3)}
        return face,(max(0,cx-8),max(0,cy-1),min(w-1,cx+8),bottom),(cx,cy,12,10),direction
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
        if direction is None:
            direction=2 if top>=21 and max(x for x,y in face)-min(x for x,y in face)<=4 else 1 if max(x for x,y in face)-min(x for x,y in face)<6 else 0
        if direction==2:cy=upper
    if direction==1:cx+=2
    hw=12
    ht=8 if direction!=2 else 10
    return face,(max(0,cx-(10 if w==32 else 8)),max(0,min(cy-2,upper) if w==16 else cy-2),min(w-1,cx+(10 if w==32 else 8)),bottom), (cx,cy,hw,ht),direction

# Actual gloves/palms, separate from the old bare-hand outfit masks which
# also included forearm pixels. Coats must cover those forearms to the cuff.
COAT_HAND_RECTS = {
 (0,'front'): [[(14,37,17,40),(45,29,50,33)]],
 (1,'front'): [[(9,29,17,32),(41,35,48,39)]],
 (0,'back'): [[(0,36,12,48),(54,47,63,55)],[(0,24,12,34),(50,59,63,63)],[(49,21,63,33)],[]],
 (1,'back'): [[(0,39,14,49),(43,47,50,52)],[(0,25,13,35),(49,57,56,63)],[(43,25,58,33),(5,57,15,63)],[]],
}
def coat_hands(g,kind,pose):
 return {(x,y) for l,t,r,b in COAT_HAND_RECTS[g,kind][pose] for y in range(t,b+1) for x in range(l,r+1)}

def head_core(p,g,kind,pose,state=''):
    face,box,anchor,direction=head(p,g,kind,pose,state)
    cx,cy,hw,ht=anchor
    if not face:return set()
    l,t,r,b=box
    if kind=='front':b=min(b,max(y for x,y in face))
    # Native filled skull, excluding the extended hat brim/tip. Retaining this
    # coverage under every cut prevents short crowns from erasing the nape.
    radius=5 if kind=='overworld' else hw//2-2
    top=cy+(6 if kind=='back' else 2) if kind!='front' else 11
    core=set()
    for y in range(max(t,top),b+1):
        width=max(3,radius-max(0,y-cy-12)//2) if kind=='back' else radius
        core|={(x,y) for x in range(max(l,cx-width),min(r,cx+width)+1) if p[y][x] and p[y][x] not in (12,13)}
    return core

def original_hair(p,g,kind,pose,state=''):
    face,box,anchor,direction=head(p,g,kind,pose,state)
    l,t,r,b=box;points=set()
    hands=hand_pixels(g,kind,pose) if kind!='overworld' else set()
    # Brown native hair only: eyes use 5/8/9/14/15, skin uses 1/2/3.
    for y in range(t,b+1):
        for x in range(l,r+1):
            if (x,y) not in hands and p[y][x] in ((4,7) if g else (4,)):
                points.add((x,y))
    return points

def hair_edits(p,g,kind,pose,style,state='',with_points=False):
    face,box,anchor,direction=head(p,g,kind,pose,state)
    if g == 0 and kind == 'overworld' and state != 'underwater' and direction in (0,1,2):
        from male_overworld_hair import imported_hair
        art,points=imported_hair(p,style,face,box,direction,state,pose)
        return (art,points) if with_points else art
    cx,cy,hw,ht=anchor
    if not hw:return (p,set()) if with_points else p
    h,w=len(p),len(p[0]);out=[r[:] for r in p];hair_points=set()
    protected=set(face)
    if kind=='overworld' and state=='fishing':
        # Rods are thin red/black components outside the native head; retain
        # them even when a long hairstyle crosses the casting silhouette.
        protected |= {(x,y) for y,row in enumerate(p) for x,v in enumerate(row)
                      if v in (12,13,15) and (x,y) in fishing_rod(p,g,pose)}
    if kind!='overworld':protected |= coat_hands(g,kind,pose)|ball_pixels(g,kind,pose)
    # Preserve eyes/mouth and face outlines inside the native face envelope.
    if face:
        fl,fr=min(x for x,y in face),max(x for x,y in face)
        ft,fb=min(y for x,y in face),max(y for x,y in face)
        protected |= {(x,y) for y in range(ft,fb+1) for x in range(fl,fr+1) if p[y][x] in (1,2,3,4,5,6,7,8,9,12,13,14,15)}
    l,t,r,b=box
    for y in range(t,b+1):
        for x in range(l,r+1):
            if (x,y) not in protected and p[y][x] not in (1,2,3,12,13):
                if kind=='front' and face and y>max(yy for xx,yy in face):
                    fl,fr=min(xx for xx,yy in face),max(xx for xx,yy in face)
                    if p[y][x] not in (4,7,8) or fl<=x<=fr:
                        continue # Native collar/neck is not part of a hat.
                # Keep the native nape behind the ear in back portraits;
                # removing it would detach the hair from the face/neck.
                if kind=='back' and face and p[y][x] in (4,7,8,15):
                    fl=min(xx for xx,yy in face);ft=min(yy for xx,yy in face)
                    if fl-3<=x<fl+2 and ft-1<=y<=max(yy for xx,yy in face):continue
                out[y][x]=0
    if g and kind=='front':
        # Native May's small swept-hair triangle sits beside her shoulder,
        # below the face envelope. Clear its outline as well as brown pixels.
        for y in range(23,28):
            for x in range(18,22):
                if (x,y) not in protected and p[y][x] in (4,7,8,15):out[y][x]=0
        # Retire the detached outline and the old jacket's extension into
        # native transparent cells. Force these edits into the sparse layer.
        for x,y in ((22,24),(21,26),(21,27)):
            out[y][x]=0
            hair_points.add((x,y))
    if g and kind=='back':
        l,t,r,b=BACK_FRONT_LOCK_RECTS[pose]
        for y in range(t,b+1):
            for x in range(l,r+1):
                if (x,y) not in protected and p[y][x] in (4,7,8,15):out[y][x]=0
    from hair_pixels import portrait, overworld
    rows = overworld(style, g) if kind == 'overworld' else portrait(style, g)
    mask = Image.new('L', (len(rows[0]), max(32 if kind=='back' else 20, len(rows))))
    for yy, row in enumerate(rows):
        for xx, char in enumerate(row):
            mask.putpixel((xx, yy), {'.':0, '#':8, '+':4, 'H':7}[char])
    if direction == 2:
        # Back-facing locks use the same outer contour, with a connected
        # shaded crown instead of the front fringe's gaps.
        width=len(rows[0])
        length=(14 if g else 12) if kind=='overworld' else (26 if g else 24)
        if style in (1,2,3,4,5,6):length-=2
        center=(width-1)//2
        for yy in range(3,length):
            radius=width//2-(2 if kind=='overworld' else 1)
            taper=length//2
            if yy>taper:
                radius=max(2,radius-(yy-taper+1)//2)
            left,right=center-radius,center+radius
            for xx in range(left,right+1):
                v=8 if xx in (left,right) or (yy>=length-3 and xx>center+1) else 4
                # A broad curved light cluster breaks into tapered locks,
                # following the supplied back-facing reference lighting.
                offset=1 if yy<length//3 else 2
                if kind!='overworld':offset=2+yy//6
                span=2 if kind=='overworld' or yy>=14 else 3 if yy>=9 else 4
                if 3<=yy<length-4 and left+offset<=xx<=left+offset+span:v=7
                if yy in (length//2,length//2+2) and xx==left+offset:v=4
                if kind!='overworld' and yy>length//2 and xx in (center+3,center+5) and (xx+yy)%4!=0:v=8
                mask.putpixel((xx,yy),v)
        # Ties remain visible from behind instead of becoming the same round
        # bob as every other cut. These are drawn at each native grid size.
        strands=[]
        if style==9:
            strands=[(center-1,5,('###','#H+#','#++#','#++#','###'))] if not g else [(center-1,6,('####','#HH#','#H+#','#H+#','#++#','#++#','###'))]
        elif g and style==10:
            strands=[(1,6,('###','#H#','#H#','#+#','###')), (width-4,6,('###','#H#','#H#','#+#','###'))]
        for sx,sy,locks in strands:
            for yy,row in enumerate(locks):
                for xx,char in enumerate(row):
                    mask.putpixel((sx+xx,sy+yy),{'#':8,'+':4,'H':7}[char])
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
            out[py][px]=v;hair_points.add((px,py))
    core=head_core(p,g,kind,pose,state)
    for x,y in core:
        if (x,y) not in protected and not out[y][x] and p[y][x] not in (1,2,3,12,13):
            out[y][x]=8 if (x-1,y) not in core or (x+1,y) not in core else 4
            hair_points.add((x,y))
    return (out,hair_points) if with_points else out

def coat_edits(p,g,kind,pose,coat,state=''):
    h,w=len(p),len(p[0]);out=[r[:] for r in p]
    cloth_points=set()
    def paint(x,y,value):
        out[y][x]=value
        if value in (5,8):cloth_points.add((x,y))
    groups=skin_components(p)
    if not groups:return out
    face=max(groups,key=len) if kind=='overworld' else head(p,g,kind,pose)[0]
    fb=max(y for x,y in face);cx=round(sum(x for x,y in face)/len(face))
    protected=set(face)
    if kind=='overworld' and state=='fishing':protected |= fishing_rod(p,g,pose)
    if kind!='overworld':protected |= coat_hands(g,kind,pose)|ball_pixels(g,kind,pose)
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
                paint(x,y,9 if rel<3 or (x+y)%3 else 5)
            elif coat==2 and kind=='front' and rel in (10,11) and g:
                paint(x,y,8) # fitted belt, feminine flared hem
            elif x==cx and kind!='back':paint(x,y,8) # front fastening
            elif kind=='front' and x==cx+1 and rel in (6,11,16):out[y][x]=9
            else:paint(x,y,8 if edge or x>cx+2 else 5)
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
                paint(x,y,v)
    if kind in ('front','back'):
        # Carry sleeves to the glove/cuff boundary. The old torso-width pass
        # missed outstretched arms, making the winter coat look sleeveless.
        for y in range(0 if kind=='back' else top, h if kind == 'back' else 37):
            for x in range(w):
                if (x,y) in protected or p[y][x] not in (1,2,3):
                    continue
                if kind == 'front' and not (x < 24 or x > 35):
                    continue
                paint(x,y,5 if p[y][x] == 1 else 8)
        if kind == 'front':
            # Continuous lower hem plus a lit opening seam; keep the shorter
            # Navy jacket distinct from Winter's longer fitted silhouette.
            hem = 43 if coat == 2 and g else 44 if coat == 2 else 38
            for x in range(22 if g else 24, 36 if g else 38):
                if (x,hem) not in protected and out[hem][x] in (5,8):
                    paint(x,hem,8)
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
                    if v and (x,y) not in protected and p[y][x] not in (12,13):paint(x,y,v)
        elif kind=='overworld':
            for y in range(top,min(top+2,h)):
                for x in range(max(0,cx-3),min(w,cx+4)):
                    if p[y][x] and p[y][x] not in (1,2,3,12,13,15) and (x,y) not in protected:out[y][x]=9
    for y in range(h):
        for x in range(w):
            if out[y][x]!=p[y][x] or (x,y) in cloth_points:
                if out[y][x]==5:out[y][x]=10
                elif out[y][x]==8:out[y][x]=15
    return out

def leggings_edits(p,g,kind,state,choice,pose=0):
    out=[row[:] for row in p]
    if not g or kind=='back' or state=='underwater':return out
    h,w=len(p),len(p[0])
    if kind=='front':
        # May's legs below her shorts and above her native shoes.
        rects=[(17,42,25,54),(29,42,36,54)]
    elif state=='walking':rects=[(3,25,12,28)]
    elif state=='running':rects=[(6,24,25,29)]
    elif state in ('mach_bike','acro_bike'):rects=[(4,23,27,30)]
    elif state=='surfing':rects=[(4,25,27,30)]
    elif state=='watering':rects=[(4,25,27,30)]
    elif state=='fishing':rects=[(4,25,27,30)]
    elif state=='field_move':rects=[(4,25,27,30)]
    else:return out
    face,_,_,_=head(p,g,kind,pose,state)
    protected=set(face)
    if kind=='front':protected |= coat_hands(g,kind,pose)
    # Keep native silhouette, face/ears, footwear outlines, shorts and hands.
    for l,t,r,b in rects:
        for y in range(t,min(b+1,h)):
            for x in range(l,min(r+1,w)):
                if (x,y) not in protected and p[y][x] in (1,2,3):
                    out[y][x]=5 if choice==1 and p[y][x] in (1,2) else 15
    return out

def build():
    mapping=json.loads((ROOT/'tools/legends/appearance_frames.json').read_text())
    blob=bytearray();headers=['// Generated pose-local hair/coat edits.\n'];pose_count=0
    tables=[];back=[];front=[];counts=[]
    def emit(p,g,kind,i,state=''):
        nonlocal pose_count
        items=[]
        for hair in range(1,11):
            art,points=hair_edits(p,g,kind,i,hair,state,True)
            items.append((art,points))
        for coat in (1,2):items.append((coat_edits(p,g,kind,i,coat,state),set()))
        original=original_hair(p,g,kind,i,state)
        # Forced native-hair values restore the two reserved hair shades even
        # if footwear or a source-color reservation touched the same index.
        items.append((p,original))
        body={(x,y) for y,row in enumerate(p) for x,v in enumerate(row)
              if v in (4,7) and (x,y) not in original}
        remap=[row[:] for row in p]
        for x,y in body:remap[y][x]=8 if p[y][x]==4 or g else 5
        items.append((remap,body))
        for choice in (1,2):items.append((leggings_edits(p,g,kind,state,choice,i),set()))
        desc=[]
        for edited,forced in items:
            off=len(blob)//2
            edits=[((y*len(p[0])+x)<<4)|v for y,row in enumerate(edited) for x,v in enumerate(row) if v!=p[y][x] or (x,y) in forced]
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
            headers.append(f'static const struct StyleEdits {symbol}[][16] = {{\n'+',\n'.join(emit(src[i],g,'overworld',i,file) for i in idx)+'\n};\n');gt.append(symbol)
        counts.append(gc)
        tables.append('{'+','.join(gt)+'}')
        front.append(emit(frames(ROOT/f'graphics/trainers/front_pics/{name.lower()}.png',64,64)[0],g,'front',0))
        back.append('{'+','.join(emit(p,g,'back',i) for i,p in enumerate(frames(ROOT/f'graphics/trainers/back_pics/{name.lower()}.png',64,64)))+'}')
    headers.insert(1,'struct StyleEdits { u32 offset; u16 count; };\nstatic const u16 sStylePixels[] = INCBIN_U16("graphics/legends/styles/edits.bin");\n')
    headers.append('static const u8 sStyleFrameCount[2][8] = {'+','.join('{'+','.join(map(str,c))+'}' for c in counts)+'};\n')
    headers.append('static const struct StyleEdits (*const sStyleWorld[2][8])[16] = {'+','.join(tables)+'};\n')
    headers.append('static const struct StyleEdits sStyleFront[2][16] = {'+','.join(front)+'};\n')
    headers.append('static const struct StyleEdits sStyleBack[2][4][16] = {'+','.join(back)+'};\n')
    directory=ROOT/'graphics/legends/styles';directory.mkdir(parents=True,exist_ok=True);(directory/'edits.bin').write_bytes(blob)
    (ROOT/'src/data/legends/style_layers.h').write_text(''.join(headers))
    print(f'{pose_count} pose masks, {len(blob)} bytes of sparse edits')
if __name__=='__main__':build()
