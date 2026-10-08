# Pokémon Emerald: Legends - Release Changelog

This is the player-facing history for the recommended **Release** build. Shared Legends changes are repeated here so this file stands on its own; Release-only behavior is called out separately.

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
