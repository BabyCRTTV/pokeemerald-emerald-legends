"""Explicit review-only polish; touches five Wyrmtide layout binaries only.

Uses exact native Sealed Chamber perimeter assemblies. Refuses unknown inputs so
subsequent Porymap edits cannot be silently regenerated.
"""
from pathlib import Path
import struct, hashlib
R=Path(__file__).resolve().parents[2]
def cells(p):
 b=p.read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
BASELINE={'Descent1': 'c2f1f0f9621208b8da55ef94883530c5e7a370903ed14f3b4239c5a44c80bf84', 'Descent2': '211fdeac53115a9489345d03b878f1363681ff90acc86b38980dfbbdc96f1515', 'Descent3': '0e3f2a58ab6549e89afd195bc5dc094628bbc603aa3f8952e98b05f74e261627', 'Descent4': '8622dfe64521af0f2f471df07322bd19a9f6b569328a7c7039d143aa03ef156c', 'Heart': 'fde183196b5e3faab14b3733b6344fbd0af89acfbd5107a59fe3b85d8e8fbb56'}
# Validate all five inputs before writing any map.
for key,digest in BASELINE.items():
 assert hashlib.sha256((R/f"data/layouts/LegendsWyrmtide_{key}/map.bin").read_bytes()).hexdigest()==digest, "Map changed; preserve edits and review: "+key
native=cells(R/'data/layouts/SealedChamber_InnerRoom/map.bin')
for name in ['Descent1','Descent2','Descent3','Descent4','Heart']:
 p=R/f'data/layouts/LegendsWyrmtide_{name}/map.bin'
 a=cells(p);w,h=(23,21) if name=='Heart' else (19,24)
 def frame(inset=0):
  # Copy full native corner assemblies and extend only straight spans.
  rw=w-2*inset
  for y in range(h):
   sy=y if y<5 else (y-h+23 if y>=h-5 else 9)
   for x in range(w):
    rx=x-inset
    if rx<0 or rx>=rw:
     a[y*w+x]=0x36f1
     continue
    sx=rx if rx<4 else (rx-rw+21 if rx>=rw-4 else 6)
    v=native[sy*21+sx]
    if rx<3 or rx>=rw-3 or y<3 or y>=h-3 or (rx in [3,rw-4] and (y<5 or y>=h-5)):
     a[y*w+x]=(v&1023)|0x3400
 frame(3 if name=='Heart' else 0)
 if name!='Heart':
  # Existing warp approaches retain their exact coordinates and behavior.
  a[2*w+8]=0x339f;a[3*w+8]=0x339e
 else:
  def put(x,y,t,solid=False):a[y*w+x]=t|0x3000|(0x400 if solid else 0)
  # Dry sanctuary: replace only the old pool/column/terrace footprints.
  for x1,y1,x2,y2 in [(3,8,7,12),(15,8,19,12),(8,12,14,14),(6,4,6,5),(16,4,16,5),(6,14,6,15),(16,14,16,15)]:
   for y in range(y1,y2+1):
    for x in range(x1,x2+1):put(x,y,0x201)
  frame(3)
  # Integrate the inscription into the rear rock face, using the original
  # Sealed Chamber five-cell tablet assembly (native cells 8..12).
  for y in range(3):
   for x in range(5):put(9+x,2+y,native[(2+y)*21+8+x]&1023,True)
  for x,y in [(6,12),(16,12)]:put(x,y,0x2d5,True)
  for x,y in [(6,15),(16,15)]:put(x,y,0x203,True)
  put(11,16,0x39F);put(11,17,0x39E)
 p.write_bytes(struct.pack('<%dH'%len(a),*a))
print('Polished Wyrmtide cave layouts; scripts, events, shared art and island unchanged.')
