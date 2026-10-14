#!/usr/bin/env python3
"""Export before/after face buffers and native front walking/running timing."""
import tempfile
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw,ImageFont
from preview_side_part import animation,compile_renderer

ROOT=Path(__file__).resolve().parents[2]

def comparison(before,after,pose=0,motion='Standing'):
    canvas=Image.new('RGB',(360,1600),(238,235,248));draw=ImageDraw.Draw(canvas)
    draw.fontmode='1'
    def center(text,x,y,size):
        draw.text((x,y),text,font=ImageFont.truetype('DejaVuSans.ttf',size),fill=(35,33,48),anchor='mt')
    center('Front-face shading',180,15,23)
    center(motion+' / native C sprite buffers',180,48,14)
    center('v0.0.48',90,80,16);center('v0.0.49',270,80,16)
    for tone in range(5):
        y=114+tone*292
        draw.rounded_rectangle((6,y,354,y+286),radius=7,fill=(252,251,255))
        center(f'Skin tone {tone+1}',180,y+8,16)
        for gender,label,top in ((0,'Male',y+35),(1,'Female',y+161)):
            center(label,180,top+38,12)
            for column,render in enumerate((before,after)):
                image=render(h=2 if gender==0 else 6,tone=tone,g=gender,kind=0,pose=pose)[0]
                image=image.crop((0,4,16,28)).resize((80,120),Image.Resampling.NEAREST)
                canvas.paste(image,(column*180+50,top),image)
    center('Front-facing only / approved pixel cleanup',180,1577,13)
    return canvas

def main():
    output=ROOT/'docs/qa'
    with tempfile.TemporaryDirectory() as temp:
        old=Path(temp)/'old';new=Path(temp)/'new';old.mkdir();new.mkdir()
        _,before=compile_renderer(old,shade=False);_,after=compile_renderer(new)
        comparison(before,after).save(output/'front-face-v0.0.49-mobile.png')
        images=[];durations=[]
        for motion,repeats in (('Go',3),('Run',5)):
            for _ in range(repeats):
                for pose,ticks,flip in animation(motion+'South'):
                    assert not flip
                    images.append(comparison(before,after,pose,'Walking' if motion=='Go' else 'Running'))
                    durations.append(round(ticks*1000/60))
        gif=output/'front-face-v0.0.49-motion.gif'
        images[0].save(gif,save_all=True,append_images=images[1:],duration=durations,loop=0,disposal=1,optimize=True)
        encoded=Image.open(gif)
        for index,expected in enumerate(images):
            encoded.seek(index)
            assert ImageChops.difference(encoded.convert('RGB'),expected).getbbox() is None,'GIF altered sprite colors/pixels'
    print('Exported 360px front-face comparison PNG and native-timing animation GIF')

if __name__=='__main__':main()
