"""Actual unmodified Release Continue and boat interactions from private current-save fixtures."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess
from PIL import Image
R = Path(__file__).resolve().parents[3]
S = Path(__file__).resolve().parent

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--prefix', type=Path, default=Path('/usr'))
    p.add_argument('--fixtures', type=Path, default=R/'build/ember-return-qa')
    p.add_argument('--output', type=Path, default=R/'build/ember-return-release-qa')
    a = p.parse_args(); out = a.output.resolve(); out.mkdir(parents=True, exist_ok=True)
    (out/'verification.json').unlink(missing_ok=True)
    prefix = a.prefix.resolve(); env = os.environ.copy()
    env['LD_LIBRARY_PATH'] = str(prefix/'lib/x86_64-linux-gnu') + ':' + env.get('LD_LIBRARY_PATH','')
    nm = subprocess.check_output([str(prefix/'bin/arm-none-eabi-nm'),str(R/'pokeemerald-release.elf')],text=True)
    symbols = {v[2]:int(v[0],16) for line in nm.splitlines() if len(v:=line.split()) == 3}
    def address(name):
        if name in symbols: return symbols[name]
        matches = {value for key,value in symbols.items() if key.startswith(name+'.lto_priv.')}
        assert len(matches) == 1, (name, [key for key in symbols if key.startswith(name)])
        return matches.pop()
    def run(cmd, log):
        result = subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        log.write_text(result.stdout)
        assert result.returncode == 0, result.stdout[-10000:]
    run(['cc',str(S/'release.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],out/'host-build.log')
    rom = R/'pokeemerald-release.gba'; before = hashlib.sha256(rom.read_bytes()).hexdigest()
    receipts = {}
    for ready in [0,1]:
        name = 'ready' if ready else 'locked'; scene = out/name; scene.mkdir(exist_ok=True)
        fixture = a.fixtures/('private-'+name+'.sav'); meta = json.loads(fixture.with_suffix('.json').read_text())
        save = scene/'private.sav'; shutil.copyfile(fixture,save)
        run([str(out/'host'),str(rom),str(save),str(scene),*[hex(address(n)) for n in ['gMain','CB2_Overworld','gSaveBlock1Ptr','gSpecialVar_Result']],str(meta['flags_offset']),*map(str,meta['flag_ids']),*map(str,meta['ember']),*map(str,meta['town']),str(ready),hex(address('sLockFieldControls'))],scene/'emulator.log')
        for raw in scene.glob('*.rgba'):
            Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png')); raw.unlink()
        receipts[name] = dict(fixture_sha256=hashlib.sha256(fixture.read_bytes()).hexdigest(), metadata=meta, log=(scene/'emulator.log').read_text())
    assert hashlib.sha256(rom.read_bytes()).hexdigest() == before
    (out/'verification.json').write_text(json.dumps(dict(version=(R/'VERSION').read_text().strip(),variant='Release',ROM_sha256=before,ROM_unmodified=True,RAM_writes=False,emulator='native mGBA core',scope='Normal title/Continue, actual boat decline/accept, return, walking and reboarding; with/without outbound gates.',limits='Controlled current Debug-produced battery fixtures, not authentic historical saves, full story traversal or Pizza Boy.',fixture_ROM_sha256=json.loads((a.fixtures/'verification.json').read_text())['ROM_sha256'],harness_sha256={n:hashlib.sha256((S/n).read_bytes()).hexdigest() for n in ['release.c','release.py']},fixtures=receipts,images={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*.png')}),indent=2)+'\n')
    print('PASS: unmodified Release Continue and native Ember boat round trips')

if __name__ == '__main__': main()
