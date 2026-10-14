"""Sample supplied four-view sheets onto an ear/eye-aligned native pixel grid.

The checked-in indexed head atlas is the reproducible authoring input. Original
high-resolution references are only needed when explicitly reimporting artwork.
"""
import argparse, hashlib, json
from pathlib import Path
import numpy as np
from PIL import Image
from build_appearance import ROOT

# Front eye boxes, and the left-facing eye center/top. Native front eyes are
# three cells apart and two cells tall; the side eye occupies native column 5.
SHEETS = (
    ('Crew Cut', '10-185669.png', ((174,658,21,45),(240,659,21,44)), (931.5,658)),
    ('Side Part', '06-185675.png', ((179,712,21,42),(246,712,21,42)), (906.5,711)),
    ('Spiky', '03-185672.png', ((162,705,20,43),(234,705,20,43)), (887.5,705)),
    ('Side Sweep', '07-185676.png', ((163,699,21,43),(229,699,20,42)), (910.5,702)),
    ('Tousled', '05-185674.png', ((168,687,19,41),(230,687,20,42)), (905.5,687)),
    ('Quiff', '09-185678.png', ((161,683,21,44),(228,683,21,44)), (910,676)),
    ('Shag', '01-185670.png', ((166,719,20,42),(233,719,21,43)), (891.5,711)),
    ('Curls', '08-185677.png', ((162,693,21,41),(226,693,20,41)), (913,690)),
    ('Man Bun', '04-185673.png', ((166,686,21,44),(234,686,21,44)), (880,686)),
    ('Undercut', '02-185671.png', ((175,698,18,38),(236,698,18,38)), (904.5,699)),
)

# Semantic slots: skin 1/2/3, hair midtone 4, highlight 7, shadow 8, outline 15.
COLORS = [(178,167,236),(255,213,180),(255,197,148),(222,148,115),
          (139,90,57),(16,32,57),(41,57,98),(189,132,82),
          (65,41,32),(222,230,238),(115,205,115),(74,148,82),
          (255,98,90),(197,65,65),(255,255,255),(0,0,0)]

def material(rgb):
    r,g,b = map(float,rgb)
    if b > r + 12 and b > g + 12 and b > 130:
        return 0
    if r > 185 and g / max(r,1) > .75 and g-b > 18:
        return 1 if r > 235 else 2 if r > 215 else 3
    if max(r,g,b) < 35:
        return 15
    if b > r + 6 and max(r,g,b) < 135:
        return 5
    if r > g + 7 and r > b + 12:
        light = .299*r + .587*g + .114*b
        return 7 if light >= 119 else 4 if light >= 56 else 8
    return 0

def import_sheets(directory):
    atlas = Image.new('P',(48,320))
    atlas.putpalette([v for rgb in COLORS for v in rgb]+[0]*(768-48))
    records = []
    for style,(name,filename,eyes,left_eye) in enumerate(SHEETS):
        path=directory/filename
        image=Image.open(path).convert('RGB');a=np.asarray(image,dtype=float)
        first,second=eyes
        centers=[x+(w-1)/2 for x,y,w,h in eyes]
        sx=(centers[1]-centers[0])/3
        sy=sum(h for x,y,w,h in eyes)/4
        eye_top=sum(y for x,y,w,h in eyes)/2
        front_center=sum(centers)/2
        # Only the backpack is green in the reference's rear body. Its center
        # registers the head independently of asymmetric hair overhangs.
        body=a[int(eye_top+sy):1050,384:768]
        red,green,blue=body[:,:,0],body[:,:,1],body[:,:,2]
        yy,xx=np.where((green>red+25)&(green>blue+15)&(green>90))
        assert len(xx)>100,(name,'backpack landmark')
        back_center=(float(xx.min())+float(xx.max()))/2+384
        anchors=((front_center-7.5*sx,eye_top),
                 (back_center-7.5*sx,eye_top),
                 (left_eye[0]-5*sx,left_eye[1]))
        for view,(zero_x,top_y) in enumerate(anchors):
            # Rows above 8 can sample the enlarged Front/Back label glyphs;
            # the highest genuine supplied hair/bun pixels begin below them.
            for y in range(8,22):
                for x in range(16):
                    px=round(zero_x+x*sx);py=round(top_y+(y-19+.5)*sy)
                    region=a[max(0,py-2):py+3,max(0,px-2):px+3]
                    rgb=np.median(region,axis=(0,1))
                    value=material(rgb)
                    if style==9 and view==2 and y>=16 and x>=8:
                        red,green,blue=rgb
                        if 70<red<185 and green/red>.77 and red>blue+6:
                            value=3 # Shaved temple follows the selected skin tone.
                    atlas.putpixel((view*16+x,style*32+y),value)
        records.append({'id':style+1,'name':name,'source_name':filename.split('-',1)[1],
                        'source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                        'grid_step':[sx,sy],'anchors':anchors})
    # Keep the separately approved Side Part corrections when reimporting
    # the original high-resolution source sheets. All other cells stay native.
    approval=json.loads((ROOT/'tools/legends/side_part_approval.json').read_text())
    for view,edits in approval['atlas_overrides'].items():
        dx=0 if view=='front' else 32
        for x,y,value in edits:atlas.putpixel((dx+x,32+y),value)
    target=ROOT/'graphics/legends/male_overworld'
    target.mkdir(parents=True,exist_ok=True)
    atlas.save(target/'heads.png',transparency=0)
    (ROOT/'tools/legends/male_overworld_sheets.json').write_text(json.dumps(records,indent=2)+'\n')
    print('Imported 10 male cuts, 30 native head views; east uses native west mirroring')

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_directory',type=Path)
    import_sheets(parser.parse_args().source_directory)
