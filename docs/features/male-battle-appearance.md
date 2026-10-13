# Prepared male battle appearance — v0.0.45

Ten male battle cuts match the saved male wardrobe IDs: Crew Cut, Side Part, Spiky, Side Sweep, Tousled, Quiff, Shag, Curls, Man Bun and Undercut (1–10). Original (0) retains Brendan's native hat. Skin tone remains active in both cases. Battle clothing stays fixed; field sprites and front/wardrobe portraits keep full customization.

## Authoring

The original uploads are preserved under `graphics/legends/battle_sources/brendan`, with names and IDs in `tools/legends/battle_brendan_sheets.json`. `import_brendan_battle_sheets.py` reuses the established source-hair extraction, native eye alignment and tiled 4bpp packing. Hair is fitted to native Brendan's face, hands, clothing and four 64x64 poses; complete supplied characters are never scaled down. Native frame order is wind-up/cast/release/idle, corresponding to supplied columns 2/3/4/1. The moving Ball remains Emerald's native animation.

Pose-local face, collar and glove/cuff masks preserve native anatomy and clear the original cap. The raised-hand regions exclude white/grey cap tips that overlap a broad hand rectangle; the release cuff is identified from the red glove rather than the similarly green brim. The Curls reference still has a cap, so an authored scalloped crown completes its covered hair while retaining exposed reference ringlets.

Male hair owns palette slots 4/7/9. Skin stays in 1–3; backpack and cuffs retain green slots 10–11, red gloves/collar retain 12–13, eyes and strap highlights retain white 14. The two darkest native navy shades are consolidated into slot 8, and grey strap highlights use fixed white. These edits free three hair shades without tinting native clothing. Eight hair ramps are shared with the approved female system; female hair keeps slots 4/7/11 and its original bitmaps.

## Runtime and validation

The same native image/palette helpers now select both gender banks from the current hairstyle, color and skin tone. They rebuild palettes on each request and resolve clothing/accessory/costume trainer IDs to the current gender, so later wardrobe APPLY changes appear in the next battle. Both banks are static ROM assets; no head/body layering runs in battle and the existing two 16-color palette buffers are reused.

The prepared-battle regression exercises reproducible assets, twenty distinct cuts/eighty connected frame silhouettes, native skin/hand/collar/lower-body geometry, green cuffs/backpack and red clothing, all eight colors/five skin tones, clothing/costume routing, Original fallback and simulated later wardrobe changes for both genders. All forty approved female frame bitmaps are byte-identical to live v0.0.44. Local Debug compilation, actual mGBA review and verified Release/Debug BPS checks are in progress. The male art remains a draft pending visual review.
