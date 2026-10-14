# Development handoff

## Working preferences

The owner may switch between models such as Astra and Sol. Preserve the same decisions, approvals and quality standard; live repository activity supersedes this snapshot. Root `VERSION` is authoritative. Use connected GitHub tools for repository writes, retain exact native pixels/animation geometry, and write completed changelog entries in past tense.

The owner uses a phone. Provide narrow vertical PNG/GIF previews and explicit downloadable filename links; wide inline sheets were clipped and could not be saved conveniently.

On 14 October 2026 the owner reversed the earlier permission to ignore older saves. Backward compatibility for Legends battery saves is now required for future updates. Preserve existing save readers, field offsets and persistent IDs; add focused migrations/tests when saved data changes. [Save-compatibility policy and evidence](SAVE-COMPATIBILITY.md) defines the release gate without adding duplicate builds or per-patch full emulator runs. Existing checks pass; a complete historical-release save-fixture matrix remains unfinished and must not be represented as verified.

## Current version — 0.0.50 (published and verified)

The owner approved all five Mom/Norman tones on 14 October 2026 (“Flawless work. Approved.”). Both parents now inherit the existing player skin choice in all native overworld frames and Norman’s battle portrait. This approval is complete. Preserve hair, clothing, outlines and native animation commands; Mom’s 54 shared-color hair highlights are separated from skin materials without changing their visible colors.

Runtime source: `29e45ad535e1bd6a57e6e18f0a01939dd94740b9`. Private overworld tags `0x1174`/`0x1175` resolve to ROM palettes; Norman’s common trainer-front palette getter handles his battle portrait. Palette entries are appended to preserve numerical berry references. Keep original PNGs and derive colors from `LegendsGetSkinTone()`; do not add separate saved parent choices. No serialized layouts, persistent IDs, old readers, initialization rules or sprite-cache RAM changed. ROM usage grew only 424/880 bytes (Debug/Release); no migration is needed.

## Verification and publication

- All 44 executable project checks passed locally after reconstruction and on [source CI](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38592974123). Actual family C matched all 95 approved asset/tone cases. Approval inputs and nineteen masks are pinned. [QA checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38593983229) passed for `ff0b287a61cbdca1e0590255a581d7a954df7b59`.
- Restored GCC 13.2.1 Debug/Release builds passed with unchanged RAM. mGBA 0.10.2 repeated 190 asset/tone buffers, twenty pond/ice reflection palettes, ten wardrobe Apply/Cancel rounds, unrelated NPC-4 isolation and full sixteen-slot tag reuse. [Reproducible native harness](../tools/legends/native_family_qa/README.md) and receipts are committed. These were controlled ARM callbacks, not normal map/menu traversal or historical-save reload tests.
- [Remote native builds, clean-base identity, independent BPS round trips and patch commit](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38592973976) passed. Patch commit: `491a43c6cf6ad3d581c6ca6b57ee219ccb706a3b`. Both pinned public GitHub downloads returned 200 and matched the manifest, all CRCs and local native target hashes. Release/Debug BPS growth was only 539/904 bytes. [Detailed QA, direct download receipts and approved PNG](qa/family-skin-v0.0.50.md).
- **Pages recovered:** [run 38597478728, attempt 2](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38597478728/attempts/2) succeeded on 14 October 2026 after retrying only failed Pages jobs. The stale deployment lock cleared. Both live BPS downloads matched the manifest, all CRCs and local target hashes; homepage/changelog/patcher/approved PNG matched committed bytes. Earlier timeout/lock/404 observations are resolved historical evidence in the QA record. No ROM rebuild or version bump was required; the temporary recovery workflow remains removed.
- For future publications, allow the active Pages deployment to finish before issuing more publication commits. Inspect stale-lock errors and retry failed jobs after the blocking deployment clears. Keep verified GitHub downloads available and verify live file hashes before claiming site publication; do not redo completed game work for a hosting failure.

- A usage-limit interruption restored an older workspace. Source was reconstructed against preview commit `73f9fae86de65a33a87423efeffa228cfe7df3d5`; the preview matched the original SHA256 and all checks/builds/native tests above were rerun. Current receipts supersede missing pre-interruption logs.

## Protected appearance baseline

The approved Side Part shipped in v0.0.48, retains saved ID 2 and its corrected front atlas cell `(4,17)` using hair shadow 8. All ten imported male overworld cuts are approved. Keep their accepted silhouettes, profiles, independent hair/material colors, v0.0.47 smile/body-color isolation, native animation commands/east mirroring, front portraits and prepared fixed battle uniforms. Retain female hairstyles, saved wardrobe choices, costumes and native diving. [Side Part provenance and verification](qa/side-part-v0.0.48.md); [earlier color repair](qa/appearance-color-fix.md). The v0.0.49 shade pass changes only authored skin-shadow 3 cells after hair/accessory composition.

The front-facing cheek cleanup shipped in v0.0.49; retain its standing edits and pose-specific running masks. [v0.0.49 proof](qa/front-face-v0.0.49.md), [v0.0.47.1 menu QA](qa/start-menu-footer.md) and [resumption audit](qa/project-state-2026-10-14.md) retain prior evidence.

## Remaining work

- Continue uninterrupted Wing Survey/return-travel, battle-balance and broader Release/Debug mGBA/Pizza Boy playtests, including native movement/field actions, wardrobe Apply/Cancel/save/load, followers and seasonal/weather transitions. Controlled scenes and host tests do not establish those outcomes. Use [QA](QA.md) and milestone records.
- All eight visiting Gyms, the three bird expeditions, the Hoenn Regigigas intermission and native Faraway Island/Mew conclusion are implemented. Quest Log, achievements, expanded storage and prepared battle uniforms are established. Do not reimplement shipped features from older summaries.
- [PR #56](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/56) is an older conflicting wiki proposal. Reconcile unique changes before deciding its disposition; do not merge its older Chapters 19–22 snapshot over the current v1.6.0 Chapters 1–25 snapshot. Wiki content remains separately maintained, last reviewed against game v0.0.46, and is updated only when requested.
- Establish a small, reproducible historical-save fixture matrix as save-affecting work proceeds: original fourteen-box format, expanded v0.0.43 format and current pre-update saves, with mid-story/postgame and non-default wardrobe/seasons. Record provenance and verified upgrade paths. Existing legacy emulator evidence and host tests are useful but do not cover every historical release.
- Lucky Egg balance review, seasonal encounters, further configuration consolidation, an upstream-update procedure and later Johto research remain unselected roadmap ideas, not established current regressions.
