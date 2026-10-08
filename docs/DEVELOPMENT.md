# Development Guide

## Repository model

Pokémon Emerald: Legends should remain a normal fork/derivative of `rh-hideout/pokeemerald-expansion` so upstream changes can be incorporated deliberately.

Recommended remotes for local development:

```text
origin   -> BabyCRTTV/pokeemerald-emerald-legends
upstream -> rh-hideout/pokeemerald-expansion
```

## Branch strategy

- `master` - current playable development line
- `feature/<name>` - larger gameplay features when isolation is useful
- tags/releases - milestone snapshots using the current `VERSION` value

Small, well-contained changes may be committed directly to `master` during early development, but each commit should describe one logical change whenever practical.

## Legends-specific code

Prefer these patterns:

1. Use existing expansion configuration options when they already solve the problem.
2. Add Legends-specific configuration flags for behavior that should remain optional.
3. Keep new systems modular rather than scattering unrelated logic across many engine files.
4. Document every substantial custom mechanic in `docs/features/`.
5. Note any upstream files that require invasive edits so future expansion updates can be reconciled carefully.

## Build artifacts

Do not commit generated ROMs, copyrighted ROM data, save files containing personal information, or temporary build output that upstream excludes.

## Versioning

The authoritative project version lives in the root `VERSION` file.

Current version: `0.0.12.1`.

During active pre-1.0 development, each meaningful shipped change increments the development revision:

- `0.0.1` - initial baseline
- `0.0.2` - Release/Debug distribution split
- `0.0.3` - separate variant changelogs
- `0.0.4` - badge-earned HM field utilities
- `0.0.4.1` - changelog-label and release-metadata maintenance
- `0.0.4.2` - changelog split housekeeping and stronger consistency checks
- `0.0.5` - default-on Gen 6-style party EXP Share with Options toggle
- `0.0.6` - Rustboro Lucky Egg reward replacing the redundant held Exp. Share
- `0.0.7` - National Pokédex from the initial Birch handoff and 25 Rare Candy Champion reward
- `0.0.8` - paged General / Legends Options framework and window-frame corruption fix
- `0.0.8.1` - browser patcher safety and regression testing
- `0.0.9` - physical Exp. Share Key Item and early DexNav unlock
- `0.0.10` - configurable wild shiny encounter rate in Legends Options
- a fourth segment such as `0.0.3.1` may be used for a very small follow-up build when that is clearer than consuming the next normal revision

Every version bump must update the canonical, Release, and Debug changelogs and be mirrored in player-facing version text. See [VERSIONING.md](VERSIONING.md).

## Quality checks

Run node --test test/legends-patcher.test.cjs for BPS decoding and ROM-selection race coverage. CI verifies both variant builds and patch byte-for-byte round trips. The QA checklist (docs/QA.md) distinguishes automated validation from emulator scenarios that still need hands-on testing.

- `0.0.12.1` - preserve title-screen Legends settings through New Game initialization
- `0.0.12` - seven-hour seasons, faded map transitions, manual gameplay season selection and Options text fixes
- `0.0.11` - real-time / 28-hour seasons, outdoor foliage and region-aware weather
