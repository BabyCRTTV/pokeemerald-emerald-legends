"""Build repo-native 4bpp outfit art from the native pose sheets.

The edited clothing masks retain native heads, hands, outlines and animation
geometry. Generated C assets are checked in; Pillow is only an authoring tool.
"""
from pathlib import Path
import json, re, struct
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
STATES = ["Normal","MachBike","AcroBike","Surfing","Underwater","FieldMove","Fishing","Watering"]
FILES = ["walking","mach_bike","acro_bike","surfing","underwater","field_move","fishing","watering"]

def skin_components(pixels):
    remaining = {(x,y) for y,row in enumerate(pixels) for x,v in enumerate(row) if v in (1,2,3)}
    groups = []
    while remaining:
        seed = remaining.pop(); group = {seed}; queue = [seed]
        while queue:
            x,y = queue.pop()
            for p in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if p in remaining:
                    remaining.remove(p);group.add(p);queue.append(p)
        groups.append(group)
    return groups

# Rectangles are pose-local, inclusive, and deliberately exclude held Poké Balls.
# Keep outlines; replace glove/cuff interiors with the existing three skin slots.
HAND_RECTS = {
    (0,"front"): [[(15,33,20,38),(42,31,46,34)]],
    (1,"front"): [[(9,30,15,34),(39,35,45,38)]],
    (0,"back"): [
        [(0,36,12,56)], [(0,24,17,40)], [(43,21,63,37)], [],
    ],
    (1,"back"): [
        [(0,39,14,56),(43,43,50,52)],
        [(0,25,17,43),(46,54,56,63)],
        [(41,25,58,37),(5,50,15,63)], [],
    ],
}

BALL_RECTS = {
    (0,"front",0): [(10,36,14,42),(45,26,50,30)],
    (1,"front",0): [(9,26,14,29)],
    (0,"back",0): [(44,51,54,58)],
}

def ball_pixels(gender,kind,pose):
    return {(x,y) for x0,y0,x1,y1 in BALL_RECTS.get((gender,kind,pose),[]) for y in range(y0,y1+1) for x in range(x0,x1+1)}

def hand_pixels(gender,kind,pose):
    rects = HAND_RECTS[(gender,kind)][pose]
    return {(x,y) for x0,y0,x1,y1 in rects for y in range(y0,y1+1) for x in range(x0,x1+1)}

