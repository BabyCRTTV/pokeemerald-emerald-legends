"""Compile native grunt uniforms and pose-local player costume action art."""
from pathlib import Path
import json,re,sys
from PIL import Image,ImageDraw
sys.path.insert(0,str(Path(__file__).resolve().parent))
from build_appearance import ROOT,STATES,FILES,frames,skin_components,hand_pixels,ball_pixels,pack,literal_lz

def colors(path):
    p=Image.open(path).getpalette()[:48]
    return [tuple(p[i:i+3]) for i in range(0,48,3)]
def pal555(p):return [((r//8)|((g//8)<<5)|((b//8)<<10)) for r,g,b in p]
def face_of(p):
    gs=skin_components(p)
    return min((g for g in gs if len(g)>30),key=lambda g:min(y for x,y in g))
def back_frame(native,team,gender,pose):
    """Keep the player's four native throwing motions under a grunt uniform."""
    p=[r[:] for r in native];face=face_of(native);hands=hand_pixels(gender,'back',pose);balls=ball_pixels(gender,'back',pose)
    lx=min(x for x,y in face);rx=max(x for x,y in face);ft=min(y for x,y in face);fb=max(y for x,y in face)
    hole={(x,y) for y in range(ft-1,fb+2) for x in range(lx-1,rx+2)}
    protected=hole|hands|balls
    # Native uniform colors: Magma gray/black body and crimson sleeves;
    # Aqua blue pants/shirt with white nautical stripes.
    for y in range(fb+1,64):
        for x,v in enumerate(native[y]):
            if (x,y) in protected or not v:continue
            if v in (5,6,7,8,10,11,12,13,14,9):
                p[y][x]=(8 if v in (6,8,11,13) else 6) if team==0 else (7 if v in (6,8,11,13) else 5)
            elif v in (1,2,3):
                p[y][x]=(12 if v==1 else 13) if team==0 else v
    # Hat/head region: remove the player cap silhouette, author the matching
    # hood or tied bandana around the original face, never around raised hands.
    head={(x,y) for y in range(max(0,ft-23),fb+2) for x in range(64)
          if native[y][x] and (x,y) not in hands|balls}
    hl=max(1,lx-15);hr=min(62,rx+2);top=max(1,ft-15)
    for x,y in head:
        if (x,y) not in hole:p[y][x]=0
    canvas=Image.new('P',(64,64),0);d=ImageDraw.Draw(canvas);cx=(hl+hr)//2
    if team==0:
        d.polygon([(hl+6,top+1),(hr-5,top+3),(hr,ft+1),(hr-2,fb),(hl+7,fb+2),(hl+1,fb-2),(hl,top+10)],fill=12,outline=15)
        d.polygon([(hl+1,top+11),(hl+6,top+2),(cx-3,top+7),(cx-3,fb),(hl+4,fb)],fill=13)
        d.line([(hl+3,fb),(cx-3,fb)],fill=10,width=2)
    else:
        d.polygon([(hl+7,top+3),(hr-4,top+5),(hr,ft+2),(hl+2,ft+2),(hl,top+11)],fill=5,outline=15)
        d.line([(hl+3,ft+1),(hr-2,ft+1)],fill=6,width=2)
        # Native Aqua bandana knot and short tails.
        d.polygon([(hl+3,ft),(hl-3,ft-3),(hl-1,ft+5),(hl+5,ft+3)],fill=5,outline=15)
        d.line([(cx,top+8),(cx+3,top+8)],fill=14,width=1)
    for y in range(64):
        for x in range(64):
            v=canvas.getpixel((x,y))
            if v and (x,y) not in protected:p[y][x]=v
    # White Aqua stripes are independent from the preserved skin/held object.
    if team==1:
        for y in (fb+7,fb+8,fb+13,fb+14):
            if y>=64:continue
            for x,v in enumerate(p[y]):
                if v in (5,6,7) and (x,y) not in protected:p[y][x]=14 if y%2 else 9
    # Flatten the old backpack/sling interior into uniform cloth. Keep only
    # the outer pose outline; grunt costumes do not carry the player backpack.
    for y in range(min(64,fb+3),64):
        for x in range(max(1,cx-7),min(63,cx+8)):
            if (x,y) in protected or not p[y][x]:continue
            if native[y][x] in (4,15) and p[y][x-1] and p[y][x+1]:
                p[y][x]=8 if team==0 else 7
    # Team symbols are placed on the back where the native sling used to be.
    emblem_y=min(58,fb+12);ex=max(20,min(40,cx))
    for dx,dy in ((-2,0),(2,0),(-1,1),(1,1),(0,2)):
        x,y=ex+dx,emblem_y+dy
        if p[y][x] and (x,y) not in protected:p[y][x]=12 if team==0 else 14
    assert all(p[y][x]==native[y][x] for x,y in face|hands|balls)
    return p

def action_frame(native,grunt,team,gender,state,pose,source_colors,target_colors):
    remap={0:0,**{i:min(range(1,16),key=lambda j:sum((source_colors[i][k]-target_colors[j][k])**2 for k in range(3))) for i in range(1,16)}}
    p=[[remap[v] for v in row] for row in native]
    groups=skin_components(native)
    if not groups:return p
    face=max(groups,key=len);fb=max(y for x,y in face);cx=round(sum(x for x,y in face)/len(face))
    w=len(p[0]);direction=1 if min(y for x,y in face)>23 else 2 if max(x for x,y in face)-min(x for x,y in face)<5 else 0
    source=grunt[direction];offset=fb-21;left=max(0,min(w-16,cx-7))
    # Actual native hood/bandana and face pixels, translated to the pose's head.
    for y in range(max(0,fb-15),min(32,fb+1)):
        for x in range(left,min(w,left+16)):p[y][x]=0
    for y in range(22):
        for x,v in enumerate(source[y]):
            if v and 0<=y+offset<32:p[y+offset][x+left]=v
    for y in range(fb+1,min(32,fb+7)):
        for x in range(max(0,cx-4),min(w,cx+5)):
            v=native[y][x]
            if v in (10,11,12,13):p[y][x]=(8 if v in (10,12) else 9) if team==0 else (14 if y in (fb+2,fb+4) else 5 if v in (10,12) else 6)
            elif v in (1,2,3):p[y][x]=v
    return p

def build():
    mapping=json.loads((ROOT/'tools/legends/appearance_frames.json').read_text());ow=bytearray();train=bytearray();h=[];th=[];entries=[];palette=[];tables={}
    for team,name in enumerate(('magma','aqua')):
        palette.append([])
        for gender,g in enumerate(('brendan','may')):
            suffix='m' if gender==0 else 'f';gp=ROOT/f'graphics/object_events/pics/people/team_{name}/{name}_member_{suffix}.png';tp=ROOT/f'graphics/trainers/front_pics/{name}_grunt_{suffix}.png'
            oc=colors(gp);tc=colors(tp);palette[-1].append((pal555(oc),pal555(tc)));grunt=frames(gp,16,32)
            for state,file in zip(STATES,FILES):
                width=16 if state=='Normal' else 32;src=ROOT/f'graphics/object_events/pics/people/{g}/{file}.png';sources=frames(src,width,32)
                if state=='Normal':sources+=frames(src.with_name('running.png'),16,32)
                if state=='Normal':poses=grunt+grunt
                else:poses=[action_frame(f,grunt,team,gender,file,i,colors(src),oc) for i,f in enumerate(sources)]
                symbol=f'sLegendsCostume{team}{gender}{state}';raw=b''.join(pack(f) for f in poses);h.append(f'#define {symbol} (sLegendsCostumeOverworldData + {len(ow)})\n');ow.extend(raw)
                table=mapping[g.title()][state]['table'];idx=list(range(len(sources))) if 'overworld_ascending_frames' in table else [int(v) for v in re.findall(r'overworld_frame\([^,]+,\s*\d+,\s*\d+,\s*(\d+)\)',table)]
                h.append(f'static const struct SpriteFrameImage {symbol}Images[] = {{\n'+''.join(f'    {{.data={symbol}+{i*width*16},.size={width*16}}},\n' for i in idx)+'};\n');tables[team,gender,state]=symbol+'Images'
            front=literal_lz(pack(frames(tp,64,64)[0]));back=b''.join(pack(back_frame(f,team,gender,i)) for i,f in enumerate(frames(ROOT/f'graphics/trainers/back_pics/{g}.png',64,64)))
            fs=f'gLegendsCostume{team}{gender}Front';bs=f'gLegendsCostume{team}{gender}Back';th.append(f'#define {fs} ((const u32 *)(gLegendsCostumeTrainerData + {len(train)}))\n');train.extend(front);th.append(f'#define {bs} (gLegendsCostumeTrainerData + {len(train)})\n');train.extend(back)
            entries.append(f'    [TRAINER_PIC_LEGENDS_COSTUME_{team*2+gender}] = {{.frontPic=TRAINER_FRONT_PIC({fs}, gLegendsTrainerPalettes[{gender}]), .backPic=TRAINER_BACK_PIC(4, {bs}, gLegendsTrainerPalettes[{gender}], sBackAnims_Hoenn)}},\n')
    h.insert(0,f'const u8 ALIGNED(4) sLegendsCostumeOverworldData[{len(ow)}] = INCBIN_U8("graphics/legends/costumes/overworld.bin");\n');th.insert(0,f'const u8 ALIGNED(4) gLegendsCostumeTrainerData[{len(train)}] = INCBIN_U8("graphics/legends/costumes/trainers.bin");\n')
    h.append('static const struct SpriteFrameImage *const sLegendsCostumeImages[2][2][8] = {\n')
    for team in range(2):h.append('    {'+','.join('{'+','.join(tables[team,g,s] for s in STATES)+'}' for g in range(2))+'},\n')
    h.append('};\n')
    for label,index in (('Overworld',0),('Trainer',1)):
        th.append(f'static const u16 sLegendsCostume{label}Palettes[2][2][16] = {{\n')
        for team in range(2):th.append('    {'+','.join('{'+','.join(f'0x{v:04X}' for v in palette[team][g][index])+'}' for g in range(2))+'},\n')
        th.append('};\n')
    directory=ROOT/'graphics/legends/costumes';directory.mkdir(parents=True,exist_ok=True);(directory/'overworld.bin').write_bytes(ow);(directory/'trainers.bin').write_bytes(train)
    (ROOT/'src/data/legends/overworld_costumes.h').write_text(''.join(h))
    # Palettes are shared with the state module without duplicating ROM pixels.
    split=''.join(th).index('static const u16 sLegendsCostumeOverworldPalettes')
    (ROOT/'src/data/legends/trainer_costumes.h').write_text(''.join(th)[:split])
    (ROOT/'src/data/legends/costume_palettes.h').write_text(''.join(th)[split:])
    (ROOT/'src/data/legends/costume_trainers.inc').write_text(''.join(entries))
if __name__=='__main__':build()
