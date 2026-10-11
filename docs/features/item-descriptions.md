# First-time obtained-item descriptions

**Status:** Implemented in 0.0.36; shared by Release and Debug.

The expansion's native `OW_SHOW_ITEM_DESCRIPTIONS` is set to `OW_ITEM_DESCRIPTIONS_FIRST_TIME`. Supported gifts, field item balls, hidden-item and berry/apricorn scripts show a small top description window and item icon alongside the ordinary receipt dialogue. On later receipts of that item type, only the native small receipt icon appears. The first receipt is recorded when the script dismisses the description. Failed bag additions do not consume a discovery.

This uses the existing `showitemdescription` / `hideitemdescription` script macros, native item descriptions, line wrapping and icon handling. It does not add pop-ups to shops, the PC, arbitrary direct `AddBagItem` calls or unlock-restoration helpers. New event rewards should use the native obtain-item scripts rather than duplicating the UI.

## Save compatibility

Upstream places `itemFlags` before other SaveBlock3 fields when first-time descriptions are enabled. Legends instead appends the bitmap at the old block end, offset `0x21C`, after the Adventure Log. A compile-time assertion guards this position. SaveBlock1/2 and all older SaveBlock3 fields keep their addresses. Old full saves zero-filled the reserved sector tail, so existing profiles start with an empty discovery history; past receipts, including items already carried, cannot be recovered. New Game resets the native flags normally.

SaveBlock3 already occupies reserved 116-byte chunks in the 14 native flash sectors. The expanded block fits this existing capacity. Full saves use the original chunk copy/load functions. Native partial/link saves normally write only sectors 0–4. `WriteSaveBlock3Tail` updates appended chunks in the remaining sectors using the previously saved PC payload, not the live RAM PC. It validates the native sector ID/signature/checksum, skips unchanged chunks and uses the native verified flash writer and damaged-sector reporting. It reuses the existing sector buffer and adds no sector-sized RAM allocation.

## Validation

`python3 test/legends-item-descriptions.test.py` exercises the real item-bit and chunk functions: all item IDs, invalid IDs, old-profile loading, both slots with every rotation, unchanged-write skipping, PC payload preservation, checksum rejection and write failures. `test/legends-options-text.test.py` checks arrow bounds, glyphs and label clearing. Native ARM builds enforce the append offset and total sector capacity. Manual emulator checks should cover first/repeat receipts, dismissal, full save/load and partial-save persistence.

mGBA 0.10.2 verifies all four speed labels/arrows, native first/repeat Potion receipts, Escape Rope and TM description wrapping, dismissal, full save/load and both native partial-save paths. The fixture enters a quiet map and invokes the native reward script; it is not a full story walkthrough. The appended history increases EWRAM by 112 bytes, with no additional sector buffer.
