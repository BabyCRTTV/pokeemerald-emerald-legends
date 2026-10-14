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

All 43 runnable project-check workflow steps passed locally. Native Debug/Release builds and verified BPS publication are being completed for this candidate. Record final workflow/download evidence before reporting publication. Host buffer checks do not establish an uninterrupted emulator traversal through every activity or a full story playthrough.
