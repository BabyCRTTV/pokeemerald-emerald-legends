"""Fit supplied hairstyles to Emerald's native May battle frames.

The presentation sheets supply only hair. Native body/face/hand geometry and
all four throw poses are retained; no complete trainer image is scaled down.
The resulting static sheets use native 4bpp layout and independent skin and
hair palette slots. Nothing is composited or inferred during battle.
"""
import json
from PIL import Image, ImageDraw
from build_appearance import ROOT, pack, frames
from build_style_layers import head, BACK_FRONT_LOCK_RECTS
from battle_hair_finishes import finish

COLUMNS = ((244,552),(557,877),(882,1203),(1208,1523))
ROWS = ((133,262),(266,399),(403,535),(540,674),(679,812),(818,952),(958,1103))
SOURCE_ORDER = (1,2,3,0)  # wind-up, cast, release, idle
NATIVE_PATH = ROOT/'graphics/trainers/back_pics/may.png'
PALETTE = [tuple(Image.open(NATIVE_PATH).getpalette()[i*3:i*3+3]) for i in range(16)]
# Consolidate body-only warm edges to 8 and belt greens to 10. This frees
# 4/7/11 for a native three-shade hair ramp without tinting skin or clothing.
PALETTE[4],PALETTE[7],PALETTE[11]=PALETTE[8],PALETTE[4],PALETTE[7]
RAMPS = [((74,49,57),(123,90,82),(164,106,82)),
         ((24,24,32),(41,41,57),(74,74,98)),
         ((49,32,32),(82,57,49),(131,90,65)),
         ((74,41,32),(123,65,41),(173,106,74)),
         ((65,24,32),(106,41,41),(164,74,57)),
         ((90,57,32),(148,98,49),(213,156,90)),
         ((131,90,49),(197,148,65),(246,213,131)),
         ((74,74,98),(139,148,180),(213,222,239))]

def groups(points):
    remaining=set(points); result=[]
    while remaining:
        seed=min(remaining); remaining.remove(seed); queue=[seed]; group={seed}
        for x,y in queue:
            for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if q in remaining:
                    remaining.remove(q);group.add(q);queue.append(q)
        result.append(group)
    return sorted(result,key=lambda g:(-len(g),min(g)))

def bounds(points):
    return min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)

def source_hair(im, column):
    l,r=COLUMNS[column];t,b=ROWS[0];cell=im.crop((l,t,r,b))
    skin=set();brown=set()
    for y in range(cell.height):
        for x in range(cell.width):
            rr,g,bb=cell.getpixel((x,y))
            if rr>184 and rr>g+20 and g>bb-12 and g>120 and rr<g*1.8:
                skin.add((x,y))
            if 30<rr<=185 and 20<g<145 and 15<bb<130 and g*1.04<rr<g*1.7 and bb>g*.62:
                brown.add((x,y))
    face=min((s for s in groups(skin) if len(s)>200 and bounds(s)[1]<85),key=lambda s:bounds(s)[1])
    fl,ft,fr,fb=bounds(face)
    # Select head-connected brown regions, including braids/ponytail which
    # can be separated from the crown by the source's dark outline or ties.
    candidates=[g for g in groups({q for q in brown if fl-125<=q[0]<=fr+12 and q[1]<=fb+47}) if len(g)>25]
    crown=min((g for g in candidates if bounds(g)[1]<ft),key=lambda g:(-len(g),min(g)))
    hair=set(crown);pending=[g for g in candidates if g is not crown]
    while pending:
        added=False
        for g in pending[:]:
            if any((x+dx,y+dy) in hair for x,y in g for dx,dy in ((-4,0),(4,0),(0,-4),(0,4),(-3,-3),(3,3),(-3,3),(3,-3))):
                hair.update(g);pending.remove(g);added=True
        if not added:break
    # Retain dark contour/strand pixels next to the brown regions, including
    # the divisions between braid lobes. Reconstructing only the outside
    # silhouette would turn woven braids into an unbroken ponytail.
    nearby=set(hair)
    for x,y in hair:
        nearby.update((x+dx,y+dy) for dx,dy in ((-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,1),(-1,1),(1,-1)))
    for x,y in nearby:
        if 0<=x<cell.width and 0<=y<cell.height:
            rr,g,bb=cell.getpixel((x,y))
            if max(rr,g,bb)<85 and rr+g+bb<175:hair.add((x,y))
    return cell,hair,(fl,ft,fr,fb)

def neighbors(points):
    return {(x+dx,y+dy) for x,y in points for dx,dy in
            ((-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1))
            if 0<=x+dx<64 and 0<=y+dy<64}

