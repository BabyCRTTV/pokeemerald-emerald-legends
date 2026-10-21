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
    p.add_argument('--output', type=Path, default=R/'build/grotto-review')
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
    run([str(out/'host'),str(private),str(out),hex(symbols(args.elf)['gMain']),hex(symbols(out/'arm.elf')['qa'])],'emulator.log')
    assert args.rom.read_bytes()==source
    for raw in list(out.glob('*.rgba')):
        Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'))
        raw.unlink()
    assert len(list(out.glob('room-*.png'))) == 28
    assert len(list(out.glob('entrance-option-*.png'))) == 3
    proof = dict(version=(R/'VERSION').read_text().strip()+' + unshipped grotto review',
        ROM_sha256=hashlib.sha256(source).hexdigest(),emulator='mGBA 0.10.2 native core',
        entrance_options={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('entrance-option-*.png'))},
        seasonal_scenes=12, walking_exit_reentry_and_decline_paths=3,
        discovery_film_frames=len(list(out.glob('discovery-*.png'))),
        cliff_approach_film_frames=len(list(out.glob('cliff-*.png'))),
        cliff_frame_hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('cliff-*.png'))],
        setup='Private callback creates controlled twelve seasonal fixtures; native map renderer, sprites, movement and dialogue are unaltered.',
        limits='This harness checks exploration and scenery only. Battles, cooldowns and flash loading are tested separately by native_grotto_encounters; no natural progression or Pizza Boy coverage.',
        images={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('room-*.png')},
        discovery_frame_hashes=[hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.glob('discovery-*.png'))])
    (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    private.unlink()
    print('PASS: native grotto review. '+str(out))

if __name__ == '__main__': main()
