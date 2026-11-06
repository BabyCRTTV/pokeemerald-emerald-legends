"""Package a verified continuous native mGBA tour; never synthesize frames/audio."""
from pathlib import Path
import argparse,array,hashlib,json,subprocess
from PIL import Image
p=argparse.ArgumentParser();p.add_argument('--native',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();src=a.native.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
proof=json.loads((src/'verification.json').read_text());stats=json.loads((src/'walkthrough-recording.json').read_text())
assert proof['passed'] and not proof['scenesOnly'] and proof['walkthroughRecorded'] and stats['noResetsDuringRecording']
video=src/'walkthrough-video.raw';audio=src/'walkthrough-audio.raw';fps=262144/4389
assert video.stat().st_size==stats['videoFrames']*240*160*4
assert audio.stat().st_size==stats['audioSamples']*4
duration=stats['emulatedFrames']/fps
assert abs(stats['audioSamples']/48000-duration)<.12
assert abs(stats['videoFrames']/(fps/2)-duration)<.04
pcm=array.array('h');pcm.frombytes(audio.read_bytes());peak=max(abs(x) for x in pcm);assert peak>256
chapters=[{'tick':int(line.split('|',1)[0]),'title':line.split('|',1)[1]} for line in (src/'walkthrough-chapters.txt').read_text().splitlines()]
meta=[';FFMETADATA1','title=Emerald Legends - Wyrmtide Cavern Walkthrough']
for i,ch in enumerate(chapters):
 start=ch['tick']/fps;end=chapters[i+1]['tick']/fps if i+1<len(chapters) else duration
 ch['seconds']=round(start,3)
 if end-start>.01:meta+=['[CHAPTER]','TIMEBASE=1/1000',f'START={round(start*1000)}',f'END={round(end*1000)}','title='+ch['title']]
metadata=out/'walkthrough.ffmeta';metadata.write_text('\n'.join(meta)+'\n')
movie=out/'Emerald-Legends-Cavern-Walkthrough.mp4'
subprocess.run(['ffmpeg','-y','-v','warning','-f','rawvideo','-pixel_format','rgba','-video_size','240x160','-framerate','131072/4389','-i',str(video),'-f','s16le','-ar','48000','-ac','2','-i',str(audio),'-i',str(metadata),'-map','0:v:0','-map','1:a:0','-map_metadata','2','-vf','scale=960:640:flags=neighbor:out_color_matrix=bt709','-c:v','libx264','-preset','medium','-crf','15','-pix_fmt','yuv420p','-colorspace','bt709','-color_primaries','bt709','-color_trc','bt709','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(movie)],check=True)
streams=json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(movie)],text=True))
assert any(s['codec_name']=='h264' and s['width']==960 and s['height']==640 for s in streams['streams'])
assert any(s['codec_name']=='aac' for s in streams['streams'])
assert abs(float(streams['format']['duration'])-duration)<.2
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest()
images={}
with video.open('rb') as f:
 for i,ch in enumerate(chapters):
  frame=min(ch['tick']//2,stats['videoFrames']-1);f.seek(frame*240*160*4)
  image=Image.frombytes('RGBA',(240,160),f.read(240*160*4)).convert('RGB');name=f'Chapter-{i+1:02}.png';path=out/name
  image.resize((720,480),Image.Resampling.NEAREST).save(path);images[name]=sha(path)
report={'version':proof['version'],'ROM_sha256':proof['ROM_sha256'],'emulator':proof['emulator'],'passed':True,'continuous':True,'setup':'Open-seal native fixture before recording; real movement and status-only fixture queries during recording. No resets or scene/party/flag setup during movie.','ending':'Sleeping Regidrago; recording ends before battle.','stats':stats,'durationSeconds':round(duration,3),'audioPeak':peak,'nativeAudio':True,'rawVideoSHA256':sha(video),'rawAudioSHA256':sha(audio),'movieSHA256':sha(movie),'movieBytes':movie.stat().st_size,'encoding':'Native 240x160 sampled every two emulated frames at actual GBA rate; exact nearest-neighbor 4x scaling, H.264 CRF15 with AAC native audio. Chapter PNGs preserve exact source RGB at 3x.','chapters':chapters,'images':images}
(out/'walkthrough-proof.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'movie':str(movie),'durationSeconds':report['durationSeconds'],'bytes':report['movieBytes'],'sha256':report['movieSHA256']}))
