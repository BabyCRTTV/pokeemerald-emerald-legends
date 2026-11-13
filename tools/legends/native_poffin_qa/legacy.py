"""Optional pre-case ROM battery migration check; baseline binaries remain private.
Run after run.py with build/poffin-native/legacy/pokeemerald.{gba,elf} present.
"""
from pathlib import Path
from subprocess import check_output
import hashlib
import json

root = Path(__file__).resolve().parents[3]
source = Path(__file__).resolve().parent
output = root / 'build/treat-case-native'
prefix = (source / 'run.py').read_text().split('# Fresh trainer, party and berries.')[0]
old = check_output(['git','show','714669411aa84f1d2efbcd37599854d95e693c14:tools/legends/native_poffin_qa/arm.c'], cwd=root,text=True)
old = old.replace('#include "pokeblock.h"','#include "pokeblock.h"\n#include "constants/vars.h"')
old = old.replace('    if (b[0] == 2)', '''    if (b[0] == 3)
    {
        gSaveBlock1Ptr->pokeblocks[0] = (struct Pokeblock){POFFIN_DRY,8,21,0,0,0,25};
        gSaveBlock1Ptr->pokeblocks[1] = (struct Pokeblock){PBLOCK_CLR_RED,10,0,0,0,0,20};
        VarSet(VAR_LEGENDS_HAIR, 2);
        VarSet(VAR_LEGENDS_SEASON_MODE, 1);
        VarSet(VAR_LEGENDS_SEASON_CLOCK_INIT, 1);
        b[10] = TrySavingData(SAVE_NORMAL);
    }
    if (b[0] == 2)''')
(output / 'legacy-arm.c').write_text(old)

def stage(legacy):
    code = prefix
    if legacy:
        code = code.replace('mailbox = 0x0203fd00', 'mailbox = 0x0203ffc0')
        code = code.replace('number == 2', 'number in (2, 3)')
        code = code.replace('ROOT / "pokeemerald.elf"','ROOT / "build/poffin-native/legacy/pokeemerald.elf"').replace('ROOT / "pokeemerald.gba"','ROOT / "build/poffin-native/legacy/pokeemerald.gba"')
        code = code.replace('str(SOURCE / "arm.c")','str(OUTPUT / "legacy-arm.c")')
    ns = {'__file__': str(source / 'run.py')}
    exec(code,ns)
    return ns

oldns=stage(True)
oldns['frames'](500)
oldns['core'].wr(oldns['main'],0)
oldns['command'](0)
oldns['frames'](430)
oldns['command'](3)
oldns['frames'](180)
assert oldns['value'](10)==1
battery=output/'pre-case.sav'
assert oldns['core'].battery(bytes(battery))
oldhash=hashlib.sha256(oldns['original']).hexdigest()
ns=stage(False)
c=ns['core']
assert c.load_battery(bytes(battery))
c.reset()

def continue_game():
    ns['frames'](500)
    for _ in range(50):
        if ns['callback']('CB2_Overworld'):
            break
        ns['key'](1,150)
    assert ns['callback']('CB2_Overworld'), 'Continue did not return to field'
    ns['frames'](180)
    ns['command'](1)
    assert tuple(ns['value'](i) for i in (5,6,7,8,9,14)) == (3,2,16,8,21,0)
    # Query only: preserved native block, hairstyle, season and party.
    assert tuple(ns['value'](i) for i in (16,17,18,19)) == (1,2,1,255)

continue_game()
ns['command'](2)
assert ns['value'](10)==ns['value'](11)==1
c.reset()
continue_game()
receipt={'passed':True,'baseline_rom_sha256':oldhash,'target_rom_sha256':hashlib.sha256(ns['original']).hexdigest(), 'tests':['older-format battery Continue','Poffin migrated with exact flavors','ordinary Pokeblock preserved','hairstyle and season preserved','Torchic and berries preserved','new save reset Continue'], 'limits':'Synthetic baseline-build battery, not an authentic historical player save.'}
(output/'legacy-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
