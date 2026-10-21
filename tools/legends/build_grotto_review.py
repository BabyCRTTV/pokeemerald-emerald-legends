"""Build three review-only grotto maps from unchanged native Hoenn metatiles.

Run from the repository root. Uses a bounded native entrance patch on each route.
"""
from pathlib import Path
import json
import struct

ROOT = Path(__file__).resolve().parents[2]
W, H = 18, 16
ROOMS = [
    ('Leafshade', 'Leafshade Hollow', 'PetalburgWoods', 'MAPSEC_PETALBURG_WOODS',
     'gTileset_Rustboro', 'MUS_PETALBURG_WOODS', 'WEATHER_SHADE', (13, 31), (13, 32)),
    ('Stillwater', 'Stillwater Nook', 'Route114', 'MAPSEC_ROUTE_114',
     'gTileset_Cave', 'MUS_PETALBURG_WOODS', 'WEATHER_NONE', (14, 40), (15, 40)),
    ('Rainroot', 'Rainroot Hollow', 'Route119', 'MAPSEC_ROUTE_119',
     'gTileset_Fortree', 'MUS_ROUTE119', 'WEATHER_RAIN', (27, 105), (27, 106)),
]

# Every cell is existing Hoenn art; no tileset, palette or persistent ID changes.
ENTRANCE_TILES = {
    'PetalburgWoods': [(12, 31, 0x036), (13, 31, 0x037)],
    'Route114': [(13, 39, 0x259), (13, 40, 0x261), (14, 40, 0x33C)],
    'Route119': [(26, 104, 0x279), (27, 104, 0x27A), (28, 104, 0x27B),
                 (26, 105, 0x281), (27, 105, 0x278), (28, 105, 0x283),
                 (26, 106, 0x001)],
}

def save(path, data):
    data = data.encode() if isinstance(data, str) else data
    if not path.exists() or path.read_bytes() != data:
        path.write_bytes(data)

def put(a, x, y, tile, solid=False):
    a[y * W + x] = tile | 0x3000 | (0x400 if solid else 0)

def tree(a, x, y):
    for dx, dy, tile in [(0, 0, 0x1D4), (1, 0, 0x1D5), (0, 1, 0x1E4), (1, 1, 0x1E5)]:
        put(a, x + dx, y + dy, tile, True)

def pool(a, x, y, cave=False):
    # Complete native shorelines: Route 102's reflective pool and Scorched Slab's
    # rock-water bank. The final row is walkable soil, never a cut water tile.
    rows = ([[0x289, 0x291, 0x281], [0x28A, 0x170, 0x288],
             [0x28A, 0x170, 0x288], [0x25E, 0x25E, 0x25E]]
            if cave else [[0x0B0, 0x0B1, 0x0B1, 0x0B2],
                          [0x0B8, 0x0A1, 0x0A1, 0x0BA],
                          [0x0B8, 0x0A1, 0x0A1, 0x0BA],
                          [0x002, 0x002, 0x002, 0x002]])
    for dy, row in enumerate(rows):
        for dx, tile in enumerate(row):
            put(a, x + dx, y + dy, tile, dy < len(rows) - 1 and tile != 0x001)

def landscape(kind):
    a = [0x3400 | 0x211] * (W * H) if kind == 1 else [0x3001] * (W * H)
    if kind == 1:
        for y in range(5, 12):
            for x in range(5, 13):
                put(a, x, y, 0x201)
            put(a, 4, y, 0x212, True)
            put(a, 13, y, 0x210, True)
        for x in range(4, 14):
            put(a, x, 4, 0x21B if x == 4 else 0x21C if x == 13 else 0x219, True)
            put(a, x, 12, 0x247 if x in [4, 13] else 0x209, True)
        pool(a, 5, 7, True)
        for x, y in [(11, 5), (12, 10)]:
            put(a, x, y, 0x202, True)
        for y in range(12, H):
            for x in [8, 9]:
                put(a, x, y, 0x201)
    else:
        for y in range(0, H, 2):
            for x in range(0, W, 2):
                # Keep complete crowns around a small, softly stepped clearing.
                if ((x + 1 - 9) / 5.1) ** 2 + ((y + 1 - 8) / 4.1) ** 2 > 1:
                    tree(a, x, y)
        for y in range(12, H):
            for x in [8, 9]:
                put(a, x, y, 0x001)
        if kind == 0:
            for x, y in [(6, 6), (7, 6), (6, 7), (11, 8), (12, 8), (12, 9)]:
                put(a, x, y, 0x004)
        else:
            pool(a, 4, 8)
            # Native Route 119 long grass needs a south-edge root row.
            # Keep a compact clump with complete stalks rather than a raw strip.
            for x in [11, 12]:
                for y in [6, 7]:
                    put(a, x, y, 0x015)
                put(a, x, 8, 0x208)
    return a