def eye_anchor(p, face):
    l,t,r,b=bounds(face)
    eye={(x,y) for y in range(t,b+1) for x in range(l,r+1) if p[y][x]==14}
    assert eye, 'native eye landmark missing'
    return sum(x for x,y in eye)/len(eye),sum(y for x,y in eye)/len(eye)

def source_eye(cell, face):
    l,t,r,b=face
    whites={(x,y) for y in range(t,b+1) for x in range(l,r+1)
            if min(cell.getpixel((x,y)))>165 and
            max(cell.getpixel((x,y)))-min(cell.getpixel((x,y)))<30}
    assert whites, 'source eye landmark missing'
    eye=groups(whites)[0]
    return sum(x for x,y in eye)/len(eye),sum(y for x,y in eye)/len(eye)

# Native collar pixels sit partly inside the old bandana/hair envelope.
COLLAR_RECTS = ((25,41,41,48),(30,41,44,50),(15,44,30,54),(26,40,42,48))
# Exact glove/cuff regions, rather than the outfit compositor's broad bare-
# hand rectangles (which also include native hat/hair in the raised poses).
GLOVE_RECTS = (
    ((0,38,14,52),(43,45,54,56)),
    ((0,25,13,35),(0,35,17,43),(46,54,56,63)),
    ((41,25,63,37),(5,50,15,63)),
    (),
)
RETIRED_NAPE = (((19,43,24,44),),(),(),((22,43,23,43),))

def native_hands(p, pose):
    result=set()
    for l,t,r,b in GLOVE_RECTS[pose]:
        points={(x,y) for y in range(t,b+1) for x in range(l,r+1) if p[y][x]}
        if (pose==0 and l==43) or (pose==2 and l==41):
            # Swept brown hair abuts these hands but is not glove anatomy.
            core={q for q in points if p[q[1]][q[0]] in (1,2,3,5,6,9,10,11,14)}
            points=core|{q for q in neighbors(core)&points if p[q[1]][q[0]]==15}
        result.update(points)
    return result

def native_base(p, pose):
    """Retain anatomy; remove only the native headwear and swept locks."""
    face,box,_,_=head(p,1,'back',pose)
    fl,ft,fr,fb=bounds(face)
    white={(x,y) for y in range(ft,fb+1) for x in range(fl,fr+1) if p[y][x]==14}
    eye=white|{(x,y) for x,y in neighbors(neighbors(white)) if p[y][x] in (5,6,9,14,15)}
    # A filled face rectangle also retains old hair beside the cheek. Keep
    # actual skin/eye cells and their one-pixel contour instead.
    features=face|eye
    face_protected=features|{(x,y) for x,y in neighbors(features) if p[y][x] in (4,7,8,15)}
    hands=native_hands(p,pose)
    l,t,r,b=COLLAR_RECTS[pose]
    collar={(x,y) for y in range(t,b+1) for x in range(l,r+1) if p[y][x] in (5,6)}
    body={(x,y) for y,row in enumerate(p) for x,v in enumerate(row)
          if v in (12,13) or (v in (1,2,3) and (x,y) not in face)}
    body_edges={(x,y) for x,y in neighbors(body|hands|collar) if p[y][x] in (4,8,15)}
    keep=face_protected|hands|collar|body|body_edges
    erase=set()
    for rect in (box,BACK_FRONT_LOCK_RECTS[pose]):
        l,t,r,b=rect
        for y in range(t,b+1):
            for x in range(l,r+1):
                if (x,y) not in keep and (rect==box or p[y][x] in (4,7,8,15)):
                    erase.add((x,y))
    for l,t,r,b in RETIRED_NAPE[pose]:
        for y in range(t,b+1):
            for x in range(l,r+1):
                if p[y][x] in (4,7,8,15):erase.add((x,y))
    out=[row[:] for row in p]
    for x,y in erase:out[y][x]=0
    # The release forearm was hidden beneath May's original swept hair.
    # Restore it behind the native face and in front of the new hair. The
    # skin materials remain 1/2/3 so all five tones affect the restored arm.
    arm=set()
    if pose==2:
        patch=Image.new('L',(64,64));draw=ImageDraw.Draw(patch)
        draw.polygon(((25,49),(30,51),(43,35),(43,31),(39,30),(26,44)),fill=8)
        draw.polygon(((27,48),(29,49),(41,34),(41,32),(39,32),(28,44)),fill=2)
        draw.polygon(((28,44),(39,32),(40,32),(29,47)),fill=1)
        draw.line(((28,48),(29,49),(41,34)),fill=3,width=1)
        for y in range(64):
            for x in range(64):
                v=patch.getpixel((x,y))
                if v:
                    arm.add((x,y))
                    if (x,y) not in keep:out[y][x]=v
    for y,row in enumerate(out):
        for x,v in enumerate(row):
            if v==11:row[x]=10
            elif v==7:row[x]=8 if (x,y) in keep else 11
            elif v==4:row[x]=8
    return out,face_protected|hands|arm,erase,(fl,ft,fr,fb)

