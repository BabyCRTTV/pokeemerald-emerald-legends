# Approved Side Part — v0.0.48

## Approval and scope

On 14 October 2026 the owner approved the retained four-view male Side Part preview, asked that animation preserve its look, and requested one small purple/transparent pixel beside the front-facing ear be filled. The review image's SHA-256 and exact native-grid head reference are retained in `tools/legends/side_part_approval.json`.

The newly requested repair changed front head cell **(4,17)** from transparent index 0 to hair-shadow index 8, matching the cells immediately beside it. Seven earlier corrections already present in the approved review were transferred from that preview: two front face/ear cells and five profile cells. These were not additional redesigns. All nine other atlas cuts are byte-identical at the pixel level.

Side Part's existing saved ID 2 now uses the same established imported-head pipeline as the other nine approved male cuts. Source registration follows native pupils/ears and keeps native motion, frames, mirroring, hands and props. Its three hair shades reserve indices 4/7/8; native clothing and pupils retain stable navy index 5. Removed the former Side Part-only palette/footwear exceptions that belonged to its unapproved legacy masks. The v0.0.47 smile/body-color repair remains active.

Female artwork, other haircuts, front/wardrobe portraits, prepared battle sheets/fixed uniforms, costumes and the native covered diving suit were preserved. Save fields, option IDs, animation tables and the existing sprite cache/bank sizes were unchanged. Sparse ROM edit data grew by 21,574 bytes; no extra runtime sprite bank was allocated.

## Animation and appearance checks

`python3 test/legends-side-part.test.py` executes the actual C appearance palette, wardrobe/footwear cache and sparse compositor. It verifies:

- Exact front/rear/profile head pixels against the approved native-grid reference, including the one repaired cell.
- The same crown/fringe through all 18 native walking/running descriptors, allowing native translation/head bob. Four native running ear-rim cells retain their existing skin-shadow variation; the hair does not morph with them.
- Actual South/North/West/East animation commands, frame IDs, durations and native east mirroring.
- Frozen pixel buffers for all 92 non-diving field descriptors: walking/running, Mach Bike, Acro Bike/tricks, Surf, field moves, fishing and watering. Covered diving frames remain native.
- Eight hair colors, five skin tones, native pupil RGB and head isolation through selected outfit/coat/scarf/shoe combinations.
- Pixel fingerprints for all nine other imported head cuts. The existing broader fingerprint tests continue protecting other sparse hair/coat layers, portraits and battle art.

The generic real-C compositor tests passed for all 212 native table poses. Smile/body-color checks passed for 400 color/skin cases and 1,440 wardrobe combinations. A legacy palette expectation was updated because Side Part now intentionally uses its approved three-shade palette rather than the previously frozen legacy palette. No unrelated test protection was removed.

## Reproducible previews

Run `python3 tools/legends/preview_side_part.py` to export:

- [Mobile four-view PNG](side-part-v0.0.48-mobile.png)
- [Mobile walking/running GIF](side-part-v0.0.48-motion.gif)
- [All 92 field descriptors](side-part-v0.0.48-all-poses.png)

The mobile PNG/GIF are 360 pixels wide, with four vertically stacked directions and nearest-neighbor scaling. The GIF reads the game's native walk/run frame commands and durations instead of inventing animation poses. These are actual compiled-C sprite-buffer previews, **not emulator captures**. The complete field contact sheet was visually reviewed for direction, hair shape, native anatomy and props.

## Build and publication

Implementation started from verified master `b81cc6e212efdc2c250b3e125a361c3340365a5a` / v0.0.47.1. Root VERSION, Options, README, homepage, browser patcher and all three changelogs were advanced together to **0.0.48**; new changelog entries used past tense. Release and Debug share the art and repair, retaining their established developer-feature separation. Wiki content remains its separate manual snapshot.

All 43 runnable project-check workflow steps passed locally and in [PR checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38555631321). GCC 13.2.1 native Debug and Release builds passed locally. The [PR native builds/clean-base/BPS verification](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38555630992) passed before [PR #66](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/66) merged as `c9d3a0675a2e4a55e99d73cd14b5a1604eae4c32`.

mGBA 0.10.2 booted a private copy of that Debug build and invoked the actual ARM appearance/footwear compositor through a controlled QA callback. All **101 native descriptors** (92 customized field poses plus nine native diving frames) and their 16-color palettes matched the host-C buffers exactly. The unmodified local Debug ROM had SHA-256 `bc21b87a634fd61d12b1159941879fb9bf7ef6689629feab5a0a1c6fa905fa78`, matching the published Debug target. Only the private QA copy contained the callback; no harness or full ROM was committed or distributed. This was a native sprite-buffer comparison, not an uninterrupted field traversal or save-persistence test.

[Merged-source project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38556684070) and [native Debug/Release build/BPS publication](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38556683931) passed. The publication workflow independently built and identity-checked vanilla Emerald, applied both patches and compared both results byte-for-byte with their compiled ROMs. Patch commit: `4b8573588c586e86a3d26dd887d54f788fc55a70`; [pinned manifest](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/blob/4b8573588c586e86a3d26dd887d54f788fc55a70/docs/downloads/SHA256SUMS.txt). [Patch Pages deployment](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38557855004) passed.

Both live v0.0.48 BPS downloads returned HTTP 200, matched that manifest and passed BPS patch CRC/source-identity checks. Both manifest target-ROM hashes matched the corresponding local native builds. Homepage, changelog, patcher HTML/JavaScript and mobile PNG/GIF returned HTTP 200 and matched committed bytes. [Structured verification evidence](side-part-v0.0.48-verification.json).

The approved Side Part and its requested cell repair are published in both variants. Full natural activity traversal, saved wardrobe changes on mGBA/Pizza Boy and broader story/balance playtests remain separate QA work.
