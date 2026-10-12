# Appearance review — v0.0.39

Reviewed with the compiled Debug ROM in mGBA 0.10.2.

- Entered New Game through the native main menu, selected each gender and skin tone, and browsed all eleven hairstyles with real button input. Verified each staged hairstyle ID, the five-row viewport, the final choice, confirmation into outfits and return to the retained selection.
- Entered the native wardrobe callback with staged intro choices. Verified its six-row HAIR list, both gender previews, Winter coat with brown boots, and return to the main wardrobe rows.
- Compared the exact rendered head/face RGB crop between Crimson and Ocean scarves: byte-identical for both genders.
- Actual-C regressions cover all 212 native animation-table poses, native eye-border pixels, hair/coat composition, footwear/cache behavior and 900 hair/scarf/coat/skin palette combinations.

## Evidence

`intro-preview-v0.0.39.png`, `hair-list-preview-v0.0.39.png` and `wardrobe-preview-v0.0.39.png` combine actual mGBA captures, with each screen enlarged by an integer factor of three.

`wardrobe-v0.0.39.png` and `wardrobe-actions-v0.0.39.png` are authoring renders rather than emulator captures.

The New Game review used ordinary menu input after controlled native main-menu entry. The wardrobe review used controlled native callback entry. Full overworld traversal and save/load were not repeated for this art revision. No complete ROM is distributed. Both variants require the established green build and BPS byte-for-byte verification workflow.