def obj(gfx, x, y, script):
    return dict(graphics_id=gfx, x=x, y=y, elevation=3,
                movement_type='MOVEMENT_TYPE_FACE_DOWN', movement_range_x=0,
                movement_range_y=0, trainer_type='TRAINER_TYPE_NONE',
                trainer_sight_or_berry_tree_id='0', script=script, flag='0')

def main():
    groups_path = ROOT / 'data/maps/map_groups.json'
    groups = json.loads(groups_path.read_text())
    layouts_path = ROOT / 'data/layouts/layouts.json'
    layouts = json.loads(layouts_path.read_text())
    for i, (key, title, route, section, secondary, music, weather, entrance, approach) in enumerate(ROOMS):
        name = 'LegendsGrotto_' + key
        mid = 'MAP_LEGENDS_GROTTO_' + key.upper()
        lid = 'LAYOUT_LEGENDS_GROTTO_' + key.upper()
        dp = ROOT / 'data/layouts' / name
        dp.mkdir(exist_ok=True)
        a = landscape(i)
        save(dp / 'map.bin', struct.pack('<%dH' % len(a), *a))
        save(dp / 'border.bin', struct.pack('<4H', *([0x3611] * 4 if i == 1 else [0x35D4, 0x35D5, 0x35E4, 0x35E5])))
        if not any(l['id'] == lid for l in layouts['layouts']):
            layouts['layouts'].append(dict(id=lid, name=name + '_Layout', width=W, height=H,
                primary_tileset='gTileset_General', secondary_tileset=secondary,
                border_filepath=f'data/layouts/{name}/border.bin',
                blockdata_filepath=f'data/layouts/{name}/map.bin', layout_version='emerald'))
        next(l for l in layouts['layouts'] if l['id'] == lid).update(width=W, height=H)
        if name not in groups['gMapGroup_LegendsHoenn']:
            groups['gMapGroup_LegendsHoenn'].append(name)
        m = dict(id=mid, name=name, layout=lid, music=music, region='REGION_HOENN',
            region_map_section=section, requires_flash=False, weather=weather,
            map_type='MAP_TYPE_UNDERGROUND' if i == 1 else 'MAP_TYPE_ROUTE',
            allow_cycling=False, allow_escaping=False, allow_running=True,
            show_map_name=False, battle_scene='MAP_BATTLE_SCENE_NORMAL', connections=None,
            object_events=[obj('OBJ_EVENT_GFX_VAR_F', 9, 6, 'LegendsGrotto_Visitor'),
                           obj('OBJ_EVENT_GFX_ITEM_BALL', 11, 10, 'LegendsGrotto_Find')],
            warp_events=[], coord_events=[], bg_events=[dict(type='sign', x=9, y=15,
                elevation=0, player_facing_dir='BG_EVENT_PLAYER_FACING_ANY', script='LegendsGrotto_Exit' + key)])
        # A bottom coordinate trigger gives an ordinary walking exit; inspecting
        # the mouth also works. Temporary native variables are not save claims.
        m['coord_events'] = [dict(type='trigger', x=x, y=14, elevation=0,
            var='VAR_TEMP_1', var_value='0', script='LegendsGrotto_Exit' + key) for x in [8, 9] if a[14*W+x] & 0xC00 == 0]
        clue = [(4, 7), (11, 5), (12, 7)][i]
        m['bg_events'].append(dict(type='sign', x=clue[0], y=clue[1], elevation=0,
            player_facing_dir='BG_EVENT_PLAYER_FACING_ANY', script='LegendsGrotto_Clue' + key))
        mp = ROOT / 'data/maps' / name
        mp.mkdir(exist_ok=True)
        save(mp / 'map.json', json.dumps(m, indent=2) + '\n')
        save(mp / 'scripts.inc', f'{name}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, LegendsGrotto_OnTransition\n\t.byte 0\n')
        rp = ROOT / 'data/maps' / route / 'map.json'
        r = json.loads(rp.read_text())
        script = 'LegendsGrotto_Enter' + key
        r['bg_events'] = [b for b in r['bg_events'] if b.get('script') != script]
        for ex, ey in ([entrance, (12, 31)] if i == 0 else [entrance]):
            r['bg_events'].append(dict(type='sign', x=ex, y=ey,
                elevation=0, player_facing_dir='BG_EVENT_PLAYER_FACING_ANY', script=script))
        route_layout = next(l for l in layouts['layouts'] if l['id'] == r['layout'])
        route_path = ROOT / route_layout['blockdata_filepath']
        words = list(struct.unpack('<%dH' % (route_path.stat().st_size // 2), route_path.read_bytes()))
        for x, y, tile in ENTRANCE_TILES[route]:
            index = y * route_layout['width'] + x
            words[index] = (words[index] & 0xF000) | (0 if tile == 0x001 else 0x400) | tile
        save(route_path, struct.pack('<%dH' % len(words), *words))
        save(rp, json.dumps(r, indent=2) + '\n')
    save(groups_path, json.dumps(groups, indent=2) + '\n')
    save(layouts_path, json.dumps(layouts, indent=2) + '\n')

if __name__ == '__main__':
    main()
