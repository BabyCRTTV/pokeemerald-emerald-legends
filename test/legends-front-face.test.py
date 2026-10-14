"""Execute the integrated C renderer; only the approved front cheeks may change."""
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root/'tools/legends'))
from build_style_layers import front_face_edits
from build_appearance import frames,FILES,STATES

approval=json.loads((root/'tools/legends/front_face_approval.json').read_text())
mapping=json.loads((root/'tools/legends/appearance_frames.json').read_text())
masks={};all_masks=[]
for g,name in enumerate(('Brendan','May')):
    for state,(label,file) in enumerate(zip(STATES,FILES)):
        width=16 if state==0 else 32
        ps=frames(root/f'graphics/object_events/pics/people/{name.lower()}/{file}.png',width,32)
        if state==0:ps+=frames(root/f'graphics/object_events/pics/people/{name.lower()}/running.png',16,32)
        table=mapping[name][label]['table']
        indices=list(range(len(ps))) if 'overworld_ascending_frames' in table else [int(v) for v in re.findall(r'overworld_frame\([^,]+,\s*\d+,\s*\d+,\s*(\d+)\)',table)]
        for pose,native in enumerate(indices):
            points=front_face_edits(ps[native],g,native,file)
            masks[g,state,pose]=points
            all_masks.append([g,state,pose,points])
assert hashlib.sha256(json.dumps(all_masks,separators=(',',':')).encode()).hexdigest()==approval['native_masks_sha256']
for g in range(2):
    assert [list(p) for p in masks[g,0,0]]==approval['standing_edits'][str(g)]
    for pose,dy in ((3,1),(4,1)):
        assert masks[g,0,pose]==[(x,y+dy) for x,y in masks[g,0,0]],(g,pose,'front animation drift')
    # Native running jaws are one row shorter than the standing face.
    # Preserve that anatomy rather than painting the standing mask over it.
    for pose,dy in ((9,2),(12,3),(13,3)):
        assert [list((x,y-dy)) for x,y in masks[g,0,pose]]==approval['running_edits'][str(g)]

path=root/'test/legends-appearance-colors.test.py';ns={'__file__':str(path)}
exec(path.read_text().split('# Artwork preservation:',1)[0],ns)
checked=0;front=0
with tempfile.TemporaryDirectory() as temp:
    olddir=Path(temp)/'old';olddir.mkdir();newdir=Path(temp)/'new';newdir.mkdir()
    _,before=ns['compile_api'](olddir,shade=False)
    _,after=ns['compile_api'](newdir)
    def compare(g,state,pose,**kwargs):
        global checked,front
        _,old,oldpal=before(g=g,state=state,pose=pose,kind=0,**kwargs)
        _,new,newpal=after(g=g,state=state,pose=pose,kind=0,**kwargs)
        assert oldpal==newpal,'global skin/material palette changed'
        allowed=set(masks[g,state,pose])
        changed=set()
        for y,row in enumerate(old):
            for x,value in enumerate(row):
                expected=2 if (x,y) in allowed and value==3 else value
                assert new[y][x]==expected,(g,state,pose,kwargs,x,y,value,new[y][x],expected)
                if new[y][x]!=value:changed.add((x,y))
        assert changed<=allowed
        checked+=1
        front+=bool(changed)
    # Every actual native descriptor, including original hair and unchanged
    # underwater poses; every custom cut and all three outerwear choices.
    for g,state,pose in masks:
        for hair in range(11):
            compare(g,state,pose,h=hair)
        for coat in (1,2):
            compare(g,state,pose,h=2 if g==0 else 6,o=3,coat=coat,scarf=2,shoe=7)
    # The exact accepted standing reference across all five tones / eight
    # hair colors; side/rear comparisons protect shared palette materials.
    for g in range(2):
        for tone in range(5):
            for color in range(8):
                for pose in (0,1,2):compare(g,0,pose,h=2 if g==0 else 6,tone=tone,col=color)
                old=before(g=g,h=2 if g==0 else 6,tone=tone,col=color,kind=1)
                new=after(g=g,h=2 if g==0 else 6,tone=tone,col=color,kind=1)
                assert old[1:]==new[1:],'wardrobe/front portrait changed'
print(f'Approved front-face shading: {checked} integrated native comparisons; {front} front-view results changed; palettes, other pixels/views, portraits and diving preserved')
