# Seasonal System

**Status:** Implemented in 0.0.11; refined in 0.0.12; new-game initialization fixed in 0.0.12.1; Kanto foliage and seasonal battle backgrounds fixed in 0.0.30. Release and Debug share identical seasonal mechanics.

## Modes and time

On the Legends Options page, use Left/Right on SEASONS to choose REAL TIME (default) or 7H PLAY. CURRENT shows the active environment. SET SEASON is editable with Left/Right only in gameplay mode; REAL TIME shows CALENDAR. A manual selection restarts the selected season’s seven-hour timer, and takes effect on the next faded map load. Leaving Options commits the setting; an ordinary game save persists it.

Real time uses the expansion's native RTC calendar directly, independent of the bedroom clock's offset. Northern Hemisphere calendar seasons are March-May Spring, June-August Summer, September-November Autumn and December-February Winter. Enable your emulator's RTC. RTC errors or invalid months fall back to the saved gameplay cycle. A valid but frozen emulator clock cannot be detected automatically; choose 7H PLAY if needed.

7H PLAY follows Spring → Summer → Autumn → Winter, repeating every 28 hours, with exactly seven gameplay hours per season. It counts active time recorded by Emerald, including menus and battles, not time while closed. Older saves initialize from recorded hours/minutes/seconds (a 40-hour save starts in Summer). The clock accumulates in both modes, so changing modes does not reset progress. Manually changing SET SEASON does reset its timer. Existing 0.0.11 cycle seconds normalize modulo the shorter 28-hour cycle without losing sub-second progress. Permanent event vars store cycle seconds and sub-second frames; time continues beyond the native 999:59:59 display cap. Ordinary saves persist progress; emulator save states restore their own earlier progress.

## New Game and title-screen Options

As of 0.0.12.1, returning from title-screen Options stages the chosen Legends settings outside the SaveBlocks. New Game clears its normal save data, applies those staged settings once, and commits the starting season before loading the truck/opening maps. Gameplay mode starts a fresh seven-hour timer for the selected season and does not require the bedroom clock to be set. Real-time mode still uses the RTC calendar. A fresh title entry clears staging; starting New Game without visiting title-screen Options uses normal defaults. Continue and in-game Options keep their existing save behavior.

## Environment

Outdoor vegetation uses fresh spring greens, deeper summer greens, amber autumn foliage and frosted winter tones. Only green RGB555 colors in map palettes 1-12 are transformed, excluding blue water, neutral buildings, transparent entries, palette zero, UI and NPC/object palettes. Shared colors may affect more than one tile type. This is a palette treatment, not new tile art or collision geometry: paths remain passable and water remains surfable.

Processing starts from original tileset colors, composes with native alternate/day-night palettes, then uses native weather processing. Repeated refreshes cannot stack tints. Since v0.0.22, ambient conditions use [regional dynamic forecasts](weather.md), with rain, storms, fog and limited winter upland snow. Forecasts use local RNG independently of battle randomness.

Mt. Chimney, Jagged Pass, Fiery Path, Lavaridge, Fallarbor and Routes 112/113 retain their volcanic/ash appearance and weather. Route 111 is excluded as a whole because its desert and grasslands share one map. Maps with native ash or sandstorm are excluded. Oceans use clouds/rain without seasonal snow; Dewford, Pacifidlog and Sootopolis also avoid seasonal snowfall. Interiors, caves, secret bases and underwater maps remain unchanged.

Only ordinary sunny/cloud/rain/thunder requests are seasonally remapped. Drought, downpour, Groudon/Kyogre abnormal weather, ash, sandstorm, underwater effects, shade, special fog and explicit no-weather requests retain native behavior. The original script/map request is stored separately so seasonal snow is never mistaken for permanent map weather after saving or switching seasons.

The clock determines a pending season, while the saved active-season snapshot controls visible foliage. Full faded map loads commit the pending state before applying native palettes/weather. Entering or leaving a building, a faded warp, and save continue apply it; seamless route crossings and returns from menus/battles retain the active state. No mid-walk seasonal palette change or extra interruption is added. Dynamic weather has its own timer and may transition while walking. CURRENT can therefore differ from SET SEASON while a change is pending. Native day/night updates continue using the active season.

## Maintenance and validation

`src/legends_seasons.c` and `include/legends_seasons.h` own the rules. Integration points are native playtime, map palette loading, day/night palette rebuilding, weather requests, save continue and paged Options. Vars 0x40F7-0x40FE were unused and are now reserved; dynamic weather also reserves 0x40FF and flag 0x26C. No SaveBlock layout change is required. Seasonal encounters and story events remain future work.

