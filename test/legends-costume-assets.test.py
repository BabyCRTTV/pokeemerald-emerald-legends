"""Native grunt fidelity, player pose preservation and reproducible costume packs."""
from pathlib import Path
import sys,re
root=Path(__file__).resolve().parents[1];sys.path.insert(0,str(root/'tools/legends'))
import build_costumes as art
from build_appearance import outfit_frame
paths=[root/p for p in ('graphics/legends/costumes/overworld.bin','graphics/legends/costumes/trainers.bin','src/data/legends/overworld_costumes.h','src/data/legends/trainer_costumes.h','src/data/legends/costume_palettes.h','src/data/legends/costume_trainers.inc')]
before=[p.read_bytes() for p in paths];art.build();assert before==[p.read_bytes() for p in paths]
ow=paths[0].read_bytes();train=paths[1].read_bytes();table=paths[2].read_text();trainer=paths[3].read_text()
for t,name in enumerate(('magma','aqua')):
 for g,player in enumerate(('brendan','may')):
  suffix='m' if g==0 else 'f';gp=root/f'graphics/object_events/pics/people/team_{name}/{name}_member_{suffix}.png';fp=root/f'graphics/trainers/front_pics/{name}_grunt_{suffix}.png'
  native=b''.join(art.pack(f) for f in art.frames(gp,16,32))
  offset=int(re.search(rf'#define sLegendsCostume{t}{g}Normal .* \+ (\d+)',table)[1])
  assert ow[offset:offset+len(native)*2]==native*2,'Exact native walking/run frame art'
  native_front=art.literal_lz(art.pack(art.frames(fp,64,64)[0]))
  offset=int(re.search(rf'#define gLegendsCostume{t}{g}Front .* \+ (\d+)',trainer)[1])
  assert train[offset:offset+len(native_front)]==native_front,'Exact native trainer portrait/Trainer Card'
  for i,f in enumerate(art.frames(root/f'graphics/trainers/back_pics/{player}.png',64,64)):
   result=art.back_frame(f,t,g,i);assert len(art.pack(result))==2048
   for x,y in art.face_of(f)|art.hand_pixels(g,'back',i)|art.ball_pixels(g,'back',i):assert result[y][x]==f[y][x]
  for state,file in zip(art.STATES,art.FILES):
   if state in ('Normal','Underwater'):continue
   p=root/f'graphics/object_events/pics/people/{player}/{file}.png'
   for i,f in enumerate(art.frames(p,32,32)):
    result=art.action_frame(f,art.frames(gp,16,32),t,g,file,i,art.colors(p),art.colors(gp))
    assert len(art.pack(result))==512 and all(0<=v<16 for row in result for v in row)
# Sport shorts retain cloth above knees, with explicit light hem stripes.
f=art.frames(root/'graphics/trainers/front_pics/brendan.png',64,64)[0];p=outfit_frame(f,0,2,'front',0)
assert any(p[y][x]==9 and f[y][x] in (5,6,7,8) for y in (44,46) for x in range(16,43))
assert any(p[48][x] in (2,3) and f[48][x] in (5,6,7,8) for x in range(16,43))
print('Four exact grunt uniforms/portraits, 16 throw frames, all field-action dimensions, native palettes and striped shorts passed')
