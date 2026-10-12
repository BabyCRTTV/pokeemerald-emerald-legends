# Appearance review — v0.0.40

Reviewed the final compiled Debug ROM in native mGBA 0.10.2.

- Entered New Game through the native main menu and used ordinary button input for both genders. Browsed all eleven hairstyles and all eight color choices, checked the five-row viewport and exact staged values, then confirmed into outfits and returned with B to the retained color.
- Used the native New Game initializer and a controlled native map warp to each player's bedroom, skipping story positioning for this focused review. Opened the wardrobe by facing the real storage box and pressing A. This tested the furniture/script entry rather than calling the wardrobe screen directly.
- Opened HAIRSTYLE with Left/Right and HAIR COLOR with A, scrolled the actual lists, confirmed pending selections, previewed Navy and Winter, and selected APPLY. The native return-to-field reload displayed the new hairstyle, Chestnut color and Winter coat.
- Applied every hairstyle through the wardrobe and rendered it facing back, right, front and left in the bedroom: 88 field captures across both genders. Inspected full skull/nape continuity, including the short male cuts and female tied styles.
- Used the native pause menu to Save, reset the emulator, chose Continue from the real saved-game menu, and checked the stored packed hairstyle/color value. Both genders retained hairstyle 10 with Chestnut (code 43) and returned to the bedroom successfully. Flash save files remain private test data.
- Actual-C regressions cover all 212 native animation-table poses, occupied skull/nape pixels, long-sleeve coverage outside protected face/glove/ball pixels, all 88 hair/color codes, old 0–10 values, Apply/Cancel/New Game handoff, list boundaries, footwear caches and isolated hair/skin/eye/coat palettes.

## Evidence

- `male-field-hairstyles-v0.0.40.png` and `female-field-hairstyles-v0.0.40.png`: cropped native field captures, enlarged 4x, with one row per saved hairstyle ID and four directions.
- `intro-mgba-v0.0.40.png`: native gender-specific hairstyle lists and previews, enlarged 3x.
- `hair-colors-mgba-v0.0.40.png`: native selected-color previews for both genders, enlarged 2x. Natural is the starting choice; the seven additional colors are shown.
- `wardrobe-mgba-v0.0.40.png`: native hairstyle lists, Navy and dark-green Winter portraits, enlarged 3x.
- `persistence-mgba-v0.0.40.png`: native Apply return, Continue menu and field after reload, enlarged 3x.
- `wardrobe-v0.0.40.png` and `wardrobe-actions-v0.0.40.png`: authoring sprite renders, not emulator screenshots.

The map-entry shortcut only prepared the scene. Wardrobe interaction, scrolling, Apply, field turning, Save and Continue used native game paths and button input. This review does not claim a complete gameplay traversal of every bike, Surf, field action, reflection or battle throw; those poses received structural and authoring-render checks. The same source builds Release and Debug, with the normal release workflow compiling both and verifying each BPS by reapplying and byte-comparing it with its compiled target. No complete ROM is committed or distributed.
