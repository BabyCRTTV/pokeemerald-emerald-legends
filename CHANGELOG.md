# Changelog

All notable Pokémon Emerald: Legends project changes are documented here.

For build-specific player views, see [CHANGELOG-RELEASE.md](CHANGELOG-RELEASE.md) and [CHANGELOG-DEBUG.md](CHANGELOG-DEBUG.md). The canonical history below records the project as a whole.

## [0.0.13] - 2026-10-08

### Added
- Enabled the expansion’s native overworld Pokémon follower system with a saved FOLLOWER ON/OFF setting on Legends Options (default ON for new and existing saves).
- The first conscious non-egg Pokémon in party order follows the player, using native walking, Poké Ball, graphics and interaction behavior. Reorder the party to change the follower.
- Reused native hiding rules for travel/forced movement, oversized indoor sprites, temporary script hiding and NPC companions; missing overworld graphics keep the configured native substitute fallback.
- Leaving Options applies the follower choice through the normal faded field reload. The selection persists across save/reload and title-screen New Game setup.
- Used an unused permanent disable flag without changing the SaveBlock layout; kept both Options pages within seven rows and the existing VRAM allocation.

### Validation
- Added host C regressions for native party selection, follower spawn/removal, script/NPC hiding, indoor limits and full object slots. Extended saved-setting and title-screen New Game regressions for the follower toggle. Emulator visual/playtesting remains separate.
- Updated the roadmap’s gameplay-season timing to the current seven-hour cycle.
- No variant-specific gameplay changes; Release disables developer tools and Debug retains them.

## [0.0.12.1] - 2026-10-08

### Fixed
- Preserved title-screen Legends Options choices when starting New Game: season mode, selected gameplay season, EXP Share and shiny rate now survive the new save reset.
- Initialized the active season before the opening maps load; 7H PLAY and manual season selection work independently of the bedroom clock event.
- New saves start with a fresh seven-hour timer for the selected gameplay season; previous save progress and story flags are not carried over.
- Cleared temporary title choices after applying them and on fresh title entry, preserving standard defaults when New Game is started without title-screen Options.

### Validation
- Added host C regressions for title choices across save reset, pre-clock season initialization, replacement/consumption of staged choices, default new saves and native lifecycle hook ordering. Emulator visual/playtesting remains separate.
- No variant-specific gameplay changes; Release disables developer tools and Debug retains them.

## [0.0.12] - 2026-10-08

### Changed
- Changed gameplay seasons to seven recorded play hours each (28 hours for a full Spring → Summer → Autumn → Winter cycle).
- Held seasonal colors and ambient weather until a faded map transition, such as entering/leaving a building, a faded warp, or save reload; seamless route crossings and menu/battle returns preserve the active environment.
- Added SET SEASON in gameplay mode. Left/Right selects the next season to apply and restarts its seven-hour timer; REAL TIME remains calendar-controlled.
- CURRENT now shows the active environment, including while a new season is pending.
- Fixed corrupted season labels by providing native color prefixes, checking those prefixes before recoloring, and clearing old choice text before redraw.
- Preserved seasonal progression in existing saves without changing the SaveBlock layout; volcanic exclusions and special weather remain intact.

### Validation
- Added host regressions for seven-hour boundaries, deferred transitions, old-cycle normalization, manual season selection and native Options text rendering. Emulator visual/playtesting remains separate.
- No variant-specific gameplay changes; Release disables developer tools and Debug retains them.

## [0.0.11] - 2026-10-08

### Added
- Added REAL TIME / 28H PLAY seasonal modes to Legends Options, plus a CURRENT season preview.
- Real time follows Northern Hemisphere calendar seasons using the native RTC; the gameplay mode cycles Spring, Summer, Autumn and Winter every 28 saved gameplay hours.
- Added seasonal outdoor vegetation colors and region-aware ambient rain, fog, thunderstorms and winter snowfall using native weather effects.
- Preserved Mt. Chimney, Jagged Pass, Fiery Path, Lavaridge, Fallarbor, Routes 112/113, and Route 111's desert corridor; oceans and mild island towns do not receive seasonal snowfall.
- Preserved indoor/underground/underwater maps, special weather, and Groudon/Kyogre story effects.
- Reused unused permanent save variables, migrated older saves from recorded playtime, and kept seasonal time running beyond the native 999-hour playtime display limit.
- Refreshed seasons safely on return to the field and during outdoor play, composing foliage palettes with existing day/night and weather processing.

### Technical
- Added host C regression coverage for calendar/timing boundaries, save migration, weather exclusions, palette bounds and safe refresh; emulator visual/play testing remains separate.

## [0.0.10] - 2026-10-07

