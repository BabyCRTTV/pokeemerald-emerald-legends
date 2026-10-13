"""Individually authored male rear walking/running crowns on the native 16px grid.

Rows end at the native nape and follow its vertical walking/running bob. Hair
uses the existing two recolorable shades, dark edge shade and native outline.
The native ears and the neck/body below the nape remain the source of truth.
"""

COLORS = {'.': 0, '#': 15, 's': 8, '+': 4, 'H': 7, 'R': 13, 't': 2, 'u': 3}

# Fourteen rows, centered around x=7.5. Empty leading rows set each cut's
# height; the common final row sits directly above the native neck.
BACKS = (
    # Crew Cut: close cropped dome and a short, even nape.
    (
        '', '', '',
        '     ######',
        '    #HHH++s#',
        '   #HHHH+++s#',
        '  #HHH++++++s#',
        '  #HH+++++++s#',
        '  #H++++++++s#',
        '  #++++++++ss#',
        '  #s++++++sss#',
        '   #s++++sss#',
        '   #ssssssss#',
        '     ######',
    ),
    # Side Part: two connected masses separated by a diagonal part.
    (
        '', '',
        '      #####',
        '    ##HH++s#',
        '   #HHHHs++s#',
        '  #HHHHs++H+s#',
        '  #HHHs++HH+s#',
        '  #HHs+++HH+s#',
        '  #Hs++++H+ss#',
        '  #s+++++++ss#',
        '   #++++++ss#',
        '   #s+++++ss#',
        '   #ss+++sss#',
        '     ######',
    ),
    # Spiky: distinct connected tips and a textured taper.
    (
        '',
        '        #',
        '    #  #H#  #',
        '   #H##HHH##H#',
        '  #HHHHHH++++s#',
        '   #HHH++HH+s#',
        '  #HH+++HH+++s#',
        '   #+++H++++s#',
        '  #++++++H++ss#',
        '   #s++++++ss#',
        '   #+s++++ss#',
        '   #s+++ssss#',
        '   #ss++ssss#',
        '     ######',
    ),
    # Side Sweep: smooth asymmetric crown with a rightward flow.
    (
        '', '', '',
        '      #####',
        '    ##HHH++#',
        '   #HHHHHH+s#',
        '  #HHHH+++++s#',
        '  #HH++++H+++s#',
        '   #+++HH+++ss#',
        '   #++HH+++ss#',
        '   #+HH+++ss#',
        '   #s+++++ss#',
        '   #ss++++ss#',
        '     ######',
    ),
    # Tousled: asymmetric overlapping locks with a broken lower contour.
    (
        '', '',
        '        ##',
        '    ####H+#',
        '   #HHHH++s##',
        '  #HHH++HH++s#',
        '   #HH++HHH++s#',
        '  #H++HH+++H+s#',
        '   #+++H++++ss#',
        '  #s+++++s++s#',
        '   #++ss++ss#',
        '   #s++ss++s#',
        '   #ss++ssss#',
        '     ######',
    ),
    # Quiff: a raised, swept crown, narrower temples and a neat neckline.
    (
        '',
        '        ###',
        '      ##HHs#',
        '     #HHHH+s#',
        '    #HHHH++s#',
        '   #HHH++++s#',
        '   #HH+++++s#',
        '  #H++++++H+s#',
        '  #++++++HH+s#',
        '   #s++++++s#',
        '   #s+++++ss#',
        '   #s++++sss#',
        '   #ssssssss#',
        '     ######',
    ),
    # Shag: layered sides and longer, stepped locks at the nape.
    (
        '', '',
        '      #####',
        '    ##HH++s##',
        '   #HHHH+++ss#',
        '  #HHH++HH++s#',
        '  #HH++HH+++ss#',
        '  #H++HH++++ss#',
        '  #++++H++++ss#',
        '  #s+++s+++sss#',
        '   #++ss++sss#',
        '   #+ss++ss+#',
        '   #s++ss++s#',
        '     #s++s#',
    ),
    # Curls: rounded clusters carry through the crown, sides and nape.
    (
        '', '',
        '     ##  ##',
        '   ##HH##HH##',
        '   #HHH++HH+s#',
        '  #HH++HHH++s#',
        '  #++HH++HH++s#',
        '   #HH++HH++s#',
        '  #HH++HH+++ss#',
        '  #s++HH++H+s#',
        '   #H++s++ss#',
        '   #+ss++ss+#',
        '   #s+ss+ss+#',
        '     ##++##',
    ),
    # Man Bun: a centered knot, visible tie, and swept-back lower hair.
    (
        '',
        '      ####',
        '     #HH+s#',
        '     #H++s#',
        '      #RR#',
        '   ###++ss###',
        '  #HHH+++++ss#',
        '  #HH++++++ss#',
        '  #H+++++++ss#',
        '  #+++++++sss#',
        '   #s++++sss#',
        '   #ss+++sss#',
        '   #ssssssss#',
        '     ######',
    ),
    # Undercut: a short top and skin-tone stubble around the lower skull.
    (
        '', '', '',
        '     ######',
        '    #HHH++s#',
        '   #HHHH+++s#',
        '  #HHH+++++ss#',
        '  #HH++++++ss#',
        '  #+++++++sss#',
        '  #stuttttuts#',
        '   #tuttuttu#',
        '   #tttttttt#',
        '   #tttttttt#',
        '     ######',
    ),
)

assert len(BACKS) == 10 and all(len(rows) == 14 for rows in BACKS)
assert all(len(row) <= 16 and set(row.replace(' ', '.')) <= COLORS.keys()
           for rows in BACKS for row in rows)


def rear_walking_hair(native, style):
    """Return a complete rear crown anchored to the native ears and nape."""
    assert len(native) == 32 and len(native[0]) == 16 and 1 <= style <= 10
    ear_y = min(y for y, row in enumerate(native) if any(v in (1, 2, 3) for v in row))
    nape_y = ear_y + 2
    top = nape_y - 13
    art = [row[:] for row in native]
    forced = set()
    for yy, row in enumerate(BACKS[style - 1]):
        y = top + yy
        for x, char in enumerate(row.replace(' ', '.').ljust(16, '.')):
            # Native ears, their outside rims, and the collar are separate
            # anatomy. The final template row only replaces the central nape.
            if native[y][x] in (1, 2, 3, 12, 13):
                continue
            if y >= ear_y and (x <= 2 or x >= 13):
                continue
            if y == nape_y and not 5 <= x <= 10:
                continue
            art[y][x] = COLORS[char]
            forced.add((x, y))
    return art, forced
