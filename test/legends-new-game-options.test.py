"""Compile the title-options bridge and seasons against native save-reset semantics."""
import ast
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
# Reuse the engine fixtures without executing the other test's cases.
fixture = ast.parse((ROOT / 'test/legends-seasons.test.py').read_text())
values = {node.targets[0].id: ast.literal_eval(node.value)
          for node in fixture.body if isinstance(node, ast.Assign)
          and isinstance(node.targets[0], ast.Name)
          and node.targets[0].id in ('COMMON', 'HARNESS')}
common = values['COMMON'].replace('typedef uint8_t u8;', 'typedef uint8_t u8;\ntypedef uint8_t bool8;\n#define EWRAM_DATA')
common = common.replace('#endif', '''bool32 FlagGet(u16);
void FlagSet(u16);
void FlagClear(u16);
bool32 CheckBagHasItem(u16, u16);
bool32 AddBagItem(u16, u16);
u8 CurrentBattlePyramidLocation(void);
#endif''')
starter_source = (ROOT / 'src/legends_starters.c').read_text()
def starter_function(name):
    start = starter_source.index(name + '\n{')
    return starter_source[start:starter_source.index('\n}', start) + 2]
harness = values['HARNESS'].split('int main(void)')[0] + r'''
#include "legends_settings.h"
#include "legends_starters.h"
#include "constants/flags.h"
u8 flags[4096];
bool32 FlagGet(u16 n) {return flags[n];}
void FlagSet(u16 n) {flags[n] = TRUE;}
void FlagClear(u16 n) {flags[n] = FALSE;}
bool32 CheckBagHasItem(u16 i, u16 n) {(void)i; (void)n; return TRUE;}
void LegendsEnsureDaBugGift(void) {} // Gift behavior has its own actual-module harness.
bool32 AddBagItem(u16 i, u16 n) {(void)i; (void)n; return TRUE;}
u8 CurrentBattlePyramidLocation(void) {return 0;}
void newSave(void)
{
    memset(vars, 0, sizeof(vars));
    memset(flags, 0, sizeof(flags));
    memset(&save, 0, sizeof(save));
    LegendsInitNewGameSettings();
    LegendsApplyTitleOptionsToNewGame();
}
int main(void)
{
    month = 10;
    LegendsClearTitleOptions();
    LegendsSetStarterSetting(LEGENDS_STARTERS_SPECIAL);
    LegendsSetExpShareEnabled(FALSE);
    LegendsSetFollowersEnabled(FALSE);
    LegendsSetShinyRateSetting(LEGENDS_SHINY_RATE_1226);
    LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
    LegendsSetPlaytimeSeason(LEGENDS_WINTER);
    LegendsStageTitleOptions();
    newSave();
    assert(LegendsGetStarterSetting() == LEGENDS_STARTERS_SPECIAL);
    assert(!LegendsIsExpShareEnabled());
    assert(!LegendsAreFollowersEnabled());
    assert(LegendsGetWildShinyRateDenominator() == 1226);
    assert(LegendsGetSeasonMode() == LEGENDS_SEASONS_PLAYTIME);
    assert(LegendsGetActiveSeason() == LEGENDS_WINTER);
    assert(LegendsGetSeason() == LEGENDS_WINTER);
    assert(save.playTimeHours == 0 && save.playTimeMinutes == 0);
    assert(VarGet(VAR_LEGENDS_SEASON_FRAMES) == 0);
    assert(!FlagGet(FLAG_SYS_CLOCK_SET));
    assert(!FlagGet(FLAG_SYS_POKEDEX_GET));
    assert(VarGet(VAR_DAYS) == 0);
    // Selection is consumed once; subsequent new saves use normal defaults.
    newSave();
    assert(LegendsIsExpShareEnabled());
    assert(LegendsAreFollowersEnabled());
    assert(LegendsGetWildShinyRateDenominator() == 8192);
    assert(LegendsGetSeasonMode() == LEGENDS_SEASONS_RTC);
    assert(LegendsGetActiveSeason() == LEGENDS_AUTUMN);
    // Existing saves default ON; OFF survives field/continue initialization.
    LegendsSetFollowersEnabled(FALSE);
    LegendsRestoreUnlocksOnContinue();
    assert(!LegendsAreFollowersEnabled());
    LegendsSetFollowersEnabled(TRUE);
    assert(LegendsAreFollowersEnabled());
    // Reopening title Options replaces the complete staged choice.
    LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
    LegendsSetPlaytimeSeason(LEGENDS_SUMMER);
    LegendsStageTitleOptions();
    LegendsSetSeasonMode(LEGENDS_SEASONS_RTC);
    LegendsSetShinyRateSetting(LEGENDS_SHINY_RATE_5680);
    LegendsStageTitleOptions();
    newSave();
    assert(LegendsGetSeasonMode() == LEGENDS_SEASONS_RTC);
    assert(LegendsGetActiveSeason() == LEGENDS_AUTUMN);
    assert(LegendsGetWildShinyRateDenominator() == 5680);
    // Fresh title entry invalidates staging; do not inherit a previous save.
    LegendsSetExpShareEnabled(FALSE);
    LegendsSetSeasonMode(LEGENDS_SEASONS_PLAYTIME);
    LegendsSetPlaytimeSeason(LEGENDS_SUMMER);
    LegendsStageTitleOptions();
    LegendsClearTitleOptions();
    newSave();
    assert(LegendsIsExpShareEnabled());
    assert(LegendsAreFollowersEnabled());
    assert(LegendsGetWildShinyRateDenominator() == 8192);
    assert(LegendsGetSeasonMode() == LEGENDS_SEASONS_RTC);
    puts("Title choices survive save reset, initialize before the bedroom clock, replace previous edits, consume once and clear on fresh title entry.");
}
'''
harness = harness.replace('void newSave(void)', starter_function('u8 LegendsGetStarterSetting(void)') + '\n' + starter_function('void LegendsSetStarterSetting(u8 setting)') + '\nvoid newSave(void)')
# Assert the actual lifecycle hooks used by the native game, not just the mocks.
new_game = (ROOT / 'src/new_game.c').read_text()
start = new_game.index('void NewGameInitData(void)')
order = ['ClearSav1();', 'InitEventData();', 'LegendsInitNewGameSettings();',
         'LegendsApplyTitleOptionsToNewGame();', 'WarpToTruck();']
