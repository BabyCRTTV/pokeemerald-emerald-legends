"""Fit supplied male hair to Brendan's native 64x64 throw poses.

Only hair is fitted. Native face, hands, clothing and pose geometry supply
all anatomy. The checked-in bank is static 4bpp, refreshed by wardrobe IDs.
"""
import json
from PIL import Image
from build_appearance import ROOT,frames,pack
from build_style_layers import head
from import_battle_sheets import groups,bounds,neighbors,source_hair,source_eye,eye_anchor,rgb555,RAMPS,COLUMNS,ROWS,SOURCE_ORDER

NATIVE_PATH=ROOT/'graphics/trainers/back_pics/brendan.png'
PALETTE=[tuple(Image.open(NATIVE_PATH).getpalette()[i*3:i*3+3]) for i in range(16)]
# Three independent hair materials, without recoloring green backpack/cuffs.
# Consolidate navy's two darkest shades and make grey strap highlights white.
HAIR_SLOTS=(4,7,9)
for i,c in zip(HAIR_SLOTS,RAMPS[0]):PALETTE[i]=c
COLLAR_RECTS=((31,37,45,43),(36,38,50,45),(24,41,41,51),(34,36,50,43))
HAND_RECTS=(((0,34,17,51),(51,45,63,58)),((0,23,18,42),(49,56,63,63)),((44,20,63,38),),())
# The pale-blue edge of Brendan's white cap touches the raised glove, but
# is not finger/cuff anatomy. A connected-silhouette check cannot detect it.
CAP_TIP_CELLS={(18,26),(17,27),(16,28),(15,29),(16,30),(17,30),(18,30)}

def native_base(p,pose):
    face,box,_,_=head(p,0,'back',pose)
    fl,ft,fr,fb=bounds(face)
    white={(x,y) for y in range(ft,fb+1) for x in range(fl,fr+1) if p[y][x]==14}
    eye=white|{q for q in neighbors(neighbors(white)) if p[q[1]][q[0]] in (8,14,15)}
    features=face|eye
    facial=features|{q for q in neighbors(features) if p[q[1]][q[0]] in (3,4,8,15)}
    hands=set()
    for l,t,r,b in HAND_RECTS[pose]:
        hands|={(x,y) for y in range(t,b+1) for x in range(l,r+1) if p[y][x] and p[y][x] not in (9,14)}
    if pose==1:
        hands-=CAP_TIP_CELLS
    # The release cuff and brim share green. Select the cuff's component by
    # the red glove rather than retaining the headwear inside a broad box.
    if pose==2:
        seeds={q for q in hands if p[q[1]][q[0]] in (12,13)}
        area={q for q in hands if q[0]>=46 or q[1]>=29}
        connected=set(seeds);queue=list(seeds)
        for x,y in queue:
            for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if q in area and q not in connected:connected.add(q);queue.append(q)
        hands=connected
    l,t,r,b=COLLAR_RECTS[pose]
    collar={(x,y) for y in range(t,b+1) for x in range(l,r+1) if p[y][x] in (5,6,7,8,12,13,15)}
    out=[row[:] for row in p];l,t,r,b=box
    protected=facial|hands|collar
    for y in range(t,b+1):
        for x in range(l,r+1):
            if (x,y) not in protected:out[y][x]=0
    for y,row in enumerate(out):
        for x,v in enumerate(row):
            if v==4:row[x]=3 # warm face/hand contours follow the skin shadow
            elif v==7:row[x]=8
            elif v==9:row[x]=14
    return out,protected,(fl,ft,fr,fb)

def hair_mask(im,column,p,pose):
    cell,hair,sface=source_hair(im,column);sx,sy=source_eye(cell,sface)
    nx,ny=eye_anchor(p,head(p,0,'back',pose)[0]);samples={}
    for x,y in hair:
        q=(round((x-sx)/3+nx),round((y-sy)/3+ny))
        if 0<=q[0]<64 and 0<=q[1]<64:samples.setdefault(q,[]).append(cell.getpixel((x,y)))
    mask={}
    for q,colors in samples.items():
        dark=sum(max(c)<65 and c[0]<=c[1]+8 for c in colors)/len(colors)
        light=sum(c[0] for c in colors)/len(colors)
        mask[q]=15 if dark>=.4 else 9 if light>=112 else 7 if light>=80 else 4
    for y in range(1,63):
        for x in range(1,63):
            if (x,y) not in mask and sum(q in mask for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)))>=3:mask[x,y]=7
    return mask,(nx,ny)

