# DexNav icon sizing and centering correction — v0.0.63

**Model: GPT-6 | Approach: measure native icon padding and grid spacing; preserve source art/animation and correct only DexNav presentation.**

The owner approved the seasonal roster and silhouette approach, but reported sizing/centering issues and confirmed the affected sprites are DexNav icons. The original preview remains historical evidence for encounter behavior; its captures do not verify this correction. Publication remains on hold for the corrected visual preview.

## Finding and correction

The grid places columns 24 pixels apart. Native party icons use two 32×32 frames with species-specific transparent padding; their visible art can be wider than the columns or sit several pixels below the cursor. Examples in the native icon PNGs include Wingull/Pelipper (26px wide), Surskit (25px), and Wattrel with its visible center 7px below the canvas center. This is a presentation issue, not damaged sprite data.

A DexNav-only factory scans the native tiled 4bpp union of both frames, targets 22×24 bounds, centers the pair and uniformly shrinks only oversized art using GBA 8.8 affine matrices. Fixed placement across both poses preserves native relative motion. Small species are not enlarged. Original graphics, tile buffers, native callbacks, animation timing, palettes and party/battle/follower rendering stay intact. Discovered and silhouette states use the same factory. The GUI frees its icon matrices on both close and search exits; the engine also resets affine resources on map return. Allocation/empty-data guards preserve safe native behavior.

## Verification in progress

Focused local checks passed: existing proximity/encounter selection, isolated palettes/search locks, seasonal resolver/data, and 4,096 executable shipped-C tiled two-pose geometry/GBA sampling cases. Geometry checks cover edge/corner padding, pose union, original tile/palette/callback preservation, shrink-only uniform matrices, raster bounds/centering, empty art and allocation failure.

The native checker now covers the original 19 scenes plus all 16 fully discovered seasonal land rosters: 35 scenes and 8,960 actual wild creations. It verifies both poses' hardware-sampled visible bounds/centering for every native grid icon, including water residents, in addition to the existing palette/animation/lock/closure/protected-state checks. Native builds, BPS round trips and refreshed captures are pending. Do not describe the correction as natively verified until the live runs succeed and the captures are reviewed.
