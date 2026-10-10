"""Manually bundle normal/shiny battle portraits from the pinned wiki snapshot.

Requires Pillow. Uses palette indices from the game, with index zero transparent.
Does not update game files or encounter data. Regenerate only on manual request.
"""
import io,json,math,subprocess,hashlib
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
WIKI=ROOT/'docs/wiki'
data=json.loads((WIKI/'dex-data.json').read_text())
icons=sorted({p.get('sprite') or p['id'].lower() for p in data['species']})
paths=set(subprocess.check_output(['git','ls-tree','-r','--name-only',data['sourceCommit']],cwd=ROOT).decode().splitlines())
columns,side=32,64
normal=Image.new('RGBA',(columns*side,math.ceil(len(icons)/columns)*side))
shiny=Image.new('RGBA',normal.size)
def read(path):
 return subprocess.check_output(['git','show',data['sourceCommit']+':'+path],cwd=ROOT)
for index,icon in enumerate(icons):
 base='graphics/pokemon/'+icon+'/'
 front=base+('anim_front.png' if base+'anim_front.png' in paths else 'front.png')
 sheet=Image.open(io.BytesIO(read(front)))
 assert sheet.mode=='P' and sheet.width==side and sheet.height>=side,icon
 indices=sheet.crop((0,0,side,side))
 frames=[]
 for name in ['normal','shiny']:
  palette=[tuple(map(int,row.split())) for row in read(base+name+'.pal').decode().splitlines()[3:]]
  assert max(indices.tobytes())<len(palette)<=16,icon
  frame=Image.new('RGBA',(side,side))
  frame.putdata([(*palette[pixel],255) if pixel else (0,0,0,0) for pixel in indices.tobytes()])
  frames.append(frame)
 bounds=frames[0].getbbox();assert bounds,icon
 for atlas,frame in zip([normal,shiny],frames):
  sprite=frame.crop(bounds)
  atlas.alpha_composite(sprite,((index%columns)*side+(side-sprite.width)//2,(index//columns)*side+(side-sprite.height)//2))
normal.save(WIKI/'dex-portraits.webp',format='WEBP',lossless=True,method=6)
shiny.save(WIKI/'dex-portraits-shiny.webp',format='WEBP',lossless=True,method=6)
print('Bundled',len(icons),'matching normal/shiny portraits from',data['sourceCommit'])
print('Normal/shiny bytes:',(WIKI/'dex-portraits.webp').stat().st_size,(WIKI/'dex-portraits-shiny.webp').stat().st_size)

metadata=dict(sourceCommit=data["sourceCommit"],count=len(icons),columns=columns,rows=normal.height//side,tileSize=side,files={name:hashlib.sha256((WIKI/name).read_bytes()).hexdigest() for name in ["dex-portraits.webp","dex-portraits-shiny.webp"]})
(WIKI/"dex-portrait-sources.json").write_text(json.dumps(metadata,indent=2)+"\n")