def curls_cap(im,column,p,pose):
    """Fit the reference's small white/green cap above its exposed ringlets."""
    cell,_,face=source_hair(im,column);sx,sy=source_eye(cell,face)
    nx,ny=eye_anchor(p,head(p,0,'back',pose)[0]);core={}
    # The face landmark separates cap greens/whites from the backpack/eye.
    for y in range(face[1]+4):
        for x in range(cell.width):
            r,g,b=cell.getpixel((x,y))
            if min(r,g,b)>120 and max(r,g,b)-min(r,g,b)<50:
                core[x,y]=14
            elif 45<g<225 and g>r*1.08 and g>b*1.2 and b<135:
                core[x,y]=10 if g>145 else 11
    pieces=groups(set(core))
    cap=max((part for part in pieces if any(core[q]==14 for q in part)),key=len)
    # Join green brim components within three source pixels of the white cap.
    for part in pieces:
        if any((x+dx,y+dy) in cap for x,y in part for dx,dy in ((-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2),(-2,2),(2,-2))):
            cap.update(part)
    shades={q:core[q] for q in cap}
    for x,y in list(cap):
        for dx,dy in ((-2,0),(2,0),(0,-2),(0,2),(-1,-1),(1,1),(-1,1),(1,-1)):
            q=x+dx,y+dy
            if 0<=q[0]<cell.width and 0<=q[1]<face[1]+4 and q not in core:
                r,g,b=cell.getpixel(q)
                if max(r,g,b)<100 and r+g+b<210:shades[q]=15
    samples={}
    for (x,y),v in shades.items():
        q=round((x-sx)/3+nx),round((y-sy)/3+ny)
        if 0<=q[0]<64 and 0<=q[1]<64:samples.setdefault(q,[]).append(v)
    result={}
    for q,values in samples.items():
        # White and fixed green cap colors never occupy a hair material slot.
        result[q]=15 if values.count(15)/len(values)>=.45 else max((14,10,11),key=lambda v:values.count(v))
    for y in range(1,63):
        for x in range(1,63):
            if (x,y) not in result and sum(q in result for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)))>=3:
                result[x,y]=14
    return result

def convert(im,column,p,pose,name):
    out,protected,face=native_base(p,pose);mask,anchor=hair_mask(im,column,p,pose)
    original=dict(mask)
    for (x,y),v in original.items():
        adjacent=[original.get(q,0) for q in ((x-1,y),(x+1,y),(x,y-1),(x,y+1))]
        if 0 in adjacent:mask[x,y]=15
        elif v==15:mask[x,y]=4 # internal strands use hair shadow, not black holes
        elif v==9 and adjacent.count(9)<2:mask[x,y]=7
    nl,nt,nr,nb=face
    for (x,y),v in mask.items():
        if x>nr and nt+3<y<=nb+2:continue
        if (x,y) not in protected:out[y][x]=v
    if name=='curls':
        for (x,y),v in curls_cap(im,column,p,pose).items():
            if (x,y) not in protected:out[y][x]=v
    return out

def build():
    manifest=json.loads((ROOT/'tools/legends/battle_brendan_sheets.json').read_text())
    native=frames(NATIVE_PATH,64,64);blob=bytearray();desc=[]
    for item in manifest:
        src=Image.open(ROOT/item['source']).convert('RGB');assert src.size==(1536,1152)
        poses=[convert(src,column,native[pose],pose,item['name']) for pose,column in enumerate(SOURCE_ORDER)]
        offset=len(blob);blob.extend(b''.join(pack(p) for p in poses));desc.append(f'    {{.data=sBrendanBattleBits+{offset}, .size=2048, .relativeFrames=TRUE}},')
        im=Image.new('P',(64,256));im.putpalette(sum((list(c) for c in PALETTE),[])+[0]*(768-48));im.putdata([v for p in poses for row in p for v in row]);im.save(ROOT/f'graphics/legends/battle_brendan/{item["name"]}.png',transparency=0)
    (ROOT/'graphics/legends/battle_brendan/frames.bin').write_bytes(blob)
    header='// Generated by tools/legends/import_brendan_battle_sheets.py.\n'
    header+='static const u8 ALIGNED(4) sBrendanBattleBits[] = INCBIN_U8("graphics/legends/battle_brendan/frames.bin");\n'
    header+='static const struct SpriteFrameImage sBrendanBattleImages[10] = {\n'+'\n'.join(desc)+'\n};\n'
    header+='static const u16 sBrendanBattleBasePalette[16] = {'+','.join(f'0x{rgb555(c):04X}' for c in PALETTE)+'};\n'
    (ROOT/'src/data/legends/battle_brendan_sheets.h').write_text(header)
    print(f'Fitted {len(manifest)} male cuts to 40 native Brendan poses, {len(blob)} bytes')

if __name__=='__main__':build()
