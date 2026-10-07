# Pokémon Emerald: Legends - Debug Changelog

This is the developer-facing history for the **Debug** build. Shared Legends changes are repeated here so this file stands on its own; Debug-only behavior is called out separately.

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
