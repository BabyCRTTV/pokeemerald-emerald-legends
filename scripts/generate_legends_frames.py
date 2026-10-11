"""Build the five Legends frames as exact native 3x3, 4bpp tile sheets.

Requires Pillow. Regenerate with: python3 scripts/generate_legends_frames.py
Indices 0/1/14/15 retain native transparency/text colors. The middle tile
stays white; embellishments never enter the text area. Each edge repeats
on an eight-pixel boundary through the native window drawing functions.
"""
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
# Background, text outline and white/shadow match the original frame palette.
COMMON = {0: (98, 197, 98), 1: (41, 49, 49), 14: (255, 255, 255), 15: (74, 65, 82)}
THEMES = [
    ('Leaf', [(48,80,56),(88,128,88),(152,176,120),(200,216,160),(216,232,192),(64,104,64),(112,152,80)]),
    ('Ocean', [(48,72,104),(72,112,144),(128,176,192),(192,216,224),(216,232,240),(88,152,184),(160,200,216)]),
    ('Lavender Stitch', [(80,64,112),(120,104,152),(168,152,192),(208,192,224),(232,224,240),(152,120,168),(224,208,232)]),
    ('Amber Circuit', [(104,72,40),(152,112,64),(200,160,88),(232,208,144),(248,232,192),(168,128,56),(232,184,96)]),
    ('Poke Ball', [(88,72,80),(144,120,128),(192,168,176),(224,208,216),(240,232,232),(184,72,80),(240,128,128)]),
]


def frame(kind, shades):
    image = Image.new('P', (24,24), 0)
    palette = [0] * 768
    colors = dict(COMMON)
    colors.update(dict(zip(range(2,9), shades)))
    for index,rgb in colors.items(): palette[index*3:index*3+3] = rgb
    image.putpalette(palette)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((1,1,22,22), radius=3, fill=3, outline=1)
    draw.rounded_rectangle((2,2,21,21), radius=2, outline=4)
    draw.line((3,3,20,3), fill=5)
    draw.line((3,20,20,20), fill=2)
    draw.line((3,4,3,19), fill=5)
    draw.line((20,4,20,19), fill=2)
    draw.rounded_rectangle((5,5,18,18), radius=2, fill=6, outline=2)
    draw.rectangle((6,6,17,17), fill=14)
    # Corner motifs are mirrored, staying entirely inside the corner tiles.
    if kind == 0:  # Two-tone leaves.
        motif={(3,5):7,(4,4):7,(4,5):8,(5,3):7,(5,4):8,(5,5):7,(6,3):8,(6,4):7}
    elif kind == 1:  # Small wave crests.
        motif={(3,5):7,(4,4):7,(5,4):8,(6,5):7,(4,6):8,(5,6):7}
    elif kind == 2:  # Thread knot.
        motif={(4,3):8,(3,4):8,(4,4):7,(5,4):8,(4,5):8}
    elif kind == 3:  # Compact circuit node and traces.
        motif={(3,3):8,(4,3):8,(3,4):8,(4,4):7,(5,4):7,(6,4):7,(4,5):7,(4,6):7}
    else:  # Five-pixel Poke Ball, with red cap and white base.
        motif={(4,2):1,(3,3):1,(4,3):7,(5,3):1,(2,4):1,(3,4):1,(4,4):14,(5,4):1,(6,4):1,(3,5):1,(4,5):14,(5,5):1,(4,6):1}
    for x,y in [(0,0),(1,0),(0,1),(1,1)]:
        for (px,py),color in motif.items():
            if kind == 4 and y and py != 4 and color in (7,14):
                color = 14 if color == 7 else 7  # Red stays above white on lower balls.
            image.putpixel((23-px if x else px,23-py if y else py),color)
    # Quiet, repeatable edge details rather than large icons along every tile.
    if kind == 0:
        for x,y in [(10,4),(13,4),(10,19),(13,19),(4,10),(4,13),(19,10),(19,13)]: image.putpixel((x,y),8)
    elif kind == 1:
        for x in range(8,16):
            y=3 + (0,0,1,1,2,2,1,1)[x-8]
            image.putpixel((x,y),8);image.putpixel((x,23-y),8)
            image.putpixel((y,x),8);image.putpixel((23-y,x),8)
    elif kind == 2:
        for t in (9,13):
            for a,b in [(t,3),(t+1,3),(t,20),(t+1,20),(3,t),(3,t+1),(20,t),(20,t+1)]:image.putpixel((a,b),8)
    elif kind == 3:
        for t in range(8,16):
            for a,b in [(t,3),(t,20),(3,t),(20,t)]:image.putpixel((a,b),7)
        for a,b in [(11,3),(12,3),(11,20),(12,20),(3,11),(3,12),(20,11),(20,12)]:image.putpixel((a,b),8)
    return image


def main():
    for index,(name,shades) in enumerate(THEMES,21):
        image=frame(index-21,shades)
        image.save(ROOT / f'graphics/text_window/{index}.png', bits=4, optimize=False)
        print(f'TYPE {index}: {name}')

if __name__ == '__main__': main()
