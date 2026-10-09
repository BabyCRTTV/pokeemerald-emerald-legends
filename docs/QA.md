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
- [ ] Open Options; switch General/Legends/Adventure using NEXT PAGE + A and L/R with normal controls and L=A mode; confirm the A: NEXT / B: SAVE hint, modify settings across pages, B save/reload, and inspect borders.
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

## Seasons (0.0.12)

Automated: `python3 test/legends-seasons.test.py` compiles the actual season module with engine mocks and verifies all twelve calendar months, seven-hour boundaries, full-cycle rollover, persisted sub-second progress, older-save migration and 0.0.11 cycle normalization, 999-hour continuation, invalid RTC fallback, regional exclusions, unchanged special weather, deterministic snow frequency, ocean snow exclusion, RGB555 bounds, protected palette slots, deferred active-season/weather snapshots and manual selection. `python3 test/legends-options-text.test.py` exercises the actual native choice renderer against plain text and encoded color prefixes. Native builds and BPS reapplication are checked by the release workflow.

Manual emulator checks (not yet verified; not replaced by host tests):

- With RTC enabled, visit Littleroot, Route 104, Fortree, Route 119 and Lilycove in March, July, October and January; inspect foliage, contrast, water and buildings during day and night.
- Switch REAL TIME / 7H PLAY in Legends Options. Verify readable labels, no leftover characters when replacing a longer label, and intact window borders. CURRENT should show the active environment; SET SEASON should display CALENDAR and ignore Left/Right in real time.
- In gameplay mode, cycle SET SEASON through all four seasons, leave Options, enter/exit a building, and confirm the selected environment. Save/reload and confirm the setting and restarted seven-hour timer persist.
- At 6:59:59, 13:59:59, 20:59:59 and 27:59:59 gameplay-cycle time, cross the next second outdoors, in a menu, in battle and indoors. Confirm the old environment remains until a faded warp or save reload. Check seamless route crossing and native day/night updates do not apply the pending season early.
- Compare Mt. Chimney, Jagged Pass, Routes 111/112/113, Lavaridge and Fallarbor across seasons; check ash collection, desert coordinate weather and hot springs.
- Check winter snow and autumn fog transitions, Surf, battle return, save/continue and indoor exits; NPC/player/UI palettes must keep their original colors.
- Check Groudon/Kyogre conflict and postgame Terra/Marine Cave drought/downpour; these must override seasonal ambient weather.

## New Game Options (0.0.12.1)

Automated: `python3 test/legends-new-game-options.test.py` compiles the actual Legends settings and seasons modules and verifies staged title choices through save resets, active-season initialization with the bedroom clock unset, replacement of staged choices, one-shot consumption, fresh-title clearing and standard defaults. Source integration checks require restoration after native resets and before the opening warp.

Manual emulator checks (not yet verified):

- With no save, select 7H PLAY and Winter, EXP SHARE OFF and 1/1226 in title Options. Start New Game; confirm the first Littleroot exterior has winter colors, the Options choices persist, and playtime begins at zero.
- Before setting the bedroom clock, change gameplay season in Options; enter/exit a building and confirm the chosen environment. Finish the clock event and confirm it does not change the season mode or selection.
- Repeat with Spring, Summer and Autumn; check RTC mode remains calendar-controlled and disabled SET SEASON still shows CALENDAR.
- With an existing save, edit title Options then choose New Game; confirm chosen settings carry over while story/Pokédex progress does not. Choose Continue instead and confirm normal saved-game behavior.
- Soft reset or return to a fresh title entry after staging, then start New Game without visiting Options; confirm standard defaults. Reopen title Options twice and confirm the latest selections take precedence.

## Followers (0.0.13)

Automated: `python3 test/legends-followers.test.py` compiles the actual native party selection, follower-info and spawn/update functions against engine mocks using the Legends follower configuration. It covers empty/all-fainted parties, skipped eggs, party changes, OFF/ON removal/re-enable, temporary script hiding, NPC companions, oversized indoor sprites, missing graphics and full object-event slots. New-game setting regressions cover default ON, persistent OFF through continue initialization and title-screen OFF through save reset.

Manual emulator checks (not yet verified):

- Start new Release/Debug games and continue an older save; FOLLOWER defaults ON, no follower appears before receiving a starter, and the starter emerges and follows afterward.
- Toggle FOLLOWER OFF and ON outdoors; confirm the faded Options return removes/restores it. Save/reload OFF and confirm it remains OFF. Select OFF in title Options and start New Game; confirm it carries over.
- Reorder party Pokémon, faint the lead, place eggs ahead of a conscious Pokémon, heal, deposit/withdraw/evolve/trade Pokémon and return from battles. Confirm the native eligible follower and sprite are refreshed.
- Walk/run, cross route edges, enter/exit buildings, use stairs/doors/elevators/escalators, jump ledges and traverse bridges. Inspect collision, ordering, shadows and sprite palettes on mGBA and Pizza Boy.
- Test both bicycles, Surf, Dive, Fly, Waterfall, currents and each badge-earned HM utility; followers must not block travel or alter progression checks.
- Test opening scenes, Wally’s tutorial, rival/team/legendary cutscenes, Groudon/Kyogre weather and scripted NPC companions. Confirm native temporary hiding/restoration and no cutscene softlocks.
- Talk to the follower; inspect native dialogue/emotes, shiny/female forms, large Pokémon indoors and the Substitute fallback where sprites are missing. Repeat under all seasons/day-night lighting.
- Visit crowded maps and Battle Frontier/Pyramid/Safari/secret-base areas; verify object-event capacity and return-from-menu behavior without duplicate followers.

## Player appearance (v0.0.15)

Follow the [player appearance emulator checklist](features/player-appearance.md#emulator-qa) for intro navigation, saved appearance, every movement pose and local battle scenes. Automated appearance and asset tests run in Legends project checks.

## v0.0.16 polish

- Check naming-screen icons for all four outfits and five skin tones, both genders.
- Inspect all battle throw frames: cohesive garment panels, unaltered Poké Balls, bare hands on custom outfits and no blue mouth pixel on May.
- Browse appearance while dialogue prints at slow/normal speed; check glyphs, shadows and arrows.
- Test grass rustle and jumps in every season with a follower and simultaneous water ripple/reflection. Check excluded ash routes remain native.
- In winter, cross standard grass; confirm tufts clear, encounters still occur, scrolling keeps scuffs, and a full map reload restores them. Test tree-edge/long grass remains intact.

- [ ] Test Lavender with all five skin tones, both genders and the four battle back poses; inspect the scarf, hands and naming icon.
- [ ] Test each of the 11 STARTERS modes before the rescue bag, verify all three balls, and confirm the rival counter or Zorua. Inspect Zoroark at Route 119 and Lilycove.
- [ ] Verify Random has no duplicate/evolved choices, stays stable while declining confirmation, and persists after save/reload. Change the preference after rescue and verify the existing rival stays fixed.

## Kanto arrival (v0.0.26.1)

Automated script/warp/heal-point checks: `python3 test/legends-kanto.test.py`. Follow the [Kanto feature checklist](features/kanto.md#emulator-checklist) and [Debug tutorial](kanto-guide.html). Emulator checklist items are pending unless explicitly recorded as verified.
