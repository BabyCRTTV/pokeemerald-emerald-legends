# DexNav icon sizing and centering correction — v0.0.63

**Model: GPT-6 | Approach: measure native icon padding and grid spacing; preserve source art/animation and correct only DexNav presentation.**

The owner approved the seasonal roster and silhouette approach, but reported sizing/centering issues and confirmed the affected sprites are DexNav icons. The original preview remains historical evidence for encounter behavior; its captures do not verify this correction. Publication remains on hold for the corrected visual preview.

## Finding and correction

The grid places columns 24 pixels apart. Native party icons use two 32×32 frames with species-specific transparent padding; their visible art can be wider than the columns or sit several pixels below the cursor. Examples in the native icon PNGs include Wingull/Pelipper (26px wide), Surskit (25px), and Wattrel with its visible center 7px below the canvas center. The native cursor and empty-X art also sit 4px/5px below their canvas centers. This is a presentation issue, not damaged sprite data.

A DexNav-only factory scans the native tiled 4bpp union of both frames, targets 22×22 bounds, centers the GBA-sampled pair and uniformly shrinks only oversized art using GBA 8.8 affine matrices. Fixed placement across both poses preserves native relative motion. Centering uses the rendered pose union after shrink sampling, so a discarded isolated pixel cannot shift the result; exceptionally sparse custom art falls back to its native scale rather than vanishing. Small species are not enlarged. Original graphics, tile buffers, native callbacks, animation timing, palettes and party/battle/follower rendering stay intact. Discovered and silhouette states use the same factory. The cursor and empty X receive matching display offsets, retaining their source pixels and interaction coordinates. The GUI frees its icon matrices on both close and search exits; the engine also resets affine resources on map return. Allocation/empty-data guards preserve safe native behavior.

## Verification in progress

Focused local checks passed: existing proximity/encounter selection, isolated palettes/search locks, seasonal resolver/data, and 4,096 executable shipped-C tiled two-pose geometry/GBA sampling cases. Geometry checks cover edge/corner padding, pose union, original tile/palette/callback preservation, shrink-only uniform matrices, raster bounds/centering, empty art and allocation failure.

A host audit executed the actual C factory against all 1,809 native 32×64 icon PNG sheets (including forms and GBA alternatives). Every rendered two-pose union stayed centered within one pixel and fit at most 22×22 pixels; native tile data/callbacks/palettes remained intact. [Asset receipt](dexnav-layout-v0.0.63-assets.json). This is host sampling coverage, not 1,809 emulator scenes. It caught two isolated-edge sampling cases (Koffing and GBA Dragonite); centering now uses the rendered union, and a sparse-pixel regression guards that case.

The native checker now covers the original 19 scenes plus all 16 fully discovered seasonal land rosters: 35 scenes and 8,960 actual wild creations. It verifies both poses' hardware-sampled visible bounds/centering for every native grid icon, including water residents, in addition to the existing palette/animation/lock/closure/protected-state checks. Native builds, BPS round trips and refreshed captures are pending. Do not describe the correction as natively verified until the live runs succeed and the captures are reviewed.
