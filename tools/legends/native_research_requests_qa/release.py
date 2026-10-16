"""Unmodified Release Continue with legacy, active and completed private request fixtures."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--fixture',type=Path,required=True);p.add_argument('--state',required=True);p.add_argument('--done',required=True);p.add_argument('--high',default='0');p.add_argument('--seafoam',default='0');p.add_argument('--master',default='0');a=p.parse_args()
 out=a.output.resolve();out.mkdir(exist_ok=True,parents=True);prefix=a.prefix.resolve();fixture=a.fixture.resolve();src=Path(__file__).resolve().parent
 env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 nm=subprocess.check_output([str(prefix/'bin/arm-none-eabi-nm'),str(R/'pokeemerald-release.elf')],text=True)
 symbols={v[2]:int(v[0],16) for line in nm.splitlines() if len(v:=line.split())==3}
 if 'sReminderHandle' not in symbols:symbols['sReminderHandle']=symbols['sReminderHandle.lto_priv.0']
 with (out/'host-build.log').open('w') as f:subprocess.run(['cc',str(src/'release.c'),'-iquote',str(R/'include'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'release')],env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 rom=R/'pokeemerald-release.gba';before=sha(rom)
 private_save=out/'private-release.sav';private_save.write_bytes(fixture.read_bytes())
 with (out/'emulator.log').open('w') as f:subprocess.run([str(out/'release'),str(rom),str(private_save),str(out),hex(symbols['sReminderHandle']),hex(symbols['gMain']),hex(symbols['CB2_Overworld']),hex(symbols['gSaveBlock1Ptr']),fixture.parent.joinpath('offsets.txt').read_text().split()[0],a.state,a.done,a.high,a.seafoam,hex(symbols['gPokemonStoragePtr']),fixture.parent.joinpath('offsets.txt').read_text().split()[2],a.master],env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 assert sha(rom)==before
 for p in out.glob('*.rgba'):Image.frombytes('RGBA',(240,160),p.read_bytes()).convert('RGB').save(p.with_suffix('.png'))
 if a.state=='0xb803':
  debug=Image.open(fixture.parent/'tracked-pause.png').crop((0,0,112,88));release=Image.open(out/'release-pause-tracked.png').crop((0,0,112,88));assert debug.tobytes()==release.tobytes()
 proof={'passed':True,'variant':'Release','emulator':'mGBA 0.10.2','ROM_sha256':before,'ROM_unmodified':True,'battery_fixture_sha256':sha(fixture),'reminder_pixels_equal_to_Debug':a.state=='0xb803','captures':{p.name:sha(p) for p in sorted(out.glob('*.png'))},'log':(out/'emulator.log').read_text(),'scope':'Unmodified Release ROM loaded the private Debug-produced controlled battery fixture via normal title/Continue input. Verified persisted request words/high bits and PC Master Ball quantity. The active-fixture run also exercised native pause pages, tracked SIDE Details and stop-tracking. Host did not write RAM or callbacks. Not a historical-release save or broader playthrough. Private fixture excluded.','harness_sha256':{name:sha(src/name) for name in ['release.c','release.py']}}
 (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof,indent=2))
if __name__=='__main__':main()
