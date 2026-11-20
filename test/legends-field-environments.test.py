"""Check event bounds, approaches, counters and Mira's terrace in the current layouts."""
import json
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return json.loads((ROOT / path).read_text())


MAPS = {m['id']: m for p in (ROOT / 'data/maps').glob('*/map.json') if (m := read(p))}
LAYOUTS = {layout['id']: layout for layout in read('data/layouts/layouts.json')['layouts']}
GROUPS = read('data/maps/map_groups.json')
ADDED = set(GROUPS['gMapGroup_LegendsHoenn'] + GROUPS['gMapGroup_LegendsKanto'])
ADDED.update(['MauvilleCity_MauvilleHills_Lobby', 'MauvilleCity_MauvilleHills_Apartment',
              'LilycoveCity_CoveLilyMotel_Apartment'])


def blocks(layout):
    return struct.unpack('<%dH' % (layout['width'] * layout['height']),
                         (ROOT / layout['blockdata_filepath']).read_bytes())


class FieldEnvironments(unittest.TestCase):
    def test_events(self):
        # The closed Cerulean back door aliases itself. The protected Vermilion
        # staff position serves customers across the counter.
        isolated = {('LegendsKanto_CeruleanCity', 31, 9, 'warp_events'),
                    ('LegendsKanto_CeruleanCity', 31, 9, 'bg_events'),
                    ('LegendsKanto_PokemonCenter_1F', 7, 2, 'object_events')}
        reviewed = set()
        for m in MAPS.values():
            if m['name'] not in ADDED:
                continue
            reviewed.add(m['name'])
            layout = LAYOUTS[m['layout']]
            width, height = layout['width'], layout['height']
            floor = {(i % width, i // width) for i, value in enumerate(blocks(layout))
                     if not value & 0xC00}
            for kind in ['warp_events', 'object_events', 'bg_events', 'coord_events']:
                for event in m[kind]:
                    if event.get('type') == 'clone':
                        continue
                    x, y = event['x'], event['y']
                    with self.subTest(map=m['name'], x=x, y=y, kind=kind):
                        self.assertTrue(0 <= x < width and 0 <= y < height)
                        if kind == 'warp_events':
                            dest = MAPS[event['dest_map']]
                            self.assertIn(int(event['dest_warp_id']), range(len(dest['warp_events'])))
                        if (m['name'], x, y, kind) not in isolated:
                            neighbors = {(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)}
                            self.assertTrue(neighbors & floor, 'no adjacent floor')
                        if kind == 'object_events' and event['graphics_id'] != 'OBJ_EVENT_GFX_LEGENDS_MIRA_ASLEEP':
                            self.assertIn((x, y), floor)
        self.assertEqual(reviewed, ADDED)

    def test_counters(self):
        for name in ['CeruleanCity', 'CinnabarIsland', 'PewterCity', 'Route4', 'ViridianCity']:
            m = read(f'data/maps/LegendsKanto_{name}_PokemonCenter_1F/map.json')
            nurse, = (e for e in m['object_events'] if e['graphics_id'] == 'OBJ_EVENT_GFX_NURSE')
            self.assertEqual((nurse['x'], nurse['y']), (7, 2), name)
            layout = LAYOUTS[m['layout']]
            tiles = blocks(layout)
            self.assertTrue(tiles[3 * layout['width'] + 7] & 0xC00, name)
            self.assertFalse(tiles[4 * layout['width'] + 7] & 0xC00, name)

    def test_terrace_and_vault(self):
        for name in ['LilycoveCity', 'LegendsNightmare_Street']:
            layout = LAYOUTS[read(f'data/maps/{name}/map.json')['layout']]
            tiles = blocks(layout)
            for x in [50, 51]:
                for y in range(16, 22):
                    self.assertFalse(tiles[y * layout['width'] + x] & 0xC00, (name, x, y))
            self.assertTrue(tiles[20 * layout['width'] + 49] & 0xC00)
        m = read('data/maps/LegendsHoenn_ContinentalVault/map.json')
        regigigas, = (e for e in m['object_events'] if e['script'] == 'LegendsHoenn_Regigigas')
        self.assertEqual(regigigas['movement_type'], 'MOVEMENT_TYPE_FACE_DOWN')


if __name__ == '__main__':
    unittest.main()
