"""Manually package maps and entries from the wiki's pinned game snapshot.

Never reads the current game checkout or advances the encounter snapshot.
Requires Pillow. Re-run only when explicitly updating the wiki.
"""
import io
import json
import re
import subprocess
from pathlib import Path
from PIL import Image
from build_wiki_cries import FORMS

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / 'docs/wiki'
data = json.loads((WIKI / 'dex-data.json').read_text())
commit = data['sourceCommit']

def read(path):
    return subprocess.check_output(['git', 'show', f'{commit}:{path}'], cwd=ROOT)

paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', commit], cwd=ROOT).decode().splitlines()
sections = {}
for path in paths:
    if path.startswith('data/maps/') and path.endswith('/map.json'):
        m = json.loads(read(path))
        sections[m['id']] = m.get('region_map_section')

regions = {}
for name, stem, layout in [('Hoenn', 'map', 'region_map_layout.h'), ('Kanto', 'map_kanto', 'region_map_layout_kanto.h')]:
    base = f'graphics/pokenav/region_map/{stem}'
    tiles = Image.open(io.BytesIO(read(base + '.png'))).convert('RGB')
    tilemap = read(base + '.bin')
    # The game uses a 64x64 affine background: one 8-bit tile index per cell.
    assert len(tilemap) == 4096
    image = Image.new('RGB', (512, 512))
    for i, n in enumerate(tilemap):
        x, y = n % (tiles.width // 8) * 8, n // (tiles.width // 8) * 8
        assert y + 8 <= tiles.height, (name, n)
        image.paste(tiles.crop((x, y, x + 8, y + 8)), (i % 64 * 8, i // 64 * 8))
    # Same origin and 28x15 bounds as the game's region-map cursor.
    image.crop((8, 16, 232, 136)).save(WIKI / f'map-{name.lower()}.png', optimize=True)
    rows = re.findall(r'\{([^{}]+)\}', read('src/data/region_map/' + layout).decode())
    cells = {}
    for y, row in enumerate(rows):
        for x, section in enumerate(re.findall(r'MAPSEC_\w+', row)):
            if section != 'MAPSEC_NONE':
                cells.setdefault(section, []).append([x * 8, y * 8])
    assert len(rows) == 15
    regions[name] = {'image': f'map-{name.lower()}.png', 'cells': cells}

def decode_strings(text):
    return ' '.join(''.join(json.loads('"' + x + '"') for x in re.findall(r'"((?:\\.|[^"\\])*)"', text)).split())

texts = []
for path in paths:
    if path.startswith('src/data/pokemon/species_info') and path.endswith('.h'):
        text = read(path).decode()
        # Keep definitions, let cpp expand shared species/form macros, and inspect
        # all family blocks regardless of compile-time family enable switches.
        text = re.sub(r'^\s*#(?!define\b)[^\n]*', '', text, flags=re.M)
        texts.append(text)
expanded = subprocess.check_output(['gcc', '-E', '-P', '-x', 'c', '-'], input='\n'.join(texts).encode(), stderr=subprocess.DEVNULL).decode()
shared = {name: decode_strings(body) for name, body in re.findall(r'const u8 (\w+)\[\]\s*=\s*_\((.*?)\);', expanded, re.S)}
descriptions = {}
blocks = re.split(r'\[SPECIES_(\w+)\]\s*=', expanded)
for species, block in zip(blocks[1::2], blocks[2::2]):
    match = re.search(r'\.description\s*=\s*COMPOUND_STRING\((.*?)\),', block, re.S)
    reference = re.search(r'\.description\s*=\s*(\w+)\s*,', block)
    entry = decode_strings(match[1]) if match else shared.get(reference[1]) if reference else None
    if entry and species not in descriptions:
        descriptions[species] = entry
descriptions['SILVALLY_NORMAL'] = shared['gSilvallyNormalPokedexText']
entries = {}
for p in data['species']:
    key = p['id'] + ('_' + FORMS[p['id']].upper() if p['id'] in FORMS else '')
    entry = descriptions.get(key) or descriptions.get(p['id'])
    if not entry:
        entry = next((text for species, text in descriptions.items() if species.startswith(p['id'] + '_')), None)
    if entry:
        entries[p['id']] = entry

section_data = {s['id']: s for s in json.loads(read('src/data/region_map/region_map_sections.json'))['map_sections']}
assert len(entries) == len(data['species']), 'Missing Pokédex entries'
locations = {}
for m in data['maps']:
    section = sections.get(m['id'])
    cells = regions[m['region']]['cells'].get(section, [])
    # Interiors use their game's map-section marker when no surface cells exist.
    if not cells and section in section_data:
        sec = section_data[section]
        cells = [[x * 8, y * 8] for y in range(sec['y'], sec['y'] + sec['height']) for x in range(sec['x'], sec['x'] + sec['width']) if 0 <= x < 28 and 0 <= y < 15]
    locations[m['id']] = {'region': m['region'], 'section': section, 'cells': cells}
output = {'sourceCommit': commit, 'entries': entries, 'locations': locations,
          'regions': {name: {'image': region['image']} for name, region in regions.items()}}
(WIKI / 'dex-profiles.js').write_text('/* Game maps and entries from the manually pinned wiki snapshot. */\nwindow.LegendsProfiles = ' + json.dumps(output, ensure_ascii=False, separators=(',', ':')) + ';\n')
print(f'Packaged {len(entries)} Pokédex entries and {sum(bool(x["cells"]) for x in locations.values())}/{len(locations)} mapped encounter locations from {commit}')