def convert(im, column, p, pose, name=None):
    cell,hair,source_face=source_hair(im,column)
    out,protected,erase,native_face=native_base(p,pose)
    fl,ft,fr,fb=source_face;nl,nt,nr,nb=native_face
    # The supplied artwork's logical grid is about three source pixels per
    # native pixel. Align to the native forehead/cheek, never the arm span.
    scale=1/3
    sx,sy=source_eye(cell,source_face)
    native_skin,_,_,_=head(p,1,'back',pose)
    nx,ny=eye_anchor(p,native_skin)
    mask={};samples={}
    for x,y in hair:
        q=(round((x-sx)*scale+nx),round((y-sy)*scale+ny))
        if 0<=q[0]<64 and 0<=q[1]<64:
            samples.setdefault(q,[]).append(cell.getpixel((x,y)))
    # Snap to one logical-pixel outline and broad native color clusters.
    for q,colors in samples.items():
        outline=sum(max(c)<65 and c[0]<=c[1]+8 for c in colors)/len(colors)
        light=sum(c[0] for c in colors)/len(colors)
        mask[q]=15 if outline>=.4 else 11 if light>=112 else 7 if light>=80 else 4
    # Close one-cell pinholes left by the presentation sheet's outlines.
    for y in range(1,63):
        for x in range(1,63):
            if (x,y) not in mask and sum(q in mask for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)))>=3:
                mask[x,y]=7
    original=dict(mask)
    for (x,y),v in original.items():
        adjacent=[original.get(q,0) for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))]
        if 0 in adjacent:mask[x,y]=15
        elif v==11 and adjacent.count(11)<2:mask[x,y]=7
    finish(mask,name,pose,out)
    for (x,y),v in mask.items():
        if x>nr and nt+3<y<=nb+2:continue
        if (x,y) not in protected:out[y][x]=v
    return out

def rgb555(rgb):
    r,g,b=rgb;return round(r*31/255)|(round(g*31/255)<<5)|(round(b*31/255)<<10)

def build():
    manifest=json.loads((ROOT/'tools/legends/battle_sheets.json').read_text())
    native=frames(NATIVE_PATH,64,64);blob=bytearray();desc=[]
    for item in manifest:
        src=Image.open(ROOT/item['source']).convert('RGB')
        assert src.size==(1536,1152)
        poses=[convert(src,column,native[pose],pose,item['name']) for pose,column in enumerate(SOURCE_ORDER)]
        offset=len(blob);blob.extend(b''.join(pack(p) for p in poses))
        desc.append(f'    {{.data=sMayBattleBits+{offset}, .size=2048, .relativeFrames=TRUE}},')
        out=Image.new('P',(64,256));out.putpalette(sum((list(c) for c in PALETTE),[])+[0]*(768-48))
        out.putdata([v for p in poses for row in p for v in row]);out.save(ROOT/f'graphics/legends/battle_may/{item["name"]}.png',transparency=0)
    (ROOT/'graphics/legends/battle_may/frames.bin').write_bytes(blob)
    header='// Generated by tools/legends/import_battle_sheets.py.\n'
    header+='static const u8 ALIGNED(4) sMayBattleBits[] = INCBIN_U8("graphics/legends/battle_may/frames.bin");\n'
    header+='static const struct SpriteFrameImage sMayBattleImages[10] = {\n'+'\n'.join(desc)+'\n};\n'
    header+='static const u16 sMayBattleBasePalette[16] = {'+','.join(f'0x{rgb555(c):04X}' for c in PALETTE)+'};\n'
    header+='static const u16 sMayBattleHairRamps[8][3] = {\n'+',\n'.join('    {'+','.join(f'0x{rgb555(c):04X}' for c in ramp)+'}' for ramp in RAMPS)+'\n};\n'
    (ROOT/'src/data/legends/battle_sheets.h').write_text(header)
    print(f'Fitted {len(manifest)} named cuts to 40 native May poses, {len(blob)} bytes')

if __name__=='__main__':build()
