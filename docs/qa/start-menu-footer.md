# Pause-menu page arrow spacing — v0.0.47.1

The owner's screenshot shows the journal page's left arrow immediately touching the EXIT line. The page arrow began at `visibleRows * 16 + 6`; the native EXIT glyph, printed at `(visibleRows - 1) * 16 + 9`, has its last ink/shadow pixel 12 rows below that origin. The previous arrow therefore began on the very next pixel row.

Move the page arrow to `visibleRows * 16 + 10`, four pixels lower. This leaves four blank rows below EXIT. The five-pixel arrow remains inside the existing window, including the full eight-row menu. Its shape and horizontal anchor stay the same; the selection cursor, text, menu dimensions, scrolling and Left/Right page navigation do not move.

The existing compiled-C pause-menu regression checks both page directions at all heights from one through eight rows, the blank gap and actual window pixel bounds. It also retains the normal/Debug builders, action reachability, wrapping, scrolling and tile-allocation checks. The world-panel lifecycle regression and browser patcher/Options checks pass locally. Native build/BPS and publication evidence will be recorded after the release workflow completes.

The approved v0.0.47 sprite and palette fixes remain unchanged. Release and Debug share this menu adjustment.
