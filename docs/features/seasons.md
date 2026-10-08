# Seasonal System

**Status:** Implemented in 0.0.11; refined in 0.0.12; new-game initialization fixed in 0.0.12.1. Release and Debug share identical seasonal mechanics.

## Modes and time

On the Legends Options page, use Left/Right on SEASONS to choose REAL TIME (default) or 7H PLAY. CURRENT shows the active environment. SET SEASON is editable with Left/Right only in gameplay mode; REAL TIME shows CALENDAR. A manual selection restarts the selected season’s seven-hour timer, and takes effect on the next faded map load. Leaving Options commits the setting; an ordinary game save persists it.

Real time uses the expansion's native RTC calendar directly, independent of the bedroom clock's offset. Northern Hemisphere calendar seasons are March-May Spring, June-August Summer, September-November Autumn and December-February Winter. Enable your emulator's RTC. RTC errors or invalid months fall back to the saved gameplay cycle. A valid but frozen emulator clock cannot be detected automatically; choose 7H PLAY if needed.

7H PLAY follows Spring → Summer → Autumn → Winter, repeating every 28 hours, with exactly seven gameplay hours per season. It counts active time recorded by Emerald, including menus and battles, not time while closed. Older saves initialize from recorded hours/minutes/seconds (a 40-hour save starts in Summer). The clock accumulates in both modes, so changing modes does not reset progress. Manually changing SET SEASON does reset its timer. Existing 0.0.11 cycle seconds normalize modulo the shorter 28-hour cycle without losing sub-second progress. Permanent event vars store cycle seconds and sub-second frames; time continues beyond the native 999:59:59 display cap. Ordinary saves persist progress; emulator save states restore their own earlier progress.

## New Game and title-screen Options

As of 0.0.12.1, returning from title-screen Options stages the chosen Legends settings outside the SaveBlocks. New Game clears its normal save data, applies those staged settings once, and commits the starting season before loading the truck/opening maps. Gameplay mode starts a fresh seven-hour timer for the selected season and does not require the bedroom clock to be set. Real-time mode still uses the RTC calendar. A fresh title entry clears staging; starting New Game without visiting title-screen Options uses normal defaults. Continue and in-game Options keep their existing save behavior.

## Environment

Outdoor vegetation uses fresh spring greens, deeper summer greens, amber autumn foliage and frosted winter tones. Only green RGB555 colors in map palettes 1-12 are transformed, excluding blue water, neutral buildings, transparent entries, palette zero, UI and NPC/object palettes. Shared colors may affect more than one tile type. This is a palette treatment, not new tile art or collision geometry: paths remain passable and water remains surfable.

Processing starts from original tileset colors, composes with native alternate/day-night palettes, then uses native weather processing. Repeated refreshes cannot stack tints. Rain, thunderstorms, horizontal fog, snow and clouds reuse native effects. Conditions are stable by region and the committed RTC day (or seven-hour gameplay season), without consuming battle RNG or rerolling on building exits. Spring gets showers, summer occasional storms, autumn occasional fog and mainland winter intermittent snow/clouds. Rainforest routes retain native rainfall when the seasonal rule does not override it.

Mt. Chimney, Jagged Pass, Fiery Path, Lavaridge, Fallarbor and Routes 112/113 retain their volcanic/ash appearance and weather. Route 111 is excluded as a whole because its desert and grasslands share one map. Maps with native ash or sandstorm are excluded. Oceans use clouds/rain without seasonal snow; Dewford, Pacifidlog and Sootopolis also avoid seasonal snowfall. Interiors, caves, secret bases and underwater maps remain unchanged.

Only ordinary sunny/cloud/rain/thunder requests are seasonally remapped. Drought, downpour, Groudon/Kyogre abnormal weather, ash, sandstorm, underwater effects, shade, special fog and explicit no-weather requests retain native behavior. The original script/map request is stored separately so seasonal snow is never mistaken for permanent map weather after saving or switching seasons.

The clock determines a pending season, while saved active-season and weather-day snapshots control the visible environment. Full faded map loads commit the pending state before applying native palettes/weather. Entering or leaving a building, a faded warp, and save continue apply it; seamless route crossings and returns from menus/battles retain the active state. No mid-walk palette/weather change or extra interruption is added. CURRENT can therefore differ from SET SEASON while a change is pending. Native day/night updates continue using the active season.

## Maintenance and validation

`src/legends_seasons.c` and `include/legends_seasons.h` own the rules. Integration points are native playtime, map palette loading, day/night palette rebuilding, weather requests, save continue and paged Options. Vars 0x40F7-0x40FE were unused and are now reserved. No SaveBlock layout change is required. Seasonal encounters and story events remain future work.

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
