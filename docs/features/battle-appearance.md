# Prepared battle appearance — v0.0.44

Battle backs use fixed clothing. Overworld/front portraits still use the full wardrobe. Selected skin tone remains active in battle. The ten supplied female sheets map directly to saved hairstyle IDs 1–10, matching Pixie through Twin Braids. Original (0) and male battle backs use native Emerald graphics. Male prepared sheets are not included in this revision.

## Authoring and palettes

`tools/legends/battle_sheets.json` is the name/ID/source manifest. Original uploads live under `graphics/legends/battle_sources`. `import_battle_sheets.py` extracts the Natural-row character component from each source cell, removes the presentation background/grid and detached illustration Ball, samples into fixed 64x64 frames with shared pose anchors, and emits native tiled 4bpp graphics. No generative reconstruction is used. The supplied sheets are RGB presentation artwork rather than directly indexed native sheets, so native-resolution sampling and palette reduction are required.

The generated indexed source sheets and 81920-byte frame bank are in `graphics/legends/battle_may`. Semantic slots 1–3 belong exclusively to skin; 4–7 belong to hair. The remaining colors belong to gloves, fixed red clothing, belt and dark outlines. Eight independent hair ramps retain the game's existing Natural, Black, Dark Brown, Chestnut, Auburn, Honey, Blond and Silver choices. The fixed skin ramps reuse the existing five skin-tone values.

Native Hoenn animation expects wind-up, cast, release and idle at indices 0,1,2,3. Store the supplied source frames 2,3,4,1 in that order. Emerald continues to animate the moving Ball separately; no static duplicate Ball is embedded in a trainer frame.

## Runtime connection

`legends_battle_appearance.c` supplies current back images/palettes through the native `GetTrainerBackPicImage` and `GetTrainerBackPicPalette` helpers. Both the sprite constructor and buffer-copy path use the same fixed art. Battle palettes are rebuilt from current staged/saved appearance settings on each request, so wardrobe Apply, Cancel and later save reloads use the authoritative current choices. There is no cached stale hairstyle.

Battle choices ignore outfit/accessory/costume IDs when choosing the fixed uniform. They retain the correct trainer gender. Non-Legends trainer IDs fall back to their native art/palette. Front portraits and field compositors keep their existing behavior, including the approved May shoulder cleanup.

## Validation

The prepared-sprite regression regenerates the checked-in art and runs the actual C image/palette selector across all ten cuts, eight hair colors and five skin tones. It checks stable hairstyle IDs, frame sizes, native routing, fixed uniforms for every wardrobe trainer ID, independent non-skin colors and a simulated wardrobe cut/color/tone change. Existing footwear, appearance, intro-hair, wardrobe and sprite-mask regressions also apply. Native build/emulator evidence will be recorded after validation.
