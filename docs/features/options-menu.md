# Paged Options Menu

**Status:** Implemented in 0.0.8

## Goal

Keep Pokémon Emerald: Legends settings expandable without compressing the original Options screen or allowing window graphics to overlap in VRAM.

## Pages

The menu currently has two pages:

- **General 1/2** - Text Speed, Battle Scene, Battle Style, Sound, Button Mode, Frame, and Cancel.
- **Legends 2/2** - project-specific settings, beginning with EXP Share, plus Cancel.

Press **L** or **R** while the Options menu is open to switch pages. The active page and an L/R hint are shown in the header. D-pad Left/Right continues to change the selected setting normally, and B still saves/exits as before.

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
