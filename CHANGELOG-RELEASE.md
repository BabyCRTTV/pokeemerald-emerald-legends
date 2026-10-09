# Pokémon Emerald: Legends - Release Changelog

This is the player-facing history for the recommended **Release** build. Shared Legends changes are repeated here so this file stands on its own; Release-only behavior is called out separately.

## [0.0.24] - 2026-10-08

### Updated
- Integrated the two upstream expansion updates through commit 7b95be15: held-item restoration after wild battles/captures, and missing/corrected overworld sprites and palettes for Pokémon forms. Retained Legends gameplay, follower controls, custom species, appearance and weather systems.
- Replaced the tall custom wardrobe with Emerald’s native closed storage-box artwork beneath each bedroom’s bed. The secret-base WARDROBE now occupies one tile; its existing decoration ID and purchase/inventory state are retained.
- Interacting with your wardrobe now opens customization directly. Removed the repeated shop advertisement and Yes/No prompt.
- Compiled pose-local scarf tails and jacket outlines/hem layers for both genders, including overworld states, battle portraits/throws and Trainer Cards. Faces, hands, held objects and native frame sizes are preserved.

### Compatibility and validation
- No save-layout or accessory encoding changes. Added focused tests of upstream held-item restoration, captured items, bag routing, berries and partner slots; retained all Legends regressions and layered-asset validation.
- Release and Debug share all changes with no variant-specific differences; native developer tools remain Debug-only.

## [0.0.23] - 2026-10-08

### Added
- A wooden wardrobe in each Littleroot bedroom, usable only in the player’s own home. Browse all five outfits, five additional scarf colors (Crimson, Ocean, Emerald, Lavender, Cream) or no added scarf, and an optional navy jacket with short sleeves.
- A dedicated native wardrobe screen with a live trainer portrait, Apply and Cancel. Scarf and jacket selections combine independently with every outfit; skin tone is retained.
- A placeable 1x2 WARDROBE ornament sold for ₽3,000 at Route 104’s Pretty Petal Flower Shop. Uses the native decoration inventory, placement/removal and save system; customization is available only in your own secret base.
- Matching accessory art for both genders across walking/running, bikes, Surf, field moves, fishing/watering, battle front/back throw frames and the local Trainer Card. The diving suit remains covered; rivals/NPCs and remote link art remain native.

### Compatibility and validation
- Accessory choices use unused var 0x40A1 without changing save layouts. Legacy saves retain native skin colors when editing clothes; new games start with no added accessories.
- Added pose-aligned native 4bpp asset generation, separate scarf coloring, safe cabinet tile reuse, actual UI access/navigation/apply/cancel tests, and all-combination appearance/asset regressions.
- Documented wardrobe controls, shopping/placement, save migration and emulator QA. Release and Debug share these changes with no variant-specific differences; developer tools remain disabled in Release and enabled in Debug.

## [0.0.22] - 2026-10-08

### Added
- Regional dynamic forecasts in most ordinary Hoenn towns and routes: rain, clouds and occasional thunderstorms; wetter conditions around Fortree and Routes 119–121.
- Fog in rainforest/upland areas, more likely in autumn and during native morning/night hours; winter flurries on non-volcanic upland Routes 114–116. Tropical coasts and lowlands never receive random snow.
- A saved 20-minute playtime forecast period, with smooth native transitions while outdoors. Local seeded randomness avoids consuming battle RNG or rerolling every time a building is entered.
- A moon and subtle star twinkle for clear nights in the pause weather indicator, using the existing game day/night clock. Drought retains its sun indicator.

### Compatibility and validation
- Preserved indoor, cave, underwater, desert, volcanic, special-map and scripted story weather; weather transitions wait for dialogue, fades and existing effects to finish.
- Existing saves initialize the weather timer from recorded playtime. One unused var and flag are reserved without changing save layouts.
- Documented climates, forecast weights and emulator QA; added actual-module checks for probabilities, exclusions, timer migration/rollover and transition guards.
- Release and Debug share all weather changes with no variant-specific differences; developer tools remain disabled in Release and enabled in Debug.

## [0.0.21] - 2026-10-08

### Changed
- Halved Da Bug’s follower art inside its existing 32x32 frames, keeping it centered and grounded; visible silhouettes now fit within 14x14 pixels.
- Reduced its shared PC/party icon to roughly 20x16 pixels, comparable to native small Pokémon icons, with padding around every frame.
- Reduced the front sprite used by the large PC/Pokédex preview from 60x48 to 48x40 pixels; preserved the normal/shiny colors and eye-only glimmer frames.
- Lowered Da Bug’s battle back sprite by 8 pixels using its native species Y offset.
- Updated sprite bounds checks and art documentation. The existing PC gift, save compatibility, moves, cry and shiny roll are unchanged.
- Release and Debug share these adjustments with no variant-specific differences; developer tools remain disabled in Release and enabled in Debug.

