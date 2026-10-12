#!/usr/bin/env python3
"""Append the Wing Survey's native FRLG habitats without renumbering old maps.

Run once to author imports. Existing imports are skipped so hand-authored events
and closures are not overwritten on subsequent runs. No commercial ROM input.
"""
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = [
    'Route20', 'SeafoamIslands_1F', 'SeafoamIslands_B1F',
    'SeafoamIslands_B2F', 'SeafoamIslands_B3F', 'SeafoamIslands_B4F',
    'Route9', 'CeruleanCity', 'CeruleanCity_Gym', 'CeruleanCity_PokemonCenter_1F',
    'CeruleanCity_Mart', 'Route4', 'Route4_PokemonCenter_1F',
    'MtMoon_1F', 'MtMoon_B1F', 'MtMoon_B2F', 'Route3', 'PewterCity',
    'PewterCity_Gym', 'PewterCity_PokemonCenter_1F', 'PewterCity_Mart',
    'CinnabarIsland', 'CinnabarIsland_Gym', 'CinnabarIsland_PokemonCenter_1F',
    'CinnabarIsland_Mart', 'MtEmber_Exterior', 'MtEmber_SummitPath_1F',
    'MtEmber_SummitPath_2F', 'MtEmber_SummitPath_3F', 'MtEmber_Summit',
]

def read(path):
    return json.loads((ROOT / path).read_text())

def write(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) + '\n')

def declaration(text, symbol):
    m = re.search(r'^const [^\n]*\b' + re.escape(symbol) + r'\b[^=]*=', text, re.M)
    if not m:
        raise ValueError(symbol)
    return text[m.start():text.index(';', m.end()) + 1]

