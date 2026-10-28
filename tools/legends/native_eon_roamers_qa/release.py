"""Unmodified Release Continue from privately generated controlled battery fixtures."""
from pathlib import Path
import argparse,subprocess,os,json,hashlib
from PIL import Image
R=Path(__file__).resolve().parents[3];S=Path(__file__).resolve().parent
def main():
 p=argparse.ArgumentParser();p.add_argument('--prefix',type=Path,default=Path('/usr'));p.add_argument('--fixtures',type=Path,default=R/'build/eon-roamers-qa');p.add_argument('--output',type=Path,default=R/'build/eon-roamers-release-qa');a=p.parse_args();prefix=a.prefix.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
 env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
 symbols={v[2]:int(v[0],16) for line in subprocess.check_output([str(prefix/'bin/arm-none-eabi-nm'),str(R/'pokeemerald-release.elf')],text=True).splitlines() if len(v:=line.split())==3}
 subprocess.run(['cc',str(S/'release.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'release-host')],env=env,check=True)
 rom=R/'pokeemerald-release.gba';before=hashlib.sha256(rom.read_bytes()).hexdigest();logs=[]
 for name in sorted(p.stem.removeprefix('private-') for p in a.fixtures.glob('private-*.json')):
  fixture=a.fixtures/('private-'+name);meta=json.loads(fixture.with_suffix('.json').read_text());save=out/('private-'+name+'.sav');save.write_bytes(fixture.with_suffix('.sav').read_bytes());raw=out/(name+'.rgba')
  result=subprocess.run([str(out/'release-host'),str(rom),str(save),str(raw),hex(symbols['gMain']),hex(symbols['CB2_Overworld']),hex(symbols['gSaveBlock1Ptr']),hex(symbols['gSaveBlock3Ptr'])]+[str(meta[k]) for k in ['offset','first_hash','checksum','first_active','partner_active','unlocked']]+[hex(symbols['gPartiesCount']),str(meta['party'])],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (out/(name+'.log')).write_text(result.stdout);assert result.returncode==0,result.stdout;logs.append(result.stdout.strip());Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'));raw.unlink()
 assert hashlib.sha256(rom.read_bytes()).hexdigest()==before
 proof={'ROM_sha256':before,'ROM_unmodified':True,'RAM_writes':False,'emulator':'mGBA 0.10.2','scope':'Title and normal Release Continue; Debug-generated legacy-initialized, first escaped/caught/defeated and partner resolved fixtures, exact original roamer and signed partner identities/state plus party count. Debug-generated controlled batteries, not authentic historical owner saves.','log':logs,'images':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')}}
 (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print('\n'.join(logs))
if __name__=='__main__':main()