## [0.0.20] - 2026-10-08

### Added
- Added Da Bug, the original single-stage Bug/Grass Leafhopper Pokémon: 0.3 m, 1.2 kg, with the approved green leaf-wing design, red eyes and amber-wing/teal-eye shiny.
- Native front/back battle art, PC icon, footprint and walking follower sprites; a gentle swaying front animation with localized red eye glimmers and a short, original two-note chirp.
- One level-5 Da Bug is placed in Box 1 on New Game, with Tackle, Leer, Mean Look and Absorb. Existing saves receive it in their first free PC box slot on continue. Full storage retries on a later continue without overwriting Pokémon.
- This gift alone has exactly a 1-in-10 shiny roll, independent of Options/Charm. A permanent receipt flag prevents replacement or rerolls after withdrawal, release or later continues. No wild encounters or Random starter inclusion.
- A relevant level-up progression introduces Bug Bite, Leech Seed, Mega Drain, Struggle Bug, Protect, Giga Drain, Agility, Leech Life, Synthesis, Energy Ball and Bug Buzz. No evolution.
- Preserved the approved Pokédex entry verbatim: “It sways in the breeze to mimic a fallen leaf. If its disguise fails, it flashes its red eyes and springs away.”

### Compatibility and validation
- Added custom species/National Dex entries without renumbering existing Pokémon. Dex save bitfields remain 129 bytes; the gift uses an unused permanent flag rather than enlarging save blocks.
- Added actual-module regressions for every shiny outcome, both ordinary shiny states, level/moves, duplicate prevention, occupied/full storage, retry and Pokédex registration; asset/cry/dex integration checks.
- Documented species data, learnset, gift migration and emulator QA in docs/features/da-bug.md.
- Release and Debug share the gameplay changes. Debug’s sprite visualizer adds a labeled Da Bug sway/eye-glimmer animation; developer tools remain disabled in Release.
- Both variants compiled successfully; both BPS patches passed byte-for-byte reapplication verification against the independently built, SHA-1-verified clean Emerald reference.

## [0.0.19] - 2026-10-08

### Added
- Added Lavender for both genders: a lavender/plum outfit with cream scarf details, bare hands, matching overworld poses, intro/naming previews, battle front/back art and Trainer Card.
- Added Adventure 3/3 Options with STARTERS: Gen 1–9, Special (Happiny/Wattrel/Mankey), and Random. Gen 3 remains the default; title Options carry into New Game.
- Random selects three distinct, enabled, unevolved canonical Pokédex species with evolutions, including babies. The lineup rolls once at the rescue bag and remains saved/stable.
- Generation rivals use their corresponding counter starter and native level evolutions. Special/Random rivals use Unovan Zorua, evolving to Zoroark at level 30. Both genders and all 30 native starter-dependent teams are covered.

### Compatibility and validation
- Lock the rescue lineup separately from future-game preferences. Existing saves retain Gen 3 rival lineage; default Gen 3 preserves exact Emerald teams. No save-block or Options-window enlargement.
- Keep starter levels, Stunky rescue, other rival team members and progression scripts. The Petalburg type tutorial now uses general examples rather than calling a Hoenn species your own starter.
- Added actual-module starter/rival tests using native evolution metadata; checked stable Random selection and all 30 teams in 11 modes. Extended title staging and three-page navigation tests.
- Appearance checks cover all 50 gender/skin/outfit combinations and 736 custom poses.
- Release and Debug share these changes with no variant-specific differences. Developer tools remain disabled in Release and enabled in Debug.

## [0.0.18] - 2026-10-08

### Changed
- Replaced the bottom CANCEL row on both Options pages with NEXT PAGE. Press A there to cycle pages; L/R remain page shortcuts.
- Added a permanent A: NEXT / B: SAVE hint on the bottom row, independent of the version label. B saves all settings and exits from any row.
- Kept the original seven-row windows and VRAM allocation. Page changes preserve pending settings, and L/R retains priority with L=A controls.
- Release and Debug share these changes with no variant-specific differences. Developer tools remain disabled in Release and enabled in Debug.

### Validation
- Added an actual-function navigation regression covering A/L/R paging, pending settings, row wrap and B save/exit on every row in both pages.

## [0.0.17] - 2026-10-08

