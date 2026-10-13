"""Fit supplied hairstyles to Emerald's native May battle frames.

The presentation sheets supply only hair. Native body/face/hand geometry and
all four throw poses are retained; no complete trainer image is scaled down.
The resulting static sheets use native 4bpp layout and independent skin and
hair palette slots. Nothing is composited or inferred during battle.
"""
import json
from PIL import Image
from build_appearance import ROOT, pack, frames
from build_style_layers import head, coat_hands, BACK_FRONT_LOCK_RECTS

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

def native_base(p, pose):
    """Remove native bandana/hair while keeping the exact face and body grid."""
    face,box,_,_=head(p,1,'back',pose)
    fl,ft,fr,fb=bounds(face)
    protected={(x,y) for y,row in enumerate(p) for x,v in enumerate(row) if v in (1,2,3,12,13)}
    # The eye, nose, mouth, ear and face contour remain native. Glove/hand
    # protection is pose-specific because the casting arm crosses the head.
    face_protected={(x,y) for y in range(ft,fb+1) for x in range(fl,fr+1)
                    if p[y][x] not in (0,10,11)}
    protected.update(face_protected)
    protected.update(coat_hands(1,'back',pose))
    erase=set()
    for rect in (box,BACK_FRONT_LOCK_RECTS[pose]):
        l,t,r,b=rect
        for y in range(t,b+1):
            for x in range(l,r+1):
                if (x,y) not in protected and (rect==box or p[y][x] in (4,7,8,15)):
                    erase.add((x,y))
    # The old nape has two dark rows below the face envelope. Clear its
    # outer sweep while keeping the connected native neck/collar in place.
    for y in range(fb+1,min(64,fb+4)):
        for x in range(max(0,fl-15),max(0,fl-3)):
            if (x,y) not in protected and p[y][x] in (4,7,8,15):erase.add((x,y))
    out=[row[:] for row in p]
    for x,y in erase:out[y][x]=0
    for y,row in enumerate(out):
        for x,v in enumerate(row):
            if v==11:row[x]=10
            elif v==7:row[x]=11
            elif v==4:row[x]=7 if (x,y) in face_protected else 8
    return out,face_protected|coat_hands(1,'back',pose),erase,(fl,ft,fr,fb)

def convert(im, column, p, pose):
    cell,hair,source_face=source_hair(im,column)
    out,protected,erase,native_face=native_base(p,pose)
    fl,ft,fr,fb=source_face;nl,nt,nr,nb=native_face
    # The supplied artwork's logical grid is about three source pixels per
    # native pixel. Align to the native forehead/cheek, never the arm span.
    scale=1/3
    mask={};samples={}
    for x,y in hair:
        q=(round((x-fr)*scale+nr),round((y-ft)*scale+nt))
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
        poses=[convert(src,column,native[pose],pose) for pose,column in enumerate(SOURCE_ORDER)]
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
