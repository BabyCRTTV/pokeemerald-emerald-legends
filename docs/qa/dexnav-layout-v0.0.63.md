# DexNav icon sizing and centering — v0.0.63

**Model: GPT-6 | Approach: measure native padding and actual panel bounds; execute shipped C and inspect compiled Legends in mGBA.**

The owner approved the seasonal roster and silhouette approach, then reported DexNav sizing/centering issues. The correction is complete at `4660dc5387b2990ccb0ddecfbe0a7156cd4d862b`; its actual-game captures passed visual review. PR #78 merged as `069b026dd8ab4c5a83981932a6a04da2219ac439`; v0.0.63 was published and its live downloads were verified. The approved encounter selections are unchanged.

## Finding and correction

DexNav spaces columns 24 pixels apart, while native party icons have two 32×32 frames with species-specific padding. Wingull/Pelipper can be 26px wide, Surskit 25px, and Wattrel's original visible center sits 7px below its canvas center. The cursor and empty-X art have their own vertical padding.

The private DexNav factory measures the native tiled 4bpp pose union, uniformly shrinks only art exceeding a 22×22 target, then centers the pixels the GBA actually samples. This also handles isolated edges that disappear during reduction. Both poses share one placement, retaining relative animation; small species are never enlarged. Exceptionally sparse custom art and exhausted matrix allocation fall back safely to native scale. Original assets, tile buffers, callbacks, timing, palettes, party/battle/follower rendering and save layouts remain intact. Known icons and silhouettes use identical fitting. Both GUI exits free icon matrices.

The OAM origins are not the visible panel centers. Actual white interiors are water y25–49, land y66–89 / y90–114, and hidden y131–155. Final anchors are water y37, land y77/y103 and hidden y143. Cursor and empty-X offsets use the same anchors, preserving interaction coordinates. Native assertions check both centering and containment inside those white interiors.

## Verified evidence

- [Project checks 39147065953](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39147065953) passed, including existing encounter/proximity/lock/palette regressions and 4,096 executable tiled two-pose geometry cases, sparse-pixel fallback, and actual panel-boundary cases.
- [Native mGBA 39147065854](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39147065854) passed unmodified Debug Quickstart, all 23 previous Living Hoenn cases and all 35 seasonal/DexNav cases. The latter created 8,960 actual wild Pokémon and checked original icon buffers/VRAM frames, black/known palettes, unseen A rejection, all grid-icon bounds/centering, closure and protected state. Every seasonal visitor also has a fully discovered color capture. All 54 native PNG frames were visually inspected.
- [Asset audit](dexnav-layout-v0.0.63-assets.json): the actual C factory executed on all 1,809 native 32×64 icon sheets, including forms/GBA alternatives. Every rendered pose union stayed centered within one pixel and measured at most 22×22; source pixels/callbacks/palettes remained intact. This is host sampling coverage, not 1,809 emulator scenes. Koffing/GBA Dragonite exposed isolated-edge sampling cases during development; the rendered-union correction and sparse fixture cover that condition.
- [Build/BPS 39147065915](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39147065915): Debug, Release, canonical-base and both BPS round trips passed.

Native Debug ROM SHA-256: `607731b0953f924e0e164b02341be128de64c2628f1d34a64a5ade9708482541`. [Machine receipt](dexnav-layout-v0.0.63-native.json) records source, workflow/artifact identity and harness hashes. Captures came from native mGBA 0.10.2 running a private diagnostic copy of the actual compiled Legends Debug ROM. Fixture setup controlled route/season/seen state; the downloadable base ROM was checked unchanged. Only PNG/JSON/logs were uploaded, never ROM/ELF/save files.

[Before/after PNG](dexnav-layout-v0.0.63-preview.png) · [native-frame GIF](dexnav-layout-v0.0.63-preview.gif) · [Route 101](route-101-seasonal-v0.0.63-centered-preview.png) · [Route 102](route-102-seasonal-v0.0.63-centered-preview.png) · [Route 103](route-103-seasonal-v0.0.63-centered-preview.png) · [Route 104](route-104-seasonal-v0.0.63-centered-preview.png) · [frame provenance](dexnav-layout-v0.0.63-previews.json).

All 20 PNG panels preserve exact native pixels at 2× nearest-neighbor with captions outside gameplay. The GIF preserves two genuine native states with illustrative 500ms timing, rather than claiming a continuous recording. The before panel is the original approved-preview source, not a synthesized reconstruction.

## Review history and limits

Intermediate `2a23cb65` passed builds and 35 native cases but its screenshots were rejected internally: those checks centered against OAM origins and missed panel-heading intrusion. It was not published. Final `4660dc53` added measured panel anchors and real containment assertions, and all replacement captures were reviewed. Do not use intermediate captures as accepted visuals.

Controlled Debug scenes do not establish natural progression, full detector hunts, native Release interaction, authentic historical-save migration or Pizza Boy coverage. Those broader tests remain separate backlog items. No saved field, persistent ID or migration was introduced. The wiki snapshot was intentionally promoted to published status only after the actual live game release was verified. Independent wiki/app versions, approved artwork and historical review provenance were preserved.

## Publication verification — 18 October 2026

Production [build/BPS 39148034379](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39148034379), [project checks 39148034495](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39148034495) and [native mGBA 39148034545](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/39148034545) passed. All 54 production frames had identical decoded pixels to the reviewed source captures. Patch commit `55b63356583daef21e11af20f0b1412c2659d354` deployed with successful Pages 39148635650. Fresh live Release and Debug BPS downloads matched committed bytes/manifest and independently reconstructed both exact production ROMs with Floating IPS and the downloaded browser decoder against canonical clean Emerald. Debug matched the native test base. Eleven public site/preview files matched committed bytes. [Public receipts, hashes and limits](dexnav-layout-v0.0.63-public.json) · [Wiki snapshot promotion](wiki-seasonal-v0.0.63-promotion.json). No game publication blocker remained.
