"""Review-map reachability, safe route returns and preserved published map IDs."""
import json
import hashlib
from pathlib import Path
import struct
import unittest
import subprocess
import tempfile

R = Path(__file__).resolve().parents[1]

def read(path): return json.loads((R/path).read_text())
def digest(value): return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()
BASE = read('docs/qa/hidden-grottos-baseline.json')
def cells(layout):
    return struct.unpack('<%dH' % (layout['width']*layout['height']), (R/layout['blockdata_filepath']).read_bytes())

class Grottos(unittest.TestCase):
    def test_append_only_ids_and_unchanged_routes(self):
        after = read('data/maps/map_groups.json')
        self.assertEqual(list(BASE['groups']),list(after))
        for group, before in BASE['groups'].items():
            self.assertEqual(before['sha256'], digest(after[group][:before['count']]))
        layouts = read('data/layouts/layouts.json')['layouts']
        self.assertEqual(BASE['layouts_sha256'],digest(layouts[:BASE['layout_count']]))
        for route in ['PetalburgWoods','Route114','Route119']:
            p=f'data/maps/{route}/map.json'; current=read(p)
            new=[b for b in current['bg_events'] if b.get('script','').startswith('LegendsGrotto_Enter')]
            self.assertEqual(len(new),2 if route=='PetalburgWoods' else 1)
            current['bg_events']=[b for b in current['bg_events'] if b not in new]
            self.assertEqual(BASE['routes'][route]['map_json_sha256'],digest(current))
            # Only the bounded review entrance cells may differ.
            for f in ['data/layouts/'+route+'/map.bin','data/maps/'+route+'/scripts.inc']:
                data=bytearray((R/f).read_bytes())
                if f.endswith('map.bin'):
                    for patch in BASE['entrance_patches'][route]:
                        offset=patch['index']*2
                        self.assertEqual(struct.unpack_from('<H',data,offset)[0],patch['new'])
                        struct.pack_into('<H',data,offset,patch['old'])
                self.assertEqual(BASE['routes'][route]['files'][f],hashlib.sha256(data).hexdigest())

    def test_approved_looks_preserved_except_cliff_opening(self):
        approved=read('docs/qa/hidden-grottos-approved-looks.json')
        for path,sha in approved['map_sha256'].items():
            self.assertEqual(hashlib.sha256((R/path).read_bytes()).hexdigest(),sha,path)
        a=bytearray((R/'data/layouts/Route114/map.bin').read_bytes())
        for patch in approved['Route114_restore_words']:
            struct.pack_into('<H',a,patch['index']*2,patch['old'])
        self.assertEqual(hashlib.sha256(a).hexdigest(),approved['Route114_sha256'])

    def test_cliff_options_append_native_assets_without_changing_baseline(self):
        proof=read('docs/qa/cliff-entrance-options.json');base='data/tilesets/secondary/fallarbor/'
        for path,sha in proof['unchanged_files'].items():
            self.assertEqual(hashlib.sha256((R/path).read_bytes()).hexdigest(),sha)
        for path,key,size in [('metatiles.bin','metatiles_prefix_sha256',16),('metatile_attributes.bin','attributes_prefix_sha256',2)]:
            data=(R/(base+path)).read_bytes();count=proof['base_metatile_count']
            self.assertEqual(len(data),(count+6)*size)
            self.assertEqual(hashlib.sha256(data[:count*size]).hexdigest(),proof[key])
        active=(R/'data/tilesets/legends_lights/fallarbor_metatiles.bin').read_bytes()
        native=(R/(base+'metatiles.bin')).read_bytes();prefix=proof['base_metatile_count']*16
        self.assertEqual(hashlib.sha256(active[:prefix]).hexdigest(),proof['compiled_metatiles_prefix_sha256'])
        self.assertEqual(active[prefix:],native[prefix:])
        self.assertEqual(hashlib.sha256((R/'data/layouts/Route114/map.bin').read_bytes()).hexdigest(),proof['route114_sha256'])

    def test_reach_every_interaction_and_exit(self):
        layouts = {l['id']:l for l in read('data/layouts/layouts.json')['layouts']}
        for key in ['Leafshade','Stillwater','Rainroot']:
            m=read(f'data/maps/LegendsGrotto_{key}/map.json');l=layouts[m['layout']];a=cells(l);w=l['width'];h=l['height']
            blocked={(o['x'],o['y']) for o in m['object_events']}
            def walkable(x,y):return 0<=x<w and 0<=y<h and not a[y*w+x]&0xC00 and (x,y) not in blocked
            seen={(9,11)};pending=list(seen)
            while pending:
                x,y=pending.pop()
                for v in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
                    if v not in seen and walkable(*v):seen.add(v);pending.append(v)
            self.assertIn((9,9),seen)
            self.assertEqual((w,h),(18,16))
            for obj in m['object_events']+m['bg_events'][1:]:
                x,y=obj['x'],obj['y'];self.assertTrue(any(p in seen for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]),(key,obj))
            for e in m['coord_events']:self.assertIn((e['x'],e['y']),seen)
            self.assertTrue(m['coord_events'])
            self.assertFalse(m['allow_escaping']);self.assertFalse(m['allow_cycling'])
            self.assertFalse(m['requires_flash'])

    def test_entrances_have_safe_returns_and_no_event_collisions(self):
        layouts = {l['id']:l for l in read('data/layouts/layouts.json')['layouts']}
        for route,approach in [('PetalburgWoods',(13,32)),('Route114',(14,40)),('Route119',(27,106))]:
            m=read(f'data/maps/{route}/map.json');l=layouts[m['layout']];a=cells(l)
            entries=[e for e in m['bg_events'] if e.get('script','').startswith('LegendsGrotto_Enter')]
            entry=min(entries,key=lambda e:abs(e['x']-approach[0])+abs(e['y']-approach[1]))
            self.assertEqual(a[approach[1]*l['width']+approach[0]]&0xC00,0)
            self.assertEqual(abs(entry['x']-approach[0])+abs(entry['y']-approach[1]),1)
            self.assertFalse(any(o['x']==approach[0] and o['y']==approach[1] for o in m['object_events']))
            self.assertFalse(any(e['x']==entry['x'] and e['y']==entry['y'] for e in m['bg_events'] if e is not entry))

    def test_cliff_mouth_has_a_real_walkable_approach(self):
        l=next(l for l in read('data/layouts/layouts.json')['layouts'] if l['name']=='Route114_Layout')
        a=cells(l);w=l['width']
        # Ordinary route -> landing -> adjacent visible cave mouth, with no
        # intervening cliff/ledge or remote background interaction.
        for x in [15,14]:
            self.assertEqual(a[40*w+x]&0xC00,0)
            self.assertEqual(a[40*w+x]&1023,0x001)
        self.assertEqual(a[40*w+13]&1023,0x261)
        m=read('data/maps/Route114/map.json')
        e=next(e for e in m['bg_events'] if e.get('script')=='LegendsGrotto_EnterStillwater')
        self.assertEqual((e['x'],e['y']),(13,40))
        self.assertIn('warp MAP_ROUTE114, 14, 40',(R/'data/scripts/legends_grotto_review.inc').read_text())

    def test_every_tree_is_complete(self):
        for key in ['Leafshade','Rainroot']:
            l=next(l for l in read('data/layouts/layouts.json')['layouts'] if l['id']=='LAYOUT_LEGENDS_GROTTO_'+key.upper())
            a=cells(l); w=l['width']
            self.assertNotIn(0x017,[v&1023 for v in a])
            for i,v in enumerate(a):
                if v&1023==0x1D4:
                    self.assertEqual([a[i+1]&1023,a[i+w]&1023,a[i+w+1]&1023],[0x1D5,0x1E4,0x1E5])
                if v&1023==0x1E4:self.assertEqual(a[i-w]&1023,0x1D4)
                if v&1023==0x1E5:self.assertEqual(a[i-w-1]&1023,0x1D4)

    def test_rainroot_long_grass_has_native_roots(self):
        l=next(l for l in read('data/layouts/layouts.json')['layouts'] if l['id']=='LAYOUT_LEGENDS_GROTTO_RAINROOT')
        a=cells(l);w=l['width'];grass=[i for i,v in enumerate(a) if v&1023==0x015]
        self.assertTrue(grass)
        for i in grass:
            self.assertLess(i+w,len(a))
            self.assertIn(a[i+w]&1023,[0x015,0x208])
            self.assertEqual(a[i]&0xC00,0)
        roots=[i for i,v in enumerate(a) if v&1023==0x208]
        self.assertTrue(roots)
        for i in roots:
            self.assertGreaterEqual(i,w)
            self.assertEqual(a[i-w]&1023,0x015)
            self.assertEqual(a[i]&0xC00,0)

    def test_real_native_warp_guard_only_matches_scripted_openings(self):
        groups=read('data/maps/map_groups.json')
        maps={}
        for gi,group in enumerate(groups['group_order']):
            names=groups[group]
            for mi,name in enumerate(names):maps[name]=(gi<<8)|mi
        source=(R/'src/legends_grotto_review.c').read_text()
        helper='bool32 LegendsGrottoIsEntrance'+source.split('bool32 LegendsGrottoIsEntrance',1)[1]
        prelude='''#include <stdint.h>
#include <assert.h>
typedef uint16_t u16;typedef int16_t s16;typedef uint32_t bool32;
#define FALSE 0
struct Save { struct {uint8_t mapNum,mapGroup;} location; } save;
struct Save *gSaveBlock1Ptr=&save;
'''
        routes={'PetalburgWoods':'MAP_PETALBURG_WOODS','Route114':'MAP_ROUTE114','Route119':'MAP_ROUTE119'}
        for route,macro in routes.items():prelude+=f'#define {macro} {maps[route]}\n'
        body='int main(void){for(int g=0;g<256;g++)for(int m=0;m<256;m++){save.location.mapGroup=g;save.location.mapNum=m;'
        body+='if(((g<<8)|m)!=MAP_PETALBURG_WOODS&&((g<<8)|m)!=MAP_ROUTE114&&((g<<8)|m)!=MAP_ROUTE119){assert(!LegendsGrottoIsEntrance(13,31));assert(!LegendsGrottoIsEntrance(27,105));continue;}'
        body+='for(int x=0;x<64;x++)for(int y=0;y<160;y++){int expected=0;'
        for route,macro in routes.items():
            coords=[(b['x'],b['y']) for b in read(f'data/maps/{route}/map.json')['bg_events'] if b.get('script','').startswith('LegendsGrotto_Enter')]
            for x,y in coords:body+=f'expected|=(((g<<8)|m)=={macro}&&x=={x}&&y=={y});'
        body+='assert(!!LegendsGrottoIsEntrance(x,y)==!!expected);}}return 0;}'
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'probe.c').write_text(prelude+helper+body)
            subprocess.run(['cc','-std=c11','-Wall','-Werror',str(p/'probe.c'),'-o',str(p/'probe')],check=True)
            subprocess.run([str(p/'probe')],check=True)

if __name__=='__main__':unittest.main()