### Added
- Added a persistent SHINY RATE setting to the Legends Options page (Left/Right: 1/8192, 1/5680, 1/1226; default 1/8192).
- Selected odds govern the base per-roll shiny chance for newly generated wild Pokémon, including fishing and DexNav encounters.
- Kept bonus rolls from Shiny Charm, chain fishing and DexNav; eggs, gifts, special/scripted Pokémon and previously caught Pokémon are unchanged.
- Used an existing unused permanent event variable, so earlier saves retain 1/8192 and a new choice survives save/load.

### Technical
- Used unbiased 16-bit rejection sampling so the three selected base probabilities are mathematically exact before modifier rerolls.
- Reused the existing paged Options UI without increasing window tile usage or the seven-row General page.
- Added static project checks for the new save variable and wild-only shiny calculation; emulator playtesting remains separate.

## [0.0.9] - 2026-10-07

### Added
- Enabled expansion DexNav using dedicated persistent search flags and variables. It appears in the Start menu after Birch's first Pokédex gift, including detector mode.
- Existing saves that already received the Pokédex automatically unlock DexNav when continued.
- Added the Gen 6-style physical Exp. Share to Key Items in new games; existing saves receive one if missing.

### Fixed
- Using the Exp. Share Key Item and changing Legends Options now affect the same persistent ON/OFF flag.
- Existing-save item restoration avoids the temporary Battle Pyramid bag; if the Key Items pocket is full it retries on a future ordinary continue.

### Quality
- Expanded repository checks to verify DexNav configuration and Exp. Share item/unlock migration.
- Release and Debug retain identical gameplay changes and separate changelogs.

## [0.0.8.1] - 2026-10-07

### Fixed
- Browser patcher now ignores stale checksum results when the selected ROM changes during verification.
- Cancels in-flight local patching when the selected ROM changes, avoiding accidental output from an older selection.
- Prevents longer version text from overlapping the Options page-navigation hint.

### Quality and maintenance
- Reviewed the Options, EXP Share settings, HM field utilities, Birch Champion reward, and Rustboro Lucky Egg paths at source level.
- Added automated BPS decoder tests for copy behavior, integrity checks, and rapid ROM selection changes.
- Documented verified automated coverage and remaining manual emulator scenarios in docs/QA.md.
- No gameplay or content changes from v0.0.8; Release and Debug retain identical Legends mechanics.

## [0.0.8] - 2026-10-07

### Added
- Added a reusable paged Options framework with separate **General** and **Legends** pages.
- Added L/R shoulder-button page switching with the active page shown in the Options header.
- Moved the Legends EXP Share toggle onto the Legends page, leaving room for additional project-specific settings later.

### Fixed
- Restored the Options menu's safe upstream window dimensions so its text tile buffer ends before the window-frame graphics begin.
- Fixed the corrupted/repeating Options window borders seen in mGBA and Pizza Boy after the 0.0.5 single-page layout expansion.
- Restored full visibility of the CANCEL row instead of allowing it to clip below the Options window.

### Changed
- The General page now contains Text Speed, Battle Scene, Battle Style, Sound, Button Mode, Frame, and Cancel.
- Each page uses the original 16-pixel row spacing; new Legends settings can be added by extending the page table rather than enlarging the window.

## [0.0.7] - 2026-10-07

### Added
- Professor Birch's initial Pokédex handoff now enables National Mode immediately.
- Birch now gives 25 Rare Candies after the player becomes Champion, replacing the old post-Elite Four National Dex upgrade reward.

### Changed
- The Champion reward first tries the Bag and falls back to the PC if the Bag cannot hold all 25 Rare Candies.
- Added a one-time reward flag so existing postgame saves that already passed the old National Dex scene can still claim the 25 Rare Candies from Birch.
- Preserved the existing postgame state progression, including the later Hoenn Pokédex completion / Johto starter reward.

## [0.0.6] - 2026-10-07

### Changed
- Replaced Mr. Stone's post-Steven-Letter Rustboro reward from the now-redundant held Exp. Share to a Lucky Egg.
- Updated Mr. Stone's reward explanation to describe the Lucky Egg's held-item EXP bonus.
- Preserved the expansion-native Lucky Egg multiplier behavior; this release changes acquisition, not the multiplier formula.
- Retained Emerald's existing `FLAG_RECEIVED_EXP_SHARE` as the one-time Devon reward completion state for save compatibility.

## [0.0.5] - 2026-10-07

### Added
- Added Gen 6-style party-wide EXP Share from the start of the game.
- Added an `EXP SHARE` ON/OFF setting to the normal Options menu.
- Added a one-time settings migration so saves created before 0.0.5 start with the new EXP Share enabled.

### Changed
- When EXP Share is ON, battle participants receive full EXP while eligible non-participating party Pokémon receive the Gen 6-style half share.
- The system reuses pokeemerald-expansion's native EXP pipeline, preserving existing Lucky Egg, traded-Pokémon, scaled EXP, catch EXP, and level-cap handling.
- The Options menu layout was tightened vertically by one tile row so the additional setting fits without reducing normal row spacing.
- Lucky Egg behavior remains unchanged and is tracked separately from EXP Share tuning.

