# Paged Options Menu

**Status:** Implemented in 0.0.8

## Goal

Keep Pokémon Emerald: Legends settings expandable without compressing the original Options screen or allowing window graphics to overlap in VRAM.

## Pages

The menu currently has three pages:

- **General 1/3** - Text Speed, Battle Scene, Battle Style, Sound, Button Mode, Frame, and Next Page.
- **Legends 2/3** - EXP Share, Follower, Shiny Rate, Seasons, Current, Set Season, and Next Page.
- **Adventure 3/3** - Starters, a New Game applicability reminder, and Next Page.

Select **NEXT PAGE** and press **A** to cycle to the next page. The bottom row always shows **A: NEXT  B: SAVE**, independently of the version label. Press **B** from any row to save all settings from both pages and exit. **L/R** remain shortcuts for switching pages; navigation is handled before A/B so L still works with Button Mode set to L=A. D-pad Left/Right continues to edit settings. The header identifies the page and build version.

## Layout safety

Version 0.0.5 temporarily expanded the single Options window to fit an eighth row. That made the 26-by-15-tile window buffer extend into tile IDs reserved for the window-frame graphics beginning at 0x1A2, producing corrupted/repeating borders on accurate emulators.

Version 0.0.8 restores the safe upstream layout:

- Header window: 26 × 2 tiles, base block 0x002.
- Options window: 26 × 14 tiles, base block 0x036.
- The Options buffer therefore ends at 0x1A1; frame graphics begin at 0x1A2.

Each page supports up to seven 16-pixel rows in the current layout. Future settings should be added to a page table (or a new page) rather than increasing the window height without another VRAM allocation review.

## Maintenance rule

When adding a setting:

1. Add the menu item identifier and label.
2. Place it in the appropriate page table.
3. Keep each page at seven rows or fewer, including Next Page.
4. Add its draw/input handling without changing the safe window dimensions.
5. Update this document and the changelog when the setting ships.

## v0.0.10 SHINY RATE

Legends 2/2 now has EXP SHARE, SHINY RATE and CANCEL. Use Left/Right to cycle 1/8192 (default), 1/5680, and 1/1226. The value is saved when leaving Options. Older saves default to 1/8192 using a zero-initialized unused permanent var, without changing existing save-block layouts.

The new setting affects newly generated ordinary wild, fishing, surfing and DexNav encounters only. Shiny Charm, chain fishing and DexNav search bonuses add rolls. Gifts, eggs and scripted Pokémon remain governed by the base expansion rules.

## v0.0.12 seasons

Legends 2/2 has six rows: EXP SHARE, SHINY RATE, SEASONS, CURRENT, SET SEASON and CANCEL. SEASONS offers REAL TIME / 7H PLAY. CURRENT shows the environment currently in use. SET SEASON is editable with Left/Right only in gameplay mode; real time displays CALENDAR. Leaving Options stores edits, while the next faded map load applies the environment.

Choice strings use the native COLOR/SHADOW prefix. The renderer checks for this prefix before recoloring, preventing ordinary letters from becoming control values. Single seasonal values clear their previous text before redraw. Keep labels within the existing 15-byte choice limit, including control codes.

## v0.0.12.1 title-screen choices

Legends settings selected in title-screen Options now carry into New Game: EXP Share, shiny rate, season mode and the selected gameplay season. The new save receives a fresh seven-hour timer and applies the season before its opening maps. Only explicitly staged title choices cross the new-save reset; story flags and playtime do not. Staging clears after use and on a fresh title entry, while Continue and in-game Options retain their native behavior.

## v0.0.13 followers

Legends 2/2 now has seven rows: EXP SHARE, FOLLOWER, SHINY RATE, SEASONS, CURRENT, SET SEASON and CANCEL. FOLLOWER uses Left/Right to toggle ON/OFF and defaults to ON. Leaving Options stores the choice and the native field reload applies it. It persists with ordinary game saves and participates in the title-screen New Game settings bridge. Both pages are now at the seven-row limit; future settings need a new page instead of a larger window.

## v0.0.18 visible page navigation

NEXT PAGE replaces the historical CANCEL row on both pages. Its A-button action uses the same page-switch function as L/R, preserving pending settings across pages and selecting the first row on arrival. B remains the save/exit action from any row. The permanent control hint uses the small native font within the seventh row; the header no longer tries to fit an optional L/R hint between the page title and version. Window sizes, tile allocation and save layout remain unchanged.

## v0.0.19 starters

Adventure 3/3 adds STARTERS: GEN 1 through GEN 9, SPECIAL and RANDOM. Left/Right cycles choices; Gen 3 is the default. Title-screen selections carry into New Game. Changes before opening the rescue bag affect that rescue; after the trio locks, edits apply to a future New Game. See [starter and rival rules](starters.md). This third page preserves all existing settings and the original window allocation.

## v0.0.34 Instant text

General → TEXT SPEED cycles SLOW / MID / FAST / INSTANT with Left/Right; B saves and exits. Only the selected value is displayed, clearing the previous label inside the original window.

INSTANT exposes the expansion's existing `OPTIONS_TEXT_SPEED_INSTANT` through the native saved `optionsTextSpeed` field and `RunTextPrinters` implementation. It immediately reveals dialogue, while native page confirmations, scripted pauses and choices still apply. No renderer fork, new save data or save migration is needed. Existing selections and the Mid default remain unchanged. Native title-screen Options also preserve this setting into New Game. Shared by Release and Debug.

Validation: actual-C Options regressions exercise both-direction wrap through all four speeds, selected-label rendering, clearing INSTANT before a shorter value, and invalid-value fallback. mGBA 0.10.2 verifies the native Options screen and saved speed after field reload, plus immediate field dialogue and a page break that waits for A. The private dialogue fixture uses controlled map entry; the renderer itself is unchanged.

## v0.0.35 Window frames

General → FRAME now cycles TYPE 1–25. Types 1–20 retain their native artwork and saved IDs. The five new choices are:

| Type | Design | Detail |
| --- | --- | --- |
| 21 | Leaf | Muted green trim and corner leaves |
| 22 | Ocean | Blue trim with a repeating wave |
| 23 | Lavender Stitch | Soft purple trim and light stitching |
| 24 | Amber Circuit | Warm amber traces with small corner nodes |
| 25 | Poké Ball | Neutral rose trim and small corner Poké Balls |

The native Options live preview and standard windows use these frames. Emerald's fixed field dialogue, signs and battle graphics keep their native behavior. Assets are appended to `sWindowFrames`; each is a 24×24 indexed PNG containing nine eight-pixel tiles (288 bytes in 4bpp), with a 16-color palette. Native transparency, text colors and the white middle tile are preserved. The existing five-bit saved selection fits 25 types, so no save migration or window/VRAM expansion is needed.

Regenerate the pixel art with `python3 scripts/generate_legends_frames.py` (Pillow). `test/legends-window-frames.test.py` checks hardware/color limits, registration, and the actual Options input function across all 25 types in both directions. Shared by Release and Debug.

mGBA 0.10.2 checks all five live Options previews, TYPE 1↔25 wrap, saved TYPE 25 after field reload, and its native Yes/No menu plus dismissal. Controlled map entry was used; RAM usage is unchanged.

## v0.0.36 Text-speed arrows

Small green Left/Right arrows bracket the selected TEXT SPEED value at window x=112 and x=188. The native small font and existing choice-area clearing keep SLOW / MID / FAST / INSTANT readable without enlarging the window. Navigation and saving remain native.

mGBA 0.10.2 checks all four labels with the arrows, then B saves back to the field.
