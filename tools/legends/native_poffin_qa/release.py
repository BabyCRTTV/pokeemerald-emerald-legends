"""Read-only checks after normal Continue in the unmodified Release ROM."""
from pathlib import Path
from subprocess import check_output, run
from ctypes import CDLL,c_uint
import hashlib,json
root=Path(__file__).resolve().parents[3]
source=Path(__file__).resolve().parent
out=root/'build/treat-case-native'
rom=root/'pokeemerald-release.gba'
original=rom.read_bytes()
sy={p[2]:int(p[0],16) for line in check_output(['arm-none-eabi-nm',str(root/'pokeemerald-release.elf')],text=True).splitlines() if len(p:=line.split())==3}
run(['cc','-shared','-fPIC',str(source/'core.c'),'-lmgba','-o',str(out/'release-core.so')],check=True)
c=CDLL(str(out/'release-core.so'));c.rd.restype=c_uint
assert c.init(bytes(rom))
assert c.load_battery(bytes(out/'private-full-case.sav'))
c.reset();c.step(500,0)
for _ in range(50):
    if c.rd(sy['gMain']+4)==sy['CB2_Overworld']|1: break
    c.step(3,1);c.step(150,0)
assert c.rd(sy['gMain']+4)==sy['CB2_Overworld']|1
c.step(180,0)
address=c.rd(sy['gSaveBlock3Ptr'])+1032
actual=b''.join(c.rd(address+i).to_bytes(4,'little') for i in range(0,284,4))
expected=(0x31464650).to_bytes(4,'little')+b''.join(bytes([15+i%5,15,9,7,5,3,20]) for i in range(40))
assert actual==expected
assert rom.read_bytes()==original
receipt={'passed':True,'version':(root/'VERSION').read_text().strip(),'rom_sha256':hashlib.sha256(original).hexdigest(),'ROM_unmodified':True,'RAM_writes':False,'checks':['normal Release Continue','all 40 exact Poffin records retained'],'limits':'Controlled Debug-generated battery, not a historical owner save.'}
(out/'release-verification.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
