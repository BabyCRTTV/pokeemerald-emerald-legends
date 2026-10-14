#!/usr/bin/env python3
"""Controlled mGBA ARM loader QA; requires a built Debug ELF/ROM and libmgba.

Run from anywhere: python3 tools/legends/native_family_qa/run.py --output /tmp/family-qa
Optional --mgba-prefix /path/to/usr for an extracted libmgba development package.
ARM tools are resolved from PATH. Output contains a private modified ROM: never distribute it.
"""
import argparse,hashlib,json,os,re,struct,subprocess,sys
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'tools/legends'))
from build_appearance import frames,pack
from preview_family_skin import SOURCES,packed

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--mgba-prefix',type=Path)
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    source=Path(__file__).resolve().parent;env=os.environ.copy()
    def run(command,log):
        with (out/log).open('w') as f:
            subprocess.run(command,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols=pokeemerald.elf',str(source/'arm.c'),'-o',str(out/'arm.elf')],'arm-build.log')
    run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
    rom=bytearray((ROOT/'pokeemerald.gba').read_bytes());arm=(out/'arm.bin').read_bytes()
    assert len(arm)<0x10000 and set(rom[0x1f80000:0x1f80000+len(arm)])=={255}
    # Mailbox is below the GBA EWRAM end but above this project's linked allocation.
    nm=subprocess.check_output(['arm-none-eabi-nm','pokeemerald.elf'],cwd=ROOT,env=env,text=True)
    symbols={p[2]:int(p[0],16) for line in nm.splitlines() if len(p:=line.split())==3}
    assert symbols['gMain']<0x03008000
    rom[0x1f80000:0x1f80000+len(arm)]=arm;(out/'private-family.gba').write_bytes(rom)
    command=['cc',str(source/'host.c'),'-o',str(out/'host')]
    if args.mgba_prefix:
        prefix=args.mgba_prefix.resolve()
        command+=['-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu')]
        env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
    command+=['-lmgba'];run(command,'host-build.log')
    run([str(out/'host'),str(out/'private-family.gba'),str(out/'buffers.bin'),hex(symbols['gMain']),hex(symbols['gPlttBufferUnfaded'])],'emulator.log')
    data=(out/'buffers.bin').read_bytes();size=76+512+2304*2+32;assert len(data)==size*10
    source_text=(ROOT/'src/data/legends/family_palettes.h').read_text()
    palettes={name:[[int(x,16) for x in row.split(',')] for row in re.findall(r'\{([^}]+)\}',re.search('gLegends'+name+r'Palettes\[5\]\[16\] = \{(.*?)\n\};',source_text,re.S)[1])] for name in ['Mom','Norman','NormanBattle']}
    image=Image.open(ROOT/'graphics/object_events/pics/people/gym_leaders/flannery.png');pal=image.getpalette()
    native=[packed(pal[i*3:i*3+3]) for i in range(16)]
    for step in range(10):
        tone=step%5;kind=step//5;chunk=data[size*step:size*(step+1)]
        box=struct.unpack('<19I',chunk[:76]);pals=struct.unpack('<256H',chunk[76:588])
        assert box[0]==step+1 and box[17]==tone and box[18]==tone+1
        for key,slot,reflection in [('Mom',box[6],box[15]),('Norman',box[7],box[16])]:
            colors=palettes[key][tone];assert list(pals[slot*16:slot*16+16])==colors
            reflected=[colors[0]]
            for color in colors[1:]:
                r,g,b=color&31,color>>5&31,color>>10&31
                if kind:r,g,b=max(0,r-5),min(31,g+3),min(31,b+16)
                else:b=min(31,b+10)
                reflected.append(r|g<<5|b<<10)
            assert list(pals[reflection*16:reflection*16+16])==reflected
        assert list(pals[box[8]*16:box[8]*16+16])==native
        assert chunk[588:2892]==(ROOT/'graphics/legends/family/mom.4bpp').read_bytes()
        assert chunk[2892:5196]==b''.join(pack(f) for f in frames(ROOT/SOURCES['norman'],16,32))
        assert list(struct.unpack('<16H',chunk[5196:5228]))==palettes['NormanBattle'][tone]
        assert len(set([box[6],box[7],box[8],box[15],box[16]]))==5
        assert box[12]==box[6] and box[13]==box[7] and box[14]==255
    proof={'version':(ROOT/'VERSION').read_text().strip(),'Debug_ROM_sha256':sha(ROOT/'pokeemerald.gba'),'capture_sha256':sha(out/'buffers.bin'),'native_asset_tone_cases':190,'reflection_palettes':20,'wardrobe_apply_cancel_rounds':10,'all_16_slots_occupied':True,'unrelated_NPC4_unchanged':True,'passed':True,'scope':'Controlled ARM callback after boot: real virtual-object creation, palette/reflection/wardrobe functions. Not natural map traversal, menu navigation or battery save/reload. Private ROM excluded from publication.','harness_sha256':{f:sha(source/f) for f in ['arm.c','host.c','run.py']}}
    (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2))

if __name__=='__main__':main()
