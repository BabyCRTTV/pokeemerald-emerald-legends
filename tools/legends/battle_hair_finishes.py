"""Small, authored finishes for the two tied May battle hairstyles.

Coordinates use the four native 64x64 poses, never the presentation sheet.
The rear braid hangs behind native anatomy; the front braid stays in front.
These finishes are baked into the checked-in 4bpp bank, not drawn at runtime.
"""

# wind-up, cast, release, idle. The red band fills the bottom of each
# crown/tail notch and uses fixed uniform colors, not skin or hair slots.
PONYTAIL_TIES = ((18,26),(24,25),(12,27),(20,25))
TIE = ('.OO.', 'ORRO', 'OrRO', 'OrrO', '.OO.')

# Keep the approved crown/front braid. Retire just the outward rear lock.
# (first row, last column) boundaries follow the original rear/crown join.
BRAID_CUTS = (((38,22),), ((38,26),),
              ((40,6),(42,9),(44,12)), ((37,20),))
BRAID_ROOTS = ((16,37),(21,37),(3,40),(15,36))

# Alternating woven lobes taper downward, with a small curved tip. The
# release pose trails by one extra pixel; the resting braid falls straight.
BRAID = ('..OOO..', '.ODDHO.', '.ODMHHO', '.ODMHHO', '.ODMMHO',
         '..ODDO.', '..ODMO.', '.ODMHO.', '.ODMHHO', '.ODMMHO',
         '..ODDO.', '..ODMO.', '..ODMHO', '..ODHHO', '..ODMHO',
         '...ODDO', '...ODMO', '...OMHO', '...ODMO', '....OO.')
MATERIALS = {'O':15, 'D':4, 'M':7, 'H':11, 'R':13, 'r':12}

def finish(mask, name, pose, base):
    """Finish only Ponytail/Twin Braids; leave the other eight cuts intact."""
    if name == 'ponytail':
        left,top=PONYTAIL_TIES[pose]
        for dy,row in enumerate(TIE):
            for dx,v in enumerate(row):
                if v!='.':mask[left+dx,top+dy]=MATERIALS[v]
    elif name == 'twin_braids':
        for q in list(mask):
            if any(q[1]>=row and q[0]<=col for row,col in BRAID_CUTS[pose]):
                del mask[q]
        left,top=BRAID_ROOTS[pose]
        for dy,row in enumerate(BRAID):
            # Slight lag during the release rather than a rigid lateral lock.
            sway=-1 if pose==2 and dy>=10 else 0
            for dx,v in enumerate(row):
                x,y=left+dx+sway,top+dy
                if v!='.' and base[y][x]==0:
                    mask[x,y]=MATERIALS[v]