### Changed
- Stunky replaces Zigzagoon in the opening Route 101 professor rescue, both in the level-2 battle and as the Pokémon chasing the professor. Uses the expansion’s native Stunky overworld sprites and palette.
- The rescue movement, starter choices and story progression are unchanged; existing saves remain compatible.
- Release and Debug share this change with no variant-specific differences. Developer tools remain disabled in Release and enabled in Debug.

## [0.0.16] - 2026-10-08

### Fixed
- The player naming-screen icon now uses the selected outfit and skin tone.
- Clear the entire intro text window so longer appearance prompts leave no stray letters/arrows. Active text printers restore their own glyph colors after menu text.
- Grass rustle/jump/short/long/shaking animations use a separate seasonal vegetation palette; water, ash, NPCs and player palettes retain their own colors.
- Refined custom front/back outfit panels across all four battle animation poses, kept bags distinct from shirts, protected held Poké Balls and corrected May’s colored mouth detail.

### Added
- Added a fourth, yellow outfit for both genders. All custom outfits use bare hands; the default Emerald outfit retains its original gloves.
- Walking through standard winter grass clears the snow-covered tuft until a full map reload, inspired by ash grass. This is a temporary visual change: encounters, collision and terrain behavior are preserved. Tree-edge, long-grass and volcanic-ash tiles retain native terrain rendering.

### Validation
- Expanded actual-module appearance checks to all 40 combinations and asset coverage to all 552 custom poses.
- Added regressions for printer color isolation, seasonal grass palettes and snow clearing/reset/bounds.
- Release and Debug share these changes; developer tools remain disabled in Release and enabled in Debug.

## [0.0.15] - 2026-10-08

### Added
- Added skin tone and outfit selection immediately after gender in Birch’s New Game introduction.
- Five realistic skin tones (Fair, Light, Medium, Brown, Deep) and three clothing designs per gender: Emerald, Trail (jacket/trousers), Sport (striped shirt/shorts).
- Added a live 64px sprite preview in a bordered popup at the bottom right, above the dialogue box. B returns to the previous choice.
- Saved appearance applies to walking/running, bikes, Surf, field moves, fishing/watering, local battle front/back poses, Safari scenes and the local Trainer Card; Dive retains the native diving-suit silhouette.
- Existing saves and Debug Quickstart keep the original Emerald appearance. Player colors and graphics use separate IDs/palettes so NPCs and rivals retain their native appearance.
- Documented appearance data, native pose reuse, asset authoring and emulator QA. Remote/link appearance synchronization is not added.

### Validation
- Added exhaustive actual-module host regressions for all 30 gender/skin/outfit combinations, intro-to-save handoff, legacy saves, graphics states and NPC isolation.
- Added generated-art reproducibility, face/held-ball protection, silhouette and LZ77 roundtrip checks across all 368 custom outfit poses.
- No Release-only gameplay differences; developer tools remain disabled.

## [0.0.14.1] - 2026-10-08

### Changed
- Colored the pause-panel weather icons using Emerald’s existing text palette: warm sunshine/sand, blue rain/water and pale blue snow.
- Added gentle two-frame weather animation twice per second: sun shimmer, falling rain/ash, drifting snow/fog/sand, a softly dimming lightning bolt and water shimmer. Indoor and cloud icons stay still.
- Redrew the clock hands as a clear L shape, removing the previous U-like appearance.
- Animation updates only the weather icon pixels, reads no RTC data and uses no additional sprite or palette slots. Menu closure retains the existing cleanup.

### Validation
- Extended the actual-module host C regressions for both animation frames, native colors, pixel bounds and RTC read limits.
- No Release-only visual/gameplay differences; developer tools remain disabled.

## [0.0.14] - 2026-10-08

### Added
- Added a bottom-left Start-menu panel using Emerald’s native border, small text and pixel clock/weather icons.
- Shows the local RTC clock in 12-hour format, live weather and the active season. Refreshes once per second and redraws only when values change; unavailable RTC displays --:--.
- Indoors/caves show a shelter icon; underwater shows a water icon. Opening the menu does not advance the active season or change weather.
- Handles save/retire dialogs, submenu transitions, returning to the menu and allocation failure without leaking a window.

### Validation
- Added host C regressions for panel lifecycle, time rollover, invalid RTC, weather categories, season display and tile/pixel bounds. Both native ROM builds and BPS round-trip verification run in Actions; emulator visual QA remains separate.
- No Release-only gameplay differences; developer tools remain disabled.

## [0.0.13.1] - 2026-10-08

