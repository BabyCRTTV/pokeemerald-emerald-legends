#!/usr/bin/env python3
"""Produce real transparent Happiny launcher assets from Legends' own icon sheet.

Use frame one of the 32x64 icon (frame two is only the alternate animation).
Clear exterior-connected background pixels without recoloring the Pokémon.
No generated PNG, ICO or commercial ROM is committed to source control.
"""
from collections import deque
from pathlib import Path
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"graphics/pokemon/happiny/icon.png"
ANDROID=ROOT/"android/wiki/app/src/main/res/drawable/happiny_icon.png"
WINDOWS=ROOT/"windows/wiki/assets/happiny.ico"

sheet=Image.open(SOURCE).convert("RGBA")
assert sheet.size[0] == 32 and sheet.size[1] >= 64, sheet.size
pixels=sheet.crop((0,0,32,32))
bg=pixels.getpixel((0,0))
seen=set()
queue=deque([(x,0) for x in range(32)]+[(x,31) for x in range(32)]
            +[(0,y) for y in range(32)]+[(31,y) for y in range(32)])
while queue:
    x,y=queue.popleft()
    if (x,y) in seen or not (0<=x<32 and 0<=y<32):
        continue
    seen.add((x,y))
    if pixels.getpixel((x,y))!=bg and pixels.getpixel((x,y))[3]!=0:
        continue
    pixels.putpixel((x,y),(0,0,0,0))
    queue.extend(((x-1,y),(x+1,y),(x,y-1),(x,y+1)))

bbox=pixels.getbbox()
assert bbox is not None, "Happiny image became empty"
silhouette=pixels.crop(bbox)
# Pixel-perfect rendering. Leave generous margins to avoid launcher masking.
def icon(size):
    canvas=Image.new("RGBA",(size,size),(0,0,0,0))
    border=int(size*.16)
    ratio=min((size-2*border)/silhouette.width,(size-2*border)/silhouette.height)
    dimensions=(max(1,int(silhouette.width*ratio)), max(1,int(silhouette.height*ratio)))
    scaled=silhouette.resize(dimensions,Image.Resampling.NEAREST)
    canvas.alpha_composite(scaled,((size-dimensions[0])//2,(size-dimensions[1])//2))
    return canvas

ANDROID.parent.mkdir(parents=True,exist_ok=True)
WINDOWS.parent.mkdir(parents=True,exist_ok=True)
icon(512).save(ANDROID)
icon(256).save(WINDOWS,format="ICO",sizes=[(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)])
print("Created transparent single-sprite Happiny icons",ANDROID,WINDOWS)
