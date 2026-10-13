# Prepared male battle appearance — v0.0.45

Ten male battle cuts match the saved male wardrobe IDs: Crew Cut, Side Part, Spiky, Side Sweep, Tousled, Quiff, Shag, Curls, Man Bun and Undercut (1–10). Original (0) retains Brendan’s native hat. Curls retains the supplied small white-and-green cap above its exposed ringlets. Skin tone remains active. Battle clothing stays fixed; field sprites and front/wardrobe portraits keep full customization.

## Authoring

Original uploads are preserved under `graphics/legends/battle_sources/brendan`; names and IDs live in `tools/legends/battle_brendan_sheets.json`. `import_brendan_battle_sheets.py` extracts hair and the Curls cap, aligns them to native eye landmarks, and packs static tiled 4bpp art. Native Brendan’s face, hands, clothing and four 64x64 poses supply all anatomy. Complete supplied characters are never scaled down. Native frame order is wind-up/cast/release/idle, corresponding to supplied columns 2/3/4/1. Emerald animates the moving Ball separately.

Pose-local face, collar and glove/cuff masks retain native anatomy. Seven blue cap-tip cells touching the raised fingers are excluded from the hand mask; the release cuff is selected from its red glove instead of the similarly green headwear. Native cap fragments are cleared before fitting the current cut. Internal hair strands use hair-shadow colors instead of fixed black specks.

The Curls cap has one connected white crown, a pale gray seam and softer slate contour. Isolated sampled white fragments are removed, and gaps in the green brim use adjacent cap materials. Its white/green/gray colors remain fixed across hair and skin choices. All nine other male cuts retain their reviewed frame blocks.

## Palettes and runtime

Male hair normally uses slots 4/7/9. Curls uses two independent hair shades in 4/7 and reserves 9 for the original Emerald cap gray. The cap uses white 14, green 10/11 and slate outlines 6/8. Skin remains in 1–3; backpack/cuffs retain green 10/11, red gloves/collar retain 12–13, eyes and strap highlights retain white 14. The two darkest native navy shades are consolidated into 8, and gray strap highlights use fixed white. Female hair keeps slots 4/7/11 and the approved v0.0.44 bitmaps.

`legends_battle_appearance.c` selects both gender banks through the native back-image/palette helpers. It rebuilds palettes from the current hairstyle, one of eight hair colors and one of five skin tones on each request. Clothing/accessory/costume trainer IDs resolve to the current gender, so wardrobe APPLY changes appear in the next battle. Original and non-Legends trainer IDs retain their established fallbacks. Both banks are static ROM assets; no head/body layering runs in battle, and the existing two 16-color palette buffers are reused.

## Validation and approval

The prepared-battle regression verifies asset reproduction, twenty distinct cuts/eighty connected frame silhouettes, native skin/hand/collar/lower-body geometry, green cuffs/backpack and red clothing, all eight colors/five skin tones, costume routing, Original fallback and later wardrobe refresh. Independent bitmap checks cover the reported cap-tip coordinates, intact fingers/cuffs, a single Curls white crown and visible gray shading in every frame. The actual C selector verifies fixed Curls cap gray and independent skin/hair materials. All forty female frame bitmaps remain byte-identical to approved v0.0.44.

Local Debug compiled with GCC 13.2.1. mGBA 0.10.2 matched all twenty compiled banks to the checked-in buffers and rendered all ten male cuts in native wild-battle introductions, observing all four frames and continuing to the command menu. The final Curls cap was reviewed again after its gray/slate polish, across all eight hair colors/five skin tones and its native throw. Reviewed Debug ROM SHA-256: `fd583687c3fe84a1fcb0c876203dbb4a341badb8187690b7b9987807bed23f9e`.

[Project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38379349836) and the [approved-artwork build](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38379350172) passed. The build compiled Release and Debug, independently built and SHA-1-verified the clean Emerald reference, and reapplied both BPS patches with byte-for-byte comparisons. The still galleries decode compiled buffers, pose loops use native animation timing, and full-battle GIFs use actual emulator video. This is targeted sprite verification, not an exhaustive playthrough.

The user visually approved all ten male styles, including the final softened Curls cap, on October 13, 2026. [PR #61](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/61) publishes the approved artwork as v0.0.45. Master repeats the full patch-verification workflow before publishing the Release/Debug downloads. Only BPS patches and checksums are distributed; ROMs and isolated QA saves remain private.
