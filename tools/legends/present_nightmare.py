"""Present genuine native quest frames; no painting or synthesized gameplay."""
from pathlib import Path
import argparse,json,hashlib,shutil,zipfile
from PIL import Image,ImageDraw,ImageFont
R=Path(__file__).resolve().parents[2]
p=argparse.ArgumentParser();p.add_argument('--captures',type=Path,default=R/'build/nightmare-native');p.add_argument('--output',type=Path,required=True);a=p.parse_args();src=a.captures.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
proof=json.loads((src/'verification.json').read_text());assert proof['passed'];assert proof['ROM_sha256']==hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest()
raw=R/'docs/designs/nightmare';raw.mkdir(parents=True,exist_ok=True)
for name,digest in proof['images'].items():
 image=src/name;assert hashlib.sha256(image.read_bytes()).hexdigest()==digest
 im=Image.open(image);assert im.size==(240,160)
 shutil.copy2(image,raw/name)
shutil.copy2(src/'verification.json',raw/'verification.json')
fontdir=Path('/usr/share/fonts/truetype/dejavu');title=ImageFont.truetype(str(fontdir/'DejaVuSans-Bold.ttf'),26);label=ImageFont.truetype(str(fontdir/'DejaVuSans-Bold.ttf'),21);normal=ImageFont.truetype(str(fontdir/'DejaVuSans.ttf'),18);small=ImageFont.truetype(str(fontdir/'DejaVuSans.ttf'),16)
chapters=[('01-Darkrai-The-Call.png','THE CALL AND THE INVESTIGATION',[
 ('01d-daughter-wont-wake.png','01  AN UNKNOWN NUMBER'),('03-miras-slumber.png','02  MIRA WILL NOT WAKE'),('04-mt-pyre-caretaker.png','03  THE CARETAKER AT MT. PYRE')]),
 ('02-Darkrai-Into-The-Dream.png','FOLLOWING THE LUNAR WING',[
 ('05-lunar-wing-at-the-bed.png','04  ENTERING THE DREAM'),('06-empty-dream-bedroom.png','05  HER ROOM IS EMPTY'),('07-deserted-lilycove.png','06  A FAMILIAR, DESERTED STREET'),('08-miras-echo.png','07  FOLLOWING MIRA\'S VOICE')]),
 ('03-Darkrai-Awakening.png','THE MOONLESS SHORE AND THE RETURN',[
 ('10-moonless-shore.png','08  DARKRAI ON THE MOONLESS SHORE'),('11-darkrai-battle.png','09  THE LEVEL-80 ENCOUNTER'),('13-miras-return.png','10  MIRA WAKES UP'),('14-fathers-thanks.png','11  A FATHER\'S THANKS')])]
boards=[];rectangles={}
for filename,heading,rows in chapters:
 canvas=Image.new('RGB',(768,126+len(rows)*542+36),'#111b2a');draw=ImageDraw.Draw(canvas);draw.text((24,16),'WHEN MORNING NEVER COMES',font=title,fill='#e9d4a2');draw.text((24,54),heading,font=normal,fill='#bed5e9');draw.text((24,85),'Emerald Legends v0.0.76 + unshipped Darkrai quest review',font=small,fill='#aab9ca');rectangles[filename]=[]
 for i,(name,caption) in enumerate(rows):
  y=126+i*542;draw.text((24,y),caption,font=label,fill='#e9d4a2');im=Image.open(src/name).convert('RGB');scaled=im.resize((720,480),Image.Resampling.NEAREST);canvas.paste(scaled,(24,y+34));rectangles[filename].append(dict(source=name,rectangle=[24,y+34,744,y+514]))
  assert canvas.crop((24,y+34,744,y+514)).resize((240,160),Image.Resampling.NEAREST).tobytes()==im.tobytes()
 draw.text((24,canvas.height-30),'Actual mGBA frames, enlarged 3x. Controlled quest fixtures.',font=small,fill='#aab9ca');canvas.save(out/filename,optimize=True);boards.append(out/filename)
readme='''# Darkrai quest progression review

Implemented on review branch codex/darkrai-nightmare; the public download has not changed.

The boards show real frames from the compiled Emerald Legends Debug ROM running in mGBA, with the game engine's actual dialogue, map movement, encounter, capture and recovery scripts. Controlled fixtures place the player at independent test stages; these are not an uninterrupted natural full-story playthrough. Each game panel is enlarged exactly3x with nearest-neighbor scaling, with framing/captions outside the original game pixels.

Story: Regidrago capture or defeat unlocks Elias's one-time call. Investigate Mira's slumber in Lilycove, obtain a real Lunar Wing at Mt. Pyre, follow it through an empty room and a deserted city, confront level80 Darkrai on the moonless shore, then return to Mira and her father. Capture or defeat wakes Mira; escape/loss remain retryable. Defeat retains a later capture opportunity without putting her back to sleep.

Native input checks passed for all these paths, the wing/Cleanse Tag rewards, both home exits, both shore passages, post-capture footprint clearing, safe wake-up/revisit, actual blackout, flash save/load and a controlled old-position Continue repair. The bound native receipt includes frame, ROM, ELF and harness hashes. Release candidate checks are recorded separately.

No ROMs, ELFs or battery saves are included.
'''
(out/'README.md').write_text(readme)
export=dict(ROM_sha256=proof['ROM_sha256'],native_proof_sha256=hashlib.sha256((src/'verification.json').read_bytes()).hexdigest(),panels=rectangles,board_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in boards},pixelVerification='Every game panel resizes back to the exact240x160 RGB source; no overlays or repainted pixels.')
(out/'gallery-verification.json').write_text(json.dumps(export,indent=2)+'\n')
with zipfile.ZipFile(out/'Darkrai-Quest-Progression.zip','w',zipfile.ZIP_DEFLATED) as z:
 for path in [*boards,out/'README.md',out/'gallery-verification.json',src/'verification.json']:
  z.write(path,path.name)
 for name in proof['images']:z.write(src/name,'native/'+name)
 assert all(Path(n).suffix in ['.png','.md','.json'] for n in z.namelist())
(raw/'README.md').write_text('''# When Morning Never Comes — native progression review

Source checkpoint bd9dd0fc2fe05fe7a147eddef992eb3b368c4c21. Actual compiled Debug game in mGBA0.10.2; controlled quest fixtures, not synthetic images. No new visual approval or public release yet.

[Quest guide](../../features/when-morning-never-comes.md), [bound evidence](../../qa/nightmare-quest.json), [native frame/harness/ROM receipt](verification.json).

The numbered native PNGs cover the unknown call, family home and slumber, caretaker, Lunar Wing, dream room/chair, deserted city/echo, moonless shore, Darkrai battle and actual awakening/report. Later frames verify escape, defeat and blackout. Both visible door/shore lanes and post-capture footprint clearing were walked in game. The source PNGs are240x160 and unmodified; present_nightmare.py creates separately exported readable boards with exact3x game pixels and external captions.

The complete native Lilycove house, House1 wall/furniture assemblies and Southern Island coast/stairs/pier were compared to the standing Emerald Crest creator gallery for coherent materials, complete silhouettes, clear approaches and night readability. No Crest art was imported. All accepted Wyrmtide, player and wardrobe source art remains unchanged.
''')
print(json.dumps(dict(output=str(out),boards=[str(p) for p in boards],archive=str(out/'Darkrai-Quest-Progression.zip'),panels=sum(len(rows) for _,_,rows in chapters),nativeFrames=len(proof['images'])),indent=2))