def main(sources=SOURCES, manifest_path='data/legends_kanto_chapters4-6.json', include_anchor='\t.include "data/scripts/legends_kanto_chapter3.inc"'):
    groups = read('data/maps/map_groups.json')
    layout_doc = read('data/layouts/layouts.json')
    layouts = {l['id']:l for l in layout_doc['layouts']}
    maps = {d['id']:d for p in (ROOT/'data/maps').glob('*/map.json')
            if (d := json.loads(p.read_text()))}
    imported = {m['id'].replace('MAP_LEGENDS_KANTO_', 'MAP_', 1):m['id']
                for m in maps.values() if m['id'].startswith('MAP_LEGENDS_KANTO_')}
    native = {n: read(f'data/maps/{n}_Frlg/map.json') for n in sources}
    imported.update({d['id']:d['id'].replace('MAP_', 'MAP_LEGENDS_KANTO_', 1)
                     for d in native.values()})
    headers = (ROOT/'src/data/tilesets/headers.h').read_text()
    graphics = (ROOT/'src/data/tilesets/graphics.h').read_text()
    metatiles = (ROOT/'src/data/tilesets/metatiles.h').read_text()
    out = ROOT/'src/data/tilesets/legends_story.h'
    art = out.read_text() if out.exists() else '#if !IS_FRLG\n\n'
    art = art.removesuffix('#endif\n')
    shared = (ROOT/'src/data/tilesets/legends_kanto.h').read_text()
    tileset_remap = {'gTileset_General_Frlg':'gTileset_LegendsKantoGeneral_Frlg',
                     'gTileset_BuildingFrlg':'gTileset_LegendsKantoBuildingFrlg',
                     'gTileset_PokemonCenter_Frlg':'gTileset_LegendsKantoPokemonCenter'}
    manifest = []
    for n, source in native.items():
        name = 'LegendsKanto_' + n
        ident = imported[source['id']]
        src_layout = layouts[source['layout']]
        lid = source['layout'].replace('LAYOUT_', 'LAYOUT_LEGENDS_KANTO_', 1)
        for key in ('primary_tileset','secondary_tileset'):
            symbol = src_layout[key]
            if symbol in tileset_remap:
                continue
            replacement = symbol.replace('gTileset_', 'gTileset_LegendsKanto', 1)
            tileset_remap[symbol] = replacement
            if replacement in shared or replacement in art:
                continue
            block = declaration(headers, symbol)
            for field, text in [('tiles',graphics),('palettes',graphics),
                                ('metatiles',metatiles),('metatileAttributes',metatiles)]:
                ref = re.search(r'\.' + field + r'\s*=\s*(\w+)', block)[1]
                decl = declaration(text, ref)
                newref = ref.replace('_', '_LegendsStory', 1)
                art += decl.replace(ref,newref) + '\n\n'
                block = block.replace(ref,newref)
            # Static native art: no FRLG-only animation callback dependency.
            block = re.sub(r'\.callback\s*=\s*\w+', '.callback = NULL', block)
            art += block.replace(symbol,replacement) + '\n\n'
        manifest.append({'source':n+'_Frlg','name':name,'id':ident,'layout':lid})
        if ident in maps:
            continue
        layout = copy.deepcopy(src_layout)
        layout.update(id=lid, name=name+'_Layout', layout_version='emerald', tileset_format='frlg')
        for key in ('primary_tileset','secondary_tileset'):
            layout[key] = tileset_remap[layout[key]]
        if lid not in layouts:
            layout_doc['layouts'].append(layout)
            layouts[lid] = layout
        d = copy.deepcopy(source)
        d.update(id=ident,name=name,layout=lid,region='REGION_HOENN')
        d['connections'] = [dict(c,map=imported[c['map']]) for c in (d['connections'] or [])
                            if c['map'] in imported]
        d['object_events'] = []
        d['coord_events'] = []
        d['bg_events'] = []
        # Preserve every warp index, including sealed, unimplemented doors.
        for i,w in enumerate(d['warp_events']):
            if w['dest_map'] in imported:
                w['dest_map'] = imported[w['dest_map']]
            else:
                w.update(dest_map=ident,dest_warp_id=str(i))
                d['bg_events'].append({'type':'sign','x':w['x'],'y':w['y'],
                    'elevation':w['elevation'],'player_facing_dir':'BG_EVENT_PLAYER_FACING_ANY',
                    'script':'LegendsKanto_EventScript_FoundationClosed'})
        write(f'data/maps/{name}/map.json',d)
        (ROOT/f'data/maps/{name}/scripts.inc').write_text(
            f'{name}_MapScripts::\n\tmap_script MAP_SCRIPT_ON_TRANSITION, LegendsKanto_Foundation_OnTransition\n\t.byte 0\n')
        groups['gMapGroup_LegendsKanto'].append(name)
    out.write_text(art+'#endif\n')
    write('data/maps/map_groups.json',groups)
    write('data/layouts/layouts.json',layout_doc)
    write(manifest_path,{'maps':manifest})
    events = ROOT/'data/event_scripts.s'
    text = events.read_text()
    anchor = include_anchor
    additions = '\n'.join('\t.include "data/maps/'+m['name']+'/scripts.inc"' for m in manifest)
    if additions not in text:
        text = text.replace(anchor,anchor+'\n'+additions)
    events.write_text(text)
    fieldmap = ROOT/'src/tilesets.c'
    text=fieldmap.read_text()
    if '#include "data/tilesets/legends_story.h"' not in text:
        text=text.replace('#include "data/tilesets/legends_kanto.h"',
                          '#include "data/tilesets/legends_kanto.h"\n#include "data/tilesets/legends_story.h"')
    fieldmap.write_text(text)
    wild = read('src/data/wild_encounters.json')
    entries = wild['wild_encounter_groups'][0]['encounters']
    present = {e['map'] for e in entries}
    for e in list(entries):
        if e['map'] in imported and e['base_label'].endswith('_FireRed'):
            ident=imported[e['map']]
            if ident not in present and ident in {m['id'] for m in manifest}:
                d=copy.deepcopy(e);d['map']=ident;d['base_label']='g'+ident.title().replace('_','')+'Encounter'
                entries.append(d);present.add(ident)
    write('src/data/wild_encounters.json',wild)
    print(f'Authored {len(manifest)} native map imports.')

if __name__ == '__main__':
    main()
