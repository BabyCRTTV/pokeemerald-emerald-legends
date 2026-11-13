from pathlib import Path
from subprocess import run,check_output
from ctypes import *
from PIL import Image
import struct
import os
S = Path(__file__).resolve().parents[1] / 'native_poffin_qa'
R = S.parents[2]
os.chdir(R)
Q = R / 'build/berry-season'
Q.mkdir(parents=True, exist_ok=True)
E = R / 'pokeemerald.elf'
run(['cc', '-shared', '-fPIC', str(S/'core.c'), '-lmgba', '-o', str(Q/'core.so')], check=True)
# The fixture only establishes the party, berries and starting location.
# All actions after that use the emulated controller.
def syms(p):
 return {v[2]:int(v[0],16) for l in check_output(['arm-none-eabi-nm',str(p)],text=True).splitlines() if len(v:=l.split())==3}
run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols='+str(E),str(R/'tools/legends/native_berry_palette_qa/arm.c'),'-o',str(Q/'arm.elf')],check=True)
run(['arm-none-eabi-objcopy','-O','binary',str(Q/'arm.elf'),str(Q/'arm.bin')],check=True)
r=bytearray((R/'pokeemerald.gba').read_bytes());b=(Q/'arm.bin').read_bytes();assert set(r[0x1f80000:0x1f80000+len(b)])=={255};r[0x1f80000:0x1f80000+len(b)]=b;(Q/'private.gba').write_bytes(r)
sy=syms(E);qa=syms(Q/'arm.elf')['qa']|1;c=CDLL(str(Q/'core.so'));c.screen.restype=c_void_p;c.rd.restype=c_uint
assert c.init(bytes(Q/'private.gba')); (Q/'private.gba').unlink();step=c.step;step(500,0);g=sy['gMain'];box=0x0203ffc0
def cmd(i):
 old=c.rd(g+4);c.wr(box,i);c.wr(box+12,old);c.wr(box+16,0);c.wr(g+4,qa);step(150 if i==2 else 1,0)
 for n in range(10):
  if c.rd(box+16):break
  c.wr(g+4,qa);step(150 if i==2 else 1,0)
 assert c.rd(box+16)
def cap(name):
 im=Image.frombytes('RGBA',(240,160),string_at(c.screen(),240*160*4)).convert('RGB');im.resize((720,480),Image.Resampling.NEAREST).save(Q/(name+'.png'))
def key(k,wait=36):step(3,k);step(wait,0)

import json, hashlib
results=[]
for season,name in enumerate(["spring","summer","autumn","winter"]):
 for stage in range(1,8):
  c.wr(box+4, stage != 5); c.wr(box+8,stage)
  c.wr(g,0);cmd(season);step(430,0)
  if stage == 5: cap("after-"+name)
  cmd(10)
  checked,errors=c.rd(box+20),c.rd(box+24)
  assert checked >= 3 and errors == 0, (name,stage,checked,errors)
  results.append(dict(season=name,stage=stage,plants=checked,mismatchedColors=errors))
(Q/'results.json').write_text(json.dumps(dict(romSha256=hashlib.sha256((R/'pokeemerald.gba').read_bytes()).hexdigest(),checks=results),indent=2)+'\n')
print('PASS: all seven growth stages in all four seasons, native OBJ palette comparisons')
