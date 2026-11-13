# Shared bag reserve

v0.0.79 expanded the Bag to 1,152 total stacks shared automatically across Items (including healing), Key Items, Poké Balls, TMs/HMs and Berries. Unused capacity is available to every pocket; adding an item definition no longer requires changing a pocket limit. Each stack remains capped at999. This is a finite GBA inventory, not unlimited storage.

The previous 450-stack Bag had 150 Items, 60 Key Items, 32 Balls, 128 TMs/HMs and 80 Berries slots. The larger shared pool avoids five oversized arrays and retains the existing heap. Menu counts, selected positions and swap markers now cover the full pool, with list IDs proportional to owned stacks and one scratch name formatted only when a row is drawn. This keeps the full bag usable alongside battle memory. PC Item Storage and facility-specific rules remain separate.

## Save format and migration

The new packed storage header uses magic0x4C504333 (LPC3). The unchanged0x4C504332 LPC2 decoder recognizes the exact old inventory width, validates its checksum, copies the old encrypted bag to scratch, relocates PC items and imports all five pockets in enum order. The original fourteen-box migration still reads the original native inventory arrays. Published SaveBlock1, SaveBlock2, SaveBlock3 and all item/quest/story identifiers retain their v0.0.78 layouts and values.

New shared-pocket lengths are bounded against the total pool before use or save. Current and old raw widths are explicit; unknown or malformed packed data fail. Newer saves are not promised to load in an older ROM. Keep normal battery-save upgrade backups as described in SAVE-COMPATIBILITY.md.

## Verification

The production-C regression tests all five pockets at full shared capacity, allocation refusal, cross-pocket preservation, sorting/swapping, positions above255, repeated actual save relocation/re-encryption (with a failing pre-fix negative control), exact multi-stack quantity removal, old native and LPC2 migration, current save/reload and malformed-size refusal under address/undefined sanitizers. The existing codec and sector tests remain required.

The extended existing native suite prepares a 600-stack bag, selects slot599 with the actual menu, saves to native flash and reloads. It also derives a format-identical LPC2 battery fixture from a 450-stack native seed. Unmodified Release must Continue both fixtures, inspect all pocket counts/quantities, select slot599/149, save through controller input, reset and Continue again. The LPC2 fixture also retains the Treat Case Key Item and all 40 Poffin records across the upgrade and reload. Fixtures are controlled and private; they are not authentic historical-owner saves. See [release evidence](../qa/shared-bag-v0.0.79.json) for the integrated verification. Native APCS places slots at byte12 (Bag size 4620); private fixtures obtain this from the compiled structure rather than assuming host padding. No new screenshots are requested for this capacity change.
