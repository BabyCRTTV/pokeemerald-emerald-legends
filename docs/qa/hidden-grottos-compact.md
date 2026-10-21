# Compact grotto interior review

Unshipped third visual review on v0.0.68, requested 21 October 2026. The owner asked for neater, smaller interiors; no merge/publication approval was given.

Each review-only layout is now 18×16 instead of 22×20 tiles: 288 rather than 440 cells, a 34.5% reduction. The outdoor clearings have complete native tree borders, grouped flowers/grass and a clear central approach. Rainroot has a smaller rectangular reflective pool. Stillwater has a continuous compact chamber wall, a narrow native spring and two rocks. The visitor, item placeholder, clues, entry warp and walking exits were moved together. Published map/layout IDs and all three existing route entrance/return locations are unchanged from the previous review.

## Validation

- Debug and Release compiled locally. The first Debug link found a zero-byte cached `menu_specialized.o`; deleting only that empty build object and rebuilding passed without source changes. Compiler warnings already present in the baseline remain.
- All five focused grotto regressions passed: append-only IDs and bounded route changes, reachability of each interaction/exit, safe route returns, complete native trees and exhaustive compiled entrance guard probes. The reachability tests now assert 18×16 dimensions and the updated approach. The tree test derives dimensions from the layout instead of assuming 22×20.
- Native mGBA 0.10.2 checked all twelve seasonal scenes, matching visitor sprites, active season and passable player positions. Real input approached each Spring visitor, closed dialogue, walked out, declined an entrance and reentered all three rooms. The continuous 176-frame Leafshade discovery film was recaptured with the compact destination. [Native receipt](../designs/hidden-grottos/verification.json), [assertions](../designs/hidden-grottos/emulator.log).
- Native Quickstart smoke passed on the unmodified Debug ROM. Existing season/calendar checks, all 84 seasonal encounter tables and eight Kanto event-script checks passed. Both build hashes are recorded in the accompanying JSON.
- Visually inspected the three actual native overview captures in the [compact preview sheet](../designs/hidden-grottos/Emerald-Legends-Grottos-Compact-Preview.png). Labels/enlargement are outside the original 240×160 images. This sheet supersedes the second review's larger interior sheet; original historical sheets remain as comparison evidence.

This is controlled native Debug scene QA, not a natural full story playthrough, historical-save matrix, Release emulator verification or Pizza Boy proof. Capture battles, item rewards and persistent refresh contents remain unimplemented. No version, BPS, public-site, wiki or release update was performed. Keep all ROMs/private fixture binaries out of uploads. Draft PR #87 remains the review checkpoint.
