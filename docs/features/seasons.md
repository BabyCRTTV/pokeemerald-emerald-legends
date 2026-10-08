# Seasonal System

**Status:** Implemented in 0.0.11. Release and Debug share identical seasonal mechanics.

## Modes and time

On the Legends Options page, use Left/Right on SEASONS to choose REAL TIME (default) or 28H PLAY. CURRENT previews the season for that choice without committing edits. Leaving Options commits the setting; an ordinary game save persists it.

Real time uses the expansion's native RTC calendar directly, independent of the bedroom clock's offset. Northern Hemisphere calendar seasons are March-May Spring, June-August Summer, September-November Autumn and December-February Winter. Enable your emulator's RTC. RTC errors or invalid months fall back to the saved gameplay cycle. A valid but frozen emulator clock cannot be detected automatically; choose 28H PLAY if needed.

28H PLAY follows Spring → Summer → Autumn → Winter, repeating every 112 hours, with exactly 28 gameplay hours per season. It counts active time recorded by Emerald, including menus and battles, not time while closed. Older saves initialize from recorded hours/minutes/seconds (a 40-hour save starts in Summer). The clock accumulates in both modes, so changing modes does not reset progress. Permanent event vars store cycle seconds and sub-second frames; time continues beyond the native 999:59:59 display cap. Ordinary saves persist progress; emulator save states restore their own earlier progress.

## Environment

Outdoor vegetation uses fresh spring greens, deeper summer greens, amber autumn foliage and frosted winter tones. Only green RGB555 colors in map palettes 1-12 are transformed, excluding blue water, neutral buildings, transparent entries, palette zero, UI and NPC/object palettes. Shared colors may affect more than one tile type. This is a palette treatment, not new tile art or collision geometry: paths remain passable and water remains surfable.

Processing starts from original tileset colors, composes with native alternate/day-night palettes, then uses native weather processing. Repeated refreshes cannot stack tints. Rain, thunderstorms, horizontal fog, snow and clouds reuse native effects. Conditions are stable by region and RTC day (or seven gameplay hours), without consuming battle RNG or rerolling on building exits. Spring gets showers, summer occasional storms, autumn occasional fog and mainland winter intermittent snow/clouds. Rainforest routes retain native rainfall when the seasonal rule does not override it.

Mt. Chimney, Jagged Pass, Fiery Path, Lavaridge, Fallarbor and Routes 112/113 retain their volcanic/ash appearance and weather. Route 111 is excluded as a whole because its desert and grasslands share one map. Maps with native ash or sandstorm are excluded. Oceans use clouds/rain without seasonal snow; Dewford, Pacifidlog and Sootopolis also avoid seasonal snowfall. Interiors, caves, secret bases and underwater maps remain unchanged.

Only ordinary sunny/cloud/rain/thunder requests are seasonally remapped. Drought, downpour, Groudon/Kyogre abnormal weather, ash, sandstorm, underwater effects, shade, special fog and explicit no-weather requests retain native behavior. The original script/map request is stored separately so seasonal snow is never mistaken for permanent map weather after saving or switching seasons.

The module checks season/weather changes once per overworld second, waiting for palette fades, active scripts and weather palette transitions before refreshing. Map loads and returns from menus/battles apply current colors; continue reevaluates weather against the current season.

## Maintenance and validation

`src/legends_seasons.c` and `include/legends_seasons.h` own the rules. Integration points are native playtime, map palette loading, day/night palette rebuilding, weather requests, save continue and paged Options. Vars 0x40F7-0x40FC were unused and are now reserved. No SaveBlock layout change is required. Seasonal encounters and story events remain future work.

Run `python3 test/legends-seasons.test.py` for host C regression checks. See [QA](../QA.md) for manual emulator scenarios. Native builds and patch verification do not replace visual playtesting.
