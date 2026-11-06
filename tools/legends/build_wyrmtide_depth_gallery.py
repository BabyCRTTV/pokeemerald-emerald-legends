"""Package actual native frames; retain exact pixels in enlargements and GIF."""
from pathlib import Path
import argparse, hashlib, json
from PIL import Image, ImageSequence

R = Path(__file__).resolve().parents[2]


def sha(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()


def build(native, out):
 proof = json.loads((native/'verification.json').read_text())
 assert proof['passed'] and not proof['scenesOnly'] and proof['protectedHeartRGBExact']
 out.mkdir(parents=True,exist_ok=True)
 def frame(name):
  p=native/name;assert sha(p)==proof['images'][name]
  return Image.open(p).convert('RGB')
 for src,dst in [('28-stone-stair-flight.png','Terrace-Depth.png'),('29-wide-stone-flight.png','Wide-Terrace-Depth.png')]:
  frame(src).resize((720,480),Image.Resampling.NEAREST).save(out/dst)
 before=Image.open(R/'docs/designs/wyrmtide/stair-fit/29-wide-stone-flight.png').convert('RGB')
 after=frame('29-wide-stone-flight.png');board=Image.new('RGB',(488,160),(24,24,30))
 board.paste(before,(0,0));board.paste(after,(248,0));board.resize((976,320),Image.Resampling.NEAREST).save(out/'Depth-Before-After.png')
 names=[f'30-descending-{i:02}.png' for i in range(24)]
 frames=[frame(n) for n in names]
 colors=sorted(set().union(*(set(im.get_flattened_data()) for im in frames)))
 assert len(colors)<=256, 'Do not quantize real game colors'
 palette=[v for c in colors for v in c]+[0]*(768-len(colors)*3)
 lookup={c:i for i,c in enumerate(colors)};indexed=[]
 for im in frames:
  p=Image.new('P',im.size);p.putpalette(palette)
  p.putdata([lookup[c] for c in im.get_flattened_data()]);p=p.resize((480,320),Image.Resampling.NEAREST)
  assert p.convert('RGB').tobytes()==im.resize((480,320),Image.Resampling.NEAREST).tobytes()
  indexed.append(p)
 duration=[70]*24;duration[0]=300;duration[-1]=500
 target=out/'Walking-Down.gif'
 indexed[0].save(target,save_all=True,append_images=indexed[1:],duration=duration,loop=0,disposal=2,optimize=True)
 decoded=[im.convert('RGB').copy() for im in ImageSequence.Iterator(Image.open(target))]
 assert len(decoded)==24
 for i,im in enumerate(decoded):
  assert im.convert('RGB').tobytes()==indexed[i].convert('RGB').tobytes(), 'GIF changed native frame colors'
 report={'ROM_sha256':proof['ROM_sha256'],'emulator':proof['emulator'],'version':proof['version'],
         'nativeFrames':names,'sampleIntervalEmulatedFrames':4,'gifColors':len(colors),'gifRGBRoundtripExact':True,
         'stillScale':3,'gifScale':2,'gifDurationMilliseconds':duration,
         'outputs':{p.name:sha(p) for p in out.iterdir() if p.suffix in ['.png','.gif']}}
 (out/'gallery.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Packaged24 real southward-descent frames; GIF colors and nearest-neighbor pixels are exact.')


if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 build(a.native.resolve(),a.output.resolve())
