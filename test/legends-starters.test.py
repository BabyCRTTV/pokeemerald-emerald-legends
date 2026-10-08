"""Exercise actual starter/rival code using evolution metadata from the live source."""
from pathlib import Path
import re, subprocess, tempfile
root = Path(__file__).resolve().parents[1]
# Read native evolutionary edges and canonical dex membership, including forms.
entries = {}
for file in (root / 'src/data/pokemon/species_info').glob('*.h'):
    for match in re.finditer(r'\[(SPECIES_\w+)\]\s*=\s*\{(.*?)(?=\[SPECIES_|\Z)', file.read_text(), re.S):
        name, body = match.groups()
        dex = re.search(r'\.natDexNum\s*=\s*(NATIONAL_DEX_\w+)', body)
        evo = re.search(r'\.evolutions\s*=\s*EVOLUTION\((.*?)\)\s*,', body, re.S)
        edges = re.findall(r'\{(EVO_\w+)\s*,\s*([^,{}]+)\s*,\s*(SPECIES_\w+)', evo[1]) if evo else []
        if dex:
            entries[name] = (dex[1], [(m, int(p) if p.strip().isdigit() else 0, t) for m,p,t in edges])
canonical = {}
# Canonical species usually share the NATIONAL_DEX suffix. This independently
# excludes mega/regional/temporary forms from the random candidate fixtures.
for name,(dex,_) in entries.items():
    if name == dex.replace('NATIONAL_DEX_', 'SPECIES_'):
        canonical[dex] = name
names = set(entries)
fixtures = []
for name,(dex,edges) in entries.items():
    edges = [(m,p,t) for m,p,t in edges if t in names]
    fixtures.append(f'static const struct Evolution evos_{name}[] = {{' + ''.join(f'{{{1 if m == "EVO_LEVEL" else 2},{p},{t}}},' for m,p,t in edges) + '{0,0,0}};')
fixtures.append('const struct SpeciesInfo gSpeciesInfo[NUM_SPECIES] = {')
for name,(dex,_) in entries.items():
    base = canonical.get(dex, 'SPECIES_NONE')
    fixtures.append(f'[{name}] = {{{base},{base},evos_{name}}},')
