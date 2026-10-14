# Development handoff

## Working preferences

On 14 October 2026, after reviewing the art and animation touch-ups and the completed v0.0.50 work, the owner explicitly confirmed that this level of quality met their expectations. Treat today's approved pixel art, faithful animation, careful material isolation and verified incremental changes as the standard to maintain in future work. Preserve that polish across model changes and do not reinterpret this positive feedback as a request to redesign approved assets.

The owner may switch between models such as Astra and Sol. Preserve the same decisions, approvals and quality standard; live repository activity supersedes this snapshot. Root `VERSION` is authoritative. Use connected GitHub tools for repository writes, retain exact native pixels/animation geometry, and write completed changelog entries in past tense.

The owner uses a phone. Provide narrow vertical PNG/GIF previews and explicit downloadable filename links; wide inline sheets were clipped and could not be saved conveniently.

On 14 October 2026 the owner reversed the earlier permission to ignore older saves. Backward compatibility for Legends battery saves is now required for future updates. Preserve existing save readers, field offsets and persistent IDs; add focused migrations/tests when saved data changes. [Save-compatibility policy and evidence](SAVE-COMPATIBILITY.md) defines the release gate without adding duplicate builds or per-patch full emulator runs. Existing checks pass; a complete historical-release save-fixture matrix remains unfinished and must not be represented as verified.

## Current version — 0.0.52 (published and verified)

The owner approved the corrected achievement preview and publication on 14 October 2026: “You did it! Perfect. Publish approved.” Approval and publication are complete. The game now has **95 achievements**, with new IDs 80–94 appended. Original IDs 0–79, earned/claimed bits and the 36-byte version-1 journal remain intact. New goals backfill quietly and stay unclaimed. Manual one-time claims, atomic full-PC retry and the temporary PC Item Storage confirmation are preserved. The upper-left unlock notice queues, defers around scripts/menus/fades/location banners, lasts about three seconds and never consumes player input.

Keep the corrected panel on BG0 tiles **0x70–0xB7** (VRAM 0x8E00–0x96FF). The first preview’s 0x2C0 allocation overlapped map screen block 28 at 0xE000 and corrupted when the camera moved. The regression now derives physical VRAM bounds from the actual overworld templates and compares every visible native/GIF frame. All 172 visible frames passed with four-direction movement; the final v0.0.52 GIF had 23 visible encoded frames (approved preview: 29, due to frame coalescing). Preserve the approved dimensions, colors, fonts and native animation/assets. [Detailed design, compatibility, approved previews and complete evidence](qa/achievement-preview.md).

[PR #67](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/67) merged as `7e166f0af96fe8e0adf2e9ebdb4edb7c8976ad9b`. [Merged checks 38613064246](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38613064246) and [native builds/independent clean-base BPS round trips 38613063922](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38613063922) passed. All 46 local check blocks and both local builds passed; CI ROM hashes matched local outputs. VERSION, all changelogs, Options, README, site/patcher, journal guides and the parity-tested JSON/C catalogues are synchronized. No save migration or art changes were introduced; static EWRAM growth is only 24 bytes.

Patch commit `5349d41f5eb70c45de316f447f09f68a96317ba5` and [Pages 38614496615](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38614496615) succeeded. Both live downloads matched HTTP 200, pinned SHA256, source/target/patch CRCs and local target hashes. Homepage/changelog/patcher/guides/approved PNG/GIF matched committed bytes. Patch growth was only 2275/1294 bytes (Release/Debug). [Public receipts](qa/achievement-v0.0.52-public.json), [final local/native receipts](qa/achievement-v0.0.52-local.json). No publication blocker remains.

For future publications, let the active Pages deployment finish before further publication commits. Earlier v0.0.50 timeout/lock/404 problems were resolved; preserve the deployment ordering and verify live hashes. Do not redo completed game work for a hosting failure. [Historical Pages recovery evidence](qa/family-skin-v0.0.50.md).

## Protected feature and appearance baseline

v0.0.51 kept Adventure Log on pause-menu page one only; page two contains Quest Log, Achievements and Exit. Keep the dark plum selected journal row, cream text/background matching and separate pointer, including claimed markers. [v0.0.51 evidence](qa/journal-selection-v0.0.51.md).

The owner approved all five Mom/Norman tones in v0.0.50. Both inherit the existing player skin choice across native overworld frames and Norman’s battle portrait. Preserve hair, clothing, silhouettes and animations; Mom’s 54 shared-color hair highlights retain their visible colors. Private palette tags 0x1174/0x1175 and the common trainer-front palette getter derive colors from `LegendsGetSkinTone()`, with no separate saved parent choices or sprite-cache RAM. Keep original PNGs and append palettes to preserve berry references. [Implementation, approval and native evidence](qa/family-skin-v0.0.50.md).

The approved Side Part shipped in v0.0.48, retains saved ID 2 and its corrected front atlas cell `(4,17)` using hair shadow 8. All ten imported male cuts are approved. Preserve silhouettes/profiles, independent hair/material colors, v0.0.47 smile/body-color isolation, native animations/east mirroring, portraits, fixed battle uniforms, female art/styles, saved choices, costumes and diving. [Side Part evidence](qa/side-part-v0.0.48.md), [earlier color repair](qa/appearance-color-fix.md).

The front-facing cheek cleanup shipped in v0.0.49; retain standing edits and pose-specific running masks. [v0.0.49 evidence](qa/front-face-v0.0.49.md), [v0.0.47.1 footer QA](qa/start-menu-footer.md), [resumption audit](qa/project-state-2026-10-14.md).

## Remaining work

- Continue uninterrupted Wing Survey/return-travel, battle-balance and broader Release/Debug mGBA/Pizza Boy playtests, including native movement/field actions, wardrobe Apply/Cancel/save/load, followers and seasonal/weather transitions. Controlled scenes and host tests do not establish those outcomes. Use [QA](QA.md) and milestone records.
- All eight visiting Gyms, the three bird expeditions, the Hoenn Regigigas intermission and native Faraway Island/Mew conclusion are implemented. Quest Log, achievements, expanded storage and prepared battle uniforms are established. Do not reimplement shipped features from older summaries.
- [PR #56](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/56) is an older conflicting wiki proposal. Reconcile unique changes before deciding its disposition; do not merge its older Chapters 19–22 snapshot over the current v1.6.0 Chapters 1–25 snapshot. Wiki content remains separately maintained, last reviewed against game v0.0.46, and is updated only when requested.
- Establish a small, reproducible historical-save fixture matrix as save-affecting work proceeds: original fourteen-box format, expanded v0.0.43 format and current pre-update saves, with mid-story/postgame and non-default wardrobe/seasons. Record provenance and verified upgrade paths. Existing legacy emulator evidence and host tests are useful but do not cover every historical release.
- Lucky Egg balance review, seasonal encounters, further configuration consolidation, an upstream-update procedure and later Johto research remain unselected roadmap ideas, not established current regressions.

## New design review — evolving bedroom (unapproved)

The owner selected evolving bedrooms, requested visual stages before implementation and asked that changes extend through the existing Kanto finale. They reiterated using existing game assets for world building; preview any proposed newly designed artwork first. [Design review, staged native-asset PNGs, milestone mapping and implementation constraints](designs/evolving-bedroom/README.md). Direction A combines family flowers, Hoenn awards, Kanto report posters and a final voyage ornament; B and C are alternatives. These are static compositions, not running ROM changes. VERSION remains 0.0.52; runtime/source artwork and public patches are unchanged. Await the owner's design review. Preserve saved decoration placements; native tile/palette capacity, collisions and old-save backfill still require implementation and verification after approval.
