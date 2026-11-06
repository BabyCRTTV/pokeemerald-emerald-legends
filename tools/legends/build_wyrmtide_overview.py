"""Render a clearly labelled source-tile layout, not a gameplay screenshot."""
from pathlib import Path
import json,struct
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
primary=R/'data/tilesets/primary/general';shore=R/'data/tilesets/legends_wyrmtide_shore';dew=R/'data/tilesets/secondary/dewford'
images=[Image.open(primary/'tiles.png'),Image.open(shore/'tiles.png')]
metas=[(p/'metatiles.bin').read_bytes() for p in [primary,shore]]
palettes=[]
for i in range(16):
 p=(primary if i<6 else dew)/f'palettes/{i:02}.pal'
 if i==6:p=R/'data/tilesets/secondary/cave/palettes/06.pal'
 palettes.append([tuple(map(int,l.split())) for l in p.read_text().splitlines()[3:19]])
layout=next(l for l in json.loads((R/'data/layouts/layouts.json').read_text())['layouts'] if l['name']=='LegendsWyrmtide_Isle_Layout')
w,h=layout['width'],layout['height'];raw=(R/layout['blockdata_filepath']).read_bytes();world=Image.new('RGB',(w*16,h*16))
for at,(cell,) in enumerate(struct.iter_unpack('<H',raw)):
 mid=cell&1023;meta=Image.new('RGBA',(16,16),(0,0,0,255))
 for i,word in enumerate(struct.unpack_from('<8H',metas[mid//512],mid%512*16)):
  tid=word&1023;im=images[tid//512];tid%=512;x,y=tid%16*8,tid//16*8;tile=im.crop((x,y,x+8,y+8))
  if word&1024:tile=tile.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
  if word&2048:tile=tile.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
  rgba=Image.new('RGBA',(8,8));rgba.putdata([(*palettes[word>>12][v%16],255 if v%16 else 0) for v in tile.get_flattened_data()]);meta.alpha_composite(rgba,(i%2*8,i//2%2*8))
 world.paste(meta,(at%w*16,at//w*16))
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',15)
board=Image.new('RGB',(w*32+32,h*32+120),'#14232a');d=ImageDraw.Draw(board);d.text((16,12),'WYRMTIDE ISLE / SOURCE MAP LAYOUT',font=font,fill='#e1ce94');d.text((16,42),'v0.0.70 + unshipped review | 34 x 29 cells | Existing Hoenn art',font=small,fill='#aabec4');board.paste(world.resize((w*32,h*32),Image.Resampling.NEAREST),(16,74));d.text((16,h*32+87),'Tile layout only; NPCs omitted. See the native mGBA gallery for gameplay.',font=small,fill='#aabec4')
out=R/'docs/designs/wyrmtide/hoenn-review/Island-Layout.png';board.save(out);print(out)
