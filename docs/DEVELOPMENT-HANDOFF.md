# Development handoff

## Working preferences

The owner may switch between models such as Astra and Sol. Preserve the same decisions, approvals and quality standard; live repository activity supersedes this snapshot. Root `VERSION` is authoritative. Use connected GitHub tools for repository writes, retain exact native pixels/animation geometry, and write completed changelog entries in past tense.

The owner uses a phone. Provide narrow vertical PNG/GIF previews and explicit downloadable filename links; wide inline sheets were clipped and could not be saved conveniently.

On 14 October 2026 the owner reversed the earlier permission to ignore older saves. Backward compatibility for Legends battery saves is now required for future updates. Preserve existing save readers, field offsets and persistent IDs; add focused migrations/tests when saved data changes. [Save-compatibility policy and evidence](SAVE-COMPATIBILITY.md) defines the release gate without adding duplicate builds or per-patch full emulator runs. Existing checks pass; a complete historical-release save-fixture matrix remains unfinished and must not be represented as verified.

## Current version — 0.0.49

The owner approved the five-tone male/female shading comparison on 14 October 2026 after explicitly limiting the cleanup to the **front-facing overworld face**. The accepted twelve male/four female standing cheek edits are implemented and published in both builds. Native running faces have shorter jaws and retain their anatomy through their own pose masks. This approval is complete; do not redesign other views or lighten the global skin palettes.

Source commit: `e1f1a53d5de5b6573a46a652dd909827be1314be`. Preserve jaw outlines, eyes, smile, ears, hair, hands/clothing, side/rear views, wardrobe/front portraits, battle art, costumes and diving. All 202 field descriptors have entries; only 62 front masks contain edits. The original sixteen style layers/offsets remain byte-identical; 404 bytes of deduplicated sparse edits plus small ROM descriptors reuse the existing cache. No saved fields, capacities, codecs, initialization rules or persistent IDs changed, so this update needs no migration. Keep the standing older-save requirement.

## Protected appearance baseline

The approved Side Part shipped in v0.0.48, retains saved ID 2 and its corrected front atlas cell `(4,17)` using hair shadow 8. All ten imported male overworld cuts are approved. Keep their accepted silhouettes, profiles, independent hair/material colors, v0.0.47 smile/body-color isolation, native animation commands/east mirroring, front portraits and prepared fixed battle uniforms. Retain female hairstyles, saved wardrobe choices, costumes and native diving. [Side Part provenance and verification](qa/side-part-v0.0.48.md); [earlier color repair](qa/appearance-color-fix.md). The new shade pass changes only authored skin-shadow 3 cells after hair/accessory composition.

## Verification and publication

- All 44 workflow commands passed locally and on the published source. [GitHub project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38562989276). The new integrated C suite made 2,866 before/after comparisons; only approved front cheek pixels changed and all palettes were unchanged.
- Local GCC 13.2.1 Debug/Release builds passed. mGBA 0.10.2 invoked the actual ARM compositor through an isolated private callback after boot; all 1,010 descriptor/palette buffers across both characters and five skin tones matched the host C output. This was not natural activity traversal or save-persistence testing. The published Debug target matches the tested native ROM.
- [Remote Debug/Release builds, independent clean-base/BPS application and publication](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38562989056) passed. Patch commit: `bd4327fc62250ab92b0a6fc615e76b49ccbf8fee`. [Patch Pages deployment](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38564243447) passed.
- Both live patches matched the pinned SHA256 manifest and passed patch/source/target CRC checks. Both target hashes matched the local native builds. Live homepage/changelog/patcher and all three review PNG/GIF files matched committed bytes.
- [Detailed QA, structured proof and downloadable mobile previews](qa/front-face-v0.0.49.md). Reproduce with `python3 tools/legends/preview_front_face.py`: 360-pixel-wide PNG/GIF exports use real C buffers and native South walking/running commands. The GIF is checked frame-by-frame for exact encoded pixels/colors; these are sprite-buffer exports, not emulator captures.

Earlier menu/state evidence remains in [v0.0.47.1 menu QA](qa/start-menu-footer.md) and the [resumption audit](qa/project-state-2026-10-14.md). Keep historical release provenance separate from current verification.

## Remaining work

- Continue uninterrupted Wing Survey/return-travel, battle-balance and broader Release/Debug mGBA/Pizza Boy playtests, including native movement/field actions, wardrobe Apply/Cancel/save/load, followers and seasonal/weather transitions. Controlled scenes and host tests do not establish those outcomes. Use [QA](QA.md) and milestone records.
- All eight visiting Gyms, the three bird expeditions, the Hoenn Regigigas intermission and native Faraway Island/Mew conclusion are implemented. Quest Log, achievements, expanded storage and prepared battle uniforms are established. Do not reimplement shipped features from older summaries.
- [PR #56](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/56) is an older conflicting wiki proposal. Reconcile unique changes before deciding its disposition; do not merge its older Chapters 19–22 snapshot over the current v1.6.0 Chapters 1–25 snapshot. Wiki content remains separately maintained, last reviewed against game v0.0.46, and is updated only when requested.
- Establish a small, reproducible historical-save fixture matrix as save-affecting work proceeds: original fourteen-box format, expanded v0.0.43 format and current pre-update saves, with mid-story/postgame and non-default wardrobe/seasons. Record provenance and verified upgrade paths. Existing legacy emulator evidence and host tests are useful but do not cover every historical release.
- Lucky Egg balance review, seasonal encounters, further configuration consolidation, an upstream-update procedure and later Johto research remain unselected roadmap ideas, not established current regressions.