fixtures.append('};')
source = (root / 'src/legends_starters.c').read_text()
source = '\n'.join(l for l in source.splitlines() if not l.startswith('#include'))
header = (root / 'include/legends_starters.h').read_text().replace('#include "global.h"', '')
stub = r'''
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <assert.h>
#include "species.h"
typedef uint8_t u8; typedef uint16_t u16; typedef uint32_t u32; typedef int bool32;
#define TRUE 1
#define FALSE 0
#define IS_FRLG 0
#define ARRAY_COUNT(a) (sizeof(a)/sizeof((a)[0]))
#define VAR_LEGENDS_STARTER_SETTING 0
#define VAR_LEGENDS_STARTER_RESCUE 1
#define VAR_LEGENDS_STARTER_RANDOM_1 2
#define VAR_LEGENDS_STARTER_RANDOM_2 3
#define VAR_LEGENDS_STARTER_RANDOM_3 4
#define FLAG_RESCUED_BIRCH 0
#define EVOLUTIONS_END 0
#define EVO_LEVEL 1
#define TRAINER_CLASS_RIVAL 1
#define TRAINER_PIC_BRENDAN 1
#define TRAINER_PIC_MAY 2
#define ABILITY_NONE 0
#define RNG_NONE 0
struct Evolution {u16 method,param,targetSpecies;};
struct SpeciesInfo {u16 natDexNum,base;const struct Evolution *evolutions;};
struct Trainer {u8 trainerClass,trainerPic;};
struct TrainerMon {u16 species,moves[4],ability,teraType,heldItem,iv;u8 lvl;};
static u16 vars[5]; static bool32 rescued;
static u32 seed=1, draws;
u16 VarGet(u16 id) {return vars[id];}
void VarSet(u16 id,u16 v) {vars[id]=v;}
bool32 FlagGet(u16 id) {(void)id;return rescued;}
u32 RandomUniform(u32 tag,u32 lo,u32 hi) {(void)tag;draws++;seed=seed*1664525+1013904223;return lo+seed%(hi-lo+1);}
void Shuffle16(void *data,size_t n) {u16 *p=data;for(size_t i=n-1;i;i--){u32 j=RandomUniform(0,0,i);u16 t=p[i];p[i]=p[j];p[j]=t;}}
extern const struct SpeciesInfo gSpeciesInfo[];
bool32 IsSpeciesEnabled(u16 s) {return s>0&&s<NUM_SPECIES&&gSpeciesInfo[s].natDexNum>0;}
const struct Evolution *GetSpeciesEvolutions(u16 s) {return gSpeciesInfo[s].evolutions;}
#define GET_BASE_SPECIES_ID(s) (gSpeciesInfo[s].base)
'''
tests = r'''
int main(void) {
assert(LegendsGetStarterSetting()==LEGENDS_STARTERS_GEN_3);
assert(LegendsGetStarterPokemon(0)==SPECIES_TREECKO);
assert(LegendsGetStarterPokemon(3)==SPECIES_TREECKO);
for(u8 mode=0;mode<=LEGENDS_STARTERS_SPECIAL;mode++) {
    memset(vars,0,sizeof(vars));rescued=TRUE; // Native script sets this before bag opens.
    LegendsSetStarterSetting(mode);LegendsPrepareStarters();
    for(u8 i=0;i<3;i++)assert(LegendsGetStarterPokemon(i)==sStarterSets[mode][i]);
    LegendsSetStarterSetting(LEGENDS_STARTERS_GEN_9);
    for(u8 i=0;i<3;i++)assert(LegendsGetStarterPokemon(i)==sStarterSets[mode][i]);
}
// A legacy save must retain Gen 3 even when its next-game preference changes.
memset(vars,0,sizeof(vars));rescued=TRUE;LegendsSetStarterSetting(LEGENDS_STARTERS_GEN_9);
assert(GetRescueSetting()==LEGENDS_STARTERS_GEN_3);
LegendsSetStarterSetting(255);assert(LegendsGetStarterSetting()==LEGENDS_STARTERS_GEN_3);
assert(sStarterSets[LEGENDS_STARTERS_SPECIAL][0]==SPECIES_HAPPINY);
assert(sStarterSets[LEGENDS_STARTERS_SPECIAL][1]==SPECIES_WATTREL);
assert(sStarterSets[LEGENDS_STARTERS_SPECIAL][2]==SPECIES_MANKEY);
for(u32 trial=0;trial<200;trial++) {
    memset(vars,0,sizeof(vars));rescued=TRUE;LegendsSetStarterSetting(LEGENDS_STARTERS_RANDOM);LegendsPrepareStarters();
    u16 a=LegendsGetStarterPokemon(0),b=LegendsGetStarterPokemon(1),c=LegendsGetStarterPokemon(2);
    assert(a!=b&&a!=c&&b!=c);
    u16 choices[]={a,b,c};
    for(u8 i=0;i<3;i++) {
        assert(IsSpeciesEnabled(choices[i]));assert(GET_BASE_SPECIES_ID(choices[i])==choices[i]);
        assert(gSpeciesInfo[choices[i]].evolutions[0].method!=EVOLUTIONS_END);
        for(u32 s=1;s<NUM_SPECIES;s++)if(IsSpeciesEnabled(s)) {
            const struct Evolution *e=GetSpeciesEvolutions(s);
            for(u32 j=0;e&&e[j].method;j++)assert(e[j].targetSpecies!=choices[i]);
        }
    }
    u32 before=draws;LegendsPrepareStarters();LegendsSetStarterSetting(LEGENDS_STARTERS_GEN_1);
    assert(draws==before&&LegendsGetStarterPokemon(0)==a&&LegendsGetStarterPokemon(1)==b&&LegendsGetStarterPokemon(2)==c);
}
'''
# Validate both genders, every actual story battle and optional Rustboro team.
parties = (root / 'src/data/trainers.party').read_text()
count = 0
for match in re.finditer(r'=== (TRAINER_(?:MAY|BRENDAN)_(?!PLACEHOLDER)\w+) ===(.*?)(?====|\Z)', parties, re.S):
    name,body = match.groups()
    for species,level in re.findall(r'\n([A-Za-z]+)\nLevel: (\d+)', body):
        original = 'SPECIES_'+species.upper()
        family = next((i for i,group in enumerate([['TREECKO','GROVYLE','SCEPTILE'],['TORCHIC','COMBUSKEN','BLAZIKEN'],['MUDKIP','MARSHTOMP','SWAMPERT']]) if species.upper() in group), None)
        if family is None:
            continue
        count += 1
        pic = 'TRAINER_PIC_MAY' if '_MAY_' in name else 'TRAINER_PIC_BRENDAN'
        tests += f'{{struct Trainer trainer={{TRAINER_CLASS_RIVAL,{pic}}};struct TrainerMon original={{{original},{{1,2,3,4}},9,9,7,31,{level}}};\n'
        tests += 'for(u8 mode=0;mode<LEGENDS_STARTERS_COUNT;mode++){vars[1]=mode+1;struct TrainerMon mon=original;LegendsCustomizeRivalMon(&trainer,&mon);\n'
        tests += f'if(mode==LEGENDS_STARTERS_GEN_3)assert(!memcmp(&mon,&original,sizeof(mon)));else{{u16 expected=mode>=LEGENDS_STARTERS_SPECIAL?SPECIES_ZORUA:sStarterSets[mode][{family}];\n'
        tests += 'for(u8 stage=0;stage<2;stage++){const struct Evolution *e=GetSpeciesEvolutions(expected);u16 next=expected;for(u8 j=0;e&&e[j].method;j++)if(e[j].method==EVO_LEVEL&&e[j].param<=mon.lvl){next=e[j].targetSpecies;break;}expected=next;}\n'
        tests += 'assert(mon.species==expected&&mon.lvl==original.lvl&&mon.heldItem==7&&mon.iv==31);assert(mon.moves[0]==0&&mon.ability==0&&mon.teraType==0);}}}\n'
tests += r'''
vars[1]=LEGENDS_STARTERS_SPECIAL+1;
struct Trainer rival={1,2};struct TrainerMon mon={.species=SPECIES_ZIGZAGOON,.lvl=31};
LegendsCustomizeRivalMon(&rival,&mon);assert(mon.species==SPECIES_ZIGZAGOON);
assert(EvolveRivalByLevel(SPECIES_ZORUA,29)==SPECIES_ZORUA);
assert(EvolveRivalByLevel(SPECIES_ZORUA,30)==SPECIES_ZOROARK);
puts("Generation/Special choices, stable distinct Random trios, legacy saves and every native rival starter team passed.");
}
'''
assert count == 30, count
with tempfile.TemporaryDirectory() as directory:
    tmp=Path(directory);(tmp/'species.h').write_text((root/'include/constants/species.h').read_text())
    (tmp/'test.c').write_text(stub+'\n'+header+'\n'+'\n'.join(fixtures)+'\n'+source+'\n'+tests)
    subprocess.run(['cc','-std=gnu11','-Wall','-Wextra','-Werror',str(tmp/'test.c'),'-o',str(tmp/'check')],check=True)
    subprocess.run([str(tmp/'check')],check=True)
print(f'Checked {count} rival teams across all 11 modes against native evolution metadata.')
