"""Explicit Wyrmtide review edit; shared/native assets and the approved Heart stay exact.

Reference complete vanilla Regi entrances, Dewford/Route 106 vegetation setbacks,
and Sealed Chamber ledges. Validate all inputs before writing to protect later
Porymap work. This is deliberately separate from routine map generation.
"""
from pathlib import Path
import hashlib,json,struct
R=Path(__file__).resolve().parents[2]
KEYS=['Isle','Descent1','Descent2','Descent3','Descent4']
BASE={'Isle': '41ee191b5ae7bad19234834a06fcfa9567b6a01c2784511dc818723b7609d928', 'Descent1': 'c616b98ab68695d07c2c4a888eafdcca9b86dede0e1588ef162d62ba6864331b', 'Descent2': '51eb5a336a65c66d828991042fd6dffdaf5b4eff17573144cd4197aeff3433bd', 'Descent3': 'd96e6b6737f6ff75c461fe7324099e9afb01534c5763716c9ca8a3a477cfff5b', 'Descent4': 'cd4d4a96ac96a0a8797ab020a69bcc9877f2d33269d56f12f94497b9d733fd81'}
def raw_path(k):return R/f'data/layouts/LegendsWyrmtide_{k}/map.bin'
def read(k):
 b=raw_path(k).read_bytes();return list(struct.unpack('<%dH'%(len(b)//2),b))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Pin to the review source, so owner edits require reconciliation, not regeneration.
for k in KEYS:assert sha(raw_path(k))==BASE[k],f'Preserve changed map and reconcile: {k}'
heart=raw_path('Heart').read_bytes()
for key in KEYS:
 a=read(key);w,h=(34,29) if key=='Isle' else (19,24)
 def put(x,y,t,solid=False,elev=3):a[y*w+x]=t|(0x400 if solid else 0)|(elev<<12)
 def fill(x1,y1,x2,y2,t,solid=False):
  for y in range(y1,y2+1):
   for x in range(x1,x2+1):put(x,y,t,solid)
 def ledge(x1,y1,x2,y2):
  fill(x1,y1,x2,y2,0x211,True)
  for x in range(x1+1,x2):put(x,y1,0x209,True);put(x,y2,0x219,True)
  for y in range(y1+1,y2):put(x1,y,0x210,True);put(x2,y,0x212,True)
  for x,y,t in [(x1,y1,0x208),(x2,y1,0x20a),(x1,y2,0x218),(x2,y2,0x21a)]:put(x,y,t,True)
 def tablet(x1,y1,x2):
  for x in range(x1,x2+1):put(x,y1,0x209,True);put(x,y1+1,0x235,True)
  for x,y,t in [(x1,y1,0x208),(x2,y1,0x20a),(x1,y1+1,0x218),(x2,y1+1,0x21a)]:put(x,y,t,True)
 def steps(x,y,width=2):fill(x,y,x+width-1,y+1,0x39f)
 if key=='Isle':
  # Restore only old tree/headland/column footprints to their native shoreline.
  shore={3:(13,21),4:(10,24),5:(8,26),6:(7,27),7:(6,28),8:(5,28),9:(5,28),10:(5,28),11:(5,28),12:(5,28),13:(5,28),14:(5,28),15:(6,28),16:(6,28),17:(7,28),18:(7,27),19:(7,27),20:(7,26),21:(9,25),22:(9,24),23:(11,22),24:(13,20)}
  land={(x,y) for y,(l,r) in shore.items() for x in range(l,r+1)}
  def beach(x,y):
   if (x,y) not in land:put(x,y,0x170,elev=1);return
   n,e,s,v=[(x+dx,y+dy) in land for dx,dy in [(0,-1),(1,0),(0,1),(-1,0)]]
   if not n:t=0x11b if not v else 0x11d if not e else 0x11c
   elif not s:t=0x12b if not v else 0x12d if not e else 0x12c
   elif not v:t=0x123
   elif not e:t=0x125
   elif (x-1,y-1) not in land:t=0x13d
   elif (x+1,y-1) not in land:t=0x13e
   elif (x-1,y+1) not in land:t=0x145
   elif (x+1,y+1) not in land:t=0x146
   else:t=0x124
   put(x,y,t)
  old_trees=[(6,11),(7,13),(8,11),(26,11),(27,13),(25,16),(26,19),(10,21)]
  for x,y in old_trees:
   for yy in [y,y+1]:beach(x,yy)
  for y in range(4,11):
   for x in range(8,26):beach(x,y)
  for x in [14,18]:
   for y in [11,12]:beach(x,y)
  # Vanilla Desert Ruins 5x4 rock geometry. All surrounding cells are
  # beach, matching its sand feet; closed/open seal coordinates remain 16,9/10.
  dome=[[0x124,0x080,0x081,0x0a4,0x124],
        [0x080,0x073,0x071,0x075,0x0a4],
        [0x088,0x07b,0x07c,0x07d,0x08a],
        [0x090,0x079,0x079,0x079,0x092]]
  for dy,row in enumerate(dome):
   for dx,t in enumerate(row):put(14+dx,7+dy,t,t!=0x124)
  # Native sand-backed Dewford trees are wholly inland; no tile replaces surf.
  for x,y in [(9,11),(11,12),(24,9),(26,11),(24,17)]:
   assert all((x+dx,yy) in land for yy in range(y-1,y+3) for dx in [-1,0,1])
   put(x,y,0x239,True);put(x,y+1,0x23a,True)
  # The old southwest boulder also replaced a shoreline cap. Restore that
  # cap and move the rock onto a complete interior sand cell.
  beach(8,20)
  for x,y in [(10,19),(12,12),(20,12),(13,6),(20,6)]:put(x,y,0x0e2,True)
  for y in range(h):
   for x in range(w):
    if a[y*w+x]&1023 in [0x239,0x23a,0x0e2]:
     assert all((x+dx,y+dy) in land for dx,dy in [(0,0),(-1,0),(1,0),(0,-1),(0,1)]), 'Decoration replaces a shoreline cap'
 else:
  # Retain the complete reviewed perimeter and clear only the interior floor.
  fill(3,4,15,20,0x201)
  fill(4,3,14,3,0x201)
  if key=='Descent1':
   tablet(6,6,10)
   ledge(3,9,15,10);steps(12,9)
   ledge(3,15,15,16);steps(5,15)
   for x,y in [(4,5),(14,5),(4,19)]:put(x,y,0x2d5,True)
  elif key=='Descent2':
   # One modest rounded tidal basin, separated from the stair by dry floor.
   from build_wyrmtide_tilesets import POOL_IDS
   x1,y1,x2,y2=11,6,15,10
   fill(x1,y1,x2,y2,0x27b,True)
   for x in range(x1+1,x2):put(x,y1,POOL_IDS[0x291],True);put(x,y2,POOL_IDS[0x26b],True)
   for y in range(y1+1,y2):put(x1,y,POOL_IDS[0x28a],True);put(x2,y,POOL_IDS[0x288],True)
   for x,y,t in [(x1,y1,0x289),(x2,y1,0x281),(x1,y2,0x26c),(x2,y2,0x26a)]:put(x,y,POOL_IDS[t],True)
   ledge(3,9,10,10);steps(5,9)
   tablet(10,15,14)
   for x,y in [(4,5),(4,15),(14,19)]:put(x,y,0x2d5,True)
  elif key=='Descent3':
   ledge(3,7,15,8);steps(12,7)
   ledge(3,13,15,14);steps(5,13)
   for x,y in [(4,5),(14,5),(4,18)]:put(x,y,0x2d5,True)
  else:
   # Dry final procession: two short, complete ledges replace the tall water
   # boxes and floating vertical wall strips. Central steps lead onward.
   ledge(3,7,15,8);steps(8,7,3)
   ledge(3,13,15,14);steps(8,13,3)
   for x,y in [(5,5),(13,5),(5,17),(13,17)]:put(x,y,0x2d5,True)
  if key in ['Descent1','Descent3']:tablet(12,17,14)
  # Preserve all existing map-warp behavior and both explicit approach cells.
  put(8,2,0x39f);put(8,3,0x39e)
  # A complete rock mouth prevents sideways entry into the stair warp.
  put(10,20,0x218,True);put(12,20,0x21a,True)
  put(11,19,0x39f);put(11,20,0x39e)
 raw_path(key).write_bytes(struct.pack('<%dH'%len(a),*a))
assert raw_path('Heart').read_bytes()==heart,'Approved chamber must remain exact'
print('Refined shore/entrance and four landings. Approved Heart and shared assets retained.')
