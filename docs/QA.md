# Pokémon Emerald: Legends — Quality Assurance

Baseline: v0.0.8. Maintenance checks added in v0.0.8.1.

## Automated checks

- VERSION, canonical/Release/Debug changelogs, homepage, patcher, and in-game version labels stay synchronized.
- Source-level checks cover the Options page allocation, Legends EXP Share flags/save initialization, Rustboro Lucky Egg, and Birch National Dex / Champion rewards.
- Node regression tests cover browser BPS SourceRead, TargetRead, TargetCopy overlaps, source and patch CRC rejection, target CRC rejection, and stale ROM selection.
- Build workflow compiles both Debug and Release ROMs, verifies a freshly built clean Emerald base SHA-1, reapplies generated BPS patches, and byte-compares both results with compiled ROMs.
- No copyrighted full .gba images are committed or distributed.

## Manual emulator regression checklist (not yet verified)

- [ ] Start new Release and Debug saves and confirm only Debug exposes developer utilities.
- [ ] Open Options; switch General/Legends using L/R with normal controls and L=A mode, modify settings, save/reload, inspect borders and CANCEL.
- [ ] Continue an older save and confirm EXP Share initializes only once. Toggle OFF, save/reload, and confirm it stays OFF.
- [ ] Battle with participants, benched Pokémon, fainted Pokémon and Eggs with EXP Share ON/OFF and Lucky Egg; check resulting EXP.
- [ ] Use each of the eight badge-earned HM utilities without taught HMs, preserving terrain, story, follower and Regi-puzzle gates.
- [ ] Receive the Rustboro Lucky Egg exactly once after Steven's letter.
- [ ] Receive early National Pokédex; test Champion Rare Candy delivery to Bag, PC, and deferred state when both are full, including postgame saves.
- [ ] Patch Release and Debug on Android and desktop using a clean Emerald ROM; try switching files midway and rejecting wrong ROMs.

CI passing does not establish emulator gameplay correctness. Record emulator version, save state and observed outcome before checking a manual item off.

## v0.0.9 manual regressions (not yet verified)

- [ ] New game: Exp. Share is a Key Item immediately and USE changes Legends Options.
- [ ] Existing save with EXP SHARE OFF: receive item on continue without altering setting; no duplicate Key Items on reload.
- [ ] Before Birch's Pokédex: DexNav is hidden from Start menu.
- [ ] After Birch's Pokédex: DexNav appears and searches wild encounter slots.
- [ ] Existing save with Pokédex: DexNav appears immediately upon continue, detector mode works.
- [ ] Battle Pyramid temporary Bag is not modified by missing-item restoration.

## v0.0.10 manual shiny rate regression checks (not yet verified)

- [ ] Existing v0.0.9 save opens Legends 2/2 with SHINY RATE 1/8192 by default.
- [ ] Cycle Left/Right through all 1/8192, 1/5680 and 1/1226; no clipped text or broken border.
- [ ] Save after selecting 1/5680, restart the ROM and confirm it persists; switch to 1/1226 and repeat.
- [ ] Generate multiple wild encounters in grass, surf, fishing and DexNav with each rate, verifying shiny rolls use the stored setting.
- [ ] Check Shiny Charm, chain-fishing and DexNav bonuses remain additive to the selected base odds.
- [ ] Verify already caught Pokémon, eggs, gifts and scripted Pokémon do not have shininess unexpectedly altered.
- [ ] Validate the normal Release build and Debug build against clean base ROMs on mGBA and Pizza Boy.

## Seasons (0.0.11)

Automated: `python3 test/legends-seasons.test.py` compiles the actual season module with engine mocks and verifies all twelve calendar months, 28-hour boundaries, complete cycle rollover, persisted sub-second progress, older-save migration, 999-hour continuation, invalid RTC fallback, regional exclusions, unchanged special weather, deterministic snow frequency, ocean snow exclusion, full RGB555 bounds, protected palette slots, and fade/script refresh deferral. Both native variants and BPS reapplication are verified by the release workflow.

Manual emulator checks (not replaced by host tests):
- With RTC enabled, visit Littleroot, Route 104, Fortree, Route 119 and Lilycove in March, July, October and January; inspect foliage, contrast, water and buildings during day and night.
- Switch REAL TIME / 28H PLAY in Legends Options; confirm CURRENT previews without saving the mode until leaving Options, and mode persists after an ordinary save/reload.
- At 27:59:59, 55:59:59, 83:59:59 and 111:59:59 gameplay-cycle time, cross the next second while standing outdoors, in a menu, in battle and indoors. Confirm the next safe field update changes season without broken fades or weather sprites.
- Compare Mt. Chimney, Jagged Pass, Routes 111/112/113, Lavaridge and Fallarbor across seasons; check ash collection, desert coordinate weather and hot springs.
- Check winter snow and autumn fog transitions, route connections, Surf, battle return, save/continue and indoor exits; NPC/player/UI palettes must keep their original colors.
- Check Groudon/Kyogre conflict and postgame Terra/Marine Cave drought/downpour; these must override seasonal ambient weather.
