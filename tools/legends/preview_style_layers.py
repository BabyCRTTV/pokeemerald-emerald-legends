"""Render wardrobe authoring contact sheets, independently of the GBA emulator."""
from pathlib import Path
import sys
from PIL import Image,ImageDraw
root=Path(__file__).resolve().parents[2]
from build_style_layers import *
canvas=Image.new('RGB',(11*180,4*210),(225,218,233));d=ImageDraw.Draw(canvas)
for g,n in enumerate(('brendan','may')):
 for row,(kind,w,h) in enumerate((('front',64,64),('overworld',16,32))):
  path=root/(f'graphics/trainers/front_pics/{n}.png' if kind=='front' else f'graphics/object_events/pics/people/{n}/walking.png')
  im=Image.open(path);frame=frames(path,w,h)[0]
  for hair in range(11):
   coat=coat_edits(frame,g,kind,0,2) if hair else frame
   hf=hair_edits(frame,g,kind,0,hair) if hair else frame
   out=[r[:] for r in coat]
   for y in range(h):
    for x in range(w):
     if hf[y][x]!=frame[y][x]:out[y][x]=hf[y][x]
   a=Image.new('P',(w,h));a.putpalette(im.getpalette());a.putdata([v for r in out for v in r]);rgb=a.convert('RGB')
   for y in range(h):
    for x in range(w):
     if out[y][x]==0:rgb.putpixel((x,y),(225,218,233))
   scale=2 if w==64 else 4;rgb=rgb.resize((w*scale,h*scale),Image.Resampling.NEAREST)
   xx=hair*180+20;yy=(g*2+row)*210+35
   canvas.paste(rgb,(xx,yy));d.text((xx,yy-20),f'{n} {hair}',fill=(20,20,20))
canvas.save(root/'docs/qa/wardrobe-v0.0.38.png')

from pathlib import Path
import sys
from PIL import Image,ImageDraw
r=root
from build_style_layers import *
c=Image.new('RGB',(1320,900),(225,218,233));d=ImageDraw.Draw(c)
for g,n in enumerate(('brendan','may')):
 cases=[]
 for kind,file,w,h in [('back','back',64,64),('overworld','walking',16,32),('overworld','mach_bike',32,32),('overworld','fishing',32,32),('overworld','field_move',32,32)]:
  path=r/(f'graphics/trainers/back_pics/{n}.png' if kind=='back' else f'graphics/object_events/pics/people/{n}/{file}.png')
  im=Image.open(path)
  for i,p in enumerate(frames(path,w,h)[:(4 if file=='back' else 3)]):cases.append((kind,file,w,h,i,p,im.getpalette()))
 for k,(kind,file,w,h,i,p,pal) in enumerate(cases):
  coat=coat_edits(p,g,kind,i,2);hf=hair_edits(p,g,kind,i,7,file)
  for y in range(h):
   for x in range(w):
    if hf[y][x]!=p[y][x]:coat[y][x]=hf[y][x]
  a=Image.new('P',(w,h));a.putpalette(pal);a.putdata([v for row in coat for v in row]);rgb=a.convert('RGB')
  for y in range(h):
   for x in range(w):
    if coat[y][x]==0:rgb.putpixel((x,y),(225,218,233))
  xx=(k%8)*165+10;yy=g*440+(k//8)*220+30
  c.paste(rgb.resize((w*3,h*3),Image.Resampling.NEAREST),(xx,yy));d.text((xx,yy-20),f'{n} {file} {i}',fill='black')
c.save(root/'docs/qa/wardrobe-actions-v0.0.38.png')
