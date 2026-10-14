# Development handoff

## Working preferences

The owner may switch between models such as Astra and Sol. Preserve the same decisions, approvals and quality standard; live repository activity supersedes this snapshot. Root `VERSION` is authoritative. Use connected GitHub tools for repository writes, retain exact native pixels/animation geometry, and write completed changelog entries in past tense.

The owner uses a phone. Provide narrow vertical PNG/GIF previews and explicit downloadable filename links; wide inline sheets were clipped and could not be saved conveniently.

On 14 October 2026 the owner reversed the earlier permission to ignore older saves. Backward compatibility for Legends battery saves is now required for future updates. Preserve existing save readers, field offsets and persistent IDs; add focused migrations/tests when saved data changes. [Save-compatibility policy and evidence](SAVE-COMPATIBILITY.md) defines the release gate without adding duplicate builds or per-patch full emulator runs. Existing checks pass; a complete historical-release save-fixture matrix remains unfinished and must not be represented as verified.

## Current version — 0.0.48

The owner approved the retained four-view male Side Part preview on 14 October 2026 and requested preserving its look throughout animation while fixing one transparent pixel beside the front ear. That approval and repair are implemented and published. Front atlas cell `(4,17)` changed from transparency 0 to neighboring hair-shadow 8. Seven earlier corrections already visible in the approved preview were retained. Do not treat this revision as awaiting approval.

[PR #66](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/66) merged as `c9d3a0675a2e4a55e99d73cd14b5a1604eae4c32`. Side Part keeps saved ID 2 and uses the established native pupil/ear registration, pose tables and east mirroring across all 92 non-diving field descriptors. All ten imported male overworld cuts are now approved. The existing sprite cache/bank sizes and save fields are unchanged.

Preserve the v0.0.47 smile/body-color repair, other nine approved cuts, native faces/props, saved wardrobe choices, female art, front portraits, fixed battle uniforms, team costumes and native diving suit. Side Part now reserves the same three independent hair shades as the other approved cuts. Its exact head, animation buffers and the other cuts remain regression-protected by `tools/legends/side_part_approval.json` and the appearance tests. Further redesigns need specific owner feedback.

## Verification and publication

- All 43 runnable project-check steps passed locally and on the merged source. [Master checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38556684070).
- Local GCC 13.2.1 Debug/Release builds passed. mGBA 0.10.2 invoked the actual ARM compositor in a private controlled callback; all 101 native descriptors/palettes matched the approved host-C results, including 92 field poses and nine unchanged diving frames. The tested Debug target hash matches the published target. This was not a natural field/story traversal or save-persistence test.
- [Merged-source native builds, clean-base/BPS application and publication](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38556683931) passed. Patch commit: `4b8573588c586e86a3d26dd887d54f788fc55a70`. [Patch Pages deployment](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38557855004) passed.
- Both live patches returned HTTP 200, matched the pinned SHA256 manifest and passed BPS CRC/source-identity checks. Both target hashes matched the local native builds. Live homepage/changelog/patcher and both mobile previews matched committed bytes.
- [Detailed QA, provenance and downloadable previews](qa/side-part-v0.0.48.md). Reproduce the 360-pixel-wide four-view PNG and native-command walking/running GIF with `python3 tools/legends/preview_side_part.py`. These are actual C sprite-buffer exports, not emulator screen captures.

Earlier evidence remains in [v0.0.47 sprite/color QA](qa/appearance-color-fix.md), [v0.0.47.1 menu QA](qa/start-menu-footer.md) and the [resumption audit](qa/project-state-2026-10-14.md). Preserve their release provenance rather than inferring current state from historical pending-work notes.

## Remaining work

- Continue uninterrupted Wing Survey/return-travel, battle-balance and broader Release/Debug mGBA/Pizza Boy playtests, including native movement/field actions, wardrobe Apply/Cancel/save/load, followers and seasonal/weather transitions. Controlled scenes and host tests do not establish those outcomes. Use [QA](QA.md) and milestone records.
- All eight visiting Gyms, the three bird expeditions, the Hoenn Regigigas intermission and native Faraway Island/Mew conclusion are implemented. Quest Log, achievements, expanded storage and prepared battle uniforms are established. Do not reimplement shipped features from older summaries.
- [PR #56](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/56) is an older conflicting wiki proposal. Reconcile unique changes before deciding its disposition; do not merge its older Chapters 19–22 snapshot over the current v1.6.0 Chapters 1–25 snapshot. Wiki content remains separately maintained, last reviewed against game v0.0.46, and is updated only when requested.
- Establish a small, reproducible historical-save fixture matrix as save-affecting work proceeds: original fourteen-box format, expanded v0.0.43 format and current pre-update saves, with mid-story/postgame and non-default wardrobe/seasons. Record provenance and verified upgrade paths. Existing legacy emulator evidence and host tests are useful but do not cover every historical release.
- Lucky Egg balance review, seasonal encounters, further configuration consolidation, an upstream-update procedure and later Johto research remain unselected roadmap ideas, not established current regressions.
