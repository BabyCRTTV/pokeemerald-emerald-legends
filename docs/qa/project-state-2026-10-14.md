# Project-state audit — 14 October 2026

## Verified baseline

The owner requested resumption from the live repository with existing features, accepted artwork and development history preserved. The audit started from a clean checkout of default branch `master` at `aa921927300c032a3f6ef3d28a962b46ccadb21e`. Root `VERSION` was **0.0.47.1**.

The latest runtime change was [PR #65](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/65), merged as `942ee29598420c22442be61c18e5a902b72759ea`: the pause-menu page arrow moved four pixels below its previous position. The approved v0.0.47 sprite/color repair and v0.0.46 artwork were retained. Commit `76aea480d17c684acc14303daec1e80ee43842f8` published the corresponding BPS patches and checksums. The comparison from that build's source to the audit head contained documentation and published patches only; there were no intervening runtime/build-input changes.

## Actions and distribution

The live repository's latest relevant runs all completed successfully:

| Workflow | Verified run | Source |
| --- | --- | --- |
| Native Debug/Release builds and BPS application | [38497167671](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38497167671) | `942ee295` |
| Project checks | [38498697791](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38498697791) | `aa921927` |
| Pages build/deployment | [38498697287](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38498697287) | `aa921927` |
| Wiki checks | [38454666276](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38454666276) | `4e795dc0` |
| Wiki Android APK | [38454666288](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38454666288) | `4e795dc0` |
| Wiki Windows installer | [38454666408](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38454666408) | `4e795dc0` |

The release job's individual steps confirmed both native builds, independently built clean Emerald, canonical base identity, both BPS applications/byte comparisons and patch publication. This audit inspected job/step results; it did not rerun native ROM builds. The supported clean base remains SHA-1 `f3ae088181bf583e55daf962a92bb46f4f1d07b7` / CRC32 `1f1c08fb`.

Direct HTTPS verification on 14 October returned HTTP 200 for the public homepage, changelog, patcher HTML/JavaScript, wiki homepage and both current BPS downloads. Homepage, changelog and patcher agreed on v0.0.47.1. Both downloaded patches were byte-identical to the repository files, matched the [pinned publication manifest](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/blob/76aea480d17c684acc14303daec1e80ee43842f8/docs/downloads/SHA256SUMS.txt), had valid BPS patch CRCs and declared the expected 16 MiB source / 32 MiB target sizes.

| Variant | Public patch | SHA-256 |
| --- | --- | --- |
| Release | [v0.0.47.1](https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Pokemon-Emerald-Legends-v0.0.47.1.bps) | `bc0430b72901d48c7111c6e36c4d3d8027ea14ea8a423ab7116c30d3a0280d97` |
| Debug | [v0.0.47.1 Debug](https://babycrttv.github.io/pokeemerald-emerald-legends/downloads/Pokemon-Emerald-Legends-v0.0.47.1-debug.bps) | `e6caf7c2a69a6f69cba89bb06d980b194affb5bb6afef64a4bfe720a849c4ee7` |

ROM distribution uses Pages-hosted BPS files. The GitHub Releases collection contained the separate `wiki-desktop` companion prerelease; it was not a newer game release. The wiki's intentional manual snapshot was revision **1.6.0**, reviewed against game **0.0.46**, with Chapters 1–25. It is not automatically synchronized on ROM releases.

## Current implementation

- The Wing Survey includes all eight visiting Gyms (Blue in Viridian), Zapdos/Articuno/Moltres expeditions, the Weather Institute/Regigigas intermission, Oak's analysis and the original Faraway Island/Mew conclusion. Optional observation/capture, retry, old caught-Mew profiles and return travel are implemented. Route 22's League approach, unrelated interiors and the rest of Sevii remain closed.
- Home/secret-base wardrobe, saved appearance choices, fixed Magma/Aqua costumes, striped Sport shorts, footwear, female leggings, independent hair colors and prepared male/female battle art are established. Battle sprites intentionally use fixed uniforms; overworld/front portraits retain wardrobe customization. Preserve the approved artwork and exact native poses, with [color-repair evidence](appearance-color-fix.md).
- Seasons use calendar time or seven saved gameplay hours per season, with changes committed at faded map loads. Seasonal grass effects/winter scuffs, Kanto foliage and battle palette restoration are implemented. Dynamic forecasts avoid the misplaced SUNNY CLOUDS reflection effect; the pause panel has day/night and animated weather indicators. Older reports of these issues are not evidence of an unresolved current regression.
- Party EXP Share, early National Dex/DexNav, starter selection, shiny-rate options, followers, badge-earned field utilities, the journal page/Quest Log, 80 achievements and expanded storage remain in the current source.

## Local validation

All **42 runnable steps** from `.github/workflows/legends-checks.yml` passed locally on the audit baseline, including metadata. This included protected-art fingerprints, native pose/compositor/color cases, wardrobe/battle refresh, seasonal/weather behavior, storage/save compatibility, event progression and browser BPS decoding. The dependency-install line was omitted locally because Pillow 12.3.0 was already installed; the successful GitHub run used its pinned Pillow 11.3.0. No new tests or runtime changes were needed for this documentation audit.

Documentation maintenance reconciled `ROADMAP.md` and `docs/DEVELOPMENT.md`, distinguished historical Kanto plans/QA checklists from current status, and retained the handoff. The root version, three versioned changelogs, game assets, runtime/build inputs, wiki snapshot and released patch bytes were preserved. Documentation validation checked whitespace, local links and the exact changed-file scope.

## Remaining work and limits

1. **Uninterrupted gameplay QA:** complete the Wing Survey naturally from a Champion save, including ferry returns, native ledges/currents/spinner paths, losses/retries and full-inventory rewards. Existing [expedition](story-v0.0.41.md) and [finale](finale-v0.0.42.md) evidence used controlled emulator entry and event tests; it does not establish an uninterrupted playthrough or human battle balance.
2. **Compatibility and appearance QA:** extend normal Release/Debug and older-save playtests on mGBA and Pizza Boy across movement/field actions, wardrobe Apply/Cancel/save/load, followers, seasonal grass/reloads, weather and day/night transitions. Keep the existing [QA checklist](../QA.md), exact tested scenarios and protected-asset checks. No new emulator session was run in this audit.
3. **Artwork feedback:** preserve v0.0.47's approved baseline. The separate Side Part redesign remains unapproved. No further artwork redesign was selected by this resumption request.
4. **Older wiki PR:** [#56](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/56) remained open with merge conflicts. Its v0.0.41 Chapters 19–22 snapshot predates the published v1.6.0 Chapters 19–25 snapshot. Compare unique changes before resolving or closing it; do not overwrite the newer wiki by merging it blindly. No other open PRs or standalone open issues were returned by the live repository listing.
5. **Future roadmap ideas:** Lucky Egg balance review, seasonal encounters, configuration consolidation, a reusable test-save matrix, an upstream-update procedure and later Johto research remain unselected work. None was established as a current runtime defect by this audit.

This maintenance milestone retained **v0.0.47.1** and its verified Release/Debug patches. The next gameplay or visual change requires a concrete task; the historical feature list is not a request to replace completed work.