## [0.0.4.2] - 2026-10-07

### Fixed
- Corrected homepage release wording so badge-earned HM field utilities are accurately credited to 0.0.4 rather than the 0.0.4.1 maintenance build.

### Changed
- Added direct Release and Debug changelog links beside their corresponding download options.
- Strengthened changelog consistency checks so the current version must be the newest entry in the canonical, Release, and Debug histories and must appear in both website changelog tabs.
- Published this changelog/site housekeeping as micro-build 0.0.4.2 with no gameplay or content divergence between Release and Debug.

## [0.0.4.1] - 2026-10-07

### Fixed
- Corrected the website changelog so the historical 0.0.3 entries are labeled 0.0.3 instead of 0.0.4.
- Synchronized the current version display across the site, browser patcher, README, and both build variants.

### Changed
- Published this documentation/maintenance correction as micro-build 0.0.4.1 without gameplay or content divergence between Release and Debug.

## [0.0.4] - 2026-10-07

### Added
- Added a global `FIELD` utility submenu to the party action menu for badge-unlocked Emerald field moves.
- Added pull-request verification for both Release and Debug ROM builds before major gameplay changes can merge.

### Changed
- Cut, Flash, Rock Smash, Strength, Surf, Fly, Dive, and Waterfall are now unlocked for overworld use by Emerald's original badge progression rather than by a Pokémon knowing the corresponding HM move.
- Preserved the original Stone, Knuckle, Dynamo, Heat, Balance, Feather, Mind, and Rain Badge progression for the eight field utilities.
- Preserved terrain, map, follower, link, and story-puzzle restrictions while removing the HM moveslot requirement.
- Contextual interactions such as Cut trees, breakable rocks, Strength boulders, Surf water, Dive spots, and Waterfalls now work after the appropriate badge without an HM user.
- Field-move prompts and success text no longer identify a Pokémon as the HM user.
- Badge utility effects suppress the old arbitrary Pokémon portrait/banner while retaining player and environment animations.
- Learned non-HM field moves such as Dig, Teleport, Sweet Scent, and similar utilities remain tied to the Pokémon that knows them.

## [0.0.3] - 2026-10-07

### Added
- Added separate, permanently maintained Release and Debug changelog files alongside the canonical project changelog.
- Added a dedicated website changelog page with one-click Release and Debug tabs.
- Added variant-aware changelog validation so every version must appear in the canonical, Release, and Debug histories.

### Changed
- Advanced both build variants to version 0.0.3.
- Added a compact Changelog link to the main project site instead of placing long update histories on the landing page.
- Clarified project documentation so the normal player build is consistently called Release, reserving “vanilla” for the untouched Pokémon Emerald base ROM.

## [0.0.2] - 2026-10-07

### Added
- Added separate Release and Debug distributions built from the same Pokémon Emerald: Legends source.
- Added a Debug download directly below the recommended Release download on the project website.
- Added browser-patcher support for both Release and Debug builds.
- Added distinct in-game version identification for Debug builds as `LEGENDS v0.0.2-D`.

### Changed
- The recommended player build now uses the expansion's native release configuration, disabling developer/debug entry points while preserving all Legends gameplay and content changes.
- The Debug build retains the overworld debug menu, battle debug menu, Pokémon sprite visualizer, and title-screen Quickstart tools supplied by the expansion base.
- The automated release pipeline now builds, patches, reapplies, and byte-for-byte verifies both Release and Debug variants before publishing them.
- Release filenames now use `Pokemon-Emerald-Legends-v0.0.2.bps` and `Pokemon-Emerald-Legends-v0.0.2-debug.bps`.

## [0.0.1] - 2026-10-07

### Added
- Added a centered `LEGENDS` subtitle to the Emerald title screen while preserving the original Pokémon Emerald logo artwork.
- Added `LEGENDS v0.0.1` identification to the in-game Options menu header.
- Added a release/download section to the project website in preparation for patch distributions.
- Added an in-browser BPS patcher that verifies a clean Emerald ROM and creates the playable `.gba` locally without uploading the source ROM.
- Added a reproducible CI workflow that builds and verifies the v0.0.1 BPS patch from decompiled source.
- Established Pokémon Emerald: Legends project identity.
- Adopted `pokeemerald-expansion` as the upstream base.
- Added project roadmap and development documentation.
- Added feature design documents for EXP changes, overworld field moves, and seasons.
- Added an initial GitHub Pages landing site.
- Added repository contribution and feature-request structure.

### Changed
- Established `0.0.1` as the authoritative current development baseline.
- Added an explicit versioning policy: each meaningful shipped change increments the development revision and receives a matching changelog entry.
- Updated release tooling so BPS filenames are derived from the root `VERSION` file.

### Planned during 0.0.x development
- Implement the revised EXP Share behavior already designed during development.
- Implement HM/field-move use from the overworld without requiring a dedicated HM move slot.
- Research and prototype a configurable seasonal system.
