"""Capture actual review-ROM frames using native mGBA; never export a ROM."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess
from PIL import Image

R = Path(__file__).resolve().parents[3]
S = Path(__file__).resolve().parent

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--prefix', type=Path, default=Path('/usr'))
    p.add_argument('--rom', type=Path, default=R/'pokeemerald.gba')
    p.add_argument('--elf', type=Path, default=R/'pokeemerald.elf')
    p.add_argument('--output', type=Path, default=R/'build/grotto-encounters')
    args = p.parse_args(); out = args.output.resolve(); out.mkdir(parents=True, exist_ok=True)
    for artifact in list(out.glob('room-*.png')) + list(out.glob('room-*.rgba')) + list(out.glob('discovery-*.png')) + list(out.glob('discovery-*.rgba')) + list(out.glob('cliff-*.png')) + list(out.glob('cliff-*.rgba')) + list(out.glob('entrance-option-*')):
        artifact.unlink()
    prefix = args.prefix.resolve(); env = os.environ.copy()
    env['PATH'] = str(prefix/'bin') + ':' + env['PATH']
    env['LD_LIBRARY_PATH'] = str(prefix/'lib/x86_64-linux-gnu') + ':' + env.get('LD_LIBRARY_PATH','')
    def run(cmd, log):
        with (out/log).open('w') as f:
            subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    def symbols(path):
        s = subprocess.check_output(['arm-none-eabi-nm',str(path)],env=env,text=True)
        return {v[2]:int(v[0],16) for line in s.splitlines() if len(v:=line.split())==3}
    run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD',
         '-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin',
         '-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa',
         '-Wl,--just-symbols='+str(args.elf),str(S/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
    run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
    source = args.rom.read_bytes()
    active_metatiles=(R/'data/tilesets/legends_grotto/fallarbor_cliff_metatiles.bin').read_bytes()
    tile_offset=symbols(args.elf)['gMetatiles_Fallarbor']-0x08000000
    assert source[tile_offset:tile_offset+len(active_metatiles)]==active_metatiles
    rom = bytearray(source); payload = (out/'arm.bin').read_bytes()
    assert len(payload)<65536 and set(rom[0x1f80000:0x1f80000+len(payload)])=={255}
    rom[0x1f80000:0x1f80000+len(payload)] = payload
    private = out/'PRIVATE-QA.gba'; private.write_bytes(rom)
    run(['cc',str(S/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),
         '-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
    run([str(out/'host'),str(private),str(out),hex(symbols(args.elf)['gMain']),hex(symbols(out/'arm.elf')['qa']),hex(symbols(args.elf)['gBattlerControllerFuncs'])]+[hex(int(line.split()[0],16)) for line in subprocess.check_output(['arm-none-eabi-nm',str(args.elf)],env=env,text=True).splitlines() if line.endswith(' t HandleInputChooseAction')]+[hex(symbols(args.elf)['gSaveBlock3Ptr'])],'emulator.log')
    assert args.rom.read_bytes()==source
    for raw in list(out.glob('*.rgba')):
        Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'))
        raw.unlink()
    proof = dict(version=(R/'VERSION').read_text().strip()+' + unshipped grotto encounters',
        ROM_sha256=hashlib.sha256(source).hexdigest(),emulator='mGBA 0.10.2 native core',
        passed=True,log=(out/'emulator.log').read_text(),
        setup='Private all-badge level-100 fixture (animations off), one physical walking step and fast-forward remaining-step callback; production battle, capture, scripts, state, flash writer and loader.',
        limits='Synthetic pre-grotto unused tail, not an authentic historical user save; no Pizza Boy or full playthrough.',
        harness_sha256={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [S/'arm.c',S/'host.c',S/'run.py']},
        images={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')})
    (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    private.unlink()
    print('PASS: native grotto battles and persistence. '+str(out))

if __name__ == '__main__': main()
