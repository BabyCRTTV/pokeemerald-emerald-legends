#!/usr/bin/env python3
"""Review-only family skin-tone study using the existing native sprite pixels."""
import argparse
import hashlib
import json
import re
import tempfile
from pathlib import Path

from PIL import Image,ImageDraw,ImageFont
from build_appearance import frames,skin_components
from preview_side_part import compile_renderer

ROOT=Path(__file__).resolve().parents[2]
SOURCES={
    'mom':'graphics/object_events/pics/people/mom.png',
    'norman':'graphics/object_events/pics/people/gym_leaders/norman.png',
    'battle':'graphics/trainers/front_pics/leader_norman.png',
}

def rgb555(color):return (color&31)*255//31,(color>>5&31)*255//31,(color>>10&31)*255//31
def packed(rgb):return (rgb[0]>>3)|((rgb[1]>>3)<<5)|((rgb[2]>>3)<<10)

def skin_mask(name,pixels):
    if name!='mom':
        slots=(1,2,3,4) if name=='battle' else (1,2,3)
        return {(x,y) for y,row in enumerate(pixels) for x,v in enumerate(row) if v in slots}
    groups=skin_components(pixels)
    # Mom's disconnected upper brown/peach dots are hair highlights. Her
    # largest face island, adjacent ears and lower hands alone inherit skin.
    face=max(groups,key=len)
    if len(face)<10:face=set() # Rear view has covered head/neck.
    mask=set(face)
    for group in groups:
        if min(y for x,y in group)>=23:
            mask|=group
        elif face and min(y for x,y in group)>=min(y for x,y in face) and max(y for x,y in group)<=max(y for x,y in face):
            mask|=group
    return mask

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output;out.mkdir(parents=True,exist_ok=True)
    text=(ROOT/'src/data/legends/appearance_palettes.h').read_text()
    body=re.search(r'sSkinPalettes\[5\]\[3\] = \{(.*?)\n\};',text,re.S)[1]
    ramps=[[int(v,16)for v in row.split(',')]for row in re.findall(r'\{([^}]+)\}',body)]
    assets={};source_hashes={};masks={}
    for name,path in SOURCES.items():
        image=Image.open(ROOT/path);palette=image.getpalette()
        colors=[packed(palette[i*3:i*3+3])for i in range(16)]
        poses=frames(ROOT/path,64,64)if name=='battle' else frames(ROOT/path,16,32)
        assets[name]=(poses,colors)
        source_hashes[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
        for pose,pixels in enumerate(poses):masks[name,pose]=skin_mask(name,pixels)
    # Brown material 4 in the battle sheet is facial/hand contour, rather
    # than Norman's slate hair or outfit. Keep its native shadow ratio.
    battle,battle_colors=assets['battle'];p=battle[0]
    for x,y in masks['battle',0]:
        if p[y][x]==4:
            assert any(0<=xx<64 and 0<=yy<64 and p[yy][xx]in(1,2,3)
                       for xx in range(x-2,x+3)for yy in range(y-2,y+3))
    validated=0
    def render(name,pose,tone=None):
        nonlocal validated
        poses,colors=assets[name];pixels=poses[pose];mask=masks[name,pose]
        ramp=ramps[tone]if tone is not None else None
        outline=None
        if ramp and name=='battle':
            channels=lambda c:(c&31,c>>5&31,c>>10&31)
            a,b,deep=map(channels,(colors[4],colors[3],ramp[2]))
            c=[round(value*edge/base)for value,edge,base in zip(deep,a,b)]
            outline=c[0]|c[1]<<5|c[2]<<10
        image=Image.new('RGBA',(len(pixels[0]),len(pixels)))
        for y,row in enumerate(pixels):
            for x,value in enumerate(row):
                if not value:continue
                color=colors[value]
                if ramp and (x,y)in mask:color=outline if value==4 else ramp[value-1]
                image.putpixel((x,y),(*rgb555(color),255))
        if tone is not None:
            native=render(name,pose)
            changed={(x,y)for y,row in enumerate(pixels)for x,v in enumerate(row)if image.getpixel((x,y))!=native.getpixel((x,y))}
            assert changed<=mask,(name,pose,'non-skin material changed')
            assert image.getchannel('A').tobytes()==native.getchannel('A').tobytes(),'silhouette changed'
            validated+=1
        return image
    for tone in range(5):
        for name,(poses,_)in assets.items():
            for pose in range(len(poses)):render(name,pose,tone)
    checks=validated
    canvas=Image.new('RGB',(360,2200),(238,235,248));draw=ImageDraw.Draw(canvas);draw.fontmode='1'
    def label(text,x,y,size=13):
        draw.text((x,y),text,font=ImageFont.truetype('DejaVuSans.ttf',size),fill=(35,33,48),anchor='mt')
    label('Family skin tones',180,16,23)
    label('Mom + Norman / five player tones',180,51,15)
    label('Native sprite recolors / preview only',180,78,12)
    with tempfile.TemporaryDirectory()as temp:
        _,player=compile_renderer(temp)
        for tone in range(5):
            y=110+tone*410
            draw.rounded_rectangle((6,y,354,y+402),radius=7,fill=(252,251,255))
            label(f'Skin tone {tone+1}',90,y+10,17)
            for i,color in enumerate(ramps[tone]):draw.rectangle((264+i*23,y+12,281+i*23,y+29),fill=rgb555(color))
            label('Player',52,y+39);label('Norman / battle',236,y+39)
            image=player(h=2,tone=tone,kind=0,pose=0)[0].resize((64,128),Image.Resampling.NEAREST)
            canvas.paste(image,(20,y+88),image)
            image=render('battle',0,tone).resize((192,192),Image.Resampling.NEAREST)
            canvas.paste(image,(140,y+58),image)
            label('Mom',90,y+260,15);label('Norman',270,y+260,15)
            for name,base in (('mom',12),('norman',192)):
                for pose,direction in enumerate(('Front','Back','Side')):
                    image=render(name,pose,tone).resize((48,96),Image.Resampling.NEAREST)
                    x=base+54*pose;canvas.paste(image,(x,y+282),image)
                    label(direction,x+24,y+383,11)
    label('Skin only / original hair, clothing and poses',180,2173,12)
    image_path=out/'Family-Skin-Tones-Preview.png';canvas.save(image_path)
    record={'baseline':'4dd6a65d32c7daf2c326df35a1898a71d6281670','scope':'Review-only Mom/Norman overworld and Norman battle portrait using the five existing player ramps. Mom hair highlights excluded; Norman battle deepest skin contour follows its native shade ratio.','source_sha256':source_hashes,'skin_ramps_RGB555':ramps,'validated_asset_tone_cases':checks,'alpha_and_non_skin_pixels_preserved':True,'image_sha256':hashlib.sha256(image_path.read_bytes()).hexdigest(),'runtime_integrated':False}
    (out/'proposal.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'preview':str(image_path),'validated_cases':checks,'sha256':record['image_sha256']}))

if __name__=='__main__':main()
