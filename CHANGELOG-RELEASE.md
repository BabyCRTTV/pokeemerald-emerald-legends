# Pokémon Emerald: Legends - Release Changelog

This is the player-facing history for the recommended **Release** build. Shared Legends changes are repeated here so this file stands on its own; Release-only behavior is called out separately.

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
