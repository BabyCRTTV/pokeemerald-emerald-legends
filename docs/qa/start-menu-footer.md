# Pause-menu page arrow spacing — v0.0.47.1

The owner's screenshot shows the journal page's left arrow immediately touching the EXIT line. The page arrow began at `visibleRows * 16 + 6`; the native EXIT glyph, printed at `(visibleRows - 1) * 16 + 9`, has its last ink/shadow pixel 12 rows below that origin. The previous arrow therefore began on the very next pixel row.

Move the page arrow to `visibleRows * 16 + 10`, four pixels lower. This leaves four blank rows below EXIT. The five-pixel arrow remains inside the existing window, including the full eight-row menu. Its shape and horizontal anchor stay the same; the selection cursor, text, menu dimensions, scrolling and Left/Right page navigation do not move.

The existing compiled-C pause-menu regression checks both page directions at all heights from one through eight rows, the blank gap and actual window pixel bounds. It also retains the normal/Debug builders, action reachability, wrapping, scrolling and tile-allocation checks. The world-panel lifecycle regression and browser patcher/Options checks pass locally. Merged-source project checks and native build/BPS verification also passed; evidence follows below.

The approved v0.0.47 sprite and palette fixes remain unchanged. Release and Debug share this menu adjustment.

## Release evidence

- Source correction merged through [PR #65](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/pull/65) as `942ee29598420c22442be61c18e5a902b72759ea`.
- [Merged-source project checks](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38497167668) passed. The [publication workflow](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/actions/runs/38497167671) built both native variants, checked the canonical clean Emerald identity, and applied both BPS patches with byte-for-byte comparisons against the compiled ROMs.
- Commit `76aea480d17c684acc14303daec1e80ee43842f8` records the verified Release/Debug patches and [pinned SHA256 manifest](https://github.com/BabyCRTTV/pokeemerald-emerald-legends/blob/76aea480d17c684acc14303daec1e80ee43842f8/docs/downloads/SHA256SUMS.txt). Live download verification is recorded in PR #65 after deployment.
