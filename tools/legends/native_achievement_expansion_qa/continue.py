"""Normal unmodified ROM Continue against the controlled extension battery fixtures."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess
from PIL import Image
R=Path(__file__).resolve().parents[3]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--prefix',type=Path,required=True);p.add_argument('--fixture',type=Path,required=True);p.add_argument('--variant',choices=['Debug','Release'],required=True);p.add_argument('--claimed',choices=['0','1'],required=True);a=p.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True);prefix=a.prefix.resolve();env=os.environ.copy();env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','');stem='pokeemerald-release' if a.variant=='Release' else 'pokeemerald';src=Path(__file__).resolve().parent
 nm=subprocess.check_output(['arm-none-eabi-nm',str(R/(stem+'.elf'))],text=True);syms={v[2]:int(v[0],16) for line in nm.splitlines() if len(v:=line.split())==3}
 subprocess.run(['cc',str(src/'continue.c'),'-iquote',str(R/'include'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],env=env,check=True)
 fixture=a.fixture.resolve();save=out/'private.sav';save.write_bytes(fixture.read_bytes());pc,vars=fixture.parent.joinpath('offsets.txt').read_text().split();rom=R/(stem+'.gba');before=sha(rom)
 with (out/'emulator.log').open('w') as log:subprocess.run([str(out/'host'),str(rom),str(save),str(out),hex(syms['gMain']),hex(syms['CB2_Overworld']),hex(syms['gSaveBlock3Ptr']),hex(syms['gPokemonStoragePtr']),pc,hex(syms['gSaveBlock1Ptr']),vars,a.claimed],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 assert sha(rom)==before
 Image.frombytes('RGBA',(240,160),(out/'continued.rgba').read_bytes()).convert('RGB').save(out/'continued.png')
 proof={'passed':True,'variant':a.variant,'ROM_sha256':before,'fixture_sha256':sha(fixture),'fixture':'Controlled format-identical v0.0.59 journal upgraded by current Debug; not an authentic historical user save.','ROM_unmodified':True,'host_wrote_RAM':False,'log':(out/'emulator.log').read_text()};(out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n');print(json.dumps(proof))
if __name__=='__main__':main()
