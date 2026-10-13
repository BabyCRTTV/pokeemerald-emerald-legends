# Shared male portrait repair — draft

The current v0.0.46 front hair masks differ from the newly approved overworld and battle art. Trainer Card, wardrobe and Birch's intro share these portraits. Broad outfit color masks also repaint strap/cuff materials.

This draft imports only hair from `graphics/legends/male_front/generated-reference.png`, generated from the native Emerald front sprite and the owner's supplied trainer reference. The prompt requests ten named cuts in a 5×2 sheet, identical native anatomy/pose/outfit, connected pixel clusters, complete scalp coverage and the white/green Curls cap. The built-in image generation tool was used; its interface does not expose a selectable model ID. `manifest.json` records its hash and native-eye registration. Native indexed source supplies all anatomy and props. Curls keeps the original connected cap panel.

`build_male_front.py` authors ten 64×24 head regions, thirty 64×64 body banks (five outfits, three coats, scarf off/on), and native shoe/boot masks. Runtime material IDs keep skin, hair, eyes and clothing independent before packing to 4bpp. Clothing uses a deterministic five-slot palette with stable native eye blue/white/black; closest native clothing shades may be merged to fit the GBA's 16-color limit. Palette selection excludes changing hair/skin colors. This reduces the palette conflicts while retaining saved wardrobe IDs and native geometry.

The renderer reuses the existing 2,308-byte male front-picture buffer and 2,048-byte scratch buffer. The intro now obtains its palette through the same front helper as wardrobe and Trainer Card. The untouched Original with no accessory/outfit/color changes, female front art, fixed costumes, NPC art and every approved world/battle asset retain their existing paths.

Validation: the actual C renderer passes 720 outfit/coat/scarf/shoe configurations (plus hair/color cross-checks), 440 hair/color/skin choices, eye/material isolation, stable wardrobe colors, cached refresh and literal LZ decoding. Existing appearance settings, intro, wardrobe, sparse style layers, footwear and prepared battle tests pass. The compact review sheet decodes compiled host-C buffers; it is not an emulator screenshot. Both native ROM builds and BPS reapplication are checked by the existing PR workflow before this draft can be called build-ready. No exhaustive emulator playthrough is claimed.

Status: awaiting visual approval. Root VERSION and published v0.0.46 downloads stay unchanged until approval. The existing pending male overworld Side Part is outside this repair. Review sheet: [male-front-repair-preview.png](male-front-repair-preview.png).

