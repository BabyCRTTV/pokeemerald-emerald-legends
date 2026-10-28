"""Verify native dual-Eon battle outcomes and append-only flash saves; never export a ROM."""
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
    p.add_argument('--output', type=Path, default=R/'build/eon-roamers-qa')
    args = p.parse_args(); out = args.output.resolve(); out.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix.resolve(); env = os.environ.copy()
    env['PATH'] = str(prefix/'bin') + ':' + env['PATH']
    env['LD_LIBRARY_PATH'] = str(prefix/'lib/x86_64-linux-gnu') + ':' + env.get('LD_LIBRARY_PATH','')
    def run(cmd, log):
        with (out/log).open('w') as f:
            result = subprocess.run(cmd,cwd=R,env=env,stdout=f,stderr=subprocess.STDOUT)
        if result.returncode:
            for raw in out.glob('*.rgba'):
                Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'))
            raise RuntimeError((out/log).read_text()[-10000:])
    def symbols(path):
        s = subprocess.check_output(['arm-none-eabi-nm',str(path)],env=env,text=True)
        return {v[2]:int(v[0],16) for line in s.splitlines() if len(v:=line.split())==3}
    run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD',
         '-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin',
         '-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa',
         '-Wl,--just-symbols='+str(args.elf),str(S/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
    run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
    (out/'symbols.json').write_text(json.dumps(symbols(args.elf),sort_keys=True))
    # Compare canonical gbagfx bytes through both codecs, not a rendered approximation.
    stem = 'graphics/battle_anims/backgrounds/psychic_terrain.4bpp'
    run(['make',stem,stem+'.smol',stem+'.fastSmol'],'codec-build.log')
    raw = (R/stem).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == '635681cae116a817b35b4510cd90b0d6ce3d9deff4925cec4c803ad60fd3e067'
    codec_rows = []
    import struct
    for suffix in ['smol','fastSmol']:
        encoded = R/(stem+'.'+suffix); decoded = out/('decoded-'+suffix+'.bin')
        run([str(R/'tools/compresSmol/compresSmol'),'-d',str(encoded),str(decoded)],'codec-'+suffix+'.log')
        assert decoded.read_bytes() == raw
        a,b = struct.unpack('<II',encoded.read_bytes()[:8]); mode = a & 15
        sym,lo = a >> 18,b >> 19
        scratch = 0 if mode == 1 else ((sym+1)&~1)*2+((lo+1)&~1)
        codec_rows.append(dict(codec=suffix,mode=mode,encoded_bytes=encoded.stat().st_size,scratch_bytes=scratch,exact_raw_bytes=True))
    assert codec_rows[0]['scratch_bytes']==12152 and codec_rows[1]['scratch_bytes']==0
    codec = dict(asset='graphics/battle_anims/backgrounds/psychic_terrain.png',raw_SHA256=hashlib.sha256(raw).hexdigest(),PNG_SHA256=hashlib.sha256((R/'graphics/battle_anims/backgrounds/psychic_terrain.png').read_bytes()).hexdigest(),canonical_gbagfx=True,decoded_pixels_identical=True,results=codec_rows)
    source = args.rom.read_bytes()
    rom = bytearray(source); payload = (out/'arm.bin').read_bytes()
    assert len(payload)<65536 and set(rom[0x1f80000:0x1f80000+len(payload)])=={255}
    rom[0x1f80000:0x1f80000+len(payload)] = payload
    private = out/'PRIVATE-QA.gba'; private.write_bytes(rom)
    run(['cc',str(S/'host.c'),'-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),
         '-L'+str(prefix/'lib/x86_64-linux-gnu'),'-lmgba','-o',str(out/'host')],'host-build.log')
    run([str(out/'host'),str(private),str(out),hex(symbols(args.elf)['gMain']),hex(symbols(out/'arm.elf')['qa']),hex(symbols(args.elf)['gBattlerControllerFuncs'])]+[hex(int(line.split()[0],16)) for line in subprocess.check_output(['arm-none-eabi-nm',str(args.elf)],env=env,text=True).splitlines() if line.endswith(' t HandleInputChooseAction')]+[hex(symbols(args.elf)[name]) for name in ['gBattleMainFunc','gHeap','sDataPtr']],'emulator.log')
    assert args.rom.read_bytes()==source
    for raw in list(out.glob('*.rgba')):
        Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB').save(raw.with_suffix('.png'))
        raw.unlink()
    proof = dict(version=(R/'VERSION').read_text().strip(), ROM_sha256=hashlib.sha256(source).hexdigest(),
        emulator='native mGBA core', variant='Release' if 'release' in args.rom.name else 'Debug',
        passed=True, codec_verification=codec, scope='Both TV choices; actual roamer battles with escape/capture/KO, partner unlock and independent resolution. Synthetic legacy/current actual flash write/load and repeated initialization with native slot, 992-byte prefix, party, Bag and season retained.',
        limits='Not an uninterrupted story playthrough, authentic historical save or Pizza Boy test.',
        log=(out/'emulator.log').read_text(),
        harness_sha256={n:hashlib.sha256((S/n).read_bytes()).hexdigest() for n in ['arm.c','host.c','run.py']},
        images={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.png')})
    (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    private.unlink()
    print('PASS: native dual Eon battles/persistence. '+str(out))

if __name__ == '__main__': main()
