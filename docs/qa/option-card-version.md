# Title-menu OPTION version — owner preview

Status: **review branch only; public v0.0.53 remains unchanged**. The owner requested the current version on the far right of the OPTION card shown below NEW GAME/CONTINUE, matching the original text size and alignment. The developer-site refresh is deferred. No publication approval is inferred from earlier bedroom approval.

[Release native preview](option-card-release.png) · [Debug native preview](option-card-debug.png) · [Build/native receipt](option-card-version.json)

The label uses the original FONT_NORMAL, header color/shadow palette and y=1 baseline. Right alignment uses the native card width and actual glyph width. One helper covers window IDs 1/4/5/6 for all existing menu layouts. Release shows `v0.0.53`; Debug shows `v0.0.53-D`, matching the established variant suffix. Root VERSION is unchanged for this preview. The existing inside-Options header remains intact. Future release bumps must update both title-card strings, now guarded by the version metadata check.

Both native builds passed, along with Options text/navigation/title-handoff regressions and the full project metadata block. mGBA 0.10.2 captured selected/unselected cards in all four layouts, including the scrolling Mystery Events layout. Exact ink bounds matched OPTION's vertical pixels in each case (44–52, 108–116 and 140–148), and the version ended at x222 within the x224 card edge. Normal emulated input entered Options and returned to an identical selected scene for both empty and saved menu layouts in both builds. Mystery layouts are controlled rendering cases, not complete event progression tests.

These are actual native 240×160 frames enlarged 2× nearest neighbor. Captions are outside the game image. The harness uses controlled RAM setup with the unmodified locally built ROM; no ROM injection or image-generated assets were used. No ROMs are distributed. No save structures, persistent IDs, gameplay, wardrobe, bedroom, seasons or existing art changed. No BPS or Pages publication was performed for this review milestone.

After owner approval, prepare the next project version, synchronize the version strings/site/changelogs, and perform the normal BPS/CI/Pages release gates. Until then, preserve the published master and downloads.
