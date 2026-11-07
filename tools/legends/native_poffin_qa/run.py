from pathlib import Path
from subprocess import run,check_output
from ctypes import *
from PIL import Image
import struct
import os
S = Path(__file__).resolve().parent
R = S.parents[2]
os.chdir(R)
Q = R / 'build/poffin-native'
Q.mkdir(parents=True, exist_ok=True)
E = R / 'pokeemerald.elf'
run(['cc', '-shared', '-fPIC', str(S/'core.c'), '-lmgba', '-o', str(Q/'core.so')], check=True)
# The fixture only establishes the party, berries and starting location.
# All actions after that use the emulated controller.
def syms(p):
 return {v[2]:int(v[0],16) for l in check_output(['arm-none-eabi-nm',str(p)],text=True).splitlines() if len(v:=l.split())==3}
run(['arm-none-eabi-gcc','-iquote','include','-iquote','.', '-DMODERN=1','-DEMERALD','-mthumb','-mcpu=arm7tdmi','-mabi=apcs-gnu','-Os','-ffreestanding','-fno-builtin','-fno-jump-tables','-nostdlib','-Wl,-Ttext=0x09f80000','-Wl,--entry=qa','-Wl,--just-symbols='+str(E),str(S/'arm.c'),'-o',str(Q/'arm.elf')],check=True)
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
c.wr(g,0);cmd(0);step(430,0);key(64);cap('01-Machine');key(1,130);cap('intro')

# Enter the machine, choose the first berry, then accept the optional second.
key(1,85);key(1,180);key(1,200);cap('second-ready')
key(1,210);cap('second-bag');key(128,20);key(1,210);cap('02-Stirring')
addr=sy['sBatch']; frame=lambda: c.rd(addr+4)&65535
print('start',hex(c.rd(addr)),frame(),flush=True)
assert c.rd(addr)&65535 and c.rd(addr)>>16
step(100,0);clock=[64,16,128,32];i=0;seen=set()
while frame()<1080 and i<400:
 f=frame()
 if 360<=f<530 and 'burn' not in seen:
  step(150,0);cap('03-Burn-Warning');seen.add('burn')
 elif f<360:
  step(9,clock[i%4])
 elif f<720:
  step(8,clock[-i%4])
 else:
  step(6,clock[i%4])
 i+=1
step(30,0);cap('04-Baked-Poffin');cmd(1);counts=[c.rd(box+4*i) for i in range(5,10)]
print('cooked',counts,flush=True);assert counts[:3]==[2,1,15] and counts[3] and counts[4]
key(1,190);cmd(2)
assert c.rd(box+28)==15 and c.rd(box+32)==counts[3] and c.rd(box+36)==counts[4]
print('battery round trip',c.rd(box+40),c.rd(box+44),flush=True)
key(1,170);key(128,20);key(1,150);key(1,160);cap('05-Treat-Case')
key(1,60);key(1,200);cap('party');key(1,150);cap('offer');key(1,180);step(110,0);cap('feeding');key(1,220);key(1,220);cap('fed')

cmd(1);print("fed", [c.rd(box+4*i) for i in (7,12,13)],flush=True);assert c.rd(box+48) and c.rd(box+52)
for k in range(10):
 key(1,100)
 cmd(1)
 if c.rd(box+28)==0:break
assert c.rd(box+28)==0
print('consumed one treat; party retained both gains')