### Shared changes
- Changed the New Game / Continue / Options main menu backdrop to a soft light lavender, preserving the existing menu cards, text, borders and fades.

### Release-specific
- No Release-only visual/gameplay divergence; developer tools remain disabled.

## [0.0.13] - 2026-10-08

### Shared changes
- Enabled the expansion’s native overworld Pokémon follower system with a saved FOLLOWER ON/OFF setting on Legends Options (default ON for new and existing saves).
- The first conscious non-egg Pokémon in party order follows the player, using native walking, Poké Ball, graphics and interaction behavior. Reorder the party to change the follower.
- Reused native hiding rules for travel/forced movement, oversized indoor sprites, temporary script hiding and NPC companions; missing overworld graphics keep the configured native substitute fallback.
- Leaving Options applies the follower choice through the normal faded field reload. The selection persists across save/reload and title-screen New Game setup.
- Used an unused permanent disable flag without changing the SaveBlock layout; kept both Options pages within seven rows and the existing VRAM allocation.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.12.1] - 2026-10-08

### Shared changes
- Preserved title-screen Legends Options choices when starting New Game: season mode, selected gameplay season, EXP Share and shiny rate now survive the new save reset.
- Initialized the active season before the opening maps load; 7H PLAY and manual season selection work independently of the bedroom clock event.
- New saves start with a fresh seven-hour timer for the selected gameplay season; previous save progress and story flags are not carried over.
- Cleared temporary title choices after applying them and on fresh title entry, preserving standard defaults when New Game is started without title-screen Options.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.12] - 2026-10-08

### Shared changes
- Changed gameplay seasons to seven recorded play hours each (28 hours for a full Spring → Summer → Autumn → Winter cycle).
- Held seasonal colors and ambient weather until a faded map transition, such as entering/leaving a building, a faded warp, or save reload; seamless route crossings and menu/battle returns preserve the active environment.
- Added SET SEASON in gameplay mode. Left/Right selects the next season to apply and restarts its seven-hour timer; REAL TIME remains calendar-controlled.
- CURRENT now shows the active environment, including while a new season is pending.
- Fixed corrupted season labels by providing native color prefixes, checking those prefixes before recoloring, and clearing old choice text before redraw.
- Preserved seasonal progression in existing saves without changing the SaveBlock layout; volcanic exclusions and special weather remain intact.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.11] - 2026-10-08

### Shared changes
- Added REAL TIME / 28H PLAY seasonal modes to Legends Options, plus a CURRENT season preview.
- Real time follows Northern Hemisphere calendar seasons using the native RTC; the gameplay mode cycles Spring, Summer, Autumn and Winter every 28 saved gameplay hours.
- Added seasonal outdoor vegetation colors and region-aware ambient rain, fog, thunderstorms and winter snowfall using native weather effects.
- Preserved Mt. Chimney, Jagged Pass, Fiery Path, Lavaridge, Fallarbor, Routes 112/113, and Route 111's desert corridor; oceans and mild island towns do not receive seasonal snowfall.
- Preserved indoor/underground/underwater maps, special weather, and Groudon/Kyogre story effects.
- Reused unused permanent save variables, migrated older saves from recorded playtime, and kept seasonal time running beyond the native 999-hour playtime display limit.
- Refreshed seasons safely on return to the field and during outdoor play, composing foliage palettes with existing day/night and weather processing.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.10] - 2026-10-07

### Shared changes
- Added a persistent SHINY RATE setting to the Legends Options page (Left/Right: 1/8192, 1/5680, 1/1226; default 1/8192).
- Selected odds govern the base per-roll shiny chance for newly generated wild Pokémon, including fishing and DexNav encounters.
- Kept bonus rolls from Shiny Charm, chain fishing and DexNav; eggs, gifts, special/scripted Pokémon and previously caught Pokémon are unchanged.
- Used an existing unused permanent event variable, so earlier saves retain 1/8192 and a new choice survives save/load.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.9] - 2026-10-07

### Shared changes
- Enabled DexNav at Birch's first Pokédex gift and on existing saves that already have the Pokédex.
- Added the physical Gen 6-style Exp. Share Key Item at new-game start and restored it for eligible existing saves.
- The Exp. Share item and Legends Options share the same persistent ON/OFF flag.
- Rustboro's Lucky Egg and the Champion Rare Candy reward are unchanged.

### Release-specific
- No Release-only gameplay divergence; developer tools are disabled.

## [0.0.8.1] - 2026-10-07

