# Development handoff

## Working preference

The owner switches between models such as Astra and Sol. Use the selected model's strengths, retain the same quality standard, and communicate project decisions, approvals, validation and unfinished work through this file and the linked records. Live repository activity supersedes this snapshot. Inspect it before resuming; do not infer publication from a commit alone.

The owner prefers changelog entries in past tense for easy reading. Use this convention in the canonical, Release, Debug and website changelogs.

## Current work — 0.0.48 Side Part

The owner approved the retained four-view male Side Part preview on 14 October 2026 and requested preserving its look through animation while fixing one purple/transparent cell beside the front ear. This authorizes that existing revision and its single-cell repair. Front atlas cell `(4,17)` now uses neighboring hair shadow 8. Seven earlier corrections from the approved preview were retained; no other haircut was redesigned.

The candidate uses all ten approved imported male overworld cuts. Side Part keeps saved ID 2 and fits the existing native walking/running, bike/trick, Surf, field-move, fishing and watering poses. Retain the v0.0.47 smile/body-color repair, fixed battle uniforms, existing front portraits, female art, costumes and native diving suit. Other nine head-atlas rows and all unrelated sparse layers remain fingerprint-protected.

Dedicated checks match the approved head reference, all 18 walk/run frames, 92 non-diving field descriptors, native command directions/flips, pupils, colors and wardrobes. The generic 212-pose/400 smile-color/1,440 wardrobe checks passed. All 43 runnable regression workflow steps passed locally. Native build/publication verification is in progress; do not report the candidate published until its workflows and live downloads are confirmed. [Side Part QA and previews](qa/side-part-v0.0.48.md).

The owner uses a phone and needs narrow vertical PNG/GIF previews plus explicit downloadable filename links. Reproduce these from actual C buffers with `python3 tools/legends/preview_side_part.py`; distinguish them from emulator captures.

## Previous verified version — 0.0.47.1

The owner requested a clear gap between EXIT and the pause-menu page arrow. The correction moves only the page indicator four pixels lower, providing four blank rows below EXIT while retaining cursor placement, horizontal alignment, eight visible rows and navigation.

Source: `942ee29598420c22442be61c18e5a902b72759ea` via [PR #65](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/65). [Merged project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38497167668) and [native Debug/Release build/BPS verification](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38497167671) passed. Patch commit: `76aea480d17c684acc14303daec1e80ee43842f8`. [Menu QA](qa/start-menu-footer.md). PR #65 retains the final live-download confirmation after deployment.

## Accepted baseline

- Approved sprite baseline: **0.0.47**, shared by Release and Debug.
- The owner approved the minimal smile/body-color repair and requested publication. Preserve the existing v0.0.46 sprites and approved hairstyle artwork. Generated replacement sprites were rejected and are absent from the released tree.
- Male native mouth/chin/ear and exposed-skin contours now use skin shadow instead of hair color. Natural custom hair receives body isolation; footwear remapping reserves both hair slots. Clothes and shoes retain their selected colors across hair-color changes.
- Existing save choices, female sprites, approved battle art, fixed costumes, diving and untouched Original retain their established behavior. The previously separate Side Part revision was approved on 14 October 2026 and is integrated in the v0.0.48 candidate above.

## Confirmed implementation and validation

- [PR #64](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/64) merged as `f6e4cd519c654865267f47e4cbcde48a233179bf`.
- Versioned PR checks and native Debug/Release/BPS verification passed before merge. Merged-source [project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38495112804) and [publication workflow](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38495112683) passed.
- Both patches independently reproduced their corresponding compiled ROMs byte-for-byte against the verified clean Emerald base. Patch commit: `818792a92ad8623b099b6486fa4413006bd5d246`. [v0.0.47 manifest](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/blob/818792a92ad8623b099b6486fa4413006bd5d246/docs/downloads/SHA256SUMS.txt).
- At v0.0.47 publication, the live Pages index, changelog and browser patcher agreed on that version. Both public BPS downloads returned HTTP 200, matched the verified SHA256 manifest and passed patch CRC checks. The simplified PNG also returned HTTP 200. QA/preview commit `12211c565f772bb6f6dde77eb77c1fd3b27dc275` passed project checks and Pages deployment.
- Relevant checks cover frozen artwork fingerprints, 212 native poses, 400 smile/color/skin cases, 1,440 front/field wardrobe combinations, footwear caches, intro, wardrobe and prepared battle sprites. [Detailed QA](qa/appearance-color-fix.md).
- [Simplified matching wardrobe/overworld PNG](qa/v0.0.47-sprite-sheet.png) shows Natural/Blond Crew Cut with identical Emerald clothing and red shoes, plus Silver Tousled with Trail/navy/Ocean scarf/black boots. It uses actual compiled-C buffers, not generated replacements or emulator captures. Reproduce with `python tools/legends/preview_appearance_baseline.py`.

## Next work

Resume audit on **14 October 2026** verified default-branch head `aa921927300c032a3f6ef3d28a962b46ccadb21e`, v0.0.47.1, current Actions and live Pages downloads. All 42 runnable project-check steps passed locally. Both public patches returned HTTP 200, matched the pinned SHA256 manifest and passed patch CRC checks. The release-source-to-head comparison contained only documentation and published patches; runtime inputs still match the verified native build. [Audit, workflow evidence and playtest limits](qa/project-state-2026-10-14.md).

- The roadmap and development guide were reconciled with shipped work: all eight visiting Gyms, three bird expeditions, the Hoenn Regigigas intermission and the native Faraway Island/Mew conclusion are implemented. Quest Log, achievements, expanded storage and prepared battle uniforms are also established. Do not rebuild these features from older summaries.
- Complete the remaining uninterrupted Wing Survey/return-travel, battle-balance and broad mGBA/Pizza Boy regression playtests. Controlled emulator scenes and host tests do not establish those outcomes. See [QA](QA.md) and the audit's priority list.
- [PR #56](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/56) remains open and merge-conflicting. It targets an older wiki snapshot; current wiki v1.6.0 already covers Chapters 19–25. Reconcile its unique changes before deciding its disposition; do not merge the older snapshot over the current wiki. Wiki updates remain separate, manual and owner-requested.
- Lucky Egg balance review, seasonal encounters, further configuration consolidation, a reusable test-save matrix, an upstream-update procedure and later Johto research remain roadmap ideas, not verified regressions or a newly selected implementation task.

The approved Side Part and its requested one-cell repair are the current visual task. Further artwork redesigns still need specific owner feedback. Preserve the color repair, protected-asset checks, native animation geometry and fixed battle-uniform decision. The earlier documentation audit retained v0.0.47.1; its evidence remains historical.
