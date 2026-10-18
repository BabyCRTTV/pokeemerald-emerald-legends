"""Explicitly package the documented Pokédex's game cries for browser playback."""
import json, wave
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
WIKI=ROOT/'docs/wiki'
# The National Dex snapshot represents these default forms.
FORMS=dict(SHAYMIN='land',TORNADUS='incarnate',THUNDURUS='incarnate',LANDORUS='incarnate',ZYGARDE='50',HOOPA='confined',ORICORIO='baile',LYCANROC='midday',WISHIWASHI='solo',TOXTRICITY='amped',EISCUE='ice',INDEEDEE='m',MORPEKO='full_belly',ZACIAN='hero',ZAMAZENTA='hero',URSHIFU='single_strike',ENAMORUS='incarnate',OINKOLOGNE='m',MAUSHOLD='four',PALAFIN='hero',TATSUGIRI='curly',GIMMIGHOUL='chest')
if __name__=='__main__':
    for p in json.loads((WIKI/'dex-data.json').read_text())['species']:
        cry=p.get('crySpecies',p['id'])
        stem=cry.lower()+('_'+FORMS[cry] if cry in FORMS else '')
        source=ROOT/'sound/direct_sound_samples/cries'/f'{stem}.wav'
        with wave.open(str(source)) as audio:
            assert audio.getnframes()>0 and audio.getcomptype()=='NONE',p['id']
    (WIKI/'cry-forms.js').write_text('/* Default-form cry aliases verified against the game source. */\nwindow.LegendsCryForms = '+json.dumps(FORMS,sort_keys=True)+';\n')
    print('Verified source cries, including documented forms and Da Bug; generated default-form aliases')