### Shared changes
- Fixed browser patcher handling of rapid ROM changes, discarding obsolete validation and download results.
- Ensured version text cannot overlap the Options header's L/R hint.
- Added automated BPS parser/checksum tests and a manual emulator regression checklist.
- Core Legends gameplay and content remain unchanged from 0.0.8.

### Release-specific
- No Release-only gameplay divergence; developer tools remain disabled.

## [0.0.8] - 2026-10-07

### Shared changes
- Reworked Options into two pages: General and Legends.
- Use L/R in Options to switch pages; the current page is shown in the header.
- Moved EXP SHARE to the Legends page to reserve clean space for future Legends-specific settings.
- Restored the original safe Options window dimensions, fixing corrupted/repeating frame graphics and the clipped CANCEL row.

### Release-specific
- No Release-only gameplay divergence in this version.

## [0.0.7] - 2026-10-07

### Shared changes
- Professor Birch now enables the National Pokédex during the initial Pokédex handoff.
- Birch's post-Elite Four National Dex upgrade reward is now 25 Rare Candies.
- If the Bag cannot hold all 25, the reward is sent to the PC; if neither has room, Birch keeps the reward pending for a later conversation.
- Existing postgame saves can claim the new Rare Candy reward once without disrupting later Johto starter progression.

### Release-specific
- No Release-only gameplay divergence in this version.

## [0.0.6] - 2026-10-07

### Shared changes
- Mr. Stone now gives a Lucky Egg after the Steven Letter delivery instead of the redundant held Exp. Share.
- His reward dialogue now explains the Lucky Egg's EXP bonus.
- Lucky Egg's native multiplier behavior is unchanged; only the Rustboro reward source changed.

### Release-specific
- No Release-only gameplay divergence in this version.

## [0.0.5] - 2026-10-07

### Shared changes
- Added default-on Gen 6-style party EXP Share from the beginning of the game.
- Added an `EXP SHARE` ON/OFF setting to Options.
- Added one-time migration for pre-0.0.5 saves so the new setting starts enabled.
- Reused the expansion-native EXP pipeline so existing multipliers and level-cap behavior remain intact.

### Release-specific
- No Release-only gameplay divergence in this version.
- Release includes the full EXP Share setting with developer/debug entry points disabled.

## [0.0.4.2] - 2026-10-07

### Shared changes
- Corrected homepage wording so the field-move feature is accurately attributed to 0.0.4.
- Added a direct Release changelog link beside the Release download.
- Tightened changelog/version consistency checks.

### Release-specific
- No Release-only gameplay or content changes in this micro-build.

## [0.0.4.1] - 2026-10-07

### Shared changes
- Corrected mislabeled 0.0.3 headings on the website changelog.
- Synchronized current version labels and download targets to 0.0.4.1.

### Release-specific
- No Release-only gameplay or content changes in this micro-build.

## [0.0.4] - 2026-10-07

### Shared changes
- Cut, Flash, Rock Smash, Strength, Surf, Fly, Dive, and Waterfall are now badge-earned overworld utilities and no longer require a Pokémon to know the HM.
- Added a compact `FIELD` submenu for manually invoking unlocked utilities.
- Preserved Emerald's original badge order, map restrictions, follower restrictions, and Regi puzzle hooks.
- Removed Pokémon-specific HM-use text and suppressed arbitrary Pokémon field-move banners.
- Kept non-HM field moves such as Dig, Teleport, and Sweet Scent move-dependent.

### Release-specific
- No Release-only gameplay divergence in this version.
- Release contains the full badge-field-move system with developer/debug entry points still disabled.

## [0.0.3] - 2026-10-07

### Shared changes
- Added dedicated Release and Debug changelog tracking.
- Added a website changelog page with tabs for switching between build histories.
- Improved version/changelog consistency checks.

### Release-specific
- No Release-only gameplay or content changes in this version.
- Release remains the recommended casual-player build with developer/debug entry points disabled.

## [0.0.2] - 2026-10-07

### Shared changes
- Introduced separate Release and Debug downloads built from the same Legends source.
- Added browser patcher support for both build variants.
- Added automated byte-for-byte verification for both published patches.

### Release-specific
- Release is built using the expansion's native release configuration.
- Overworld debug menu, battle debug menu, Pokémon sprite visualizer, and title-screen Quickstart are disabled.
- All Pokémon Emerald: Legends gameplay/content changes remain present.

## [0.0.1] - 2026-10-07

### Pre-split baseline
- Added the `LEGENDS` title-screen subtitle.
- Added the initial in-game Legends version label.
- Added the project website, browser patcher, reproducible patch workflow, roadmap, and initial feature design documentation.
- Formal Release/Debug variants had not yet been separated.
