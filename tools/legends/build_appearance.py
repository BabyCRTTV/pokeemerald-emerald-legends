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

def outfit_frame(pixels, gender, outfit, kind="overworld", pose=0):
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
        # Separate jacket/jersey material from gloves and hair.
        for y in range(face_bottom+1,h):
            for x in range(w):
                v = pixels[y][x]
                if abs(x-center) <= 3 and y <= face_bottom+5 and v in (12,13):
                    result[y][x] = 10 if v == 12 else 11
                if outfit == 1 and abs(x-center) <= 3 and face_bottom+3 <= y <= face_bottom+5 and v in (5,6):
                    result[y][x] = 10 if v == 5 else 11
                if outfit == 2 and y == face_bottom+3 and abs(x-center)<=3 and result[y][x] in (10,11):
                    result[y][x] = 9
                if outfit == 2 and gender == 0 and face_bottom+5 <= y <= face_bottom+6 and abs(x-center)<=4 and v in (5,6,7,8):
                    result[y][x] = 2 if v in (5,6) else 3
        if outfit == 1:
            for group in groups:
                if group == face: continue
                for x,y in group:
                    # Cover bare legs with trail trousers; leave feet intact.
                    if y >= face_bottom+5 and abs(x-center)<=4:
                        result[y][x] = 5 if pixels[y][x]==1 else 6
                    # Jacket shoulders, preserving gloved hands.
                    elif face_bottom < y <= face_bottom+2:
                        result[y][x] = 10 if pixels[y][x]==1 else 11
    else:
        # Native 64px trainer poses: jacket/jersey panels stay below the head.
        face = min((c for c in groups if len(c)>30),key=lambda c:min(y for x,y in c))
        face_bottom = max(y for x,y in face)
        if kind == "front":
            body_top,body_bottom = (23,39) if gender==0 else (22,37)
        else:
            body_top,body_bottom = (38,63)
        for y in range(body_top,body_bottom+1):
            for x in range(w):
                v = pixels[y][x]
                if (x,y) in face or (gender==1 and v in (7,8)):
                    continue
                clothing = v in (10,11) or (v in (12,13) and 24 <= x <= 42)
                if clothing or (kind=="back" and 20 < x < 50 and y>face_bottom+3 and v in (5,6,7,8)):
                    result[y][x] = 10 if v in (5,7,10,12) else 11
                if outfit == 2 and y in (body_top+6,body_top+7) and result[y][x] in (10,11):
                    result[y][x] = 9
        if outfit == 1:
            for group in groups:
                if group == face or len(group)<6:
                    continue
                low=min(y for x,y in group)
                if kind=="front" and gender==1 and low>=39:
                    for x,y in group:
                        result[y][x]=5 if pixels[y][x]==1 else 6
                elif low>=(24 if kind=="front" else 36):
                    left=min(x for x,y in group);right=max(x for x,y in group)
                    mid=(left+right)/2
                    for x,y in group:
                        # The half nearest the torso is a sleeve; distal hands remain skin.
                        if (mid<32 and x>=mid) or (mid>=32 and x<=mid):
                            result[y][x]=10 if pixels[y][x]==1 else 11
        elif kind=="front" and gender==0:
            for y in range(46,55):
                for x in range(16,43):
                    if pixels[y][x] in (5,6,7,8):
                        result[y][x]=2 if pixels[y][x] in (5,6) else 3
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
        for outfit,label in ((1,"Trail"),(2,"Sport")):
            for state,file in zip(STATES,FILES):
                width=16 if state=="Normal" else 32
                sources=frames(ROOT/f"graphics/object_events/pics/people/{gender.lower()}/{file}.png",width,32)
                if state=="Normal":sources+=frames(ROOT/f"graphics/object_events/pics/people/{gender.lower()}/running.png",16,32)
                modified=[outfit_frame(f,g,outfit) for f in sources]
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
    ow.append("static const struct SpriteFrameImage *const sLegendsOutfitImages[2][2][8] = {\n")
    for gender in ("Brendan","May"):
        ow.append("    {\n")
        for label in ("Trail","Sport"):
            ow.append("        {"+",".join(f"sLegends{gender}{label}{state}Images" for state in STATES)+"},\n")
        ow.append("    },\n")
    ow.append("};\n")
    (ROOT/"src/data/legends/overworld_outfits.h").write_text("".join(ow))
    (ROOT/"src/data/legends/trainer_outfits.h").write_text("".join(trainer))
    (ROOT/"tools/legends/appearance_asset_manifest.json").write_text(json.dumps(counts,indent=2)+"\n")

if __name__=="__main__":build()