def outfit_frame(pixels, gender, outfit, kind="overworld", pose=0, state="walking"):
    result = [row[:] for row in pixels]
    if outfit == 0:
        return result
    h,w = len(pixels),len(pixels[0])
    groups = skin_components(pixels)
    if not groups:
        return result
    if kind == "overworld":
        face = max(groups,key=len)
        face_bottom = max(y for x,y in face)
        center = sum(x for x,y in face)/len(face)
        for y in range(face_bottom+1,h):
            for x in range(w):
                v=pixels[y][x]
                if abs(x-center)<=3 and y<=face_bottom+5 and v in (12,13):
                    result[y][x]=10 if v==12 else 11
                if outfit==1 and abs(x-center)<=3 and face_bottom+3<=y<=face_bottom+5 and v in (5,6):
                    result[y][x]=10 if v==5 else 11
                if outfit==2 and y==face_bottom+3 and abs(x-center)<=3 and result[y][x] in (10,11):
                    result[y][x]=9
                if outfit==2 and gender==0 and face_bottom+5<=y<=face_bottom+6 and abs(x-center)<=4 and v in (5,6,7,8):
                    result[y][x]=2 if v in (5,6) else 3
                # Tiny hands beside the torso, avoiding feet, hair and red balls.
                if 3<abs(x-center)<=6 and face_bottom+1<=y<=face_bottom+4 and v in (5,6,9,10,11,12,13,14):
                    result[y][x]=1 if v in (9,14) else (2 if v in (5,10,12) else 3)
        if outfit==1:
            for group in groups:
                if group==face:continue
                for x,y in group:
                    if y>=face_bottom+5 and abs(x-center)<=4:
                        result[y][x]=5 if pixels[y][x]==1 else 6
                    elif face_bottom<y<=face_bottom+2:
                        result[y][x]=10 if pixels[y][x]==1 else 11
    else:
        face=min((c for c in groups if len(c)>30),key=lambda c:min(y for x,y in c))
        face_bottom=max(y for x,y in face)
        face_left=min(x for x,y in face)
        hands=hand_pixels(gender,kind,pose)
        balls=ball_pixels(gender,kind,pose)
        # May's mouth/chin includes red pixels: start below the entire head.
        top,bottom=((25,39) if gender==1 else (24,39)) if kind=="front" else (38,63)
        shirt_top = min((y for y in range(top,bottom+1) for x in range(w) if pixels[y][x] in (12,13) and y > face_bottom+1), default=top)
        stripe = (shirt_top+8 if kind=="back" else top+6)
        for y in range(top,bottom+1):
            for x in range(w):
                v=pixels[y][x]
                if (x,y) in face or (x,y) in hands or (x,y) in balls or (gender==1 and v in (7,8)):
                    continue
                if kind=="back" and y<=face_bottom+1 and x>=face_left-10 and v in (5,6,7,8):
                    continue # dark hair, headband and outlines beside the face
                if v in (12,13) and (kind=="back" or 23<=x<=37):
                    result[y][x]=10 if v==12 else 11
                elif gender==0 and v in (5,6,7,8) and ((kind=="back" and x>=14) or (kind=="front" and 20<=x<=42)):
                    result[y][x]=10 if v in (5,7) else 11
                elif v in (10,11):
                    # Backpack/sling stays navy, separate from the shirt/jacket.
                    result[y][x]=5 if v==10 else 6
                if outfit==2 and y in (stripe,stripe+1) and result[y][x] in (10,11):
                    result[y][x]=9
        if outfit==1:
            for group in groups:
                if group==face or len(group)<6:continue
                low=min(y for x,y in group)
                if kind=="front" and gender==1 and low>=39:
                    for x,y in group:result[y][x]=5 if pixels[y][x]==1 else 6
                elif low>=(24 if kind=="front" else 36):
                    mid=(min(x for x,y in group)+max(x for x,y in group))/2
                    for x,y in group:
                        if (x,y) not in hands and (x,y) not in balls and ((mid<32 and x>=mid) or (mid>=32 and x<=mid)):
                            result[y][x]=10 if pixels[y][x]==1 else 11
        elif outfit==2 and kind=="front" and gender==0:
            for y in range(46,55):
                for x in range(16,43):
                    if pixels[y][x] in (5,6,7,8):result[y][x]=2 if pixels[y][x] in (5,6) else 3
        for x,y in hands - balls:
            v=pixels[y][x]
            if (x,y) not in face and v not in (0,1,2,3,4,15):
                result[y][x]=1 if v in (9,14) else (2 if v in (5,7,10,12) else 3)
    if outfit == 4:
        # A cream scarf collar and short tail, confined to existing shirt pixels.
        # Pose-derived placement keeps it coherent through turns and throws.
        collar = face_bottom + 1 if kind == "overworld" else max(face_bottom + 2, shirt_top)
        center_x = round(sum(x for x,y in face) / len(face)) if kind == "overworld" else 30
        depth = 3 if kind == "overworld" else 7
        for y in range(collar, min(collar + depth, h)):
            for x in range(w):
                if result[y][x] not in (10,11):
                    continue
                if kind != "overworld" and ((x,y) in face or (x,y) in hands or (x,y) in balls):
                    continue
                collar_pixel = y <= collar + (0 if kind == "overworld" else 1)
                tail_pixel = center_x <= x <= center_x + (0 if kind == "overworld" else 1)
                if collar_pixel or tail_pixel:
                    result[y][x] = 9 if x % 2 == 0 else 14
    assert all((pixels[y][x]==0)==(result[y][x]==0) for y in range(h) for x in range(w))
    return result

def frames(path,width,height):
    im=Image.open(path)
    return [[[im.getpixel((ox+x,oy+y)) for x in range(width)] for y in range(height)]
            for oy in range(0,im.height,height) for ox in range(0,im.width,width)]

def pack(frame):
    h,w=len(frame),len(frame[0]);out=bytearray()
    for ty in range(0,h,8):
        for tx in range(0,w,8):
            for y in range(8):
                for x in range(0,8,2):
                    out.append(frame[ty+y][tx+x] | frame[ty+y][tx+x+1]<<4)
    return bytes(out)