Run `python3 test/legends-seasons.test.py` for host C regression checks. See [QA](../QA.md) for manual emulator scenarios. Native builds and patch verification do not replace visual playtesting.

## Grass effects and winter scuffs (v0.0.16)

Grass rustle, jump, short/long and shaking effects use a dedicated sprite palette
with the same vegetation color conversion as map palettes. Each load starts from
the native palette, including cached tags and connected transitions to excluded
ash/desert maps. Water and ash keep their own palette.

On standard General-tileset tall grass in winter, movement clears the snowy tuft
visually, inspired by native ash grass. The renderer substitutes ordinary ground
art without changing the map-grid entry: grass encounters, collision, elevation
and field-move checks remain intact. A 1280-byte per-map bitset tracks scuffed
cells; full map initialization clears it. It is never written to the save.
Tree-edge and long grass retain native artwork. `legends_grass.c` owns tracking;
`field_effect_helpers.c`, `field_camera.c` and `fieldmap.c` supply the hooks.

## Kanto foliage and battle backgrounds (v0.0.30)

FRLG's imported Kanto General tileset puts grass and tree colors in palette slot zero. This tileset now receives seasonal conversion there, excluding transparent entry zero; Hoenn retains its protected slot-zero behavior. Native day/night rebuilds reload the original Kanto palette and then apply the active season, so time changes cannot restore green foliage or accumulate tints. Blue water colors keep their original values. Interiors still have no seasonal foliage treatment.

Both Hoenn and Kanto battles use the same visible active-season snapshot as the overworld. Grass, long grass and ordinary outdoor plain backgrounds receive spring/summer greens, autumn amber and winter frost. The entry grass shares these colors. Both normal battle initialization and staged palette loads/background restores start from the original art each time; no tint stacking. Pokemon, trainers, healthboxes and battle text palettes remain separate.

Water, pond, underwater, cave, sand, rock/mountain and all other special environment art remains native. Indoor maps, the protected volcanic/desert belt, facilities, linked/recorded battles and special legendary battles are excluded. Native environment IDs and Nature Power/Secret Power/Camouflage effects are unchanged; seasonal appearance is cosmetic. Terrain move animation backgrounds remain native and restore the seasonal main background when they end.

`src/legends_battle_seasons.c` owns the narrow battle-palette policy. `test/legends-season-scenes.test.py` compiles the actual loader, native LoadPalette, seasonal color conversion and overworld palette rebuild with real battle/Kanto colors. It verifies all seasons, exclusions, protected slots, fresh reloads, Kanto grass/tree conversion and unchanged blue water. A native-tile battle preview was visually inspected. Emulator checks: compare grass/long-grass/plain encounters in both regions across all seasons; trigger a move that replaces/restores the background; enter a cave, Surf, challenge a Gym, and return to ordinary grass; verify Kanto foliage before/after a day/night update. These visual emulator checks remain outstanding.

### Outdoor battle stripe fix — v0.0.32.1

Bare-ground/event/trainer encounters can choose PLAIN while tall-grass encounters choose GRASS. The plain palette's almost-white stripe and cyan sky ramp fall outside vegetation color detection. Before seasonal tinting, the plain loader now copies the native tall-grass stripe (index 1) and sky ramp (indices 11–15) in its two background banks. It preserves the remaining plain platform colors and tiles, native terrain mechanics, sprites and UI palettes. All four seasons and all twenty native map-weather IDs are checked with wild, scripted first-battle and ordinary trainer flags. Sandstorm, volcanic ash, indoor and special battle exclusions remain native. The existing initial load and animation restoration both use this loader.

Validation for this fix: mGBA 0.10.2 booted the privately compiled Debug ROM and rendered 240 native battle scenes (four active seasons × twenty map-weather inputs × tall-grass Poochyena / plain first-battle Stunky / May Route 103). Native party creation and battle initialization were invoked from a private, test-only callback; no harness or complete ROM is published. Eligible shared ramp slots were compared from the emulated palette buffers and representative screens visually reviewed. May uses native terrain selection; dynamic weather resolved to sandstorm in this sample and correctly selected the excluded native sand background. Stunky and May were also advanced to the Torchic command screen, with consistent stripes, portraits, sprites and healthboxes. Full story traversal and unrelated seasonal map checks listed above remain separate playtest work.
