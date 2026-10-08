# Paged Options Menu

**Status:** Implemented in 0.0.8

## Goal

Keep Pokémon Emerald: Legends settings expandable without compressing the original Options screen or allowing window graphics to overlap in VRAM.

## Pages

The menu currently has two pages:

- **General 1/2** - Text Speed, Battle Scene, Battle Style, Sound, Button Mode, Frame, and Cancel.
- **Legends 2/2** - project-specific settings, beginning with EXP Share, plus Cancel.

Press **L** or **R** while the Options menu is open to switch pages. The active page is shown in the header. The L/R hint appears when enough horizontal space remains beside the current version label, avoiding text collisions as version numbers grow. Page navigation is handled before A/B input so L still switches pages when Button Mode is set to L=A. D-pad Left/Right continues to change the selected setting normally, and B still saves/exits as before.

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
3. Keep each page at seven rows or fewer, including Cancel.
4. Add its draw/input handling without changing the safe window dimensions.
5. Update this document and the changelog when the setting ships.

## v0.0.10 SHINY RATE

Legends 2/2 now has EXP SHARE, SHINY RATE and CANCEL. Use Left/Right to cycle 1/8192 (default), 1/5680, and 1/1226. The value is saved when leaving Options. Older saves default to 1/8192 using a zero-initialized unused permanent var, without changing existing save-block layouts.

The new setting affects newly generated ordinary wild, fishing, surfing and DexNav encounters only. Shiny Charm, chain fishing and DexNav search bonuses add rolls. Gifts, eggs and scripted Pokémon remain governed by the base expansion rules.