positions = [new_game.index(item, start) for item in order]
assert positions == sorted(positions)
main_menu = (ROOT / 'src/main_menu.c').read_text()
assert 'LegendsClearTitleOptions();' in main_menu.split('void CB2_InitMainMenu(void)')[1].split('void CB2_ReinitMainMenu(void)')[0]
assert 'LegendsStageTitleOptions();' in main_menu.split('void CB2_ReinitMainMenu(void)')[1].split('static u32 InitMainMenu')[0]
with tempfile.TemporaryDirectory() as directory:
    tmp = Path(directory)
    (tmp / 'global.h').write_text(common)
    (tmp / 'legends_starters.h').write_text((ROOT / 'include/legends_starters.h').read_text())
    for name in ['event_data.h', 'field_weather.h', 'overworld.h', 'palette.h', 'rtc.h', 'item.h', 'battle_pyramid.h']:
        (tmp / name).write_text('#include "global.h"\n')
    (tmp / 'constants').mkdir()
    names = ['MT_CHIMNEY', 'JAGGED_PASS', 'FIERY_PATH', 'LAVARIDGE_TOWN', 'FALLARBOR_TOWN', 'ROUTE_111', 'ROUTE_112', 'ROUTE_113', 'DEWFORD_TOWN', 'PACIFIDLOG_TOWN', 'SOOTOPOLIS_CITY', 'TEST_ROUTE']
    (tmp / 'constants/region_map_sections.h').write_text('\n'.join(f'#define MAPSEC_{name} {i}' for i, name in enumerate(names)))
    (tmp / 'constants/items.h').write_text('#define ITEM_EXP_SHARE 1\n')
    flag_names = ['LEGENDS_EXP_SHARE', 'LEGENDS_SETTINGS_INITIALIZED', 'SYS_POKEDEX_GET', 'LEGENDS_DEXNAV_UNLOCKED', 'LEGENDS_DEXNAV_DETECTOR_MODE', 'STORING_ITEMS_IN_PYRAMID_BAG', 'SYS_CLOCK_SET', 'LEGENDS_FOLLOWERS_DISABLED']
    (tmp / 'constants/flags.h').write_text('\n'.join(f'#define FLAG_{name} {i}' for i, name in enumerate(flag_names)))
    (tmp / 'constants/battle_frontier.h').write_text('#define PYRAMID_LOCATION_NONE 0\n')
    (tmp / 'harness.c').write_text(harness)
    subprocess.run(['cc', '-std=c99', '-Wall', '-Wextra', '-Werror', '-I', str(tmp), '-I', str(ROOT / 'include'), str(ROOT / 'src/legends_settings.c'), str(ROOT / 'src/legends_seasons.c'), str(tmp / 'harness.c'), '-o', str(tmp / 'check')], check=True)
    subprocess.run([str(tmp / 'check')], check=True)
