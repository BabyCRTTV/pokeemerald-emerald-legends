#!/usr/bin/env python3
"""Controlled mGBA journal selection QA; requires a built Debug/Release ELF/ROM and libmgba.

Run from anywhere: python3 tools/legends/native_journal_qa/run.py --output /tmp/journal-qa
Optional --mgba-prefix /path/to/usr for an extracted libmgba development package.
ARM tools are resolved from PATH. Output contains a private modified ROM: never distribute it.
"""
import argparse,hashlib,json,os,subprocess
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[3]

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--mgba-prefix',type=Path)
    parser.add_argument('--variant',choices=['Debug','Release'],default='Debug')
    args=parser.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    source=Path(__file__).resolve().parent;env=os.environ.copy()
    stem="pokeemerald-release" if args.variant=="Release" else "pokeemerald"
    elf=stem+".elf";rom_path=ROOT/(stem+".gba")
    def run(command,log):
        with (out/log).open('w') as f:
            subprocess.run(command,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
    nm=subprocess.check_output(['arm-none-eabi-nm',elf],cwd=ROOT,env=env,text=True)
    symbols={p[2]:int(p[0],16) for line in nm.splitlines() if len(p:=line.split())==3}
    assert symbols['gMain']<0x03008000
    for name in ['sSelected','sTop','sDetail']:
        if name not in symbols:
            symbols[name]=symbols[name+'.lto_priv.0']
    arm_source=source/('arm_release.c' if args.variant=='Release' else 'arm.c')
    fixture_flags=[]
    if args.variant=='Release':
        fixture_flags=['-DQA_QUESTS_ADDRESS='+hex(symbols['sQuests']),
                       '-DQA_QUEST_COUNT='+str(len(json.loads((ROOT/'data/legends/quests.json').read_text())))]
    run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols='+elf,*fixture_flags,str(arm_source),'-o',str(out/'arm.elf')],'arm-build.log')
    run(['arm-none-eabi-objcopy','-O','binary',str(out/'arm.elf'),str(out/'arm.bin')],'objcopy.log')
    rom=bytearray(rom_path.read_bytes());arm=(out/'arm.bin').read_bytes()
    assert len(arm)<0x10000 and set(rom[0x1f80000:0x1f80000+len(arm)])=={255}
    # Mailbox is below the GBA EWRAM end but above this project's linked allocation.
    rom[0x1f80000:0x1f80000+len(arm)]=arm;(out/'private-journal.gba').write_bytes(rom)
    command=['cc',str(source/'host.c'),'-o',str(out/'host')]
    if args.mgba_prefix:
        prefix=args.mgba_prefix.resolve()
        command+=['-I'+str(prefix/'include'),'-I'+str(prefix/'include/x86_64-linux-gnu'),'-L'+str(prefix/'lib/x86_64-linux-gnu')]
        env['LD_LIBRARY_PATH']=str(prefix/'lib/x86_64-linux-gnu')+':'+env.get('LD_LIBRARY_PATH','')
    command+=['-lmgba'];run(command,'host-build.log')
    run([str(out/'host'),str(out/'private-journal.gba'),str(out),hex(symbols['gMain']),hex(symbols['sSelected']),hex(symbols['sTop']),hex(symbols['sDetail'])],'emulator.log')
    captures=[]
    for raw in sorted(out.glob('*.rgba')):
        im=Image.frombytes('RGBA',(240,160),raw.read_bytes()).convert('RGB')
        im.save(out/(raw.stem+'.png'))
        # Confirm a dark, continuous row and a separate cream pointer in native video.
        if raw.stem not in ['quest-detail','achievement-detail','achievement-claim-popup','achievement-claimed-status']:
            row=5 if raw.stem in ['quest-scrolled','quest-return'] else 1 if raw.stem.endswith('second') or raw.stem=='achievement-return' else 0
            y=40+row*15
            dark=im.getpixel((235,y+1));paper=im.getpixel((239,80))
            assert max(dark)<max(paper)-40, (raw.stem,dark,paper)
            assert im.getpixel((8,y+5))==paper and im.getpixel((11,y+5))==dark
            assert im.getpixel((14,y+6))==paper
        # First-open captures must include the complete screen and footer.
        assert im.getpixel((239,159)) == (255,239,198), raw.stem
        captures.append({'name':raw.stem,'sha256':sha(out/(raw.stem+'.png'))})
    assert (out/'quest-return.rgba').read_bytes()==(out/'quest-scrolled.rgba').read_bytes()
    assert (out/'achievement-return.rgba').read_bytes()!=(out/'achievement-second.rgba').read_bytes()
    # Narrow, lossless phone-friendly preview of two actual emulator screens.
    sheet=Image.new('RGB',(480,672),(31,25,38))
    for i,name in enumerate(['quest-second','achievement-second']):
        image=Image.open(out/(name+'.png')).resize((480,320),Image.Resampling.NEAREST)
        sheet.paste(image,(0,8+i*336))
    sheet.save(out/'journal-v0.0.56-preview.png')
    proof={'version':(ROOT/'VERSION').read_text().strip(),'variant':args.variant,'ROM_sha256':sha(rom_path),'emulator':'mGBA 0.10.2','captures':captures,'passed':True,'fixture':('Release seeds quest flags/journal/one claimed entry directly because LTO internalizes Debug setup helpers; the next manual claim uses actual game input.' if args.variant=='Release' else 'Debug sets quest flags and initializes/claims the first achievement through native functions.'),'scope':'Controlled ARM callback opened the actual journal with quest flags set. Emulated keys drove native tasks, scrolling, details/back, filters and Achievements with a claimed reward. Claims and confirmation timeout use actual emulated input. Not natural map traversal or historical-save loading. Private ROM excluded from publication.','harness_sha256':{f:sha(source/f) for f in ['arm.c','arm_release.c','host.c','run.py']}}
    (out/'verification.json').write_text(json.dumps(proof,indent=2)+'\n')
    print(json.dumps(proof,indent=2))

if __name__=='__main__':main()
