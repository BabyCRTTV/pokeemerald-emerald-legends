"""Build three review-only grotto maps from unchanged native Hoenn metatiles.

Run from the repository root. Does not edit existing map pixels or published IDs.
"""
from pathlib import Path
import json
import struct

ROOT = Path(__file__).resolve().parents[2]
W, H = 22, 20
ROOMS = [
    ('Leafshade', 'Leafshade Hollow', 'PetalburgWoods', 'MAPSEC_PETALBURG_WOODS',
     'gTileset_Rustboro', 'MUS_PETALBURG_WOODS', 'WEATHER_SHADE', (13, 31), (13, 32)),
    ('Stillwater', 'Stillwater Nook', 'Route114', 'MAPSEC_ROUTE_114',
     'gTileset_Cave', 'MUS_PETALBURG_WOODS', 'WEATHER_NONE', (14, 40), (15, 40)),
    ('Rainroot', 'Rainroot Hollow', 'Route119', 'MAPSEC_ROUTE_119',
     'gTileset_Fortree', 'MUS_ROUTE119', 'WEATHER_RAIN', (27, 105), (28, 105)),
]

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
    # Native grass-bank and cave-bank water edges. Water is deliberately solid:
    # the review needs no Surf transition, fishing table or new random battles.
    tiles = ([0x286, 0x283, 0x285, 0x28A, 0x283, 0x282, 0x274, 0x284, 0x272]
             if cave else [0x180, 0x189, 0x181, 0x190, 0x170, 0x192, 0x198, 0x199, 0x19A])
    for i, tile in enumerate(tiles):
        put(a, x + i % 3, y + i // 3, tile, True)
    if not cave:
        for dx in range(3):
            put(a, x + dx, y + 3, 0x002)

def landscape(kind):
    a = [0x3400 | 0x20D] * (W * H) if kind == 1 else [0x3001] * (W * H)
    if kind == 1:
        for y in range(7, 17):
            left = 4 if 9 <= y <= 13 else 6
            right = 17 if 9 <= y <= 13 else 16
            for x in range(left, right + 1):
                put(a, x, y, 0x201)
            put(a, left - 1, y, 0x213, True)
            put(a, right + 1, y, 0x210, True)
        for x in range(6, 17):
            put(a, x, 5, 0x20D, True)
            put(a, x, 6, 0x214, True)
        pool(a, 5, 10, True)
        for x, y in [(15, 8), (16, 12), (5, 13), (13, 7)]:
            put(a, x, y, 0x202, True)
        for y in range(16, 20):
            put(a, 11, y, 0x201)
            put(a, 12, y, 0x201)
    else:
        for y in range(0, H, 2):
            for x in range(0, W, 2):
                # Clear whole trees to preserve native crowns and trunks.
                if ((x + 1 - 11) / 6.2) ** 2 + ((y + 1 - 10) / 4.8) ** 2 > 1:
                    tree(a, x, y)
        for y in range(14, H):
            for x in [10, 11]:
                put(a, x, y, 0x001)
        if kind == 0:
            for x, y in [(7, 7), (8, 7), (7, 8), (14, 10), (15, 10), (14, 11)]:
                put(a, x, y, 0x004)
            for x, y in [(6, 11), (7, 12), (15, 12)]:
                put(a, x, y, 0x017, True)
        else:
            pool(a, 6, 9)
            for x, y in [(13, 7), (14, 7), (15, 7), (14, 8), (15, 8), (15, 11), (15, 12)]:
                # Long grass is scenery; no encounter table is registered.
                put(a, x, y, 0x015)
            for x, y in [(7, 6), (15, 9), (7, 13)]:
                put(a, x, y, 0x017, True)
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
        save(dp / 'border.bin', struct.pack('<4H', *([0x360D] * 4 if i == 1 else [0x35D4, 0x35D5, 0x35E4, 0x35E5])))
        if not any(l['id'] == lid for l in layouts['layouts']):
            layouts['layouts'].append(dict(id=lid, name=name + '_Layout', width=W, height=H,
                primary_tileset='gTileset_General', secondary_tileset=secondary,
                border_filepath=f'data/layouts/{name}/border.bin',
                blockdata_filepath=f'data/layouts/{name}/map.bin', layout_version='emerald'))
        if name not in groups['gMapGroup_LegendsHoenn']:
            groups['gMapGroup_LegendsHoenn'].append(name)
        m = dict(id=mid, name=name, layout=lid, music=music, region='REGION_HOENN',
            region_map_section=section, requires_flash=False, weather=weather,
            map_type='MAP_TYPE_UNDERGROUND' if i == 1 else 'MAP_TYPE_ROUTE',
            allow_cycling=False, allow_escaping=False, allow_running=True,
            show_map_name=False, battle_scene='MAP_BATTLE_SCENE_NORMAL', connections=None,
            object_events=[obj('OBJ_EVENT_GFX_VAR_F', 11, 8, 'LegendsGrotto_Visitor'),
                           obj('OBJ_EVENT_GFX_ITEM_BALL', 14, 13, 'LegendsGrotto_Find')],
            warp_events=[], coord_events=[], bg_events=[dict(type='sign', x=11, y=19,
                elevation=0, player_facing_dir='BG_EVENT_PLAYER_FACING_ANY', script='LegendsGrotto_Exit' + key)])
        # A bottom coordinate trigger gives an ordinary walking exit; inspecting
        # the mouth also works. Temporary native variables are not save claims.
        m['coord_events'] = [dict(type='trigger', x=x, y=18, elevation=0,
            var='VAR_TEMP_1', var_value='0', script='LegendsGrotto_Exit' + key) for x in [10, 11, 12] if a[18*W+x] & 0xC00 == 0]
        clue = [(6, 11), (13, 7), (15, 9)][i]
        m['bg_events'].append(dict(type='sign', x=clue[0], y=clue[1], elevation=0,
            player_facing_dir='BG_EVENT_PLAYER_FACING_ANY', script='LegendsGrotto_Clue' + key))
        mp = ROOT / 'data/maps' / name
        mp.mkdir(exist_ok=True)
        save(mp / 'map.json', json.dumps(m, indent=2) + '\n')
        save(mp / 'scripts.inc', f'{name}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, LegendsGrotto_OnTransition\n\t.byte 0\n')
        rp = ROOT / 'data/maps' / route / 'map.json'
        r = json.loads(rp.read_text())
        script = 'LegendsGrotto_Enter' + key
        if not any(b.get('script') == script for b in r['bg_events']):
            r['bg_events'].append(dict(type='sign', x=entrance[0], y=entrance[1],
                elevation=0, player_facing_dir='BG_EVENT_PLAYER_FACING_ANY', script=script))
        save(rp, json.dumps(r, indent=2) + '\n')
    save(groups_path, json.dumps(groups, indent=2) + '\n')
    save(layouts_path, json.dumps(layouts, indent=2) + '\n')

if __name__ == '__main__':
    main()
