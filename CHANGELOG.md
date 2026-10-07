# Changelog

All notable Pokémon Emerald: Legends project changes are documented here.

For build-specific player views, see [CHANGELOG-RELEASE.md](CHANGELOG-RELEASE.md) and [CHANGELOG-DEBUG.md](CHANGELOG-DEBUG.md). The canonical history below records the project as a whole.

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