def literal_lz(data):
    out=bytearray(bytes([0x10])+len(data).to_bytes(3,"little"))
    for i in range(0,len(data),8): out.extend(b"\0"+data[i:i+8])
    out.extend(bytes((-len(out))%4));return bytes(out)

def c_bytes(name,data,words=False):
    if words:
        data += bytes((-len(data))%4)
        values=[f"0x{v:08X}" for v, in struct.iter_unpack("<I",data)]
        type_="u32"
    else:
        values=[f"0x{v:02X}" for v in data];type_="u8 ALIGNED(4)"
    return f"const {type_} {name}[] = {{\n"+ "\n".join("    "+",".join(values[i:i+16])+"," for i in range(0,len(values),16))+"\n};\n"

def build():
    mapping=json.loads((ROOT/"tools/legends/appearance_frames.json").read_text())
    ow=["// Generated by tools/legends/build_appearance.py.\n"]
    trainer=["// Generated by tools/legends/build_appearance.py.\n"]
    gallery=[];counts={}
    for g,gender in enumerate(("Brendan","May")):
        for outfit,label in ((1,"Trail"),(2,"Sport"),(3,"Yellow"),(4,"Lavender")):
            for state,file in zip(STATES,FILES):
                width=16 if state=="Normal" else 32
                sources=frames(ROOT/f"graphics/object_events/pics/people/{gender.lower()}/{file}.png",width,32)
                if state=="Normal":sources+=frames(ROOT/f"graphics/object_events/pics/people/{gender.lower()}/running.png",16,32)
                modified=[outfit_frame(f,g,outfit,pose=i,state=file) for i,f in enumerate(sources)]
                raw=b"".join(pack(f) for f in modified)
                name=f"sLegends{gender}{label}{state}"
                ow.append(c_bytes(name,raw))
                table=mapping[gender][state]["table"]
                if "overworld_ascending_frames" in table:indices=range(len(sources))
                else:indices=[int(v) for v in re.findall(r"overworld_frame\([^,]+,\s*\d+,\s*\d+,\s*(\d+)\)",table)]
                assert indices and max(indices)<len(sources)
                ow.append(f"static const struct SpriteFrameImage {name}Images[] = {{\n"+
                          "\n".join(f"    {{.data={name}+{i*width*16},.size={width*16}}}," for i in indices)+"\n};\n")
                counts[name]={"frames":len(sources),"image_indices":list(indices),"bytes":len(raw)}
                if state=="Normal":gallery.append((g,outfit,modified[0],Image.open(ROOT/f"graphics/object_events/pics/people/{gender.lower()}/walking.png").getpalette()))
            for kind,directory in (("Front","front_pics"),("Back","back_pics")):
                sources=frames(ROOT/f"graphics/trainers/{directory}/{gender.lower()}.png",64,64)
                modified=[outfit_frame(f,g,outfit,kind.lower(),i) for i,f in enumerate(sources)]
                raw=b"".join(pack(f) for f in modified)
                name=f"gLegends{gender}{label}{kind}"
                trainer.append(c_bytes(name,literal_lz(raw) if kind=="Front" else raw,kind=="Front"))
                counts[name]={"frames":len(sources),"bytes":len(raw)}
                if kind=="Front":gallery.append((g,outfit,modified[0],Image.open(ROOT/f"graphics/trainers/{directory}/{gender.lower()}.png").getpalette()))
    ow.append("static const struct SpriteFrameImage *const sLegendsOutfitImages[2][4][8] = {\n")
    for gender in ("Brendan","May"):
        ow.append("    {\n")
        for label in ("Trail","Sport","Yellow","Lavender"):
            ow.append("        {"+",".join(f"sLegends{gender}{label}{state}Images" for state in STATES)+"},\n")
        ow.append("    },\n")
    ow.append("};\n")
    (ROOT/"src/data/legends/overworld_outfits.h").write_text("".join(ow))
    (ROOT/"src/data/legends/trainer_outfits.h").write_text("".join(trainer))
    (ROOT/"tools/legends/appearance_asset_manifest.json").write_text(json.dumps(counts,indent=2)+"\n")

if __name__=="__main__":build()
