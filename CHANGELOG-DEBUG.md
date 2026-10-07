# Pokémon Emerald: Legends - Debug Changelog

This is the developer-facing history for the **Debug** build. Shared Legends changes are repeated here so this file stands on its own; Debug-only behavior is called out separately.

## [0.0.7] - 2026-10-07

### Shared changes
- Professor Birch now enables the National Pokédex during the initial Pokédex handoff.
- Birch's post-Elite Four National Dex upgrade reward is now 25 Rare Candies.
- If the Bag cannot hold all 25, the reward is sent to the PC; if neither has room, Birch keeps the reward pending for a later conversation.
- Existing postgame saves can claim the new Rare Candy reward once without disrupting later Johto starter progression.

### Debug-specific
- No Debug-only gameplay divergence in this version; existing developer tools remain available

## [0.0.6] - 2026-10-07

### Shared changes
- Mr. Stone now gives a Lucky Egg after the Steven Letter delivery instead of the redundant held Exp. Share.
- His reward dialogue now explains the Lucky Egg's EXP bonus.
- Lucky Egg's native multiplier behavior is unchanged; only the Rustboro reward source changed.

### Debug-specific
- No Debug-only gameplay divergence in this version; existing developer tools remain available.

## [0.0.5] - 2026-10-07

### Shared changes
- Added default-on Gen 6-style party EXP Share from the beginning of the game.
- Added an `EXP SHARE` ON/OFF setting to Options.
- Added one-time migration for pre-0.0.5 saves so the new setting starts enabled.
- Reused the expansion-native EXP pipeline so existing multipliers and level-cap behavior remain intact.

### Debug-specific
- No Debug-only gameplay divergence in this version.
- Debug includes the same EXP Share behavior while retaining the existing developer menus, sprite visualizer, and Quickstart tools.

## [0.0.4.2] - 2026-10-07

### Shared changes
- Corrected homepage wording so the field-move feature is accurately attributed to 0.0.4.
- Added a direct Debug changelog link beside the Debug download.
- Tightened changelog/version consistency checks.

### Debug-specific
- No Debug-only gameplay or content changes in this micro-build; existing developer tools remain available.

## [0.0.4.1] - 2026-10-07

### Shared changes
- Corrected mislabeled 0.0.3 headings on the website changelog.
- Synchronized current version labels and download targets to 0.0.4.1.

### Debug-specific
- No Debug-only gameplay or content changes in this micro-build; existing developer tools remain available.

## [0.0.4] - 2026-10-07

### Shared changes
- Cut, Flash, Rock Smash, Strength, Surf, Fly, Dive, and Waterfall are now badge-earned overworld utilities and no longer require a Pokémon to know the HM.
- Added a compact `FIELD` submenu for manually invoking unlocked utilities.
- Preserved Emerald's original badge order, map restrictions, follower restrictions, and Regi puzzle hooks.
- Removed Pokémon-specific HM-use text and suppressed arbitrary Pokémon field-move banners.
- Kept non-HM field moves such as Dig, Teleport, and Sweet Scent move-dependent.

### Debug-specific
- No Debug-only gameplay divergence in this version.
- Debug contains the same badge-field-move behavior while retaining the existing developer menus, sprite visualizer, and Quickstart tools.

## [0.0.3] - 2026-10-07

### Shared changes
- Added dedicated Release and Debug changelog tracking.
- Added a website changelog page with tabs for switching between build histories.
- Improved version/changelog consistency checks.

### Debug-specific
- No new Debug-only gameplay behavior in this version.
- Debug continues to retain the expansion developer tools while matching Release gameplay/content changes.

## [0.0.2] - 2026-10-07

### Shared changes
- Introduced separate Release and Debug downloads built from the same Legends source.
- Added browser patcher support for both build variants.
- Added automated byte-for-byte verification for both published patches.

### Debug-specific
- First formally published Debug variant.
- Retains the overworld debug menu.
- Retains the battle debug menu.
- Retains the Pokémon sprite visualizer.
- Retains title-screen Quickstart.
- Uses `LEGENDS v0.0.2-D` in the in-game Options header to distinguish it from Release.

## [0.0.1] - 2026-10-07

### Pre-split baseline
- Added the `LEGENDS` title-screen subtitle.
- Added the initial in-game Legends version label.
- Added the project website, browser patcher, reproducible patch workflow, roadmap, and initial feature design documentation.
- The original development build already contained expansion debug conveniences, but a separately labeled public Debug distribution had not yet been established.
