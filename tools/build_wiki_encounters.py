#!/usr/bin/env python3
"""Refresh encounter tables only during an owner-requested wiki snapshot review.

Retain the curated Hoenn map list; include every imported Legends Kanto/Sevii
table. Species metadata is reviewed separately, never fabricated from slots.
Reads the commit explicitly pinned in dex-data.json, never a moving branch.
"""
import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / 'docs/wiki/dex-data.json'


def read(commit, path):
    return subprocess.check_output(['git', 'show', f'{commit}:{path}'], cwd=ROOT)


def main():
    data = json.loads(TARGET.read_text())
    commit = data['sourceCommit']
    group = next(g for g in json.loads(read(commit, 'src/data/wild_encounters.json'))['wild_encounter_groups']
                 if g['label'] == 'gWildMonHeaders')
    fields = {f['type']: f for f in group['fields']}
    # The first Altering Cave set is the default; special rotations aren't
    # simultaneous encounters. Unused upstream FRLG tables stay excluded.
    encounters = {}
    for encounter in group['encounters']:
        encounters.setdefault(encounter['map'], encounter)
    old = {m['id']: m for m in data['maps']}
    selected = [ident for ident, m in old.items() if m.get('region') != 'Grotto']
    selected.extend(e['map'] for e in group['encounters']
                    if e['map'].startswith('MAP_LEGENDS_KANTO_') and e['map'] not in old)
    names = {}
    for path in read(commit, 'data/maps/map_groups.json').decode().splitlines():
        match = re.match(r'\s*"(LegendsKanto_\w+)"', path)
        if match:
            name = match[1]
            source = json.loads(read(commit, f'data/maps/{name}/map.json'))
            human = name.removeprefix('LegendsKanto_')
            human = re.sub(r'([a-z])([A-Z])', r'\1 \2', human).replace('_', ' ')
            human = re.sub(r'Route(\d+)', r'Route \1', human).replace('Mt Ember', 'Mt. Ember').replace('Mt Moon', 'Mt. Moon')
            names[source['id']] = human
    species = {p['id'] for p in data['species']}
    result = []
    for ident in selected:
        source = encounters[ident]
        region = 'Sevii' if ident.startswith('MAP_LEGENDS_KANTO_MT_EMBER_') else old.get(ident, {}).get('region', 'Kanto')
        out = dict(id=ident, name=old.get(ident, {}).get('name', names.get(ident, ident)), region=region, methods=[])
        for key, method, label in [('land_mons', 'land', 'Land'), ('water_mons', 'surf', 'Surf'),
                                   ('rock_smash_mons', 'rock', 'Rock Smash'), ('fishing_mons', None, None)]:
            if key not in source:
                continue
            field = fields[key]
            slots = source[key]
            subsets = field.get('groups', {method: list(range(len(field['encounter_rates'])))})
            for method_id, indices in subsets.items():
                merged = defaultdict(lambda: {'min': 101, 'max': 0, 'rate': 0})
                for index in indices:
                    mon = slots['mons'][index]
                    name = mon['species'].removeprefix('SPECIES_')
                    assert name in species, name
                    entry = merged[name]
                    entry['min'] = min(entry['min'], mon['min_level'])
                    entry['max'] = max(entry['max'], mon['max_level'])
                    entry['rate'] += field['encounter_rates'][index]
                assert sum(e['rate'] for e in merged.values()) == 100
                entries = [dict(id=name, **entry) for name, entry in merged.items()]
                entries.sort(key=lambda e: -e['rate'])
                out['methods'].append(dict(id=method_id, label=label or method_id.replace('_', ' ').title(),
                                           encounterRate=slots['encounter_rate'], entries=entries))
        # Retain curated slot display order when the source tables are identical.
        if ident in old:
            previous = {m['id']: m for m in old[ident]['methods']}
            for index, method in enumerate(out['methods']):
                prior = previous.get(method['id'])
                if prior and method['encounterRate'] == prior['encounterRate'] and sorted(method['entries'], key=lambda e: e['id']) == sorted(prior['entries'], key=lambda e: e['id']):
                    out['methods'][index] = prior
        result.append(out)
    data['maps'] = result + [m for m in old.values() if m.get('region') == 'Grotto']
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(f'Review snapshot {commit}: {len(result)} ordinary locations, {len(data["maps"]) - len(result)} preserved grotto supplements')


if __name__ == '__main__':
    main()
